"""
Hamilton Depression Rating Scale Calculator

Assesses severity of depression symptoms based on 17-item questionnaire.

References:
- Hamilton M. J Neurol Neurosurg Psychiatry. 1960;23(1):56-62.
- Zimmerman M, et al. J Affect Disord. 2013;150(2):384-8.
"""

from typing import Dict, Any


class HamiltonDepressionRatingScaleCalculator:
    """Calculator for Hamilton Depression Rating Scale (HAM-D)"""
    
    def __init__(self):
        # Scoring constants
        self.ITEMS_0_TO_4 = [
            "depressed_mood", "feelings_of_guilt", "suicide",
            "work_and_activities", "retardation", "anxiety_psychological",
            "anxiety_somatic", "hypochondriasis"
        ]
        self.ITEMS_0_TO_2 = [
            "insomnia_early", "insomnia_middle", "insomnia_late",
            "agitation", "somatic_symptoms_gastrointestinal",
            "somatic_symptoms_general", "genital_symptoms",
            "loss_of_weight", "insight"
        ]
    
    def calculate(self, depressed_mood: int, feelings_of_guilt: int, suicide: int,
                  insomnia_early: int, insomnia_middle: int, insomnia_late: int,
                  work_and_activities: int, retardation: int, agitation: int,
                  anxiety_psychological: int, anxiety_somatic: int,
                  somatic_symptoms_gastrointestinal: int, somatic_symptoms_general: int,
                  genital_symptoms: int, hypochondriasis: int, loss_of_weight: int,
                  insight: int) -> Dict[str, Any]:
        """
        Calculates the HAM-D score
        
        Args:
            depressed_mood: Sadness, hopelessness (0-4)
            feelings_of_guilt: Self-reproach, guilt (0-4)
            suicide: Suicidal ideation (0-4)
            insomnia_early: Difficulty falling asleep (0-2)
            insomnia_middle: Waking during night (0-2)
            insomnia_late: Early morning awakening (0-2)
            work_and_activities: Loss of interest (0-4)
            retardation: Psychomotor retardation (0-4)
            agitation: Psychomotor agitation (0-2)
            anxiety_psychological: Psychological anxiety (0-4)
            anxiety_somatic: Somatic anxiety (0-4)
            somatic_symptoms_gastrointestinal: GI symptoms (0-2)
            somatic_symptoms_general: General somatic symptoms (0-2)
            genital_symptoms: Sexual symptoms (0-2)
            hypochondriasis: Health preoccupation (0-4)
            loss_of_weight: Weight loss (0-2)
            insight: Awareness of illness (0-2)
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Collect all parameters
        scores = {
            "depressed_mood": depressed_mood,
            "feelings_of_guilt": feelings_of_guilt,
            "suicide": suicide,
            "insomnia_early": insomnia_early,
            "insomnia_middle": insomnia_middle,
            "insomnia_late": insomnia_late,
            "work_and_activities": work_and_activities,
            "retardation": retardation,
            "agitation": agitation,
            "anxiety_psychological": anxiety_psychological,
            "anxiety_somatic": anxiety_somatic,
            "somatic_symptoms_gastrointestinal": somatic_symptoms_gastrointestinal,
            "somatic_symptoms_general": somatic_symptoms_general,
            "genital_symptoms": genital_symptoms,
            "hypochondriasis": hypochondriasis,
            "loss_of_weight": loss_of_weight,
            "insight": insight
        }
        
        # Validate inputs
        self._validate_inputs(scores)
        
        # Calculate total score
        result = self._calculate_total_score(scores)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, scores: Dict[str, int]):
        """Validates input parameters"""
        
        for item_name, score in scores.items():
            if not isinstance(score, int):
                raise ValueError(f"{item_name} must be an integer")
            
            # Check range based on item type
            if item_name in self.ITEMS_0_TO_4:
                if score < 0 or score > 4:
                    raise ValueError(f"{item_name} must be between 0 and 4")
            elif item_name in self.ITEMS_0_TO_2:
                if score < 0 or score > 2:
                    raise ValueError(f"{item_name} must be between 0 and 2")
    
    def _calculate_total_score(self, scores: Dict[str, int]) -> int:
        """Calculates the total HAM-D score"""
        
        # Sum all item scores
        total_score = sum(scores.values())
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): HAM-D score (0-50)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 7:
            return {
                "stage": "No Depression",
                "description": "Normal range",
                "interpretation": "Patient shows no significant depressive symptoms. No specific intervention typically required."
            }
        elif score <= 16:
            return {
                "stage": "Mild Depression",
                "description": "Mild depressive symptoms",
                "interpretation": "Patient experiences mild depressive symptoms that may cause some distress. Consider monitoring and supportive interventions."
            }
        elif score <= 23:
            return {
                "stage": "Moderate Depression",
                "description": "Moderate depressive symptoms",
                "interpretation": "Patient experiences moderate depressive symptoms that interfere with daily functioning. Consider psychotherapy and/or antidepressant medication."
            }
        else:
            return {
                "stage": "Severe Depression",
                "description": "Severe depressive symptoms",
                "interpretation": "Patient experiences severe depressive symptoms that significantly impair functioning. Strongly consider intensive treatment including medication and psychotherapy. Assess suicide risk."
            }


def calculate_hamilton_depression_rating_scale(
    depressed_mood, feelings_of_guilt, suicide,
    insomnia_early, insomnia_middle, insomnia_late,
    work_and_activities, retardation, agitation,
    anxiety_psychological, anxiety_somatic,
    somatic_symptoms_gastrointestinal, somatic_symptoms_general,
    genital_symptoms, hypochondriasis, loss_of_weight,
    insight) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HamiltonDepressionRatingScaleCalculator()
    return calculator.calculate(
        depressed_mood, feelings_of_guilt, suicide,
        insomnia_early, insomnia_middle, insomnia_late,
        work_and_activities, retardation, agitation,
        anxiety_psychological, anxiety_somatic,
        somatic_symptoms_gastrointestinal, somatic_symptoms_general,
        genital_symptoms, hypochondriasis, loss_of_weight,
        insight
    )