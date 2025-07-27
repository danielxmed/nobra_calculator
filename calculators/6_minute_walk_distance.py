"""
6 Minute Walk Distance Calculator

Calculates reference values for walk distance as a measure of functional status.
Reference: Enright PL, Sherrill DL. Am J Respir Crit Care Med. 1998;158(5):1384-7.
"""

from typing import Dict, Any, Optional


class SixMinuteWalkDistanceCalculator:
    """Calculator for 6 Minute Walk Distance"""
    
    def __init__(self):
        # Constants from Enright-Sherrill equations
        self.MALE_HEIGHT_COEFF = 7.57
        self.MALE_AGE_COEFF = -5.02
        self.MALE_WEIGHT_COEFF = -1.76
        self.MALE_CONSTANT = -309
        
        self.FEMALE_HEIGHT_COEFF = 2.11
        self.FEMALE_AGE_COEFF = -5.78
        self.FEMALE_WEIGHT_COEFF = -2.29
        self.FEMALE_CONSTANT = 667
        
        # Lower limit of normality
        self.LOWER_LIMIT_NORMAL = 153
    
    def calculate(self, age: int, sex: str, height: float, weight: float, 
                 observed_distance: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the predicted 6-minute walk distance
        
        Args:
            age: Age in years
            sex: "male" or "female"
            height: Height in centimeters
            weight: Weight in kilograms
            observed_distance: Observed distance (optional)
            
        Returns:
            Dict with predicted result, interpretation, and comparison
        """
        
        # Validations
        self._validate_inputs(age, sex, height, weight, observed_distance)
        
        # Calculate predicted distance
        predicted_distance = self._calculate_predicted_distance(age, sex, height, weight)
        
        # Calculate lower limit of normality
        lower_limit = predicted_distance - self.LOWER_LIMIT_NORMAL
        
        # Base results
        result = {
            "result": round(predicted_distance, 1),
            "unit": "meters",
            "lower_limit_normal": round(lower_limit, 1),
            "interpretation": f"Predicted distance of {predicted_distance:.1f} meters for a {sex} patient aged {age} years, {height} cm, and {weight} kg. Lower limit of normality: {lower_limit:.1f} meters.",
            "stage": "Predicted",
            "stage_description": "Calculated reference value",
            "percentage_predicted": None
        }
        
        # If observed distance was provided, add comparative analysis
        if observed_distance is not None:
            percentage_predicted = (observed_distance / predicted_distance) * 100
            interpretation_observed = self._get_interpretation_observed(percentage_predicted, observed_distance, lower_limit)
            
            result.update({
                "observed_distance": observed_distance,
                "percentage_predicted": round(percentage_predicted, 1),
                "interpretation": interpretation_observed["interpretation"],
                "stage": interpretation_observed["stage"],
                "stage_description": interpretation_observed["description"]
            })
        
        return result
    
    def _validate_inputs(self, age: int, sex: str, height: float, weight: float, 
                        observed_distance: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(height, (int, float)) or height < 120.0 or height > 220.0:
            raise ValueError("Height must be between 120.0 and 220.0 cm")
        
        if not isinstance(weight, (int, float)) or weight < 30.0 or weight > 200.0:
            raise ValueError("Weight must be between 30.0 and 200.0 kg")
        
        if observed_distance is not None:
            if not isinstance(observed_distance, (int, float)) or observed_distance < 0.0 or observed_distance > 1000.0:
                raise ValueError("Observed distance must be between 0.0 and 1000.0 meters")
    
    def _calculate_predicted_distance(self, age: int, sex: str, height: float, weight: float) -> float:
        """Calculates predicted distance using Enright-Sherrill equations"""
        
        if sex == "male":
            # Equation for men: 6MWD = (7.57 × height) - (5.02 × age) - (1.76 × weight) - 309
            predicted = (self.MALE_HEIGHT_COEFF * height + 
                        self.MALE_AGE_COEFF * age + 
                        self.MALE_WEIGHT_COEFF * weight + 
                        self.MALE_CONSTANT)
        else:
            # Equation for women: 6MWD = (2.11 × height) - (2.29 × weight) - (5.78 × age) + 667
            predicted = (self.FEMALE_HEIGHT_COEFF * height + 
                        self.FEMALE_WEIGHT_COEFF * weight + 
                        self.FEMALE_AGE_COEFF * age + 
                        self.FEMALE_CONSTANT)
        
        # Ensure it's not negative
        return max(predicted, 0.0)
    
    def _get_interpretation_observed(self, percentage_predicted: float, 
                                   observed_distance: float, lower_limit: float) -> Dict[str, str]:
        """
        Interprets the observed distance compared to the predicted
        
        Args:
            percentage_predicted: Percentage of predicted value
            observed_distance: Observed distance
            lower_limit: Lower limit of normality
            
        Returns:
            Dict with interpretation
        """
        
        # Classification based on percentage of predicted and lower limit
        if observed_distance < lower_limit or percentage_predicted < 50:
            return {
                "stage": "Severely Reduced",
                "description": "Severely reduced functional capacity",
                "interpretation": f"Observed distance of {observed_distance:.1f}m represents {percentage_predicted:.1f}% of predicted. Value is much lower than expected, indicating severe functional limitation requiring intensive investigation and treatment."
            }
        elif percentage_predicted < 75:
            return {
                "stage": "Moderately Reduced",
                "description": "Moderately reduced functional capacity",
                "interpretation": f"Observed distance of {observed_distance:.1f}m represents {percentage_predicted:.1f}% of predicted. Value is lower than expected, suggesting moderate functional limitation that may benefit from rehabilitation."
            }
        elif percentage_predicted < 90:
            return {
                "stage": "Slightly Reduced",
                "description": "Slightly reduced functional capacity",
                "interpretation": f"Observed distance of {observed_distance:.1f}m represents {percentage_predicted:.1f}% of predicted. Value is slightly lower than expected, potentially indicating mild functional limitation or onset of decline."
            }
        else:
            return {
                "stage": "Normal",
                "description": "Normal functional capacity",
                "interpretation": f"Observed distance of {observed_distance:.1f}m represents {percentage_predicted:.1f}% of predicted. Value is within expected limits, indicating preserved functional capacity."
            }


def calculate_6_minute_walk_distance(age: int, sex: str, height: float, weight: float, 
                                   observed_distance: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = SixMinuteWalkDistanceCalculator()
    return calculator.calculate(age, sex, height, weight, observed_distance)
