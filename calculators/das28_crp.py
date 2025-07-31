"""
Disease Activity Score-28 for Rheumatoid Arthritis with CRP (DAS28-CRP) Calculator

Describes severity of rheumatoid arthritis using clinical and laboratory data, specifically CRP.

References:
1. van der Heijde DM, van 't Hof MA, van Riel PL, et al. Judging disease activity in clinical 
   practice in rheumatoid arthritis: first step in the development of a disease activity score. 
   Ann Rheum Dis. 1990 Nov;49(11):916-20.
2. Prevoo ML, van 't Hof MA, Kuper HH, van Leeuwen MA, van de Putte LB, van Riel PL. 
   Modified disease activity scores that include twenty-eight-joint counts. Development and 
   validation in a prospective longitudinal study of patients with rheumatoid arthritis. 
   Arthritis Rheum. 1995 Jan;38(1):44-8.
"""

import math
from typing import Dict, Any


class Das28CrpCalculator:
    """Calculator for Disease Activity Score-28 for Rheumatoid Arthritis with CRP"""
    
    def __init__(self):
        # DAS28-CRP formula coefficients
        self.TENDER_JOINT_COEFF = 0.56
        self.SWOLLEN_JOINT_COEFF = 0.28
        self.CRP_COEFF = 0.36
        self.GLOBAL_HEALTH_COEFF = 0.014
        self.CONSTANT = 0.96
    
    def calculate(self, tender_joint_count: int, swollen_joint_count: int,
                  crp_level: float, patient_global_health: int) -> Dict[str, Any]:
        """
        Calculates the DAS28-CRP score
        
        Args:
            tender_joint_count (int): Number of tender joints (0-28)
            swollen_joint_count (int): Number of swollen joints (0-28)
            crp_level (float): C-reactive protein level in mg/L
            patient_global_health (int): Patient global assessment (0-10 scale)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(tender_joint_count, swollen_joint_count, 
                             crp_level, patient_global_health)
        
        # Calculate DAS28-CRP score using the formula:
        # DAS28-CRP = 0.56*√(TJC) + 0.28*√(SJC) + 0.36*ln(CRP+1) + 0.014*GH*10 + 0.96
        score = (
            self.TENDER_JOINT_COEFF * math.sqrt(tender_joint_count) +
            self.SWOLLEN_JOINT_COEFF * math.sqrt(swollen_joint_count) +
            self.CRP_COEFF * math.log(crp_level + 1) +
            self.GLOBAL_HEALTH_COEFF * patient_global_health * 10 +
            self.CONSTANT
        )
        
        # Round to 2 decimal places
        score = round(score, 2)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, tender_joint_count: int, swollen_joint_count: int,
                        crp_level: float, patient_global_health: int):
        """Validates input parameters"""
        
        # Validate tender joint count
        if not isinstance(tender_joint_count, int):
            raise ValueError("tender_joint_count must be an integer")
        if tender_joint_count < 0 or tender_joint_count > 28:
            raise ValueError("tender_joint_count must be between 0 and 28")
        
        # Validate swollen joint count
        if not isinstance(swollen_joint_count, int):
            raise ValueError("swollen_joint_count must be an integer")
        if swollen_joint_count < 0 or swollen_joint_count > 28:
            raise ValueError("swollen_joint_count must be between 0 and 28")
        
        # Validate CRP level
        if not isinstance(crp_level, (int, float)):
            raise ValueError("crp_level must be a number")
        if crp_level < 0 or crp_level > 300:
            raise ValueError("crp_level must be between 0 and 300 mg/L")
        
        # Validate patient global health
        if not isinstance(patient_global_health, int):
            raise ValueError("patient_global_health must be an integer")
        if patient_global_health < 0 or patient_global_health > 10:
            raise ValueError("patient_global_health must be between 0 and 10")
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (float): DAS28-CRP score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 2.6:
            return {
                "stage": "Remission",
                "description": "Disease remission",
                "interpretation": "Remission. Patient is in remission with minimal or no disease activity. Continue current therapy and monitor."
            }
        elif score < 3.2:
            return {
                "stage": "Low",
                "description": "Low disease activity",
                "interpretation": "Low disease activity. Current therapy is effective. Continue monitoring and may consider treatment optimization for remission target."
            }
        elif score <= 5.1:
            return {
                "stage": "Moderate",
                "description": "Moderate disease activity",
                "interpretation": "Moderate disease activity. Consider treatment intensification or modification. Reassess treatment strategy to achieve lower disease activity."
            }
        else:  # score > 5.1
            return {
                "stage": "High",
                "description": "High disease activity",
                "interpretation": "High disease activity. Treatment intensification or change is strongly recommended. Consider combination therapy or biologic agents."
            }


def calculate_das28_crp(tender_joint_count: int, swollen_joint_count: int,
                       crp_level: float, patient_global_health: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Das28CrpCalculator()
    return calculator.calculate(tender_joint_count, swollen_joint_count,
                               crp_level, patient_global_health)