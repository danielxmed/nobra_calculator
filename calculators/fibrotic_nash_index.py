"""
Fibrotic NASH Index (FNI) Calculator

Screens for fibrotic NASH in individuals at high risk for NAFLD.

References:
- Tavaglione F, et al. Development and Validation of a Score for Fibrotic 
  Nonalcoholic Steatohepatitis. Clin Gastroenterol Hepatol. 2023;21(6):1523-1532.e1.
"""

import math
from typing import Dict, Any


class FibroticNashIndexCalculator:
    """Calculator for Fibrotic NASH Index (FNI)"""
    
    def __init__(self):
        # Formula constants
        self.INTERCEPT = -10.33
        self.AST_COEFFICIENT = 2.54
        self.HBA1C_COEFFICIENT = 3.86
        self.HDL_COEFFICIENT = -1.66
        
        # Interpretation thresholds
        self.LOW_RISK_THRESHOLD = 0.10
        self.HIGH_RISK_THRESHOLD = 0.33
    
    def calculate(self, ast: float, hba1c: float, hdl: float) -> Dict[str, Any]:
        """
        Calculates the FNI score using the provided parameters
        
        Formula: FNI = e^x / (1 + e^x)
        Where x = -10.33 + 2.54 × ln(AST) + 3.86 × ln(HbA1c) - 1.66 × ln(HDL)
        
        Args:
            ast (float): Aspartate aminotransferase (AST) in U/L
            hba1c (float): Hemoglobin A1c in %
            hdl (float): HDL cholesterol in mg/dL
            
        Returns:
            Dict with the FNI score and interpretation
        """
        
        # Validations
        self._validate_inputs(ast, hba1c, hdl)
        
        # Calculate FNI
        result = self._calculate_fni(ast, hba1c, hdl)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "probability",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, ast, hba1c, hdl):
        """Validates input parameters"""
        
        if not isinstance(ast, (int, float)):
            raise ValueError("AST must be a number")
        
        if ast < 5 or ast > 1000:
            raise ValueError("AST must be between 5 and 1000 U/L")
        
        if not isinstance(hba1c, (int, float)):
            raise ValueError("HbA1c must be a number")
        
        if hba1c < 3 or hba1c > 20:
            raise ValueError("HbA1c must be between 3 and 20 %")
        
        if not isinstance(hdl, (int, float)):
            raise ValueError("HDL must be a number")
        
        if hdl < 10 or hdl > 200:
            raise ValueError("HDL must be between 10 and 200 mg/dL")
    
    def _calculate_fni(self, ast, hba1c, hdl):
        """Implements the FNI formula"""
        
        # Calculate x = -10.33 + 2.54 × ln(AST) + 3.86 × ln(HbA1c) - 1.66 × ln(HDL)
        x = (self.INTERCEPT + 
             self.AST_COEFFICIENT * math.log(ast) + 
             self.HBA1C_COEFFICIENT * math.log(hba1c) + 
             self.HDL_COEFFICIENT * math.log(hdl))
        
        # Calculate FNI = e^x / (1 + e^x)
        # This is the logistic function
        try:
            # Prevent overflow for large positive x
            if x > 700:
                fni = 1.0
            else:
                exp_x = math.exp(x)
                fni = exp_x / (1 + exp_x)
        except OverflowError:
            fni = 1.0
        
        # Round to 3 decimal places (as it's a probability)
        return round(fni, 3)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the FNI score
        
        Args:
            result (float): FNI score (0-1)
            
        Returns:
            Dict with interpretation
        """
        
        if result < self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Fibrotic NASH ruled out",
                "interpretation": "Fibrotic NASH can be confidently ruled out. Negative predictive value 0.93. No immediate need for liver specialist referral. Continue routine monitoring in primary care."
            }
        elif result < self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "Indeterminate Risk",
                "description": "Further evaluation needed",
                "interpretation": "Cannot rule in or rule out fibrotic NASH. Consider additional non-invasive tests (e.g., FIB-4, NAFLD fibrosis score). May warrant referral to hepatology for further evaluation."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Likely fibrotic NASH",
                "interpretation": "High probability of fibrotic NASH. Specificity ≥0.90, positive predictive value 0.57. Refer to liver specialist for further investigation. Consider liver biopsy or advanced imaging."
            }


def calculate_fibrotic_nash_index(ast, hba1c, hdl) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FibroticNashIndexCalculator()
    return calculator.calculate(ast, hba1c, hdl)