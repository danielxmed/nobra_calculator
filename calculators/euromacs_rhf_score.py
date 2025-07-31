"""
EUROMACS-RHF Score Calculator

Determines risk of right ventricular heart failure in patients after left ventricular assist device (LVAD) implantation.

References:
1. Soliman OII, Akin S, Muslem R, Boersma E, Manintveld OC, Krabatsch T, et al. Derivation and 
   Validation of a Novel Right-Sided Heart Failure Model After Implantation of Continuous Flow 
   Left Ventricular Assist Devices: The EUROMACS (European Registry for Patients with Mechanical 
   Circulatory Support) Right-Sided Heart Failure Risk Score. Circulation. 2018 Mar 6;137(9):891-906. 
   doi: 10.1161/CIRCULATIONAHA.117.030543.
2. Bellavia D, Iacovoni A, Scardulla C, Moja L, Pilato M, Kushwaha SS, et al. Prediction of right 
   heart failure after left ventricular assist device implantation. Eur Heart J Acute Cardiovasc Care. 
   2017 Dec;6(8):668-676. doi: 10.1177/2048872615612455.
"""

from typing import Dict, Any


class EuromacsRhfScoreCalculator:
    """Calculator for EUROMACS-RHF Score"""
    
    def __init__(self):
        """Initialize calculator with scoring constants"""
        # Scoring weights for each parameter
        self.SCORING_WEIGHTS = {
            "ra_pcwp_ratio_elevated": 2.0,  # RA/PCWP >0.54
            "hemoglobin_low": 1.0,           # Hemoglobin ≤10 g/dL
            "multiple_inotropes": 2.5,       # Multiple IV inotropes (highest weight)
            "intermacs_class_low": 2.0,      # INTERMACS Class 1-3
            "severe_rv_dysfunction": 2.0     # Severe RV dysfunction
        }
        
        # Risk thresholds
        self.RISK_THRESHOLDS = {
            "low": (0, 2),         # 0-2 points: 11% RHF incidence
            "intermediate": (2.5, 4),  # 2.5-4 points: intermediate risk
            "high": (4.5, 9.5)     # 4.5-9.5 points: 43.1% RHF incidence
        }
    
    def calculate(self, ra_pcwp_ratio_elevated: str, hemoglobin_low: str, 
                 multiple_inotropes: str, intermacs_class_low: str, 
                 severe_rv_dysfunction: str) -> Dict[str, Any]:
        """
        Calculates EUROMACS-RHF Score for right heart failure risk after LVAD implantation
        
        Args:
            ra_pcwp_ratio_elevated (str): RA/PCWP ratio >0.54 (yes/no)
            hemoglobin_low (str): Hemoglobin ≤10 g/dL (yes/no)
            multiple_inotropes (str): Multiple intravenous inotropes (yes/no)
            intermacs_class_low (str): INTERMACS Class 1-3 (yes/no)
            severe_rv_dysfunction (str): Severe RV dysfunction by echo (yes/no)
            
        Returns:
            Dict with score, risk stratification, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(ra_pcwp_ratio_elevated, hemoglobin_low, multiple_inotropes,
                            intermacs_class_low, severe_rv_dysfunction)
        
        # Calculate total score
        score = self._calculate_score(ra_pcwp_ratio_elevated, hemoglobin_low, 
                                    multiple_inotropes, intermacs_class_low, 
                                    severe_rv_dysfunction)
        
        # Get risk stratification
        risk_category = self._get_risk_category(score)
        
        # Get interpretation
        interpretation = self._get_interpretation(score, risk_category)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "risk_category": risk_category,
            "rhf_incidence": interpretation["incidence"],
            "score_breakdown": self._get_score_breakdown(ra_pcwp_ratio_elevated, hemoglobin_low,
                                                        multiple_inotropes, intermacs_class_low,
                                                        severe_rv_dysfunction)
        }
    
    def _validate_inputs(self, ra_pcwp_ratio_elevated: str, hemoglobin_low: str,
                        multiple_inotropes: str, intermacs_class_low: str,
                        severe_rv_dysfunction: str):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        parameters = {
            "ra_pcwp_ratio_elevated": ra_pcwp_ratio_elevated,
            "hemoglobin_low": hemoglobin_low,
            "multiple_inotropes": multiple_inotropes,
            "intermacs_class_low": intermacs_class_low,
            "severe_rv_dysfunction": severe_rv_dysfunction
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_responses:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_score(self, ra_pcwp_ratio_elevated: str, hemoglobin_low: str,
                        multiple_inotropes: str, intermacs_class_low: str,
                        severe_rv_dysfunction: str) -> float:
        """
        Calculates the total EUROMACS-RHF score
        
        Args:
            Parameters for each risk factor
            
        Returns:
            float: Total score (0-9.5 points)
        """
        
        score = 0.0
        
        # Add points for each positive risk factor
        if ra_pcwp_ratio_elevated == "yes":
            score += self.SCORING_WEIGHTS["ra_pcwp_ratio_elevated"]
        
        if hemoglobin_low == "yes":
            score += self.SCORING_WEIGHTS["hemoglobin_low"]
        
        if multiple_inotropes == "yes":
            score += self.SCORING_WEIGHTS["multiple_inotropes"]
        
        if intermacs_class_low == "yes":
            score += self.SCORING_WEIGHTS["intermacs_class_low"]
        
        if severe_rv_dysfunction == "yes":
            score += self.SCORING_WEIGHTS["severe_rv_dysfunction"]
        
        return score
    
    def _get_risk_category(self, score: float) -> str:
        """
        Determines risk category based on total score
        
        Args:
            score (float): Total EUROMACS-RHF score
            
        Returns:
            str: Risk category (Low Risk, Intermediate Risk, High Risk)
        """
        
        if score <= self.RISK_THRESHOLDS["low"][1]:
            return "Low Risk"
        elif score <= self.RISK_THRESHOLDS["intermediate"][1]:
            return "Intermediate Risk"
        else:
            return "High Risk"
    
    def _get_interpretation(self, score: float, risk_category: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on score and risk category
        
        Args:
            score (float): Total score
            risk_category (str): Risk category
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_category == "Low Risk":
            return {
                "stage": "Low Risk",
                "description": "Low risk for RHF",
                "incidence": "11%",
                "interpretation": (
                    f"EUROMACS-RHF Score: {score} points. LOW RISK of right heart failure "
                    f"after LVAD implantation (11% incidence). Standard perioperative monitoring "
                    f"and management recommended. Consider routine hemodynamic assessment "
                    f"post-LVAD implantation with standard protocols."
                )
            }
        elif risk_category == "Intermediate Risk":
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate risk for RHF",
                "incidence": "Intermediate",
                "interpretation": (
                    f"EUROMACS-RHF Score: {score} points. INTERMEDIATE RISK of right heart "
                    f"failure after LVAD implantation. Enhanced monitoring recommended. "
                    f"Consider closer hemodynamic surveillance, optimization of right ventricular "
                    f"support, and more frequent assessment of RV function post-operatively."
                )
            }
        else:  # High Risk
            return {
                "stage": "High Risk", 
                "description": "High risk for RHF",
                "incidence": "43.1%",
                "interpretation": (
                    f"EUROMACS-RHF Score: {score} points. HIGH RISK of right heart failure "
                    f"after LVAD implantation (43.1% incidence). Requires intensive monitoring "
                    f"and proactive management. Consider biventricular assist device or total "
                    f"heart support. Optimize hemodynamics pre-operatively and implement "
                    f"advanced RV support strategies. Expect prolonged ICU stay and increased "
                    f"mortality risk."
                )
            }
    
    def _get_score_breakdown(self, ra_pcwp_ratio_elevated: str, hemoglobin_low: str,
                           multiple_inotropes: str, intermacs_class_low: str,
                           severe_rv_dysfunction: str) -> Dict[str, float]:
        """
        Provides detailed breakdown of score components
        
        Returns:
            Dict with individual component contributions
        """
        
        breakdown = {
            "ra_pcwp_ratio_elevated": self.SCORING_WEIGHTS["ra_pcwp_ratio_elevated"] if ra_pcwp_ratio_elevated == "yes" else 0,
            "hemoglobin_low": self.SCORING_WEIGHTS["hemoglobin_low"] if hemoglobin_low == "yes" else 0,
            "multiple_inotropes": self.SCORING_WEIGHTS["multiple_inotropes"] if multiple_inotropes == "yes" else 0,
            "intermacs_class_low": self.SCORING_WEIGHTS["intermacs_class_low"] if intermacs_class_low == "yes" else 0,
            "severe_rv_dysfunction": self.SCORING_WEIGHTS["severe_rv_dysfunction"] if severe_rv_dysfunction == "yes" else 0
        }
        
        return breakdown


def calculate_euromacs_rhf_score(ra_pcwp_ratio_elevated: str, hemoglobin_low: str,
                                multiple_inotropes: str, intermacs_class_low: str,
                                severe_rv_dysfunction: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_euromacs_rhf_score pattern
    """
    calculator = EuromacsRhfScoreCalculator()
    return calculator.calculate(ra_pcwp_ratio_elevated, hemoglobin_low, multiple_inotropes,
                               intermacs_class_low, severe_rv_dysfunction)