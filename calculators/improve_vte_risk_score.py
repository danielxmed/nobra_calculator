"""
IMPROVE VTE Risk Score Calculator

Predicts 3-month risk of acute venous thromboembolism (VTE) in hospitalized medical patients.
The IMPROVE (International Medical Prevention Registry on Venous Thromboembolism) Predictive 
score helps identify patients who may not require pharmacological thromboprophylaxis.

References (Vancouver style):
1. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
   models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
   Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
2. Hostler DC, Marx ES, Moores LK, et al. Validation of the International Medical 
   Prevention Registry on Venous Thromboembolism bleeding risk model. Chest. 2016 
   Apr;149(4):1002-1009. doi: 10.1378/chest.15-2082.
3. Rosenberg D, Eichorn A, Alarcon M, et al. External validation of the risk assessment 
   model of the International Medical Prevention Registry on Venous Thromboembolism 
   (IMPROVE) for medical patients in a tertiary health system. J Am Heart Assoc. 2014 
   Nov 4;3(6):e001152. doi: 10.1161/JAHA.114.001152.
"""

from typing import Dict, Any


class ImproveVteRiskScoreCalculator:
    """Calculator for IMPROVE VTE Risk Score"""
    
    def __init__(self):
        # IMPROVE VTE Risk Score weights
        self.scoring_weights = {
            "previous_vte": {
                "no": 0,
                "yes": 3
            },
            "known_thrombophilia": {
                "no": 0,
                "yes": 2
            },
            "current_lower_limb_paralysis": {
                "no": 0,
                "yes": 2
            },
            "current_cancer": {
                "no": 0,
                "yes": 2
            },
            "immobilized_7_days": {
                "no": 0,
                "yes": 1
            },
            "icu_ccu_stay": {
                "no": 0,
                "yes": 1
            },
            "age_over_60": {
                "no": 0,
                "yes": 1
            }
        }
        
        # Risk interpretation thresholds with VTE percentages
        self.risk_categories = {
            0: {
                "stage": "Very Low Risk",
                "description": "Score 0 points",
                "vte_risk": "0.4%",
                "interpretation": "0.4% 3-month VTE risk. Pharmacologic thromboprophylaxis not warranted. Consider mechanical prophylaxis or early mobilization as appropriate."
            },
            1: {
                "stage": "Low Risk", 
                "description": "Score 1 point",
                "vte_risk": "0.6%",
                "interpretation": "0.6% 3-month VTE risk. Pharmacologic thromboprophylaxis not warranted. Consider mechanical prophylaxis or early mobilization as appropriate."
            },
            2: {
                "stage": "Moderate Risk",
                "description": "Score 2 points", 
                "vte_risk": "1.0%",
                "interpretation": "1.0% 3-month VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
            },
            3: {
                "stage": "Moderate-High Risk",
                "description": "Score 3 points",
                "vte_risk": "1.7%", 
                "interpretation": "1.7% 3-month VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
            },
            4: {
                "stage": "High Risk",
                "description": "Score 4 points",
                "vte_risk": "2.9%",
                "interpretation": "2.9% 3-month VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
            }
        }
    
    def calculate(self, previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                 current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str, 
                 age_over_60: str) -> Dict[str, Any]:
        """
        Calculates the IMPROVE VTE Risk Score
        
        Args:
            previous_vte (str): History of previous VTE
            known_thrombophilia (str): Known thrombophilia or hereditary thrombotic disorder
            current_lower_limb_paralysis (str): Current lower-limb paralysis or paresis
            current_cancer (str): Current active cancer diagnosis
            immobilized_7_days (str): Immobilized ≥7 days prior to and during admission
            icu_ccu_stay (str): Current ICU/CCU stay
            age_over_60 (str): Age greater than 60 years
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(previous_vte, known_thrombophilia, current_lower_limb_paralysis,
                            current_cancer, immobilized_7_days, icu_ccu_stay, age_over_60)
        
        # Calculate total score
        score = self._calculate_total_score(
            previous_vte, known_thrombophilia, current_lower_limb_paralysis, current_cancer,
            immobilized_7_days, icu_ccu_stay, age_over_60
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                        current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str, age_over_60: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "previous_vte": ["yes", "no"],
            "known_thrombophilia": ["yes", "no"],
            "current_lower_limb_paralysis": ["yes", "no"],
            "current_cancer": ["yes", "no"],
            "immobilized_7_days": ["yes", "no"],
            "icu_ccu_stay": ["yes", "no"],
            "age_over_60": ["yes", "no"]
        }
        
        # Validate each parameter
        parameters = {
            "previous_vte": previous_vte,
            "known_thrombophilia": known_thrombophilia,
            "current_lower_limb_paralysis": current_lower_limb_paralysis,
            "current_cancer": current_cancer,
            "immobilized_7_days": immobilized_7_days,
            "icu_ccu_stay": icu_ccu_stay,
            "age_over_60": age_over_60
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of: {valid_options[param_name]}")
    
    def _calculate_total_score(self, previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                              current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str, age_over_60: str) -> int:
        """
        Calculates the total IMPROVE VTE Risk Score
        
        IMPROVE VTE Risk Scoring:
        - Previous VTE: 3 points
        - Known thrombophilia: 2 points
        - Current lower-limb paralysis: 2 points
        - Current cancer: 2 points
        - Immobilized ≥7 days: 1 point
        - ICU/CCU stay: 1 point
        - Age >60 years: 1 point
        """
        
        total_score = 0
        
        # Add points for each risk factor
        total_score += self.scoring_weights["previous_vte"][previous_vte]
        total_score += self.scoring_weights["known_thrombophilia"][known_thrombophilia]
        total_score += self.scoring_weights["current_lower_limb_paralysis"][current_lower_limb_paralysis]
        total_score += self.scoring_weights["current_cancer"][current_cancer]
        total_score += self.scoring_weights["immobilized_7_days"][immobilized_7_days]
        total_score += self.scoring_weights["icu_ccu_stay"][icu_ccu_stay]
        total_score += self.scoring_weights["age_over_60"][age_over_60]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on IMPROVE VTE Risk Score
        
        Args:
            score (int): IMPROVE VTE Risk Score
            
        Returns:
            Dict with interpretation details
        """
        
        # Handle specific score interpretations
        if score in self.risk_categories:
            return self.risk_categories[score]
        elif score >= 5:  # Score 5-12 (very high risk)
            return {
                "stage": "Very High Risk",
                "description": f"Score {score} points (5-12 points)",
                "interpretation": "7.2% or higher 3-month VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation. May benefit from extended prophylaxis duration."
            }
        else:  # Fallback (should not occur with valid inputs)
            return {
                "stage": "Unknown Risk",
                "description": f"Score {score} points",
                "interpretation": f"Score {score} points. Please consult clinical guidelines for appropriate management."
            }


def calculate_improve_vte_risk_score(previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                                   current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str,
                                   age_over_60: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImproveVteRiskScoreCalculator()
    return calculator.calculate(
        previous_vte, known_thrombophilia, current_lower_limb_paralysis, current_cancer,
        immobilized_7_days, icu_ccu_stay, age_over_60
    )