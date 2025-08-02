"""
MDRD GFR Equation Calculator

Estimates glomerular filtration rate (GFR) based on serum creatinine and patient
characteristics using the Modification of Diet in Renal Disease (MDRD) equation.

Reference:
Levey AS, Coresh J, Greene T, et al. Using standardized serum creatinine values in the 
modification of diet in renal disease study equation for estimating glomerular filtration 
rate. Ann Intern Med. 2006;145(4):247-54.
"""

import math
from typing import Dict, Any


class MdrdGfrCalculator:
    """Calculator for MDRD GFR Equation"""
    
    def __init__(self):
        # MDRD equation constants (IDMS-traceable version)
        self.CONSTANT = 175
        self.CREATININE_EXPONENT = -1.154
        self.AGE_EXPONENT = -0.203
        self.BLACK_RACE_FACTOR = 1.212
        self.FEMALE_FACTOR = 0.742
    
    def calculate(self, creatinine: float, age: float, sex: str, black_race: str) -> Dict[str, Any]:
        """
        Calculates GFR using the MDRD equation
        
        Args:
            creatinine (float): Serum creatinine in mg/dL
            age (float): Patient age in years
            sex (str): Patient sex ("male" or "female")
            black_race (str): "yes" if patient identifies as Black/African American, "no" otherwise
            
        Returns:
            Dict with the GFR result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(creatinine, age, sex, black_race)
        
        # Calculate GFR using MDRD equation
        gfr = self._calculate_gfr(creatinine, age, sex, black_race)
        
        # Get interpretation based on GFR
        interpretation = self._get_interpretation(gfr)
        
        return {
            "result": gfr,
            "unit": "mL/min/1.73 m²",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, creatinine: float, age: float, sex: str, black_race: str):
        """Validates input parameters"""
        
        # Validate creatinine
        if not isinstance(creatinine, (int, float)):
            raise ValueError("Creatinine must be a number")
        if creatinine < 0.1 or creatinine > 20.0:
            raise ValueError("Creatinine must be between 0.1 and 20.0 mg/dL")
        
        # Validate age
        if not isinstance(age, (int, float)):
            raise ValueError("Age must be a number")
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        # Validate black_race
        if black_race not in ["yes", "no"]:
            raise ValueError("Black race must be 'yes' or 'no'")
    
    def _calculate_gfr(self, creatinine: float, age: float, sex: str, black_race: str) -> float:
        """
        Implements the MDRD GFR equation
        
        Formula: GFR = 175 × (Serum Cr)^-1.154 × (age)^-0.203 × 1.212 (if Black) × 0.742 (if female)
        """
        
        # Base calculation
        gfr = self.CONSTANT * math.pow(creatinine, self.CREATININE_EXPONENT) * math.pow(age, self.AGE_EXPONENT)
        
        # Apply race adjustment if applicable
        if black_race == "yes":
            gfr *= self.BLACK_RACE_FACTOR
        
        # Apply sex adjustment if female
        if sex == "female":
            gfr *= self.FEMALE_FACTOR
        
        # Round to 1 decimal place
        return round(gfr, 1)
    
    def _get_interpretation(self, gfr: float) -> Dict[str, str]:
        """
        Determines the CKD stage and interpretation based on GFR
        
        Args:
            gfr (float): Calculated GFR value
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if gfr >= 90:
            return {
                "stage": "G1",
                "description": "Normal or high",
                "interpretation": "Normal kidney function or hyperfiltration. If evidence of kidney damage (proteinuria, hematuria, pathologic abnormalities, or imaging abnormalities), this represents CKD stage 1."
            }
        elif gfr >= 60:
            return {
                "stage": "G2",
                "description": "Mildly decreased",
                "interpretation": "Mildly reduced kidney function. If evidence of kidney damage, this represents CKD stage 2. Monitor annually."
            }
        elif gfr >= 45:
            return {
                "stage": "G3a",
                "description": "Mildly to moderately decreased",
                "interpretation": "Moderate reduction in kidney function (CKD stage 3a). Monitor every 6 months. Consider nephrology referral."
            }
        elif gfr >= 30:
            return {
                "stage": "G3b",
                "description": "Moderately to severely decreased",
                "interpretation": "Moderate reduction in kidney function (CKD stage 3b). Monitor every 3 months. Nephrology referral recommended."
            }
        elif gfr >= 15:
            return {
                "stage": "G4",
                "description": "Severely decreased",
                "interpretation": "Severe reduction in kidney function (CKD stage 4). Monitor every 3 months. Urgent nephrology referral. Prepare for renal replacement therapy."
            }
        else:
            return {
                "stage": "G5",
                "description": "Kidney failure",
                "interpretation": "Kidney failure (CKD stage 5). Immediate nephrology referral if not already under care. Initiate renal replacement therapy (dialysis or transplant) if uremic."
            }


def calculate_mdrd_gfr(creatinine: float, age: float, sex: str, black_race: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_mdrd_gfr pattern
    """
    calculator = MdrdGfrCalculator()
    return calculator.calculate(creatinine, age, sex, black_race)