"""
Adult Self-Report Scale (ASRS v1.1) for ADHD Calculator

Screens and diagnoses adult ADHD based on DSM-IV-TR criteria using an 18-question 
self-report questionnaire.

References:
- Kessler RC, Adler L, Ames M, et al. The World Health Organization Adult ADHD 
  Self-Report Scale (ASRS): a short screening scale for use in the general population. 
  Psychol Med. 2005 Feb;35(2):245-56.
- Schweitzer JB, Cummins TK, Kant CA. Attention-deficit/hyperactivity disorder. 
  Med Clin North Am. 2001 May;85(3):757-77.
"""

from typing import Dict, Any


class AsrsV11AdhdCalculator:
    """Calculator for Adult Self-Report Scale (ASRS v1.1) for ADHD"""
    
    def __init__(self):
        # Part A questions (1-6) - Primary screener with specific scoring thresholds
        self.PART_A_THRESHOLDS = {
            'q1_wrapping_details': ['sometimes', 'often', 'very_often'],
            'q2_organization': ['often', 'very_often'],
            'q3_appointments': ['sometimes', 'often', 'very_often'],
            'q4_avoidance': ['often', 'very_often'],
            'q5_fidgeting': ['sometimes', 'often', 'very_often'],
            'q6_hyperactivity': ['sometimes', 'often', 'very_often']
        }
        
        # Part B questions (7-18) - Additional clinical information
        self.PART_B_QUESTIONS = [
            'q7_careless_mistakes', 'q8_attention_difficulty', 'q9_concentration',
            'q10_misplacing', 'q11_distractibility', 'q12_leaving_seat',
            'q13_restlessness', 'q14_difficulty_relaxing', 'q15_talking_too_much',
            'q16_finishing_sentences', 'q17_waiting_turn', 'q18_interrupting'
        ]
        
        # Response scoring
        self.RESPONSE_SCORES = {
            'never': 0,
            'rarely': 1,
            'sometimes': 2,
            'often': 3,
            'very_often': 4
        }
    
    def calculate(self, q1_wrapping_details: str, q2_organization: str, q3_appointments: str,
                 q4_avoidance: str, q5_fidgeting: str, q6_hyperactivity: str,
                 q7_careless_mistakes: str, q8_attention_difficulty: str, q9_concentration: str,
                 q10_misplacing: str, q11_distractibility: str, q12_leaving_seat: str,
                 q13_restlessness: str, q14_difficulty_relaxing: str, q15_talking_too_much: str,
                 q16_finishing_sentences: str, q17_waiting_turn: str, q18_interrupting: str) -> Dict[str, Any]:
        """
        Calculates the ASRS v1.1 ADHD screening result
        
        Args:
            q1-q18: Responses to the 18 ASRS questions (never, rarely, sometimes, often, very_often)
            
        Returns:
            Dict with the screening result and interpretation
        """
        
        # Collect all responses
        responses = {
            'q1_wrapping_details': q1_wrapping_details,
            'q2_organization': q2_organization,
            'q3_appointments': q3_appointments,
            'q4_avoidance': q4_avoidance,
            'q5_fidgeting': q5_fidgeting,
            'q6_hyperactivity': q6_hyperactivity,
            'q7_careless_mistakes': q7_careless_mistakes,
            'q8_attention_difficulty': q8_attention_difficulty,
            'q9_concentration': q9_concentration,
            'q10_misplacing': q10_misplacing,
            'q11_distractibility': q11_distractibility,
            'q12_leaving_seat': q12_leaving_seat,
            'q13_restlessness': q13_restlessness,
            'q14_difficulty_relaxing': q14_difficulty_relaxing,
            'q15_talking_too_much': q15_talking_too_much,
            'q16_finishing_sentences': q16_finishing_sentences,
            'q17_waiting_turn': q17_waiting_turn,
            'q18_interrupting': q18_interrupting
        }
        
        # Validate responses
        self._validate_inputs(responses)
        
        # Calculate Part A score (primary screener)
        part_a_score = self._calculate_part_a_score(responses)
        
        # Calculate Part B scores (additional information)
        part_b_scores = self._calculate_part_b_scores(responses)
        
        # Calculate total score for reference
        total_score = sum(self.RESPONSE_SCORES[response] for response in responses.values())
        
        # Determine screening result
        screening_result = self._determine_screening_result(part_a_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(part_a_score, screening_result)
        
        return {
            "result": f"Part A: {part_a_score}/6 | Total: {total_score}/72",
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "part_a_score": part_a_score,
            "part_b_total": sum(part_b_scores.values()),
            "total_score": total_score,
            "screening_positive": screening_result
        }
    
    def _validate_inputs(self, responses: Dict[str, str]):
        """Validates all input responses"""
        
        valid_responses = ['never', 'rarely', 'sometimes', 'often', 'very_often']
        
        for question, response in responses.items():
            if response not in valid_responses:
                raise ValueError(f"Response for {question} must be one of: {', '.join(valid_responses)}")
    
    def _calculate_part_a_score(self, responses: Dict[str, str]) -> int:
        """
        Calculates Part A score using specific thresholds for each question
        
        Part A uses weighted scoring where each question has specific thresholds
        that count as "positive" responses based on validation studies.
        """
        score = 0
        
        for question, threshold_responses in self.PART_A_THRESHOLDS.items():
            if responses[question] in threshold_responses:
                score += 1
        
        return score
    
    def _calculate_part_b_scores(self, responses: Dict[str, str]) -> Dict[str, int]:
        """
        Calculates Part B scores for additional clinical information
        
        Part B provides supplementary information and uses standard scoring.
        """
        part_b_scores = {}
        
        for question in self.PART_B_QUESTIONS:
            part_b_scores[question] = self.RESPONSE_SCORES[responses[question]]
        
        return part_b_scores
    
    def _determine_screening_result(self, part_a_score: int) -> bool:
        """
        Determines if screening is positive based on Part A score
        
        A score of 4 or more on Part A indicates positive screening.
        """
        return part_a_score >= 4
    
    def _get_interpretation(self, part_a_score: int, screening_positive: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on the Part A score
        
        Args:
            part_a_score: Score on Part A (0-6)
            screening_positive: Whether screening is positive
            
        Returns:
            Dict with interpretation details
        """
        
        if screening_positive:
            return {
                "stage": "Positive Screen",
                "description": "Possible ADHD",
                "interpretation": f"Screening positive for ADHD (Part A score: {part_a_score}/6). Score ≥4 on Part A indicates symptoms highly consistent with adult ADHD. Further comprehensive clinical evaluation by a qualified healthcare professional is warranted to confirm diagnosis and determine appropriate treatment options."
            }
        else:
            return {
                "stage": "Negative Screen", 
                "description": "Unlikely ADHD",
                "interpretation": f"Screening negative for ADHD (Part A score: {part_a_score}/6). Score <4 on Part A indicates symptoms are less likely to be consistent with adult ADHD. However, if clinical concerns persist, consider consultation with a healthcare professional for further evaluation."
            }


def calculate_asrs_v1_1_adhd(q1_wrapping_details, q2_organization, q3_appointments,
                            q4_avoidance, q5_fidgeting, q6_hyperactivity,
                            q7_careless_mistakes, q8_attention_difficulty, q9_concentration,
                            q10_misplacing, q11_distractibility, q12_leaving_seat,
                            q13_restlessness, q14_difficulty_relaxing, q15_talking_too_much,
                            q16_finishing_sentences, q17_waiting_turn, q18_interrupting) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AsrsV11AdhdCalculator()
    return calculator.calculate(
        q1_wrapping_details, q2_organization, q3_appointments,
        q4_avoidance, q5_fidgeting, q6_hyperactivity,
        q7_careless_mistakes, q8_attention_difficulty, q9_concentration,
        q10_misplacing, q11_distractibility, q12_leaving_seat,
        q13_restlessness, q14_difficulty_relaxing, q15_talking_too_much,
        q16_finishing_sentences, q17_waiting_turn, q18_interrupting
    )