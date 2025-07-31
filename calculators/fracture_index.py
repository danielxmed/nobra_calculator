"""
FRACTURE Index Calculator

Predicts 5-year hip fracture risk in postmenopausal women using clinical risk factors 
with or without bone mineral density measurements.

References:
1. Black DM, Steinbuch M, Palermo L, et al. An assessment tool for predicting fracture 
   risk in postmenopausal women. Osteoporos Int. 2001;12(7):519-28.
2. Black DM, Palermo L, Nevitt MC, et al. Defining incident vertebral deformity: a 
   prospective comparison of several approaches. The Study of Osteoporotic Fractures 
   Research Group. J Bone Miner Res. 1999;14(1):90-101.
3. Cummings SR, Nevitt MC, Browner WS, et al. Risk factors for hip fracture in white 
   women. Study of Osteoporotic Fractures Research Group. N Engl J Med. 1995;332(12):767-73.
4. Ensrud KE, Lipschutz RC, Cauley JA, et al. Body size and hip fracture risk in older 
   women: a prospective study. Study of Osteoporotic Fractures Research Group. Am J Med. 1997;103(4):274-80.
"""

from typing import Dict, Any, Optional


class FractureIndexCalculator:
    """Calculator for FRACTURE Index"""
    
    def __init__(self):
        # Scoring thresholds and constants
        self.WEIGHT_THRESHOLD_KG = 57.7  # 127 lbs converted to kg
        self.LOW_RISK_THRESHOLD_WITHOUT_BMD = 4
        self.LOW_RISK_THRESHOLD_WITH_BMD = 6
        
        # Age scoring ranges
        self.AGE_SCORING = {
            (65, 69): 1,
            (70, 74): 2,
            (75, 79): 3,
            (80, 84): 4,
            (85, 100): 5
        }
        
        # BMD T-score scoring ranges
        self.BMD_SCORING = [
            (-5.0, -3.01, 4),  # <-3.0
            (-3.0, -2.61, 3),  # -2.6 to -3.0
            (-2.6, -2.11, 2),  # -2.1 to -2.5
            (-2.5, -1.11, 1),  # -1.1 to -2.0
            (-1.1, 3.0, 0)     # ≥-1.0
        ]
    
    def calculate(self, age: int, fracture_after_50: str, mother_hip_fracture: str,
                  weight: float, current_smoker: str, arms_to_stand: str,
                  bmd_t_score: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the FRACTURE Index score
        
        Args:
            age (int): Patient age in years
            fracture_after_50 (str): History of fracture after age 50 ("yes" or "no")
            mother_hip_fracture (str): Mother's history of hip fracture ("yes" or "no")
            weight (float): Patient weight in kg
            current_smoker (str): Current smoking status ("yes" or "no")
            arms_to_stand (str): Need to use arms to stand from chair ("yes" or "no")
            bmd_t_score (Optional[float]): BMD T-score (optional)
            
        Returns:
            Dict with the FRACTURE Index score and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(age, fracture_after_50, mother_hip_fracture, weight,
                             current_smoker, arms_to_stand, bmd_t_score)
        
        # Calculate individual component scores
        age_score = self._calculate_age_score(age)
        fracture_score = 1 if fracture_after_50.lower() == "yes" else 0
        mother_fracture_score = 1 if mother_hip_fracture.lower() == "yes" else 0
        weight_score = 1 if weight < self.WEIGHT_THRESHOLD_KG else 0
        smoker_score = 1 if current_smoker.lower() == "yes" else 0
        arms_score = 2 if arms_to_stand.lower() == "yes" else 0
        bmd_score = self._calculate_bmd_score(bmd_t_score) if bmd_t_score is not None else 0
        
        # Calculate total score
        total_score = (age_score + fracture_score + mother_fracture_score + 
                      weight_score + smoker_score + arms_score + bmd_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, bmd_t_score is not None)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, fracture_after_50: str, mother_hip_fracture: str,
                        weight: float, current_smoker: str, arms_to_stand: str,
                        bmd_t_score: Optional[float]):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        if age < 50 or age > 100:
            raise ValueError("Age must be between 50 and 100 years")
        
        # Validate yes/no parameters
        yes_no_params = {
            "Fracture after 50": fracture_after_50,
            "Mother's hip fracture": mother_hip_fracture,
            "Current smoker": current_smoker,
            "Arms to stand": arms_to_stand
        }
        
        for param_name, value in yes_no_params.items():
            if not isinstance(value, str):
                raise ValueError(f"{param_name} must be a string")
            if value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate weight
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        if weight < 30 or weight > 200:
            raise ValueError("Weight must be between 30 and 200 kg")
        
        # Validate BMD T-score if provided
        if bmd_t_score is not None:
            if not isinstance(bmd_t_score, (int, float)):
                raise ValueError("BMD T-score must be a number")
            if bmd_t_score < -5.0 or bmd_t_score > 3.0:
                raise ValueError("BMD T-score must be between -5.0 and 3.0")
    
    def _calculate_age_score(self, age: int) -> int:
        """Calculates age component score"""
        
        # Age <65 gets 0 points
        if age < 65:
            return 0
        
        # Find appropriate age range
        for (min_age, max_age), score in self.AGE_SCORING.items():
            if min_age <= age <= max_age:
                return score
        
        # Should not reach here due to validation, but return max score for safety
        return 5
    
    def _calculate_bmd_score(self, bmd_t_score: float) -> int:
        """Calculates BMD T-score component score"""
        
        # Find appropriate BMD range
        for min_val, max_val, score in self.BMD_SCORING:
            if min_val <= bmd_t_score < max_val:
                return score
        
        # Handle edge case for exactly 3.0
        if bmd_t_score >= -1.0:
            return 0
        
        # Should not reach here due to validation, but return max score for safety
        return 4
    
    def _get_interpretation(self, total_score: int, has_bmd: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on total score and BMD availability
        
        Args:
            total_score (int): Total FRACTURE Index score
            has_bmd (bool): Whether BMD was included in calculation
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine risk threshold based on BMD availability
        threshold = self.LOW_RISK_THRESHOLD_WITH_BMD if has_bmd else self.LOW_RISK_THRESHOLD_WITHOUT_BMD
        
        if total_score < threshold:
            return {
                "stage": "Low Risk",
                "description": "Low 5-year hip fracture risk",
                "interpretation": (f"FRACTURE Index score: {total_score}/15. Score <{threshold} "
                                f"{'(with BMD)' if has_bmd else '(without BMD)'} indicates low risk for hip fracture. "
                                f"5-year hip fracture risk ranges from <0.6% to 2.9%. Continue routine care with "
                                f"lifestyle measures including adequate calcium and vitamin D intake, weight-bearing "
                                f"exercise, and fall prevention strategies.")
            }
        else:
            return {
                "stage": "Elevated Risk",
                "description": "Elevated 5-year hip fracture risk requiring evaluation",
                "interpretation": (f"FRACTURE Index score: {total_score}/15. Score ≥{threshold} "
                                f"{'(with BMD)' if has_bmd else '(without BMD)'} suggests further evaluation is warranted. "
                                f"5-year hip fracture risk ranges from 3.0% to 8.7%. Consider bone density testing "
                                f"{'and ' if not has_bmd else ', '}FRAX assessment, and evaluation for osteoporosis "
                                f"treatment based on clinical judgment and current guidelines. Implement comprehensive "
                                f"fall prevention and bone health strategies.")
            }


def calculate_fracture_index(age: int, fracture_after_50: str, mother_hip_fracture: str,
                           weight: float, current_smoker: str, arms_to_stand: str,
                           bmd_t_score: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fracture_index pattern
    """
    calculator = FractureIndexCalculator()
    return calculator.calculate(age, fracture_after_50, mother_hip_fracture, weight,
                               current_smoker, arms_to_stand, bmd_t_score)