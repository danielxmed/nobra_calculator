"""
Antivenom Dosing Algorithm Calculator

Doses antivenom (CroFab only, not Anavip) for pit viper snakebites.
This unified treatment algorithm assists with quick identification and management 
of patients who may benefit from treatment with Crotalidae Polyvalent Immune Fab (CroFab®).

References:
- Lavonas EJ, Ruha AM, Banner W, et al. Unified treatment algorithm for the management 
  of crotaline snakebite in the United States: results of an evidence-informed consensus 
  workshop. BMC Emerg Med. 2011;11:2.
- Dart RC, Seifert SA, Boyer LV, et al. A randomized multicenter trial of crotalinae 
  polyvalent immune Fab (ovine) antivenom for the treatment for crotaline snakebite 
  in the United States. Arch Intern Med. 2001;161(16):2030-2036.
"""

from typing import Dict, Any


class AntivenomDosingAlgorithmCalculator:
    """Calculator for Antivenom Dosing Algorithm"""
    
    def __init__(self):
        # Algorithm constants
        self.STANDARD_INITIAL_DOSE_MIN = 4
        self.STANDARD_INITIAL_DOSE_MAX = 6
        self.SEVERE_INITIAL_DOSE_MAX = 12
        self.MAINTENANCE_DOSE = 2
        self.MAINTENANCE_INTERVALS = 3
    
    def calculate(self, signs_of_envenomation: str, severity_grade: str, patient_weight_kg: float) -> Dict[str, Any]:
        """
        Calculates the antivenom dosing recommendation based on clinical presentation
        
        Args:
            signs_of_envenomation (str): "yes" or "no" - presence of envenomation signs
            severity_grade (str): Clinical severity grade ("none", "minimal", "moderate", "severe")
            patient_weight_kg (float): Patient weight in kg (dosing same for adults/pediatrics)
            
        Returns:
            Dict with the dosing recommendation and clinical guidance
        """
        
        # Validations
        self._validate_inputs(signs_of_envenomation, severity_grade, patient_weight_kg)
        
        # Determine dosing based on algorithm
        dosing_result = self._calculate_dosing(signs_of_envenomation, severity_grade)
        
        # Get interpretation
        interpretation = self._get_interpretation(dosing_result, severity_grade)
        
        return {
            "result": dosing_result["initial_dose"],
            "unit": "vials",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "additional_info": {
                "maintenance_dose": f"{self.MAINTENANCE_DOSE} vials every 6 hours for {self.MAINTENANCE_INTERVALS} doses",
                "poison_control": "1-800-222-1222",
                "monitoring_requirements": dosing_result["monitoring"]
            }
        }
    
    def _validate_inputs(self, signs_of_envenomation: str, severity_grade: str, patient_weight_kg: float):
        """Validates input parameters"""
        
        if not isinstance(signs_of_envenomation, str):
            raise ValueError("Signs of envenomation must be a string")
            
        if signs_of_envenomation.lower() not in ["yes", "no"]:
            raise ValueError("Signs of envenomation must be 'yes' or 'no'")
        
        if not isinstance(severity_grade, str):
            raise ValueError("Severity grade must be a string")
            
        if severity_grade.lower() not in ["none", "minimal", "moderate", "severe"]:
            raise ValueError("Severity grade must be 'none', 'minimal', 'moderate', or 'severe'")
        
        if not isinstance(patient_weight_kg, (int, float)):
            raise ValueError("Patient weight must be a number")
        
        if patient_weight_kg < 1 or patient_weight_kg > 300:
            raise ValueError("Patient weight must be between 1 and 300 kg")
    
    def _calculate_dosing(self, signs_of_envenomation: str, severity_grade: str) -> Dict[str, Any]:
        """Implements the antivenom dosing algorithm"""
        
        signs_present = signs_of_envenomation.lower() == "yes"
        severity = severity_grade.lower()
        
        # No signs of envenomation = no antivenom
        if not signs_present or severity == "none":
            return {
                "initial_dose": 0,
                "monitoring": "Close observation for progression of symptoms"
            }
        
        # Determine initial dose based on severity
        if severity == "minimal":
            initial_dose = self.STANDARD_INITIAL_DOSE_MIN  # 4 vials
            monitoring = "Monitor for initial control in ~1 hour"
        elif severity == "moderate":  
            initial_dose = self.STANDARD_INITIAL_DOSE_MAX  # 6 vials
            monitoring = "Monitor for initial control in ~1 hour, may need additional 4-6 vials"
        elif severity == "severe":
            initial_dose = self.SEVERE_INITIAL_DOSE_MAX  # Up to 12 vials
            monitoring = "Close monitoring required, likely need additional doses"
        else:
            # Default to standard dose if unclear
            initial_dose = self.STANDARD_INITIAL_DOSE_MIN
            monitoring = "Monitor for initial control in ~1 hour"
        
        return {
            "initial_dose": initial_dose,
            "monitoring": monitoring
        }
    
    def _get_interpretation(self, dosing_result: Dict[str, Any], severity_grade: str) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the dosing result
        
        Args:
            dosing_result (Dict): Result from dosing calculation
            severity_grade (str): Clinical severity grade
            
        Returns:
            Dict with interpretation details
        """
        
        initial_dose = dosing_result["initial_dose"]
        severity = severity_grade.lower()
        
        if initial_dose == 0:
            return {
                "stage": "No Treatment",
                "description": "No antivenom needed",
                "interpretation": (
                    "No signs of envenomation present. Monitor patient closely for progression. "
                    "Provide supportive care including tetanus prophylaxis, wound care, and pain management. "
                    "Mark leading edge of any swelling every 15-30 minutes. "
                    "Report case to poison control (1-800-222-1222)."
                )
            }
        elif initial_dose <= 6:
            return {
                "stage": "Standard Initial Dose",
                "description": "Standard initial antivenom dose",
                "interpretation": (
                    f"Administer {initial_dose} vials CroFab IV over 60 minutes. "
                    "Monitor for initial control of envenomation: "
                    "(1) arrest of local effects progression, "
                    "(2) resolution of systemic effects, "
                    "(3) reduction of hematologic abnormalities. "
                    "If initial control not achieved in ~1 hour, administer additional 4-6 vials. "
                    "Once initial control achieved, give maintenance doses of 2 vials every 6 hours "
                    "for 3 doses (at 6, 12, and 18 hours). "
                    "Contact poison control (1-800-222-1222)."
                )
            }
        else:
            return {
                "stage": "Higher Initial Dose",
                "description": "Higher initial antivenom dose for severe cases",
                "interpretation": (
                    f"Severe envenomation requires {initial_dose} vials CroFab IV over 60 minutes. "
                    "Monitor closely for initial control of envenomation. "
                    "May require additional doses if control not achieved. "
                    "Once initial control achieved, give maintenance doses of 2 vials every 6 hours "
                    "for 3 doses (at 6, 12, and 18 hours). "
                    "Consider ICU monitoring. "
                    "Immediately contact poison control (1-800-222-1222) and consider toxicology consultation."
                )
            }


def calculate_antivenom_dosing_algorithm(signs_of_envenomation: str, severity_grade: str, patient_weight_kg: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_antivenom_dosing_algorithm pattern
    """
    calculator = AntivenomDosingAlgorithmCalculator()
    return calculator.calculate(signs_of_envenomation, severity_grade, patient_weight_kg)