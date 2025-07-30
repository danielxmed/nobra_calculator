"""
Corrected Count Increment (CCI) for Platelet Transfusion Calculator

Assesses adequacy of response to platelet transfusion by measuring the expected 
increase in platelets adjusted for patient size and platelet dose.

References:
1. Davis KB, Slichter SJ, Corash L. Corrected count increment and percent platelet recovery 
   as measures of posttransfusion platelet response: problems and a solution. 
   Transfusion. 1999;39(6):586-92.
2. Bishop JF, Matthews JP, McGrath K, Yuen K, Wolf MM, Szer J. Factors influencing 20-hour 
   increments after platelet transfusion. Transfusion. 1991;31(5):392-6.
3. Slichter SJ, Davis K, Enright H, et al. Factors affecting posttransfusion platelet increments, 
   platelet refractoriness, and platelet transfusion intervals in thrombocytopenic patients. 
   Blood. 2005;105(10):4106-14.
"""

import math
from typing import Dict, Any


class CorrectedCountIncrementCalculator:
    """Calculator for Corrected Count Increment (CCI) for Platelet Transfusion"""
    
    def __init__(self):
        # CCI interpretation thresholds
        self.THRESHOLD_1_HOUR = 7500  # CCI >7,500 at 1 hour indicates success
        self.THRESHOLD_20_HOUR = 4800  # CCI >4,800 at 20 hours indicates success
        
        # Unit conversion constants
        self.INCHES_TO_CM = 2.54
        self.LBS_TO_KG = 0.453592
        
        # BSA calculation constant (DuBois formula)
        self.BSA_CONSTANT = 3600  # for sqrt((height_cm × weight_kg) / 3600)
    
    def calculate(
        self,
        pre_transfusion_count: int,
        post_transfusion_count: int,
        time_after_transfusion: str,
        patient_height: float,
        patient_weight: float,
        platelet_unit_content: float
    ) -> Dict[str, Any]:
        """
        Calculates the Corrected Count Increment (CCI) for platelet transfusion
        
        Args:
            pre_transfusion_count: Pre-transfusion platelet count (platelets/μL)
            post_transfusion_count: Post-transfusion platelet count (platelets/μL)
            time_after_transfusion: Time after transfusion ("1_hour" or "20_hour")
            patient_height: Patient height (inches)
            patient_weight: Patient weight (lbs)
            platelet_unit_content: Total platelet content in transfused units (×10¹¹ platelets)
            
        Returns:
            Dict with CCI value and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            pre_transfusion_count, post_transfusion_count, time_after_transfusion,
            patient_height, patient_weight, platelet_unit_content
        )
        
        # Calculate count increment
        count_increment = post_transfusion_count - pre_transfusion_count
        
        # Convert units and calculate BSA
        height_cm = patient_height * self.INCHES_TO_CM
        weight_kg = patient_weight * self.LBS_TO_KG
        bsa = self._calculate_bsa(height_cm, weight_kg)
        
        # Calculate CCI
        cci_value = self._calculate_cci(count_increment, bsa, platelet_unit_content)
        
        # Get interpretation
        interpretation = self._get_interpretation(cci_value, time_after_transfusion)
        
        return {
            "result": round(cci_value, 1),
            "unit": "platelets/μL/m²/(×10¹¹ platelets)",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "count_increment": count_increment,
                "body_surface_area": round(bsa, 2),
                "platelet_dose": platelet_unit_content,
                "time_point": time_after_transfusion,
                "threshold": interpretation["threshold"],
                "response_adequate": interpretation["adequate_response"]
            }
        }
    
    def _validate_inputs(
        self, 
        pre_count: int, 
        post_count: int, 
        time_point: str,
        height: float, 
        weight: float, 
        platelet_content: float
    ):
        """Validates input parameters"""
        
        # Validate platelet counts
        if not isinstance(pre_count, int) or pre_count < 0 or pre_count > 500000:
            raise ValueError("Pre-transfusion platelet count must be an integer between 0 and 500,000/μL")
            
        if not isinstance(post_count, int) or post_count < 0 or post_count > 500000:
            raise ValueError("Post-transfusion platelet count must be an integer between 0 and 500,000/μL")
        
        # Validate time point
        if time_point not in ["1_hour", "20_hour"]:
            raise ValueError("Time after transfusion must be '1_hour' or '20_hour'")
        
        # Validate height
        if not isinstance(height, (int, float)) or height < 48 or height > 90:
            raise ValueError("Patient height must be between 48 and 90 inches")
        
        # Validate weight
        if not isinstance(weight, (int, float)) or weight < 0.5 or weight > 620:
            raise ValueError("Patient weight must be between 0.5 and 620 lbs")
        
        # Validate platelet unit content
        if not isinstance(platelet_content, (int, float)) or platelet_content < 0.5 or platelet_content > 500:
            raise ValueError("Platelet unit content must be between 0.5 and 500 ×10¹¹ platelets")
    
    def _calculate_bsa(self, height_cm: float, weight_kg: float) -> float:
        """
        Calculates body surface area using DuBois formula
        
        Args:
            height_cm: Height in centimeters
            weight_kg: Weight in kilograms
            
        Returns:
            Body surface area in m²
        """
        return math.sqrt((height_cm * weight_kg) / self.BSA_CONSTANT)
    
    def _calculate_cci(self, count_increment: int, bsa: float, platelet_dose: float) -> float:
        """
        Calculates the Corrected Count Increment
        
        Args:
            count_increment: Difference between post- and pre-transfusion counts
            bsa: Body surface area in m²
            platelet_dose: Platelet dose in ×10¹¹ platelets
            
        Returns:
            CCI value
        """
        if platelet_dose == 0:
            raise ValueError("Platelet dose cannot be zero")
        
        return (count_increment * bsa) / platelet_dose
    
    def _get_interpretation(self, cci_value: float, time_point: str) -> Dict[str, Any]:
        """
        Determines the interpretation based on CCI value and time point
        
        Args:
            cci_value: Calculated CCI value
            time_point: Time after transfusion
            
        Returns:
            Dict with interpretation details
        """
        
        if time_point == "1_hour":
            threshold = self.THRESHOLD_1_HOUR
            time_description = "1 hour"
        else:  # "20_hour"
            threshold = self.THRESHOLD_20_HOUR
            time_description = "20 hours"
        
        adequate_response = cci_value > threshold
        
        if adequate_response:
            stage = "Successful Transfusion"
            description = f"Good platelet response at {time_description}"
            interpretation = (
                f"CCI of {cci_value:.1f} at {time_description} post-transfusion is above the "
                f"threshold of {threshold:,}, indicating successful platelet transfusion with "
                f"adequate platelet response. This suggests good platelet survival and function."
            )
        else:
            stage = "Poor Response"
            description = f"Inadequate platelet response at {time_description}"
            interpretation = (
                f"CCI of {cci_value:.1f} at {time_description} post-transfusion is at or below the "
                f"threshold of {threshold:,}, suggesting poor platelet response. Consider platelet "
                f"refractoriness and evaluate for underlying causes such as fever, sepsis, DIC, "
                f"bleeding, splenomegaly, or drug interactions. Repeat transfusion may be needed."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "threshold": threshold,
            "adequate_response": adequate_response
        }


def calculate_corrected_count_increment(
    pre_transfusion_count: int,
    post_transfusion_count: int,
    time_after_transfusion: str,
    patient_height: float,
    patient_weight: float,
    platelet_unit_content: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CorrectedCountIncrementCalculator()
    return calculator.calculate(
        pre_transfusion_count=pre_transfusion_count,
        post_transfusion_count=post_transfusion_count,
        time_after_transfusion=time_after_transfusion,
        patient_height=patient_height,
        patient_weight=patient_weight,
        platelet_unit_content=platelet_unit_content
    )