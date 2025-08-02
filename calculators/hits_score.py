"""
HITS (Hurt, Insult, Threaten, Scream) Score Calculator

Detects domestic abuse (intimate partner violence) in women and men in healthcare 
settings using four questions about frequency of partner abuse behaviors.

References:
- Sherin KM, Sinacore JM, Li XQ, Zitter RE, Shakil A. HITS: a short domestic 
  violence screening tool for use in a family practice setting. Fam Med. 1998 Jul-Aug;30(7):508-12.
- Shakil A, Donald S, Sinacore JM, Krepcho M. Validation of the HITS domestic 
  violence screening tool with males. Fam Med. 2005 Mar;37(3):193-8.
"""

from typing import Dict, Any


class HitsScoreCalculator:
    """Calculator for HITS (Hurt, Insult, Threaten, Scream) Score"""
    
    def __init__(self):
        # Point values for frequency responses
        self.frequency_points = {
            "never": 1,
            "rarely": 2,
            "sometimes": 3,
            "fairly_often": 4,
            "frequently": 5
        }
    
    def calculate(self, physically_hurt: str, insult_talk_down: str, 
                 threaten_with_harm: str, scream_curse: str) -> Dict[str, Any]:
        """
        Calculates HITS score for intimate partner violence screening
        
        Args:
            physically_hurt (str): Frequency of physical hurt by partner
            insult_talk_down (str): Frequency of insults/talking down by partner
            threaten_with_harm (str): Frequency of threats of harm by partner
            scream_curse (str): Frequency of screaming/cursing by partner
            
        Returns:
            Dict with HITS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(physically_hurt, insult_talk_down, threaten_with_harm, scream_curse)
        
        # Calculate total score (sum of frequency ratings)
        score = (
            self.frequency_points[physically_hurt] +
            self.frequency_points[insult_talk_down] +
            self.frequency_points[threaten_with_harm] +
            self.frequency_points[scream_curse]
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        # Identify specific abuse types and frequencies
        abuse_behaviors = self._identify_abuse_behaviors(
            physically_hurt, insult_talk_down, threaten_with_harm, scream_curse
        )
        
        # Determine screening result based on cut-off
        positive_screen = score >= 11
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "positive_screen": positive_screen,
            "requires_safety_assessment": positive_screen,
            "abuse_behaviors_identified": abuse_behaviors,
            "sensitivity_english": 86 if positive_screen else None,
            "specificity_english": 99 if not positive_screen else None
        }
    
    def _validate_inputs(self, physically_hurt: str, insult_talk_down: str, 
                        threaten_with_harm: str, scream_curse: str):
        """Validates input parameters"""
        
        valid_frequencies = list(self.frequency_points.keys())
        
        if physically_hurt not in valid_frequencies:
            raise ValueError(f"Physically hurt frequency must be one of: {valid_frequencies}")
        
        if insult_talk_down not in valid_frequencies:
            raise ValueError(f"Insult/talk down frequency must be one of: {valid_frequencies}")
        
        if threaten_with_harm not in valid_frequencies:
            raise ValueError(f"Threaten with harm frequency must be one of: {valid_frequencies}")
        
        if scream_curse not in valid_frequencies:
            raise ValueError(f"Scream/curse frequency must be one of: {valid_frequencies}")
    
    def _identify_abuse_behaviors(self, physically_hurt: str, insult_talk_down: str,
                                 threaten_with_harm: str, scream_curse: str) -> Dict[str, str]:
        """
        Identifies specific abuse behaviors and their frequencies
        
        Returns:
            Dict with abuse types and their reported frequencies
        """
        
        behaviors = {}
        
        if physically_hurt != "never":
            behaviors["Physical Violence"] = self._format_frequency(physically_hurt)
        
        if insult_talk_down != "never":
            behaviors["Emotional/Verbal Abuse"] = self._format_frequency(insult_talk_down)
        
        if threaten_with_harm != "never":
            behaviors["Threats of Harm"] = self._format_frequency(threaten_with_harm)
        
        if scream_curse != "never":
            behaviors["Screaming/Cursing"] = self._format_frequency(scream_curse)
        
        return behaviors
    
    def _format_frequency(self, frequency: str) -> str:
        """Formats frequency string for display"""
        frequency_display = {
            "never": "Never",
            "rarely": "Rarely",
            "sometimes": "Sometimes", 
            "fairly_often": "Fairly Often",
            "frequently": "Frequently"
        }
        return frequency_display[frequency]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on HITS score
        
        Args:
            score (int): HITS score (4-20)
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 11:
            return {
                "stage": "Low Risk",
                "description": "Score 4-10",
                "interpretation": "Low risk for intimate partner violence based on current screening. Continue to provide supportive care and maintain awareness for signs of abuse. Consider follow-up screening at future visits."
            }
        else:
            return {
                "stage": "Positive Screen",
                "description": "Score ≥11",
                "interpretation": "Positive screen for intimate partner violence. Patient reports frequent abusive behaviors by partner. Requires immediate safety assessment, documentation, resource provision, and follow-up care planning in accordance with institutional protocols."
            }


def calculate_hits_score(physically_hurt: str, insult_talk_down: str,
                        threaten_with_harm: str, scream_curse: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HitsScoreCalculator()
    return calculator.calculate(physically_hurt, insult_talk_down, threaten_with_harm, scream_curse)