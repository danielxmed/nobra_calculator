"""
Fat Free Mass (FFM) Calculator

Calculates the predictive value of fat-free mass from body weight and body mass index (BMI). 
This calculation is useful for weight-based medication dosing, especially in anesthesia, 
and helps calculate body composition.

References:
- Janmahasatian S, Duffull SB, Ash S, Ward LC, Byrnes NM, Green B. Quantification of lean 
  bodyweight. Clin Pharmacokinet. 2005;44(10):1051-65.
- La Colla L, Albertin A, La Colla G, Mangano A. Predictive value of the Janmahasatian 
  formula for lean body weight in the dosing of sugammadex in morbidly obese patients. 
  Anaesthesia. 2010;65(4):445-6.
"""

from typing import Dict, Any


class FatFreeMassCalculator:
    """Calculator for Fat Free Mass (FFM)"""
    
    def __init__(self):
        # Formula constants from Janmahasatian 2005 study
        self.MALE_WEIGHT_COEFFICIENT = 9.27e3  # 9.27 × 10³
        self.FEMALE_WEIGHT_COEFFICIENT = 9.27e3  # 9.27 × 10³
        self.MALE_DENOMINATOR_CONSTANT = 6.68e3  # 6.68 × 10³
        self.FEMALE_DENOMINATOR_CONSTANT = 8.78e3  # 8.78 × 10³
        self.MALE_BMI_COEFFICIENT = 216
        self.FEMALE_BMI_COEFFICIENT = 244
    
    def calculate(self, sex: str, body_weight_kg: float, bmi: float) -> Dict[str, Any]:
        """
        Calculates the Fat Free Mass using sex-specific formulas
        
        Args:
            sex (str): Patient biological sex ("male" or "female")
            body_weight_kg (float): Body weight in kilograms (10-300 kg)
            bmi (float): Body Mass Index in kg/m² (10-80 kg/m²)
            
        Returns:
            Dict with the FFM result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sex, body_weight_kg, bmi)
        
        # Calculate Fat Free Mass using sex-specific formula
        ffm = self._calculate_ffm(sex, body_weight_kg, bmi)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(ffm, body_weight_kg, sex)
        
        return {
            "result": ffm,
            "unit": "kg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "percentage_of_body_weight": round((ffm / body_weight_kg) * 100, 1),
            "fat_mass": round(body_weight_kg - ffm, 1)
        }
    
    def _validate_inputs(self, sex: str, body_weight_kg: float, bmi: float):
        """Validates input parameters"""
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(body_weight_kg, (int, float)):
            raise ValueError("Body weight must be a number")
        
        if not isinstance(bmi, (int, float)):
            raise ValueError("BMI must be a number")
        
        if body_weight_kg < 10 or body_weight_kg > 300:
            raise ValueError("Body weight must be between 10 and 300 kg")
        
        if bmi < 10 or bmi > 80:
            raise ValueError("BMI must be between 10 and 80 kg/m²")
    
    def _calculate_ffm(self, sex: str, body_weight_kg: float, bmi: float) -> float:
        """
        Calculates Fat Free Mass using the Janmahasatian formula:
        Male: FFM = (9.27 × 10³ × Body Weight) / (6.68 × 10³ + 216 × BMI)
        Female: FFM = (9.27 × 10³ × Body Weight) / (8.78 × 10³ + 244 × BMI)
        """
        
        if sex == "male":
            numerator = self.MALE_WEIGHT_COEFFICIENT * body_weight_kg
            denominator = self.MALE_DENOMINATOR_CONSTANT + (self.MALE_BMI_COEFFICIENT * bmi)
        else:  # female
            numerator = self.FEMALE_WEIGHT_COEFFICIENT * body_weight_kg
            denominator = self.FEMALE_DENOMINATOR_CONSTANT + (self.FEMALE_BMI_COEFFICIENT * bmi)
        
        # Check for division by zero (should not occur with valid inputs)
        if denominator == 0:
            raise ValueError("Invalid calculation: denominator is zero")
        
        ffm = numerator / denominator
        
        return round(ffm, 1)
    
    def _get_interpretation(self, ffm: float, body_weight_kg: float, sex: str) -> Dict[str, str]:
        """
        Provides clinical interpretation of the Fat Free Mass result
        
        Args:
            ffm (float): Calculated Fat Free Mass
            body_weight_kg (float): Total body weight
            sex (str): Patient sex for context
            
        Returns:
            Dict with clinical interpretation
        """
        
        percentage_ffm = (ffm / body_weight_kg) * 100
        fat_mass = body_weight_kg - ffm
        percentage_fat = (fat_mass / body_weight_kg) * 100
        
        # Provide context based on typical FFM percentages
        if sex == "male":
            if percentage_ffm >= 85:
                ffm_category = "high lean mass"
            elif percentage_ffm >= 75:
                ffm_category = "normal lean mass"
            elif percentage_ffm >= 65:
                ffm_category = "low lean mass"
            else:
                ffm_category = "very low lean mass"
        else:  # female
            if percentage_ffm >= 80:
                ffm_category = "high lean mass"
            elif percentage_ffm >= 70:
                ffm_category = "normal lean mass"
            elif percentage_ffm >= 60:
                ffm_category = "low lean mass"
            else:
                ffm_category = "very low lean mass"
        
        return {
            "stage": "Calculated",
            "description": "Fat-free mass estimation",
            "interpretation": f"Calculated fat-free mass: {ffm} kg ({percentage_ffm:.1f}% of body weight). Fat mass: {fat_mass:.1f} kg ({percentage_fat:.1f}% of body weight). This represents {ffm_category} for a {sex} patient. FFM includes muscle, bone, organs, and water content, excluding adipose tissue. This value is useful for medication dosing calculations, particularly in anesthesia and for drugs with specific distribution properties in lean versus adipose tissue."
        }


def calculate_fat_free_mass(sex: str, body_weight_kg: float, bmi: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fat_free_mass pattern
    """
    calculator = FatFreeMassCalculator()
    return calculator.calculate(sex, body_weight_kg, bmi)