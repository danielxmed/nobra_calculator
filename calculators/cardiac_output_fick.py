"""
Cardiac Output (Fick's Formula) Calculator

Calculates cardiac output, cardiac index, and stroke volume using Fick's principle.
The gold standard method for measuring cardiac output.

References:
1. Ragosta M. Textbook of Clinical Hemodynamics. 1st ed. Philadelphia: Elsevier; 2017.
2. Swan HJ, Ganz W, Forrester J, et al. Catheterization of the heart in man with 
   use of a flow-directed balloon-tipped catheter. N Engl J Med. 1970;283(9):447-51.
3. LaFarge CG, Miettinen OS. The estimation of oxygen consumption. 
   Cardiovasc Res. 1970;4(1):23-30.
"""

import math
from typing import Dict, Any


class CardiacOutputFickCalculator:
    """Calculator for Cardiac Output using Fick's Formula"""
    
    def __init__(self):
        # Constants for Fick calculation
        self.HB_OXYGEN_CAPACITY = 1.34  # mL O2/g Hb
        self.VO2_YOUNG = 125  # mL O2/min/m² for age <70
        self.VO2_ELDERLY = 110  # mL O2/min/m² for age ≥70
    
    def calculate(
        self,
        height_cm: float,
        weight_kg: float,
        age_years: int,
        hemoglobin_g_dl: float,
        sao2_percent: float,
        svo2_percent: float,
        heart_rate_bpm: int
    ) -> Dict[str, Any]:
        """
        Calculates cardiac output, cardiac index, and stroke volume using Fick's formula
        
        Args:
            height_cm: Patient height in cm
            weight_kg: Patient weight in kg
            age_years: Patient age in years
            hemoglobin_g_dl: Hemoglobin level in g/dL
            sao2_percent: Arterial oxygen saturation (%)
            svo2_percent: Mixed venous oxygen saturation (%)
            heart_rate_bpm: Heart rate in beats per minute
            
        Returns:
            Dict with cardiac measurements and interpretations
        """
        
        # Validate inputs
        self._validate_inputs(
            height_cm, weight_kg, age_years, hemoglobin_g_dl,
            sao2_percent, svo2_percent, heart_rate_bpm
        )
        
        # Calculate Body Surface Area (Mosteller formula)
        bsa = math.sqrt((height_cm * weight_kg) / 3600)
        
        # Calculate VO2 (oxygen consumption)
        vo2_per_m2 = self.VO2_ELDERLY if age_years >= 70 else self.VO2_YOUNG
        vo2 = vo2_per_m2 * bsa  # mL O2/min
        
        # Convert saturations to decimals
        sao2_decimal = sao2_percent / 100
        svo2_decimal = svo2_percent / 100
        
        # Calculate arteriovenous oxygen difference in mL O2/dL blood
        av_o2_diff = (sao2_decimal - svo2_decimal) * hemoglobin_g_dl * self.HB_OXYGEN_CAPACITY
        
        # Calculate Cardiac Output using Fick equation
        # CO (L/min) = VO2 (mL/min) / [AV O2 diff (mL O2/dL) × 10 (dL/L)]
        cardiac_output = vo2 / (av_o2_diff * 10)
        
        # Calculate Cardiac Index (L/min/m²)
        cardiac_index = cardiac_output / bsa
        
        # Calculate Stroke Volume (mL/beat)
        stroke_volume = (cardiac_output * 1000) / heart_rate_bpm  # Convert L to mL
        
        # Calculate Stroke Volume Index (mL/beat/m²)
        stroke_volume_index = stroke_volume / bsa
        
        # Get interpretations
        co_interpretation = self._interpret_cardiac_output(cardiac_output)
        ci_interpretation = self._interpret_cardiac_index(cardiac_index)
        sv_interpretation = self._interpret_stroke_volume(stroke_volume)
        
        return {
            "result": {
                "cardiac_output": round(cardiac_output, 2),
                "cardiac_index": round(cardiac_index, 2),
                "stroke_volume": round(stroke_volume, 1),
                "stroke_volume_index": round(stroke_volume_index, 1),
                "body_surface_area": round(bsa, 2),
                "oxygen_consumption": round(vo2, 1),
                "av_oxygen_difference": round(av_o2_diff, 2)
            },
            "unit": "L/min, L/min/m², mL/beat",
            "interpretation": f"Cardiac Output: {co_interpretation}. Cardiac Index: {ci_interpretation}. Stroke Volume: {sv_interpretation}",
            "stage": self._get_overall_stage(cardiac_output, cardiac_index, stroke_volume),
            "stage_description": self._get_overall_description(cardiac_output, cardiac_index, stroke_volume)
        }
    
    def _validate_inputs(self, height_cm, weight_kg, age_years, hemoglobin_g_dl,
                        sao2_percent, svo2_percent, heart_rate_bpm):
        """Validates input parameters"""
        
        if not (50 <= height_cm <= 250):
            raise ValueError("Height must be between 50-250 cm")
        
        if not (10 <= weight_kg <= 300):
            raise ValueError("Weight must be between 10-300 kg")
        
        if not (0 <= age_years <= 120):
            raise ValueError("Age must be between 0-120 years")
        
        if not (3.0 <= hemoglobin_g_dl <= 25.0):
            raise ValueError("Hemoglobin must be between 3.0-25.0 g/dL")
        
        if not (50.0 <= sao2_percent <= 100.0):
            raise ValueError("Arterial oxygen saturation must be between 50-100%")
        
        if not (30.0 <= svo2_percent <= 90.0):
            raise ValueError("Mixed venous oxygen saturation must be between 30-90%")
        
        if not (30 <= heart_rate_bpm <= 250):
            raise ValueError("Heart rate must be between 30-250 bpm")
        
        if svo2_percent >= sao2_percent:
            raise ValueError("Mixed venous oxygen saturation must be less than arterial oxygen saturation")
    
    def _interpret_cardiac_output(self, co: float) -> str:
        """Interprets cardiac output value"""
        if co < 4.0:
            return "Low cardiac output (<4.0 L/min). Consider hypovolemia, shock, or cardiac dysfunction"
        elif co > 8.0:
            return "High cardiac output (>8.0 L/min). Consider hypoxia, sepsis, anemia, or hyperthyroidism"
        else:
            return "Normal cardiac output (4.0-8.0 L/min)"
    
    def _interpret_cardiac_index(self, ci: float) -> str:
        """Interprets cardiac index value"""
        if ci < 2.5:
            return "Low cardiac index (<2.5 L/min/m²). Inadequate cardiac function relative to body size"
        elif ci > 4.0:
            return "High cardiac index (>4.0 L/min/m²). Hyperdynamic circulation"
        else:
            return "Normal cardiac index (2.5-4.0 L/min/m²)"
    
    def _interpret_stroke_volume(self, sv: float) -> str:
        """Interprets stroke volume value"""
        if sv < 60:
            return "Low stroke volume (<60 mL/beat). Consider impaired contractility or increased afterload"
        elif sv > 100:
            return "High stroke volume (>100 mL/beat). Consider bradycardia or decreased afterload"
        else:
            return "Normal stroke volume (60-100 mL/beat)"
    
    def _get_overall_stage(self, co: float, ci: float, sv: float) -> str:
        """Determines overall cardiac function stage"""
        normal_count = 0
        if 4.0 <= co <= 8.0:
            normal_count += 1
        if 2.5 <= ci <= 4.0:
            normal_count += 1
        if 60 <= sv <= 100:
            normal_count += 1
        
        if normal_count == 3:
            return "Normal Cardiac Function"
        elif normal_count >= 2:
            return "Mostly Normal Cardiac Function"
        elif normal_count == 1:
            return "Abnormal Cardiac Function"
        else:
            return "Severely Abnormal Cardiac Function"
    
    def _get_overall_description(self, co: float, ci: float, sv: float) -> str:
        """Gets overall description based on measurements"""
        low_count = sum([co < 4.0, ci < 2.5, sv < 60])
        high_count = sum([co > 8.0, ci > 4.0, sv > 100])
        
        if low_count >= 2:
            return "Low cardiac performance"
        elif high_count >= 2:
            return "Hyperdynamic cardiac state"
        else:
            return "Mixed cardiac parameters"


def calculate_cardiac_output_fick(
    height_cm: float,
    weight_kg: float,
    age_years: int,
    hemoglobin_g_dl: float,
    sao2_percent: float,
    svo2_percent: float,
    heart_rate_bpm: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CardiacOutputFickCalculator()
    return calculator.calculate(
        height_cm=height_cm,
        weight_kg=weight_kg,
        age_years=age_years,
        hemoglobin_g_dl=hemoglobin_g_dl,
        sao2_percent=sao2_percent,
        svo2_percent=svo2_percent,
        heart_rate_bpm=heart_rate_bpm
    )