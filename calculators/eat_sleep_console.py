"""
Eat, Sleep, Console (ESC) Assessment Calculator

Aids in management of infants with neonatal abstinence syndrome (NAS) by focusing 
on functional assessment rather than symptom scoring. This approach emphasizes 
nonpharmacologic interventions and family-centered care to optimize infant functioning.

References:
1. Grossman MR, Berkwitt AK, Osborn RR, Xu Y, Esserman DA, Shapiro ED, et al. 
   An Initiative to Improve the Quality of Care of Infants with Neonatal Abstinence 
   Syndrome. Pediatrics. 2017;139(6):e20163360. doi: 10.1542/peds.2016-3360.
2. Young LW, Hu D, Grossman M, Clark M, Sharma J, Hudak ML, et al. Eat, Sleep, 
   Console Approach or Usual Care for Neonatal Opioid Withdrawal. N Engl J Med. 
   2023;388(25):2326-2337. doi: 10.1056/NEJMoa2214470.
"""

from typing import Dict, Any


class EatSleepConsoleCalculator:
    """Calculator for Eat, Sleep, Console (ESC) Assessment"""
    
    def __init__(self):
        # ESC functional criteria
        self.FUNCTIONS = ['able_to_eat', 'able_to_sleep', 'able_to_console']
        
        # Assessment criteria definitions
        self.CRITERIA_DEFINITIONS = {
            'able_to_eat': 'Taking ≥1 oz per kg per feeding OR breastfeeding well for ≥10 minutes',
            'able_to_sleep': 'Sleeping ≥1 hour undisturbed after routine care',
            'able_to_console': 'Can be consoled within 10 minutes using standard comfort measures'
        }
    
    def calculate(self, able_to_eat: str, able_to_sleep: str, able_to_console: str) -> Dict[str, Any]:
        """
        Performs the Eat, Sleep, Console functional assessment
        
        Args:
            able_to_eat (str): Can infant eat adequately (yes/no)
            able_to_sleep (str): Can infant sleep ≥1 hour undisturbed (yes/no)
            able_to_console (str): Can infant be consoled within 10 minutes (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'able_to_eat': able_to_eat,
            'able_to_sleep': able_to_sleep,
            'able_to_console': able_to_console
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Assess functional status
        assessment_result = self._assess_esc_status(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(assessment_result, parameters)
        
        return {
            "result": assessment_result["status"],
            "unit": "status",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name in self.FUNCTIONS:
            value = parameters[param_name]
            
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{value}'")
    
    def _assess_esc_status(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Assesses ESC functional status"""
        
        # Count functions that are impaired
        impaired_functions = []
        
        for function in self.FUNCTIONS:
            if parameters[function].lower() == 'no':
                impaired_functions.append(function)
        
        # Determine overall status
        if len(impaired_functions) == 0:
            status = "ESC Criteria Met"
            all_functions_met = True
        else:
            status = "ESC Criteria Not Met"
            all_functions_met = False
        
        return {
            "status": status,
            "all_functions_met": all_functions_met,
            "impaired_functions": impaired_functions,
            "impaired_count": len(impaired_functions)
        }
    
    def _get_interpretation(self, assessment_result: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines the interpretation based on the ESC assessment
        
        Args:
            assessment_result (Dict): Results from ESC assessment
            parameters (Dict): Original input parameters
            
        Returns:
            Dict with interpretation
        """
        
        if assessment_result["all_functions_met"]:
            # All ESC criteria met
            interpretation = (
                "ESC criteria met - Infant is able to eat, sleep, and be consoled with "
                "nonpharmacologic interventions. Continue current nonpharmacologic care "
                "with family involvement. No pharmacologic intervention needed at this time. "
                "Monitor for changes in functional status. Support family in providing "
                "comfort measures including skin-to-skin contact, swaddling, breastfeeding, "
                "and maintaining a low-stimulation environment."
            )
            
            return {
                "stage": "ESC Criteria Met",
                "description": "All three functions achieved",
                "interpretation": interpretation
            }
        
        else:
            # One or more ESC criteria not met
            impaired_functions = assessment_result["impaired_functions"]
            impaired_list = []
            
            for function in impaired_functions:
                if function == 'able_to_eat':
                    impaired_list.append("eating")
                elif function == 'able_to_sleep':
                    impaired_list.append("sleeping")
                elif function == 'able_to_console':
                    impaired_list.append("consoling")
            
            impaired_text = ", ".join(impaired_list)
            
            interpretation = (
                f"ESC criteria not met - Infant is unable to achieve adequate {impaired_text} "
                "despite optimal nonpharmacologic interventions. Consider pharmacologic "
                "intervention with morphine (typical starting dose 0.05-0.1 mg/kg every "
                "3-4 hours). Reassess ESC criteria after each dose. Continue nonpharmacologic "
                "interventions alongside medication. Ensure family involvement in care and "
                "comfort measures. Re-evaluate environmental factors and feeding approach."
            )
            
            return {
                "stage": "ESC Criteria Not Met",
                "description": "One or more functions impaired",
                "interpretation": interpretation
            }


def calculate_eat_sleep_console(able_to_eat: str, able_to_sleep: str, able_to_console: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_eat_sleep_console pattern
    """
    calculator = EatSleepConsoleCalculator()
    return calculator.calculate(able_to_eat, able_to_sleep, able_to_console)