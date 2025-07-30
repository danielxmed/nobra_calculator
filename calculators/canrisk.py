"""
Canadian Diabetes Risk Assessment Questionnaire (CANRISK) Calculator

Screens for undiagnosed type 2 diabetes mellitus and prediabetes in Canadian 
adults aged 18-74 years.

References:
1. Robinson CA, Agarwal G, Nerenberg K. Validating the CANRISK prognostic model 
   for assessing diabetes risk in Canada's multi-ethnic population. Chronic Dis 
   Inj Can. 2011;32(1):19-31.
2. Public Health Agency of Canada. CANRISK: The Canadian Diabetes Risk Questionnaire 
   User Guide for Pharmacists. Ottawa: Public Health Agency of Canada; 2011.
"""

from typing import Dict, Any


class CanriskCalculator:
    """Calculator for Canadian Diabetes Risk Assessment Questionnaire (CANRISK)"""
    
    def __init__(self):
        # Age scoring
        self.age_scores = {
            "18-44": 0,
            "45-54": 7,
            "55-64": 13,
            "65-74": 15
        }
        
        # Gender scoring
        self.gender_scores = {
            "female": 0,
            "male": 6
        }
        
        # BMI scoring
        self.bmi_scores = {
            "under_25": 0,
            "25_to_29": 4,
            "30_to_34": 9,
            "35_or_over": 14
        }
        
        # Waist circumference scoring (differs by gender)
        self.waist_scores = {
            "male": {
                "small": 0,     # <94 cm
                "medium": 4,    # 94-102 cm
                "large": 6      # >102 cm
            },
            "female": {
                "small": 0,     # <80 cm
                "medium": 4,    # 80-88 cm
                "large": 6      # >88 cm
            }
        }
        
        # Physical activity scoring
        self.physical_activity_scores = {
            "yes": 0,
            "no": 1
        }
        
        # Vegetable/fruit consumption scoring
        self.diet_scores = {
            "every_day": 0,
            "not_every_day": 2
        }
        
        # High blood pressure scoring
        self.blood_pressure_scores = {
            "no": 0,
            "dont_know": 0,
            "yes": 4
        }
        
        # High blood sugar scoring
        self.blood_sugar_scores = {
            "no": 0,
            "dont_know": 0,
            "yes": 14
        }
        
        # Large baby scoring (females only)
        self.large_baby_scores = {
            "no": 0,
            "dont_know": 0,
            "not_applicable": 0,
            "yes": 1
        }
        
        # Family diabetes history scoring
        self.family_diabetes_scores = {
            "no": 0,
            "dont_know": 0,
            "one_relative": 2,
            "two_relatives": 4,
            "three_relatives": 6,
            "all_relatives": 8
        }
        
        # Ethnicity scoring
        self.ethnicity_scores = {
            "white": 0,
            "other": 0,
            "east_asian": 10,
            "south_asian": 11
        }
    
    def calculate(
        self,
        age: str,
        gender: str,
        bmi: str,
        waist_circumference: str,
        physical_activity: str,
        vegetable_fruit_consumption: str,
        high_blood_pressure: str,
        high_blood_sugar: str,
        large_baby: str,
        family_diabetes: str,
        ethnicity: str
    ) -> Dict[str, Any]:
        """
        Calculates the CANRISK score
        
        Args:
            age: Age range (18-44, 45-54, 55-64, 65-74)
            gender: Biological sex (female, male)
            bmi: BMI category 
            waist_circumference: Waist size (small, medium, large)
            physical_activity: 30 min daily activity (yes, no)
            vegetable_fruit_consumption: Daily consumption (every_day, not_every_day)
            high_blood_pressure: History or medication (yes, no, dont_know)
            high_blood_sugar: Ever found high (yes, no, dont_know)
            large_baby: Birth >9 lbs (yes, no, dont_know, not_applicable)
            family_diabetes: Family history (no, one_relative, etc.)
            ethnicity: Ethnic background (white, south_asian, east_asian, other)
            
        Returns:
            Dict with CANRISK score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age, gender, bmi, waist_circumference, physical_activity,
            vegetable_fruit_consumption, high_blood_pressure, high_blood_sugar,
            large_baby, family_diabetes, ethnicity
        )
        
        # Calculate total score
        total_score = 0
        
        # Add age score
        total_score += self.age_scores[age]
        
        # Add gender score
        total_score += self.gender_scores[gender]
        
        # Add BMI score
        total_score += self.bmi_scores[bmi]
        
        # Add waist circumference score (gender-specific)
        total_score += self.waist_scores[gender][waist_circumference]
        
        # Add physical activity score
        total_score += self.physical_activity_scores[physical_activity]
        
        # Add diet score
        total_score += self.diet_scores[vegetable_fruit_consumption]
        
        # Add blood pressure score
        total_score += self.blood_pressure_scores[high_blood_pressure]
        
        # Add blood sugar score
        total_score += self.blood_sugar_scores[high_blood_sugar]
        
        # Add large baby score (only for females)
        if gender == "female" and large_baby != "not_applicable":
            total_score += self.large_baby_scores[large_baby]
        
        # Add family diabetes score
        total_score += self.family_diabetes_scores[family_diabetes]
        
        # Add ethnicity score
        total_score += self.ethnicity_scores[ethnicity]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        # This validation is handled by the parameter enums in the JSON
        # Additional validation could be added here if needed
        pass
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CANRISK score
        
        Args:
            score (int): Total CANRISK score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 21:
            return {
                "stage": "Low Risk",
                "description": "Low risk of type 2 diabetes",
                "interpretation": "Your risk of having prediabetes or type 2 diabetes is low. Maintain a healthy lifestyle with regular physical activity and a balanced diet. Re-assess your risk annually or if your health status changes."
            }
        elif score <= 32:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of type 2 diabetes",
                "interpretation": "You have a moderate risk of having prediabetes or type 2 diabetes. You should discuss your risk with a healthcare practitioner and consider lifestyle modifications. Screening with fasting glucose or HbA1c may be recommended."
            }
        else:  # score >= 33
            return {
                "stage": "High Risk",
                "description": "High risk of type 2 diabetes",
                "interpretation": "You have a high risk of having prediabetes or type 2 diabetes. You should consult with a healthcare practitioner to discuss getting your blood sugar tested. Immediate screening with fasting glucose or HbA1c is recommended, along with lifestyle interventions."
            }


def calculate_canrisk(
    age: str,
    gender: str,
    bmi: str,
    waist_circumference: str,
    physical_activity: str,
    vegetable_fruit_consumption: str,
    high_blood_pressure: str,
    high_blood_sugar: str,
    large_baby: str,
    family_diabetes: str,
    ethnicity: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CanriskCalculator()
    return calculator.calculate(
        age=age,
        gender=gender,
        bmi=bmi,
        waist_circumference=waist_circumference,
        physical_activity=physical_activity,
        vegetable_fruit_consumption=vegetable_fruit_consumption,
        high_blood_pressure=high_blood_pressure,
        high_blood_sugar=high_blood_sugar,
        large_baby=large_baby,
        family_diabetes=family_diabetes,
        ethnicity=ethnicity
    )