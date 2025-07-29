"""
Australian Type 2 Diabetes Risk (AUSDRISK) Assessment Tool Calculator

Estimates 5-year risk of developing type 2 diabetes in Australian patients.

Reference:
Chen L, Magliano DJ, Balkau B, Colagiuri S, Zimmet PZ, Tonkin AM, et al. AUSDRISK: 
an Australian Type 2 Diabetes Risk Assessment Tool based on demographic, lifestyle 
and simple anthropometric measures. Med J Aust. 2010;192(4):197-202.
"""

from typing import Dict, Any


class AusdriskCalculator:
    """Calculator for Australian Type 2 Diabetes Risk Assessment Tool"""
    
    def __init__(self):
        # Age group scoring
        self.AGE_SCORES = {
            "25-34": 0,
            "35-44": 2,
            "45-54": 4,
            "55-64": 6,
            "65+": 8
        }
        
        # Sex scoring
        self.SEX_SCORES = {
            "female": 0,
            "male": 3
        }
        
        # Ethnicity scoring
        self.ETHNICITY_SCORES = {
            "southern_european": 2,
            "asian": 2,
            "aboriginal_torres_strait": 2,
            "pacific_islander": 2,
            "other": 0
        }
        
        # Binary risk factors
        self.PARENTAL_DIABETES_SCORE = 3
        self.HIGH_GLUCOSE_HISTORY_SCORE = 6
        self.ANTIHYPERTENSIVE_SCORE = 2
        self.SMOKING_SCORE = 2
        self.PHYSICAL_INACTIVITY_SCORE = 2
        
        # Waist circumference categories
        self.WAIST_SCORES = {
            "category_1": 0,
            "category_2": 4,
            "category_3": 7
        }
    
    def calculate(self, age: str, sex: str, ethnicity: str, parental_diabetes: str,
                  high_blood_glucose_history: str, antihypertensive_medication: str,
                  current_smoker: str, physical_activity: str, 
                  waist_circumference_category: str) -> Dict[str, Any]:
        """
        Calculates the AUSDRISK score
        
        Args:
            age: Age group ("25-34", "35-44", "45-54", "55-64", "65+")
            sex: Biological sex ("male", "female")
            ethnicity: Ethnic background
            parental_diabetes: Family history of diabetes ("yes", "no")
            high_blood_glucose_history: History of high blood glucose ("yes", "no")
            antihypertensive_medication: Taking BP medication ("yes", "no")
            current_smoker: Currently smoking ("yes", "no")
            physical_activity: Activity status ("active", "inactive")
            waist_circumference_category: Waist category ("category_1", "category_2", "category_3")
            
        Returns:
            Dict with score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, ethnicity, parental_diabetes,
                            high_blood_glucose_history, antihypertensive_medication,
                            current_smoker, physical_activity, waist_circumference_category)
        
        # Calculate total score
        score = 0
        
        # Age points
        score += self.AGE_SCORES[age]
        
        # Sex points
        score += self.SEX_SCORES[sex]
        
        # Ethnicity points
        score += self.ETHNICITY_SCORES[ethnicity]
        
        # Parental diabetes
        if parental_diabetes == "yes":
            score += self.PARENTAL_DIABETES_SCORE
        
        # High blood glucose history
        if high_blood_glucose_history == "yes":
            score += self.HIGH_GLUCOSE_HISTORY_SCORE
        
        # Antihypertensive medication
        if antihypertensive_medication == "yes":
            score += self.ANTIHYPERTENSIVE_SCORE
        
        # Current smoker
        if current_smoker == "yes":
            score += self.SMOKING_SCORE
        
        # Physical inactivity
        if physical_activity == "inactive":
            score += self.PHYSICAL_INACTIVITY_SCORE
        
        # Waist circumference
        score += self.WAIST_SCORES[waist_circumference_category]
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, sex: str, ethnicity: str, parental_diabetes: str,
                        high_blood_glucose_history: str, antihypertensive_medication: str,
                        current_smoker: str, physical_activity: str, 
                        waist_circumference_category: str):
        """Validates input parameters"""
        
        if age not in self.AGE_SCORES:
            raise ValueError(f"Invalid age group: {age}")
        
        if sex not in self.SEX_SCORES:
            raise ValueError(f"Invalid sex: {sex}")
        
        if ethnicity not in self.ETHNICITY_SCORES:
            raise ValueError(f"Invalid ethnicity: {ethnicity}")
        
        if parental_diabetes not in ["yes", "no"]:
            raise ValueError("Parental diabetes must be 'yes' or 'no'")
        
        if high_blood_glucose_history not in ["yes", "no"]:
            raise ValueError("High blood glucose history must be 'yes' or 'no'")
        
        if antihypertensive_medication not in ["yes", "no"]:
            raise ValueError("Antihypertensive medication must be 'yes' or 'no'")
        
        if current_smoker not in ["yes", "no"]:
            raise ValueError("Current smoker must be 'yes' or 'no'")
        
        if physical_activity not in ["active", "inactive"]:
            raise ValueError("Physical activity must be 'active' or 'inactive'")
        
        if waist_circumference_category not in self.WAIST_SCORES:
            raise ValueError(f"Invalid waist circumference category: {waist_circumference_category}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the AUSDRISK score
        
        Args:
            score (int): AUSDRISK score (0-35)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 5:
            return {
                "stage": "Low Risk",
                "description": "5 or less points",
                "interpretation": "Approximately 1 in 100 chance of developing type 2 diabetes within 5 years. Consider lifestyle modifications to maintain low risk."
            }
        elif score <= 8:
            return {
                "stage": "Intermediate Risk",
                "description": "6-8 points",
                "interpretation": "Approximately 1 in 50 chance of developing type 2 diabetes within 5 years. Lifestyle modifications strongly recommended."
            }
        elif score <= 11:
            return {
                "stage": "Intermediate Risk",
                "description": "9-11 points",
                "interpretation": "Approximately 1 in 30 chance of developing type 2 diabetes within 5 years. Lifestyle modifications strongly recommended, consider consulting healthcare provider."
            }
        elif score <= 15:
            return {
                "stage": "High Risk",
                "description": "12-15 points",
                "interpretation": "Approximately 1 in 14 chance of developing type 2 diabetes within 5 years. See your doctor about your risk of diabetes and consider blood glucose testing."
            }
        elif score <= 19:
            return {
                "stage": "High Risk",
                "description": "16-19 points",
                "interpretation": "Approximately 1 in 7 chance of developing type 2 diabetes within 5 years. See your doctor about your risk of diabetes. Blood glucose testing strongly recommended."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "20 or more points",
                "interpretation": "Approximately 1 in 3 chance of developing type 2 diabetes within 5 years. See your doctor about your risk of diabetes as soon as possible. You may already have diabetes."
            }


def calculate_ausdrisk(age: str, sex: str, ethnicity: str, parental_diabetes: str,
                      high_blood_glucose_history: str, antihypertensive_medication: str,
                      current_smoker: str, physical_activity: str, 
                      waist_circumference_category: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AusdriskCalculator()
    return calculator.calculate(age, sex, ethnicity, parental_diabetes,
                              high_blood_glucose_history, antihypertensive_medication,
                              current_smoker, physical_activity, waist_circumference_category)