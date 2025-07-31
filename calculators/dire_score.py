"""
DIRE Score for Opioid Treatment Calculator

Predicts compliance with opioid treatment for chronic non-cancer pain.

References:
1. Belgrade MJ, Schamber CD, Lindgren BR. The DIRE score: predicting outcomes of 
   opioid prescribing for chronic pain. J Pain. 2006;7(9):671-81.
2. Chou R, Fanciullo GJ, Fine PG, et al. Clinical guidelines for the use of chronic 
   opioid therapy in chronic noncancer pain. J Pain. 2009;10(2):113-30.
"""

from typing import Dict, Any


class DireScoreCalculator:
    """Calculator for DIRE Score for Opioid Treatment"""
    
    def __init__(self):
        # Define parameter descriptions for clarity
        self.PARAMETER_DESCRIPTIONS = {
            "diagnosis": {
                1: "Benign chronic condition, minimal objective findings, or no definite diagnosis",
                2: "Slowly progressive condition concordant with moderate pain or fixed condition with moderate objective findings",
                3: "Advanced condition concordant with severe pain with objective findings"
            },
            "intractability": {
                1: "Few therapies tried; patient takes a passive role in pain management process",
                2: "Most customary treatments tried but patient not fully engaged or barriers prevent",
                3: "Patient fully engaged in appropriate treatments but with inadequate response"
            },
            "psychological_risk": {
                1: "Serious personality dysfunction or mental illness interfering with care",
                2: "Personality or mental health interferes moderately",
                3: "Good communication with clinic, no significant personality dysfunction"
            },
            "chemical_health_risk": {
                1: "Active or very recent use of illicit drugs, excessive alcohol, or prescription drug abuse",
                2: "Chemical coper or history of chemical dependence in remission",
                3: "No CD history, not drug-focused or chemically reliant"
            },
            "reliability_risk": {
                1: "History of numerous problems (medication misuse, missed appointments)",
                2: "Occasional difficulties with compliance but generally reliable",
                3: "Highly reliable patient with meds, appointments, and treatment"
            },
            "social_support_risk": {
                1: "Life in chaos, little family support, few close relationships",
                2: "Reduction in some relationships and life roles",
                3: "Supportive family/close relationships, involved in work or school"
            }
        }
    
    def calculate(self, diagnosis: int, intractability: int, psychological_risk: int,
                  chemical_health_risk: int, reliability_risk: int, 
                  social_support_risk: int) -> Dict[str, Any]:
        """
        Calculates the DIRE score
        
        Args:
            diagnosis (int): Diagnosis category (1-3 points)
            intractability (int): Treatment response (1-3 points)
            psychological_risk (int): Psychological risk factors (1-3 points)
            chemical_health_risk (int): Chemical dependency risk (1-3 points)
            reliability_risk (int): Reliability with treatment (1-3 points)
            social_support_risk (int): Social support system (1-3 points)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(diagnosis, intractability, psychological_risk,
                             chemical_health_risk, reliability_risk, social_support_risk)
        
        # Calculate total score
        score = (diagnosis + intractability + psychological_risk + 
                chemical_health_risk + reliability_risk + social_support_risk)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, diagnosis: int, intractability: int, 
                        psychological_risk: int, chemical_health_risk: int,
                        reliability_risk: int, social_support_risk: int):
        """Validates input parameters"""
        
        parameters = {
            "diagnosis": diagnosis,
            "intractability": intractability,
            "psychological_risk": psychological_risk,
            "chemical_health_risk": chemical_health_risk,
            "reliability_risk": reliability_risk,
            "social_support_risk": social_support_risk
        }
        
        for param_name, param_value in parameters.items():
            if not isinstance(param_value, int):
                raise ValueError(f"{param_name} must be an integer")
            
            if param_value not in [1, 2, 3]:
                raise ValueError(f"{param_name} must be 1, 2, or 3")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Total DIRE score (7-21)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 13:
            return {
                "stage": "Not suitable",
                "description": "Not a suitable candidate",
                "interpretation": "Not a suitable candidate for long-term opioid analgesia. Consider alternative pain management strategies, address psychological/social issues, and consider addiction medicine consultation if substance use concerns."
            }
        else:  # score >= 14
            return {
                "stage": "Good candidate",
                "description": "Good candidate",
                "interpretation": "Good candidate for long-term opioid analgesia. May proceed with opioid therapy with appropriate monitoring, treatment agreement, and regular follow-up."
            }


def calculate_dire_score(diagnosis: int, intractability: int, psychological_risk: int,
                        chemical_health_risk: int, reliability_risk: int,
                        social_support_risk: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DireScoreCalculator()
    return calculator.calculate(diagnosis, intractability, psychological_risk,
                               chemical_health_risk, reliability_risk,
                               social_support_risk)