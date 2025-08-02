"""
Intracerebral Hemorrhage (ICH) Score Calculator

Estimates 30-day mortality risk in patients with spontaneous intracerebral hemorrhage 
based on clinical and radiographic findings at presentation.

References (Vancouver style):
1. Hemphill JC 3rd, Bonovich DC, Besmertis L, Manley GT, Johnston SC. The ICH score: a 
   simple, reliable grading scale for intracerebral hemorrhage. Stroke. 2001 Apr;32(4):891-7. 
   doi: 10.1161/01.str.32.4.891.
2. Rost NS, Smith EE, Chang Y, Snider RW, Chanderraj R, Schwab K, et al. Prediction of 
   functional outcome in patients with primary intracerebral hemorrhage: the FUNC score. 
   Stroke. 2008 Aug;39(8):2304-9. doi: 10.1161/STROKEAHA.107.512202.
3. Godoy DA, Pinero G, Papa F. Predicting mortality in spontaneous intracerebral hemorrhage: 
   can modification to original score improve the prediction? Stroke. 2006 Apr;37(4):1038-44. 
   doi: 10.1161/01.STR.0000206441.79646.49.
"""

from typing import Dict, Any


class IchScoreCalculator:
    """Calculator for Intracerebral Hemorrhage (ICH) Score"""
    
    def __init__(self):
        # Scoring weights for each parameter
        self.scoring_weights = {
            "glasgow_coma_scale": {
                "13_15": 0,
                "5_12": 1,
                "3_4": 2
            },
            "age": {
                "under_80": 0,
                "80_or_older": 1
            },
            "ich_location": {
                "supratentorial": 0,
                "infratentorial": 1
            },
            "ich_volume": {
                "less_than_30": 0,
                "30_or_greater": 1
            },
            "intraventricular_hemorrhage": {
                "absent": 0,
                "present": 1
            }
        }
    
    def calculate(self, glasgow_coma_scale: str, age: str, ich_location: str, 
                  ich_volume: str, intraventricular_hemorrhage: str) -> Dict[str, Any]:
        """
        Calculates the ICH Score using the provided parameters
        
        Args:
            glasgow_coma_scale (str): GCS score category ("13_15", "5_12", "3_4")
            age (str): Age category ("under_80", "80_or_older")
            ich_location (str): ICH location ("supratentorial", "infratentorial")
            ich_volume (str): ICH volume category ("less_than_30", "30_or_greater")
            intraventricular_hemorrhage (str): IVH presence ("absent", "present")
            
        Returns:
            Dict with the ICH score and mortality prediction
        """
        
        # Validate inputs
        self._validate_inputs(glasgow_coma_scale, age, ich_location, ich_volume, intraventricular_hemorrhage)
        
        # Calculate total score
        total_score = self._calculate_total_score(glasgow_coma_scale, age, ich_location, 
                                                ich_volume, intraventricular_hemorrhage)
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, glasgow_coma_scale: str, age: str, ich_location: str, 
                        ich_volume: str, intraventricular_hemorrhage: str):
        """Validates input parameters"""
        
        # Validate Glasgow Coma Scale
        if glasgow_coma_scale not in self.scoring_weights["glasgow_coma_scale"]:
            raise ValueError(f"Glasgow Coma Scale must be one of: {list(self.scoring_weights['glasgow_coma_scale'].keys())}")
        
        # Validate age
        if age not in self.scoring_weights["age"]:
            raise ValueError(f"Age must be one of: {list(self.scoring_weights['age'].keys())}")
        
        # Validate ICH location
        if ich_location not in self.scoring_weights["ich_location"]:
            raise ValueError(f"ICH location must be one of: {list(self.scoring_weights['ich_location'].keys())}")
        
        # Validate ICH volume
        if ich_volume not in self.scoring_weights["ich_volume"]:
            raise ValueError(f"ICH volume must be one of: {list(self.scoring_weights['ich_volume'].keys())}")
        
        # Validate intraventricular hemorrhage
        if intraventricular_hemorrhage not in self.scoring_weights["intraventricular_hemorrhage"]:
            raise ValueError(f"Intraventricular hemorrhage must be one of: {list(self.scoring_weights['intraventricular_hemorrhage'].keys())}")
    
    def _calculate_total_score(self, glasgow_coma_scale: str, age: str, ich_location: str, 
                              ich_volume: str, intraventricular_hemorrhage: str) -> int:
        """Calculates the total ICH score"""
        
        total_score = 0
        total_score += self.scoring_weights["glasgow_coma_scale"][glasgow_coma_scale]
        total_score += self.scoring_weights["age"][age]
        total_score += self.scoring_weights["ich_location"][ich_location]
        total_score += self.scoring_weights["ich_volume"][ich_volume]
        total_score += self.scoring_weights["intraventricular_hemorrhage"][intraventricular_hemorrhage]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ICH score
        
        Args:
            score (int): Calculated ICH score (0-6 points)
            
        Returns:
            Dict with mortality risk prediction and clinical recommendations
        """
        
        if score == 0:
            return {
                "stage": "Very Low Risk",
                "description": "Score 0 points",
                "interpretation": "Excellent prognosis. 30-day mortality: 0-5%. All patients with ICH Score 0 survived in the original validation study. Standard ICH management with close monitoring. Consider less aggressive interventions. Favorable outcome expected with appropriate care. Excellent candidate for rehabilitation planning."
            }
        elif score == 1:
            return {
                "stage": "Low Risk",
                "description": "Score 1 point",
                "interpretation": "Good prognosis. 30-day mortality: ~16%. Low mortality risk with appropriate management. Standard intensive care with neurological monitoring. Consider early rehabilitation planning. Favorable functional outcome possible with optimal care."
            }
        elif score == 2:
            return {
                "stage": "Moderate Risk",
                "description": "Score 2 points",
                "interpretation": "Moderate prognosis. 30-day mortality: ~33%. Intermediate risk requiring intensive management. Consider aggressive medical management and possible surgical intervention based on clinical status. Close neurological monitoring essential. Discuss prognosis with family."
            }
        elif score == 3:
            return {
                "stage": "High Risk",
                "description": "Score 3 points",
                "interpretation": "Poor prognosis. 30-day mortality: ~54%. High mortality risk despite optimal care. Consider intensive treatment approaches and surgical evaluation. Goals of care discussions with family recommended. Palliative care consultation may be appropriate."
            }
        elif score == 4:
            return {
                "stage": "Very High Risk",
                "description": "Score 4 points",
                "interpretation": "Very poor prognosis. 30-day mortality: ~93%. Extremely high mortality risk. Consider comfort care measures and goals of care discussions. Palliative care consultation recommended. Family support and end-of-life planning important."
            }
        else:  # score >= 5
            return {
                "stage": "Extremely High Risk",
                "description": "Score 5-6 points",
                "interpretation": "Extremely poor prognosis. 30-day mortality: 95-100%. Near-universal mortality. All patients with ICH Score ≥5 died in original validation study. Comfort care measures and palliative care consultation recommended. Focus on family support and dignified end-of-life care."
            }


def calculate_ich_score(glasgow_coma_scale: str, age: str, ich_location: str, 
                       ich_volume: str, intraventricular_hemorrhage: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the ICH Score for 30-day mortality prediction in intracerebral hemorrhage
    using five clinical and radiographic parameters.
    
    Args:
        glasgow_coma_scale (str): GCS score category
        age (str): Age category
        ich_location (str): Location of hemorrhage
        ich_volume (str): Volume of hemorrhage
        intraventricular_hemorrhage (str): Presence of IVH
        
    Returns:
        Dict with ICH score and mortality risk prediction
    """
    calculator = IchScoreCalculator()
    return calculator.calculate(glasgow_coma_scale, age, ich_location, ich_volume, intraventricular_hemorrhage)