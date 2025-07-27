"""
CKD-EPI 2021 Calculator

Implements the CKD-EPI 2021 equation to estimate glomerular filtration rate (eGFR)
based on serum creatinine, age, and sex.

Formula: eGFR = 142 × min(SCr/κ,1)^α × max(SCr/κ,1)^(-1.200) × 0.9938^Age × 1.012 [if female]

Where:
- κ = 0.7 for females, 0.9 for males
- α = -0.241 for females, -0.302 for males
"""

import math
from typing import Dict, Any


class CKDEpi2021Calculator:
    """Calculator for CKD-EPI 2021"""
    
    def __init__(self):
        # Formula constants
        self.KAPPA_FEMALE = 0.7
        self.KAPPA_MALE = 0.9
        self.ALPHA_FEMALE = -0.241
        self.ALPHA_MALE = -0.302
        self.BASE_MULTIPLIER = 142
        self.AGE_FACTOR = 0.9938
        self.FEMALE_MULTIPLIER = 1.012
        self.CREATININE_EXPONENT = -1.200
    
    def calculate(self, sex: str, age: int, serum_creatinine: float) -> Dict[str, Any]:
        """
        Calculates eGFR using the CKD-EPI 2021 equation
        
        Args:
            sex (str): "male" or "female"
            age (int): Age in years
            serum_creatinine (float): Serum creatinine in mg/dL
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(sex, age, serum_creatinine)
        
        # Determine constants based on sex
        if sex.lower() == "female":
            kappa = self.KAPPA_FEMALE
            alpha = self.ALPHA_FEMALE
            sex_multiplier = self.FEMALE_MULTIPLIER
        else:
            kappa = self.KAPPA_MALE
            alpha = self.ALPHA_MALE
            sex_multiplier = 1.0
        
        # Calculate creatinine/kappa ratio
        scr_kappa_ratio = serum_creatinine / kappa
        
        # Apply min and max functions
        min_term = min(scr_kappa_ratio, 1.0)
        max_term = max(scr_kappa_ratio, 1.0)
        
        # Calculate each component of the formula
        min_component = math.pow(min_term, alpha)
        max_component = math.pow(max_term, self.CREATININE_EXPONENT)
        age_component = math.pow(self.AGE_FACTOR, age)
        
        # Calculate final eGFR
        egfr = (self.BASE_MULTIPLIER * 
                min_component * 
                max_component * 
                age_component * 
                sex_multiplier)
        
        # Round to 1 decimal place
        egfr = round(egfr, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(egfr)
        
        return {
            "result": egfr,
            "unit": "mL/min/1.73 m²",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sex: str, age: int, serum_creatinine: float):
        """Validates input parameters"""
        
        if sex.lower() not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(serum_creatinine, (int, float)) or serum_creatinine <= 0:
            raise ValueError("Serum creatinine must be a positive value")
        
        if serum_creatinine < 0.1 or serum_creatinine > 20.0:
            raise ValueError("Serum creatinine must be between 0.1 and 20.0 mg/dL")
    
    def _get_interpretation(self, egfr: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the eGFR value
        
        Args:
            egfr (float): Estimated glomerular filtration rate
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if egfr >= 90:
            return {
                "stage": "G1",
                "description": "Normal or high kidney function",
                "interpretation": "Normal or high GFR. Investigate for presence of kidney damage (proteinuria, hematuria, structural abnormalities) to determine if CKD is present. If no kidney damage, no CKD diagnosis. Continue routine health maintenance."
            }
        elif egfr >= 60:
            return {
                "stage": "G2",
                "description": "Mild decrease in GFR",
                "interpretation": "Mild decrease in GFR. Investigate for presence of kidney damage (proteinuria, hematuria, structural abnormalities) to determine if CKD is present. If no kidney damage and age >65, may be normal aging. Monitor annually."
            }
        elif egfr >= 45:
            return {
                "stage": "G3a",
                "description": "Mild to moderate decrease in GFR",
                "interpretation": "Stage 3a Chronic Kidney Disease. Nephrology referral recommended within 6 months. Evaluate and treat complications (anemia, bone disease, acidosis). Monitor every 6 months. Blood pressure target <130/80. Consider ACE inhibitor/ARB if proteinuria present."
            }
        elif egfr >= 30:
            return {
                "stage": "G3b",
                "description": "Moderate to severe decrease in GFR",
                "interpretation": "Stage 3b Chronic Kidney Disease. Urgent nephrology referral within 1-3 months. Actively manage complications (anemia, mineral bone disorder, acidosis, hyperkalemia). Monitor every 3-6 months. Optimize blood pressure control. Prepare for renal replacement therapy education."
            }
        elif egfr >= 15:
            return {
                "stage": "G4",
                "description": "Severe decrease in GFR",
                "interpretation": "Stage 4 Chronic Kidney Disease. Immediate nephrology referral within 2-4 weeks. Intensive management of complications. Monitor monthly to every 3 months. Begin renal replacement therapy preparation: patient education, access planning, transplant evaluation. Consider palliative care consultation if appropriate."
            }
        else:
            return {
                "stage": "G5",
                "description": "Kidney failure",
                "interpretation": "Stage 5 Chronic Kidney Disease (kidney failure). Immediate nephrology referral within 1-2 weeks. Kidney replacement therapy (dialysis or transplant) is necessary. Urgent dialysis access creation if not already present. Expedite transplant evaluation if candidate. Manage uremic symptoms and complications."
            }


def calculate_ckd_epi_2021(sex: str, age: int, serum_creatinine: float) -> Dict[str, Any]:
    """
    Convenience function to calculate CKD-EPI 2021
    
    Args:
        sex (str): "male" or "female"
        age (int): Age in years
        serum_creatinine (float): Serum creatinine in mg/dL
        
    Returns:
        Dict with the result and interpretation
    """
    calculator = CKDEpi2021Calculator()
    return calculator.calculate(sex, age, serum_creatinine)
