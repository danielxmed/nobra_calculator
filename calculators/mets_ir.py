"""
Metabolic Score for Insulin Resistance (METS-IR) Calculator

Predicts risk of type 2 diabetes using fasting glucose, triglycerides, BMI, and HDL cholesterol.
A non-insulin dependent marker for insulin resistance.

References:
1. Bello-Chavolla OY, et al. Eur J Endocrinol. 2018;178(5):533-544.
2. Zhang M, et al. J Diabetes. 2021;13(9):725-734.
3. Bello-Chavolla OY, et al. Clin Nutr. 2020;39(5):1613-1621.
"""

import math
from typing import Dict, Any


class MetsIrCalculator:
    """Calculator for Metabolic Score for Insulin Resistance (METS-IR)"""
    
    def __init__(self):
        # Cutoff value for risk stratification
        self.CUTOFF_VALUE = 50.39
        
        # Normal ranges for reference
        self.NORMAL_RANGES = {
            "fasting_glucose": {"min": 70, "max": 105},
            "triglycerides": {"min": 0, "max": 150},
            "bmi": {"min": 20, "max": 25},
            "hdl_cholesterol": {"min": 60, "max": 155}
        }
    
    def calculate(self, fasting_glucose: float, triglycerides: float, 
                  bmi: float, hdl_cholesterol: float) -> Dict[str, Any]:
        """
        Calculates the METS-IR score for insulin resistance assessment
        
        Args:
            fasting_glucose (float): Fasting plasma glucose in mg/dL
            triglycerides (float): Fasting triglycerides in mg/dL
            bmi (float): Body Mass Index in kg/m²
            hdl_cholesterol (float): HDL cholesterol in mg/dL
            
        Returns:
            Dict with the METS-IR score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(fasting_glucose, triglycerides, bmi, hdl_cholesterol)
        
        # Calculate METS-IR using the formula:
        # METS-IR = (ln((2 × Glucose) + Triglycerides) × BMI) / ln(HDL)
        try:
            numerator = math.log((2 * fasting_glucose) + triglycerides) * bmi
            denominator = math.log(hdl_cholesterol)
            
            if denominator == 0:
                raise ValueError("Cannot calculate METS-IR with HDL value that results in ln(HDL) = 0")
            
            mets_ir = numerator / denominator
            
            # Round to 2 decimal places
            mets_ir = round(mets_ir, 2)
            
        except ValueError as e:
            if "math domain error" in str(e):
                raise ValueError("Cannot calculate METS-IR with negative or zero values in logarithm")
            raise
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(mets_ir)
        
        return {
            "result": mets_ir,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fasting_glucose: float, triglycerides: float,
                        bmi: float, hdl_cholesterol: float):
        """Validates input parameters"""
        
        # Validate fasting glucose
        if not isinstance(fasting_glucose, (int, float)):
            raise ValueError("Fasting glucose must be a number")
        if fasting_glucose < 40 or fasting_glucose > 700:
            raise ValueError(f"Fasting glucose must be between 40 and 700 mg/dL, got {fasting_glucose}")
        
        # Validate triglycerides
        if not isinstance(triglycerides, (int, float)):
            raise ValueError("Triglycerides must be a number")
        if triglycerides < 10 or triglycerides > 2000:
            raise ValueError(f"Triglycerides must be between 10 and 2000 mg/dL, got {triglycerides}")
        
        # Validate BMI
        if not isinstance(bmi, (int, float)):
            raise ValueError("BMI must be a number")
        if bmi < 10 or bmi > 70:
            raise ValueError(f"BMI must be between 10 and 70 kg/m², got {bmi}")
        
        # Validate HDL cholesterol
        if not isinstance(hdl_cholesterol, (int, float)):
            raise ValueError("HDL cholesterol must be a number")
        if hdl_cholesterol < 10 or hdl_cholesterol > 200:
            raise ValueError(f"HDL cholesterol must be between 10 and 200 mg/dL, got {hdl_cholesterol}")
        
        # Additional validation for logarithm domain
        if (2 * fasting_glucose + triglycerides) <= 0:
            raise ValueError("The expression (2 × glucose + triglycerides) must be positive")
        if hdl_cholesterol <= 0:
            raise ValueError("HDL cholesterol must be positive for logarithm calculation")
    
    def _get_interpretation(self, mets_ir: float) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the METS-IR score
        
        Args:
            mets_ir (float): Calculated METS-IR score
            
        Returns:
            Dict with risk category, description, and clinical interpretation
        """
        
        if mets_ir <= self.CUTOFF_VALUE:
            return {
                "stage": "Low Risk",
                "description": f"METS-IR ≤{self.CUTOFF_VALUE}",
                "interpretation": (
                    "Low risk of developing Type 2 Diabetes. Continue routine screening "
                    "and maintain healthy lifestyle habits including diet and exercise."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": f"METS-IR >{self.CUTOFF_VALUE}",
                "interpretation": (
                    "High risk of developing Type 2 Diabetes. Consider more intensive "
                    "lifestyle interventions, closer monitoring of glucose levels, and "
                    "possible preventive interventions. Further evaluation with oral "
                    "glucose tolerance test may be warranted."
                )
            }


def calculate_mets_ir(fasting_glucose: float, triglycerides: float,
                     bmi: float, hdl_cholesterol: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MetsIrCalculator()
    return calculator.calculate(fasting_glucose, triglycerides, bmi, hdl_cholesterol)