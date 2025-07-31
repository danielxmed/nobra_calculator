"""
Hamilton Anxiety Scale Calculator

Rates level of anxiety based on clinical assessment across 14 domains.

References:
- Hamilton M. Br J Med Psychol. 1959;32(1):50-5.
- Matza LS, et al. Int J Methods Psychiatr Res. 2010;19(4):223-32.
"""

from typing import Dict, Any


class HamiltonAnxietyScaleCalculator:
    """Calculator for Hamilton Anxiety Scale (HAM-A)"""
    
    def __init__(self):
        # Scoring constants
        self.MIN_SCORE = 0
        self.MAX_SCORE = 4
        self.NUM_ITEMS = 14
        self.MAX_TOTAL_SCORE = self.MAX_SCORE * self.NUM_ITEMS  # 56
    
    def calculate(self, anxious_mood: int, tension: int, fears: int, insomnia: int,
                  intellectual: int, depressed_mood: int, somatic_muscular: int,
                  somatic_sensory: int, cardiovascular: int, respiratory: int,
                  gastrointestinal: int, genitourinary: int, autonomic_symptoms: int,
                  behavior_at_interview: int) -> Dict[str, Any]:
        """
        Calculates the HAM-A score
        
        Args:
            anxious_mood: Worries, anticipation of worst (0-4)
            tension: Feelings of tension, fatigability (0-4)
            fears: Of dark, strangers, being left alone (0-4)
            insomnia: Difficulty falling/staying asleep (0-4)
            intellectual: Difficulty concentrating, poor memory (0-4)
            depressed_mood: Loss of interest, depression (0-4)
            somatic_muscular: Pains, aches, twitching (0-4)
            somatic_sensory: Tinnitus, blurring vision (0-4)
            cardiovascular: Tachycardia, palpitations (0-4)
            respiratory: Pressure in chest, dyspnea (0-4)
            gastrointestinal: Swallowing difficulty, nausea (0-4)
            genitourinary: Urinary frequency, sexual dysfunction (0-4)
            autonomic_symptoms: Dry mouth, sweating (0-4)
            behavior_at_interview: Fidgeting, restlessness (0-4)
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        items = {
            "anxious_mood": anxious_mood,
            "tension": tension,
            "fears": fears,
            "insomnia": insomnia,
            "intellectual": intellectual,
            "depressed_mood": depressed_mood,
            "somatic_muscular": somatic_muscular,
            "somatic_sensory": somatic_sensory,
            "cardiovascular": cardiovascular,
            "respiratory": respiratory,
            "gastrointestinal": gastrointestinal,
            "genitourinary": genitourinary,
            "autonomic_symptoms": autonomic_symptoms,
            "behavior_at_interview": behavior_at_interview
        }
        
        self._validate_inputs(items)
        
        # Calculate total score
        result = self._calculate_total_score(items)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, items: Dict[str, int]):
        """Validates input parameters"""
        
        for item_name, score in items.items():
            if not isinstance(score, int):
                raise ValueError(f"{item_name} must be an integer")
            if score < self.MIN_SCORE or score > self.MAX_SCORE:
                raise ValueError(f"{item_name} must be between {self.MIN_SCORE} and {self.MAX_SCORE}")
    
    def _calculate_total_score(self, items: Dict[str, int]) -> int:
        """Calculates the total HAM-A score"""
        
        # Sum all item scores
        total_score = sum(items.values())
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): HAM-A score (0-56)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 7:
            return {
                "stage": "No/Minimal Anxiety",
                "description": "No or minimal anxiety symptoms",
                "interpretation": "Patient reports no significant anxiety symptoms or experiences minimal anxiety that does not interfere with daily functioning. No specific intervention typically required."
            }
        elif score <= 14:
            return {
                "stage": "Mild Anxiety",
                "description": "Mild anxiety symptoms",
                "interpretation": "Patient experiences mild anxiety symptoms that may cause some distress but generally do not significantly impair functioning. Consider monitoring and supportive interventions."
            }
        elif score <= 23:
            return {
                "stage": "Moderate Anxiety",
                "description": "Moderate anxiety symptoms",
                "interpretation": "Patient experiences moderate anxiety symptoms that interfere with daily activities and quality of life. Consider psychotherapy and/or pharmacological intervention."
            }
        else:
            return {
                "stage": "Severe Anxiety",
                "description": "Severe anxiety symptoms",
                "interpretation": "Patient experiences severe anxiety symptoms that significantly impair functioning and quality of life. Strongly consider intensive treatment including medication and psychotherapy."
            }


def calculate_hamilton_anxiety_scale(anxious_mood, tension, fears, insomnia,
                                   intellectual, depressed_mood, somatic_muscular,
                                   somatic_sensory, cardiovascular, respiratory,
                                   gastrointestinal, genitourinary, autonomic_symptoms,
                                   behavior_at_interview) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HamiltonAnxietyScaleCalculator()
    return calculator.calculate(anxious_mood, tension, fears, insomnia,
                              intellectual, depressed_mood, somatic_muscular,
                              somatic_sensory, cardiovascular, respiratory,
                              gastrointestinal, genitourinary, autonomic_symptoms,
                              behavior_at_interview)