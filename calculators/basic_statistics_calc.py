"""
Basic Statistics Calculator

Calculates common epidemiological values for diagnostic tests and treatments.

References (Vancouver style):
1. Altman DG, Bland JM. Diagnostic tests. 1: Sensitivity and specificity. BMJ. 1994 Jun 11;308(6943):1552.
2. Van der Helm HJ, Hische EA. Application of Bayes's theorem to results of quantitative clinical chemical determinations. Clin Chem. 1979 Jun;25(6):985-8.
3. Akobeng AK. Understanding diagnostic tests 1: sensitivity, specificity and predictive values. Acta Paediatr. 2007 Mar;96(3):338-41.
4. Laupacis A, Sackett DL, Roberts RS. An assessment of clinically useful measures of the consequences of treatment. N Engl J Med. 1988 Jun 30;318(26):1728-33.
"""

import math
from typing import Dict, Any, Optional


class BasicStatisticsCalcCalculator:
    """Calculator for Basic Statistics"""
    
    def calculate(self, calculation_type: str, input_method: Optional[str] = None,
                  prevalence: Optional[float] = None, sensitivity: Optional[float] = None,
                  specificity: Optional[float] = None, true_positive: Optional[int] = None,
                  false_positive: Optional[int] = None, false_negative: Optional[int] = None,
                  true_negative: Optional[int] = None, experimental_with_outcome: Optional[int] = None,
                  experimental_without_outcome: Optional[int] = None, control_with_outcome: Optional[int] = None,
                  control_without_outcome: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates statistics based on the type of calculation requested
        
        Args:
            calculation_type: 'diagnostic_test' or 'treatment'
            Various parameters depending on calculation type
            
        Returns:
            Dict with comprehensive statistical results
        """
        
        if calculation_type == "diagnostic_test":
            return self._calculate_diagnostic_test(
                input_method, prevalence, sensitivity, specificity,
                true_positive, false_positive, false_negative, true_negative
            )
        elif calculation_type == "treatment":
            return self._calculate_treatment(
                experimental_with_outcome, experimental_without_outcome,
                control_with_outcome, control_without_outcome
            )
        else:
            raise ValueError("Invalid calculation_type. Must be 'diagnostic_test' or 'treatment'")
    
    def _calculate_diagnostic_test(self, input_method: Optional[str], prevalence: Optional[float],
                                   sensitivity: Optional[float], specificity: Optional[float],
                                   tp: Optional[int], fp: Optional[int], fn: Optional[int],
                                   tn: Optional[int]) -> Dict[str, Any]:
        """Calculates diagnostic test statistics"""
        
        # Determine calculation method based on input
        if input_method == "rates" or (prevalence is not None and sensitivity is not None and specificity is not None):
            # Convert percentages to decimals
            prev = prevalence / 100.0
            sens = sensitivity / 100.0
            spec = specificity / 100.0
            
            # Calculate using Bayes' theorem
            ppv = (sens * prev) / ((sens * prev) + ((1 - spec) * (1 - prev)))
            npv = (spec * (1 - prev)) / (((1 - sens) * prev) + (spec * (1 - prev)))
            
            # Calculate likelihood ratios
            lr_positive = sens / (1 - spec) if spec < 1 else float('inf')
            lr_negative = (1 - sens) / spec if spec > 0 else 0
            
            # Pre and post-test odds
            pre_test_odds = prev / (1 - prev)
            post_test_odds_positive = pre_test_odds * lr_positive
            post_test_odds_negative = pre_test_odds * lr_negative
            
            # Post-test probabilities
            post_test_prob_positive = post_test_odds_positive / (1 + post_test_odds_positive)
            post_test_prob_negative = post_test_odds_negative / (1 + post_test_odds_negative)
            
            return {
                "result": {
                    "prevalence": round(prevalence, 2),
                    "sensitivity": round(sensitivity, 2),
                    "specificity": round(specificity, 2),
                    "positive_predictive_value": round(ppv * 100, 2),
                    "negative_predictive_value": round(npv * 100, 2),
                    "positive_likelihood_ratio": round(lr_positive, 2),
                    "negative_likelihood_ratio": round(lr_negative, 2),
                    "pre_test_probability": round(prevalence, 2),
                    "post_test_probability_positive": round(post_test_prob_positive * 100, 2),
                    "post_test_probability_negative": round(post_test_prob_negative * 100, 2)
                },
                "unit": "percent/ratio",
                "interpretation": self._interpret_diagnostic_test(sens, spec, ppv, npv, lr_positive, lr_negative)
            }
            
        elif tp is not None and fp is not None and fn is not None and tn is not None:
            # Calculate from counts
            total_diseased = tp + fn
            total_healthy = fp + tn
            total = total_diseased + total_healthy
            
            if total == 0:
                raise ValueError("Total count cannot be zero")
            
            # Calculate metrics
            prevalence = (total_diseased / total) * 100
            sensitivity = (tp / total_diseased) * 100 if total_diseased > 0 else 0
            specificity = (tn / total_healthy) * 100 if total_healthy > 0 else 0
            ppv = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
            npv = (tn / (tn + fn)) * 100 if (tn + fn) > 0 else 0
            accuracy = ((tp + tn) / total) * 100
            
            # Likelihood ratios
            lr_positive = (tp / total_diseased) / (fp / total_healthy) if fp > 0 and total_healthy > 0 else float('inf')
            lr_negative = (fn / total_diseased) / (tn / total_healthy) if tn > 0 and total_healthy > 0 and total_diseased > 0 else 0
            
            return {
                "result": {
                    "true_positive": tp,
                    "false_positive": fp,
                    "false_negative": fn,
                    "true_negative": tn,
                    "total": total,
                    "prevalence": round(prevalence, 2),
                    "sensitivity": round(sensitivity, 2),
                    "specificity": round(specificity, 2),
                    "positive_predictive_value": round(ppv, 2),
                    "negative_predictive_value": round(npv, 2),
                    "accuracy": round(accuracy, 2),
                    "positive_likelihood_ratio": round(lr_positive, 2),
                    "negative_likelihood_ratio": round(lr_negative, 2)
                },
                "unit": "percent/ratio",
                "interpretation": self._interpret_diagnostic_test(
                    sensitivity/100, specificity/100, ppv/100, npv/100, lr_positive, lr_negative
                )
            }
        else:
            raise ValueError("Invalid input parameters for diagnostic test calculation")
    
    def _calculate_treatment(self, a: Optional[int], b: Optional[int], 
                            c: Optional[int], d: Optional[int]) -> Dict[str, Any]:
        """Calculates treatment effectiveness statistics"""
        
        if None in [a, b, c, d]:
            raise ValueError("All treatment parameters (A, B, C, D) must be provided")
        
        # Total patients in each group
        experimental_total = a + b
        control_total = c + d
        
        if experimental_total == 0 or control_total == 0:
            raise ValueError("Total patients in experimental or control group cannot be zero")
        
        # Event rates
        eer = a / experimental_total  # Experimental Event Rate
        cer = c / control_total        # Control Event Rate
        
        # Risk measures
        rr = eer / cer if cer > 0 else float('inf')  # Relative Risk
        arr = eer - cer  # Absolute Risk Reduction (can be negative)
        rrr = (eer - cer) / cer * 100 if cer > 0 else 0  # Relative Risk Reduction
        
        # Odds ratio
        odds_experimental = a / b if b > 0 else float('inf')
        odds_control = c / d if d > 0 else float('inf')
        or_value = odds_experimental / odds_control if odds_control > 0 else float('inf')
        
        # Number Needed to Treat
        nnt = 1 / abs(arr) if arr != 0 else float('inf')
        
        # Confidence intervals (95%) for RR and OR using log transformation
        if a > 0 and b > 0 and c > 0 and d > 0:
            # Log RR standard error
            se_log_rr = math.sqrt(1/a - 1/experimental_total + 1/c - 1/control_total)
            log_rr = math.log(rr)
            rr_ci_lower = math.exp(log_rr - 1.96 * se_log_rr)
            rr_ci_upper = math.exp(log_rr + 1.96 * se_log_rr)
            
            # Log OR standard error
            se_log_or = math.sqrt(1/a + 1/b + 1/c + 1/d)
            log_or = math.log(or_value)
            or_ci_lower = math.exp(log_or - 1.96 * se_log_or)
            or_ci_upper = math.exp(log_or + 1.96 * se_log_or)
        else:
            rr_ci_lower = rr_ci_upper = None
            or_ci_lower = or_ci_upper = None
        
        return {
            "result": {
                "experimental_event_rate": round(eer * 100, 2),
                "control_event_rate": round(cer * 100, 2),
                "relative_risk": round(rr, 3),
                "relative_risk_ci": f"({round(rr_ci_lower, 3)} - {round(rr_ci_upper, 3)})" if rr_ci_lower else "N/A",
                "odds_ratio": round(or_value, 3),
                "odds_ratio_ci": f"({round(or_ci_lower, 3)} - {round(or_ci_upper, 3)})" if or_ci_lower else "N/A",
                "absolute_risk_reduction": round(arr * 100, 2),
                "relative_risk_reduction": round(rrr, 2),
                "number_needed_to_treat": round(nnt, 1) if nnt != float('inf') else "∞"
            },
            "unit": "percent/ratio",
            "interpretation": self._interpret_treatment(rr, or_value, arr, nnt)
        }
    
    def _interpret_diagnostic_test(self, sens: float, spec: float, ppv: float, 
                                  npv: float, lr_pos: float, lr_neg: float) -> str:
        """Provides interpretation for diagnostic test results"""
        
        interpretation = []
        
        # Sensitivity interpretation
        if sens >= 0.95:
            interpretation.append("Very high sensitivity (≥95%): Excellent for ruling out disease when negative.")
        elif sens >= 0.90:
            interpretation.append("High sensitivity (90-94%): Good for ruling out disease when negative.")
        elif sens >= 0.80:
            interpretation.append("Moderate sensitivity (80-89%): Reasonable for screening.")
        else:
            interpretation.append("Low sensitivity (<80%): Limited ability to rule out disease.")
        
        # Specificity interpretation
        if spec >= 0.95:
            interpretation.append("Very high specificity (≥95%): Excellent for ruling in disease when positive.")
        elif spec >= 0.90:
            interpretation.append("High specificity (90-94%): Good for ruling in disease when positive.")
        elif spec >= 0.80:
            interpretation.append("Moderate specificity (80-89%): Reasonable for confirmation.")
        else:
            interpretation.append("Low specificity (<80%): Limited ability to rule in disease.")
        
        # Likelihood ratio interpretation
        if lr_pos > 10:
            interpretation.append("LR+ >10: Large and often conclusive increase in disease likelihood.")
        elif lr_pos > 5:
            interpretation.append("LR+ 5-10: Moderate increase in disease likelihood.")
        elif lr_pos > 2:
            interpretation.append("LR+ 2-5: Small increase in disease likelihood.")
        
        if lr_neg < 0.1:
            interpretation.append("LR- <0.1: Large and often conclusive decrease in disease likelihood.")
        elif lr_neg < 0.2:
            interpretation.append("LR- 0.1-0.2: Moderate decrease in disease likelihood.")
        elif lr_neg < 0.5:
            interpretation.append("LR- 0.2-0.5: Small decrease in disease likelihood.")
        
        return " ".join(interpretation)
    
    def _interpret_treatment(self, rr: float, or_value: float, arr: float, nnt: float) -> str:
        """Provides interpretation for treatment results"""
        
        interpretation = []
        
        # Relative risk interpretation
        if rr > 1:
            interpretation.append(f"RR = {rr:.2f}: Treatment increases risk of outcome by {((rr-1)*100):.1f}%.")
        elif rr < 1:
            interpretation.append(f"RR = {rr:.2f}: Treatment reduces risk of outcome by {((1-rr)*100):.1f}%.")
        else:
            interpretation.append("RR = 1: No difference in risk between treatment and control.")
        
        # Absolute risk reduction
        if arr > 0:
            interpretation.append(f"ARR = {arr*100:.1f}%: Treatment increases absolute risk.")
        elif arr < 0:
            interpretation.append(f"ARR = {abs(arr)*100:.1f}%: Treatment reduces absolute risk.")
        
        # NNT interpretation
        if nnt != float('inf') and nnt > 0:
            if arr < 0:  # Beneficial treatment
                interpretation.append(f"NNT = {nnt:.0f}: Need to treat {nnt:.0f} patients to prevent one adverse outcome.")
            else:  # Harmful treatment
                interpretation.append(f"NNH = {nnt:.0f}: One additional adverse outcome for every {nnt:.0f} patients treated.")
        
        return " ".join(interpretation)


def calculate_basic_statistics_calc(**kwargs) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BasicStatisticsCalcCalculator()
    return calculator.calculate(**kwargs)