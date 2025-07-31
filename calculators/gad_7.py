"""
GAD-7 (General Anxiety Disorder-7) Calculator

Measures anxiety severity and screens for generalized anxiety disorder using a 
7-item questionnaire about symptoms over the past 2 weeks.

References:
1. Spitzer RL, Kroenke K, Williams JB, Löwe B. A brief measure for assessing generalized 
   anxiety disorder: the GAD-7. Arch Intern Med. 2006;166(10):1092-7. 
   doi: 10.1001/archinte.166.10.1092.
2. Löwe B, Decker O, Müller S, et al. Validation and standardization of the Generalized 
   Anxiety Disorder Screener (GAD-7) in the general population. Med Care. 2008;46(3):266-74. 
   doi: 10.1097/MLR.0b013e318160d093.
3. Plummer F, Manea L, Trepel D, McMillan D. Screening for anxiety disorders with the GAD-7 
   and GAD-2: a systematic review and diagnostic metaanalysis. Gen Hosp Psychiatry. 
   2016;39:24-31. doi: 10.1016/j.genhosppsych.2015.11.005.
"""

from typing import Dict, Any


class Gad7Calculator:
    """Calculator for GAD-7 (General Anxiety Disorder-7) Scale"""
    
    def __init__(self):
        # GAD-7 questionnaire items
        self.QUESTIONNAIRE_ITEMS = [
            "nervous_anxious_on_edge",
            "not_able_stop_control_worrying", 
            "worrying_too_much_different_things",
            "trouble_relaxing",
            "being_so_restless", 
            "becoming_easily_annoyed_irritable",
            "feeling_afraid_something_awful"
        ]
        
        # Response scale (same for all items)
        self.RESPONSE_SCALE = {
            0: "Not at all",
            1: "Several days", 
            2: "More than half the days",
            3: "Nearly every day"
        }
    
    def calculate(self, nervous_anxious_on_edge: int, not_able_stop_control_worrying: int,
                  worrying_too_much_different_things: int, trouble_relaxing: int,
                  being_so_restless: int, becoming_easily_annoyed_irritable: int,
                  feeling_afraid_something_awful: int) -> Dict[str, Any]:
        """
        Calculates GAD-7 total score and provides interpretation
        
        Args:
            nervous_anxious_on_edge (int): Score for feeling nervous, anxious, or on edge (0-3)
            not_able_stop_control_worrying (int): Score for not being able to stop or control worrying (0-3)
            worrying_too_much_different_things (int): Score for worrying too much about different things (0-3)
            trouble_relaxing (int): Score for trouble relaxing (0-3)
            being_so_restless (int): Score for being so restless that it's hard to sit still (0-3)
            becoming_easily_annoyed_irritable (int): Score for becoming easily annoyed or irritable (0-3)
            feeling_afraid_something_awful (int): Score for feeling afraid as if something awful might happen (0-3)
            
        Returns:
            Dict with total score and interpretation
        """
        
        # Create parameter dictionary for validation
        parameters = {
            "nervous_anxious_on_edge": nervous_anxious_on_edge,
            "not_able_stop_control_worrying": not_able_stop_control_worrying,
            "worrying_too_much_different_things": worrying_too_much_different_things,
            "trouble_relaxing": trouble_relaxing,
            "being_so_restless": being_so_restless,
            "becoming_easily_annoyed_irritable": becoming_easily_annoyed_irritable,
            "feeling_afraid_something_awful": feeling_afraid_something_awful
        }
        
        # Validations
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, int]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name} must be an integer")
            if value < 0 or value > 3:
                raise ValueError(f"{param_name} must be between 0 and 3")
    
    def _calculate_total_score(self, parameters: Dict[str, int]) -> int:
        """Calculates the total GAD-7 score by summing all item scores"""
        
        total_score = sum(parameters.values())
        return total_score
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on total GAD-7 score
        
        Args:
            total_score (int): Total GAD-7 score (0-21)
            
        Returns:
            Dict with interpretation
        """
        
        if total_score <= 4:
            return {
                "stage": "Minimal Anxiety",
                "description": "Minimal anxiety symptoms",
                "interpretation": (f"GAD-7 score of {total_score} indicates minimal anxiety symptoms. "
                                f"No intervention necessary at this time. Routine monitoring may be appropriate. "
                                f"Continue to assess for changes in anxiety levels during follow-up visits. "
                                f"Provide general wellness counseling including stress management, regular exercise, "
                                f"adequate sleep, and healthy lifestyle habits.")
            }
        elif total_score <= 9:
            return {
                "stage": "Mild Anxiety",
                "description": "Mild anxiety symptoms",
                "interpretation": (f"GAD-7 score of {total_score} indicates mild anxiety symptoms. "
                                f"Monitor symptoms and provide reassurance and support. Consider stress management "
                                f"techniques such as relaxation training, mindfulness exercises, or cognitive behavioral "
                                f"strategies. Evaluate for psychosocial stressors and provide appropriate counseling. "
                                f"Reassess in 2-4 weeks to monitor symptom progression.")
            }
        elif total_score <= 14:
            return {
                "stage": "Moderate Anxiety",
                "description": "Moderate anxiety symptoms",
                "interpretation": (f"GAD-7 score of {total_score} indicates moderate anxiety symptoms representing a "
                                f"possible clinically significant condition. Further assessment and/or referral to a "
                                f"mental health professional is recommended. Consider structured clinical interview to "
                                f"evaluate for specific anxiety disorders. Discuss treatment options including "
                                f"psychotherapy (CBT, exposure therapy) and/or pharmacotherapy. Monitor closely for "
                                f"symptom progression and functional impairment.")
            }
        else:  # Score 15-21
            return {
                "stage": "Severe Anxiety",
                "description": "Severe anxiety symptoms",
                "interpretation": (f"GAD-7 score of {total_score} indicates severe anxiety symptoms. Active treatment "
                                f"is probably warranted. Strongly recommend referral to a mental health professional "
                                f"for comprehensive evaluation and treatment planning. Consider immediate interventions "
                                f"including psychotherapy (cognitive behavioral therapy) and/or pharmacotherapy "
                                f"(SSRIs, SNRIs, or other anxiolytics as appropriate). Assess for comorbid conditions "
                                f"including depression, substance use, and suicide risk. Provide crisis resources if needed.")
            }


def calculate_gad_7(nervous_anxious_on_edge: int, not_able_stop_control_worrying: int,
                   worrying_too_much_different_things: int, trouble_relaxing: int,
                   being_so_restless: int, becoming_easily_annoyed_irritable: int,
                   feeling_afraid_something_awful: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gad_7 pattern
    """
    calculator = Gad7Calculator()
    return calculator.calculate(
        nervous_anxious_on_edge, not_able_stop_control_worrying,
        worrying_too_much_different_things, trouble_relaxing,
        being_so_restless, becoming_easily_annoyed_irritable,
        feeling_afraid_something_awful
    )