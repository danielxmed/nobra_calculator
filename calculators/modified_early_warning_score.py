"""
Modified Early Warning Score (MEWS) for Clinical Deterioration Calculator

Determines the degree of illness of a patient and identifies patients at risk 
of clinical deterioration using physiological parameters.

References:
1. Subbe CP, et al. QJM. 2001;94(10):521-6.
2. Morgan RJM, et al. Clinical Intensive Care. 1997;8:100.
3. Goldhill DR, et al. Anaesthesia. 2005;60(6):547-53.
"""

from typing import Dict, Any


class ModifiedEarlyWarningScoreCalculator:
    """Calculator for Modified Early Warning Score (MEWS) for Clinical Deterioration"""
    
    def __init__(self):
        # MEWS scoring criteria
        self.BP_SCORING = [
            (70, float('-inf'), 3),  # ≤70
            (80, 71, 2),             # 71-80
            (100, 81, 1),            # 81-100
            (199, 101, 0),           # 101-199
            (float('inf'), 200, 2)   # ≥200
        ]
        
        self.HR_SCORING = [
            (39, float('-inf'), 2),  # <40
            (50, 40, 1),             # 40-50
            (100, 51, 0),            # 51-100
            (110, 101, 1),           # 101-110
            (129, 111, 2),           # 111-129
            (float('inf'), 130, 3)   # ≥130
        ]
        
        self.RR_SCORING = [
            (8, float('-inf'), 2),   # <9
            (14, 9, 0),              # 9-14
            (20, 15, 1),             # 15-20
            (29, 21, 2),             # 21-29
            (float('inf'), 30, 3)    # ≥30
        ]
        
        self.TEMP_SCORING = [
            (34.9, float('-inf'), 2),  # <35
            (38.4, 35.0, 0),           # 35.0-38.4
            (float('inf'), 38.5, 2)    # >38.5
        ]
        
        self.CONSCIOUSNESS_SCORING = {
            "alert": 0,
            "voice": 1,
            "pain": 2,
            "unresponsive": 3
        }
    
    def calculate(self, systolic_bp: int, heart_rate: int, respiratory_rate: int,
                  temperature: float, consciousness_level: str) -> Dict[str, Any]:
        """
        Calculates the Modified Early Warning Score (MEWS)
        
        Args:
            systolic_bp (int): Systolic blood pressure in mmHg
            heart_rate (int): Heart rate in beats per minute
            respiratory_rate (int): Respiratory rate in breaths per minute
            temperature (float): Body temperature in degrees Celsius
            consciousness_level (str): Level of consciousness (alert, voice, pain, unresponsive)
            
        Returns:
            Dict with MEWS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(systolic_bp, heart_rate, respiratory_rate, 
                            temperature, consciousness_level)
        
        # Calculate individual component scores
        bp_score = self._calculate_bp_score(systolic_bp)
        hr_score = self._calculate_hr_score(heart_rate)
        rr_score = self._calculate_rr_score(respiratory_rate)
        temp_score = self._calculate_temp_score(temperature)
        consciousness_score = self._calculate_consciousness_score(consciousness_level)
        
        # Calculate total score
        total_score = bp_score + hr_score + rr_score + temp_score + consciousness_score
        
        # Check for any single parameter scoring 3 points (high risk indicator)
        high_risk_parameter = any(score == 3 for score in 
                                [bp_score, hr_score, rr_score, temp_score, consciousness_score])
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, high_risk_parameter)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, systolic_bp: int, heart_rate: int, respiratory_rate: int,
                        temperature: float, consciousness_level: str):
        """Validates input parameters"""
        
        # Validate data types
        if not isinstance(systolic_bp, int):
            raise ValueError("systolic_bp must be an integer")
        if not isinstance(heart_rate, int):
            raise ValueError("heart_rate must be an integer")
        if not isinstance(respiratory_rate, int):
            raise ValueError("respiratory_rate must be an integer")
        if not isinstance(temperature, (int, float)):
            raise ValueError("temperature must be a number")
        if not isinstance(consciousness_level, str):
            raise ValueError("consciousness_level must be a string")
        
        # Validate ranges
        if systolic_bp < 50 or systolic_bp > 300:
            raise ValueError("systolic_bp must be between 50 and 300 mmHg")
        if heart_rate < 20 or heart_rate > 200:
            raise ValueError("heart_rate must be between 20 and 200 bpm")
        if respiratory_rate < 5 or respiratory_rate > 60:
            raise ValueError("respiratory_rate must be between 5 and 60 breaths/min")
        if temperature < 30.0 or temperature > 45.0:
            raise ValueError("temperature must be between 30.0 and 45.0 °C")
        
        # Validate consciousness level
        valid_consciousness = ["alert", "voice", "pain", "unresponsive"]
        if consciousness_level not in valid_consciousness:
            raise ValueError(f"consciousness_level must be one of: {', '.join(valid_consciousness)}")
    
    def _calculate_bp_score(self, systolic_bp: int) -> int:
        """Calculates blood pressure component score"""
        for max_val, min_val, score in self.BP_SCORING:
            if min_val <= systolic_bp <= max_val:
                return score
        return 0
    
    def _calculate_hr_score(self, heart_rate: int) -> int:
        """Calculates heart rate component score"""
        for max_val, min_val, score in self.HR_SCORING:
            if min_val <= heart_rate <= max_val:
                return score
        return 0
    
    def _calculate_rr_score(self, respiratory_rate: int) -> int:
        """Calculates respiratory rate component score"""
        for max_val, min_val, score in self.RR_SCORING:
            if min_val <= respiratory_rate <= max_val:
                return score
        return 0
    
    def _calculate_temp_score(self, temperature: float) -> int:
        """Calculates temperature component score"""
        for max_val, min_val, score in self.TEMP_SCORING:
            if min_val <= temperature <= max_val:
                return score
        return 0
    
    def _calculate_consciousness_score(self, consciousness_level: str) -> int:
        """Calculates consciousness level component score"""
        return self.CONSCIOUSNESS_SCORING[consciousness_level]
    
    def _get_interpretation(self, score: int, high_risk_parameter: bool) -> Dict[str, str]:
        """
        Provides clinical interpretation based on MEWS score
        
        Args:
            score: MEWS total score (0-14)
            high_risk_parameter: Whether any single parameter scored 3 points
            
        Returns:
            Dict with interpretation details
        """
        
        # Base interpretation by score
        if score <= 2:
            base_interpretation = {
                "stage": "Low Risk",
                "description": "Low risk of deterioration",
                "interpretation": (f"MEWS score of {score} indicates low risk of clinical deterioration. "
                                 "Continue routine monitoring and standard nursing observations as per "
                                 "protocol. Reassess vital signs according to hospital policy.")
            }
        elif score <= 4:
            base_interpretation = {
                "stage": "Moderate Risk",
                "description": "Moderate risk of deterioration",
                "interpretation": (f"MEWS score of {score} indicates moderate risk of clinical deterioration. "
                                 "Increase monitoring frequency and consider medical review within 1-2 hours. "
                                 "Alert healthcare team and ensure appropriate escalation protocols are followed.")
            }
        else:  # score >= 5
            base_interpretation = {
                "stage": "High Risk",
                "description": "High risk of deterioration",
                "interpretation": (f"MEWS score of {score} indicates high risk of clinical deterioration. "
                                 "Immediate medical review required. Consider ICU consultation. This score "
                                 "is associated with significantly increased risk of death or ICU admission. "
                                 "Implement continuous monitoring and prepare for potential transfer to "
                                 "higher level of care.")
            }
        
        # Add warning for high-risk single parameter
        if high_risk_parameter and score < 5:
            base_interpretation["interpretation"] += (" NOTE: One or more vital signs scored 3 points, "
                                                    "which suggests considering a higher level of care "
                                                    "despite the total score being <5.")
        
        return base_interpretation


def calculate_modified_early_warning_score(systolic_bp: int, heart_rate: int,
                                         respiratory_rate: int, temperature: float,
                                         consciousness_level: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedEarlyWarningScoreCalculator()
    return calculator.calculate(systolic_bp, heart_rate, respiratory_rate,
                              temperature, consciousness_level)