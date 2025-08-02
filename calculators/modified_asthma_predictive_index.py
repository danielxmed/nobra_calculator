"""
Modified Asthma Predictive Index (mAPI) Calculator

Predicts future asthma onset probability in pediatric patients ≤3 years old 
with recurrent wheezing episodes.

References:
1. Guilbert TW, et al. N Engl J Med. 2006;354(19):1985-97.
2. Chang TS, et al. J Allergy Clin Immunol Pract. 2013;1(2):152-6.
3. Castro-Rodríguez JA, et al. Am J Respir Crit Care Med. 2000;162(4):1403-6.
"""

from typing import Dict, Any


class ModifiedAsthmaPredictiveIndexCalculator:
    """Calculator for Modified Asthma Predictive Index (mAPI)"""
    
    def __init__(self):
        # mAPI criteria definitions
        self.MIN_WHEEZING_EPISODES = 4
        
    def calculate(self, wheezing_episodes_per_year: int, parent_asthma: str,
                  atopic_dermatitis: str, aeroallergen_sensitivity: str,
                  wheezing_unrelated_colds: str, eosinophils_4_percent: str,
                  food_allergies: str) -> Dict[str, Any]:
        """
        Calculates the Modified Asthma Predictive Index (mAPI)
        
        Args:
            wheezing_episodes_per_year (int): Number of wheezing episodes per year
            parent_asthma (str): Parent has asthma ("yes" or "no")
            atopic_dermatitis (str): Patient has atopic dermatitis ("yes" or "no")
            aeroallergen_sensitivity (str): Patient has aeroallergen sensitivity ("yes" or "no")
            wheezing_unrelated_colds (str): Wheezing unrelated to colds ("yes" or "no")
            eosinophils_4_percent (str): Eosinophils ≥4% on CBC ("yes" or "no")
            food_allergies (str): Allergy to milk, egg, or peanuts ("yes" or "no")
            
        Returns:
            Dict with mAPI result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(wheezing_episodes_per_year, parent_asthma, atopic_dermatitis,
                            aeroallergen_sensitivity, wheezing_unrelated_colds, 
                            eosinophils_4_percent, food_allergies)
        
        # Check if mAPI is applicable (≥4 wheezing episodes per year)
        if wheezing_episodes_per_year < self.MIN_WHEEZING_EPISODES:
            return {
                "result": "Not Applicable",
                "unit": "result",
                "interpretation": (f"mAPI is not applicable. Patient has {wheezing_episodes_per_year} "
                                 f"wheezing episodes per year, but ≥{self.MIN_WHEEZING_EPISODES} episodes "
                                 "are required for mAPI evaluation. Consider monitoring and reassessment."),
                "stage": "Not Applicable",
                "stage_description": "Insufficient wheezing episodes"
            }
        
        # Calculate major criteria score
        major_criteria_score = self._calculate_major_criteria(
            parent_asthma, atopic_dermatitis, aeroallergen_sensitivity
        )
        
        # Calculate minor criteria score
        minor_criteria_score = self._calculate_minor_criteria(
            wheezing_unrelated_colds, eosinophils_4_percent, food_allergies
        )
        
        # Determine mAPI result
        is_positive = self._is_mapi_positive(major_criteria_score, minor_criteria_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(is_positive, major_criteria_score, 
                                               minor_criteria_score, wheezing_episodes_per_year)
        
        return {
            "result": "Positive" if is_positive else "Negative",
            "unit": "result",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, wheezing_episodes_per_year: int, parent_asthma: str,
                        atopic_dermatitis: str, aeroallergen_sensitivity: str,
                        wheezing_unrelated_colds: str, eosinophils_4_percent: str,
                        food_allergies: str):
        """Validates input parameters"""
        
        # Validate wheezing episodes
        if not isinstance(wheezing_episodes_per_year, int):
            raise ValueError("wheezing_episodes_per_year must be an integer")
        if wheezing_episodes_per_year < 0 or wheezing_episodes_per_year > 50:
            raise ValueError("wheezing_episodes_per_year must be between 0 and 50")
        
        # Validate yes/no responses
        yes_no_params = [
            ("parent_asthma", parent_asthma),
            ("atopic_dermatitis", atopic_dermatitis),
            ("aeroallergen_sensitivity", aeroallergen_sensitivity),
            ("wheezing_unrelated_colds", wheezing_unrelated_colds),
            ("eosinophils_4_percent", eosinophils_4_percent),
            ("food_allergies", food_allergies)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_major_criteria(self, parent_asthma: str, atopic_dermatitis: str,
                                aeroallergen_sensitivity: str) -> int:
        """Calculates major criteria score"""
        
        score = 0
        if parent_asthma == "yes":
            score += 1
        if atopic_dermatitis == "yes":
            score += 1
        if aeroallergen_sensitivity == "yes":
            score += 1
        
        return score
    
    def _calculate_minor_criteria(self, wheezing_unrelated_colds: str,
                                eosinophils_4_percent: str, food_allergies: str) -> int:
        """Calculates minor criteria score"""
        
        score = 0
        if wheezing_unrelated_colds == "yes":
            score += 1
        if eosinophils_4_percent == "yes":
            score += 1
        if food_allergies == "yes":
            score += 1
        
        return score
    
    def _is_mapi_positive(self, major_criteria_score: int, minor_criteria_score: int) -> bool:
        """
        Determines if mAPI is positive
        
        mAPI is positive if:
        - ≥1 major criteria OR ≥2 minor criteria
        """
        return major_criteria_score >= 1 or minor_criteria_score >= 2
    
    def _get_interpretation(self, is_positive: bool, major_criteria_score: int,
                          minor_criteria_score: int, wheezing_episodes: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mAPI result
        
        Args:
            is_positive: Whether mAPI is positive
            major_criteria_score: Number of major criteria present
            minor_criteria_score: Number of minor criteria present
            wheezing_episodes: Number of wheezing episodes per year
            
        Returns:
            Dict with interpretation details
        """
        
        if is_positive:
            return {
                "stage": "Positive mAPI",
                "description": "Increased asthma risk",
                "interpretation": (f"mAPI is POSITIVE. Patient has {wheezing_episodes} wheezing episodes "
                                 f"per year with {major_criteria_score} major criteria and "
                                 f"{minor_criteria_score} minor criteria present. This indicates an "
                                 "increased risk of future asthma development. Consider close monitoring, "
                                 "environmental control measures, and discussion with pediatric pulmonologist "
                                 "or allergist. Note: mAPI has high specificity (98-100%) but variable "
                                 "sensitivity (8.2-19%), and does not guarantee future asthma diagnosis.")
            }
        else:
            return {
                "stage": "Negative mAPI",
                "description": "Lower asthma risk",
                "interpretation": (f"mAPI is NEGATIVE. Patient has {wheezing_episodes} wheezing episodes "
                                 f"per year with {major_criteria_score} major criteria and "
                                 f"{minor_criteria_score} minor criteria present. This indicates a lower "
                                 "risk of future asthma development. Continue routine monitoring and "
                                 "reassess if clinical picture changes. Standard supportive care for "
                                 "acute wheezing episodes as appropriate.")
            }


def calculate_modified_asthma_predictive_index(wheezing_episodes_per_year: int,
                                             parent_asthma: str, atopic_dermatitis: str,
                                             aeroallergen_sensitivity: str,
                                             wheezing_unrelated_colds: str,
                                             eosinophils_4_percent: str,
                                             food_allergies: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedAsthmaPredictiveIndexCalculator()
    return calculator.calculate(wheezing_episodes_per_year, parent_asthma, atopic_dermatitis,
                              aeroallergen_sensitivity, wheezing_unrelated_colds,
                              eosinophils_4_percent, food_allergies)