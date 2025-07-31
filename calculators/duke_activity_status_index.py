"""
Duke Activity Status Index (DASI) Calculator

Estimates functional capacity of patients through self-reported activities. 
A 12-item questionnaire that assesses daily activities with respective metabolic 
costs to predict maximal oxygen consumption (VO2 max) and maximum metabolic 
equivalent of tasks (METs).

References:
1. Hlatky MA, Boineau RE, Higginbotham MB, Lee KL, Mark DB, Califf RM, et al. 
   A brief self-administered questionnaire to determine functional capacity 
   (the Duke Activity Status Index). Am J Cardiol. 1989;64(10):651-4.
2. Wijeysundera DN, Pearse RM, Shulman MA, Abbott TEF, Torres E, Ambosta A, et al. 
   Assessment of functional capacity before major non-cardiac surgery: an international, 
   prospective cohort study. Lancet. 2018;391(10140):2631-2640.
"""

from typing import Dict, Any
import math


class DukeActivityStatusIndexCalculator:
    """Calculator for Duke Activity Status Index (DASI)"""
    
    def __init__(self):
        # DASI scoring weights based on metabolic equivalent of tasks (METs)
        self.ACTIVITY_WEIGHTS = {
            'personal_care': 2.75,       # Taking care of yourself
            'walk_indoors': 1.75,        # Walking indoors
            'walk_1_2_blocks': 2.75,     # Walking a block or two on level ground
            'climb_stairs': 5.50,        # Climbing a flight of stairs or walking up a hill
            'run_short_distance': 8.00,  # Running a short distance
            'light_housework': 2.70,     # Light work around the house
            'moderate_housework': 3.50,  # Moderate work around the house
            'heavy_housework': 8.00,     # Heavy work around the house
            'yard_work': 4.50,           # Yard work
            'sexual_relations': 5.25,    # Sexual relations
            'moderate_recreation': 6.00, # Moderate recreational activities
            'strenuous_sports': 7.50     # Strenuous sports
        }
        
        # Constants for METs estimation formula: METs = (DASI + 43.24) / 9.6
        self.METS_INTERCEPT = 43.24
        self.METS_COEFFICIENT = 9.6
    
    def calculate(self, personal_care: str, walk_indoors: str, walk_1_2_blocks: str,
                  climb_stairs: str, run_short_distance: str, light_housework: str,
                  moderate_housework: str, heavy_housework: str, yard_work: str,
                  sexual_relations: str, moderate_recreation: str, strenuous_sports: str) -> Dict[str, Any]:
        """
        Calculates the Duke Activity Status Index (DASI) score
        
        Args:
            All 12 DASI activity parameters as strings ("yes"/"no")
            
        Returns:
            Dict with the result and interpretation including estimated METs
        """
        
        # Map parameters for easier processing
        parameters = {
            'personal_care': personal_care,
            'walk_indoors': walk_indoors,
            'walk_1_2_blocks': walk_1_2_blocks,
            'climb_stairs': climb_stairs,
            'run_short_distance': run_short_distance,
            'light_housework': light_housework,
            'moderate_housework': moderate_housework,
            'heavy_housework': heavy_housework,
            'yard_work': yard_work,
            'sexual_relations': sexual_relations,
            'moderate_recreation': moderate_recreation,
            'strenuous_sports': strenuous_sports
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate DASI score
        dasi_score = self._calculate_dasi_score(parameters)
        
        # Calculate estimated METs
        estimated_mets = self._calculate_estimated_mets(dasi_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(dasi_score, estimated_mets)
        
        return {
            "result": round(dasi_score, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "estimated_mets": round(estimated_mets, 1)
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        for param_name, response in parameters.items():
            if not isinstance(response, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if response.lower() not in valid_responses:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{response}'")
    
    def _calculate_dasi_score(self, parameters: Dict[str, str]) -> float:
        """Calculates the DASI score by summing weighted activities"""
        
        total_score = 0.0
        
        for activity, response in parameters.items():
            if response.lower() == 'yes':
                weight = self.ACTIVITY_WEIGHTS.get(activity, 0.0)
                total_score += weight
        
        return total_score
    
    def _calculate_estimated_mets(self, dasi_score: float) -> float:
        """Calculates estimated METs using the DASI-METs formula"""
        
        # Formula: METs = (DASI + 43.24) / 9.6
        estimated_mets = (dasi_score + self.METS_INTERCEPT) / self.METS_COEFFICIENT
        
        # METs should be positive
        return max(0.0, estimated_mets)
    
    def _get_interpretation(self, dasi_score: float, estimated_mets: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the DASI score and estimated METs
        
        Args:
            dasi_score (float): Calculated DASI score
            estimated_mets (float): Estimated METs value
            
        Returns:
            Dict with interpretation
        """
        
        if dasi_score < 20:
            return {
                "stage": "Poor Functional Capacity",
                "description": "Limited functional capacity (<4 METs)",
                "interpretation": f"Poor functional capacity with estimated {estimated_mets:.1f} METs. High perioperative risk. Consider cardiopulmonary exercise testing and optimization before major surgery. May require intensive perioperative monitoring and care."
            }
        elif dasi_score < 34:
            return {
                "stage": "Moderate Functional Capacity",
                "description": "Moderate functional capacity (4-7 METs)",
                "interpretation": f"Moderate functional capacity with estimated {estimated_mets:.1f} METs. Intermediate perioperative risk. Consider further cardiovascular evaluation if planning major surgery. May benefit from preoperative optimization."
            }
        else:  # dasi_score >= 34
            return {
                "stage": "Good Functional Capacity",
                "description": "Good functional capacity (>7 METs)",
                "interpretation": f"Good functional capacity with estimated {estimated_mets:.1f} METs. Lower perioperative risk. DASI score ≥34 associated with reduced odds of 30-day death, myocardial injury, and 1-year death or new disability. Generally adequate for major surgery."
            }


def calculate_duke_activity_status_index(personal_care: str, walk_indoors: str, walk_1_2_blocks: str,
                                        climb_stairs: str, run_short_distance: str, light_housework: str,
                                        moderate_housework: str, heavy_housework: str, yard_work: str,
                                        sexual_relations: str, moderate_recreation: str, strenuous_sports: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_duke_activity_status_index pattern
    """
    calculator = DukeActivityStatusIndexCalculator()
    return calculator.calculate(
        personal_care, walk_indoors, walk_1_2_blocks, climb_stairs,
        run_short_distance, light_housework, moderate_housework, heavy_housework,
        yard_work, sexual_relations, moderate_recreation, strenuous_sports
    )