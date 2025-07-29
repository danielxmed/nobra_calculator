"""
BeAM Value Calculator

Calculates the difference between bedtime and morning fasting blood glucose to guide
prandial insulin therapy decisions in patients with type 2 diabetes.

References (Vancouver style):
1. Raz I, Wilson PW, Strojek K, Kowalska I, Bozikov V, Gitt AK, et al. Effects of 
   prandial versus fasting glycemia on cardiovascular outcomes in type 2 diabetes: 
   the HEART2D trial. Diabetes Care. 2009 Mar;32(3):381-6.
2. Blonde L, Merilainen M, Karwe V, Raskin P; TITRATE Study Group. Patient-directed 
   titration for achieving glycaemic goals using a once-daily basal insulin analogue: 
   an assessment of two different fasting plasma glucose targets - the TITRATE study. 
   Diabetes Obes Metab. 2009 Jun;11(6):623-31.
3. Garber AJ, King AB, Del Prato S, Sreenan S, Balci MK, Muñoz-Torres M, et al. 
   Insulin degludec, an ultra-longacting basal insulin, versus insulin glargine in 
   basal-bolus treatment with mealtime insulin aspart in type 2 diabetes (BEGIN 
   Basal-Bolus Type 2): a phase 3, randomised, open-label, treat-to-target 
   non-inferiority trial. Lancet. 2012 Apr 21;379(9825):1498-507.
"""

from typing import Dict, Any


class BeamValueCalculator:
    """Calculator for BeAM Value"""
    
    def __init__(self):
        # BeAM thresholds
        self.HIGH_BEAM_THRESHOLD = 30.0
        self.NEGATIVE_BEAM_THRESHOLD = 0.0
    
    def calculate(self, bedtime_glucose: float, morning_glucose: float) -> Dict[str, Any]:
        """
        Calculates the BeAM value
        
        Args:
            bedtime_glucose (float): Bedtime blood glucose level (mg/dL)
            morning_glucose (float): Morning fasting blood glucose level (mg/dL)
            
        Returns:
            Dict with BeAM value and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(bedtime_glucose, morning_glucose)
        
        # Calculate BeAM value
        beam_value = self._calculate_beam_value(bedtime_glucose, morning_glucose)
        
        # Get interpretation
        interpretation = self._get_interpretation(beam_value, bedtime_glucose, morning_glucose)
        
        return {
            "result": beam_value,
            "unit": "mg/dL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bedtime_glucose: float, morning_glucose: float):
        """Validates input parameters"""
        
        if not isinstance(bedtime_glucose, (int, float)):
            raise ValueError("Bedtime glucose must be a number")
        
        if not isinstance(morning_glucose, (int, float)):
            raise ValueError("Morning glucose must be a number")
        
        if bedtime_glucose < 40 or bedtime_glucose > 600:
            raise ValueError("Bedtime glucose must be between 40 and 600 mg/dL")
            
        if morning_glucose < 40 or morning_glucose > 600:
            raise ValueError("Morning glucose must be between 40 and 600 mg/dL")
    
    def _calculate_beam_value(self, bedtime_glucose: float, morning_glucose: float) -> float:
        """Calculates BeAM value using the standard formula"""
        
        # BeAM Value = Bedtime glucose - Morning glucose
        beam_value = bedtime_glucose - morning_glucose
        
        # Round to 1 decimal place for clinical relevance
        return round(beam_value, 1)
    
    def _get_interpretation(self, beam_value: float, bedtime_glucose: float, 
                          morning_glucose: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on BeAM value
        
        Args:
            beam_value (float): Calculated BeAM value
            bedtime_glucose (float): Original bedtime glucose value
            morning_glucose (float): Original morning glucose value
            
        Returns:
            Dict with clinical interpretation
        """
        
        if beam_value >= self.HIGH_BEAM_THRESHOLD:
            return {
                "stage": "High BeAM",
                "description": f"Large BeAM value (≥30 mg/dL)",
                "interpretation": (
                    f"BeAM value: {beam_value} mg/dL (bedtime {bedtime_glucose} mg/dL - "
                    f"morning {morning_glucose} mg/dL). High BeAM value (≥30 mg/dL) suggests "
                    "postprandial glucose excursions during the day leading to high bedtime "
                    "glucose and well-controlled fasting glucose. This is an indicator for "
                    "prandial insulin supplementation rather than advancing basal insulin dose. "
                    "Clinical recommendation: Consider adding rapid-acting insulin before meals "
                    "to target postprandial hyperglycemia. Monitor HbA1c and adjust therapy "
                    "accordingly. The BeAM value helps identify patients who would benefit from "
                    "targeting postprandial control rather than continuing to increase basal insulin."
                )
            }
        
        elif beam_value >= self.NEGATIVE_BEAM_THRESHOLD:
            return {
                "stage": "Medium/Low BeAM",
                "description": f"Medium/Low BeAM value (0-29 mg/dL)",
                "interpretation": (
                    f"BeAM value: {beam_value} mg/dL (bedtime {bedtime_glucose} mg/dL - "
                    f"morning {morning_glucose} mg/dL). Medium/Low BeAM value (0-29 mg/dL) "
                    "suggests that prandial insulin supplementation may be of little benefit. "
                    "The glucose difference between bedtime and morning is modest, indicating "
                    "relatively stable overnight glucose levels. Clinical recommendation: "
                    "Consider optimizing basal insulin dosing or other diabetes management "
                    "strategies before adding prandial insulin. Focus on lifestyle modifications, "
                    "medication adherence, and basal insulin optimization."
                )
            }
        
        else:  # beam_value < 0
            return {
                "stage": "Negative BeAM",
                "description": f"Negative BeAM value (<0 mg/dL)",
                "interpretation": (
                    f"BeAM value: {beam_value} mg/dL (bedtime {bedtime_glucose} mg/dL - "
                    f"morning {morning_glucose} mg/dL). Negative BeAM value indicates higher "
                    "morning glucose than bedtime glucose. This pattern suggests dawn phenomenon "
                    "or inadequate basal insulin coverage overnight. Patients with negative BeAM "
                    "tend to be younger, have shorter diabetes duration, and higher fasting glucose "
                    "levels. Clinical recommendation: This is a contraindication for intensification "
                    "of prandial insulin therapy. Focus on optimizing basal insulin dosing, consider "
                    "timing adjustments, or evaluate for dawn phenomenon. Address fasting glucose "
                    "control before targeting postprandial glucose."
                )
            }


def calculate_beam_value(bedtime_glucose: float, morning_glucose: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BeamValueCalculator()
    return calculator.calculate(bedtime_glucose, morning_glucose)