"""
FINDRISC (Finnish Diabetes Risk Score) Calculator

Calculates the 10-year risk of developing type 2 diabetes based on non-laboratory parameters.

References:
- Lindström J, Tuomilehto J. Diabetes Care. 2003;26(3):725-31.
- Saaristo T, et al. Diab Vasc Dis Res. 2005;2(2):67-72.
"""

from typing import Dict, Any


class FindriscCalculator:
    """Calculator for FINDRISC (Finnish Diabetes Risk Score)"""
    
    def __init__(self):
        # Define point values for each parameter
        self.AGE_POINTS = {
            "under_45": 0,
            "45_to_54": 2,
            "55_to_64": 3,
            "over_64": 4
        }
        
        self.BMI_POINTS = {
            "under_25": 0,
            "25_to_30": 1,
            "over_30": 3
        }
        
        # Waist circumference points depend on gender
        self.WAIST_POINTS_MALE = {
            "normal": 0,      # <94 cm
            "elevated": 3,    # 94-102 cm
            "high": 4         # ≥102 cm
        }
        
        self.WAIST_POINTS_FEMALE = {
            "normal": 0,      # <80 cm
            "elevated": 3,    # 80-88 cm
            "high": 4         # ≥88 cm
        }
        
        self.FAMILY_HISTORY_POINTS = {
            "none": 0,
            "second_degree": 3,
            "first_degree": 5
        }
    
    def calculate(self, age: str, bmi: str, waist_circumference: str, gender: str,
                 physical_activity: str, fruit_vegetable_consumption: str,
                 blood_pressure_medication: str, high_blood_glucose_history: str,
                 family_diabetes_history: str) -> Dict[str, Any]:
        """
        Calculates the FINDRISC score
        
        Args:
            age: Age category (under_45, 45_to_54, 55_to_64, over_64)
            bmi: BMI category (under_25, 25_to_30, over_30)
            waist_circumference: Waist category (normal, elevated, high)
            gender: Patient gender (male, female)
            physical_activity: Physical activity ≥30 min/day (yes, no)
            fruit_vegetable_consumption: Daily consumption (yes, no)
            blood_pressure_medication: Antihypertensive medication (yes, no)
            high_blood_glucose_history: Previous high blood glucose (yes, no)
            family_diabetes_history: Family history (none, second_degree, first_degree)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, bmi, waist_circumference, gender, physical_activity,
                            fruit_vegetable_consumption, blood_pressure_medication,
                            high_blood_glucose_history, family_diabetes_history)
        
        # Calculate total score
        score = 0
        
        # Age points
        score += self.AGE_POINTS[age]
        
        # BMI points
        score += self.BMI_POINTS[bmi]
        
        # Waist circumference points (gender-specific)
        if gender == "male":
            score += self.WAIST_POINTS_MALE[waist_circumference]
        else:
            score += self.WAIST_POINTS_FEMALE[waist_circumference]
        
        # Physical activity points
        if physical_activity == "no":
            score += 2
        
        # Fruit/vegetable consumption points
        if fruit_vegetable_consumption == "no":
            score += 1
        
        # Blood pressure medication points
        if blood_pressure_medication == "yes":
            score += 2
        
        # High blood glucose history points
        if high_blood_glucose_history == "yes":
            score += 5
        
        # Family history points
        score += self.FAMILY_HISTORY_POINTS[family_diabetes_history]
        
        # Get interpretation
        interpretation = self._get_interpretation(score, gender)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, bmi, waist_circumference, gender,
                        physical_activity, fruit_vegetable_consumption,
                        blood_pressure_medication, high_blood_glucose_history,
                        family_diabetes_history):
        """Validates input parameters"""
        
        # Validate age
        if age not in self.AGE_POINTS:
            raise ValueError(f"Invalid age category. Must be one of: {list(self.AGE_POINTS.keys())}")
        
        # Validate BMI
        if bmi not in self.BMI_POINTS:
            raise ValueError(f"Invalid BMI category. Must be one of: {list(self.BMI_POINTS.keys())}")
        
        # Validate waist circumference
        valid_waist_categories = ["normal", "elevated", "high"]
        if waist_circumference not in valid_waist_categories:
            raise ValueError(f"Invalid waist circumference category. Must be one of: {valid_waist_categories}")
        
        # Validate gender
        if gender not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        # Validate yes/no parameters
        yes_no_params = {
            "physical_activity": physical_activity,
            "fruit_vegetable_consumption": fruit_vegetable_consumption,
            "blood_pressure_medication": blood_pressure_medication,
            "high_blood_glucose_history": high_blood_glucose_history
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate family history
        if family_diabetes_history not in self.FAMILY_HISTORY_POINTS:
            raise ValueError(f"Invalid family history. Must be one of: {list(self.FAMILY_HISTORY_POINTS.keys())}")
    
    def _get_interpretation(self, score: int, gender: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and gender
        
        Args:
            score: Calculated FINDRISC score
            gender: Patient gender (for risk percentage)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            risk_percent = "0.3%" if gender == "male" else "0.1%"
            return {
                "stage": "Very Low",
                "description": "Very low risk",
                "interpretation": f"Estimated 1 in 100 will develop diabetes within 10 years. 10-year risk: {risk_percent}"
            }
        elif score <= 8:
            risk_percent = "0.8%" if gender == "male" else "0.4%"
            return {
                "stage": "Low",
                "description": "Low risk", 
                "interpretation": f"Estimated 1 in 25 will develop diabetes within 10 years. 10-year risk: {risk_percent}"
            }
        elif score <= 12:
            risk_percent = "2.6%" if gender == "male" else "2.2%"
            return {
                "stage": "Moderate",
                "description": "Moderate risk",
                "interpretation": f"Estimated 1 in 6 will develop diabetes within 10 years. 10-year risk: {risk_percent}"
            }
        elif score <= 20:
            risk_percent = "23.1%" if gender == "male" else "14.1%"
            return {
                "stage": "High",
                "description": "High risk",
                "interpretation": f"Estimated 1 in 3 will develop diabetes within 10 years. 10-year risk: {risk_percent}. Consider lifestyle changes and possibly medication"
            }
        else:
            return {
                "stage": "Very High",
                "description": "Very high risk",
                "interpretation": "Estimated 1 in 2 will develop diabetes within 10 years. 10-year risk: 50%. Lifestyle changes needed; consider medications to prevent diabetes"
            }


def calculate_findrisc(age, bmi, waist_circumference, gender, physical_activity,
                      fruit_vegetable_consumption, blood_pressure_medication,
                      high_blood_glucose_history, family_diabetes_history) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_findrisc pattern
    """
    calculator = FindriscCalculator()
    return calculator.calculate(age, bmi, waist_circumference, gender,
                              physical_activity, fruit_vegetable_consumption,
                              blood_pressure_medication, high_blood_glucose_history,
                              family_diabetes_history)