"""
Fibrosis-4 (FIB-4) Index for Liver Fibrosis Calculator

Non-invasive estimate of liver scarring in HCV and HBV patients, to assess need for biopsy.

References:
- Sterling RK, et al. Development of a simple noninvasive index to predict significant 
  fibrosis in patients with HIV/HCV coinfection. Hepatology. 2006;43(6):1317-25.
- Vallet-Pichard A, et al. FIB-4: an inexpensive and accurate marker of fibrosis in 
  HCV infection. Hepatology. 2007;46(1):32-6.
"""

import math
from typing import Dict, Any


class Fibrosis4IndexCalculator:
    """Calculator for Fibrosis-4 (FIB-4) Index for Liver Fibrosis"""
    
    def __init__(self):
        # Interpretation thresholds
        self.LOW_RISK_THRESHOLD = 1.45
        self.HIGH_RISK_THRESHOLD = 3.25
    
    def calculate(self, age: int, ast: float, alt: float, 
                 platelet_count: float) -> Dict[str, Any]:
        """
        Calculates the FIB-4 index using the provided parameters
        
        Formula: FIB-4 = (Age × AST) / (Platelet count × √ALT)
        
        Args:
            age (int): Patient's age in years
            ast (float): Aspartate aminotransferase (AST) in U/L
            alt (float): Alanine aminotransferase (ALT) in U/L
            platelet_count (float): Platelet count in 10⁹/L
            
        Returns:
            Dict with the FIB-4 score and interpretation
        """
        
        # Validations
        self._validate_inputs(age, ast, alt, platelet_count)
        
        # Calculate FIB-4 index
        result = self._calculate_fib4(age, ast, alt, platelet_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "index",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, age, ast, alt, platelet_count):
        """Validates input parameters"""
        
        if not isinstance(age, (int, float)):
            raise ValueError("Age must be a number")
        
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        if not isinstance(ast, (int, float)):
            raise ValueError("AST must be a number")
        
        if ast < 1 or ast > 10000:
            raise ValueError("AST must be between 1 and 10000 U/L")
        
        if not isinstance(alt, (int, float)):
            raise ValueError("ALT must be a number")
        
        if alt < 1 or alt > 10000:
            raise ValueError("ALT must be between 1 and 10000 U/L")
        
        if not isinstance(platelet_count, (int, float)):
            raise ValueError("Platelet count must be a number")
        
        if platelet_count < 1 or platelet_count > 1000:
            raise ValueError("Platelet count must be between 1 and 1000 × 10⁹/L")
    
    def _calculate_fib4(self, age, ast, alt, platelet_count):
        """Implements the FIB-4 formula"""
        
        # FIB-4 = (Age × AST) / (Platelet count × √ALT)
        numerator = age * ast
        denominator = platelet_count * math.sqrt(alt)
        
        # Prevent division by zero
        if denominator == 0:
            raise ValueError("Invalid calculation: denominator is zero")
        
        result = numerator / denominator
        
        # Round to 2 decimal places
        return round(result, 2)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the FIB-4 score
        
        Args:
            result (float): FIB-4 index value
            
        Returns:
            Dict with interpretation
        """
        
        if result < self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low risk",
                "description": "Low risk of advanced fibrosis (F0-F1)",
                "interpretation": "Low risk for advanced fibrosis. Excludes advanced fibrosis with ~90% negative predictive value. Can avoid liver biopsy. Monitor with repeat FIB-4 every 2-3 years."
            }
        elif result < self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "Indeterminate risk",
                "description": "Indeterminate risk (F2-F3)",
                "interpretation": "Indeterminate risk for advanced fibrosis. Consider second-line testing (elastography, FibroTest, or liver biopsy). Close monitoring required."
            }
        else:
            return {
                "stage": "High risk",
                "description": "High risk of advanced fibrosis/cirrhosis (F3-F4)",
                "interpretation": "High risk for advanced fibrosis/cirrhosis. Suggests advanced fibrosis with 97% specificity. Refer to hepatologist. Consider liver biopsy or elastography for confirmation."
            }


def calculate_fibrosis_4_index(age, ast, alt, platelet_count) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Fibrosis4IndexCalculator()
    return calculator.calculate(age, ast, alt, platelet_count)