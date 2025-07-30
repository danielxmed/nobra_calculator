"""
CAHP (Cardiac Arrest Hospital Prognosis) Score Calculator

Predicts poor prognosis after out-of-hospital cardiac arrest and guides utility 
of cardiac catheterization.

References:
1. Maupain C, et al. The CAHP (Cardiac Arrest Hospital Prognosis) score: a tool 
   for risk stratification after out-of-hospital cardiac arrest. Eur Heart J. 
   2016;37(42):3222-3228.
2. Bougouin W, et al. Should We Perform an Immediate Coronary Angiography in All 
   Patients After Cardiac Arrest?: Insights From a Large French Registry. JACC 
   Cardiovasc Interv. 2018;11(3):249-256.
"""

import math
from typing import Dict, Any


class CahpScoreCalculator:
    """Calculator for CAHP (Cardiac Arrest Hospital Prognosis) Score"""
    
    def __init__(self):
        # Points for setting
        self.SETTING_POINTS = {
            "public": 0,
            "home": 24
        }
        
        # Points for initial rhythm
        self.RHYTHM_POINTS = {
            "shockable": 0,
            "non_shockable": 27
        }
        
        # Points for epinephrine dose
        self.EPINEPHRINE_POINTS = {
            "0mg": 0,
            "1-2mg": 27,
            ">=3mg": 43
        }
    
    def calculate(self, age: int, setting: str, initial_rhythm: str, 
                  collapse_to_cpr: float, cpr_to_rosc: float, 
                  admission_ph: float, epinephrine_dose: str) -> Dict[str, Any]:
        """
        Calculates the CAHP score using the provided parameters
        
        Args:
            age (int): Patient age in years
            setting (str): Setting of cardiac arrest ("public" or "home")
            initial_rhythm (str): Initial cardiac rhythm ("shockable" or "non_shockable")
            collapse_to_cpr (float): Duration from collapse to CPR in minutes
            cpr_to_rosc (float): Duration from CPR to ROSC in minutes
            admission_ph (float): Arterial pH on admission
            epinephrine_dose (str): Total epinephrine dose ("0mg", "1-2mg", or ">=3mg")
            
        Returns:
            Dict with the CAHP score and interpretation
        """
        
        # Validations
        self._validate_inputs(age, setting, initial_rhythm, collapse_to_cpr, 
                            cpr_to_rosc, admission_ph, epinephrine_dose)
        
        # Calculate CAHP score components
        age_points = 1.1 * (age - 10)
        setting_points = self.SETTING_POINTS[setting]
        rhythm_points = self.RHYTHM_POINTS[initial_rhythm]
        collapse_cpr_points = 2.8 * collapse_to_cpr
        cpr_rosc_points = 0.8 * cpr_to_rosc
        ph_points = 585 - (77 * admission_ph)
        epinephrine_points = self.EPINEPHRINE_POINTS[epinephrine_dose]
        
        # Total CAHP score
        total_score = (age_points + setting_points + rhythm_points + 
                      collapse_cpr_points + cpr_rosc_points + ph_points + 
                      epinephrine_points)
        
        # Round to integer
        total_score = round(total_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "age_points": round(age_points, 1),
                "setting_points": setting_points,
                "rhythm_points": rhythm_points,
                "collapse_cpr_points": round(collapse_cpr_points, 1),
                "cpr_rosc_points": round(cpr_rosc_points, 1),
                "ph_points": round(ph_points, 1),
                "epinephrine_points": epinephrine_points
            }
        }
    
    def _validate_inputs(self, age, setting, initial_rhythm, collapse_to_cpr, 
                        cpr_to_rosc, admission_ph, epinephrine_dose):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        if setting not in self.SETTING_POINTS:
            raise ValueError("Setting must be 'public' or 'home'")
        
        if initial_rhythm not in self.RHYTHM_POINTS:
            raise ValueError("Initial rhythm must be 'shockable' or 'non_shockable'")
        
        if not isinstance(collapse_to_cpr, (int, float)):
            raise ValueError("Collapse to CPR duration must be a number")
        
        if collapse_to_cpr < 0 or collapse_to_cpr > 60:
            raise ValueError("Collapse to CPR duration must be between 0 and 60 minutes")
        
        if not isinstance(cpr_to_rosc, (int, float)):
            raise ValueError("CPR to ROSC duration must be a number")
        
        if cpr_to_rosc < 0 or cpr_to_rosc > 120:
            raise ValueError("CPR to ROSC duration must be between 0 and 120 minutes")
        
        if not isinstance(admission_ph, (int, float)):
            raise ValueError("Admission pH must be a number")
        
        if admission_ph < 6.5 or admission_ph > 7.8:
            raise ValueError("Admission pH must be between 6.5 and 7.8")
        
        if epinephrine_dose not in self.EPINEPHRINE_POINTS:
            raise ValueError("Epinephrine dose must be '0mg', '1-2mg', or '>=3mg'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CAHP score
        
        Args:
            score (int): Calculated CAHP score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 150:
            return {
                "stage": "Low Risk",
                "description": "Low risk of poor neurological outcome",
                "interpretation": (
                    "39% risk of poor neurological outcome (CPC 3-5) at hospital "
                    "discharge. Consider aggressive treatment including cardiac "
                    "catheterization if indicated."
                )
            }
        elif score <= 200:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of poor neurological outcome",
                "interpretation": (
                    "81% risk of poor neurological outcome (CPC 3-5) at hospital "
                    "discharge. Individualized treatment decisions should be made "
                    "based on clinical context."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk of poor neurological outcome",
                "interpretation": (
                    "100% risk of poor neurological outcome (CPC 3-5) at hospital "
                    "discharge. Consider goals of care discussion, though high scores "
                    "do not automatically warrant withdrawal of care."
                )
            }


def calculate_cahp_score(age, setting, initial_rhythm, collapse_to_cpr, 
                        cpr_to_rosc, admission_ph, epinephrine_dose) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CahpScoreCalculator()
    return calculator.calculate(age, setting, initial_rhythm, collapse_to_cpr,
                               cpr_to_rosc, admission_ph, epinephrine_dose)