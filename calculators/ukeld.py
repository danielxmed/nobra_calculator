"""
United Kingdom Model for End-Stage Liver Disease (UKELD) Calculator

Predicts mortality in end-stage liver disease patients for liver transplant planning.
Developed specifically for UK population to determine eligibility for liver transplantation.

References:
- Neuberger J, Gimson A, Davies M, Akyol M, O'Grady J, Burroughs A, Hudson M. 
  Selection of patients for liver transplantation and allocation of donated livers in the UK. 
  Gut. 2008;57(2):252-7.
- Barber K, Madden S, Allen J, Collett D, Neuberger J, Gimson A. 
  Elective liver transplant list mortality: development of a United Kingdom end-stage liver disease score. 
  Transplantation. 2011;92(4):469-76.
"""

import math
from typing import Dict, Any


class UkeldCalculator:
    """Calculator for United Kingdom Model for End-Stage Liver Disease (UKELD)"""
    
    def __init__(self):
        # UKELD formula coefficients
        self.INR_COEFF = 5.395
        self.CREATININE_COEFF = 1.485
        self.BILIRUBIN_COEFF = 3.13
        self.SODIUM_COEFF = -81.565
        self.CONSTANT = 435
        
        # Clinical thresholds
        self.TRANSPLANT_THRESHOLD = 49
        self.HIGH_PRIORITY_THRESHOLD = 60
    
    def calculate(self, inr: float, creatinine_umol_l: float, bilirubin_umol_l: float, sodium_mmol_l: float) -> Dict[str, Any]:
        """
        Calculates the UKELD score using the provided laboratory parameters
        
        Args:
            inr (float): International Normalized Ratio (0.8-10.0)
            creatinine_umol_l (float): Serum creatinine in µmol/L (30-800)
            bilirubin_umol_l (float): Serum bilirubin in µmol/L (5-1000)
            sodium_mmol_l (float): Serum sodium in mmol/L (120-150)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(inr, creatinine_umol_l, bilirubin_umol_l, sodium_mmol_l)
        
        # Calculate UKELD score using natural logarithm
        ukeld_score = self._calculate_formula(inr, creatinine_umol_l, bilirubin_umol_l, sodium_mmol_l)
        
        # Get interpretation
        interpretation = self._get_interpretation(ukeld_score)
        
        return {
            "result": ukeld_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, inr: float, creatinine_umol_l: float, bilirubin_umol_l: float, sodium_mmol_l: float):
        """Validates input parameters"""
        
        # Validate INR
        if not isinstance(inr, (int, float)) or inr <= 0:
            raise ValueError("INR must be a positive number")
        if inr < 0.8 or inr > 10.0:
            raise ValueError("INR must be between 0.8 and 10.0")
        
        # Validate creatinine
        if not isinstance(creatinine_umol_l, (int, float)) or creatinine_umol_l <= 0:
            raise ValueError("Creatinine must be a positive number")
        if creatinine_umol_l < 30 or creatinine_umol_l > 800:
            raise ValueError("Creatinine must be between 30 and 800 µmol/L")
        
        # Validate bilirubin
        if not isinstance(bilirubin_umol_l, (int, float)) or bilirubin_umol_l <= 0:
            raise ValueError("Bilirubin must be a positive number")
        if bilirubin_umol_l < 5 or bilirubin_umol_l > 1000:
            raise ValueError("Bilirubin must be between 5 and 1000 µmol/L")
        
        # Validate sodium
        if not isinstance(sodium_mmol_l, (int, float)) or sodium_mmol_l <= 0:
            raise ValueError("Sodium must be a positive number")
        if sodium_mmol_l < 120 or sodium_mmol_l > 150:
            raise ValueError("Sodium must be between 120 and 150 mmol/L")
    
    def _calculate_formula(self, inr: float, creatinine_umol_l: float, bilirubin_umol_l: float, sodium_mmol_l: float) -> float:
        """
        Implements the UKELD mathematical formula
        
        UKELD = 5.395 × ln(INR) + 1.485 × ln(creatinine) + 3.13 × ln(bilirubin) - 81.565 × ln(sodium) + 435
        """
        
        try:
            # Calculate each component using natural logarithm
            inr_component = self.INR_COEFF * math.log(inr)
            creatinine_component = self.CREATININE_COEFF * math.log(creatinine_umol_l)
            bilirubin_component = self.BILIRUBIN_COEFF * math.log(bilirubin_umol_l)
            sodium_component = self.SODIUM_COEFF * math.log(sodium_mmol_l)
            
            # Calculate final UKELD score
            ukeld_score = inr_component + creatinine_component + bilirubin_component + sodium_component + self.CONSTANT
            
            # Round to 1 decimal place
            return round(ukeld_score, 1)
            
        except ValueError as e:
            raise ValueError(f"Error in UKELD calculation: {str(e)}")
    
    def _get_interpretation(self, ukeld_score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the UKELD score
        
        Args:
            ukeld_score (float): Calculated UKELD score
            
        Returns:
            Dict with interpretation details
        """
        
        if ukeld_score < self.TRANSPLANT_THRESHOLD:
            return {
                "stage": "Below Transplant Threshold",
                "description": "Low mortality risk",
                "interpretation": f"UKELD score of {ukeld_score} is below 49, indicating relatively low 1-year mortality risk (<9% without transplantation). Patient does not meet the UK criteria for liver transplant eligibility based on mortality risk alone. Continue medical management and monitor disease progression."
            }
        elif ukeld_score < self.HIGH_PRIORITY_THRESHOLD:
            return {
                "stage": "Transplant Eligible",
                "description": "Moderate to high mortality risk",
                "interpretation": f"UKELD score of {ukeld_score} meets the UK cutoff for transplant eligibility (≥49), indicating >9% 1-year mortality risk without transplantation. Patient should be evaluated for liver transplantation and placed on the waiting list if appropriate. Optimize medical management while awaiting transplant."
            }
        else:
            return {
                "stage": "High Priority Transplant",
                "description": "Very high mortality risk",
                "interpretation": f"UKELD score of {ukeld_score} predicts very high mortality risk (≥50% 1-year mortality at score ≥60). Patient has very high priority for liver transplantation. Urgent transplant evaluation and aggressive supportive care are indicated. Consider intensive care unit monitoring if clinically unstable."
            }


def calculate_ukeld(inr: float, creatinine_umol_l: float, bilirubin_umol_l: float, sodium_mmol_l: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = UkeldCalculator()
    return calculator.calculate(inr, creatinine_umol_l, bilirubin_umol_l, sodium_mmol_l)