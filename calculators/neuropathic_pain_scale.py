"""
Neuropathic Pain Scale (NPS) Calculator

Quantifies severity of neuropathic pain in patients already diagnosed with neuropathic pain.

Reference:
Galer BS, Jensen MP. Development and preliminary validation of a pain measure specific 
to neuropathic pain: the Neuropathic Pain Scale. Neurology. 1997 Feb;48(2):332-8. 
doi: 10.1212/wnl.48.2.332.
"""

from typing import Dict, Any


class NeuropathicPainScaleCalculator:
    """Calculator for Neuropathic Pain Scale (NPS)"""
    
    def calculate(self, intensity: int, sharp: int, hot: int, dull: int, 
                  cold: int, sensitive: int, itchy: int, unpleasant: int,
                  deep_pain: int, surface_pain: int) -> Dict[str, Any]:
        """
        Calculates the NPS score
        
        Args:
            intensity (int): How intense is the pain? (0-10)
            sharp (int): How sharp is the pain? ('Like a knife') (0-10)
            hot (int): How hot is the pain? ('On fire') (0-10)
            dull (int): How dull is the pain? (0-10)
            cold (int): How cold is the pain? ('Freezing') (0-10)
            sensitive (int): How sensitive is the skin to light touch? ('Raw skin') (0-10)
            itchy (int): How itchy is the pain? (0-10)
            unpleasant (int): How unpleasant is the pain? ('Intolerable') (0-10)
            deep_pain (int): If the pain is deep, how intense is the deep pain? (0-10)
            surface_pain (int): If the pain is on the surface, how intense is the surface pain? (0-10)
            
        Returns:
            Dict with the total score and interpretation
        """
        
        # Validations
        self._validate_inputs(intensity, sharp, hot, dull, cold, sensitive,
                            itchy, unpleasant, deep_pain, surface_pain)
        
        # Calculate total score - simple sum of all 10 items
        total_score = (intensity + sharp + hot + dull + cold + 
                      sensitive + itchy + unpleasant + deep_pain + surface_pain)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, intensity: int, sharp: int, hot: int, dull: int,
                        cold: int, sensitive: int, itchy: int, unpleasant: int,
                        deep_pain: int, surface_pain: int):
        """Validates input parameters"""
        
        # Validate all pain quality scores (0-10)
        pain_qualities = [
            ("Intensity", intensity),
            ("Sharp", sharp),
            ("Hot", hot),
            ("Dull", dull),
            ("Cold", cold),
            ("Sensitive", sensitive),
            ("Itchy", itchy),
            ("Unpleasant", unpleasant),
            ("Deep pain", deep_pain),
            ("Surface pain", surface_pain)
        ]
        
        for name, value in pain_qualities:
            if not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
            if value < 0 or value > 10:
                raise ValueError(f"{name} must be between 0 and 10")
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Calculated NPS score
            
        Returns:
            Dict with interpretation
        """
        
        if total_score <= 20:
            return {
                "stage": "Mild",
                "description": "Mild neuropathic pain",
                "interpretation": (
                    f"NPS score of {total_score} indicates mild neuropathic pain symptoms. "
                    "Consider monitoring and conservative management strategies. "
                    "Track scores over time to assess treatment effectiveness and disease progression."
                )
            }
        elif total_score <= 40:
            return {
                "stage": "Moderate",
                "description": "Moderate neuropathic pain",
                "interpretation": (
                    f"NPS score of {total_score} indicates moderate neuropathic pain symptoms. "
                    "May benefit from multimodal pain management approach including both "
                    "pharmacological and non-pharmacological interventions. Consider adjusting "
                    "current treatment regimen if pain is not adequately controlled."
                )
            }
        elif total_score <= 60:
            return {
                "stage": "Severe",
                "description": "Severe neuropathic pain",
                "interpretation": (
                    f"NPS score of {total_score} indicates severe neuropathic pain symptoms. "
                    "Comprehensive pain management strategy recommended. Consider referral to "
                    "pain specialist or neurologist for optimization of treatment. Combination "
                    "therapies and adjuvant medications may be necessary."
                )
            }
        else:
            return {
                "stage": "Very Severe",
                "description": "Very severe neuropathic pain",
                "interpretation": (
                    f"NPS score of {total_score} indicates very severe neuropathic pain symptoms. "
                    "Urgent comprehensive pain management intervention may be needed. Strong "
                    "consideration for multidisciplinary pain management approach including "
                    "specialist referral, psychological support, and aggressive multimodal therapy."
                )
            }


def calculate_neuropathic_pain_scale(intensity: int, sharp: int, hot: int, dull: int,
                                    cold: int, sensitive: int, itchy: int, unpleasant: int,
                                    deep_pain: int, surface_pain: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NeuropathicPainScaleCalculator()
    return calculator.calculate(intensity, sharp, hot, dull, cold, sensitive,
                              itchy, unpleasant, deep_pain, surface_pain)