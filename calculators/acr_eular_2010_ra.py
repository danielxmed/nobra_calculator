"""
ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria Calculator

Implements the 2010 ACR/EULAR classification criteria for rheumatoid arthritis
using joint involvement, serology, acute-phase reactants, and symptom duration.

References:
- Aletaha D, et al. 2010 Rheumatoid arthritis classification criteria: an American 
  College of Rheumatology/European League Against Rheumatism collaborative initiative. 
  Arthritis Rheum. 2010;62(9):2569-81.
"""

from typing import Dict, Any


class AcrEular2010RaCalculator:
    """Calculator for ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria"""
    
    def __init__(self):
        # Joint involvement scoring
        self.JOINT_SCORES = {
            "1_large": 0,
            "2_to_10_large": 1,
            "1_to_3_small": 2,
            "4_to_10_small": 3,
            "more_than_10_small": 5
        }
        
        # Serology scoring weights
        self.SEROLOGY_SCORES = {
            "negative": 0,
            "low_positive": 2,
            "high_positive": 3
        }
        
        # Acute-phase reactant scoring
        self.APR_SCORES = {
            "normal": 0,
            "abnormal": 1
        }
        
        # Duration scoring
        self.DURATION_SCORES = {
            "less_than_6_weeks": 0,
            "6_weeks_or_more": 1
        }
    
    def calculate(self, joint_involvement: str, rf_status: str, acpa_status: str,
                  crp_status: str, esr_status: str, symptom_duration: str) -> Dict[str, Any]:
        """
        Calculates the ACR/EULAR 2010 RA classification score
        
        Args:
            joint_involvement (str): Joint involvement pattern
            rf_status (str): Rheumatoid factor status (negative/low_positive/high_positive)
            acpa_status (str): ACPA status (negative/low_positive/high_positive)
            crp_status (str): CRP status (normal/abnormal)
            esr_status (str): ESR status (normal/abnormal)
            symptom_duration (str): Duration of symptoms (less_than_6_weeks/6_weeks_or_more)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(joint_involvement, rf_status, acpa_status, 
                            crp_status, esr_status, symptom_duration)
        
        # Calculate component scores
        joint_score = self._calculate_joint_score(joint_involvement)
        serology_score = self._calculate_serology_score(rf_status, acpa_status)
        apr_score = self._calculate_apr_score(crp_status, esr_status)
        duration_score = self._calculate_duration_score(symptom_duration)
        
        # Calculate total score
        total_score = joint_score + serology_score + apr_score + duration_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, joint_involvement, rf_status, acpa_status,
                        crp_status, esr_status, symptom_duration):
        """Validates input parameters"""
        
        if joint_involvement not in self.JOINT_SCORES:
            raise ValueError(f"Invalid joint_involvement: {joint_involvement}")
        
        if rf_status not in self.SEROLOGY_SCORES:
            raise ValueError(f"Invalid rf_status: {rf_status}")
        
        if acpa_status not in self.SEROLOGY_SCORES:
            raise ValueError(f"Invalid acpa_status: {acpa_status}")
        
        if crp_status not in ["normal", "abnormal"]:
            raise ValueError(f"Invalid crp_status: {crp_status}")
        
        if esr_status not in ["normal", "abnormal"]:
            raise ValueError(f"Invalid esr_status: {esr_status}")
        
        if symptom_duration not in self.DURATION_SCORES:
            raise ValueError(f"Invalid symptom_duration: {symptom_duration}")
    
    def _calculate_joint_score(self, joint_involvement: str) -> int:
        """Calculates the joint involvement score"""
        return self.JOINT_SCORES[joint_involvement]
    
    def _calculate_serology_score(self, rf_status: str, acpa_status: str) -> int:
        """
        Calculates the serology score based on RF and ACPA status
        
        Uses the higher of the two serology scores as per ACR/EULAR criteria
        """
        rf_score = self.SEROLOGY_SCORES[rf_status]
        acpa_score = self.SEROLOGY_SCORES[acpa_status]
        
        # Return the higher score (as per original criteria)
        return max(rf_score, acpa_score)
    
    def _calculate_apr_score(self, crp_status: str, esr_status: str) -> int:
        """
        Calculates the acute-phase reactant score
        
        Score is 1 if either CRP or ESR is abnormal, 0 if both are normal
        """
        if crp_status == "abnormal" or esr_status == "abnormal":
            return 1
        return 0
    
    def _calculate_duration_score(self, symptom_duration: str) -> int:
        """Calculates the symptom duration score"""
        return self.DURATION_SCORES[symptom_duration]
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Total calculated score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score >= 6:
            return {
                "stage": "Definite RA",
                "description": "Meets classification criteria",
                "interpretation": f"Score {total_score}/10 points. Meets ACR/EULAR 2010 classification criteria for rheumatoid arthritis. Consider early DMARD therapy initiation."
            }
        else:
            return {
                "stage": "Non-RA",
                "description": "Does not meet criteria",
                "interpretation": f"Score {total_score}/10 points. Does not meet criteria for rheumatoid arthritis classification. Consider other diagnoses or continued monitoring."
            }


def calculate_acr_eular_2010_ra(joint_involvement: str, rf_status: str, acpa_status: str,
                               crp_status: str, esr_status: str, symptom_duration: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AcrEular2010RaCalculator()
    return calculator.calculate(joint_involvement, rf_status, acpa_status,
                               crp_status, esr_status, symptom_duration)