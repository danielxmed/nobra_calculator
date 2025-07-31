"""
Disease Activity Score-28 for Rheumatoid Arthritis with ESR (DAS28-ESR) Calculator

Describes severity of rheumatoid arthritis using clinical and laboratory data, specifically ESR.

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


class Das28EsrCalculator:
    """Calculator for Disease Activity Score-28 for Rheumatoid Arthritis with ESR"""
    
    def __init__(self):
        # DAS28-ESR formula coefficients
        self.TENDER_JOINT_COEFF = 0.56
        self.SWOLLEN_JOINT_COEFF = 0.28
        self.ESR_COEFF = 0.70
        self.GLOBAL_HEALTH_COEFF = 0.014
    
    def calculate(self, tender_joint_count: int, swollen_joint_count: int,
                  esr_level: int, patient_global_health: int) -> Dict[str, Any]:
        """
        Calculates the DAS28-ESR score
        
        Args:
            tender_joint_count (int): Number of tender joints (0-28)
            swollen_joint_count (int): Number of swollen joints (0-28)
            esr_level (int): Erythrocyte sedimentation rate in mm/hr
            patient_global_health (int): Patient global assessment (0-10 scale)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(tender_joint_count, swollen_joint_count, 
                             esr_level, patient_global_health)
        
        # Calculate DAS28-ESR score using the formula:
        # DAS28-ESR = 0.56*√(TJC) + 0.28*√(SJC) + 0.70*ln(ESR) + 0.014*GH*10
        score = (
            self.TENDER_JOINT_COEFF * math.sqrt(tender_joint_count) +
            self.SWOLLEN_JOINT_COEFF * math.sqrt(swollen_joint_count) +
            self.ESR_COEFF * math.log(esr_level) +
            self.GLOBAL_HEALTH_COEFF * patient_global_health * 10
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
                        esr_level: int, patient_global_health: int):
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
        
        # Validate ESR level
        if not isinstance(esr_level, int):
            raise ValueError("esr_level must be an integer")
        if esr_level < 1 or esr_level > 200:
            raise ValueError("esr_level must be between 1 and 200 mm/hr")
        
        # Validate patient global health
        if not isinstance(patient_global_health, int):
            raise ValueError("patient_global_health must be an integer")
        if patient_global_health < 0 or patient_global_health > 10:
            raise ValueError("patient_global_health must be between 0 and 10")
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (float): DAS28-ESR score
            
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


def calculate_das28_esr(tender_joint_count: int, swollen_joint_count: int,
                       esr_level: int, patient_global_health: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Das28EsrCalculator()
    return calculator.calculate(tender_joint_count, swollen_joint_count,
                               esr_level, patient_global_health)