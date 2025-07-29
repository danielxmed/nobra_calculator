"""
American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index Calculator

Calculates cardiovascular risk for patients undergoing noncardiac surgery using
6 easily obtainable clinical variables. Superior discriminatory power compared
to other risk indices like the Revised Cardiac Risk Index.

References:
- Dakik H, Chehab O, Eldirani M, et al. A New Index for Pre-Operative 
  Cardiovascular Evaluation. J Am Coll Cardiol. 2019;73(26):3067-3078.
- Dakik H, Sbaity E, Msheik A, et al. AUB-HAS2 Cardiovascular Risk Index: 
  Performance in Surgical Subpopulations and Comparison to the Revised Cardiac 
  Risk Index. J Am Heart Assoc. 2020;9(10):e016228.
"""

from typing import Dict, Any


class AubHas2CardiovascularRiskIndexCalculator:
    """Calculator for American University of Beirut HAS2 Cardiovascular Risk Index"""
    
    def __init__(self):
        # Each risk factor contributes 1 point to the total score
        self.RISK_FACTOR_POINTS = 1
        
    def calculate(self, history_heart_disease: str, age_75_or_older: str,
                 symptoms_angina_dyspnea: str, anemia_hgb_less_12: str,
                 vascular_surgery: str, emergency_surgery: str) -> Dict[str, Any]:
        """
        Calculates the AUB-HAS2 cardiovascular risk score
        
        Args:
            history_heart_disease (str): History of heart disease ("yes"/"no")
            age_75_or_older (str): Age 75 years or older ("yes"/"no")
            symptoms_angina_dyspnea (str): Symptoms of angina or dyspnea ("yes"/"no")
            anemia_hgb_less_12 (str): Anemia with Hgb <12 mg/dL ("yes"/"no")
            vascular_surgery (str): Vascular surgery procedure ("yes"/"no")
            emergency_surgery (str): Emergency surgery ("yes"/"no")
            
        Returns:
            Dict containing the score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(history_heart_disease, age_75_or_older, 
                            symptoms_angina_dyspnea, anemia_hgb_less_12,
                            vascular_surgery, emergency_surgery)
        
        # Calculate total score
        score = self._calculate_aub_has2_score(
            history_heart_disease, age_75_or_older, symptoms_angina_dyspnea,
            anemia_hgb_less_12, vascular_surgery, emergency_surgery
        )
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, history_heart_disease: str, age_75_or_older: str,
                        symptoms_angina_dyspnea: str, anemia_hgb_less_12: str,
                        vascular_surgery: str, emergency_surgery: str):
        """Validates all input parameters"""
        
        valid_options = ["yes", "no"]
        
        # Validate each parameter
        params = [
            ("history_heart_disease", history_heart_disease),
            ("age_75_or_older", age_75_or_older),
            ("symptoms_angina_dyspnea", symptoms_angina_dyspnea),
            ("anemia_hgb_less_12", anemia_hgb_less_12),
            ("vascular_surgery", vascular_surgery),
            ("emergency_surgery", emergency_surgery)
        ]
        
        for param_name, param_value in params:
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got '{param_value}'")
    
    def _calculate_aub_has2_score(self, history_heart_disease: str, age_75_or_older: str,
                                 symptoms_angina_dyspnea: str, anemia_hgb_less_12: str,
                                 vascular_surgery: str, emergency_surgery: str) -> int:
        """
        Calculates the AUB-HAS2 score by summing individual risk factors
        
        Each risk factor present contributes 1 point to the total score.
        Total possible range: 0-6 points.
        """
        score = 0
        
        # History of heart disease (1 point if yes)
        if history_heart_disease == "yes":
            score += self.RISK_FACTOR_POINTS
            
        # Age ≥75 years (1 point if yes)
        if age_75_or_older == "yes":
            score += self.RISK_FACTOR_POINTS
            
        # Symptoms of angina or dyspnea (1 point if yes)
        if symptoms_angina_dyspnea == "yes":
            score += self.RISK_FACTOR_POINTS
            
        # Anemia with hemoglobin <12 mg/dL (1 point if yes)
        if anemia_hgb_less_12 == "yes":
            score += self.RISK_FACTOR_POINTS
            
        # Vascular surgery (1 point if yes)
        if vascular_surgery == "yes":
            score += self.RISK_FACTOR_POINTS
            
        # Emergency surgery (1 point if yes)
        if emergency_surgery == "yes":
            score += self.RISK_FACTOR_POINTS
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines cardiovascular risk category and clinical interpretation
        
        Args:
            score (int): AUB-HAS2 score (0-6 points)
            
        Returns:
            Dict with risk category and clinical recommendations  
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Low cardiovascular risk",
                "interpretation": "Very low risk of major cardiovascular events (death, myocardial infarction, or stroke) within 30 days after surgery. Event rate <1%. Routine perioperative management without additional cardiac monitoring or interventions."
            }
        elif score <= 3:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate cardiovascular risk", 
                "interpretation": "Moderate risk of major cardiovascular events within 30 days after surgery. Event rate 5-11%. Consider enhanced perioperative monitoring and cardiac consultation for optimization of medical therapy."
            }
        else:  # score >= 4
            return {
                "stage": "High Risk",
                "description": "High cardiovascular risk",
                "interpretation": "High risk of major cardiovascular events within 30 days after surgery. Event rate >15%. Recommend preoperative cardiac consultation, optimization of medical therapy, enhanced perioperative monitoring, and consideration of postoperative ICU care."
            }


def calculate_aub_has2_cardiovascular_risk_index(history_heart_disease: str, age_75_or_older: str,
                                               symptoms_angina_dyspnea: str, anemia_hgb_less_12: str,
                                               vascular_surgery: str, emergency_surgery: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates AUB-HAS2 cardiovascular risk score for noncardiac surgery patients.
    """
    calculator = AubHas2CardiovascularRiskIndexCalculator()
    return calculator.calculate(history_heart_disease, age_75_or_older,
                              symptoms_angina_dyspnea, anemia_hgb_less_12,
                              vascular_surgery, emergency_surgery)