"""
CAGE Questions for Alcohol Use Calculator

Screens for excessive drinking and alcoholism using 4 clinical questions.

Reference:
Ewing JA. Detecting alcoholism: The CAGE questionnaire. JAMA. 1984 Oct 12;252(14):1905-7.
"""

from typing import Dict, Any


class CageQuestionsCalculator:
    """Calculator for CAGE Questions for Alcohol Use"""
    
    def __init__(self):
        # Define the questions for reference
        self.questions = {
            "cut_down": "Have you ever felt you needed to Cut down on your drinking?",
            "annoyed": "Have people Annoyed you by criticizing your drinking?",
            "guilty": "Have you ever felt Guilty about drinking?",
            "eye_opener": "Have you ever felt you needed a drink first thing in the morning (Eye-opener) to steady your nerves or to get rid of a hangover?"
        }
    
    def calculate(
        self,
        cut_down: str,
        annoyed: str,
        guilty: str,
        eye_opener: str
    ) -> Dict[str, Any]:
        """
        Calculates CAGE score for alcohol use screening
        
        Args:
            cut_down (str): "yes" or "no" - Ever felt need to cut down on drinking
            annoyed (str): "yes" or "no" - People annoyed by criticizing drinking
            guilty (str): "yes" or "no" - Ever felt guilty about drinking
            eye_opener (str): "yes" or "no" - Ever needed morning drink to steady nerves
            
        Returns:
            Dict with score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(cut_down, annoyed, guilty, eye_opener)
        
        # Calculate score
        score = self._calculate_score(cut_down, annoyed, guilty, eye_opener)
        
        # Get interpretation
        interpretation = self._get_interpretation(score, eye_opener)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "cut_down": cut_down,
                "annoyed": annoyed,
                "guilty": guilty,
                "eye_opener": eye_opener,
                "positive_screen": score >= 2
            }
        }
    
    def _validate_inputs(
        self,
        cut_down: str,
        annoyed: str,
        guilty: str,
        eye_opener: str
    ):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        # Check cut_down
        if cut_down not in valid_responses:
            raise ValueError(f"cut_down must be 'yes' or 'no', got '{cut_down}'")
        
        # Check annoyed
        if annoyed not in valid_responses:
            raise ValueError(f"annoyed must be 'yes' or 'no', got '{annoyed}'")
        
        # Check guilty
        if guilty not in valid_responses:
            raise ValueError(f"guilty must be 'yes' or 'no', got '{guilty}'")
        
        # Check eye_opener
        if eye_opener not in valid_responses:
            raise ValueError(f"eye_opener must be 'yes' or 'no', got '{eye_opener}'")
    
    def _calculate_score(
        self,
        cut_down: str,
        annoyed: str,
        guilty: str,
        eye_opener: str
    ) -> int:
        """Calculates total CAGE score"""
        
        score = 0
        
        # Add 1 point for each "yes" answer
        if cut_down == "yes":
            score += 1
        if annoyed == "yes":
            score += 1
        if guilty == "yes":
            score += 1
        if eye_opener == "yes":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int, eye_opener: str) -> Dict[str, str]:
        """
        Determines interpretation based on CAGE score
        
        Args:
            score (int): Total CAGE score (0-4)
            eye_opener (str): Response to eye-opener question
            
        Returns:
            Dict with interpretation details
        """
        
        if score >= 2:
            return {
                "stage": "Positive Screen",
                "description": "Higher likelihood of alcohol use disorder",
                "interpretation": (
                    f"CAGE score of {score} indicates a positive screen with >90% sensitivity "
                    "for alcohol disorders. Further evaluation is warranted including detailed "
                    "alcohol history, physical examination, laboratory testing, and potentially "
                    "referral to addiction specialist. Consider using additional assessment tools "
                    "such as AUDIT (Alcohol Use Disorders Identification Test) or MAST (Michigan "
                    "Alcoholism Screening Test) for more comprehensive evaluation. "
                    "Note that CAGE is a screening tool, not a diagnostic test."
                )
            }
        else:
            # Check for special case of positive eye-opener
            if eye_opener == "yes":
                return {
                    "stage": "Negative Screen",
                    "description": "Low likelihood of alcohol use disorder",
                    "interpretation": (
                        f"CAGE score of {score} indicates a negative screen. However, a positive "
                        "response to the 'eye-opener' question is concerning and may indicate "
                        "physiologic dependence on alcohol. This warrants further clinical "
                        "evaluation despite the overall negative screen. Consider detailed "
                        "assessment of drinking patterns, withdrawal symptoms, and impact on "
                        "daily functioning. Clinical judgment should guide next steps."
                    )
                }
            else:
                return {
                    "stage": "Negative Screen",
                    "description": "Low likelihood of alcohol use disorder",
                    "interpretation": (
                        f"CAGE score of {score} indicates a negative screen. While alcohol use "
                        "disorder is less likely, clinical judgment should be used, especially "
                        "if clinical suspicion remains high. Consider discussing safe drinking "
                        "limits (no more than 14 drinks per week for men, 7 for women) and "
                        "potential risks with the patient. Reassess periodically, particularly "
                        "if drinking patterns change or new concerns arise."
                    )
                }


def calculate_cage_questions(
    cut_down: str,
    annoyed: str,
    guilty: str,
    eye_opener: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CageQuestionsCalculator()
    return calculator.calculate(cut_down, annoyed, guilty, eye_opener)