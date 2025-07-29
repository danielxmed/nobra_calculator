"""
American Diabetes Association (ADA) Risk Calculator

Predicts risk of undiagnosed diabetes to determine who should be screened.
Uses demographic and clinical factors to identify individuals at high risk 
for type 2 diabetes mellitus without requiring laboratory tests.

References:
- Bang H, Edwards AM, Bomback AS, et al. Development and validation of a patient self-assessment score for diabetes risk. Ann Intern Med. 2009;151(11):775-83.
- American Diabetes Association. Classification and Diagnosis of Diabetes: Standards of Medical Care in Diabetes-2021. Diabetes Care. 2021;44(Suppl 1):S15-S33.
"""

from typing import Dict, Any


class AdaRiskCalculatorCalculator:
    """Calculator for American Diabetes Association (ADA) Risk Calculator"""
    
    def __init__(self):
        # Age scoring weights
        self.AGE_WEIGHTS = {
            "under_40": 0,
            "40_49": 1,
            "50_59": 2,
            "60_or_older": 3
        }
        
        # Gender scoring weights
        self.GENDER_WEIGHTS = {
            "female": 0,
            "male": 1
        }
        
        # Family history scoring weights
        self.FAMILY_HISTORY_WEIGHTS = {
            "no": 0,
            "yes": 1
        }
        
        # Hypertension scoring weights
        self.HYPERTENSION_WEIGHTS = {
            "no": 0,
            "yes": 1
        }
        
        # Physical activity scoring weights (note: reversed scoring)
        self.PHYSICAL_ACTIVITY_WEIGHTS = {
            "yes": 0,  # Active = 0 points
            "no": 1    # Not active = 1 point
        }
        
        # BMI scoring weights
        self.BMI_WEIGHTS = {
            "under_25": 0,
            "25_to_30": 1,
            "30_to_40": 2,
            "40_or_higher": 3
        }
    
    def calculate(self, age_category: str, gender: str, family_history_diabetes: str,
                 hypertension: str, physically_active: str, bmi_category: str) -> Dict[str, Any]:
        """
        Calculates the ADA diabetes risk score
        
        Args:
            age_category (str): Age category ("under_40", "40_49", "50_59", "60_or_older")
            gender (str): Patient gender ("female", "male")
            family_history_diabetes (str): First-degree relative with diabetes ("no", "yes")
            hypertension (str): History of hypertension ("no", "yes")
            physically_active (str): Physically active ("yes", "no")
            bmi_category (str): BMI category ("under_25", "25_to_30", "30_to_40", "40_or_higher")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_category, gender, family_history_diabetes,
                            hypertension, physically_active, bmi_category)
        
        # Calculate score
        score = self._calculate_ada_score(age_category, gender, family_history_diabetes,
                                        hypertension, physically_active, bmi_category)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category, gender, family_history_diabetes,
                        hypertension, physically_active, bmi_category):
        """Validates input parameters"""
        
        # Validate age category
        if not isinstance(age_category, str):
            raise ValueError("age_category must be a string")
        if age_category not in self.AGE_WEIGHTS:
            raise ValueError(f"age_category must be one of: {list(self.AGE_WEIGHTS.keys())}")
        
        # Validate gender
        if not isinstance(gender, str):
            raise ValueError("gender must be a string")
        if gender not in self.GENDER_WEIGHTS:
            raise ValueError(f"gender must be one of: {list(self.GENDER_WEIGHTS.keys())}")
        
        # Validate family history
        if not isinstance(family_history_diabetes, str):
            raise ValueError("family_history_diabetes must be a string")
        if family_history_diabetes not in self.FAMILY_HISTORY_WEIGHTS:
            raise ValueError(f"family_history_diabetes must be one of: {list(self.FAMILY_HISTORY_WEIGHTS.keys())}")
        
        # Validate hypertension
        if not isinstance(hypertension, str):
            raise ValueError("hypertension must be a string")
        if hypertension not in self.HYPERTENSION_WEIGHTS:
            raise ValueError(f"hypertension must be one of: {list(self.HYPERTENSION_WEIGHTS.keys())}")
        
        # Validate physical activity
        if not isinstance(physically_active, str):
            raise ValueError("physically_active must be a string")
        if physically_active not in self.PHYSICAL_ACTIVITY_WEIGHTS:
            raise ValueError(f"physically_active must be one of: {list(self.PHYSICAL_ACTIVITY_WEIGHTS.keys())}")
        
        # Validate BMI category
        if not isinstance(bmi_category, str):
            raise ValueError("bmi_category must be a string")
        if bmi_category not in self.BMI_WEIGHTS:
            raise ValueError(f"bmi_category must be one of: {list(self.BMI_WEIGHTS.keys())}")
    
    def _calculate_ada_score(self, age_category, gender, family_history_diabetes,
                           hypertension, physically_active, bmi_category) -> int:
        """Calculates the ADA diabetes risk score"""
        
        score = 0
        
        # Add points for age
        score += self.AGE_WEIGHTS[age_category]
        
        # Add points for gender (male gets 1 point)
        score += self.GENDER_WEIGHTS[gender]
        
        # Add points for family history
        score += self.FAMILY_HISTORY_WEIGHTS[family_history_diabetes]
        
        # Add points for hypertension
        score += self.HYPERTENSION_WEIGHTS[hypertension]
        
        # Add points for physical inactivity (note: reversed scoring)
        score += self.PHYSICAL_ACTIVITY_WEIGHTS[physically_active]
        
        # Add points for BMI
        score += self.BMI_WEIGHTS[bmi_category]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ADA diabetes risk score
        
        Args:
            score (int): Calculated ADA risk score (0-10)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low Risk",
                "description": "Low risk for diabetes",
                "interpretation": "Low risk for diabetes. Continue routine preventive care and lifestyle counseling. No additional diabetes screening needed at this time."
            }
        elif score == 4:
            return {
                "stage": "High Risk for Prediabetes",
                "description": "High risk for prediabetes",
                "interpretation": "High risk for prediabetes. Consider screening with fasting glucose, oral glucose tolerance test, or HbA1c. Lifestyle interventions recommended."
            }
        else:  # score >= 5
            return {
                "stage": "High Risk for Diabetes",
                "description": "High risk for diabetes",
                "interpretation": "High risk for undiagnosed diabetes. Recommend screening with fasting glucose, oral glucose tolerance test, or HbA1c. Consider diabetes prevention programs and lifestyle interventions."
            }


def calculate_ada_risk_calculator(age_category, gender, family_history_diabetes,
                                hypertension, physically_active, bmi_category) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ada_risk_calculator pattern
    """
    calculator = AdaRiskCalculatorCalculator()
    return calculator.calculate(age_category, gender, family_history_diabetes,
                              hypertension, physically_active, bmi_category)