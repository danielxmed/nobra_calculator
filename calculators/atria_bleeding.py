"""
ATRIA Bleeding Risk Score Calculator

Determines bleeding risk for patients on warfarin therapy for atrial fibrillation.
The ATRIA (Anticoagulation and Risk Factors in Atrial Fibrillation) score stratifies
patients into low, intermediate, and high risk categories for major hemorrhage.

References:
1. Fang MC, Go AS, Chang Y, et al. A new risk scheme to predict warfarin-associated 
   hemorrhage: The ATRIA Study. J Am Coll Cardiol. 2011;58(4):395-401.
"""

from typing import Dict, Any


class AtriaBleedingCalculator:
    """Calculator for ATRIA Bleeding Risk Score"""
    
    def __init__(self):
        # Scoring points for each risk factor
        self.ANEMIA_POINTS = 3
        self.SEVERE_RENAL_DISEASE_POINTS = 3
        self.AGE_75_OR_OVER_POINTS = 2
        self.PRIOR_HEMORRHAGE_POINTS = 1
        self.HYPERTENSION_POINTS = 1
    
    def calculate(self, anemia: str, severe_renal_disease: str, age_75_or_over: str,
                  prior_hemorrhage: str, hypertension: str) -> Dict[str, Any]:
        """
        Calculates the ATRIA Bleeding Risk Score
        
        Args:
            anemia (str): "yes" if hemoglobin <13 g/dL (males) or <12 g/dL (females)
            severe_renal_disease (str): "yes" if GFR <30 mL/min or dialysis-dependent
            age_75_or_over (str): "yes" if age ≥75 years
            prior_hemorrhage (str): "yes" if any prior hemorrhage diagnosis
            hypertension (str): "yes" if history of hypertension
            
        Returns:
            Dict with the score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(anemia, severe_renal_disease, age_75_or_over,
                             prior_hemorrhage, hypertension)
        
        # Calculate total score
        score = self._calculate_score(anemia, severe_renal_disease, age_75_or_over,
                                     prior_hemorrhage, hypertension)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, anemia: str, severe_renal_disease: str, 
                        age_75_or_over: str, prior_hemorrhage: str, 
                        hypertension: str):
        """Validates all input parameters"""
        
        valid_options = ["yes", "no"]
        
        parameters = {
            "anemia": anemia,
            "severe_renal_disease": severe_renal_disease,
            "age_75_or_over": age_75_or_over,
            "prior_hemorrhage": prior_hemorrhage,
            "hypertension": hypertension
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(
                    f"{param_name} must be 'yes' or 'no', got '{param_value}'"
                )
    
    def _calculate_score(self, anemia: str, severe_renal_disease: str,
                        age_75_or_over: str, prior_hemorrhage: str,
                        hypertension: str) -> int:
        """Calculates the total ATRIA bleeding risk score"""
        
        score = 0
        
        # Add points for each risk factor
        if anemia == "yes":
            score += self.ANEMIA_POINTS
            
        if severe_renal_disease == "yes":
            score += self.SEVERE_RENAL_DISEASE_POINTS
            
        if age_75_or_over == "yes":
            score += self.AGE_75_OR_OVER_POINTS
            
        if prior_hemorrhage == "yes":
            score += self.PRIOR_HEMORRHAGE_POINTS
            
        if hypertension == "yes":
            score += self.HYPERTENSION_POINTS
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the score
        
        Args:
            score (int): Calculated ATRIA bleeding risk score
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low",
                "description": "Low bleeding risk",
                "interpretation": "Low risk (<1%) of major hemorrhage per year. These patients have the lowest bleeding risk on warfarin therapy. Consider standard anticoagulation management with regular INR monitoring."
            }
        elif score == 4:
            return {
                "stage": "Intermediate",
                "description": "Intermediate bleeding risk",
                "interpretation": "Intermediate risk (2.6%) of major hemorrhage per year. These patients require careful monitoring and consideration of bleeding risk when making anticoagulation decisions. More frequent INR monitoring may be warranted."
            }
        else:  # score >= 5
            return {
                "stage": "High",
                "description": "High bleeding risk",
                "interpretation": "High risk (5.8%) of major hemorrhage per year. These patients have substantial bleeding risk on warfarin therapy. Consider alternative strategies including closer INR monitoring, lower INR targets, or alternative anticoagulation options. The risk-benefit ratio of anticoagulation should be carefully evaluated."
            }


def calculate_atria_bleeding(anemia: str, severe_renal_disease: str,
                           age_75_or_over: str, prior_hemorrhage: str,
                           hypertension: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AtriaBleedingCalculator()
    return calculator.calculate(anemia, severe_renal_disease, age_75_or_over,
                               prior_hemorrhage, hypertension)