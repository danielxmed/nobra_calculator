"""
tPA (Alteplase) Dosing for Ischemic Stroke Calculator

Calculates alteplase dose for acute ischemic stroke treatment using 
weight-based dosing protocol (0.9 mg/kg) with proper bolus and 
infusion component calculations.

References (Vancouver style):
1. The National Institute of Neurological Disorders and Stroke rt-PA Stroke 
   Study Group. Tissue plasminogen activator for acute ischemic stroke. 
   N Engl J Med. 1995 Dec 14;333(24):1581-7. doi: 10.1056/NEJM199512143332401.
2. Hacke W, Kaste M, Bluhmki E, Brozman M, Dávalos A, Guidetti D, et al. 
   Thrombolysis with alteplase 3 to 4.5 hours after acute ischemic stroke. 
   N Engl J Med. 2008 Sep 25;359(13):1317-29. doi: 10.1056/NEJMoa0804656.
3. Powers WJ, Rabinstein AA, Ackerson T, Adeoye OM, Bambakidis NC, Becker K, 
   et al. Guidelines for the Early Management of Patients With Acute Ischemic 
   Stroke: 2019 Update to the 2018 Guidelines for the Early Management of 
   Acute Ischemic Stroke. Stroke. 2019 Dec;50(12):e344-e418. 
   doi: 10.1161/STR.0000000000000211.
"""

from typing import Dict, Any


class TpaAlteplaseDosingStrokeCalculator:
    """Calculator for tPA (Alteplase) dosing in acute ischemic stroke"""
    
    def __init__(self):
        # Dosing constants
        self.DOSE_PER_KG = 0.9  # mg/kg
        self.MAXIMUM_DOSE = 90.0  # mg
        self.BOLUS_PERCENTAGE = 0.10  # 10% of total dose
        self.INFUSION_PERCENTAGE = 0.90  # 90% of total dose
        self.BOLUS_DURATION_MINUTES = 1  # minutes
        self.INFUSION_DURATION_MINUTES = 60  # minutes
        
        # Safety thresholds
        self.MIN_WEIGHT = 30.0  # kg
        self.MAX_WEIGHT = 200.0  # kg
        self.MAXIMUM_DOSE_WEIGHT_THRESHOLD = 100.0  # kg
    
    def calculate(self, weight: float) -> Dict[str, Any]:
        """
        Calculates tPA (Alteplase) dosing for acute ischemic stroke
        
        The standard dose is 0.9 mg/kg with a maximum total dose of 90 mg.
        The dose is administered as 10% IV bolus over 1 minute, followed
        by 90% as continuous infusion over 60 minutes.
        
        Args:
            weight (float): Patient weight in kilograms
            
        Returns:
            Dict with complete dosing regimen and administration instructions
        """
        
        # Validate inputs
        self._validate_inputs(weight)
        
        # Calculate total dose
        total_dose = self._calculate_total_dose(weight)
        
        # Calculate bolus and infusion components
        bolus_dose = self._calculate_bolus_dose(total_dose)
        infusion_dose = self._calculate_infusion_dose(total_dose)
        
        # Determine if maximum dose was applied
        max_dose_applied = weight > self.MAXIMUM_DOSE_WEIGHT_THRESHOLD
        
        # Get interpretation
        interpretation = self._get_interpretation(total_dose, weight, max_dose_applied)
        
        return {
            "result": {
                "total_dose": total_dose,
                "bolus_dose": bolus_dose,
                "infusion_dose": infusion_dose,
                "bolus_duration_minutes": self.BOLUS_DURATION_MINUTES,
                "infusion_duration_minutes": self.INFUSION_DURATION_MINUTES,
                "max_dose_applied": max_dose_applied,
                "actual_dose_per_kg": round(total_dose / weight, 3)
            },
            "unit": "mg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, weight: float):
        """Validates input parameters for tPA dosing calculation"""
        
        # Weight validation
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        
        if weight <= 0:
            raise ValueError("Weight must be greater than 0 kg")
        
        if weight < self.MIN_WEIGHT:
            raise ValueError(f"Weight must be at least {self.MIN_WEIGHT} kg for safety")
        
        if weight > self.MAX_WEIGHT:
            raise ValueError(f"Weight must not exceed {self.MAX_WEIGHT} kg")
    
    def _calculate_total_dose(self, weight: float) -> float:
        """Calculates total tPA dose with maximum dose cap"""
        
        # Calculate weight-based dose
        calculated_dose = weight * self.DOSE_PER_KG
        
        # Apply maximum dose cap
        total_dose = min(calculated_dose, self.MAXIMUM_DOSE)
        
        # Round to one decimal place for practical dosing
        return round(total_dose, 1)
    
    def _calculate_bolus_dose(self, total_dose: float) -> float:
        """Calculates bolus dose (10% of total dose)"""
        bolus_dose = total_dose * self.BOLUS_PERCENTAGE
        return round(bolus_dose, 1)
    
    def _calculate_infusion_dose(self, total_dose: float) -> float:
        """Calculates infusion dose (90% of total dose)"""
        infusion_dose = total_dose * self.INFUSION_PERCENTAGE
        return round(infusion_dose, 1)
    
    def _get_interpretation(self, total_dose: float, weight: float, 
                          max_dose_applied: bool) -> Dict[str, str]:
        """
        Provides clinical interpretation and administration instructions
        
        Args:
            total_dose (float): Calculated total dose in mg
            weight (float): Patient weight in kg
            max_dose_applied (bool): Whether maximum dose cap was applied
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if max_dose_applied:
            return {
                "stage": "Maximum Dose Applied",
                "description": "90 mg maximum dose for patients >100 kg",
                "interpretation": (
                    f"Patient weighs {weight} kg, which exceeds 100 kg threshold. "
                    f"Maximum dose of {total_dose} mg applied (instead of "
                    f"{round(weight * self.DOSE_PER_KG, 1)} mg) for safety. "
                    f"Administer {round(total_dose * self.BOLUS_PERCENTAGE, 1)} mg "
                    f"as IV bolus over 1 minute, followed by "
                    f"{round(total_dose * self.INFUSION_PERCENTAGE, 1)} mg "
                    f"as continuous infusion over 60 minutes. Monitor closely for "
                    f"bleeding complications. Note: Up to 20 mg may remain in pump "
                    f"tubing; flush with 50 mL normal saline after infusion."
                )
            }
        
        else:
            return {
                "stage": "Standard Weight-Based Dosing",
                "description": f"0.9 mg/kg dosing protocol applied",
                "interpretation": (
                    f"Patient weighs {weight} kg. Total dose: {total_dose} mg "
                    f"(0.9 mg/kg). Administer {round(total_dose * self.BOLUS_PERCENTAGE, 1)} mg "
                    f"as IV bolus over 1 minute, followed by "
                    f"{round(total_dose * self.INFUSION_PERCENTAGE, 1)} mg "
                    f"as continuous infusion over 60 minutes. Ensure treatment "
                    f"is initiated within 3-4.5 hours of stroke symptom onset. "
                    f"Monitor for bleeding complications and neurological changes. "
                    f"Note: Up to 20 mg may remain in pump tubing; flush with "
                    f"50 mL normal saline after infusion."
                )
            }


def calculate_tpa_alteplase_dosing_stroke(weight: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates tPA (Alteplase) dosing for acute ischemic stroke treatment.
    
    Args:
        weight (float): Patient weight in kilograms
        
    Returns:
        Dict with complete dosing regimen and administration instructions
    """
    calculator = TpaAlteplaseDosingStrokeCalculator()
    return calculator.calculate(weight)