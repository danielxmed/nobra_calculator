"""
Endotracheal Tube (ETT) Depth and Tidal Volume Calculator

Estimates optimal ETT placement depth using the Chula formula and calculates
target tidal volume based on ideal body weight for lung-protective ventilation.

References:
1. Techanivate A, Kumwilaisak K, Samranrean S. Estimation of the proper length 
   of orotracheal intubation by Chula formula. J Med Assoc Thai. 2005 Dec;88(12):1838-46.
2. Acute Respiratory Distress Syndrome Network, Brower RG, Matthay MA, Morris A, 
   Schoenfeld D, Thompson BT, Wheeler A. Ventilation with lower tidal volumes as 
   compared with traditional tidal volumes for acute lung injury and the acute 
   respiratory distress syndrome. N Engl J Med. 2000 May 4;342(18):1301-8.
3. Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm. 1974;8:650-655.
"""

from typing import Dict, Any


class EttDepthTidalVolumeCalculator:
    """Calculator for ETT Depth and Tidal Volume"""
    
    def __init__(self):
        """Initialize calculator with constants"""
        # Devine formula constants for ideal body weight
        self.IBW_MALE_BASE = 50.0  # kg
        self.IBW_FEMALE_BASE = 45.5  # kg
        self.IBW_HEIGHT_MULTIPLIER = 2.3  # kg per inch above 60 inches
        self.BASE_HEIGHT_INCHES = 60  # inches (5 feet)
        
        # Tidal volume constants (mL/kg IBW)
        self.TIDAL_VOLUME_MIN = 6.0  # mL/kg
        self.TIDAL_VOLUME_MAX = 8.0  # mL/kg
        
        # Chula formula constants
        self.CHULA_HEIGHT_MULTIPLIER = 0.1
        self.CHULA_CONSTANT = 4.0
        
        # Conversion constants
        self.CM_TO_INCHES = 0.393701
    
    def calculate(self, height_cm: float, sex: str) -> Dict[str, Any]:
        """
        Calculates ETT depth and tidal volume recommendations
        
        Args:
            height_cm (float): Patient height in centimeters
            sex (str): Patient biological sex ('male' or 'female')
            
        Returns:
            Dict with ETT depth and tidal volume calculations
        """
        
        # Validate inputs
        self._validate_inputs(height_cm, sex)
        
        # Calculate ETT depth using Chula formula
        ett_depth = self._calculate_ett_depth(height_cm)
        
        # Convert height to inches for IBW calculation
        height_inches = height_cm * self.CM_TO_INCHES
        
        # Calculate ideal body weight
        ideal_body_weight = self._calculate_ideal_body_weight(height_inches, sex)
        
        # Calculate tidal volume range
        tidal_volume_min, tidal_volume_max = self._calculate_tidal_volume_range(ideal_body_weight)
        
        # Get interpretation
        interpretation = self._get_interpretation(ett_depth, ideal_body_weight, 
                                               tidal_volume_min, tidal_volume_max, 
                                               height_cm, sex)
        
        return {
            "result": "normal_calculations",
            "unit": "various",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "ett_depth_cm": round(ett_depth, 1),
            "ideal_body_weight_kg": round(ideal_body_weight, 1),
            "tidal_volume_min_ml": int(round(tidal_volume_min)),
            "tidal_volume_max_ml": int(round(tidal_volume_max)),
            "height_inches": round(height_inches, 1)
        }
    
    def _validate_inputs(self, height_cm: float, sex: str):
        """Validates input parameters"""
        
        if not isinstance(height_cm, (int, float)):
            raise ValueError("height_cm must be a number")
        
        if height_cm < 152.4:  # 60 inches
            raise ValueError("height_cm must be at least 152.4 cm (60 inches)")
        
        if height_cm > 250:
            raise ValueError("height_cm must be less than 250 cm")
        
        if sex not in ["male", "female"]:
            raise ValueError("sex must be 'male' or 'female'")
    
    def _calculate_ett_depth(self, height_cm: float) -> float:
        """
        Calculates ETT depth using the Chula formula
        
        Args:
            height_cm (float): Height in centimeters
            
        Returns:
            float: ETT depth from front teeth in centimeters
        """
        
        # Chula formula: ETT depth = 0.1 × Height (cm) + 4
        return (self.CHULA_HEIGHT_MULTIPLIER * height_cm) + self.CHULA_CONSTANT
    
    def _calculate_ideal_body_weight(self, height_inches: float, sex: str) -> float:
        """
        Calculates ideal body weight using Devine formula
        
        Args:
            height_inches (float): Height in inches
            sex (str): Biological sex
            
        Returns:
            float: Ideal body weight in kilograms
        """
        
        # Calculate height above base (60 inches)
        height_above_base = height_inches - self.BASE_HEIGHT_INCHES
        
        if sex == "male":
            # Men: IBW = 50 kg + 2.3 × (height in inches - 60)
            return self.IBW_MALE_BASE + (self.IBW_HEIGHT_MULTIPLIER * height_above_base)
        else:  # female
            # Women: IBW = 45.5 kg + 2.3 × (height in inches - 60)
            return self.IBW_FEMALE_BASE + (self.IBW_HEIGHT_MULTIPLIER * height_above_base)
    
    def _calculate_tidal_volume_range(self, ideal_body_weight: float) -> tuple:
        """
        Calculates tidal volume range for lung-protective ventilation
        
        Args:
            ideal_body_weight (float): Ideal body weight in kg
            
        Returns:
            tuple: (min_tidal_volume, max_tidal_volume) in mL
        """
        
        tidal_volume_min = self.TIDAL_VOLUME_MIN * ideal_body_weight
        tidal_volume_max = self.TIDAL_VOLUME_MAX * ideal_body_weight
        
        return tidal_volume_min, tidal_volume_max
    
    def _get_interpretation(self, ett_depth: float, ideal_body_weight: float,
                           tidal_volume_min: float, tidal_volume_max: float,
                           height_cm: float, sex: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on calculations
        
        Args:
            ett_depth (float): Calculated ETT depth
            ideal_body_weight (float): Calculated IBW
            tidal_volume_min (float): Minimum tidal volume
            tidal_volume_max (float): Maximum tidal volume
            height_cm (float): Patient height
            sex (str): Patient sex
            
        Returns:
            Dict with interpretation details
        """
        
        return {
            "stage": "Calculated Values",
            "description": "ETT depth and tidal volume recommendations",
            "interpretation": (
                f"For a {height_cm:.1f} cm tall {sex} patient: "
                f"Recommended ETT depth is {ett_depth:.1f} cm from front teeth (Chula formula). "
                f"Ideal body weight is {ideal_body_weight:.1f} kg (Devine formula). "
                f"Target tidal volume for lung-protective ventilation is "
                f"{int(round(tidal_volume_min))}-{int(round(tidal_volume_max))} mL "
                f"(6-8 mL/kg IBW). Always verify ETT position with chest radiograph, "
                f"auscultation, or ultrasound for extended intubation."
            )
        }


def calculate_ett_depth_tidal_volume(height_cm: float, sex: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ett_depth_tidal_volume pattern
    """
    calculator = EttDepthTidalVolumeCalculator()
    return calculator.calculate(height_cm, sex)