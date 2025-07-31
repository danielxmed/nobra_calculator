"""
DSM-5 Criteria for Posttraumatic Stress Disorder Calculator

Diagnostic criteria checker for PTSD based on DSM-5. Evaluates trauma exposure
and four symptom clusters: intrusion, avoidance, negative alterations in 
cognitions/mood, and alterations in arousal/reactivity.

References:
1. American Psychiatric Association. Diagnostic and statistical manual of mental 
   disorders: DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Weathers FW, Litz BT, Keane TM, Palmieri PA, Marx BP, Schnurr PP. The PTSD 
   Checklist for DSM-5 (PCL-5). National Center for PTSD; 2013.
"""

from typing import Dict, Any


class Dsm5PtsdCalculator:
    """Calculator for DSM-5 Criteria for Posttraumatic Stress Disorder"""
    
    def __init__(self):
        # DSM-5 PTSD symptom clusters
        self.CRITERION_B_INTRUSION = [
            'intrusive_memories',
            'traumatic_nightmares', 
            'dissociative_reactions',
            'psychological_distress',
            'physiological_reactions'
        ]
        
        self.CRITERION_C_AVOIDANCE = [
            'avoidance_thoughts',
            'avoidance_reminders'
        ]
        
        self.CRITERION_D_COGNITION_MOOD = [
            'inability_remember',
            'negative_beliefs',
            'distorted_blame',
            'negative_emotional_state',
            'diminished_interest',
            'detachment_estrangement',
            'inability_positive_emotions'
        ]
        
        self.CRITERION_E_AROUSAL_REACTIVITY = [
            'irritability_aggression',
            'reckless_behavior',
            'hypervigilance',
            'exaggerated_startle',
            'concentration_problems',
            'sleep_disturbance'
        ]
    
    def calculate(self, trauma_exposure: str, intrusive_memories: str, traumatic_nightmares: str, 
                  dissociative_reactions: str, psychological_distress: str, physiological_reactions: str,
                  avoidance_thoughts: str, avoidance_reminders: str, inability_remember: str,
                  negative_beliefs: str, distorted_blame: str, negative_emotional_state: str,
                  diminished_interest: str, detachment_estrangement: str, inability_positive_emotions: str,
                  irritability_aggression: str, reckless_behavior: str, hypervigilance: str,
                  exaggerated_startle: str, concentration_problems: str, sleep_disturbance: str,
                  duration_one_month: str, functional_impairment: str, not_substance_medical: str,
                  dissociative_symptoms: str) -> Dict[str, Any]:
        """
        Evaluates DSM-5 criteria for PTSD
        
        Args:
            All DSM-5 PTSD criteria parameters as strings ("yes"/"no")
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'trauma_exposure': trauma_exposure,
            'intrusive_memories': intrusive_memories,
            'traumatic_nightmares': traumatic_nightmares,
            'dissociative_reactions': dissociative_reactions,
            'psychological_distress': psychological_distress,
            'physiological_reactions': physiological_reactions,
            'avoidance_thoughts': avoidance_thoughts,
            'avoidance_reminders': avoidance_reminders,
            'inability_remember': inability_remember,
            'negative_beliefs': negative_beliefs,
            'distorted_blame': distorted_blame,
            'negative_emotional_state': negative_emotional_state,
            'diminished_interest': diminished_interest,
            'detachment_estrangement': detachment_estrangement,
            'inability_positive_emotions': inability_positive_emotions,
            'irritability_aggression': irritability_aggression,
            'reckless_behavior': reckless_behavior,
            'hypervigilance': hypervigilance,
            'exaggerated_startle': exaggerated_startle,
            'concentration_problems': concentration_problems,
            'sleep_disturbance': sleep_disturbance,
            'duration_one_month': duration_one_month,
            'functional_impairment': functional_impairment,
            'not_substance_medical': not_substance_medical,
            'dissociative_symptoms': dissociative_symptoms
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
        
        for param_name, response in parameters.items():
            if not isinstance(response, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if response.lower() not in valid_yes_no:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{response}'")
    
    def _evaluate_criteria(self, parameters: Dict[str, str]) -> int:
        """Evaluates DSM-5 criteria for PTSD diagnosis"""
        
        # Criterion A: Trauma exposure (mandatory)
        if parameters['trauma_exposure'].lower() != 'yes':
            return 0  # No trauma exposure = no PTSD diagnosis possible
        
        # Criterion B: At least 1 intrusion symptom required
        criterion_b_count = sum(
            1 for symptom in self.CRITERION_B_INTRUSION 
            if parameters[symptom].lower() == 'yes'
        )
        if criterion_b_count < 1:
            return 0  # Insufficient Criterion B symptoms
        
        # Criterion C: At least 1 avoidance symptom required  
        criterion_c_count = sum(
            1 for symptom in self.CRITERION_C_AVOIDANCE
            if parameters[symptom].lower() == 'yes'
        )
        if criterion_c_count < 1:
            return 0  # Insufficient Criterion C symptoms
        
        # Criterion D: At least 2 negative cognition/mood symptoms required
        criterion_d_count = sum(
            1 for symptom in self.CRITERION_D_COGNITION_MOOD
            if parameters[symptom].lower() == 'yes'
        )
        if criterion_d_count < 2:
            return 0  # Insufficient Criterion D symptoms
        
        # Criterion E: At least 2 arousal/reactivity symptoms required
        criterion_e_count = sum(
            1 for symptom in self.CRITERION_E_AROUSAL_REACTIVITY
            if parameters[symptom].lower() == 'yes'
        )
        if criterion_e_count < 2:
            return 0  # Insufficient Criterion E symptoms
        
        # Criterion F: Duration > 1 month
        if parameters['duration_one_month'].lower() != 'yes':
            return 0  # Duration criterion not met
        
        # Criterion G: Functional impairment
        if parameters['functional_impairment'].lower() != 'yes':
            return 0  # Functional impairment criterion not met
        
        # Criterion H: Not due to substance/medical condition
        if parameters['not_substance_medical'].lower() != 'yes':
            return 0  # Exclusion criterion not met
        
        # All basic PTSD criteria met
        base_diagnosis = 1
        
        # Check for dissociative subtype
        if parameters['dissociative_symptoms'].lower() == 'yes':
            return 2  # PTSD with dissociative subtype
        
        return base_diagnosis  # PTSD without dissociative subtype
    
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
                "description": "Does not meet DSM-5 PTSD criteria",
                "interpretation": "Does not meet DSM-5 criteria for PTSD. Consider other trauma-related disorders, acute stress disorder, or subclinical PTSD symptoms. Refer for comprehensive trauma evaluation if clinical concerns persist."
            }
        elif result == 1:
            return {
                "stage": "PTSD",
                "description": "Meets criteria for PTSD",
                "interpretation": "Meets DSM-5 criteria for Posttraumatic Stress Disorder. Requires comprehensive trauma-informed psychiatric evaluation and treatment planning. Consider evidence-based treatments such as trauma-focused psychotherapy (CPT, PE, EMDR) and/or pharmacotherapy."
            }
        else:  # result == 2
            return {
                "stage": "PTSD with Dissociative Subtype",
                "description": "Meets criteria for PTSD with dissociative features",
                "interpretation": "Meets DSM-5 criteria for PTSD with Dissociative Subtype. This more severe form includes depersonalization or derealization symptoms. Requires specialized trauma treatment with attention to dissociative symptoms and safety planning."
            }


def calculate_dsm5_ptsd(trauma_exposure: str, intrusive_memories: str, traumatic_nightmares: str, 
                       dissociative_reactions: str, psychological_distress: str, physiological_reactions: str,
                       avoidance_thoughts: str, avoidance_reminders: str, inability_remember: str,
                       negative_beliefs: str, distorted_blame: str, negative_emotional_state: str,
                       diminished_interest: str, detachment_estrangement: str, inability_positive_emotions: str,
                       irritability_aggression: str, reckless_behavior: str, hypervigilance: str,
                       exaggerated_startle: str, concentration_problems: str, sleep_disturbance: str,
                       duration_one_month: str, functional_impairment: str, not_substance_medical: str,
                       dissociative_symptoms: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dsm5_ptsd pattern
    """
    calculator = Dsm5PtsdCalculator()
    return calculator.calculate(
        trauma_exposure, intrusive_memories, traumatic_nightmares, dissociative_reactions,
        psychological_distress, physiological_reactions, avoidance_thoughts, avoidance_reminders,
        inability_remember, negative_beliefs, distorted_blame, negative_emotional_state,
        diminished_interest, detachment_estrangement, inability_positive_emotions,
        irritability_aggression, reckless_behavior, hypervigilance, exaggerated_startle,
        concentration_problems, sleep_disturbance, duration_one_month, functional_impairment,
        not_substance_medical, dissociative_symptoms
    )