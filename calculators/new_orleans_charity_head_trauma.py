"""
New Orleans/Charity Head Trauma/Injury Rule Calculator

Offers criteria for which patients are unlikely to require imaging after head trauma.

Reference:
Haydel MJ, Preston CA, Mills TJ, Luber S, Blaudeau E, DeBlieux PM. Indications for 
computed tomography in patients with minor head injury. N Engl J Med. 2000 Jul 13;
343(2):100-5. doi: 10.1056/NEJM200007133430204.
"""

from typing import Dict, Any


class NewOrleansCharityHeadTraumaCalculator:
    """Calculator for New Orleans/Charity Head Trauma/Injury Rule"""
    
    def calculate(self, headache: str, vomiting: str, age_over_60: str,
                  intoxication: str, persistent_amnesia: str, 
                  visible_trauma: str, seizure: str) -> Dict[str, Any]:
        """
        Calculates the New Orleans/Charity Head Trauma Rule
        
        Args:
            headache (str): Headache (yes/no)
            vomiting (str): Vomiting (yes/no)
            age_over_60 (str): Age > 60 (yes/no)
            intoxication (str): Alcohol or drug intoxication (yes/no)
            persistent_amnesia (str): Persistent anterograde amnesia (yes/no)
            visible_trauma (str): Visible trauma above the clavicle (yes/no)
            seizure (str): Seizure (yes/no)
            
        Returns:
            Dict with the recommendation and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(headache, vomiting, age_over_60, intoxication,
                            persistent_amnesia, visible_trauma, seizure)
        
        # Count positive criteria
        criteria_count = 0
        criteria = [
            headache, vomiting, age_over_60, intoxication,
            persistent_amnesia, visible_trauma, seizure
        ]
        
        for criterion in criteria:
            if criterion == "yes":
                criteria_count += 1
        
        # Determine recommendation
        if criteria_count == 0:
            result = "CT not required"
            interpretation = {
                "stage": "Negative",
                "description": "No criteria met",
                "interpretation": (
                    "CT scan not required. The patient meets none of the New Orleans criteria. "
                    "The rule is 100% sensitive for detecting intracranial injuries requiring "
                    "neurosurgical intervention."
                )
            }
        else:
            result = "CT recommended"
            interpretation = {
                "stage": "Positive",
                "description": f"{criteria_count} criteria met",
                "interpretation": (
                    f"CT scan recommended. The patient meets {criteria_count} of the New Orleans criteria. "
                    "Consider CT head imaging to rule out intracranial injury. This rule has 100% "
                    "sensitivity for detecting intracranial injuries requiring neurosurgical intervention."
                )
            }
        
        return {
            "result": result,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "criteria_count": criteria_count
        }
    
    def _validate_inputs(self, headache: str, vomiting: str, age_over_60: str,
                        intoxication: str, persistent_amnesia: str,
                        visible_trauma: str, seizure: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        criteria = [
            ("Headache", headache),
            ("Vomiting", vomiting),
            ("Age over 60", age_over_60),
            ("Intoxication", intoxication),
            ("Persistent amnesia", persistent_amnesia),
            ("Visible trauma", visible_trauma),
            ("Seizure", seizure)
        ]
        
        for name, value in criteria:
            if value not in valid_options:
                raise ValueError(f"{name} must be 'yes' or 'no'")


def calculate_new_orleans_charity_head_trauma(headache: str, vomiting: str, age_over_60: str,
                                            intoxication: str, persistent_amnesia: str,
                                            visible_trauma: str, seizure: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NewOrleansCharityHeadTraumaCalculator()
    return calculator.calculate(headache, vomiting, age_over_60, intoxication,
                              persistent_amnesia, visible_trauma, seizure)