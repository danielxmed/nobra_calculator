"""
Calcium Correction for Hypoalbuminemia and Hyperalbuminemia Calculator

Calculates corrected calcium level for patients with abnormal albumin levels.

References:
1. Payne RB, et al. Interpretation of serum calcium in patients with abnormal 
   serum proteins. Br Med J. 1973;4(5893):643-6.
2. Clase CM, et al. Albumin-corrected calcium and ionized calcium in stable 
   haemodialysis patients. Nephrol Dial Transplant. 2000;15(11):1841-6.
"""

import math
from typing import Dict, Any


class CalciumCorrectionCalculator:
    """Calculator for Calcium Correction for Hypoalbuminemia and Hyperalbuminemia"""
    
    def __init__(self):
        # Normal albumin values for calculation
        self.NORMAL_ALBUMIN_US = 4.0  # g/dL
        self.NORMAL_ALBUMIN_SI = 40.0  # g/L
        
        # Correction factors
        self.CORRECTION_FACTOR_US = 0.8
        self.CORRECTION_FACTOR_SI = 0.02
        
        # Normal calcium ranges for interpretation
        self.CALCIUM_NORMAL_MIN_US = 8.5  # mg/dL
        self.CALCIUM_NORMAL_MAX_US = 10.5  # mg/dL
        self.CALCIUM_NORMAL_MIN_SI = 2.125  # mmol/L
        self.CALCIUM_NORMAL_MAX_SI = 2.625  # mmol/L
    
    def calculate(self, calcium: float, albumin: float, 
                  unit_system: str = "us") -> Dict[str, Any]:
        """
        Calculates the corrected calcium level
        
        Args:
            calcium (float): Total serum calcium level (mg/dL for US, mmol/L for SI)
            albumin (float): Serum albumin level (g/dL for US, g/L for SI)
            unit_system (str): Unit system - "us" or "si"
            
        Returns:
            Dict with the corrected calcium and interpretation
        """
        
        # Validations
        self._validate_inputs(calcium, albumin, unit_system)
        
        # Calculate corrected calcium based on unit system
        if unit_system == "us":
            # US Formula: Corrected Ca = [0.8 × (4 - Patient's Albumin)] + Serum Ca
            albumin_deficit = self.NORMAL_ALBUMIN_US - albumin
            correction = self.CORRECTION_FACTOR_US * albumin_deficit
            corrected_calcium = calcium + correction
            unit = "mg/dL"
            
            # Get interpretation based on US normal ranges
            interpretation = self._get_interpretation_us(corrected_calcium)
            
        else:  # SI units
            # SI Formula: Corrected Ca = Total Ca + 0.02 × (40 - Albumin)
            albumin_deficit = self.NORMAL_ALBUMIN_SI - albumin
            correction = self.CORRECTION_FACTOR_SI * albumin_deficit
            corrected_calcium = calcium + correction
            unit = "mmol/L"
            
            # Get interpretation based on SI normal ranges
            interpretation = self._get_interpretation_si(corrected_calcium)
        
        # Round to 2 decimal places
        corrected_calcium = round(corrected_calcium, 2)
        
        return {
            "result": corrected_calcium,
            "unit": unit,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "original_calcium": calcium,
                "albumin": albumin,
                "albumin_deficit": round(albumin_deficit, 2),
                "correction_applied": round(correction, 2),
                "unit_system": unit_system
            }
        }
    
    def _validate_inputs(self, calcium, albumin, unit_system):
        """Validates input parameters"""
        
        if not isinstance(calcium, (int, float)):
            raise ValueError("Calcium must be a number")
        
        if not isinstance(albumin, (int, float)):
            raise ValueError("Albumin must be a number")
        
        if unit_system not in ["us", "si"]:
            raise ValueError("Unit system must be 'us' or 'si'")
        
        if unit_system == "us":
            # US unit validations
            if calcium < 4 or calcium > 18:
                raise ValueError("Calcium must be between 4 and 18 mg/dL")
            
            if albumin < 0 or albumin > 7:
                raise ValueError("Albumin must be between 0 and 7 g/dL")
        else:
            # SI unit validations
            if calcium < 1 or calcium > 4.5:
                raise ValueError("Calcium must be between 1 and 4.5 mmol/L")
            
            if albumin < 0 or albumin > 70:
                raise ValueError("Albumin must be between 0 and 70 g/L")
    
    def _get_interpretation_us(self, corrected_calcium: float) -> Dict[str, str]:
        """
        Determines the interpretation based on US unit ranges
        
        Args:
            corrected_calcium (float): Corrected calcium in mg/dL
            
        Returns:
            Dict with interpretation
        """
        
        if corrected_calcium < self.CALCIUM_NORMAL_MIN_US:
            return {
                "stage": "Hypocalcemia",
                "description": "Low corrected calcium",
                "interpretation": (
                    "Consider evaluation for hypocalcemia. Confirm with ionized "
                    "calcium measurement. Common causes include hypoparathyroidism, "
                    "vitamin D deficiency, chronic kidney disease, or medications."
                )
            }
        elif corrected_calcium <= self.CALCIUM_NORMAL_MAX_US:
            return {
                "stage": "Normal",
                "description": "Normal corrected calcium",
                "interpretation": (
                    "Calcium level is within normal range when adjusted for albumin. "
                    "No immediate intervention needed based on calcium level alone."
                )
            }
        else:
            return {
                "stage": "Hypercalcemia",
                "description": "High corrected calcium",
                "interpretation": (
                    "Consider evaluation for hypercalcemia. Confirm with ionized "
                    "calcium measurement. Common causes include hyperparathyroidism, "
                    "malignancy, vitamin D intoxication, or medications."
                )
            }
    
    def _get_interpretation_si(self, corrected_calcium: float) -> Dict[str, str]:
        """
        Determines the interpretation based on SI unit ranges
        
        Args:
            corrected_calcium (float): Corrected calcium in mmol/L
            
        Returns:
            Dict with interpretation
        """
        
        if corrected_calcium < self.CALCIUM_NORMAL_MIN_SI:
            return {
                "stage": "Hypocalcemia",
                "description": "Low corrected calcium",
                "interpretation": (
                    "Consider evaluation for hypocalcemia. Confirm with ionized "
                    "calcium measurement. Common causes include hypoparathyroidism, "
                    "vitamin D deficiency, chronic kidney disease, or medications."
                )
            }
        elif corrected_calcium <= self.CALCIUM_NORMAL_MAX_SI:
            return {
                "stage": "Normal",
                "description": "Normal corrected calcium",
                "interpretation": (
                    "Calcium level is within normal range when adjusted for albumin. "
                    "No immediate intervention needed based on calcium level alone."
                )
            }
        else:
            return {
                "stage": "Hypercalcemia",
                "description": "High corrected calcium",
                "interpretation": (
                    "Consider evaluation for hypercalcemia. Confirm with ionized "
                    "calcium measurement. Common causes include hyperparathyroidism, "
                    "malignancy, vitamin D intoxication, or medications."
                )
            }


def calculate_calcium_correction(calcium, albumin, unit_system="us") -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CalciumCorrectionCalculator()
    return calculator.calculate(calcium, albumin, unit_system)