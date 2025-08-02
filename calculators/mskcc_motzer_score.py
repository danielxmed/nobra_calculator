"""
MSKCC/Motzer Score Calculator

Predicts survival in metastatic renal cell carcinoma using clinical and laboratory data.
Developed at Memorial Sloan-Kettering Cancer Center.

References:
1. Motzer RJ, et al. J Clin Oncol. 1999;17(8):2530-40.
2. Motzer RJ, et al. J Clin Oncol. 2002;20(1):289-96.
3. Motzer RJ, et al. J Clin Oncol. 2004;22(3):454-63.
"""

from typing import Dict, Any


class MskccMotzerScoreCalculator:
    """Calculator for MSKCC/Motzer Score for Metastatic RCC"""
    
    def __init__(self):
        # Survival data by risk group (in months)
        self.SURVIVAL_DATA = {
            "good": 20,
            "intermediate": 10,
            "high": 4
        }
    
    def calculate(self, time_to_treatment_less_than_1_year: str, hemoglobin_low: str,
                  calcium_high: str, ldh_high: str, performance_status_low: str) -> Dict[str, Any]:
        """
        Calculates the MSKCC/Motzer Score for metastatic RCC prognosis
        
        Args:
            time_to_treatment_less_than_1_year (str): Time from diagnosis to treatment < 1 year ("yes"/"no")
            hemoglobin_low (str): Hemoglobin < LLN (Men <13.5, Women <12.0 g/dL) ("yes"/"no")
            calcium_high (str): Corrected calcium > 10 mg/dL ("yes"/"no")
            ldh_high (str): LDH > 1.5x ULN ("yes"/"no")
            performance_status_low (str): Karnofsky PS < 80% ("yes"/"no")
            
        Returns:
            Dict with the score, risk category, and survival prognosis
        """
        
        # Validate inputs
        self._validate_inputs(time_to_treatment_less_than_1_year, hemoglobin_low,
                             calcium_high, ldh_high, performance_status_low)
        
        # Calculate score - each risk factor contributes 1 point
        score = 0
        
        if time_to_treatment_less_than_1_year == "yes":
            score += 1
        if hemoglobin_low == "yes":
            score += 1
        if calcium_high == "yes":
            score += 1
        if ldh_high == "yes":
            score += 1
        if performance_status_low == "yes":
            score += 1
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "risk factors",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, time_to_treatment_less_than_1_year: str, hemoglobin_low: str,
                        calcium_high: str, ldh_high: str, performance_status_low: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        parameters = {
            "time_to_treatment_less_than_1_year": time_to_treatment_less_than_1_year,
            "hemoglobin_low": hemoglobin_low,
            "calcium_high": calcium_high,
            "ldh_high": ldh_high,
            "performance_status_low": performance_status_low
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got '{param_value}'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the score
        
        Args:
            score (int): Number of risk factors (0-5)
            
        Returns:
            Dict with risk category, description, and clinical interpretation
        """
        
        if score == 0:
            return {
                "stage": "Good Risk",
                "description": "0 risk factors",
                "interpretation": (
                    f"Good risk group with median survival of {self.SURVIVAL_DATA['good']} months. "
                    "These patients have the best prognosis and may be candidates for a variety "
                    "of treatment approaches including targeted therapy, immunotherapy, or clinical trials."
                )
            }
        elif score <= 2:
            return {
                "stage": "Intermediate Risk",
                "description": "1-2 risk factors",
                "interpretation": (
                    f"Intermediate risk group with median survival of {self.SURVIVAL_DATA['intermediate']} months. "
                    "These patients require active treatment with targeted therapy or immunotherapy. "
                    "Close monitoring is essential."
                )
            }
        else:  # score >= 3
            return {
                "stage": "High Risk",
                "description": "≥3 risk factors",
                "interpretation": (
                    f"High risk group with median survival of {self.SURVIVAL_DATA['high']} months. "
                    "These patients have poor prognosis and may benefit from aggressive systemic "
                    "therapy, clinical trial enrollment, or supportive care depending on overall condition."
                )
            }


def calculate_mskcc_motzer_score(time_to_treatment_less_than_1_year: str, hemoglobin_low: str,
                                 calcium_high: str, ldh_high: str, 
                                 performance_status_low: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MskccMotzerScoreCalculator()
    return calculator.calculate(time_to_treatment_less_than_1_year, hemoglobin_low,
                               calcium_high, ldh_high, performance_status_low)