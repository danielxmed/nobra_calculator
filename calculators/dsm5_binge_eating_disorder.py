"""
DSM-5 Criteria for Binge Eating Disorder Calculator

Diagnostic criteria checker for binge eating disorder (BED) based on DSM-5.
Evaluates all required criteria and determines severity level.

References:
1. American Psychiatric Association. Diagnostic and statistical manual of mental 
   disorders: DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Grilo CM, Ivezaj V, White MA. Evaluation of the DSM-5 severity indicator for 
   binge eating disorder in a clinical sample. Behav Res Ther. 2015;71:110-4.
"""

from typing import Dict, Any


class Dsm5BingeEatingDisorderCalculator:
    """Calculator for DSM-5 Criteria for Binge Eating Disorder"""
    
    def __init__(self):
        # DSM-5 BED criteria structure
        self.CRITERION_B_FEATURES = [
            'eating_rapidly',
            'eating_until_uncomfortably_full', 
            'eating_when_not_hungry',
            'eating_alone_embarrassment',
            'negative_feelings_after'
        ]
        
        self.SEVERITY_LEVELS = {
            "1_3_per_week": {"level": "Mild", "code": 1},
            "4_7_per_week": {"level": "Moderate", "code": 2}, 
            "8_13_per_week": {"level": "Severe", "code": 3},
            "14_or_more_per_week": {"level": "Extreme", "code": 4}
        }
    
    def calculate(self, binge_eating_episodes: str, eating_rapidly: str,
                  eating_until_uncomfortably_full: str, eating_when_not_hungry: str,
                  eating_alone_embarrassment: str, negative_feelings_after: str,
                  marked_distress: str, frequency_duration: str,
                  no_compensatory_behaviors: str, not_during_other_disorders: str,
                  weekly_frequency: str) -> Dict[str, Any]:
        """
        Evaluates DSM-5 criteria for Binge Eating Disorder
        
        Args:
            binge_eating_episodes (str): Recurrent binge eating episodes (Criterion A)
            eating_rapidly (str): Eating more rapidly than normal (Criterion B1)
            eating_until_uncomfortably_full (str): Eating until uncomfortably full (Criterion B2)
            eating_when_not_hungry (str): Eating when not physically hungry (Criterion B3)
            eating_alone_embarrassment (str): Eating alone due to embarrassment (Criterion B4)
            negative_feelings_after (str): Negative feelings afterward (Criterion B5)
            marked_distress (str): Marked distress regarding binge eating (Criterion C)
            frequency_duration (str): At least once weekly for 3 months (Criterion D)
            no_compensatory_behaviors (str): No compensatory behaviors (Criterion E1)
            not_during_other_disorders (str): Not exclusively during other disorders (Criterion E2)
            weekly_frequency (str): Frequency category for severity assessment
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'binge_eating_episodes': binge_eating_episodes,
            'eating_rapidly': eating_rapidly,
            'eating_until_uncomfortably_full': eating_until_uncomfortably_full,
            'eating_when_not_hungry': eating_when_not_hungry,
            'eating_alone_embarrassment': eating_alone_embarrassment,
            'negative_feelings_after': negative_feelings_after,
            'marked_distress': marked_distress,
            'frequency_duration': frequency_duration,
            'no_compensatory_behaviors': no_compensatory_behaviors,
            'not_during_other_disorders': not_during_other_disorders,
            'weekly_frequency': weekly_frequency
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
        valid_frequency = ["1_3_per_week", "4_7_per_week", "8_13_per_week", "14_or_more_per_week"]
        
        for param_name, response in parameters.items():
            if not isinstance(response, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if param_name == 'weekly_frequency':
                if response not in valid_frequency:
                    raise ValueError(f"Parameter '{param_name}' must be one of {valid_frequency}")
            else:
                if response.lower() not in valid_yes_no:
                    raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{response}'")
    
    def _evaluate_criteria(self, parameters: Dict[str, str]) -> int:
        """Evaluates DSM-5 criteria for BED diagnosis"""
        
        # Criterion A: Recurrent binge eating episodes
        criterion_a = parameters['binge_eating_episodes'].lower() == 'yes'
        
        # Criterion B: At least 3 of 5 associated features
        criterion_b_count = sum(
            1 for feature in self.CRITERION_B_FEATURES
            if parameters[feature].lower() == 'yes'
        )
        criterion_b = criterion_b_count >= 3
        
        # Criterion C: Marked distress
        criterion_c = parameters['marked_distress'].lower() == 'yes'
        
        # Criterion D: Frequency and duration (≥1/week for 3 months)
        criterion_d = parameters['frequency_duration'].lower() == 'yes'
        
        # Criterion E: Exclusion criteria (both must be true)
        criterion_e1 = parameters['no_compensatory_behaviors'].lower() == 'yes'
        criterion_e2 = parameters['not_during_other_disorders'].lower() == 'yes'
        criterion_e = criterion_e1 and criterion_e2
        
        # All criteria must be met for diagnosis
        if criterion_a and criterion_b and criterion_c and criterion_d and criterion_e:
            # Return severity code based on frequency
            return self.SEVERITY_LEVELS[parameters['weekly_frequency']]['code']
        else:
            # Criteria not met
            return 0
    
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
                "interpretation": "The individual does not meet the diagnostic criteria for Binge Eating Disorder according to DSM-5. Consider other eating disorders or refer for comprehensive evaluation if clinical concerns persist."
            }
        elif result == 1:
            return {
                "stage": "Criteria Met - Mild",
                "description": "Meets DSM-5 criteria - Mild severity",
                "interpretation": "Meets DSM-5 criteria for Binge Eating Disorder, Mild severity (1-3 episodes per week). Treatment recommendations include psychotherapy, nutritional counseling, and consideration of medication if indicated."
            }
        elif result == 2:
            return {
                "stage": "Criteria Met - Moderate", 
                "description": "Meets DSM-5 criteria - Moderate severity",
                "interpretation": "Meets DSM-5 criteria for Binge Eating Disorder, Moderate severity (4-7 episodes per week). Intensive treatment recommended including specialized eating disorder therapy and comprehensive medical evaluation."
            }
        elif result == 3:
            return {
                "stage": "Criteria Met - Severe",
                "description": "Meets DSM-5 criteria - Severe severity",
                "interpretation": "Meets DSM-5 criteria for Binge Eating Disorder, Severe severity (8-13 episodes per week). Urgent referral to specialized eating disorder treatment program with intensive therapeutic intervention."
            }
        else:  # result == 4
            return {
                "stage": "Criteria Met - Extreme",
                "description": "Meets DSM-5 criteria - Extreme severity", 
                "interpretation": "Meets DSM-5 criteria for Binge Eating Disorder, Extreme severity (14+ episodes per week). Immediate specialized eating disorder treatment with potential consideration of higher levels of care including intensive outpatient or inpatient treatment."
            }


def calculate_dsm5_binge_eating_disorder(binge_eating_episodes: str, eating_rapidly: str,
                                        eating_until_uncomfortably_full: str, eating_when_not_hungry: str,
                                        eating_alone_embarrassment: str, negative_feelings_after: str,
                                        marked_distress: str, frequency_duration: str,
                                        no_compensatory_behaviors: str, not_during_other_disorders: str,
                                        weekly_frequency: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dsm5_binge_eating_disorder pattern
    """
    calculator = Dsm5BingeEatingDisorderCalculator()
    return calculator.calculate(
        binge_eating_episodes, eating_rapidly, eating_until_uncomfortably_full,
        eating_when_not_hungry, eating_alone_embarrassment, negative_feelings_after,
        marked_distress, frequency_duration, no_compensatory_behaviors,
        not_during_other_disorders, weekly_frequency
    )