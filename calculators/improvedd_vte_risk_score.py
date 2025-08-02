"""
IMPROVEDD VTE Risk Score Calculator

Predicts 77-day risk of acute venous thromboembolism (VTE) in hospitalized medical patients
by incorporating D-dimer levels into the IMPROVE Risk Score. The IMPROVEDD (IMPROVE + D-dimer) 
score enhances VTE risk stratification through the addition of D-dimer ≥2× upper limit of normal.

References (Vancouver style):
1. Gibson CM, Spyropoulos AC, Cohen AT, et al. The IMPROVEDD VTE Risk Score: Incorporation 
   of D-Dimer into the IMPROVE Score to Improve Venous Thromboembolism Risk Stratification. 
   TH Open. 2017 Oct 9;1(1):e56-e65. doi: 10.1055/s-0037-1603929.
2. Spyropoulos AC, Lipardi C, Xu J, et al. Modified IMPROVE VTE Risk Score and Elevated 
   D-Dimer Identify a High Venous Thromboembolism Risk in Acutely Ill Medical Population 
   for Extended Thromboprophylaxis. TH Open. 2020 Mar 6;4(1):e59-e65. doi: 10.1055/s-0040-1705137.
3. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
   models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
   Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
"""

from typing import Dict, Any


class ImprovedVteRiskScoreCalculator:
    """Calculator for IMPROVEDD VTE Risk Score"""
    
    def __init__(self):
        # IMPROVEDD VTE Risk Score weights (same as IMPROVE + D-dimer)
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
            },
            "d_dimer_elevated": {
                "no": 0,
                "yes": 2
            }
        }
        
        # Risk interpretation thresholds with 77-day VTE percentages
        self.risk_categories = {
            0: {
                "stage": "Very Low Risk",
                "description": "Score 0 points",
                "vte_risk": "0.5%",
                "interpretation": "0.5% 77-day VTE risk. Pharmacologic thromboprophylaxis not warranted. Consider mechanical prophylaxis or early mobilization as appropriate."
            },
            1: {
                "stage": "Low Risk", 
                "description": "Score 1 point",
                "vte_risk": "0.7%",
                "interpretation": "0.7% 77-day VTE risk. Pharmacologic thromboprophylaxis not warranted. Consider mechanical prophylaxis or early mobilization as appropriate."
            },
            2: {
                "stage": "Moderate Risk",
                "description": "Score 2 points", 
                "vte_risk": "1.0%",
                "interpretation": "1.0% 77-day VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
            },
            3: {
                "stage": "Moderate-High Risk",
                "description": "Score 3 points",
                "vte_risk": "1.4%", 
                "interpretation": "1.4% 77-day VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
            },
            4: {
                "stage": "High Risk",
                "description": "Score 4 points",
                "vte_risk": "1.9%",
                "interpretation": "1.9% 77-day VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
            }
        }
    
    def calculate(self, previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                 current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str, 
                 age_over_60: str, d_dimer_elevated: str) -> Dict[str, Any]:
        """
        Calculates the IMPROVEDD VTE Risk Score
        
        Args:
            previous_vte (str): History of previous VTE
            known_thrombophilia (str): Known thrombophilia or hereditary thrombotic disorder
            current_lower_limb_paralysis (str): Current lower-limb paralysis or paresis
            current_cancer (str): Current active cancer diagnosis
            immobilized_7_days (str): Immobilized ≥7 days prior to and during admission
            icu_ccu_stay (str): Current ICU/CCU stay
            age_over_60 (str): Age greater than 60 years
            d_dimer_elevated (str): D-dimer ≥2× upper limit of normal
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(previous_vte, known_thrombophilia, current_lower_limb_paralysis,
                            current_cancer, immobilized_7_days, icu_ccu_stay, age_over_60, d_dimer_elevated)
        
        # Calculate total score
        score = self._calculate_total_score(
            previous_vte, known_thrombophilia, current_lower_limb_paralysis, current_cancer,
            immobilized_7_days, icu_ccu_stay, age_over_60, d_dimer_elevated
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
                        current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str, age_over_60: str, 
                        d_dimer_elevated: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "previous_vte": ["yes", "no"],
            "known_thrombophilia": ["yes", "no"],
            "current_lower_limb_paralysis": ["yes", "no"],
            "current_cancer": ["yes", "no"],
            "immobilized_7_days": ["yes", "no"],
            "icu_ccu_stay": ["yes", "no"],
            "age_over_60": ["yes", "no"],
            "d_dimer_elevated": ["yes", "no"]
        }
        
        # Validate each parameter
        parameters = {
            "previous_vte": previous_vte,
            "known_thrombophilia": known_thrombophilia,
            "current_lower_limb_paralysis": current_lower_limb_paralysis,
            "current_cancer": current_cancer,
            "immobilized_7_days": immobilized_7_days,
            "icu_ccu_stay": icu_ccu_stay,
            "age_over_60": age_over_60,
            "d_dimer_elevated": d_dimer_elevated
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of: {valid_options[param_name]}")
    
    def _calculate_total_score(self, previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                              current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str, age_over_60: str,
                              d_dimer_elevated: str) -> int:
        """
        Calculates the total IMPROVEDD VTE Risk Score
        
        IMPROVEDD VTE Risk Scoring:
        - Previous VTE: 3 points
        - Known thrombophilia: 2 points
        - Current lower-limb paralysis: 2 points
        - Current cancer: 2 points
        - Immobilized ≥7 days: 1 point
        - ICU/CCU stay: 1 point
        - Age >60 years: 1 point
        - D-dimer ≥2×ULN: 2 points (NEW addition to IMPROVE)
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
        total_score += self.scoring_weights["d_dimer_elevated"][d_dimer_elevated]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on IMPROVEDD VTE Risk Score
        
        Args:
            score (int): IMPROVEDD VTE Risk Score
            
        Returns:
            Dict with interpretation details
        """
        
        # Handle specific score interpretations
        if score in self.risk_categories:
            return self.risk_categories[score]
        elif score >= 5:  # Score 5-14 (very high risk)
            return {
                "stage": "Very High Risk",
                "description": f"Score {score} points (5-14 points)",
                "interpretation": "2.7% or higher 77-day VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation. May benefit from extended prophylaxis duration."
            }
        else:  # Fallback (should not occur with valid inputs)
            return {
                "stage": "Unknown Risk",
                "description": f"Score {score} points",
                "interpretation": f"Score {score} points. Please consult clinical guidelines for appropriate management."
            }


def calculate_improvedd_vte_risk_score(previous_vte: str, known_thrombophilia: str, current_lower_limb_paralysis: str,
                                     current_cancer: str, immobilized_7_days: str, icu_ccu_stay: str,
                                     age_over_60: str, d_dimer_elevated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImprovedVteRiskScoreCalculator()
    return calculator.calculate(
        previous_vte, known_thrombophilia, current_lower_limb_paralysis, current_cancer,
        immobilized_7_days, icu_ccu_stay, age_over_60, d_dimer_elevated
    )