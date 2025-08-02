"""
HIV Incidence Risk Index for MSM (HIRI-MSM) Calculator

Identifies MSM at high risk for HIV infection for PrEP prioritization.

References:
- Smith DK, et al. J Acquir Immune Defic Syndr. 2012;60(4):421-7.
- Wilton J, et al. BMC Public Health. 2018;18(1):292.
"""

from typing import Dict, Any


class HiriMsmCalculator:
    """Calculator for HIV Incidence Risk Index for MSM (HIRI-MSM)"""
    
    def __init__(self):
        # Age scoring points
        self.age_points = {
            "<18": 0,
            "18-28": 8,
            "29-40": 5,
            "41-48": 2,
            ">=49": 0
        }
        
        # Number of male partners points
        self.partners_points = {
            "0_to_5": 0,
            "6_to_10": 4,
            "more_than_10": 7
        }
        
        # Receptive anal sex without condom points
        self.receptive_anal_points = {
            "no": 0,
            "yes": 10
        }
        
        # HIV-positive partners points
        self.hiv_positive_partners_points = {
            "none": 0,
            "one": 4,
            "more_than_one": 8
        }
        
        # Insertive anal sex with HIV-positive partner points
        self.insertive_anal_points = {
            "0_to_4_times": 0,
            "5_or_more_times": 6
        }
        
        # Methamphetamine use points
        self.meth_points = {
            "no": 0,
            "yes": 5
        }
        
        # Poppers use points
        self.poppers_points = {
            "no": 0,
            "yes": 3
        }
    
    def calculate(self, age: int, num_male_partners: str, receptive_anal_no_condom: str,
                  num_hiv_positive_partners: str, insertive_anal_hiv_positive: str,
                  methamphetamine_use: str, poppers_use: str) -> Dict[str, Any]:
        """
        Calculates the HIRI-MSM score
        
        Args:
            age (int): Patient age in years
            num_male_partners (str): Number of male partners in last 6 months
            receptive_anal_no_condom (str): Receptive anal sex without condom
            num_hiv_positive_partners (str): Number of HIV-positive partners
            insertive_anal_hiv_positive (str): Insertive anal sex with HIV-positive
            methamphetamine_use (str): Methamphetamine use in last 6 months
            poppers_use (str): Poppers use in last 6 months
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, num_male_partners, receptive_anal_no_condom,
                            num_hiv_positive_partners, insertive_anal_hiv_positive,
                            methamphetamine_use, poppers_use)
        
        # Calculate age category
        age_category = self._get_age_category(age)
        
        # Calculate total score
        total_score = 0
        
        # Add points for each factor
        total_score += self.age_points[age_category]
        total_score += self.partners_points[num_male_partners]
        total_score += self.receptive_anal_points[receptive_anal_no_condom]
        total_score += self.hiv_positive_partners_points[num_hiv_positive_partners]
        total_score += self.insertive_anal_points[insertive_anal_hiv_positive]
        total_score += self.meth_points[methamphetamine_use]
        total_score += self.poppers_points[poppers_use]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, num_male_partners: str, receptive_anal_no_condom: str,
                        num_hiv_positive_partners: str, insertive_anal_hiv_positive: str,
                        methamphetamine_use: str, poppers_use: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120")
        
        if num_male_partners not in self.partners_points:
            raise ValueError(f"Invalid num_male_partners: {num_male_partners}")
        
        if receptive_anal_no_condom not in self.receptive_anal_points:
            raise ValueError(f"Invalid receptive_anal_no_condom: {receptive_anal_no_condom}")
        
        if num_hiv_positive_partners not in self.hiv_positive_partners_points:
            raise ValueError(f"Invalid num_hiv_positive_partners: {num_hiv_positive_partners}")
        
        if insertive_anal_hiv_positive not in self.insertive_anal_points:
            raise ValueError(f"Invalid insertive_anal_hiv_positive: {insertive_anal_hiv_positive}")
        
        if methamphetamine_use not in self.meth_points:
            raise ValueError(f"Invalid methamphetamine_use: {methamphetamine_use}")
        
        if poppers_use not in self.poppers_points:
            raise ValueError(f"Invalid poppers_use: {poppers_use}")
    
    def _get_age_category(self, age: int) -> str:
        """Determines age category for scoring"""
        if age < 18:
            return "<18"
        elif age <= 28:
            return "18-28"
        elif age <= 40:
            return "29-40"
        elif age <= 48:
            return "41-48"
        else:
            return ">=49"
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated HIRI-MSM score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 10:
            return {
                "stage": "Low Risk",
                "description": "Score <10",
                "interpretation": "Low HIV risk. Standard HIV prevention counseling recommended. "
                                "Continue routine HIV testing and safer sex practices."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Score ≥10",
                "interpretation": "High HIV risk. This score has 84% sensitivity and 45% specificity "
                                "for predicting incident HIV infection in the next 6 months. "
                                "Strongly consider pre-exposure prophylaxis (PrEP) and intensive "
                                "HIV prevention interventions. Discuss risk reduction strategies "
                                "and increase HIV testing frequency."
            }


def calculate_hiri_msm(age: int, num_male_partners: str, receptive_anal_no_condom: str,
                       num_hiv_positive_partners: str, insertive_anal_hiv_positive: str,
                       methamphetamine_use: str, poppers_use: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HiriMsmCalculator()
    return calculator.calculate(age, num_male_partners, receptive_anal_no_condom,
                              num_hiv_positive_partners, insertive_anal_hiv_positive,
                              methamphetamine_use, poppers_use)