"""
HOMA-IR (Homeostatic Model Assessment for Insulin Resistance) Calculator

Approximates insulin resistance using fasting glucose and insulin levels.

References:
- Matthews DR, et al. Diabetologia. 1985;28(7):412-9.
- Tohidi M, et al. Clin Biochem. 2014;47(6):432-8.
"""

from typing import Dict, Any


class HomaIrCalculator:
    """Calculator for HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)"""
    
    def __init__(self):
        # Formula constant
        self.FORMULA_CONSTANT = 405
    
    def calculate(self, fasting_insulin: float, fasting_glucose: float) -> Dict[str, Any]:
        """
        Calculates the HOMA-IR score
        
        Args:
            fasting_insulin (float): Fasting insulin in μIU/mL
            fasting_glucose (float): Fasting glucose in mg/dL
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(fasting_insulin, fasting_glucose)
        
        # Calculate HOMA-IR
        # Formula: HOMA-IR = (Fasting Insulin × Fasting Glucose) / 405
        homa_ir = (fasting_insulin * fasting_glucose) / self.FORMULA_CONSTANT
        
        # Round to 2 decimal places
        homa_ir = round(homa_ir, 2)
        
        # Get interpretation
        interpretation = self._get_interpretation(homa_ir)
        
        return {
            "result": homa_ir,
            "unit": "score",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fasting_insulin: float, fasting_glucose: float):
        """Validates input parameters"""
        
        if not isinstance(fasting_insulin, (int, float)):
            raise ValueError("Fasting insulin must be a number")
        
        if not isinstance(fasting_glucose, (int, float)):
            raise ValueError("Fasting glucose must be a number")
        
        if fasting_insulin < 0.1 or fasting_insulin > 300:
            raise ValueError("Fasting insulin must be between 0.1 and 300 μIU/mL")
        
        if fasting_glucose < 10 or fasting_glucose > 600:
            raise ValueError("Fasting glucose must be between 10 and 600 mg/dL")
    
    def _get_interpretation(self, homa_ir: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the HOMA-IR score
        
        Args:
            homa_ir (float): Calculated HOMA-IR score
            
        Returns:
            Dict with interpretation
        """
        
        if homa_ir < 0.7:
            return {
                "stage": "Low",
                "description": "Below normal range",
                "interpretation": "HOMA-IR below normal range. This may indicate insulin sensitivity, "
                                "but consider clinical context."
            }
        elif homa_ir < 2.0:
            return {
                "stage": "Normal",
                "description": "Normal insulin sensitivity",
                "interpretation": "Normal insulin resistance range (0.7-2.0). No evidence of "
                                "significant insulin resistance."
            }
        elif homa_ir < 2.5:
            return {
                "stage": "Borderline",
                "description": "Borderline insulin resistance",
                "interpretation": "Borderline insulin resistance (2.0-2.5). Consider lifestyle "
                                "modifications and monitoring for metabolic syndrome risk factors."
            }
        elif homa_ir < 5.0:
            return {
                "stage": "Moderate",
                "description": "Moderate insulin resistance",
                "interpretation": "Moderate insulin resistance (2.5-5.0). Increased risk for type 2 "
                                "diabetes and metabolic syndrome. Consider comprehensive metabolic evaluation."
            }
        else:
            return {
                "stage": "Severe",
                "description": "Severe insulin resistance",
                "interpretation": "Severe insulin resistance (>5.0). High risk for type 2 diabetes "
                                "and cardiovascular disease. Recommend comprehensive evaluation and intervention."
            }


def calculate_homa_ir(fasting_insulin: float, fasting_glucose: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HomaIrCalculator()
    return calculator.calculate(fasting_insulin, fasting_glucose)