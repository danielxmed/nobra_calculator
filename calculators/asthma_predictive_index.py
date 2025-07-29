"""
Asthma Predictive Index (API) Calculator

Determines likelihood of pediatric patients developing childhood asthma in children 
≤3 years old with recurrent wheezing episodes.

References:
1. Castro-Rodríguez JA, Holberg CJ, Wright AL, Martinez FD. A clinical index to define 
   risk of asthma in young children with recurrent wheezing. Am J Respir Crit Care Med. 
   2000;162(4 Pt 1):1403-6.
2. Leonardi NA, Spycher BD, Strippoli MP, Frey U, Silverman M, Kuehni CE. Validation of 
   the Asthma Predictive Index and comparison with simpler clinical prediction rules. 
   J Allergy Clin Immunol. 2011;127(6):1466-72.e6.
"""

from typing import Dict, Any


class AsthmaStrictiveIndexCalculator:
    """Calculator for Asthma Predictive Index (API)"""
    
    def __init__(self):
        # Major criteria
        self.MAJOR_CRITERIA = ['family_history_asthma', 'eczema_diagnosis']
        
        # Minor criteria  
        self.MINOR_CRITERIA = [
            'air_allergen_sensitivity', 
            'wheezing_apart_from_colds', 
            'eosinophils_over_4_percent'
        ]
    
    def calculate(self, wheezing_episodes: str, family_history_asthma: str, 
                 eczema_diagnosis: str, air_allergen_sensitivity: str,
                 wheezing_apart_from_colds: str, eosinophils_over_4_percent: str) -> Dict[str, Any]:
        """
        Calculates the Asthma Predictive Index using the provided parameters
        
        Args:
            wheezing_episodes (str): Number of wheezing episodes per year ('less_than_3' or '3_or_more')
            family_history_asthma (str): Family history (parent) with asthma ('yes' or 'no')
            eczema_diagnosis (str): Patient diagnosed with eczema ('yes' or 'no')
            air_allergen_sensitivity (str): Sensitivity to air allergens ('yes' or 'no')
            wheezing_apart_from_colds (str): Wheezing apart from colds ('yes' or 'no')
            eosinophils_over_4_percent (str): >4% blood eosinophils ('yes' or 'no')
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(wheezing_episodes, family_history_asthma, eczema_diagnosis,
                            air_allergen_sensitivity, wheezing_apart_from_colds, 
                            eosinophils_over_4_percent)
        
        # Count major and minor criteria
        major_count = self._count_major_criteria(family_history_asthma, eczema_diagnosis)
        minor_count = self._count_minor_criteria(air_allergen_sensitivity, 
                                               wheezing_apart_from_colds,
                                               eosinophils_over_4_percent)
        
        # Determine API result
        api_result = self._determine_api_result(wheezing_episodes, major_count, minor_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(api_result)
        
        return {
            "result": api_result,
            "unit": "classification",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, wheezing_episodes, family_history_asthma, eczema_diagnosis,
                        air_allergen_sensitivity, wheezing_apart_from_colds, 
                        eosinophils_over_4_percent):
        """Validates input parameters"""
        
        valid_episodes = ["less_than_3", "3_or_more"]
        valid_yes_no = ["yes", "no"]
        
        if wheezing_episodes not in valid_episodes:
            raise ValueError(f"wheezing_episodes must be one of {valid_episodes}")
        
        for param, name in [
            (family_history_asthma, "family_history_asthma"),
            (eczema_diagnosis, "eczema_diagnosis"),
            (air_allergen_sensitivity, "air_allergen_sensitivity"),
            (wheezing_apart_from_colds, "wheezing_apart_from_colds"),
            (eosinophils_over_4_percent, "eosinophils_over_4_percent")
        ]:
            if param not in valid_yes_no:
                raise ValueError(f"{name} must be 'yes' or 'no'")
    
    def _count_major_criteria(self, family_history_asthma: str, eczema_diagnosis: str) -> int:
        """Counts positive major criteria"""
        count = 0
        if family_history_asthma == "yes":
            count += 1
        if eczema_diagnosis == "yes":
            count += 1
        return count
    
    def _count_minor_criteria(self, air_allergen_sensitivity: str, 
                            wheezing_apart_from_colds: str,
                            eosinophils_over_4_percent: str) -> int:
        """Counts positive minor criteria"""
        count = 0
        if air_allergen_sensitivity == "yes":
            count += 1
        if wheezing_apart_from_colds == "yes":
            count += 1
        if eosinophils_over_4_percent == "yes":
            count += 1
        return count
    
    def _determine_api_result(self, wheezing_episodes: str, major_count: int, 
                            minor_count: int) -> str:
        """
        Determines API result based on wheezing episodes and criteria counts
        
        Args:
            wheezing_episodes (str): Number of wheezing episodes per year
            major_count (int): Number of positive major criteria
            minor_count (int): Number of positive minor criteria
            
        Returns:
            str: API classification result
        """
        
        # Check if criteria are met (1 major OR 2 minor)
        criteria_met = (major_count >= 1) or (minor_count >= 2)
        
        if not criteria_met:
            return "Negative"
        
        # If criteria are met, determine stringent vs loose based on wheezing episodes
        if wheezing_episodes == "3_or_more":
            return "Positive Stringent"
        else:  # less_than_3
            return "Positive Loose"
    
    def _get_interpretation(self, api_result: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the API result
        
        Args:
            api_result (str): API classification result
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            "Positive Stringent": {
                "stage": "Positive Stringent",
                "description": "High risk for asthma development",
                "interpretation": "77% chance of diagnosed active asthma. Requires ≥3 wheezing episodes per year AND either 1 major criterion OR 2 minor criteria. Consider close monitoring and preventive measures."
            },
            "Positive Loose": {
                "stage": "Positive Loose", 
                "description": "Moderate risk for asthma development",
                "interpretation": "59% chance of diagnosed asthma. Requires <3 wheezing episodes per year AND either 1 major criterion OR 2 minor criteria. Consider monitoring and evaluation for asthma development."
            },
            "Negative": {
                "stage": "Negative",
                "description": "Low risk for asthma development",
                "interpretation": "Less than 3% chance of asthma diagnosis. Does not meet criteria for positive stringent or loose classification. Routine follow-up appropriate."
            }
        }
        
        return interpretations.get(api_result, interpretations["Negative"])


def calculate_asthma_predictive_index(wheezing_episodes, family_history_asthma, 
                                    eczema_diagnosis, air_allergen_sensitivity,
                                    wheezing_apart_from_colds, eosinophils_over_4_percent) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_asthma_predictive_index pattern
    """
    calculator = AsthmaStrictiveIndexCalculator()
    return calculator.calculate(wheezing_episodes, family_history_asthma, eczema_diagnosis,
                               air_allergen_sensitivity, wheezing_apart_from_colds, 
                               eosinophils_over_4_percent)
