"""
Barnes Jewish Hospital Stroke Dysphagia Screen Calculator

Assesses ability to swallow without aspiration after stroke.

References:
1. Edmiaston J, et al. Validation of a dysphagia screening tool in acute 
   stroke patients. Am J Crit Care. 2010 Jul;19(4):357-64.
"""

from typing import Dict, Any, Optional


class BarnesJewishDysphagiaCalculator:
    """Calculator for Barnes Jewish Hospital Stroke Dysphagia Screen"""
    
    def __init__(self):
        # Define preliminary screening criteria
        self.preliminary_criteria = [
            "gcs_less_than_13",
            "facial_asymmetry", 
            "tongue_asymmetry",
            "palatal_asymmetry"
        ]
        
        # Define water test criteria
        self.water_test_criteria = [
            "throat_clearing_initial",
            "cough_initial",
            "voice_change_initial",
            "throat_clearing_delayed",
            "cough_delayed", 
            "voice_change_delayed"
        ]
    
    def calculate(self, gcs_less_than_13: str, facial_asymmetry: str,
                  tongue_asymmetry: str, palatal_asymmetry: str,
                  water_test_performed: str,
                  throat_clearing_initial: Optional[str] = None,
                  cough_initial: Optional[str] = None,
                  voice_change_initial: Optional[str] = None,
                  throat_clearing_delayed: Optional[str] = None,
                  cough_delayed: Optional[str] = None,
                  voice_change_delayed: Optional[str] = None) -> Dict[str, Any]:
        """
        Performs Barnes Jewish Hospital Stroke Dysphagia Screen
        
        Args:
            gcs_less_than_13 (str): GCS < 13 ("yes" or "no")
            facial_asymmetry (str): Facial asymmetry/weakness ("yes" or "no")
            tongue_asymmetry (str): Tongue asymmetry/weakness ("yes" or "no")
            palatal_asymmetry (str): Palatal asymmetry/weakness ("yes" or "no")
            water_test_performed (str): Water test done ("yes", "no", "not_applicable")
            throat_clearing_initial (str, optional): Throat clearing during swallow
            cough_initial (str, optional): Cough during swallow
            voice_change_initial (str, optional): Voice change during swallow
            throat_clearing_delayed (str, optional): Throat clearing after 1 min
            cough_delayed (str, optional): Cough after 1 min
            voice_change_delayed (str, optional): Voice change after 1 min
            
        Returns:
            Dict with screening result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(gcs_less_than_13, facial_asymmetry, tongue_asymmetry,
                            palatal_asymmetry, water_test_performed)
        
        # Check preliminary screening questions
        preliminary_fail = self._check_preliminary_criteria(
            gcs_less_than_13, facial_asymmetry, tongue_asymmetry, palatal_asymmetry
        )
        
        if preliminary_fail:
            # Failed preliminary screening
            result = "Fail"
            interpretation = ("Patient failed preliminary screening due to neurological deficits. " +
                            "Keep NPO (nothing by mouth) and refer to Speech-Language Pathology " +
                            "for comprehensive swallowing evaluation before initiating oral intake.")
        
        elif water_test_performed == "no" or water_test_performed == "not_applicable":
            # Water test not performed
            result = "Fail"
            interpretation = ("Screening incomplete - water test not performed. " +
                            "Complete screening required before allowing oral intake. " +
                            "Refer to Speech-Language Pathology for evaluation.")
        
        else:
            # Check water test results
            water_test_fail = self._check_water_test(
                throat_clearing_initial, cough_initial, voice_change_initial,
                throat_clearing_delayed, cough_delayed, voice_change_delayed
            )
            
            if water_test_fail:
                result = "Fail"
                interpretation = ("Patient failed water swallow test due to signs of aspiration. " +
                                "Keep NPO (nothing by mouth) and refer to Speech-Language Pathology " +
                                "for comprehensive swallowing evaluation before initiating oral intake.")
            else:
                result = "Pass"
                interpretation = ("Patient passed dysphagia screen. Can be started on regular diet. " +
                                "Continue to monitor for any changes in swallowing ability.")
        
        return {
            "result": result,
            "unit": "",
            "interpretation": interpretation,
            "stage": result,
            "stage_description": "No dysphagia detected" if result == "Pass" else "Dysphagia risk identified"
        }
    
    def _validate_inputs(self, gcs_less_than_13: str, facial_asymmetry: str,
                        tongue_asymmetry: str, palatal_asymmetry: str,
                        water_test_performed: str):
        """Validates input parameters"""
        
        yes_no_params = {
            "GCS less than 13": gcs_less_than_13,
            "Facial asymmetry": facial_asymmetry,
            "Tongue asymmetry": tongue_asymmetry,
            "Palatal asymmetry": palatal_asymmetry
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        if water_test_performed not in ["yes", "no", "not_applicable"]:
            raise ValueError("Water test performed must be 'yes', 'no', or 'not_applicable'")
    
    def _check_preliminary_criteria(self, gcs_less_than_13: str, facial_asymmetry: str,
                                   tongue_asymmetry: str, palatal_asymmetry: str) -> bool:
        """
        Checks if any preliminary criteria fail
        
        Returns:
            bool: True if ANY preliminary question is "yes" (fail), False if all are "no" (pass)
        """
        return any([
            gcs_less_than_13 == "yes",
            facial_asymmetry == "yes",
            tongue_asymmetry == "yes",
            palatal_asymmetry == "yes"
        ])
    
    def _check_water_test(self, throat_clearing_initial: Optional[str],
                         cough_initial: Optional[str], voice_change_initial: Optional[str],
                         throat_clearing_delayed: Optional[str], cough_delayed: Optional[str],
                         voice_change_delayed: Optional[str]) -> bool:
        """
        Checks if water test shows any signs of aspiration
        
        Returns:
            bool: True if ANY water test sign is positive (fail), False if all negative (pass)
        """
        water_test_results = [
            throat_clearing_initial,
            cough_initial,
            voice_change_initial,
            throat_clearing_delayed,
            cough_delayed,
            voice_change_delayed
        ]
        
        # Check if any water test parameter is "yes"
        return any(result == "yes" for result in water_test_results if result is not None)


def calculate_barnes_jewish_dysphagia(
    gcs_less_than_13: str, facial_asymmetry: str, tongue_asymmetry: str,
    palatal_asymmetry: str, water_test_performed: str,
    throat_clearing_initial: Optional[str] = None,
    cough_initial: Optional[str] = None,
    voice_change_initial: Optional[str] = None,
    throat_clearing_delayed: Optional[str] = None,
    cough_delayed: Optional[str] = None,
    voice_change_delayed: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BarnesJewishDysphagiaCalculator()
    return calculator.calculate(
        gcs_less_than_13, facial_asymmetry, tongue_asymmetry,
        palatal_asymmetry, water_test_performed,
        throat_clearing_initial, cough_initial, voice_change_initial,
        throat_clearing_delayed, cough_delayed, voice_change_delayed
    )