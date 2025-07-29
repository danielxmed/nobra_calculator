"""
Basal Energy Expenditure Calculator

Calculates daily energy expenditure using the Harris-Benedict equation.

References:
1. Harris JA, Benedict FG. A biometric study of basal metabolism in man. 
   Washington DC: Carnegie Institute of Washington; 1919.
"""

from typing import Dict, Any, Optional


class BasalEnergyExpenditureCalculator:
    """Calculator for Basal Energy Expenditure using Harris-Benedict equation"""
    
    def __init__(self):
        # Harris-Benedict equation constants
        self.male_constants = {
            "base": 66.5,
            "weight_factor": 13.75,
            "height_factor": 5.003,
            "age_factor": 6.775
        }
        
        self.female_constants = {
            "base": 655.1,
            "weight_factor": 9.563,
            "height_factor": 1.850,
            "age_factor": 4.676
        }
        
        # Activity level multipliers
        self.activity_factors = {
            "sedentary": 1.2,      # Little to no exercise
            "light": 1.375,        # Light exercise 1-3 days/week
            "moderate": 1.55,      # Moderate exercise 3-5 days/week
            "heavy": 1.725,        # Heavy exercise 6-7 days/week
            "very_heavy": 1.9      # Very heavy physical job or training
        }
    
    def calculate(self, sex: str, weight: float, height: float, age: int,
                  activity_level: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates basal energy expenditure using Harris-Benedict equation
        
        Args:
            sex (str): Biological sex ("male" or "female")
            weight (float): Body weight in kg
            height (float): Height in cm
            age (int): Age in years
            activity_level (str, optional): Activity level for total daily energy expenditure
            
        Returns:
            Dict with BEE and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sex, weight, height, age, activity_level)
        
        # Calculate basal energy expenditure
        bee = self._calculate_bee(sex, weight, height, age)
        
        # Apply activity factor if provided
        if activity_level:
            tdee = bee * self.activity_factors[activity_level]
            result_value = tdee
            result_type = "TDEE"
        else:
            result_value = bee
            result_type = "BEE"
        
        # Get interpretation
        interpretation = self._get_interpretation(bee, activity_level, result_value, result_type)
        
        return {
            "result": round(result_value, 0),
            "unit": "kcal/day",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sex: str, weight: float, height: float, age: int,
                        activity_level: Optional[str]):
        """Validates input parameters"""
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(weight, (int, float)) or weight < 20 or weight > 300:
            raise ValueError("Weight must be between 20 and 300 kg")
        
        if not isinstance(height, (int, float)) or height < 100 or height > 250:
            raise ValueError("Height must be between 100 and 250 cm")
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        if activity_level is not None and activity_level not in self.activity_factors:
            raise ValueError(f"Activity level must be one of: {', '.join(self.activity_factors.keys())}")
    
    def _calculate_bee(self, sex: str, weight: float, height: float, age: int) -> float:
        """
        Calculates basal energy expenditure using Harris-Benedict equation
        
        Men: BEE = 66.5 + (13.75 × weight) + (5.003 × height) - (6.775 × age)
        Women: BEE = 655.1 + (9.563 × weight) + (1.850 × height) - (4.676 × age)
        """
        
        if sex == "male":
            constants = self.male_constants
        else:
            constants = self.female_constants
        
        bee = (constants["base"] + 
               (constants["weight_factor"] * weight) +
               (constants["height_factor"] * height) -
               (constants["age_factor"] * age))
        
        return bee
    
    def _get_interpretation(self, bee: float, activity_level: Optional[str],
                           result_value: float, result_type: str) -> Dict[str, str]:
        """
        Determines interpretation based on BEE value
        
        Args:
            bee (float): Basal energy expenditure
            activity_level (str): Activity level if provided
            result_value (float): Either BEE or TDEE
            result_type (str): "BEE" or "TDEE"
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine stage based on BEE (not TDEE)
        if bee < 1500:
            stage = "Low"
            description = "Low basal energy expenditure"
            base_interpretation = "Low basal metabolic rate. Consider evaluating for metabolic disorders if unexpectedly low."
        elif bee < 2000:
            stage = "Normal"
            description = "Normal basal energy expenditure"
            base_interpretation = "Normal basal metabolic rate for most adults."
        elif bee < 2500:
            stage = "High"
            description = "High basal energy expenditure"
            base_interpretation = "Higher than average basal metabolic rate. Common in younger males and individuals with higher muscle mass."
        else:
            stage = "Very High"
            description = "Very high basal energy expenditure"
            base_interpretation = "Very high basal metabolic rate. May be seen in athletes or individuals with very high muscle mass."
        
        # Build complete interpretation
        if activity_level:
            activity_desc = {
                "sedentary": "sedentary lifestyle (little to no exercise)",
                "light": "light exercise (1-3 days/week)",
                "moderate": "moderate exercise (3-5 days/week)",
                "heavy": "heavy exercise (6-7 days/week)",
                "very_heavy": "very heavy physical activity"
            }
            
            interpretation = (f"{base_interpretation} Basal Energy Expenditure (BEE): {round(bee, 0)} kcal/day. " +
                            f"Total Daily Energy Expenditure (TDEE) adjusted for {activity_desc[activity_level]}: " +
                            f"{round(result_value, 0)} kcal/day.")
        else:
            interpretation = f"{base_interpretation} This represents resting metabolic rate without activity adjustment."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }


def calculate_basal_energy_expenditure(sex: str, weight: float, height: float, age: int,
                                     activity_level: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BasalEnergyExpenditureCalculator()
    return calculator.calculate(sex, weight, height, age, activity_level)