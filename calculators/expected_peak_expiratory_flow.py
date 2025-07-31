"""
Estimated/Expected Peak Expiratory Flow (Peak Flow) Calculator

Estimates expected peak expiratory flow rate and quantifies asthma exacerbation severity
based on age, height, race, and sex using established regression equations.

References:
1. Hankinson JL, Odencrantz JR, Fedan KB. Spirometric reference values from a sample of the general U.S. population. 
   Am J Respir Crit Care Med. 1999 Jan;159(1):179-87. doi: 10.1164/ajrccm.159.1.9712108.
2. Nunn AJ, Gregg I. New regression equations for predicting peak expiratory flow in adults. 
   BMJ. 1989 Apr 22;298(6680):1068-70. doi: 10.1136/bmj.298.6680.1068.
3. Godfrey S, Kamburoff PL, Nairn JR. Spirometry, lung volumes and airway resistance in normal children aged 5 to 18 years. 
   Br J Dis Chest. 1970 Jan;64(1):15-24. doi: 10.1016/s0007-0971(70)80045-0.
"""

import math
from typing import Dict, Any, Optional


class ExpectedPeakExpiratoryFlowCalculator:
    """Calculator for Estimated/Expected Peak Expiratory Flow (Peak Flow)"""
    
    def __init__(self):
        """Initialize calculator with constants"""
        # Hankinson 1999 NHANES III coefficients for Caucasian, African American, Mexican American
        # Ages 8-80 years
        self.HANKINSON_COEFFICIENTS = {
            "caucasian": {
                "male": {"height_coef": 5.48, "intercept": 1.58, "age_coef": 0.041},
                "female": {"height_coef": 3.72, "intercept": 2.24, "age_coef": 0.03}
            },
            "african_american": {
                "male": {"height_coef": 4.82, "intercept": 1.76, "age_coef": 0.041},
                "female": {"height_coef": 3.27, "intercept": 2.38, "age_coef": 0.03}
            },
            "mexican_american": {
                "male": {"height_coef": 5.22, "intercept": 1.64, "age_coef": 0.041},
                "female": {"height_coef": 3.54, "intercept": 2.29, "age_coef": 0.03}
            }
        }
    
    def calculate(self, age_years: int, height_cm: float, sex: str, race_ethnicity: str, 
                 measured_pef: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates estimated peak expiratory flow and zone assessment
        
        Args:
            age_years (int): Patient age in years (5-80)
            height_cm (float): Patient height in centimeters
            sex (str): Patient biological sex (male/female)
            race_ethnicity (str): Patient race/ethnicity
            measured_pef (float, optional): Measured peak expiratory flow for comparison
            
        Returns:
            Dict with expected PEF, zone assessment, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_years, height_cm, sex, race_ethnicity, measured_pef)
        
        # Calculate expected PEF based on age and ethnicity
        expected_pef = self._calculate_expected_pef(age_years, height_cm, sex, race_ethnicity)
        
        # Calculate zone and percentage if measured PEF provided
        zone_assessment = self._calculate_zone_assessment(expected_pef, measured_pef)
        
        # Get interpretation
        interpretation = self._get_interpretation(expected_pef, measured_pef, zone_assessment)
        
        result = {
            "result": "expected_pef_calculated",
            "unit": "L/min",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "expected_pef": round(expected_pef, 1),
            "measured_pef": round(measured_pef, 1) if measured_pef is not None else None,
            "percentage_of_expected": zone_assessment["percentage"] if zone_assessment["percentage"] is not None else None,
            "zone": zone_assessment["zone"],
            "zone_color": zone_assessment["color"]
        }
        
        return result
    
    def _validate_inputs(self, age_years: int, height_cm: float, sex: str, 
                        race_ethnicity: str, measured_pef: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(age_years, int) or age_years < 5 or age_years > 80:
            raise ValueError("age_years must be an integer between 5 and 80")
        
        if not isinstance(height_cm, (int, float)) or height_cm < 100 or height_cm > 220:
            raise ValueError("height_cm must be between 100 and 220 cm")
        
        if sex not in ["male", "female"]:
            raise ValueError("sex must be 'male' or 'female'")
        
        valid_ethnicities = ["caucasian", "african_american", "mexican_american", "other"]
        if race_ethnicity not in valid_ethnicities:
            raise ValueError(f"race_ethnicity must be one of {valid_ethnicities}")
        
        if measured_pef is not None:
            if not isinstance(measured_pef, (int, float)) or measured_pef < 50 or measured_pef > 800:
                raise ValueError("measured_pef must be between 50 and 800 L/min")
    
    def _calculate_expected_pef(self, age_years: int, height_cm: float, sex: str, race_ethnicity: str) -> float:
        """
        Calculates expected PEF using appropriate formula based on age and ethnicity
        
        Args:
            age_years (int): Patient age
            height_cm (float): Patient height in cm
            sex (str): Patient sex
            race_ethnicity (str): Patient race/ethnicity
            
        Returns:
            float: Expected PEF in L/min
        """
        
        # Ages 5-7 years (all ethnicities)
        if 5 <= age_years <= 7:
            return ((height_cm - 100) * 5) + 100
        
        # Ages 8-17 years, non-Caucasian/African American/Mexican American (other ethnicity)
        elif 8 <= age_years <= 17 and race_ethnicity == "other":
            return ((height_cm - 100) * 5) + 100
        
        # Ages 18-80 years, non-Caucasian/African American/Mexican American (other ethnicity)
        elif 18 <= age_years <= 80 and race_ethnicity == "other":
            height_m = height_cm / 100
            if sex == "male":
                return (((height_m * 5.48) + 1.58) - (age_years * 0.041)) * 60
            else:  # female
                return (((height_m * 3.72) + 2.24) - (age_years * 0.03)) * 60
        
        # Ages 8-80 years, Caucasian/African American/Mexican American (Hankinson equations)
        elif 8 <= age_years <= 80 and race_ethnicity in self.HANKINSON_COEFFICIENTS:
            return self._calculate_hankinson_pef(age_years, height_cm, sex, race_ethnicity)
        
        else:
            raise ValueError(f"No appropriate formula for age {age_years} and ethnicity {race_ethnicity}")
    
    def _calculate_hankinson_pef(self, age_years: int, height_cm: float, sex: str, race_ethnicity: str) -> float:
        """
        Calculates PEF using Hankinson 1999 NHANES III equations
        
        Args:
            age_years (int): Patient age
            height_cm (float): Patient height in cm
            sex (str): Patient sex
            race_ethnicity (str): Patient race/ethnicity
            
        Returns:
            float: Expected PEF in L/min
        """
        
        coeffs = self.HANKINSON_COEFFICIENTS[race_ethnicity][sex]
        height_m = height_cm / 100
        
        # Hankinson formula: PEF = [(Height × height_coef) + intercept - (Age × age_coef)] × 60
        pef = ((height_m * coeffs["height_coef"]) + coeffs["intercept"] - (age_years * coeffs["age_coef"])) * 60
        
        return max(pef, 50)  # Minimum reasonable PEF value
    
    def _calculate_zone_assessment(self, expected_pef: float, measured_pef: Optional[float]) -> Dict[str, Any]:
        """
        Calculates zone assessment based on percentage of expected PEF
        
        Args:
            expected_pef (float): Expected PEF value
            measured_pef (float, optional): Measured PEF value
            
        Returns:
            Dict with zone assessment
        """
        
        if measured_pef is None:
            return {
                "percentage": None,
                "zone": "Not assessed",
                "color": "gray"
            }
        
        percentage = (measured_pef / expected_pef) * 100
        
        if percentage >= 80:
            return {
                "percentage": round(percentage, 1),
                "zone": "Green Zone",
                "color": "green"
            }
        elif percentage >= 50:
            return {
                "percentage": round(percentage, 1),
                "zone": "Yellow Zone", 
                "color": "yellow"
            }
        else:
            return {
                "percentage": round(percentage, 1),
                "zone": "Red Zone",
                "color": "red"
            }
    
    def _get_interpretation(self, expected_pef: float, measured_pef: Optional[float], 
                          zone_assessment: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines clinical interpretation based on PEF values and zone assessment
        
        Args:
            expected_pef (float): Expected PEF value
            measured_pef (float, optional): Measured PEF value
            zone_assessment (Dict): Zone assessment results
            
        Returns:
            Dict with interpretation
        """
        
        base_text = f"Expected peak expiratory flow: {expected_pef:.1f} L/min based on age, height, sex, and ethnicity."
        
        if measured_pef is None:
            return {
                "stage": "Expected Value",
                "description": "Baseline reference",
                "interpretation": (
                    f"{base_text} This represents the predicted normal peak flow for this patient. "
                    f"Use this value as a reference for comparison with measured peak flow values. "
                    f"Regular monitoring and comparison to this expected value can help assess asthma control and detect exacerbations."
                )
            }
        
        percentage = zone_assessment["percentage"]
        zone = zone_assessment["zone"]
        
        if zone == "Green Zone":
            return {
                "stage": "Normal",
                "description": "Good control",
                "interpretation": (
                    f"{base_text} Measured peak flow: {measured_pef:.1f} L/min ({percentage:.1f}% of expected). "
                    f"GREEN ZONE - Good asthma control. Peak flow is within normal range (≥80% of expected). "
                    f"Continue current treatment plan and regular monitoring."
                )
            }
        elif zone == "Yellow Zone":
            return {
                "stage": "Caution",
                "description": "Reduced lung function",
                "interpretation": (
                    f"{base_text} Measured peak flow: {measured_pef:.1f} L/min ({percentage:.1f}% of expected). "
                    f"YELLOW ZONE - Caution indicated. Peak flow is below normal (50-79% of expected). "
                    f"May indicate developing asthma exacerbation. Consider increasing treatment per asthma action plan. "
                    f"Monitor closely and contact healthcare provider if symptoms worsen."
                )
            }
        else:  # Red Zone
            return {
                "stage": "Emergency",
                "description": "Severe obstruction",
                "interpretation": (
                    f"{base_text} Measured peak flow: {measured_pef:.1f} L/min ({percentage:.1f}% of expected). "
                    f"RED ZONE - EMERGENCY! Dangerously low peak flow (<50% of expected). "
                    f"Severe asthma exacerbation requiring immediate medical attention. "
                    f"Use rescue medications and seek emergency care immediately."
                )
            }


def calculate_expected_peak_expiratory_flow(age_years: int, height_cm: float, sex: str, 
                                          race_ethnicity: str, measured_pef: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_expected_peak_expiratory_flow pattern
    """
    calculator = ExpectedPeakExpiratoryFlowCalculator()
    return calculator.calculate(age_years, height_cm, sex, race_ethnicity, measured_pef)