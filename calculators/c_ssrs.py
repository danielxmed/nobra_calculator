"""
Columbia Suicide Severity Rating Scale (C-SSRS) Screener Calculator

Screens for suicidal ideation and behavior to assess suicide risk 
and guide clinical management decisions.

References:
1. Posner K, et al. Am J Psychiatry. 2011;168(12):1266-77.
2. Bjureberg J, et al. Psychol Med. 2022;52(16):3904-3912.
3. Madan A, et al. J Clin Psychiatry. 2016;77(7):e867-73.
"""

from typing import Dict, Any


class CSSRSCalculator:
    """Calculator for Columbia Suicide Severity Rating Scale (C-SSRS) Screener"""
    
    def __init__(self):
        # Risk levels based on ideation and behavior
        self.RISK_LOW = "Low Risk"
        self.RISK_MODERATE = "Moderate Risk"
        self.RISK_HIGH = "High Risk"
    
    def calculate(self, ideation_level: int, behavior_level: int, 
                 behavior_recent: str) -> Dict[str, Any]:
        """
        Calculates the C-SSRS risk level based on ideation and behavior
        
        Args:
            ideation_level (int): Severity of suicidal ideation in past month (0-5)
            behavior_level (int): Most severe lifetime suicidal behavior (0-5)
            behavior_recent (str): Timing of most recent suicidal behavior
            
        Returns:
            Dict with risk level and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(ideation_level, behavior_level, behavior_recent)
        
        # Determine risk level
        risk_level = self._determine_risk_level(ideation_level, behavior_level, 
                                               behavior_recent)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_level)
        
        # Create detailed assessment
        assessment_details = self._create_assessment_details(
            ideation_level, behavior_level, behavior_recent
        )
        
        return {
            "result": risk_level,
            "unit": "category",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "assessment_details": assessment_details
        }
    
    def _validate_inputs(self, ideation_level: int, behavior_level: int,
                        behavior_recent: str):
        """Validates input parameters"""
        
        if not isinstance(ideation_level, int) or ideation_level < 0 or ideation_level > 5:
            raise ValueError("Ideation level must be an integer between 0 and 5")
        
        if not isinstance(behavior_level, int) or behavior_level < 0 or behavior_level > 5:
            raise ValueError("Behavior level must be an integer between 0 and 5")
        
        valid_timings = ["Never", "More than 3 months ago", "Within past 3 months"]
        if behavior_recent not in valid_timings:
            raise ValueError(f"Behavior timing must be one of: {', '.join(valid_timings)}")
        
        # Logical validation
        if behavior_level == 0 and behavior_recent != "Never":
            raise ValueError("If no suicidal behavior reported, timing must be 'Never'")
        
        if behavior_level > 0 and behavior_recent == "Never":
            raise ValueError("If suicidal behavior reported, timing cannot be 'Never'")
    
    def _determine_risk_level(self, ideation_level: int, behavior_level: int,
                             behavior_recent: str) -> str:
        """
        Determines risk level based on C-SSRS criteria
        
        Risk stratification:
        - High Risk: Ideation 4-5 OR behavior within past 3 months
        - Moderate Risk: Ideation 3 OR any lifetime behavior (>3 months ago)
        - Low Risk: Ideation 1-2 OR no ideation/behavior
        """
        
        # High risk criteria
        if ideation_level >= 4 or behavior_recent == "Within past 3 months":
            return self.RISK_HIGH
        
        # Moderate risk criteria
        if ideation_level == 3 or (behavior_level > 0 and behavior_recent == "More than 3 months ago"):
            return self.RISK_MODERATE
        
        # Low risk (includes ideation 1-2 or no ideation/behavior)
        return self.RISK_LOW
    
    def _get_interpretation(self, risk_level: str) -> Dict[str, str]:
        """
        Provides interpretation based on risk level
        
        Args:
            risk_level (str): Calculated risk level
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_level == self.RISK_LOW:
            return {
                "stage": "Low Risk",
                "description": "Low suicide risk",
                "interpretation": "Low risk for suicide. Consider behavioral health referral at discharge as appropriate. Continue to monitor for changes in ideation or behavior."
            }
        elif risk_level == self.RISK_MODERATE:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate suicide risk",
                "interpretation": "Moderate risk for suicide. Recommend behavioral health consultation and implementation of patient safety precautions. Develop safety plan before discharge."
            }
        else:  # High Risk
            return {
                "stage": "High Risk",
                "description": "High suicide risk",
                "interpretation": "High risk for suicide. Immediate physician and behavioral health notification required. Implement patient safety precautions. Consider psychiatric hospitalization."
            }
    
    def _create_assessment_details(self, ideation_level: int, behavior_level: int,
                                  behavior_recent: str) -> Dict[str, Any]:
        """Creates detailed assessment information"""
        
        ideation_descriptions = [
            "No reported suicidal ideation",
            "Wish to be dead",
            "Nonspecific active suicidal thoughts",
            "Active suicidal ideation with methods (no intent)",
            "Active suicidal ideation with some intent to act",
            "Active suicidal ideation with specific plan and intent"
        ]
        
        behavior_descriptions = [
            "No reported suicidal behavior",
            "Preparatory acts or behavior",
            "Aborted/self-interrupted attempt",
            "Interrupted attempt",
            "Actual suicide attempt",
            "Suicide (death occurred)"
        ]
        
        return {
            "ideation": {
                "level": ideation_level,
                "description": ideation_descriptions[ideation_level]
            },
            "behavior": {
                "level": behavior_level,
                "description": behavior_descriptions[behavior_level],
                "timing": behavior_recent
            }
        }


def calculate_c_ssrs(ideation_level: int, behavior_level: int, 
                    behavior_recent: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CSSRSCalculator()
    return calculator.calculate(ideation_level, behavior_level, behavior_recent)