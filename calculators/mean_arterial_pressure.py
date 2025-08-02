"""
Mean Arterial Pressure (MAP) Calculator

Calculates the average arterial pressure during one cardiac cycle using systolic 
and diastolic blood pressure. MAP represents the average blood pressure throughout 
the cardiac cycle and is a better indicator of tissue perfusion than systolic BP alone.

References:
1. Magder SA. The highs and lows of blood pressure: toward meaningful clinical targets 
   in patients with shock. Crit Care Med. 2014 May;42(5):1241-51.
2. Walsh M, et al. Relationship between intraoperative mean arterial pressure and 
   clinical outcomes after noncardiac surgery. Anesthesiology. 2013 Sep;119(3):507-15.
3. Sesso HD, et al. Systolic and diastolic blood pressure, pulse pressure, and mean 
   arterial pressure as predictors of cardiovascular disease risk. Hypertension. 2000.
"""

import math
from typing import Dict, Any


class MeanArterialPressureCalculator:
    """Calculator for Mean Arterial Pressure (MAP)"""
    
    def __init__(self):
        # MAP ranges for interpretation (in mmHg)
        self.CRITICAL_LOW = 60.0
        self.BORDERLINE_LOW = 65.0
        self.LOW_NORMAL = 70.0
        self.NORMAL_MIN = 90.0
        self.NORMAL_MAX = 110.0
        self.ELEVATED = 130.0
    
    def calculate(self, systolic_bp: float, diastolic_bp: float) -> Dict[str, Any]:
        """
        Calculates Mean Arterial Pressure using systolic and diastolic blood pressure
        
        MAP = (2 × Diastolic BP + Systolic BP) / 3
        
        This formula accounts for the fact that approximately two-thirds of the 
        cardiac cycle is spent in diastole.
        
        Args:
            systolic_bp (float): Systolic blood pressure in mmHg
            diastolic_bp (float): Diastolic blood pressure in mmHg
            
        Returns:
            Dict with MAP result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(systolic_bp, diastolic_bp)
        
        # Calculate MAP using the standard formula
        map_value = self._calculate_map(systolic_bp, diastolic_bp)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(map_value)
        
        return {
            "result": map_value,
            "unit": "mmHg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, systolic_bp: float, diastolic_bp: float):
        """Validates blood pressure inputs"""
        
        # Type validation
        if not isinstance(systolic_bp, (int, float)):
            raise ValueError("Systolic blood pressure must be a number")
        
        if not isinstance(diastolic_bp, (int, float)):
            raise ValueError("Diastolic blood pressure must be a number")
        
        # Range validation based on JSON metadata
        if systolic_bp < 40 or systolic_bp > 300:
            raise ValueError("Systolic blood pressure must be between 40 and 300 mmHg")
        
        if diastolic_bp < 20 or diastolic_bp > 200:
            raise ValueError("Diastolic blood pressure must be between 20 and 200 mmHg")
        
        # Logical validation
        if diastolic_bp >= systolic_bp:
            raise ValueError("Systolic blood pressure must be greater than diastolic blood pressure")
        
        # Clinical plausibility check
        pulse_pressure = systolic_bp - diastolic_bp
        if pulse_pressure < 10:
            raise ValueError("Pulse pressure (systolic - diastolic) must be at least 10 mmHg")
    
    def _calculate_map(self, systolic_bp: float, diastolic_bp: float) -> float:
        """
        Implements the MAP formula
        
        MAP = (2 × Diastolic BP + Systolic BP) / 3
        
        Alternative formula: MAP = Diastolic BP + 1/3 × (Systolic BP - Diastolic BP)
        Both formulas are mathematically equivalent.
        """
        
        # Calculate using the primary formula
        map_value = (2 * diastolic_bp + systolic_bp) / 3
        
        # Round to 1 decimal place for clinical relevance
        return round(map_value, 1)
    
    def _get_interpretation(self, map_value: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on MAP value
        
        Args:
            map_value (float): Calculated MAP in mmHg
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if map_value < self.CRITICAL_LOW:
            return {
                "stage": "Critical",
                "description": "Critically low MAP",
                "interpretation": "Critically low MAP with high risk of organ hypoperfusion and ischemia. "
                                "Immediate intervention required. Even brief periods at MAP <50 mmHg "
                                "significantly increase mortality risk."
            }
        elif map_value < self.BORDERLINE_LOW:
            return {
                "stage": "Low",
                "description": "Low MAP",
                "interpretation": "Low MAP with risk of inadequate tissue perfusion. This is the minimum "
                                "MAP generally needed to maintain adequate perfusion to vital organs. "
                                "Consider fluids, vasopressors, or other interventions."
            }
        elif map_value < self.LOW_NORMAL:
            return {
                "stage": "Borderline Low",
                "description": "Borderline low MAP",
                "interpretation": "Borderline low MAP. This is the minimum recommended MAP in patients "
                                "with sepsis and septic shock. May require intervention to maintain "
                                "adequate organ perfusion."
            }
        elif map_value < self.NORMAL_MIN:
            return {
                "stage": "Low Normal",
                "description": "Low normal MAP",
                "interpretation": "Low normal MAP but still adequate for tissue perfusion in most patients. "
                                "Monitor closely in elderly patients or those with chronic hypertension "
                                "who may require higher MAP for adequate perfusion."
            }
        elif map_value <= self.NORMAL_MAX:
            return {
                "stage": "Normal",
                "description": "Normal MAP",
                "interpretation": "Normal mean arterial pressure indicating adequate tissue perfusion. "
                                "This range provides optimal blood flow to vital organs."
            }
        elif map_value <= self.ELEVATED:
            return {
                "stage": "Elevated",
                "description": "Elevated MAP",
                "interpretation": "Elevated MAP which may indicate hypertension or increased systemic "
                                "vascular resistance. Evaluate for underlying causes and consider "
                                "antihypertensive therapy if persistently elevated."
            }
        else:
            return {
                "stage": "High",
                "description": "High MAP",
                "interpretation": "Significantly elevated MAP indicating severe hypertension. Risk of "
                                "end-organ damage. Requires urgent evaluation and treatment to prevent "
                                "complications such as stroke, myocardial infarction, or renal failure."
            }


def calculate_mean_arterial_pressure(systolic_bp: float, diastolic_bp: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MeanArterialPressureCalculator()
    return calculator.calculate(systolic_bp, diastolic_bp)