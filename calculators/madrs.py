"""
Montgomery-Asberg Depression Rating Scale (MADRS) Calculator

Stratifies severity of depressive episodes in adults using 10 core mood symptoms,
particularly sensitive to treatment-induced changes in depression severity.

References:
1. Montgomery SA, Asberg M. Br J Psychiatry. 1979;134:382-9.
2. Snaith RP, et al. Br J Psychiatry. 1986;148:599-601.
3. Turkoz I, et al. J Affect Disord. 2021;281:267-273.
"""

from typing import Dict, Any


class MadrsCalculator:
    """Calculator for Montgomery-Asberg Depression Rating Scale (MADRS)"""
    
    def __init__(self):
        # MADRS item descriptions for validation
        self.MADRS_ITEMS = [
            "apparent_sadness",
            "reported_sadness", 
            "inner_tension",
            "reduced_sleep",
            "reduced_appetite",
            "concentration_difficulties",
            "lassitude",
            "inability_to_feel",
            "pessimistic_thoughts",
            "suicidal_thoughts"
        ]
    
    def calculate(self, apparent_sadness: int, reported_sadness: int, inner_tension: int,
                  reduced_sleep: int, reduced_appetite: int, concentration_difficulties: int,
                  lassitude: int, inability_to_feel: int, pessimistic_thoughts: int,
                  suicidal_thoughts: int) -> Dict[str, Any]:
        """
        Calculates the MADRS score for depression severity assessment
        
        Args:
            apparent_sadness (int): Apparent sadness (0-6 points)
            reported_sadness (int): Reported sadness (0-6 points)
            inner_tension (int): Inner tension (0-6 points)
            reduced_sleep (int): Reduced sleep (0-6 points)
            reduced_appetite (int): Reduced appetite (0-6 points)
            concentration_difficulties (int): Concentration difficulties (0-6 points)
            lassitude (int): Lassitude (0-6 points)
            inability_to_feel (int): Inability to feel (0-6 points)
            pessimistic_thoughts (int): Pessimistic thoughts (0-6 points)
            suicidal_thoughts (int): Suicidal thoughts (0-6 points)
            
        Returns:
            Dict with MADRS score and clinical interpretation
        """
        
        # Collect all scores for validation
        scores = [
            apparent_sadness, reported_sadness, inner_tension, reduced_sleep,
            reduced_appetite, concentration_difficulties, lassitude,
            inability_to_feel, pessimistic_thoughts, suicidal_thoughts
        ]
        
        # Validate inputs
        self._validate_inputs(scores)
        
        # Calculate total MADRS score
        total_score = sum(scores)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, scores: list):
        """Validates input parameters"""
        
        if len(scores) != 10:
            raise ValueError("MADRS requires exactly 10 item scores")
        
        for i, score in enumerate(scores):
            if not isinstance(score, int):
                raise ValueError(f"All MADRS item scores must be integers. Item {i+1} is not an integer.")
            
            if score < 0 or score > 6:
                raise ValueError(f"All MADRS item scores must be between 0 and 6. Item {i+1} score is {score}.")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on MADRS score
        
        Args:
            score (int): Total MADRS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 6:
            return {
                "stage": "Normal",
                "description": "No or minimal depression",
                "interpretation": (f"MADRS Score {score}: Normal mood or minimal depressive symptoms. "
                                f"This score indicates no clinically significant depression. The patient "
                                f"shows normal mood functioning or only minimal depressive symptoms that "
                                f"do not significantly impact daily functioning. This level is considered "
                                f"within the normal range and typically does not require specific depression "
                                f"treatment. Regular monitoring may be appropriate if there are risk factors "
                                f"or recent changes in mood. The MADRS is designed to be sensitive to "
                                f"treatment-induced changes, making it valuable for monitoring depression "
                                f"over time. A score in this range may also indicate successful treatment "
                                f"response if the patient was previously experiencing higher scores.")
            }
        elif score <= 19:
            return {
                "stage": "Mild Depression",
                "description": "Mild depressive symptoms",
                "interpretation": (f"MADRS Score {score}: Mild depression with some impact on daily functioning. "
                                f"The patient experiences mild depressive symptoms that may affect mood and "
                                f"activities but are generally manageable. Symptoms might include occasional "
                                f"sadness, mild sleep disturbances, slight appetite changes, or minor "
                                f"concentration difficulties. While functioning is maintained, the patient "
                                f"may benefit from psychosocial interventions, lifestyle modifications, or "
                                f"close monitoring. Consider psychotherapy, behavioral interventions, exercise, "
                                f"sleep hygiene, and stress management techniques. Pharmacological treatment "
                                f"may not be immediately necessary but should be considered if symptoms worsen "
                                f"or persist despite psychosocial interventions.")
            }
        elif score <= 34:
            return {
                "stage": "Moderate Depression",
                "description": "Moderate depressive symptoms",
                "interpretation": (f"MADRS Score {score}: Moderate depression with significant impact on "
                                f"functioning requiring treatment intervention. The patient experiences "
                                f"notable depressive symptoms that substantially interfere with daily "
                                f"activities, work performance, and relationships. Symptoms may include "
                                f"persistent sadness, sleep disturbances, appetite changes, concentration "
                                f"problems, fatigue, anhedonia, and negative thinking patterns. Active "
                                f"treatment is recommended, typically including psychotherapy and consideration "
                                f"of antidepressant medication. Regular monitoring is essential to assess "
                                f"treatment response. A clinically meaningful improvement would be a reduction "
                                f"of 6 or more points from baseline. Treatment response is defined as a 50% "
                                f"or greater reduction in MADRS score.")
            }
        else:  # score >= 35
            return {
                "stage": "Severe Depression",
                "description": "Severe depressive symptoms",
                "interpretation": (f"MADRS Score {score}: Severe depression with major impairment in functioning "
                                f"requiring intensive treatment and monitoring. The patient experiences severe "
                                f"depressive symptoms that significantly impair daily functioning, work capacity, "
                                f"and interpersonal relationships. Symptoms likely include persistent profound "
                                f"sadness, marked sleep disturbances, significant appetite changes, severe "
                                f"concentration difficulties, psychomotor changes, anhedonia, hopelessness, "
                                f"and possible suicidal ideation. Immediate and intensive treatment is required, "
                                f"including antidepressant medication and psychotherapy. Consider psychiatry "
                                f"referral for specialized care. Close monitoring for suicide risk is essential. "
                                f"Hospitalization may be necessary if there is significant suicide risk or "
                                f"severe functional impairment. Family and social support should be mobilized. "
                                f"Treatment response should be monitored closely with frequent MADRS reassessments.")
            }


def calculate_madrs(apparent_sadness: int, reported_sadness: int, inner_tension: int,
                   reduced_sleep: int, reduced_appetite: int, concentration_difficulties: int,
                   lassitude: int, inability_to_feel: int, pessimistic_thoughts: int,
                   suicidal_thoughts: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MadrsCalculator()
    return calculator.calculate(apparent_sadness, reported_sadness, inner_tension,
                               reduced_sleep, reduced_appetite, concentration_difficulties,
                               lassitude, inability_to_feel, pessimistic_thoughts,
                               suicidal_thoughts)