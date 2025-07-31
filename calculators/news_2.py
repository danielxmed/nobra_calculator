"""
National Early Warning Score (NEWS) 2 Calculator

Determines the degree of illness of a patient and prompts critical care intervention.
Recommended by NHS over original NEWS with improved oxygen saturation scoring for 
hypercapnic respiratory failure patients.

References:
- Royal College of Physicians. National Early Warning Score (NEWS) 2. London: RCP, 2017.
"""

from typing import Dict, Any


class News2Calculator:
    """Calculator for National Early Warning Score (NEWS) 2"""
    
    def __init__(self):
        # Scoring ranges for each parameter
        self.respiratory_rate_scores = {
            "8_or_less": 3,
            "9_to_11": 1,
            "12_to_20": 0,
            "21_to_24": 2,
            "25_or_more": 3
        }
        
        # Standard oxygen saturation scores (for non-hypercapnic patients)
        self.standard_spo2_scores = {
            "91_or_less": 3,
            "92_to_93": 2,
            "94_to_95": 1,
            "96_or_more": 0
        }
        
        # Hypercapnic respiratory failure oxygen saturation scores
        self.hypercapnic_spo2_scores = {
            "83_or_less": 3,
            "84_to_85": 2,
            "86_to_87": 1,
            "88_to_92": 0,  # Target range for hypercapnic patients
            "93_to_94": 1,  # On supplemental O2
            "95_to_96": 2,  # On supplemental O2
            "97_or_more": 3  # On supplemental O2
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
        
        self.consciousness_scores = {
            "alert": 0,
            "altered": 3  # Includes new-onset confusion, responds to voice/pain, unresponsive
        }
        
        self.supplemental_oxygen_scores = {
            "yes": 2,
            "no": 0
        }
    
    def calculate(self, respiratory_rate: str, hypercapnic_respiratory_failure: str,
                  oxygen_saturation: str, supplemental_oxygen: str, temperature: str,
                  systolic_bp: str, heart_rate: str, consciousness: str) -> Dict[str, Any]:
        """
        Calculates the NEWS 2 score using the provided parameters
        
        Args:
            respiratory_rate: Respiratory rate category
            hypercapnic_respiratory_failure: Whether patient has hypercapnic respiratory failure
            oxygen_saturation: Oxygen saturation category
            supplemental_oxygen: Whether on supplemental oxygen
            temperature: Temperature category
            systolic_bp: Systolic blood pressure category
            heart_rate: Heart rate category
            consciousness: Consciousness level
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(respiratory_rate, hypercapnic_respiratory_failure,
                            oxygen_saturation, supplemental_oxygen, temperature,
                            systolic_bp, heart_rate, consciousness)
        
        # Calculate individual scores
        resp_score = self.respiratory_rate_scores[respiratory_rate]
        temp_score = self.temperature_scores[temperature]
        bp_score = self.systolic_bp_scores[systolic_bp]
        hr_score = self.heart_rate_scores[heart_rate]
        consciousness_score = self.consciousness_scores[consciousness]
        o2_supplement_score = self.supplemental_oxygen_scores[supplemental_oxygen]
        
        # Calculate oxygen saturation score based on hypercapnic status
        spo2_score = self._calculate_spo2_score(oxygen_saturation, 
                                               hypercapnic_respiratory_failure == "yes",
                                               supplemental_oxygen == "yes")
        
        # Calculate total score
        total_score = (resp_score + spo2_score + o2_supplement_score + 
                      temp_score + bp_score + hr_score + consciousness_score)
        
        # Check for RED score (any parameter scoring 3)
        has_red_score = any([
            resp_score == 3,
            spo2_score == 3,
            temp_score == 3,
            bp_score == 3,
            hr_score == 3,
            consciousness_score == 3
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
    
    def _validate_inputs(self, respiratory_rate: str, hypercapnic_respiratory_failure: str,
                        oxygen_saturation: str, supplemental_oxygen: str, temperature: str,
                        systolic_bp: str, heart_rate: str, consciousness: str):
        """Validates input parameters"""
        
        if respiratory_rate not in self.respiratory_rate_scores:
            raise ValueError(f"Invalid respiratory_rate: {respiratory_rate}")
        
        if hypercapnic_respiratory_failure not in ["yes", "no"]:
            raise ValueError(f"Invalid hypercapnic_respiratory_failure: {hypercapnic_respiratory_failure}")
        
        if temperature not in self.temperature_scores:
            raise ValueError(f"Invalid temperature: {temperature}")
        
        if systolic_bp not in self.systolic_bp_scores:
            raise ValueError(f"Invalid systolic_bp: {systolic_bp}")
        
        if heart_rate not in self.heart_rate_scores:
            raise ValueError(f"Invalid heart_rate: {heart_rate}")
        
        if consciousness not in self.consciousness_scores:
            raise ValueError(f"Invalid consciousness: {consciousness}")
        
        if supplemental_oxygen not in self.supplemental_oxygen_scores:
            raise ValueError(f"Invalid supplemental_oxygen: {supplemental_oxygen}")
    
    def _calculate_spo2_score(self, oxygen_saturation: str, is_hypercapnic: bool, 
                             on_supplemental_o2: bool) -> int:
        """
        Calculates oxygen saturation score based on hypercapnic status
        
        Args:
            oxygen_saturation: Oxygen saturation category
            is_hypercapnic: Whether patient has hypercapnic respiratory failure
            on_supplemental_o2: Whether patient is on supplemental oxygen
            
        Returns:
            Score for oxygen saturation
        """
        
        if is_hypercapnic:
            # Hypercapnic respiratory failure scoring
            if oxygen_saturation == "83_or_less":
                return 3
            elif oxygen_saturation == "84_to_85":
                return 2
            elif oxygen_saturation == "86_to_87":
                return 1
            elif oxygen_saturation == "88_to_92":
                return 0  # Target range
            elif oxygen_saturation == "93_to_94" and on_supplemental_o2:
                return 1
            elif oxygen_saturation == "95_to_96" and on_supplemental_o2:
                return 2
            elif oxygen_saturation == "97_or_more" and on_supplemental_o2:
                return 3
            elif oxygen_saturation in ["93_to_94", "94_to_95", "95_to_96", "96_or_more", "97_or_more"] and not on_supplemental_o2:
                return 0  # ≥93% on room air scores 0
            else:
                # Map general ranges to hypercapnic ranges
                if oxygen_saturation == "91_or_less":
                    return 3
                elif oxygen_saturation == "92_to_93":
                    return 0  # Falls in 88-92% range
                else:
                    return 0
        else:
            # Standard oxygen saturation scoring
            if oxygen_saturation == "91_or_less":
                return 3
            elif oxygen_saturation == "92_to_93":
                return 2
            elif oxygen_saturation == "94_to_95":
                return 1
            elif oxygen_saturation in ["96_or_more", "97_or_more"]:
                return 0
            else:
                # Map hypercapnic ranges to standard ranges for non-hypercapnic patients
                if oxygen_saturation == "83_or_less":
                    return 3  # ≤91%
                elif oxygen_saturation in ["84_to_85", "86_to_87"]:
                    return 3  # ≤91%
                elif oxygen_saturation == "88_to_92":
                    return 2  # 92-93%
                elif oxygen_saturation == "93_to_94":
                    return 1  # 94-95%
                elif oxygen_saturation == "95_to_96":
                    return 0  # ≥96%
                else:
                    return 0
    
    def _get_interpretation(self, score: int, has_red_score: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and RED score status
        
        Args:
            score: Total NEWS 2 score
            has_red_score: Whether any parameter scored 3 points
            
        Returns:
            Dict with interpretation details
        """
        
        # RED score (any parameter = 3) triggers medium risk response
        if has_red_score and score < 5:
            return {
                "stage": "Low-Medium Risk",
                "description": "RED score - Individual parameter scoring 3",
                "interpretation": "Urgent review by ward-based doctor required. Minimum monitoring frequency every hour."
            }
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Very low early warning score",
                "interpretation": "Continue routine monitoring. Minimum monitoring frequency every 12 hours."
            }
        elif score >= 1 and score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Low early warning score",
                "interpretation": "Assessment by competent registered nurse. Minimum monitoring frequency every 4-6 hours."
            }
        elif score >= 5 and score <= 6:
            return {
                "stage": "Medium Risk",
                "description": "Medium early warning score",
                "interpretation": "Urgent review by ward-based doctor or acute team nurse to decide if critical care team assessment needed."
            }
        else:  # score >= 7
            return {
                "stage": "High Risk",
                "description": "High early warning score",
                "interpretation": "Emergent assessment by clinical team or critical care team. Continuous monitoring of vital signs. Usually requires transfer to higher level of care."
            }


def calculate_news_2(respiratory_rate: str, hypercapnic_respiratory_failure: str,
                    oxygen_saturation: str, supplemental_oxygen: str, temperature: str,
                    systolic_bp: str, heart_rate: str, consciousness: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = News2Calculator()
    return calculator.calculate(respiratory_rate, hypercapnic_respiratory_failure,
                              oxygen_saturation, supplemental_oxygen, temperature,
                              systolic_bp, heart_rate, consciousness)