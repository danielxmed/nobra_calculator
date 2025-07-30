"""
CKiD U25 eGFR Calculator

Estimates glomerular filtration rate based on creatinine and/or cystatin C in 
patients aged 1 to 25 years with chronic kidney disease.

References:
1. Pierce CB, Muñoz A, Ng DK, Warady BA, Furth SL, Schwartz GJ. Age- and sex-dependent 
   clinical equations to estimate glomerular filtration rates in children and young adults 
   with chronic kidney disease. Kidney Int. 2021 Oct;100(4):948-959.
2. Schwartz GJ, Muñoz A, Schneider MF, Mak RH, Kaskel F, Warady BA, et al. New equations 
   to estimate GFR in children with CKD. J Am Soc Nephrol. 2009 Mar;20(3):629-37.
3. Levey AS, Stevens LA, Schmid CH, Zhang YL, Castro AF 3rd, Feldman HI, et al. A new 
   equation to estimate glomerular filtration rate. Ann Intern Med. 2009 May 5;150(9):604-12.
"""

import math
from typing import Dict, Any, Optional


class CkidU25EgfrCalculator:
    """Calculator for CKiD U25 eGFR"""
    
    def __init__(self):
        # Age-dependent k values for creatinine-based equations
        self.creatinine_k_values = {
            "male": {
                "1_to_12": lambda age: 39.0 * (1.008 ** (age - 12)),
                "12_to_18": lambda age: 39.0 * (1.045 ** (age - 12)),
                "18_to_25": 50.8
            },
            "female": {
                "1_to_12": lambda age: 36.1 * (1.008 ** (age - 12)),
                "12_to_18": lambda age: 36.1 * (1.023 ** (age - 12)),
                "18_to_25": 41.4
            }
        }
        
        # Age-dependent k values for cystatin C-based equations
        self.cystatin_k_values = {
            "male": {
                "1_to_12": lambda age: 70.7 * (0.990 ** (age - 12)),
                "12_to_18": lambda age: 70.7 * (0.931 ** (age - 12)),
                "18_to_25": 135.0
            },
            "female": {
                "1_to_12": lambda age: 70.7 * (0.990 ** (age - 12)),
                "12_to_18": lambda age: 70.7 * (0.969 ** (age - 12)),
                "18_to_25": 113.0
            }
        }
    
    def calculate(
        self,
        equation_type: str,
        age: int,
        sex: str,
        height: Optional[float] = None,
        serum_creatinine: Optional[float] = None,
        cystatin_c: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates CKiD U25 eGFR using specified parameters
        
        Args:
            equation_type: Type of equation ('creatinine', 'cystatin_c', 'creatinine_cystatin_c')
            age: Patient age in years (1-25)
            sex: Patient sex ('male' or 'female')
            height: Patient height in cm (required for creatinine-based equations)
            serum_creatinine: Serum creatinine in mg/dL (required for creatinine-based equations)
            cystatin_c: Cystatin C in mg/L (required for cystatin C-based equations)
            
        Returns:
            Dict with eGFR result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(equation_type, age, sex, height, serum_creatinine, cystatin_c)
        
        # Calculate eGFR based on equation type
        if equation_type == "creatinine":
            egfr = self._calculate_creatinine_egfr(age, sex, height, serum_creatinine)
            method_used = "Creatinine-based CKiD U25"
            
        elif equation_type == "cystatin_c":
            egfr = self._calculate_cystatin_egfr(age, sex, cystatin_c)
            method_used = "Cystatin C-based CKiD U25"
            
        elif equation_type == "creatinine_cystatin_c":
            creatinine_egfr = self._calculate_creatinine_egfr(age, sex, height, serum_creatinine)
            cystatin_egfr = self._calculate_cystatin_egfr(age, sex, cystatin_c)
            egfr = (creatinine_egfr + cystatin_egfr) / 2
            method_used = "Combined Creatinine-Cystatin C CKiD U25"
        
        # Get CKD stage interpretation
        ckd_interpretation = self._get_ckd_interpretation(egfr)
        
        # Generate detailed breakdown
        calculation_details = self._get_calculation_details(
            equation_type, age, sex, height, serum_creatinine, cystatin_c, egfr, method_used
        )
        
        return {
            "result": egfr,
            "unit": "mL/min/1.73m²",
            "interpretation": ckd_interpretation["interpretation"],
            "stage": ckd_interpretation["stage"],
            "stage_description": ckd_interpretation["description"],
            "calculation_details": calculation_details
        }
    
    def _validate_inputs(self, equation_type, age, sex, height, serum_creatinine, cystatin_c):
        """Validates input parameters"""
        
        # Validate equation type
        valid_types = ["creatinine", "cystatin_c", "creatinine_cystatin_c"]
        if equation_type not in valid_types:
            raise ValueError(f"Equation type must be one of {valid_types}")
        
        # Validate age
        if not isinstance(age, int) or age < 1 or age > 25:
            raise ValueError("Age must be an integer between 1 and 25 years")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        # Validate equation-specific requirements
        if equation_type in ["creatinine", "creatinine_cystatin_c"]:
            if height is None or serum_creatinine is None:
                raise ValueError("Height and serum creatinine are required for creatinine-based equations")
            
            if not isinstance(height, (int, float)) or height < 50.0 or height > 250.0:
                raise ValueError("Height must be between 50.0 and 250.0 cm")
            
            if not isinstance(serum_creatinine, (int, float)) or serum_creatinine < 0.1 or serum_creatinine > 20.0:
                raise ValueError("Serum creatinine must be between 0.1 and 20.0 mg/dL")
        
        if equation_type in ["cystatin_c", "creatinine_cystatin_c"]:
            if cystatin_c is None:
                raise ValueError("Cystatin C is required for cystatin C-based equations")
            
            if not isinstance(cystatin_c, (int, float)) or cystatin_c < 0.1 or cystatin_c > 10.0:
                raise ValueError("Cystatin C must be between 0.1 and 10.0 mg/L")
    
    def _get_k_value_creatinine(self, age: int, sex: str) -> float:
        """Gets the appropriate k value for creatinine-based calculation"""
        
        k_values = self.creatinine_k_values[sex]
        
        if age < 12:
            return k_values["1_to_12"](age)
        elif age < 18:
            return k_values["12_to_18"](age)
        else:  # age 18-25
            return k_values["18_to_25"]
    
    def _get_k_value_cystatin(self, age: int, sex: str) -> float:
        """Gets the appropriate k value for cystatin C-based calculation"""
        
        k_values = self.cystatin_k_values[sex]
        
        if age < 12:
            return k_values["1_to_12"](age)
        elif age < 18:
            return k_values["12_to_18"](age)
        else:  # age 18-25
            return k_values["18_to_25"]
    
    def _calculate_creatinine_egfr(self, age: int, sex: str, height: float, serum_creatinine: float) -> float:
        """Calculates eGFR using creatinine-based CKiD U25 equation"""
        
        k = self._get_k_value_creatinine(age, sex)
        height_m = height / 100  # Convert cm to meters
        
        egfr = k * (height_m / serum_creatinine)
        
        return round(egfr, 1)
    
    def _calculate_cystatin_egfr(self, age: int, sex: str, cystatin_c: float) -> float:
        """Calculates eGFR using cystatin C-based CKiD U25 equation"""
        
        k = self._get_k_value_cystatin(age, sex)
        
        egfr = k * (1 / cystatin_c)
        
        return round(egfr, 1)
    
    def _get_ckd_interpretation(self, egfr: float) -> Dict[str, str]:
        """
        Determines CKD stage and interpretation based on eGFR
        
        Args:
            egfr: Estimated GFR value
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if egfr >= 90:
            return {
                "stage": "G1",
                "description": "Normal or high",
                "interpretation": f"eGFR {egfr} mL/min/1.73m²: Normal kidney function. If kidney damage is present (proteinuria, hematuria, or structural abnormalities), this indicates CKD stage G1. Regular monitoring recommended."
            }
        elif egfr >= 60:
            return {
                "stage": "G2",
                "description": "Mildly decreased",
                "interpretation": f"eGFR {egfr} mL/min/1.73m²: Mildly decreased kidney function (CKD stage G2). Monitor kidney function progression and address cardiovascular risk factors."
            }
        elif egfr >= 45:
            return {
                "stage": "G3a",
                "description": "Mild to moderately decreased",
                "interpretation": f"eGFR {egfr} mL/min/1.73m²: Mild to moderate reduction in kidney function (CKD stage G3a). Evaluate and treat complications, slow progression, and prepare for renal replacement therapy."
            }
        elif egfr >= 30:
            return {
                "stage": "G3b",
                "description": "Moderately to severely decreased",
                "interpretation": f"eGFR {egfr} mL/min/1.73m²: Moderate to severe reduction in kidney function (CKD stage G3b). Evaluate and treat complications, prepare for renal replacement therapy."
            }
        elif egfr >= 15:
            return {
                "stage": "G4",
                "description": "Severely decreased",
                "interpretation": f"eGFR {egfr} mL/min/1.73m²: Severe reduction in kidney function (CKD stage G4). Prepare for renal replacement therapy (dialysis or transplantation)."
            }
        else:
            return {
                "stage": "G5",
                "description": "Kidney failure",
                "interpretation": f"eGFR {egfr} mL/min/1.73m²: Kidney failure (CKD stage G5). Renal replacement therapy (dialysis or transplantation) required or patient receiving dialysis."
            }
    
    def _get_calculation_details(self, equation_type, age, sex, height, serum_creatinine, 
                               cystatin_c, egfr, method_used) -> Dict[str, Any]:
        """Provides detailed calculation breakdown"""
        
        details = {
            "method": method_used,
            "patient_demographics": {
                "age": f"{age} years",
                "sex": sex.capitalize(),
                "age_group": "Pediatric (1-17 years)" if age < 18 else "Young Adult (18-25 years)"
            },
            "laboratory_values": {},
            "equation_parameters": {},
            "clinical_context": {
                "equation_advantages": [
                    "Superior to other pediatric equations for ages 1-25 years",
                    "Eliminates 'jumps' in eGFR when transitioning from pediatric to adult care",
                    "Does not require race-based adjustments",
                    "Validated in diverse populations with chronic kidney disease"
                ],
                "clinical_applications": [
                    "Monitoring kidney function progression in children and young adults",
                    "Supporting clinical decision-making for CKD management",
                    "Facilitating smooth transition from pediatric to adult nephrology care",
                    "Guiding timing of renal replacement therapy preparation"
                ]
            }
        }
        
        # Add laboratory values used
        if equation_type in ["creatinine", "creatinine_cystatin_c"]:
            details["laboratory_values"]["height"] = f"{height} cm"
            details["laboratory_values"]["serum_creatinine"] = f"{serum_creatinine} mg/dL"
            
            k_cr = self._get_k_value_creatinine(age, sex)
            details["equation_parameters"]["creatinine_k_value"] = round(k_cr, 2)
        
        if equation_type in ["cystatin_c", "creatinine_cystatin_c"]:
            details["laboratory_values"]["cystatin_c"] = f"{cystatin_c} mg/L"
            
            k_cys = self._get_k_value_cystatin(age, sex)
            details["equation_parameters"]["cystatin_k_value"] = round(k_cys, 2)
        
        # Add equation type explanation
        if equation_type == "creatinine":
            details["equation_explanation"] = "eGFR = k × (height_m / serum_creatinine_mg/dL)"
        elif equation_type == "cystatin_c":
            details["equation_explanation"] = "eGFR = k × (1 / cystatin_c_mg/L)"
        else:
            details["equation_explanation"] = "eGFR = (creatinine_eGFR + cystatin_c_eGFR) / 2"
        
        # Add clinical recommendations
        if age >= 18:
            details["clinical_context"]["transition_considerations"] = [
                "For patients 18-25 years, consider comparing with adult CKD-EPI equations",
                "CKiD U25 equations may be more appropriate for young adults with CKD",
                "Smooth transition monitoring without eGFR 'jumps' at age 18"
            ]
        
        return details


def calculate_ckid_u25_egfr(
    equation_type: str,
    age: int,
    sex: str,
    height: Optional[float] = None,
    serum_creatinine: Optional[float] = None,
    cystatin_c: Optional[float] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CkidU25EgfrCalculator()
    return calculator.calculate(
        equation_type=equation_type,
        age=age,
        sex=sex,
        height=height,
        serum_creatinine=serum_creatinine,
        cystatin_c=cystatin_c
    )