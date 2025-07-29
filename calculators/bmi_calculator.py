"""
BMI Calculator (Body Mass Index and BSA) Calculator

Calculates body mass index (BMI) and body surface area (BSA) based on height and weight.
BMI provides assessment of weight appropriateness and health risk screening.
BSA is used for medication dosing calculations and cardiac index measurements.

References:
1. World Health Organization. Obesity: preventing and managing the global epidemic. 
   Report of a WHO consultation. World Health Organ Tech Rep Ser. 2000;894:i-xii, 1-253.
2. Mosteller RD. Simplified calculation of body-surface area. N Engl J Med. 1987 Oct 22;317(17):1098.
3. National Institutes of Health. Clinical Guidelines on the Identification, Evaluation, 
   and Treatment of Overweight and Obesity in Adults--The Evidence Report. Obes Res. 1998 Sep;6 Suppl 2:51S-209S.
"""

import math
from typing import Dict, Any


class BmiCalculatorCalculator:
    """Calculator for BMI and BSA using standard medical formulas"""
    
    def __init__(self):
        # BMI classification thresholds (WHO standards)
        self.BMI_THRESHOLDS = {
            'underweight': (0, 18.5),
            'normal': (18.5, 25.0),
            'overweight': (25.0, 30.0),
            'obese_class1': (30.0, 35.0),
            'obese_class2': (35.0, 40.0),
            'obese_class3': (40.0, float('inf'))
        }
    
    def calculate(self, weight: float, height: float) -> Dict[str, Any]:
        """
        Calculates BMI and BSA using standard medical formulas
        
        Args:
            weight (float): Patient weight in kilograms
            height (float): Patient height in centimeters
            
        Returns:
            Dict with BMI, BSA, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(weight, height)
        
        # Calculate BMI and BSA
        bmi = self._calculate_bmi(weight, height)
        bsa = self._calculate_bsa_mosteller(weight, height)
        
        # Get BMI interpretation
        bmi_interpretation = self._get_bmi_interpretation(bmi)
        
        # Format results
        results = {
            'bmi': round(bmi, 1),
            'bsa': round(bsa, 2),
            'height_meters': round(height / 100, 2),
            'weight_kg': weight
        }
        
        return {
            "result": results,
            "unit": "BMI: kg/m², BSA: m²",
            "interpretation": self._format_interpretation(results, bmi_interpretation),
            "stage": bmi_interpretation["stage"],
            "stage_description": bmi_interpretation["description"]
        }
    
    def _validate_inputs(self, weight: float, height: float):
        """Validates input parameters"""
        
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("Weight must be a positive number")
        
        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive number")
        
        if weight < 0.5 or weight > 500:
            raise ValueError("Weight must be between 0.5 and 500 kg")
        
        if height < 30 or height > 250:
            raise ValueError("Height must be between 30 and 250 cm")
    
    def _calculate_bmi(self, weight: float, height: float) -> float:
        """
        Calculates Body Mass Index using standard formula
        
        Formula: BMI = weight (kg) / [height (m)]²
        
        Args:
            weight (float): Weight in kilograms
            height (float): Height in centimeters
            
        Returns:
            float: BMI in kg/m²
        """
        height_meters = height / 100  # Convert cm to meters
        bmi = weight / (height_meters ** 2)
        return bmi
    
    def _calculate_bsa_mosteller(self, weight: float, height: float) -> float:
        """
        Calculates Body Surface Area using Mosteller formula
        
        Formula: BSA (m²) = √[height (cm) × weight (kg) / 3600]
        
        Args:
            weight (float): Weight in kilograms
            height (float): Height in centimeters
            
        Returns:
            float: BSA in m²
        """
        bsa = math.sqrt((height * weight) / 3600)
        return bsa
    
    def _get_bmi_interpretation(self, bmi: float) -> Dict[str, str]:
        """
        Determines BMI classification and clinical interpretation
        
        Args:
            bmi (float): Calculated BMI value
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if bmi < 18.5:
            return {
                "stage": "Underweight",
                "description": "BMI less than 18.5",
                "interpretation": "Below normal weight. May indicate malnutrition, eating disorders, or underlying medical conditions. Consider nutritional assessment and medical evaluation."
            }
        elif bmi < 25.0:
            return {
                "stage": "Normal weight",
                "description": "BMI 18.5-24.9",
                "interpretation": "Healthy weight range. Associated with lowest risk of weight-related health problems. Continue current lifestyle and eating habits."
            }
        elif bmi < 30.0:
            return {
                "stage": "Overweight",
                "description": "BMI 25.0-29.9",
                "interpretation": "Above normal weight. Increased risk of cardiovascular disease, type 2 diabetes, and other health conditions. Consider lifestyle modifications including diet and exercise."
            }
        elif bmi < 35.0:
            return {
                "stage": "Obese (Class 1)",
                "description": "BMI 30.0-34.9",
                "interpretation": "Moderate obesity. Significantly increased risk of health complications. Recommend comprehensive weight management program including dietary changes, physical activity, and medical monitoring."
            }
        elif bmi < 40.0:
            return {
                "stage": "Obese (Class 2)",
                "description": "BMI 35.0-39.9",
                "interpretation": "Severe obesity. High risk of serious health complications including cardiovascular disease, diabetes, and sleep apnea. Consider intensive medical intervention and possibly bariatric surgery evaluation."
            }
        else:  # bmi >= 40.0
            return {
                "stage": "Obese (Class 3)",
                "description": "BMI ≥40.0",
                "interpretation": "Extreme obesity (morbid obesity). Very high risk of life-threatening health complications. Requires immediate medical intervention and consideration of bariatric surgery or other intensive treatments."
            }
    
    def _format_interpretation(self, results: Dict[str, Any], bmi_interpretation: Dict[str, str]) -> str:
        """
        Formats comprehensive clinical interpretation
        
        Args:
            results (dict): Calculation results
            bmi_interpretation (dict): BMI classification information
            
        Returns:
            str: Formatted interpretation text
        """
        
        interpretation = (
            f"BMI: {results['bmi']} kg/m² ({bmi_interpretation['stage']}). "
            f"BSA: {results['bsa']} m² (Mosteller formula). "
            f"Height: {results['height_meters']} m, Weight: {results['weight_kg']} kg. "
            f"{bmi_interpretation['interpretation']} "
            f"BSA is used for medication dosing calculations (especially chemotherapy) and cardiac index measurements. "
            f"BMI should be interpreted alongside other clinical assessments including waist circumference and body composition."
        )
        
        return interpretation


def calculate_bmi_calculator(weight: float, height: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BmiCalculatorCalculator()
    return calculator.calculate(weight, height)