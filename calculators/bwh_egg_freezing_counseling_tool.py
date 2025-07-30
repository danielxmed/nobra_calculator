"""
BWH Egg Freezing Counseling Tool (EFCT) Calculator

Predicts likelihood of live birth for elective egg freezing in women based on age and number of mature eggs.

References:
1. Goldman RH, Racowsky C, Farland LV, Munné S, Ribustello L, Fox JH. Predicting the likelihood 
   of live birth for elective oocyte cryopreservation: a counseling tool for physicians and 
   patients. Hum Reprod. 2017 Apr 1;32(4):853-859. doi: 10.1093/humrep/dex008.
"""

import math
from typing import Dict, Any


class BwhEggFreezingCounselingToolCalculator:
    """Calculator for BWH Egg Freezing Counseling Tool (EFCT)"""
    
    def __init__(self):
        # Age-specific probabilities of euploid embryos
        self.euploid_probabilities = {
            24: 0.647,  # Egg donor rate used for ages 24-26
            25: 0.647,
            26: 0.647,
            27: 0.626,
            28: 0.604,
            29: 0.583,
            30: 0.561,
            31: 0.540,
            32: 0.518,
            33: 0.497,
            34: 0.475,
            35: 0.454,
            36: 0.432,
            37: 0.411,
            38: 0.389,
            39: 0.368,
            40: 0.346,
            41: 0.325,
            42: 0.303,
            43: 0.282,
            44: 0.260,
            # 44+ uses exponential decay: 0.238 * exp(-0.078 * (age - 44))
        }
        
        # Constants for live birth calculation
        self.LIVE_BIRTH_RATE_PER_EUPLOID_BLAST = 0.6
    
    def calculate(self, age: int, number_of_mature_eggs: int) -> Dict[str, Any]:
        """
        Calculates the probability of live births using the BWH EFCT formula
        
        Args:
            age (int): Woman's age at time of egg freezing (24-44 years)
            number_of_mature_eggs (int): Number of mature eggs retrieved (1-100)
            
        Returns:
            Dict with probabilities for 1, 2, and 3 live births
        """
        
        # Validate inputs
        self._validate_inputs(age, number_of_mature_eggs)
        
        # Calculate probability of blastocyst formation
        p_blast = self._calculate_blast_probability(age)
        
        # Get probability of euploid embryo
        p_euploid = self._get_euploid_probability(age)
        
        # Calculate probability of live birth per egg
        p_live_birth_per_egg = self.LIVE_BIRTH_RATE_PER_EUPLOID_BLAST * p_euploid * p_blast
        
        # Calculate probabilities for different numbers of live births
        prob_at_least_one = 1 - math.pow(1 - p_live_birth_per_egg, number_of_mature_eggs)
        prob_at_least_two = self._calculate_multiple_births(p_live_birth_per_egg, number_of_mature_eggs, 2)
        prob_at_least_three = self._calculate_multiple_births(p_live_birth_per_egg, number_of_mature_eggs, 3)
        
        # Get interpretation based on probability of at least one live birth
        interpretation = self._get_interpretation(prob_at_least_one)
        
        return {
            "result": {
                "at_least_one_live_birth": round(prob_at_least_one, 3),
                "at_least_two_live_births": round(prob_at_least_two, 3),
                "at_least_three_live_births": round(prob_at_least_three, 3)
            },
            "unit": "probability",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "p_blast": round(p_blast, 3),
                "p_euploid": round(p_euploid, 3),
                "p_live_birth_per_egg": round(p_live_birth_per_egg, 3),
                "age": age,
                "number_of_eggs": number_of_mature_eggs
            }
        }
    
    def _validate_inputs(self, age: int, number_of_mature_eggs: int):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 24 or age > 44:
            raise ValueError("Age must be between 24 and 44 years")
        
        if not isinstance(number_of_mature_eggs, int):
            raise ValueError("Number of mature eggs must be an integer")
        
        if number_of_mature_eggs < 1 or number_of_mature_eggs > 100:
            raise ValueError("Number of mature eggs must be between 1 and 100")
    
    def _calculate_blast_probability(self, age: int) -> float:
        """
        Calculates probability of blastocyst formation based on age
        
        Formula varies by age:
        - Age < 36: 0.95 * exp(2.8043 - 0.1112 * age)
        - Age >= 36: 0.85 * exp(2.8043 - 0.1112 * age)
        """
        
        base_prob = math.exp(2.8043 - 0.1112 * age)
        
        if age < 36:
            return 0.95 * base_prob
        else:
            return 0.85 * base_prob
    
    def _get_euploid_probability(self, age: int) -> float:
        """
        Gets probability of euploid embryo based on age
        
        Uses lookup table for ages 24-44, exponential decay for ages > 44
        """
        
        if age <= 44:
            return self.euploid_probabilities.get(age, self.euploid_probabilities[44])
        else:
            # For ages > 44, use exponential decay (though input validation prevents this)
            return 0.238 * math.exp(-0.078 * (age - 44))
    
    def _calculate_multiple_births(self, p_per_egg: float, n_eggs: int, n_births: int) -> float:
        """
        Calculates probability of at least n births using binomial probability
        
        P(at least n births) = 1 - P(fewer than n births)
        """
        
        if n_births > n_eggs:
            return 0.0
        
        # Calculate cumulative probability of fewer than n births
        prob_fewer = 0.0
        for k in range(n_births):
            prob_fewer += self._binomial_probability(n_eggs, k, p_per_egg)
        
        return 1 - prob_fewer
    
    def _binomial_probability(self, n: int, k: int, p: float) -> float:
        """
        Calculates binomial probability P(X = k) for n trials with probability p
        """
        
        if k > n:
            return 0.0
        
        # Calculate binomial coefficient
        coeff = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))
        
        # Calculate probability
        return coeff * math.pow(p, k) * math.pow(1 - p, n - k)
    
    def _get_interpretation(self, probability: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the probability of at least one live birth
        
        Args:
            probability (float): Probability of at least one live birth
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if probability < 0.1:
            return {
                "stage": "Very Low",
                "description": "Very low probability of live birth",
                "interpretation": f"With a {probability*100:.1f}% chance of at least one live birth, the probability is very low. Consider additional egg freezing cycles or alternative family-building options. Each additional cycle can significantly improve cumulative success rates, particularly for younger women."
            }
        elif probability < 0.3:
            return {
                "stage": "Low",
                "description": "Low probability of live birth",
                "interpretation": f"With a {probability*100:.1f}% chance of at least one live birth, the probability is low. Additional egg freezing cycles would substantially improve the chances of success. Consider discussing the potential benefits and costs of additional cycles with your physician."
            }
        elif probability < 0.5:
            return {
                "stage": "Moderate",
                "description": "Moderate probability of live birth",
                "interpretation": f"With a {probability*100:.1f}% chance of at least one live birth, there is a moderate probability of success. While not guaranteed, these odds represent a reasonable chance. You may wish to consider whether additional cycles would be beneficial based on your personal goals."
            }
        elif probability < 0.7:
            return {
                "stage": "Good",
                "description": "Good probability of live birth",
                "interpretation": f"With a {probability*100:.1f}% chance of at least one live birth, the probability of success is good. These are favorable odds, though additional eggs could further improve your chances if you desire multiple children or want additional reassurance."
            }
        else:
            return {
                "stage": "Excellent",
                "description": "Excellent probability of live birth",
                "interpretation": f"With a {probability*100:.1f}% chance of at least one live birth, the probability of success is excellent. This represents very favorable odds for achieving pregnancy through your frozen eggs. The current egg count provides strong reassurance for future family building."
            }


def calculate_bwh_egg_freezing_counseling_tool(age: int, number_of_mature_eggs: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BwhEggFreezingCounselingToolCalculator()
    return calculator.calculate(age, number_of_mature_eggs)