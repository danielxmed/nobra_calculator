"""
Cambridge Diabetes Risk Score Calculator

Predicts risk of having previously undiagnosed type 2 diabetes based on clinical
and demographic factors. Uses logistic regression model with seven risk factors.

References:
1. Griffin SJ, Little PS, Hales CN, Kinmonth AL, Wareham NJ. Diabetes risk score: 
   towards earlier detection of type 2 diabetes in general practice. Diabetes Metab 
   Res Rev. 2000 May-Jun;16(3):164-71.
"""

import math
from typing import Dict, Any


class CambridgeDiabetesRiskScoreCalculator:
    """Calculator for Cambridge Diabetes Risk Score"""
    
    def __init__(self):
        # Model intercept
        self.ALPHA = -6.322
        
        # Coefficients for each risk factor
        self.COEFFICIENTS = {
            'male': 0.879,
            'age_45_54': 1.222,
            'age_55_64': 1.797,
            'age_65_plus': 2.192,
            'bmi_25_27.5': 0.699,
            'bmi_27.5_30': 1.192,
            'bmi_30_plus': 2.131,
            'family_history': 0.728,
            'smoking': 0.855,
            'antihypertensive': 1.222,
            'steroid': 2.191
        }
    
    def calculate(self, gender: str, age: int, bmi_category: str, 
                  family_history: str, smoking_status: str,
                  antihypertensive_use: str, steroid_use: str) -> Dict[str, Any]:
        """
        Calculates Cambridge Diabetes Risk Score
        
        Args:
            gender (str): 'male' or 'female'
            age (int): Age in years
            bmi_category (str): BMI category
            family_history (str): 'yes' or 'no'
            smoking_status (str): 'yes' or 'no'
            antihypertensive_use (str): 'yes' or 'no'
            steroid_use (str): 'yes' or 'no'
            
        Returns:
            Dict with probability and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(gender, age, bmi_category, family_history,
                            smoking_status, antihypertensive_use, steroid_use)
        
        # Calculate linear predictor
        linear_predictor = self._calculate_linear_predictor(
            gender, age, bmi_category, family_history,
            smoking_status, antihypertensive_use, steroid_use
        )
        
        # Calculate probability
        probability = self._calculate_probability(linear_predictor)
        
        # Get interpretation
        interpretation = self._get_interpretation(probability)
        
        return {
            "result": round(probability, 3),
            "unit": "probability",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "linear_predictor": round(linear_predictor, 3),
                "percentage_risk": round(probability * 100, 1),
                "sensitivity_at_0.11": "85%",
                "specificity_at_0.11": "51%",
                "sensitivity_at_0.29": "51%",
                "specificity_at_0.29": "78%"
            }
        }
    
    def _validate_inputs(self, gender: str, age: int, bmi_category: str,
                        family_history: str, smoking_status: str,
                        antihypertensive_use: str, steroid_use: str):
        """Validates input parameters"""
        
        if gender not in ['male', 'female']:
            raise ValueError("Gender must be 'male' or 'female'")
        
        if not isinstance(age, (int, float)) or age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        valid_bmi_categories = ['under_25', '25_to_27.5', '27.5_to_30', '30_or_more']
        if bmi_category not in valid_bmi_categories:
            raise ValueError(f"BMI category must be one of: {', '.join(valid_bmi_categories)}")
        
        yes_no_params = {
            'family_history': family_history,
            'smoking_status': smoking_status,
            'antihypertensive_use': antihypertensive_use,
            'steroid_use': steroid_use
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ['yes', 'no']:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_linear_predictor(self, gender: str, age: int, bmi_category: str,
                                   family_history: str, smoking_status: str,
                                   antihypertensive_use: str, steroid_use: str) -> float:
        """Calculates the linear predictor for the logistic regression model"""
        
        # Start with intercept
        linear_predictor = self.ALPHA
        
        # Add gender coefficient
        if gender == 'male':
            linear_predictor += self.COEFFICIENTS['male']
        
        # Add age category coefficient
        if 45 <= age < 55:
            linear_predictor += self.COEFFICIENTS['age_45_54']
        elif 55 <= age < 65:
            linear_predictor += self.COEFFICIENTS['age_55_64']
        elif age >= 65:
            linear_predictor += self.COEFFICIENTS['age_65_plus']
        
        # Add BMI category coefficient
        if bmi_category == '25_to_27.5':
            linear_predictor += self.COEFFICIENTS['bmi_25_27.5']
        elif bmi_category == '27.5_to_30':
            linear_predictor += self.COEFFICIENTS['bmi_27.5_30']
        elif bmi_category == '30_or_more':
            linear_predictor += self.COEFFICIENTS['bmi_30_plus']
        
        # Add other risk factors
        if family_history == 'yes':
            linear_predictor += self.COEFFICIENTS['family_history']
        
        if smoking_status == 'yes':
            linear_predictor += self.COEFFICIENTS['smoking']
        
        if antihypertensive_use == 'yes':
            linear_predictor += self.COEFFICIENTS['antihypertensive']
        
        if steroid_use == 'yes':
            linear_predictor += self.COEFFICIENTS['steroid']
        
        return linear_predictor
    
    def _calculate_probability(self, linear_predictor: float) -> float:
        """Calculates probability using logistic function"""
        
        # Probability = 1 / (1 + e^(-linear_predictor))
        try:
            probability = 1 / (1 + math.exp(-linear_predictor))
        except OverflowError:
            # Handle extreme values
            if linear_predictor > 0:
                probability = 1.0
            else:
                probability = 0.0
        
        return probability
    
    def _get_interpretation(self, probability: float) -> Dict[str, str]:
        """
        Determines risk category and interpretation based on probability
        
        Args:
            probability (float): Calculated probability (0-1)
            
        Returns:
            Dict with interpretation details
        """
        
        if probability < 0.11:
            return {
                "stage": "Low Risk",
                "description": "Low probability of undiagnosed diabetes",
                "interpretation": (
                    "Low risk of undiagnosed type 2 diabetes. At 0.11 cutoff: "
                    "85% sensitivity, 51% specificity. Routine screening may still "
                    "be appropriate based on other clinical factors."
                )
            }
        elif probability < 0.29:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate probability of undiagnosed diabetes",
                "interpretation": (
                    "Moderate risk of undiagnosed type 2 diabetes. Consider diabetes "
                    "screening with fasting glucose or HbA1c. This range captures "
                    "most individuals with undiagnosed diabetes."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High probability of undiagnosed diabetes",
                "interpretation": (
                    "High risk of undiagnosed type 2 diabetes. At 0.29 cutoff: "
                    "51% sensitivity, 78% specificity. Strongly recommend immediate "
                    "diabetes screening with fasting glucose, HbA1c, or oral glucose "
                    "tolerance test."
                )
            }


def calculate_cambridge_diabetes_risk_score(gender: str, age: int, bmi_category: str,
                                          family_history: str, smoking_status: str,
                                          antihypertensive_use: str, 
                                          steroid_use: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CambridgeDiabetesRiskScoreCalculator()
    return calculator.calculate(
        gender, age, bmi_category, family_history,
        smoking_status, antihypertensive_use, steroid_use
    )