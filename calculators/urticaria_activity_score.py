"""
Urticaria Activity Score (UAS) Calculator

Stratifies severity of urticaria through diary-based assessment of wheals and itch 
intensity. The UAS7 score is calculated by summing daily scores over 7 consecutive 
days, providing a standardized measure for chronic spontaneous urticaria activity 
monitoring and treatment response assessment.

References:
- Młynek A, Zalewska-Janowska A, Martus P, et al. How to assess disease activity 
  in patients with chronic urticaria? Allergy. 2008;63(6):777-780.
- Hawro T, Ohanyan T, Schoepke N, et al. The Urticaria Activity Score--Validity, 
  Reliability, and Responsiveness. J Allergy Clin Immunol Pract. 2018;6(4):1185-1190.e1.
- Zuberbier T, Aberer W, Asero R, et al. The EAACI/GA²LEN/EDF/WAO Guideline for 
  the definition, classification, diagnosis, and management of urticaria: the 2014 
  revision. Allergy. 2014;69(7):868-887.
"""

from typing import Dict, Any


class UrticariaActivityScoreCalculator:
    """Calculator for Urticaria Activity Score (UAS)"""
    
    def __init__(self):
        # Score ranges for UAS7 interpretation
        self.WELL_CONTROLLED_THRESHOLD = 6
        self.MILD_THRESHOLD = 15
        self.MODERATE_THRESHOLD = 27
        self.SEVERE_THRESHOLD = 42
        
        # Cutoff for identifying active disease (from literature)
        self.ACTIVE_DISEASE_CUTOFF = 11
        self.ADEQUATE_CONTROL_CUTOFF = 7
        self.SEVERE_DISEASE_CUTOFF = 28
    
    def calculate(self, day1_wheals: int, day1_itch: int, day2_wheals: int, day2_itch: int,
                  day3_wheals: int, day3_itch: int, day4_wheals: int, day4_itch: int,
                  day5_wheals: int, day5_itch: int, day6_wheals: int, day6_itch: int,
                  day7_wheals: int, day7_itch: int) -> Dict[str, Any]:
        """
        Calculates the UAS7 score using daily wheals and itch scores
        
        Args:
            day1_wheals to day7_wheals (int): Daily wheals scores (0-3 each day)
                0 = None
                1 = Mild (<20 wheals/24h)
                2 = Moderate (20-50 wheals/24h)
                3 = Intense (>50 wheals/24h or large confluent areas)
            day1_itch to day7_itch (int): Daily itch intensity scores (0-3 each day)
                0 = None
                1 = Mild (present but not annoying)
                2 = Moderate (troublesome but doesn't interfere with daily activity)
                3 = Intense (severe, interferes with daily activity or sleep)
            
        Returns:
            Dict with the UAS7 result and interpretation
        """
        
        # Validate inputs
        daily_scores = [
            (day1_wheals, day1_itch), (day2_wheals, day2_itch), (day3_wheals, day3_itch),
            (day4_wheals, day4_itch), (day5_wheals, day5_itch), (day6_wheals, day6_itch),
            (day7_wheals, day7_itch)
        ]
        
        self._validate_inputs(daily_scores)
        
        # Calculate daily UAS scores
        daily_uas_scores = []
        for wheals, itch in daily_scores:
            daily_score = wheals + itch
            daily_uas_scores.append(daily_score)
        
        # Calculate UAS7 total score
        uas7_score = sum(daily_uas_scores)
        
        # Get interpretation
        interpretation = self._get_interpretation(uas7_score, daily_uas_scores)
        
        return {
            "result": uas7_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "daily_scores": daily_uas_scores,
            "average_daily_score": round(uas7_score / 7, 1)
        }
    
    def _validate_inputs(self, daily_scores):
        """Validates input parameters"""
        
        for day_num, (wheals, itch) in enumerate(daily_scores, 1):
            # Validate wheals score
            if not isinstance(wheals, int) or wheals < 0 or wheals > 3:
                raise ValueError(f"Day {day_num} wheals score must be an integer between 0 and 3")
            
            # Validate itch score
            if not isinstance(itch, int) or itch < 0 or itch > 3:
                raise ValueError(f"Day {day_num} itch score must be an integer between 0 and 3")
    
    def _get_interpretation(self, uas7_score: int, daily_scores: list) -> Dict[str, str]:
        """
        Determines the interpretation based on the UAS7 score
        
        Args:
            uas7_score (int): Total UAS7 score (0-42)
            daily_scores (list): List of daily UAS scores
            
        Returns:
            Dict with interpretation details
        """
        
        # Calculate average daily score
        avg_daily_score = uas7_score / 7
        
        # Additional clinical context based on literature cutoffs
        clinical_notes = []
        
        if uas7_score < self.ADEQUATE_CONTROL_CUTOFF:
            clinical_notes.append("indicates adequate disease control")
        elif uas7_score >= self.ACTIVE_DISEASE_CUTOFF:
            clinical_notes.append("suggests active disease requiring attention")
        
        if uas7_score >= self.SEVERE_DISEASE_CUTOFF:
            clinical_notes.append("requires intensive management and possible specialist referral")
        
        # Format daily scores for interpretation
        daily_scores_str = ", ".join([str(score) for score in daily_scores])
        
        # Base interpretation text
        base_interpretation = f"UAS7 score of {uas7_score}/42 (average daily score: {avg_daily_score:.1f}). Daily scores: {daily_scores_str}."
        
        if clinical_notes:
            clinical_context = " This score " + " and ".join(clinical_notes) + "."
        else:
            clinical_context = ""
        
        # Determine stage and specific interpretation
        if uas7_score == 0:
            return {
                "stage": "Urticaria-free",
                "description": "No urticaria activity",
                "interpretation": f"{base_interpretation} No wheals or itch reported over the 7-day period. This indicates complete disease control or absence of urticaria activity. Continue current management approach.{clinical_context}"
            }
        elif uas7_score <= self.WELL_CONTROLLED_THRESHOLD:
            return {
                "stage": "Well-controlled",
                "description": "Very mild urticaria activity",
                "interpretation": f"{base_interpretation} Minimal urticaria activity with very mild symptoms. Disease is well-controlled with current therapy. Consider maintaining current treatment regimen.{clinical_context}"
            }
        elif uas7_score <= self.MILD_THRESHOLD:
            return {
                "stage": "Mild",
                "description": "Mild urticaria activity",
                "interpretation": f"{base_interpretation} Mild urticaria activity that may require monitoring and potential adjustment of therapy. A UAS7 score <7 generally indicates adequate disease control, so scores in this range suggest mild but noticeable disease activity.{clinical_context}"
            }
        elif uas7_score <= self.MODERATE_THRESHOLD:
            return {
                "stage": "Moderate",
                "description": "Moderate urticaria activity",
                "interpretation": f"{base_interpretation} Moderate urticaria activity that likely impacts quality of life and daily activities. Consider intensifying treatment or adding therapies. Regular monitoring and reassessment of therapeutic approach recommended.{clinical_context}"
            }
        else:
            return {
                "stage": "Severe",
                "description": "Severe urticaria activity",
                "interpretation": f"{base_interpretation} Severe urticaria activity with significant impact on quality of life, daily activities, and sleep. UAS7 scores >28 indicate severe disease requiring aggressive treatment optimization, possible specialist referral, and consideration of advanced therapies.{clinical_context}"
            }


def calculate_urticaria_activity_score(day1_wheals: int, day1_itch: int, day2_wheals: int, day2_itch: int,
                                     day3_wheals: int, day3_itch: int, day4_wheals: int, day4_itch: int,
                                     day5_wheals: int, day5_itch: int, day6_wheals: int, day6_itch: int,
                                     day7_wheals: int, day7_itch: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = UrticariaActivityScoreCalculator()
    return calculator.calculate(day1_wheals, day1_itch, day2_wheals, day2_itch,
                               day3_wheals, day3_itch, day4_wheals, day4_itch,
                               day5_wheals, day5_itch, day6_wheals, day6_itch,
                               day7_wheals, day7_itch)