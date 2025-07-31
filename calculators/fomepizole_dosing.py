"""
Fomepizole Dosing Calculator

Calculates fomepizole (4-methylpyrazole) dosing for treatment of methanol and ethylene glycol poisoning.
Provides initial loading dose, maintenance doses, and special hemodialysis considerations.

References:
1. Howland MA. Antidotes in Depth: Fomepizole. In: Nelson LS, Howland MA, Lewin NA, Smith SW, 
   Goldfrank LR, Hoffman RS, editors. Goldfrank's Toxicologic Emergencies. 11th ed. New York: 
   McGraw-Hill; 2019.
2. Brent J, McMartin K, Phillips S, et al. Fomepizole for the treatment of ethylene glycol poisoning. 
   N Engl J Med. 1999;340(11):832-838.
3. Brent J, McMartin K, Phillips S, et al. Fomepizole for the treatment of methanol poisoning. 
   N Engl J Med. 2001;344(6):424-429.
"""

from typing import Dict, Any, Optional


class FomepizoleDosingCalculator:
    """Calculator for Fomepizole Dosing"""
    
    def __init__(self):
        # Dosing constants (mg/kg)
        self.INITIAL_LOADING_DOSE = 15.0  # mg/kg
        self.MAINTENANCE_FIRST_FOUR_DOSES = 10.0  # mg/kg q12h
        self.MAINTENANCE_AFTER_48H = 15.0  # mg/kg q12h
        self.DIALYSIS_DOSE = 10.0  # mg/kg q4h during dialysis
        self.DIALYSIS_CONTINUOUS_MIN = 1.0  # mg/kg/h minimum continuous infusion
        self.DIALYSIS_CONTINUOUS_MAX = 1.5  # mg/kg/h maximum continuous infusion
    
    def calculate(self, weight: float, clinical_scenario: str, hours_since_last_dose: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates fomepizole dose based on clinical scenario
        
        Args:
            weight (float): Patient body weight in kg
            clinical_scenario (str): Clinical scenario (initial_loading, maintenance_no_dialysis, 
                                   during_hemodialysis, post_hemodialysis)
            hours_since_last_dose (Optional[float]): Hours since last dose (for dialysis scenarios)
            
        Returns:
            Dict with the dose, unit, interpretation, and administration details
        """
        
        # Validations
        self._validate_inputs(weight, clinical_scenario, hours_since_last_dose)
        
        # Calculate dose based on scenario
        dose_result = self._calculate_dose(weight, clinical_scenario, hours_since_last_dose)
        
        # Get interpretation and administration details
        interpretation_data = self._get_interpretation(clinical_scenario, dose_result)
        
        return {
            "result": dose_result["dose"],
            "unit": "mg",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"],
            "additional_info": dose_result.get("additional_info", "")
        }
    
    def _validate_inputs(self, weight: float, clinical_scenario: str, hours_since_last_dose: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        
        if weight < 1 or weight > 300:
            raise ValueError("Weight must be between 1 and 300 kg")
        
        valid_scenarios = ["initial_loading", "maintenance_no_dialysis", "during_hemodialysis", "post_hemodialysis"]
        if clinical_scenario not in valid_scenarios:
            raise ValueError(f"Clinical scenario must be one of: {', '.join(valid_scenarios)}")
        
        # For dialysis scenarios, hours_since_last_dose is required
        if clinical_scenario in ["during_hemodialysis", "post_hemodialysis"] and hours_since_last_dose is None:
            raise ValueError("Hours since last dose is required for hemodialysis scenarios")
        
        if hours_since_last_dose is not None:
            if not isinstance(hours_since_last_dose, (int, float)):
                raise ValueError("Hours since last dose must be a number")
            if hours_since_last_dose < 0 or hours_since_last_dose > 48:
                raise ValueError("Hours since last dose must be between 0 and 48 hours")
    
    def _calculate_dose(self, weight: float, clinical_scenario: str, hours_since_last_dose: Optional[float]) -> Dict[str, Any]:
        """Calculates the appropriate fomepizole dose"""
        
        if clinical_scenario == "initial_loading":
            dose = weight * self.INITIAL_LOADING_DOSE
            additional_info = "Initial loading dose. Administer IV over 30 minutes."
            
        elif clinical_scenario == "maintenance_no_dialysis":
            # First 4 doses (within 48 hours): 10 mg/kg q12h
            # After 48 hours: 15 mg/kg q12h
            dose_10mg = weight * self.MAINTENANCE_FIRST_FOUR_DOSES
            dose_15mg = weight * self.MAINTENANCE_AFTER_48H
            additional_info = f"First 4 doses (0-48h): {dose_10mg:.0f} mg q12h. After 48h: {dose_15mg:.0f} mg q12h."
            dose = dose_10mg  # Return the first dose for primary result
            
        elif clinical_scenario == "during_hemodialysis":
            dose = weight * self.DIALYSIS_DOSE
            continuous_min = weight * self.DIALYSIS_CONTINUOUS_MIN
            continuous_max = weight * self.DIALYSIS_CONTINUOUS_MAX
            additional_info = (f"During dialysis: {dose:.0f} mg q4h OR continuous infusion "
                             f"{continuous_min:.1f}-{continuous_max:.1f} mg/h")
            
        elif clinical_scenario == "post_hemodialysis":
            if hours_since_last_dose >= 6:
                # Give at dialysis onset if last dose was >6 hours prior
                dose = weight * self.DIALYSIS_DOSE
                additional_info = "Give full dose at dialysis onset (≥6h since last dose)."
            elif hours_since_last_dose >= 3:
                # Give scheduled dose if >3 hours since last dose
                dose = weight * self.MAINTENANCE_FIRST_FOUR_DOSES
                additional_info = "Give scheduled dose at dialysis completion (3-6h since last dose)."
            elif hours_since_last_dose >= 1:
                # Give half dose if 1-3 hours since last dose
                dose = (weight * self.MAINTENANCE_FIRST_FOUR_DOSES) / 2
                additional_info = "Give half dose at dialysis completion (1-3h since last dose)."
            else:
                # No dose needed if <1 hour since last dose
                dose = 0
                additional_info = "No dose needed at dialysis completion (<1h since last dose)."
        
        return {
            "dose": round(dose, 0),
            "additional_info": additional_info
        }
    
    def _get_interpretation(self, clinical_scenario: str, dose_result: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines the interpretation based on the clinical scenario and dose
        
        Args:
            clinical_scenario (str): The clinical scenario
            dose_result (Dict): Result from dose calculation
            
        Returns:
            Dict with interpretation details
        """
        
        base_interpretation = (
            "Fomepizole is the antidote of choice for methanol and ethylene glycol poisoning. "
            "It competitively inhibits alcohol dehydrogenase, preventing formation of toxic metabolites. "
            "Administer IV over 30 minutes in ≥100 mL diluent. Monitor for side effects and treatment endpoints."
        )
        
        if clinical_scenario == "initial_loading":
            return {
                "stage": "Initial Loading Dose",
                "description": "First dose of fomepizole",
                "interpretation": f"{base_interpretation} This is the initial loading dose of 15 mg/kg."
            }
        
        elif clinical_scenario == "maintenance_no_dialysis":
            return {
                "stage": "Maintenance Dosing",
                "description": "Maintenance dosing for patients not on dialysis",
                "interpretation": (f"{base_interpretation} Maintenance dosing: 10 mg/kg q12h for first 4 doses, "
                                f"then 15 mg/kg q12h until treatment endpoints are met. "
                                f"{dose_result.get('additional_info', '')}")
            }
        
        elif clinical_scenario == "during_hemodialysis":
            return {
                "stage": "Hemodialysis Dosing",
                "description": "Dosing during hemodialysis",
                "interpretation": (f"{base_interpretation} During hemodialysis, fomepizole is removed and "
                                f"dosing frequency must be increased. Give every 4 hours or as continuous infusion. "
                                f"{dose_result.get('additional_info', '')}")
            }
        
        elif clinical_scenario == "post_hemodialysis":
            if dose_result["dose"] == 0:
                return {
                    "stage": "Post-Dialysis Assessment",
                    "description": "No additional dose needed",
                    "interpretation": (f"{base_interpretation} No additional dose needed at this time based on "
                                     f"timing of last dose. Continue with regular dosing schedule.")
                }
            else:
                return {
                    "stage": "Post-Dialysis Dosing",
                    "description": "Dose adjustment after hemodialysis",
                    "interpretation": (f"{base_interpretation} Post-dialysis dosing depends on time since last dose. "
                                     f"{dose_result.get('additional_info', '')}")
                }
        
        return {
            "stage": "Standard Protocol",
            "description": "Follow standard fomepizole protocol",
            "interpretation": base_interpretation
        }


def calculate_fomepizole_dosing(weight: float, clinical_scenario: str, hours_since_last_dose: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fomepizole_dosing pattern
    """
    calculator = FomepizoleDosingCalculator()
    return calculator.calculate(weight, clinical_scenario, hours_since_last_dose)