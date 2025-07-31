"""
HAS-BLED Score for Major Bleeding Risk Calculator

Estimates 1-year risk of major bleeding for patients on anticoagulation to assess
quality of atrial fibrillation care. Used with CHA2DS2-VASc score to balance
stroke vs bleeding risk.

References:
1. Pisters R, et al. Chest. 2010;138(5):1093-100.
2. Lip GY, et al. J Am Coll Cardiol. 2011;57(2):173-80.
"""

from typing import Dict, Any


class HasBledScoreCalculator:
    """Calculator for HAS-BLED Score for Major Bleeding Risk"""
    
    def __init__(self):
        # Risk percentages based on score
        self.RISK_PERCENTAGES = {
            0: "0.9-1.3%",
            1: "1.3-3.4%",
            2: "4.1%",
            3: "5.8%",
            4: "8.7%",
            5: "9.1%",
            6: ">10%",
            7: ">10%",
            8: ">10%",
            9: ">10%"
        }
    
    def calculate(self, hypertension: str, abnormal_renal_function: str,
                  abnormal_liver_function: str, stroke_history: str,
                  bleeding_history: str, labile_inr: str, elderly: str,
                  drugs: str, alcohol: str) -> Dict[str, Any]:
        """
        Calculates the HAS-BLED score using the provided parameters
        
        Args:
            hypertension (str): "no" or "yes" - uncontrolled, >160 mmHg systolic
            abnormal_renal_function (str): "no" or "yes" - dialysis, transplant, Cr >2.26
            abnormal_liver_function (str): "no" or "yes" - cirrhosis or elevated enzymes
            stroke_history (str): "no" or "yes" - previous stroke
            bleeding_history (str): "no" or "yes" - major bleeding or predisposition
            labile_inr (str): "no" or "yes" - unstable INR, TTR <60%
            elderly (str): "no" or "yes" - age >65
            drugs (str): "no" or "yes" - antiplatelet agents, NSAIDs
            alcohol (str): "no" or "yes" - ≥8 drinks per week
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(hypertension, abnormal_renal_function,
                            abnormal_liver_function, stroke_history,
                            bleeding_history, labile_inr, elderly,
                            drugs, alcohol)
        
        # Calculate HAS-BLED score - each positive factor adds 1 point
        score = 0
        
        # H - Hypertension
        if hypertension == "yes":
            score += 1
            
        # A - Abnormal renal/liver function (max 2 points - 1 for each)
        if abnormal_renal_function == "yes":
            score += 1
        if abnormal_liver_function == "yes":
            score += 1
            
        # S - Stroke history
        if stroke_history == "yes":
            score += 1
            
        # B - Bleeding history or predisposition
        if bleeding_history == "yes":
            score += 1
            
        # L - Labile INR
        if labile_inr == "yes":
            score += 1
            
        # E - Elderly (>65)
        if elderly == "yes":
            score += 1
            
        # D - Drugs/alcohol (max 2 points - 1 for each)
        if drugs == "yes":
            score += 1
        if alcohol == "yes":
            score += 1
        
        # Get interpretation and risk percentage
        interpretation = self._get_interpretation(score)
        risk_percentage = self.RISK_PERCENTAGES.get(score, ">10%")
        
        # Add risk percentage to interpretation
        full_interpretation = interpretation["interpretation"].replace(
            "per year)",
            f"per year, estimated {risk_percentage})"
        )
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": full_interpretation,
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates all input parameters are yes/no"""
        
        valid_options = ["yes", "no"]
        param_names = [
            "hypertension", "abnormal_renal_function", "abnormal_liver_function",
            "stroke_history", "bleeding_history", "labile_inr", "elderly",
            "drugs", "alcohol"
        ]
        
        for value, name in zip(args, param_names):
            if value not in valid_options:
                raise ValueError(f"{name} must be one of: {', '.join(valid_options)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the HAS-BLED score
        
        Args:
            score (int): Calculated HAS-BLED score (0-9)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Low bleeding risk",
                "interpretation": (
                    "Low risk of major bleeding (0.9-3.4% per year). Anticoagulation should be "
                    "considered if indicated. Regular monitoring and attention to modifiable risk "
                    "factors recommended."
                )
            }
        elif score == 2:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate bleeding risk",
                "interpretation": (
                    "Moderate risk of major bleeding (approximately 4.1% per year). Caution with "
                    "anticoagulation, but do not necessarily withhold treatment. Address modifiable "
                    "risk factors (hypertension, labile INR, concomitant drugs)."
                )
            }
        else:  # score >= 3
            return {
                "stage": "High Risk",
                "description": "High bleeding risk",
                "interpretation": (
                    "High risk of major bleeding (5.8% to >10% per year). Requires regular clinical "
                    "review and careful monitoring if anticoagulated. Address all modifiable risk "
                    "factors. Consider alternatives to anticoagulation if appropriate. Do not use "
                    "score alone to withhold anticoagulation."
                )
            }


def calculate_has_bled_score(hypertension: str, abnormal_renal_function: str,
                            abnormal_liver_function: str, stroke_history: str,
                            bleeding_history: str, labile_inr: str, elderly: str,
                            drugs: str, alcohol: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HasBledScoreCalculator()
    return calculator.calculate(hypertension, abnormal_renal_function,
                              abnormal_liver_function, stroke_history,
                              bleeding_history, labile_inr, elderly,
                              drugs, alcohol)