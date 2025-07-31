"""
DSM-5 Criteria for Bipolar Disorder Calculator

Diagnostic criteria checker for bipolar disorder based on DSM-5.
Evaluates manic and hypomanic episodes to determine bipolar disorder subtypes.

References:
1. American Psychiatric Association. Diagnostic and statistical manual of mental 
   disorders: DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Youngstrom EA, Birmaher B, Findling RL. Pediatric bipolar disorder: validity, 
   phenomenology, and recommendations for diagnosis. Bipolar Disord. 2008;10(1 Pt 2):194-214.
"""

from typing import Dict, Any


class Dsm5BipolarDisorderCalculator:
    """Calculator for DSM-5 Criteria for Bipolar Disorder"""
    
    def __init__(self):
        # DSM-5 bipolar disorder criteria structure
        self.MANIC_HYPOMANIC_SYMPTOMS = [
            'inflated_self_esteem',
            'decreased_need_sleep',
            'more_talkative',
            'flight_of_ideas',
            'distractibility',
            'increased_goal_directed_activity',
            'excessive_risky_behavior'
        ]
    
    def calculate(self, elevated_expansive_irritable_mood: str, increased_activity_energy: str,
                  inflated_self_esteem: str, decreased_need_sleep: str, more_talkative: str,
                  flight_of_ideas: str, distractibility: str, increased_goal_directed_activity: str,
                  excessive_risky_behavior: str, episode_duration: str, functional_impairment: str,
                  substance_medical_cause: str, history_major_depressive_episode: str) -> Dict[str, Any]:
        """
        Evaluates DSM-5 criteria for Bipolar Disorder
        
        Args:
            elevated_expansive_irritable_mood (str): Elevated, expansive, or irritable mood
            increased_activity_energy (str): Increased goal-directed activity or energy
            inflated_self_esteem (str): Inflated self-esteem or grandiosity
            decreased_need_sleep (str): Decreased need for sleep
            more_talkative (str): More talkative than usual or pressure to keep talking
            flight_of_ideas (str): Flight of ideas or racing thoughts
            distractibility (str): Distractibility
            increased_goal_directed_activity (str): Increase in goal-directed activity
            excessive_risky_behavior (str): Excessive risky activities
            episode_duration (str): Duration of mood episode
            functional_impairment (str): Level of functional impairment
            substance_medical_cause (str): Not due to substance/medical condition
            history_major_depressive_episode (str): History of major depressive episode
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'elevated_expansive_irritable_mood': elevated_expansive_irritable_mood,
            'increased_activity_energy': increased_activity_energy,
            'inflated_self_esteem': inflated_self_esteem,
            'decreased_need_sleep': decreased_need_sleep,
            'more_talkative': more_talkative,
            'flight_of_ideas': flight_of_ideas,
            'distractibility': distractibility,
            'increased_goal_directed_activity': increased_goal_directed_activity,
            'excessive_risky_behavior': excessive_risky_behavior,
            'episode_duration': episode_duration,
            'functional_impairment': functional_impairment,
            'substance_medical_cause': substance_medical_cause,
            'history_major_depressive_episode': history_major_depressive_episode
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Evaluate criteria
        result = self._evaluate_criteria(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": interpretation["stage"],
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_duration = ["less_than_4_days", "4_to_6_days", "7_days_or_more", "hospitalization_required"]
        valid_impairment = ["none", "mild_noticeable", "marked_impairment", "psychotic_hospitalization"]
        
        for param_name, response in parameters.items():
            if not isinstance(response, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if param_name == 'episode_duration':
                if response not in valid_duration:
                    raise ValueError(f"Parameter '{param_name}' must be one of {valid_duration}")
            elif param_name == 'functional_impairment':
                if response not in valid_impairment:
                    raise ValueError(f"Parameter '{param_name}' must be one of {valid_impairment}")
            else:
                if response.lower() not in valid_yes_no:
                    raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{response}'")
    
    def _evaluate_criteria(self, parameters: Dict[str, str]) -> int:
        """Evaluates DSM-5 criteria for bipolar disorder diagnosis"""
        
        # Core criteria A: Elevated mood OR irritable mood
        mood_criterion = parameters['elevated_expansive_irritable_mood'].lower() == 'yes'
        
        # Core criteria B: Increased activity/energy (DSM-5 addition)
        activity_criterion = parameters['increased_activity_energy'].lower() == 'yes'
        
        # Core criteria must both be present
        if not (mood_criterion and activity_criterion):
            return 0  # Criteria not met
        
        # Count manic/hypomanic symptoms (Criterion C)
        symptom_count = sum(
            1 for symptom in self.MANIC_HYPOMANIC_SYMPTOMS
            if parameters[symptom].lower() == 'yes'
        )
        
        # Need at least 3 symptoms (or 4 if mood is only irritable - simplified here)
        if symptom_count < 3:
            return 0  # Criteria not met
        
        # Duration and impairment criteria
        duration = parameters['episode_duration']
        impairment = parameters['functional_impairment']
        
        # Exclusion criteria
        not_substance_medical = parameters['substance_medical_cause'].lower() == 'yes'
        if not not_substance_medical:
            return 0  # Criteria not met due to substance/medical cause
        
        # History of depression
        depression_history = parameters['history_major_depressive_episode'].lower() == 'yes'
        
        # Determine episode type based on duration and impairment
        if (duration == "hospitalization_required" or 
            impairment == "psychotic_hospitalization" or
            duration == "7_days_or_more" or
            impairment == "marked_impairment"):
            # Manic episode - Bipolar I
            return 2
        elif (duration == "4_to_6_days" and 
              impairment in ["mild_noticeable", "none"]):
            # Hypomanic episode
            if depression_history:
                return 3  # Bipolar II (hypomanic + depression)
            else:
                return 1  # Hypomanic episode only
        else:
            return 0  # Insufficient duration/impairment
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the evaluation result
        
        Args:
            result (int): Diagnostic result code
            
        Returns:
            Dict with interpretation details
        """
        
        if result == 0:
            return {
                "stage": "Criteria Not Met",
                "description": "Does not meet DSM-5 criteria",
                "interpretation": "Does not meet DSM-5 criteria for Bipolar Disorder. Consider other mood disorders, substance-induced conditions, or refer for comprehensive psychiatric evaluation if clinical concerns persist."
            }
        elif result == 1:
            return {
                "stage": "Hypomanic Episode",
                "description": "Meets criteria for hypomanic episode",
                "interpretation": "Meets criteria for a hypomanic episode. If history of major depressive episode exists, consider Bipolar II Disorder. Requires comprehensive evaluation for full bipolar disorder assessment."
            }
        elif result == 2:
            return {
                "stage": "Manic Episode",
                "description": "Meets criteria for manic episode",
                "interpretation": "Meets criteria for a manic episode, indicating Bipolar I Disorder. Requires immediate psychiatric evaluation and treatment. Consider hospitalization if psychotic features or significant functional impairment present."
            }
        else:  # result == 3
            return {
                "stage": "Bipolar II Disorder",
                "description": "Meets criteria for Bipolar II",
                "interpretation": "Meets criteria for Bipolar II Disorder (hypomanic episode + major depressive episode history). Requires specialized psychiatric treatment including mood stabilizers and psychotherapy."
            }


def calculate_dsm5_bipolar_disorder(elevated_expansive_irritable_mood: str, increased_activity_energy: str,
                                   inflated_self_esteem: str, decreased_need_sleep: str, more_talkative: str,
                                   flight_of_ideas: str, distractibility: str, increased_goal_directed_activity: str,
                                   excessive_risky_behavior: str, episode_duration: str, functional_impairment: str,
                                   substance_medical_cause: str, history_major_depressive_episode: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dsm5_bipolar_disorder pattern
    """
    calculator = Dsm5BipolarDisorderCalculator()
    return calculator.calculate(
        elevated_expansive_irritable_mood, increased_activity_energy, inflated_self_esteem,
        decreased_need_sleep, more_talkative, flight_of_ideas, distractibility,
        increased_goal_directed_activity, excessive_risky_behavior, episode_duration,
        functional_impairment, substance_medical_cause, history_major_depressive_episode
    )