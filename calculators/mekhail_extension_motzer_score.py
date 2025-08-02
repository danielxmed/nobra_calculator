"""
Mekhail Extension of the Motzer Score Calculator

Predicts survival of metastatic renal cell carcinoma (mRCC) using clinical and laboratory parameters.
The Mekhail extension adds prior radiotherapy and number of metastatic sites to the original Motzer score.

References:
1. Mekhail TM, et al. J Clin Oncol. 2005;23(4):832-41.
2. Motzer RJ, et al. J Clin Oncol. 1999;17(8):2530-40.
"""

from typing import Dict, Any


class MekhailExtensionMotzerScoreCalculator:
    """Calculator for Mekhail Extension of the Motzer Score"""
    
    def __init__(self):
        # Survival data by risk group (in months)
        self.SURVIVAL_DATA = {
            "favorable": 28,
            "intermediate": 14,
            "poor": 5
        }
    
    def calculate(self, ldh_elevated: str, hemoglobin_low: str, corrected_calcium_high: str,
                  time_to_treatment_less_than_1_year: str, prior_radiotherapy: str,
                  metastatic_sites_2_or_more: str) -> Dict[str, Any]:
        """
        Calculates the Mekhail Extension of the Motzer Score for mRCC prognosis
        
        Args:
            ldh_elevated (str): LDH > 1.5x upper limit of normal ("yes"/"no")
            hemoglobin_low (str): Hemoglobin < lower limit of normal ("yes"/"no")
            corrected_calcium_high (str): Corrected calcium > 10 mg/dL ("yes"/"no")
            time_to_treatment_less_than_1_year (str): Time from diagnosis to treatment < 1 year ("yes"/"no")
            prior_radiotherapy (str): Prior radiation therapy ("yes"/"no")
            metastatic_sites_2_or_more (str): ≥2 sites of metastasis ("yes"/"no")
            
        Returns:
            Dict with the score, risk category, and survival prognosis
        """
        
        # Validate inputs
        self._validate_inputs(ldh_elevated, hemoglobin_low, corrected_calcium_high,
                             time_to_treatment_less_than_1_year, prior_radiotherapy,
                             metastatic_sites_2_or_more)
        
        # Calculate score - each risk factor contributes 1 point
        score = 0
        
        if ldh_elevated == "yes":
            score += 1
        if hemoglobin_low == "yes":
            score += 1
        if corrected_calcium_high == "yes":
            score += 1
        if time_to_treatment_less_than_1_year == "yes":
            score += 1
        if prior_radiotherapy == "yes":
            score += 1
        if metastatic_sites_2_or_more == "yes":
            score += 1
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ldh_elevated: str, hemoglobin_low: str, corrected_calcium_high: str,
                        time_to_treatment_less_than_1_year: str, prior_radiotherapy: str,
                        metastatic_sites_2_or_more: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        parameters = {
            "ldh_elevated": ldh_elevated,
            "hemoglobin_low": hemoglobin_low,
            "corrected_calcium_high": corrected_calcium_high,
            "time_to_treatment_less_than_1_year": time_to_treatment_less_than_1_year,
            "prior_radiotherapy": prior_radiotherapy,
            "metastatic_sites_2_or_more": metastatic_sites_2_or_more
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got '{param_value}'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the score
        
        Args:
            score (int): Calculated Mekhail score (0-6)
            
        Returns:
            Dict with risk category, description, and clinical interpretation
        """
        
        if score <= 1:
            return {
                "stage": "Favorable Risk",
                "description": "0-1 risk factors",
                "interpretation": (
                    f"Favorable risk group with median survival of {self.SURVIVAL_DATA['favorable']} months. "
                    "These patients have the best prognosis and may be candidates for less aggressive "
                    "treatment approaches or observation in some cases."
                )
            }
        elif score == 2:
            return {
                "stage": "Intermediate Risk",
                "description": "2 risk factors",
                "interpretation": (
                    f"Intermediate risk group with median survival of {self.SURVIVAL_DATA['intermediate']} months. "
                    "These patients require active treatment and close monitoring."
                )
            }
        else:  # score >= 3
            return {
                "stage": "Poor Risk",
                "description": "≥3 risk factors",
                "interpretation": (
                    f"Poor risk group with median survival of {self.SURVIVAL_DATA['poor']} months. "
                    "These patients have the worst prognosis and may benefit from aggressive systemic "
                    "therapy or clinical trial enrollment."
                )
            }


def calculate_mekhail_extension_motzer_score(ldh_elevated: str, hemoglobin_low: str, 
                                            corrected_calcium_high: str, time_to_treatment_less_than_1_year: str,
                                            prior_radiotherapy: str, metastatic_sites_2_or_more: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MekhailExtensionMotzerScoreCalculator()
    return calculator.calculate(ldh_elevated, hemoglobin_low, corrected_calcium_high,
                               time_to_treatment_less_than_1_year, prior_radiotherapy,
                               metastatic_sites_2_or_more)