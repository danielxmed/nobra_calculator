"""
qSOFA (Quick SOFA) Score for Sepsis Calculator

Identifies high-risk patients for in-hospital mortality with suspected infection outside 
the ICU. This simplified bedside assessment tool helps rapidly identify patients at 
greater risk for poor outcomes and guides clinical decision-making in sepsis management.

References:
1. Seymour CW, Liu VX, Iwashyna TJ, Brunkhorst FM, Rea TD, Scherag A, et al. 
   Assessment of Clinical Criteria for Sepsis: For the Third International Consensus 
   Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016 Feb 23;315(8):762-74. 
   doi: 10.1001/jama.2016.0288.
2. Singer M, Deutschman CS, Seymour CW, Shankar-Hari M, Annane D, Bauer M, et al. 
   The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). 
   JAMA. 2016 Feb 23;315(8):801-10. doi: 10.1001/jama.2016.0287.
"""

from typing import Dict, Any


class QsofaScoreCalculator:
    """Calculator for qSOFA (Quick SOFA) Score for Sepsis"""
    
    def __init__(self):
        # qSOFA scoring points (each criterion = 1 point)
        self.CRITERION_POINTS = 1
        
        # Risk threshold
        self.HIGH_RISK_THRESHOLD = 2
    
    def calculate(self, respiratory_rate_22_or_higher: str, altered_mental_status: str, 
                 systolic_bp_100_or_lower: str) -> Dict[str, Any]:
        """
        Calculates qSOFA score for sepsis mortality risk assessment
        
        Args:
            respiratory_rate_22_or_higher (str): Respiratory rate ≥22/min ('yes' or 'no')
            altered_mental_status (str): Altered mental status GCS <15 ('yes' or 'no')
            systolic_bp_100_or_lower (str): Systolic BP ≤100 mmHg ('yes' or 'no')
            
        Returns:
            Dict with qSOFA score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(respiratory_rate_22_or_higher, altered_mental_status, 
                             systolic_bp_100_or_lower)
        
        # Calculate total qSOFA score
        total_score = self._calculate_total_score(respiratory_rate_22_or_higher, 
                                                 altered_mental_status, 
                                                 systolic_bp_100_or_lower)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, respiratory_rate_22_or_higher: str, altered_mental_status: str,
                        systolic_bp_100_or_lower: str):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = [
            (respiratory_rate_22_or_higher, "respiratory_rate_22_or_higher"),
            (altered_mental_status, "altered_mental_status"),
            (systolic_bp_100_or_lower, "systolic_bp_100_or_lower")
        ]
        
        for param, name in yes_no_params:
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, respiratory_rate_22_or_higher: str, 
                              altered_mental_status: str, systolic_bp_100_or_lower: str) -> int:
        """Calculates the total qSOFA score"""
        
        score = 0
        
        # Add 1 point for each present criterion
        if respiratory_rate_22_or_higher == "yes":
            score += self.CRITERION_POINTS
            
        if altered_mental_status == "yes":
            score += self.CRITERION_POINTS
            
        if systolic_bp_100_or_lower == "yes":
            score += self.CRITERION_POINTS
            
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on qSOFA score
        
        Args:
            score (int): Calculated qSOFA score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score < self.HIGH_RISK_THRESHOLD:  # 0-1 points
            return {
                "stage": "Low Risk",
                "description": "Low mortality risk",
                "interpretation": "qSOFA score <2. Lower risk for poor outcomes associated with sepsis. Continue standard infection management and monitoring. Consider obtaining full SOFA score with laboratory results if clinical suspicion remains high for sepsis. Monitor closely for clinical deterioration and reassess qSOFA if patient condition changes."
            }
        else:  # 2-3 points
            return {
                "stage": "High Risk",
                "description": "High mortality risk",
                "interpretation": "qSOFA score ≥2. Significantly increased risk for in-hospital mortality (3- to 14-fold increase). Strongly suggests sepsis and requires immediate aggressive management. Consider ICU evaluation, obtain blood cultures before antibiotics, initiate broad-spectrum antibiotics within 1 hour, implement sepsis bundle protocols including fluid resuscitation and vasopressor support if needed."
            }


def calculate_qsofa_score(respiratory_rate_22_or_higher: str, altered_mental_status: str,
                         systolic_bp_100_or_lower: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = QsofaScoreCalculator()
    return calculator.calculate(respiratory_rate_22_or_higher, altered_mental_status,
                               systolic_bp_100_or_lower)