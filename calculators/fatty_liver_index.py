"""
Fatty Liver Index Calculator

Diagnoses fatty liver using lab and exam findings. A simple and accurate predictor 
of hepatic steatosis in the general population.

References:
- Bedogni G, et al. The Fatty Liver Index: a simple and accurate predictor of 
  hepatic steatosis in the general population. BMC Gastroenterol. 2006;6:33.
"""

import math
from typing import Dict, Any


class FattyLiverIndexCalculator:
    """Calculator for Fatty Liver Index"""
    
    def __init__(self):
        # Formula constants
        self.TRIG_COEFFICIENT = 0.953
        self.BMI_COEFFICIENT = 0.139
        self.GGT_COEFFICIENT = 0.718
        self.WAIST_COEFFICIENT = 0.053
        self.CONSTANT = -15.745
    
    def calculate(self, triglycerides: float, bmi: float, ggt: float, 
                 waist_circumference: float) -> Dict[str, Any]:
        """
        Calculates the Fatty Liver Index using the provided parameters
        
        Args:
            triglycerides (float): Serum triglycerides in mg/dL
            bmi (float): Body Mass Index in kg/m²
            ggt (float): Gamma-glutamyl transpeptidase in U/L
            waist_circumference (float): Waist circumference in cm
            
        Returns:
            Dict with the FLI score and interpretation
        """
        
        # Validations
        self._validate_inputs(triglycerides, bmi, ggt, waist_circumference)
        
        # Calculate FLI score
        result = self._calculate_fli(triglycerides, bmi, ggt, waist_circumference)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, triglycerides, bmi, ggt, waist_circumference):
        """Validates input parameters"""
        
        # Validate triglycerides
        if not isinstance(triglycerides, (int, float)) or triglycerides <= 0:
            raise ValueError("Triglycerides must be a positive number")
        if triglycerides > 1000:
            raise ValueError("Triglycerides value seems too high (>1000 mg/dL)")
        
        # Validate BMI
        if not isinstance(bmi, (int, float)) or bmi < 10 or bmi > 60:
            raise ValueError("BMI must be between 10 and 60 kg/m²")
        
        # Validate GGT
        if not isinstance(ggt, (int, float)) or ggt <= 0:
            raise ValueError("GGT must be a positive number")
        if ggt > 1000:
            raise ValueError("GGT value seems too high (>1000 U/L)")
        
        # Validate waist circumference
        if not isinstance(waist_circumference, (int, float)) or waist_circumference < 40 or waist_circumference > 200:
            raise ValueError("Waist circumference must be between 40 and 200 cm")
    
    def _calculate_fli(self, triglycerides, bmi, ggt, waist_circumference):
        """Implements the FLI mathematical formula"""
        
        # Calculate y value using natural logarithm
        y = (self.TRIG_COEFFICIENT * math.log(triglycerides) + 
             self.BMI_COEFFICIENT * bmi + 
             self.GGT_COEFFICIENT * math.log(ggt) + 
             self.WAIST_COEFFICIENT * waist_circumference + 
             self.CONSTANT)
        
        # Calculate FLI = (e^y / (1 + e^y)) × 100
        e_y = math.exp(y)
        fli = (e_y / (1 + e_y)) * 100
        
        # Round to 1 decimal place
        return round(fli, 1)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the FLI score
        
        Args:
            result (float): FLI score (0-100)
            
        Returns:
            Dict with interpretation
        """
        
        if result < 30:
            return {
                "stage": "Low Risk",
                "description": "Fatty liver ruled out",
                "interpretation": "Fatty liver ruled out with negative likelihood ratio of 0.2. The probability of fatty liver disease is low."
            }
        elif result >= 30 and result < 60:
            return {
                "stage": "Indeterminate Risk",
                "description": "Inconclusive",
                "interpretation": "Fatty liver neither ruled in nor ruled out. Further evaluation may be needed."
            }
        else:  # result >= 60
            return {
                "stage": "High Risk",
                "description": "Fatty liver ruled in",
                "interpretation": "Fatty liver ruled in with positive likelihood ratio of 4.3. High probability of fatty liver disease. Consider further evaluation and management."
            }


def calculate_fatty_liver_index(triglycerides, bmi, ggt, waist_circumference) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FattyLiverIndexCalculator()
    return calculator.calculate(triglycerides, bmi, ggt, waist_circumference)