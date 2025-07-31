"""
Focused Assessment with Sonography for Trauma (FAST) Calculator

Predicts presence of pericardial or intra-abdominal injury after 
penetrating or blunt trauma based on ultrasound findings.

References:
1. Rozycki GS, Ochsner MG, Jaffin JH, Champion HR. Prospective evaluation 
   of surgeons' use of ultrasound in the evaluation of trauma patients. 
   J Trauma. 1993 Apr;34(4):516-26.
2. Rozycki GS, Ballard RB, Feliciano DV, Schmidt JA, Pennington SD. 
   Surgeon-performed ultrasound for the assessment of truncal injuries: 
   lessons learned from 1540 patients. Ann Surg. 1998 Oct;228(4):557-67.
"""

from typing import Dict, Any


class FastCalculator:
    """Calculator for Focused Assessment with Sonography for Trauma (FAST)"""
    
    def __init__(self):
        # No specific constants needed for FAST
        pass
    
    def calculate(self, pericardial_fluid: str, right_upper_quadrant_fluid: str,
                  left_upper_quadrant_fluid: str, suprapubic_fluid: str,
                  patient_stability: str) -> Dict[str, Any]:
        """
        Evaluates FAST examination findings and provides clinical recommendations
        
        Args:
            pericardial_fluid (str): Pericardial fluid status (absent/present/equivocal)
            right_upper_quadrant_fluid (str): RUQ fluid status (absent/present/equivocal)
            left_upper_quadrant_fluid (str): LUQ fluid status (absent/present/equivocal)
            suprapubic_fluid (str): Suprapubic fluid status (absent/present/equivocal)
            patient_stability (str): Patient hemodynamic stability (stable/unstable)
            
        Returns:
            Dict with FAST result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pericardial_fluid, right_upper_quadrant_fluid,
                            left_upper_quadrant_fluid, suprapubic_fluid,
                            patient_stability)
        
        # Determine FAST result and interpretation
        result = self._determine_fast_result(
            pericardial_fluid, right_upper_quadrant_fluid,
            left_upper_quadrant_fluid, suprapubic_fluid,
            patient_stability
        )
        
        return result
    
    def _validate_inputs(self, pericardial_fluid: str, right_upper_quadrant_fluid: str,
                        left_upper_quadrant_fluid: str, suprapubic_fluid: str,
                        patient_stability: str):
        """Validates input parameters"""
        
        valid_fluid_options = ["absent", "present", "equivocal"]
        valid_stability_options = ["stable", "unstable"]
        
        # Validate fluid findings
        for fluid, location in [
            (pericardial_fluid, "Pericardial fluid"),
            (right_upper_quadrant_fluid, "Right upper quadrant fluid"),
            (left_upper_quadrant_fluid, "Left upper quadrant fluid"),
            (suprapubic_fluid, "Suprapubic fluid")
        ]:
            if fluid not in valid_fluid_options:
                raise ValueError(f"{location} must be one of {valid_fluid_options}")
        
        # Validate patient stability
        if patient_stability not in valid_stability_options:
            raise ValueError(f"Patient stability must be one of {valid_stability_options}")
    
    def _determine_fast_result(self, pericardial_fluid: str, right_upper_quadrant_fluid: str,
                              left_upper_quadrant_fluid: str, suprapubic_fluid: str,
                              patient_stability: str) -> Dict[str, Any]:
        """
        Determines FAST examination result and provides clinical interpretation
        
        Returns:
            Dict with result, interpretation, stage, and stage_description
        """
        
        # Check for pericardial fluid first (highest priority)
        if pericardial_fluid == "present":
            return {
                "result": "Positive FAST - Pericardial fluid",
                "unit": "",
                "interpretation": ("Pericardial fluid detected. Emergent surgical intervention "
                                 "is recommended. Consider immediate pericardiocentesis or "
                                 "thoracotomy based on clinical status and local expertise."),
                "stage": "Positive FAST - Pericardial",
                "stage_description": "Pericardial fluid present"
            }
        
        # Check for intra-abdominal fluid
        abdominal_fluid_present = any([
            right_upper_quadrant_fluid == "present",
            left_upper_quadrant_fluid == "present",
            suprapubic_fluid == "present"
        ])
        
        if abdominal_fluid_present:
            if patient_stability == "unstable":
                return {
                    "result": "Positive FAST - Intra-abdominal fluid (unstable patient)",
                    "unit": "",
                    "interpretation": ("Intra-abdominal fluid detected in hemodynamically unstable "
                                     "patient. Emergent exploratory laparotomy is recommended. "
                                     "Activate trauma team and prepare for immediate surgery."),
                    "stage": "Positive FAST - Abdominal (Unstable)",
                    "stage_description": "Intra-abdominal fluid with hemodynamic instability"
                }
            else:  # stable patient
                return {
                    "result": "Positive FAST - Intra-abdominal fluid (stable patient)",
                    "unit": "",
                    "interpretation": ("Intra-abdominal fluid detected in hemodynamically stable "
                                     "patient. Cross-sectional imaging (CT scan) is recommended "
                                     "for further evaluation. Consider contrast-enhanced CT of "
                                     "abdomen/pelvis to identify source and grade of injury."),
                    "stage": "Positive FAST - Abdominal (Stable)",
                    "stage_description": "Intra-abdominal fluid with hemodynamic stability"
                }
        
        # Check for equivocal findings
        equivocal_findings = any([
            pericardial_fluid == "equivocal",
            right_upper_quadrant_fluid == "equivocal",
            left_upper_quadrant_fluid == "equivocal",
            suprapubic_fluid == "equivocal"
        ])
        
        if equivocal_findings:
            return {
                "result": "Equivocal FAST",
                "unit": "",
                "interpretation": ("Equivocal FAST findings. Consider repeat FAST examination in "
                                 "10-15 minutes, clinical correlation, and/or additional imaging "
                                 "as indicated. Monitor vital signs closely. If clinical suspicion "
                                 "remains high, proceed with CT imaging or exploratory surgery "
                                 "based on clinical status."),
                "stage": "Equivocal FAST",
                "stage_description": "Equivocal findings"
            }
        
        # All findings negative
        return {
            "result": "Negative FAST",
            "unit": "",
            "interpretation": ("FAST negative. However, negative FAST does not exclude injury. "
                             "Sensitivity varies widely (22-98%). Clinical correlation and "
                             "consideration of additional imaging based on mechanism of injury "
                             "and clinical status is recommended. Serial FAST examinations or "
                             "CT imaging may be warranted if clinical suspicion remains."),
            "stage": "Negative FAST",
            "stage_description": "No fluid detected"
        }


def calculate_fast(pericardial_fluid: str, right_upper_quadrant_fluid: str,
                   left_upper_quadrant_fluid: str, suprapubic_fluid: str,
                   patient_stability: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FastCalculator()
    return calculator.calculate(pericardial_fluid, right_upper_quadrant_fluid,
                              left_upper_quadrant_fluid, suprapubic_fluid,
                              patient_stability)