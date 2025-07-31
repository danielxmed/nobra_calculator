"""
DSM-5 Criteria for Major Depressive Disorder Calculator

Diagnostic criteria checker for major depressive disorder (MDD) based on DSM-5.
Evaluates all required criteria for major depressive episodes.

References:
1. American Psychiatric Association. Diagnostic and statistical manual of mental 
   disorders: DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Uher R, Payne JL, Pavlova B, Perlis RH. Major depressive disorder in DSM-5: 
   implications for clinical practice and research of changes from DSM-IV. 
   Depress Anxiety. 2014;31(6):459-71.
"""

from typing import Dict, Any


class Dsm5MajorDepressiveDisorderCalculator:
    """Calculator for DSM-5 Criteria for Major Depressive Disorder"""
    
    def __init__(self):
        # DSM-5 MDD criteria structure
        self.CORE_SYMPTOMS = [
            'depressed_mood',
            'anhedonia'
        ]
        
        self.ALL_SYMPTOMS = [
            'depressed_mood',
            'anhedonia', 
            'weight_appetite_change',
            'sleep_disturbance',
            'psychomotor_changes',
            'fatigue_energy_loss',
            'worthlessness_guilt',
            'concentration_problems',
            'suicidal_thoughts'
        ]
    
    def calculate(self, depressed_mood: str, anhedonia: str, weight_appetite_change: str,
                  sleep_disturbance: str, psychomotor_changes: str, fatigue_energy_loss: str,
                  worthlessness_guilt: str, concentration_problems: str, suicidal_thoughts: str,
                  duration_two_weeks: str, functional_impairment: str, not_substance_medical: str,
                  not_better_explained: str, no_manic_hypomanic_history: str) -> Dict[str, Any]:
        """
        Evaluates DSM-5 criteria for Major Depressive Disorder
        
        Args:
            depressed_mood (str): Depressed mood most of the day, nearly every day
            anhedonia (str): Loss of interest or pleasure in activities
            weight_appetite_change (str): Significant weight/appetite changes
            sleep_disturbance (str): Insomnia or hypersomnia nearly every day
            psychomotor_changes (str): Psychomotor agitation or retardation
            fatigue_energy_loss (str): Fatigue or loss of energy nearly every day
            worthlessness_guilt (str): Feelings of worthlessness or excessive guilt
            concentration_problems (str): Diminished ability to think or concentrate
            suicidal_thoughts (str): Recurrent thoughts of death or suicidal ideation
            duration_two_weeks (str): Symptoms present for at least 2 weeks
            functional_impairment (str): Clinically significant distress/impairment
            not_substance_medical (str): Not due to substance use or medical condition
            not_better_explained (str): Not better explained by other psychiatric disorders
            no_manic_hypomanic_history (str): Never had manic or hypomanic episodes
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'depressed_mood': depressed_mood,
            'anhedonia': anhedonia,
            'weight_appetite_change': weight_appetite_change,
            'sleep_disturbance': sleep_disturbance,
            'psychomotor_changes': psychomotor_changes,
            'fatigue_energy_loss': fatigue_energy_loss,
            'worthlessness_guilt': worthlessness_guilt,
            'concentration_problems': concentration_problems,
            'suicidal_thoughts': suicidal_thoughts,
            'duration_two_weeks': duration_two_weeks,
            'functional_impairment': functional_impairment,
            'not_substance_medical': not_substance_medical,
            'not_better_explained': not_better_explained,
            'no_manic_hypomanic_history': no_manic_hypomanic_history
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
        """Evaluates DSM-5 criteria for MDD diagnosis"""
        
        # Criterion A: At least 5 symptoms, with at least one core symptom
        
        # Count all symptoms present
        symptom_count = sum(
            1 for symptom in self.ALL_SYMPTOMS
            if parameters[symptom].lower() == 'yes'
        )
        
        # Check if at least one core symptom is present
        core_symptom_present = any(
            parameters[core_symptom].lower() == 'yes'
            for core_symptom in self.CORE_SYMPTOMS
        )
        
        # Must have at least 5 symptoms AND at least one core symptom
        if symptom_count < 5 or not core_symptom_present:
            return 0  # Criteria not met
        
        # Criterion B: Duration (at least 2 weeks)
        duration_met = parameters['duration_two_weeks'].lower() == 'yes'
        if not duration_met:
            return 0  # Criteria not met
        
        # Criterion C: Functional impairment
        impairment_present = parameters['functional_impairment'].lower() == 'yes'
        if not impairment_present:
            return 0  # Criteria not met
        
        # Criterion D: Not due to substance or medical condition
        not_substance_medical = parameters['not_substance_medical'].lower() == 'yes'
        if not not_substance_medical:
            return 0  # Criteria not met
        
        # Criterion E: Not better explained by other psychiatric disorders
        not_better_explained = parameters['not_better_explained'].lower() == 'yes'
        if not not_better_explained:
            return 0  # Criteria not met
        
        # Exclusion: No history of manic/hypomanic episodes (to distinguish from bipolar)
        no_manic_history = parameters['no_manic_hypomanic_history'].lower() == 'yes'
        if not no_manic_history:
            return 0  # Criteria not met (suggests bipolar disorder)
        
        # All criteria met
        return 1
    
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
                "interpretation": "Does not meet DSM-5 criteria for Major Depressive Disorder. Consider other mood disorders, adjustment disorders, or subclinical depression. Refer for comprehensive evaluation if clinical concerns persist."
            }
        else:  # result == 1
            return {
                "stage": "Major Depressive Episode",
                "description": "Meets criteria for major depressive episode",
                "interpretation": "Meets DSM-5 criteria for Major Depressive Disorder. Requires comprehensive psychiatric evaluation and treatment planning. Consider psychotherapy, medication, or combination treatment based on severity and patient preferences."
            }


def calculate_dsm5_major_depressive_disorder(depressed_mood: str, anhedonia: str, weight_appetite_change: str,
                                           sleep_disturbance: str, psychomotor_changes: str, fatigue_energy_loss: str,
                                           worthlessness_guilt: str, concentration_problems: str, suicidal_thoughts: str,
                                           duration_two_weeks: str, functional_impairment: str, not_substance_medical: str,
                                           not_better_explained: str, no_manic_hypomanic_history: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dsm5_major_depressive_disorder pattern
    """
    calculator = Dsm5MajorDepressiveDisorderCalculator()
    return calculator.calculate(
        depressed_mood, anhedonia, weight_appetite_change, sleep_disturbance,
        psychomotor_changes, fatigue_energy_loss, worthlessness_guilt,
        concentration_problems, suicidal_thoughts, duration_two_weeks,
        functional_impairment, not_substance_medical, not_better_explained,
        no_manic_hypomanic_history
    )