"""
FUNC Score Calculator

Predicts functional outcome in patients with primary intracerebral hemorrhage.

References:
- Rost NS, et al. Stroke. 2008;39(8):2304-9.
- Garrett JS, et al. Neurocrit Care. 2013;19(3):329-35.
"""

from typing import Dict, Any


class FuncScoreCalculator:
    """Calculator for Functional Outcome in Patients With Primary ICH (FUNC) Score"""
    
    def __init__(self):
        # Score mapping for each parameter
        self.ICH_VOLUME_SCORES = {
            "less_than_30": 4,
            "30_to_60": 2,
            "greater_than_60": 0
        }
        
        self.AGE_SCORES = {
            "less_than_70": 2,
            "70_to_79": 1,
            "80_or_greater": 0
        }
        
        self.LOCATION_SCORES = {
            "lobar": 2,
            "deep": 1,
            "infratentorial": 0
        }
        
        self.GCS_SCORES = {
            "9_or_greater": 2,
            "8_or_less": 0
        }
        
        self.COGNITIVE_SCORES = {
            "no": 1,
            "yes": 0
        }
    
    def calculate(self, ich_volume: str, age: str, ich_location: str, 
                  glasgow_coma_scale: str, pre_ich_cognitive_impairment: str) -> Dict[str, Any]:
        """
        Calculates the FUNC score
        
        Args:
            ich_volume: ICH volume category (less_than_30, 30_to_60, greater_than_60)
            age: Age category (less_than_70, 70_to_79, 80_or_greater)
            ich_location: ICH location (lobar, deep, infratentorial)
            glasgow_coma_scale: GCS category (9_or_greater, 8_or_less)
            pre_ich_cognitive_impairment: Cognitive impairment (yes/no)
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(ich_volume, age, ich_location, glasgow_coma_scale, pre_ich_cognitive_impairment)
        
        # Calculate total score
        result = self._calculate_score(ich_volume, age, ich_location, glasgow_coma_scale, pre_ich_cognitive_impairment)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ich_volume: str, age: str, ich_location: str, 
                        glasgow_coma_scale: str, pre_ich_cognitive_impairment: str):
        """Validates input parameters"""
        
        if ich_volume not in self.ICH_VOLUME_SCORES:
            raise ValueError(f"ICH volume must be one of: {', '.join(self.ICH_VOLUME_SCORES.keys())}")
        
        if age not in self.AGE_SCORES:
            raise ValueError(f"Age must be one of: {', '.join(self.AGE_SCORES.keys())}")
        
        if ich_location not in self.LOCATION_SCORES:
            raise ValueError(f"ICH location must be one of: {', '.join(self.LOCATION_SCORES.keys())}")
        
        if glasgow_coma_scale not in self.GCS_SCORES:
            raise ValueError(f"Glasgow Coma Scale must be one of: {', '.join(self.GCS_SCORES.keys())}")
        
        if pre_ich_cognitive_impairment not in self.COGNITIVE_SCORES:
            raise ValueError(f"Pre-ICH cognitive impairment must be one of: {', '.join(self.COGNITIVE_SCORES.keys())}")
    
    def _calculate_score(self, ich_volume: str, age: str, ich_location: str, 
                        glasgow_coma_scale: str, pre_ich_cognitive_impairment: str) -> int:
        """Calculates the total FUNC score"""
        
        total_score = (
            self.ICH_VOLUME_SCORES[ich_volume] +
            self.AGE_SCORES[age] +
            self.LOCATION_SCORES[ich_location] +
            self.GCS_SCORES[glasgow_coma_scale] +
            self.COGNITIVE_SCORES[pre_ich_cognitive_impairment]
        )
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): FUNC score (0-11)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 4:
            return {
                "stage": "Very Poor",
                "description": "0% chance of functional independence",
                "interpretation": "No patients in this group achieved functional independence (GOS ≥4) at 90 days. Consider comfort care measures and discussion of goals of care with family."
            }
        elif score <= 7:
            return {
                "stage": "Poor",
                "description": "13% chance of functional independence",
                "interpretation": "Only 13% of all patients (29% of survivors) achieved functional independence at 90 days. Most patients will have severe disability or require full-time care."
            }
        elif score == 8:
            return {
                "stage": "Moderate",
                "description": "42% chance of functional independence",
                "interpretation": "42% of all patients (48% of survivors) achieved functional independence at 90 days. Aggressive supportive care may be warranted."
            }
        elif score <= 10:
            return {
                "stage": "Good",
                "description": "66% chance of functional independence",
                "interpretation": "66% of all patients (75% of survivors) achieved functional independence at 90 days. Aggressive supportive care is recommended."
            }
        else:  # score == 11
            return {
                "stage": "Excellent",
                "description": "82% chance of functional independence",
                "interpretation": "82% of all patients (95% of survivors) achieved functional independence at 90 days. Full supportive care with rehabilitation planning is strongly recommended."
            }


def calculate_func_score(ich_volume, age, ich_location, 
                        glasgow_coma_scale, pre_ich_cognitive_impairment) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FuncScoreCalculator()
    return calculator.calculate(ich_volume, age, ich_location, 
                               glasgow_coma_scale, pre_ich_cognitive_impairment)