"""
ATRIA Stroke Risk Score Calculator

Determines stroke risk in patients with atrial fibrillation. The ATRIA 
(Anticoagulation and Risk Factors in Atrial Fibrillation) stroke risk score 
predicts ischemic stroke and other thromboembolism.

References:
1. Singer DE, Chang Y, Borowsky LH, et al. A new risk scheme to predict ischemic 
   stroke and other thromboembolism in atrial fibrillation: the ATRIA study stroke 
   risk score. J Am Heart Assoc. 2013;2(3):e000250.
"""

from typing import Dict, Any


class AtriaStrokeCalculator:
    """Calculator for ATRIA Stroke Risk Score"""
    
    def __init__(self):
        # Age scoring without prior stroke
        self.AGE_SCORES_NO_STROKE = {
            (0, 65): 0,
            (65, 75): 3,
            (75, 85): 5,
            (85, 121): 6
        }
        
        # Age scoring with prior stroke
        self.AGE_SCORES_WITH_STROKE = {
            (0, 65): 8,
            (65, 75): 7,
            (75, 85): 7,
            (85, 121): 9
        }
        
        # Other risk factor points
        self.FEMALE_POINTS = 1
        self.DIABETES_POINTS = 1
        self.CHF_POINTS = 1
        self.HYPERTENSION_POINTS = 1
        self.PROTEINURIA_POINTS = 1
        self.RENAL_DISEASE_POINTS = 1
    
    def calculate(self, age: int, sex: str, history_of_stroke: str, diabetes: str,
                  congestive_heart_failure: str, hypertension: str, proteinuria: str,
                  egfr_less_than_45_or_esrd: str) -> Dict[str, Any]:
        """
        Calculates the ATRIA Stroke Risk Score
        
        Args:
            age (int): Patient age in years
            sex (str): "male" or "female"
            history_of_stroke (str): "yes" or "no" - prior ischemic stroke or TIA
            diabetes (str): "yes" or "no"
            congestive_heart_failure (str): "yes" or "no"
            hypertension (str): "yes" or "no"
            proteinuria (str): "yes" or "no" - >1+ on dipstick or >300 mg/day
            egfr_less_than_45_or_esrd (str): "yes" or "no" - eGFR <45 or ESRD
            
        Returns:
            Dict with the score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, history_of_stroke, diabetes,
                             congestive_heart_failure, hypertension,
                             proteinuria, egfr_less_than_45_or_esrd)
        
        # Calculate total score
        score = self._calculate_score(age, sex, history_of_stroke, diabetes,
                                     congestive_heart_failure, hypertension,
                                     proteinuria, egfr_less_than_45_or_esrd)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, history_of_stroke: str,
                        diabetes: str, congestive_heart_failure: str,
                        hypertension: str, proteinuria: str,
                        egfr_less_than_45_or_esrd: str):
        """Validates all input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError(f"Age must be between 0 and 120 years, got {age}")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError(f"Sex must be 'male' or 'female', got '{sex}'")
        
        # Validate yes/no parameters
        valid_options = ["yes", "no"]
        parameters = {
            "history_of_stroke": history_of_stroke,
            "diabetes": diabetes,
            "congestive_heart_failure": congestive_heart_failure,
            "hypertension": hypertension,
            "proteinuria": proteinuria,
            "egfr_less_than_45_or_esrd": egfr_less_than_45_or_esrd
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(
                    f"{param_name} must be 'yes' or 'no', got '{param_value}'"
                )
    
    def _get_age_score(self, age: int, has_prior_stroke: bool) -> int:
        """Calculates age-based score component"""
        
        # Select appropriate age scoring based on stroke history
        age_scores = (self.AGE_SCORES_WITH_STROKE if has_prior_stroke 
                     else self.AGE_SCORES_NO_STROKE)
        
        # Find the appropriate age range and return the score
        for (min_age, max_age), score in age_scores.items():
            if min_age <= age < max_age:
                return score
        
        # Should not reach here due to validation
        return 0
    
    def _calculate_score(self, age: int, sex: str, history_of_stroke: str,
                        diabetes: str, congestive_heart_failure: str,
                        hypertension: str, proteinuria: str,
                        egfr_less_than_45_or_esrd: str) -> int:
        """Calculates the total ATRIA stroke risk score"""
        
        score = 0
        
        # Add age-based score
        has_prior_stroke = history_of_stroke == "yes"
        score += self._get_age_score(age, has_prior_stroke)
        
        # Add sex points
        if sex == "female":
            score += self.FEMALE_POINTS
        
        # Add comorbidity points
        if diabetes == "yes":
            score += self.DIABETES_POINTS
            
        if congestive_heart_failure == "yes":
            score += self.CHF_POINTS
            
        if hypertension == "yes":
            score += self.HYPERTENSION_POINTS
            
        if proteinuria == "yes":
            score += self.PROTEINURIA_POINTS
            
        if egfr_less_than_45_or_esrd == "yes":
            score += self.RENAL_DISEASE_POINTS
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the score
        
        Args:
            score (int): Calculated ATRIA stroke risk score
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if score <= 5:
            return {
                "stage": "Low",
                "description": "Low stroke risk",
                "interpretation": "Low risk of stroke (<1% per year). These patients have minimal stroke risk with atrial fibrillation. Consider patient preferences and bleeding risk when making anticoagulation decisions."
            }
        elif score == 6:
            return {
                "stage": "Intermediate",
                "description": "Intermediate stroke risk",
                "interpretation": "Intermediate risk of stroke (1-<2% per year). These patients have moderate stroke risk. Anticoagulation should be considered based on patient preferences, bleeding risk, and overall clinical context."
            }
        else:  # score >= 7
            return {
                "stage": "High",
                "description": "High stroke risk",
                "interpretation": "High risk of stroke (≥2% per year). These patients have substantial stroke risk from atrial fibrillation. Anticoagulation is strongly recommended unless contraindicated. The benefit of stroke prevention generally outweighs bleeding risk in these patients."
            }


def calculate_atria_stroke(age: int, sex: str, history_of_stroke: str,
                          diabetes: str, congestive_heart_failure: str,
                          hypertension: str, proteinuria: str,
                          egfr_less_than_45_or_esrd: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AtriaStrokeCalculator()
    return calculator.calculate(age, sex, history_of_stroke, diabetes,
                               congestive_heart_failure, hypertension,
                               proteinuria, egfr_less_than_45_or_esrd)