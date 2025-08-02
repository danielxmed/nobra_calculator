"""
Ideal Body Weight and Adjusted Body Weight Calculator

Calculates ideal body weight using the Devine formula and adjusted body weight 
for clinical use, particularly medication dosing and physiological calculations.

References:
- Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm. 1974;8:650-655
- Pai MP, Paloucek FP. The origin of the "ideal" body weight equations. 
  Ann Pharmacother. 2000 Sep;34(9):1066-9.
"""

from typing import Dict, Any, Optional


class IdealBodyWeightAdjustedCalculator:
    """Calculator for Ideal Body Weight and Adjusted Body Weight using Devine formula"""
    
    def __init__(self):
        # Devine formula constants
        self.male_base_weight = 50.0      # kg
        self.female_base_weight = 45.5    # kg
        self.height_increment = 2.3       # kg per inch over 60 inches
        self.base_height = 60             # inches (5 feet)
        self.adjustment_factor = 0.4      # for adjusted body weight calculation
        
        # Height thresholds
        self.minimum_height = 48.0        # inches (4 feet)
        self.normal_height_threshold = 60.0  # inches (5 feet)
    
    def calculate(self, sex: str, height_inches: float, 
                 actual_weight_kg: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates ideal body weight and adjusted body weight
        
        Args:
            sex (str): Patient sex ("male" or "female")
            height_inches (float): Height in inches
            actual_weight_kg (float, optional): Actual weight in kg for adjusted weight calculation
            
        Returns:
            Dict with ideal body weight, adjusted body weight (if applicable), and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sex, height_inches, actual_weight_kg)
        
        # Calculate ideal body weight using Devine formula
        ideal_body_weight = self._calculate_ideal_body_weight(sex, height_inches)
        
        # Calculate adjusted body weight if actual weight provided
        adjusted_body_weight = None
        if actual_weight_kg is not None:
            adjusted_body_weight = self._calculate_adjusted_body_weight(
                ideal_body_weight, actual_weight_kg
            )
        
        # Get interpretation
        interpretation = self._get_interpretation(height_inches, ideal_body_weight, 
                                                actual_weight_kg, adjusted_body_weight)
        
        result = {
            "result": {
                "ideal_body_weight": round(ideal_body_weight, 1),
                "adjusted_body_weight": round(adjusted_body_weight, 1) if adjusted_body_weight else None,
                "height_inches": height_inches,
                "height_cm": round(height_inches * 2.54, 1)
            },
            "unit": "kg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "clinical_applications": interpretation["applications"],
            "dosing_considerations": interpretation["dosing_notes"]
        }
        
        return result
    
    def _validate_inputs(self, sex: str, height_inches: float, actual_weight_kg: Optional[float]):
        """Validates input parameters"""
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(height_inches, (int, float)) or height_inches < self.minimum_height or height_inches > 84:
            raise ValueError("Height must be between 48 and 84 inches")
        
        if actual_weight_kg is not None:
            if not isinstance(actual_weight_kg, (int, float)) or actual_weight_kg < 20 or actual_weight_kg > 300:
                raise ValueError("Actual weight must be between 20 and 300 kg")
    
    def _calculate_ideal_body_weight(self, sex: str, height_inches: float) -> float:
        """
        Calculates ideal body weight using Devine formula
        
        Devine Formula:
        - Men: IBW = 50 kg + 2.3 kg × (height in inches - 60)
        - Women: IBW = 45.5 kg + 2.3 kg × (height in inches - 60)
        
        Args:
            sex (str): Patient sex
            height_inches (float): Height in inches
            
        Returns:
            float: Ideal body weight in kg
        """
        
        # Base weight depending on sex
        if sex == "male":
            base_weight = self.male_base_weight
        else:
            base_weight = self.female_base_weight
        
        # Calculate height above base height (60 inches)
        height_above_base = height_inches - self.base_height
        
        # Calculate ideal body weight
        ideal_weight = base_weight + (self.height_increment * height_above_base)
        
        return max(ideal_weight, 20.0)  # Ensure minimum reasonable weight
    
    def _calculate_adjusted_body_weight(self, ideal_weight: float, actual_weight: float) -> float:
        """
        Calculates adjusted body weight for overweight/obese patients
        
        Formula: AjBW = IBW + 0.4 × (ABW - IBW)
        
        Args:
            ideal_weight (float): Ideal body weight in kg
            actual_weight (float): Actual body weight in kg
            
        Returns:
            float: Adjusted body weight in kg
        """
        
        # If actual weight is less than or equal to ideal, return actual weight
        if actual_weight <= ideal_weight:
            return actual_weight
        
        # Calculate adjusted body weight for overweight patients
        weight_difference = actual_weight - ideal_weight
        adjusted_weight = ideal_weight + (self.adjustment_factor * weight_difference)
        
        return adjusted_weight
    
    def _get_interpretation(self, height_inches: float, ideal_weight: float,
                          actual_weight: Optional[float], adjusted_weight: Optional[float]) -> Dict[str, Any]:
        """
        Determines interpretation based on calculations
        
        Args:
            height_inches (float): Height in inches
            ideal_weight (float): Calculated ideal body weight
            actual_weight (float, optional): Actual body weight
            adjusted_weight (float, optional): Calculated adjusted body weight
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine height category
        if height_inches >= self.normal_height_threshold:
            stage = "Normal Height"
            description = "≥60 inches (5 feet)"
            height_note = "Standard Devine formula applies."
        else:
            stage = "Short Stature"
            description = "<60 inches (5 feet)"
            inches_below = self.normal_height_threshold - height_inches
            height_note = f"Consider subtracting 2-5 lbs per inch below 60 inches ({inches_below:.1f} inches below threshold)."
        
        # Build interpretation
        if actual_weight is None:
            interpretation = f"Ideal body weight calculated as {ideal_weight:.1f} kg using Devine formula. {height_note}"
            
            applications = [
                "Medication dosing calculations",
                "Tidal volume calculation for mechanical ventilation",
                "Clinical assessment reference"
            ]
            
            dosing_notes = [
                "Confirm medication dosing recommendations with pharmacy",
                "Some medications use ideal body weight, others use actual body weight",
                "Consider patient-specific factors for dosing decisions"
            ]
        
        else:
            weight_diff = actual_weight - ideal_weight
            if weight_diff <= 0:
                weight_status = "at or below ideal weight"
                weight_recommendation = "Use actual body weight for most calculations."
            else:
                weight_status = f"{weight_diff:.1f} kg above ideal weight"
                weight_recommendation = f"Consider using adjusted body weight ({adjusted_weight:.1f} kg) for certain medications and calculations."
            
            interpretation = f"Ideal body weight: {ideal_weight:.1f} kg. Patient is {weight_status}. {weight_recommendation} {height_note}"
            
            applications = [
                "Medication dosing in overweight/obese patients",
                "Tidal volume calculation (use ideal body weight)",
                "Nutritional assessment and planning",
                "Clinical research calculations"
            ]
            
            dosing_notes = [
                "Hydrophilic drugs: typically use ideal body weight",
                "Lipophilic drugs: may use adjusted body weight",
                "Confirm specific medication dosing guidelines",
                "Adjusted body weight = IBW + 0.4 × (actual weight - IBW)"
            ]
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "applications": applications,
            "dosing_notes": dosing_notes
        }


def calculate_ideal_body_weight_adjusted(sex: str, height_inches: float,
                                       actual_weight_kg: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = IdealBodyWeightAdjustedCalculator()
    return calculator.calculate(sex, height_inches, actual_weight_kg)