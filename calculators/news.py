"""
National Early Warning Score (NEWS) Calculator

Determines the degree of illness of a patient and prompts critical care intervention.

References:
1. Royal College of Physicians. National Early Warning Score (NEWS): Standardising 
   the assessment of acute-illness severity in the NHS. Report of a working party. 
   London: RCP, 2012.
2. Smith GB, Prytherch DR, Meredith P, Schmidt PE, Featherstone PI. The ability 
   of the National Early Warning Score (NEWS) to discriminate patients at risk of 
   early cardiac arrest, unanticipated intensive care unit admission, and death. 
   Resuscitation. 2013 Apr;84(4):465-70.
"""

from typing import Dict, Any


class NewsCalculator:
    """Calculator for National Early Warning Score (NEWS)"""
    
    def __init__(self):
        # Scoring matrices for each parameter
        self.respiratory_rate_scores = {
            "8_or_less": 3,
            "9_to_11": 1,
            "12_to_20": 0,
            "21_to_24": 2,
            "25_or_more": 3
        }
        
        self.oxygen_saturation_scores = {
            "91_or_less": 3,
            "92_to_93": 2,
            "94_to_95": 1,
            "96_or_more": 0
        }
        
        self.supplemental_oxygen_scores = {
            "yes": 2,
            "no": 0
        }
        
        self.temperature_scores = {
            "35_or_less": 3,
            "35_1_to_36": 1,
            "36_1_to_38": 0,
            "38_1_to_39": 1,
            "39_1_or_more": 2
        }
        
        self.systolic_bp_scores = {
            "90_or_less": 3,
            "91_to_100": 2,
            "101_to_110": 1,
            "111_to_219": 0,
            "220_or_more": 3
        }
        
        self.heart_rate_scores = {
            "40_or_less": 3,
            "41_to_50": 1,
            "51_to_90": 0,
            "91_to_110": 1,
            "111_to_130": 2,
            "131_or_more": 3
        }
        
        self.avpu_scores = {
            "alert": 0,
            "voice_pain_unresponsive": 3
        }
    
    def calculate(self, respiratory_rate: str, oxygen_saturation: str, 
                  supplemental_oxygen: str, temperature: str, systolic_bp: str,
                  heart_rate: str, avpu_score: str) -> Dict[str, Any]:
        """
        Calculates the NEWS score using the provided parameters
        
        Args:
            respiratory_rate: Respiratory rate range
            oxygen_saturation: Oxygen saturation percentage range
            supplemental_oxygen: Whether on supplemental oxygen (yes/no)
            temperature: Temperature range
            systolic_bp: Systolic blood pressure range
            heart_rate: Heart rate range
            avpu_score: AVPU neurological assessment
            
        Returns:
            Dict with the NEWS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(respiratory_rate, oxygen_saturation, supplemental_oxygen,
                            temperature, systolic_bp, heart_rate, avpu_score)
        
        # Calculate total score
        total_score = 0
        
        # Add scores from each parameter
        total_score += self.respiratory_rate_scores[respiratory_rate]
        total_score += self.oxygen_saturation_scores[oxygen_saturation]
        total_score += self.supplemental_oxygen_scores[supplemental_oxygen]
        total_score += self.temperature_scores[temperature]
        total_score += self.systolic_bp_scores[systolic_bp]
        total_score += self.heart_rate_scores[heart_rate]
        total_score += self.avpu_scores[avpu_score]
        
        # Check for RED score (any single parameter scoring 3)
        has_red_score = any([
            self.respiratory_rate_scores[respiratory_rate] == 3,
            self.oxygen_saturation_scores[oxygen_saturation] == 3,
            self.temperature_scores[temperature] == 3,
            self.systolic_bp_scores[systolic_bp] == 3,
            self.heart_rate_scores[heart_rate] == 3,
            self.avpu_scores[avpu_score] == 3
        ])
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, has_red_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, respiratory_rate, oxygen_saturation, supplemental_oxygen,
                        temperature, systolic_bp, heart_rate, avpu_score):
        """Validates input parameters"""
        
        if respiratory_rate not in self.respiratory_rate_scores:
            raise ValueError(f"Invalid respiratory rate: {respiratory_rate}")
        
        if oxygen_saturation not in self.oxygen_saturation_scores:
            raise ValueError(f"Invalid oxygen saturation: {oxygen_saturation}")
        
        if supplemental_oxygen not in self.supplemental_oxygen_scores:
            raise ValueError(f"Invalid supplemental oxygen value: {supplemental_oxygen}")
        
        if temperature not in self.temperature_scores:
            raise ValueError(f"Invalid temperature: {temperature}")
        
        if systolic_bp not in self.systolic_bp_scores:
            raise ValueError(f"Invalid systolic BP: {systolic_bp}")
        
        if heart_rate not in self.heart_rate_scores:
            raise ValueError(f"Invalid heart rate: {heart_rate}")
        
        if avpu_score not in self.avpu_scores:
            raise ValueError(f"Invalid AVPU score: {avpu_score}")
    
    def _get_interpretation(self, score: int, has_red_score: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on the NEWS score
        
        Args:
            score: Total NEWS score
            has_red_score: Whether any single parameter scored 3 (RED score)
            
        Returns:
            Dict with interpretation
        """
        
        # If score is 5-6 OR has RED score, it's medium risk
        if (score >= 5 and score <= 6) or (score < 5 and has_red_score):
            return {
                "stage": "Medium Risk",
                "description": "Medium early warning score" + (" (RED score present)" if has_red_score and score < 5 else ""),
                "interpretation": "Urgent review by a clinician skilled with competencies in the assessment of acute illness – usually a ward-based doctor or acute team nurse, who should consider whether escalation of care to a team with critical-care skills is required."
            }
        elif score >= 7:
            return {
                "stage": "High Risk",
                "description": "High early warning score",
                "interpretation": "Emergency assessment by a clinical team/critical care outreach team with critical-care competencies and usually transfer of the patient to a higher dependency care area."
            }
        elif score >= 1 and score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Low early warning score",
                "interpretation": "Assessment by a competent registered nurse should decide if a change to frequency of clinical monitoring or an escalation of clinical care is required."
            }
        else:  # score == 0
            return {
                "stage": "Low Risk",
                "description": "Very low early warning score",
                "interpretation": "Continue routine monitoring."
            }


def calculate_news(respiratory_rate, oxygen_saturation, supplemental_oxygen,
                  temperature, systolic_bp, heart_rate, avpu_score) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NewsCalculator()
    return calculator.calculate(respiratory_rate, oxygen_saturation, supplemental_oxygen,
                              temperature, systolic_bp, heart_rate, avpu_score)