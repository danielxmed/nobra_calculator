"""
HCM Risk-SCD Calculator

Estimates 5-year risk of sudden cardiac death in patients with hypertrophic
cardiomyopathy to guide ICD implantation decisions.

References:
1. O'Mahony C, et al. Eur Heart J. 2014;35(30):2010-20.
2. Elliott PM, et al. Eur Heart J. 2014;35(39):2733-79.
"""

import math
from typing import Dict, Any


class HcmRiskScdCalculator:
    """Calculator for HCM Risk-SCD"""
    
    def __init__(self):
        # Model coefficients from the original paper
        self.COEFF_MAX_WALL_THICKNESS = 0.15939858
        self.COEFF_MAX_WALL_THICKNESS_SQ = -0.00294271
        self.COEFF_LA_DIAMETER = 0.0259082
        self.COEFF_MAX_LVOT_GRADIENT = 0.00446131
        self.COEFF_FAMILY_HISTORY = 0.4583082
        self.COEFF_NSVT = 0.82639195
        self.COEFF_UNEXPLAINED_SYNCOPE = 0.71650361
        self.COEFF_AGE = -0.01799934
        
        # Baseline survival probability at 5 years
        self.BASELINE_SURVIVAL = 0.998
    
    def calculate(self, age: int, family_history_scd: str, max_wall_thickness: float,
                  left_atrial_diameter: float, max_lvot_gradient: float,
                  nsvt: str, unexplained_syncope: str) -> Dict[str, Any]:
        """
        Calculates the 5-year SCD risk using the HCM Risk-SCD model
        
        Args:
            age (int): Age at evaluation (16-110 years)
            family_history_scd (str): "yes" or "no" - Family history of SCD
            max_wall_thickness (float): Maximum LV wall thickness in mm
            left_atrial_diameter (float): Left atrial diameter in mm
            max_lvot_gradient (float): Max LVOT gradient in mmHg
            nsvt (str): "yes" or "no" - Non-sustained VT
            unexplained_syncope (str): "yes" or "no" - Unexplained syncope
            
        Returns:
            Dict with the 5-year SCD risk percentage and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, family_history_scd, max_wall_thickness,
                            left_atrial_diameter, max_lvot_gradient,
                            nsvt, unexplained_syncope)
        
        # Convert binary variables to numeric
        family_history_binary = 1 if family_history_scd == "yes" else 0
        nsvt_binary = 1 if nsvt == "yes" else 0
        syncope_binary = 1 if unexplained_syncope == "yes" else 0
        
        # Calculate prognostic index
        prognostic_index = (
            self.COEFF_MAX_WALL_THICKNESS * max_wall_thickness +
            self.COEFF_MAX_WALL_THICKNESS_SQ * (max_wall_thickness ** 2) +
            self.COEFF_LA_DIAMETER * left_atrial_diameter +
            self.COEFF_MAX_LVOT_GRADIENT * max_lvot_gradient +
            self.COEFF_FAMILY_HISTORY * family_history_binary +
            self.COEFF_NSVT * nsvt_binary +
            self.COEFF_UNEXPLAINED_SYNCOPE * syncope_binary +
            self.COEFF_AGE * age
        )
        
        # Calculate 5-year SCD risk
        # Risk = 1 - (baseline survival)^exp(prognostic index)
        five_year_risk = (1 - math.pow(self.BASELINE_SURVIVAL, math.exp(prognostic_index))) * 100
        
        # Ensure risk is within 0-100% range
        five_year_risk = max(0, min(100, five_year_risk))
        
        # Round to 1 decimal place for clinical use
        five_year_risk = round(five_year_risk, 1)
        
        # Get interpretation based on risk
        interpretation = self._get_interpretation(five_year_risk)
        
        return {
            "result": five_year_risk,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, family_history_scd: str, max_wall_thickness: float,
                        left_atrial_diameter: float, max_lvot_gradient: float,
                        nsvt: str, unexplained_syncope: str):
        """Validates input parameters"""
        
        # Age validation
        if not isinstance(age, (int, float)):
            raise ValueError("Age must be a number")
        if age < 16 or age > 110:
            raise ValueError("Age must be between 16 and 110 years")
        
        # Binary variable validation
        valid_yes_no = ["yes", "no"]
        if family_history_scd not in valid_yes_no:
            raise ValueError(f"Family history SCD must be one of: {', '.join(valid_yes_no)}")
        if nsvt not in valid_yes_no:
            raise ValueError(f"NSVT must be one of: {', '.join(valid_yes_no)}")
        if unexplained_syncope not in valid_yes_no:
            raise ValueError(f"Unexplained syncope must be one of: {', '.join(valid_yes_no)}")
        
        # Continuous variable validation
        if not isinstance(max_wall_thickness, (int, float)):
            raise ValueError("Maximum wall thickness must be a number")
        if max_wall_thickness < 10 or max_wall_thickness > 40:
            raise ValueError("Maximum wall thickness must be between 10 and 40 mm")
        
        if not isinstance(left_atrial_diameter, (int, float)):
            raise ValueError("Left atrial diameter must be a number")
        if left_atrial_diameter < 15 or left_atrial_diameter > 70:
            raise ValueError("Left atrial diameter must be between 15 and 70 mm")
        
        if not isinstance(max_lvot_gradient, (int, float)):
            raise ValueError("Maximum LVOT gradient must be a number")
        if max_lvot_gradient < 0 or max_lvot_gradient > 200:
            raise ValueError("Maximum LVOT gradient must be between 0 and 200 mmHg")
    
    def _get_interpretation(self, risk: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the 5-year SCD risk
        
        Args:
            risk (float): 5-year SCD risk percentage
            
        Returns:
            Dict with interpretation
        """
        
        if risk < 4.0:
            return {
                "stage": "Low Risk",
                "description": "Low 5-year SCD risk",
                "interpretation": (
                    f"5-year risk of SCD is {risk}% (Low Risk). ICD generally not indicated. "
                    "Continue regular follow-up and reassess risk every 1-2 years or if "
                    "clinical change occurs."
                )
            }
        elif risk < 6.0:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate 5-year SCD risk",
                "interpretation": (
                    f"5-year risk of SCD is {risk}% (Intermediate Risk). ICD may be considered. "
                    "Discuss risks and benefits with patient, consider additional risk modifiers "
                    "such as LV apical aneurysm, extensive LGE on MRI, or abnormal BP response "
                    "to exercise."
                )
            }
        else:  # risk >= 6.0
            return {
                "stage": "High Risk",
                "description": "High 5-year SCD risk",
                "interpretation": (
                    f"5-year risk of SCD is {risk}% (High Risk). ICD should be considered. "
                    "Strong recommendation for prophylactic ICD implantation after thorough "
                    "discussion with patient regarding risks, benefits, and implications."
                )
            }


def calculate_hcm_risk_scd(age: int, family_history_scd: str, max_wall_thickness: float,
                          left_atrial_diameter: float, max_lvot_gradient: float,
                          nsvt: str, unexplained_syncope: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HcmRiskScdCalculator()
    return calculator.calculate(age, family_history_scd, max_wall_thickness,
                              left_atrial_diameter, max_lvot_gradient,
                              nsvt, unexplained_syncope)