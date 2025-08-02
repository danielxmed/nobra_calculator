"""
Ottawa Subarachnoid Hemorrhage (SAH) Rule for Headache Evaluation Calculator

Clinical decision rule to identify alert patients with acute headache who are 
at risk for subarachnoid hemorrhage. This tool has 100% sensitivity for ruling 
out SAH but low specificity, making it an excellent rule-out tool.

References:
1. Perry JJ, Stiell IG, Sivilotti ML, Bullard MJ, Emond M, Symington C, et al. 
   Sensitivity of computed tomography performed within six hours of onset of 
   headache for diagnosis of subarachnoid haemorrhage: prospective cohort study. 
   BMJ. 2011;343:d4277. doi: 10.1136/bmj.d4277.
2. Perry JJ, Stiell IG, Sivilotti ML, Bullard MJ, Lee JS, Eisenhauer M, et al. 
   High risk clinical characteristics for subarachnoid haemorrhage in patients 
   with acute headache: prospective cohort study. BMJ. 2010;341:c5204. 
   doi: 10.1136/bmj.c5204.
3. Perry JJ, Sivilotti ML, Sutherland J, Hohl CM, Émond M, Calder LA, et al. 
   Validation of the Ottawa Subarachnoid Hemorrhage Rule in patients with acute 
   headache. CMAJ. 2017;189(45):E1379-E1385. doi: 10.1503/cmaj.170072.
"""

from typing import Dict, Any


class OttawaSahRuleCalculator:
    """Calculator for Ottawa Subarachnoid Hemorrhage (SAH) Rule"""
    
    def __init__(self):
        # Ottawa SAH Rule criteria - any positive criterion indicates cannot rule out SAH
        self.CRITERIA = [
            "age_40_or_older",
            "neck_pain_stiffness", 
            "witnessed_loss_of_consciousness",
            "onset_during_exertion",
            "thunderclap_headache",
            "limited_neck_flexion"
        ]
    
    def calculate(self, age_40_or_older: str, neck_pain_stiffness: str,
                 witnessed_loss_of_consciousness: str, onset_during_exertion: str,
                 thunderclap_headache: str, limited_neck_flexion: str) -> Dict[str, Any]:
        """
        Calculates the Ottawa SAH Rule result
        
        Args:
            age_40_or_older (str): Patient age 40 years or older
            neck_pain_stiffness (str): Neck pain or stiffness
            witnessed_loss_of_consciousness (str): Witnessed loss of consciousness
            onset_during_exertion (str): Onset during exertion
            thunderclap_headache (str): Thunderclap headache
            limited_neck_flexion (str): Limited neck flexion on examination
            
        Returns:
            Dict with the rule result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_40_or_older, neck_pain_stiffness, witnessed_loss_of_consciousness,
                            onset_during_exertion, thunderclap_headache, limited_neck_flexion)
        
        # Count positive criteria
        criteria_values = [
            age_40_or_older, neck_pain_stiffness, witnessed_loss_of_consciousness,
            onset_during_exertion, thunderclap_headache, limited_neck_flexion
        ]
        
        positive_criteria = sum(1 for value in criteria_values if value == "yes")
        
        # Determine specific positive criteria for detailed interpretation
        positive_criteria_list = []
        if age_40_or_older == "yes":
            positive_criteria_list.append("Age ≥40 years")
        if neck_pain_stiffness == "yes":
            positive_criteria_list.append("Neck pain or stiffness")
        if witnessed_loss_of_consciousness == "yes":
            positive_criteria_list.append("Witnessed loss of consciousness")
        if onset_during_exertion == "yes":
            positive_criteria_list.append("Onset during exertion")
        if thunderclap_headache == "yes":
            positive_criteria_list.append("Thunderclap headache")
        if limited_neck_flexion == "yes":
            positive_criteria_list.append("Limited neck flexion")
        
        # Get interpretation
        interpretation = self._get_interpretation(positive_criteria, positive_criteria_list)
        
        return {
            "result": interpretation["result"],
            "unit": "result",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_40_or_older: str, neck_pain_stiffness: str,
                        witnessed_loss_of_consciousness: str, onset_during_exertion: str,
                        thunderclap_headache: str, limited_neck_flexion: str):
        """Validates input parameters"""
        
        valid_values = ["yes", "no"]
        
        parameters = [
            ("age_40_or_older", age_40_or_older),
            ("neck_pain_stiffness", neck_pain_stiffness),
            ("witnessed_loss_of_consciousness", witnessed_loss_of_consciousness),
            ("onset_during_exertion", onset_during_exertion),
            ("thunderclap_headache", thunderclap_headache),
            ("limited_neck_flexion", limited_neck_flexion)
        ]
        
        for param_name, param_value in parameters:
            if param_value not in valid_values:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _get_interpretation(self, positive_criteria: int, positive_criteria_list: list) -> Dict[str, str]:
        """
        Determines the interpretation based on positive criteria count
        
        Args:
            positive_criteria (int): Number of positive criteria
            positive_criteria_list (list): List of specific positive criteria
            
        Returns:
            Dict with interpretation details
        """
        
        if positive_criteria == 0:
            return {
                "result": "SAH Ruled Out",
                "stage": "SAH Ruled Out",
                "description": "Subarachnoid hemorrhage ruled out",
                "interpretation": "SUBARACHNOID HEMORRHAGE RULED OUT: All Ottawa SAH Rule criteria are negative. "
                                "SAH can be ruled out with 100% sensitivity. MANAGEMENT: No further testing required "
                                "specifically for subarachnoid hemorrhage. Consider alternative diagnoses for the "
                                "headache. SAFETY: This rule has been validated in multiple studies with 100% "
                                "sensitivity for SAH. FOLLOW-UP: Routine headache management and reassurance. "
                                "Return precautions for new neurological symptoms or worsening headache pattern."
            }
        else:
            positive_criteria_text = ", ".join(positive_criteria_list)
            return {
                "result": "Cannot Rule Out SAH",
                "stage": "Cannot Rule Out SAH", 
                "description": "Cannot rule out subarachnoid hemorrhage",
                "interpretation": f"CANNOT RULE OUT SUBARACHNOID HEMORRHAGE: {positive_criteria} positive "
                                f"criterion/criteria detected: {positive_criteria_text}. IMMEDIATE ACTION: "
                                f"Further investigation required to exclude SAH. RECOMMENDED WORKUP: Non-contrast "
                                f"head CT scan within 6 hours of headache onset (99% sensitive within 6 hours, "
                                f"95% sensitive within 24 hours). If CT negative and high clinical suspicion, "
                                f"consider lumbar puncture for xanthochromia and red blood cell count. "
                                f"CONSULTATION: Neurology or neurosurgical consultation if SAH suspected. "
                                f"MONITORING: Close observation, blood pressure control, analgesia as appropriate. "
                                f"SAFETY: The Ottawa SAH Rule has 15.3% specificity, so positive results require "
                                f"careful evaluation but do not confirm SAH diagnosis."
            }


def calculate_ottawa_sah_rule(age_40_or_older: str, neck_pain_stiffness: str,
                             witnessed_loss_of_consciousness: str, onset_during_exertion: str,
                             thunderclap_headache: str, limited_neck_flexion: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OttawaSahRuleCalculator()
    return calculator.calculate(age_40_or_older, neck_pain_stiffness, witnessed_loss_of_consciousness,
                               onset_during_exertion, thunderclap_headache, limited_neck_flexion)