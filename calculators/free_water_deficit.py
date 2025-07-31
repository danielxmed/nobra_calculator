"""
Free Water Deficit in Hypernatremia Calculator

Calculates free water deficit by estimated total body water in patients with 
hypernatremia or dehydration.

References:
1. Adrogue HJ, Madias NE. Hypernatremia. N Engl J Med. 2000;342(20):1493-9. 
   doi: 10.1056/NEJM200005183422006.
2. Moritz ML, Ayus JC. The changing pattern of hypernatremia in hospitalized children. 
   Pediatrics. 1999;104(3 Pt 1):435-9. doi: 10.1542/peds.104.3.435.
3. Verbalis JG, Goldsmith SR, Greenberg A, et al. Diagnosis, evaluation, and treatment 
   of hyponatremia: expert panel recommendations. Am J Med. 2013;126(10 Suppl 1):S1-42. 
   doi: 10.1016/j.amjmed.2013.07.006.
"""

from typing import Dict, Any


class FreeWaterDeficitCalculator:
    """Calculator for Free Water Deficit in Hypernatremia"""
    
    def __init__(self):
        # Total body water fractions by age and sex
        self.TBW_FRACTIONS = {
            ('child', 'male'): 0.6,
            ('child', 'female'): 0.6,
            ('adult', 'male'): 0.6,
            ('adult', 'female'): 0.5,
            ('elderly', 'male'): 0.5,
            ('elderly', 'female'): 0.45
        }
    
    def calculate(self, sex: str, age_category: str, weight: float, 
                  current_sodium: float, desired_sodium: float) -> Dict[str, Any]:
        """
        Calculates free water deficit for hypernatremia correction
        
        Args:
            sex (str): Patient sex ("male" or "female")
            age_category (str): Age category ("child", "adult", or "elderly")
            weight (float): Patient weight in kg
            current_sodium (float): Current serum sodium in mEq/L
            desired_sodium (float): Desired serum sodium in mEq/L (typically 140)
            
        Returns:
            Dict with free water deficit and interpretation
        """
        
        # Validations
        self._validate_inputs(sex, age_category, weight, current_sodium, desired_sodium)
        
        # Calculate free water deficit
        deficit_liters = self._calculate_deficit(sex, age_category, weight, 
                                               current_sodium, desired_sodium)
        
        # Get interpretation
        interpretation = self._get_interpretation(deficit_liters, current_sodium, desired_sodium)
        
        return {
            "result": round(deficit_liters, 2),
            "unit": "L",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sex, age_category, weight, current_sodium, desired_sodium):
        """Validates input parameters"""
        
        if not isinstance(sex, str) or sex.lower() not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(age_category, str) or age_category.lower() not in ["child", "adult", "elderly"]:
            raise ValueError("Age category must be 'child', 'adult', or 'elderly'")
        
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        if weight < 0.226 or weight > 226.796:
            raise ValueError("Weight must be between 0.226 and 226.796 kg")
        
        if not isinstance(current_sodium, (int, float)):
            raise ValueError("Current sodium must be a number")
        if current_sodium < 100 or current_sodium > 200:
            raise ValueError("Current sodium must be between 100 and 200 mEq/L")
        
        if not isinstance(desired_sodium, (int, float)):
            raise ValueError("Desired sodium must be a number")
        if desired_sodium < 135 or desired_sodium > 145:
            raise ValueError("Desired sodium must be between 135 and 145 mEq/L")
        
        if current_sodium <= desired_sodium:
            raise ValueError("Current sodium must be greater than desired sodium for hypernatremia calculation")
    
    def _calculate_deficit(self, sex, age_category, weight, current_sodium, desired_sodium):
        """Calculates the free water deficit using the standard formula"""
        
        # Get total body water fraction
        key = (age_category.lower(), sex.lower())
        tbw_fraction = self.TBW_FRACTIONS.get(key, 0.5)  # Default to 0.5 if not found
        
        # Formula: Free water deficit (L) = TBW fraction × Weight (kg) × (Current Na/Desired Na - 1)
        deficit_liters = tbw_fraction * weight * (current_sodium / desired_sodium - 1)
        
        # Free water deficit should be positive for hypernatremia
        return max(0, deficit_liters)
    
    def _get_interpretation(self, deficit_liters: float, current_sodium: float, 
                           desired_sodium: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on free water deficit
        
        Args:
            deficit_liters (float): Calculated free water deficit in liters
            current_sodium (float): Current serum sodium
            desired_sodium (float): Desired serum sodium
            
        Returns:
            Dict with interpretation
        """
        
        # Calculate sodium difference for context
        sodium_diff = current_sodium - desired_sodium
        
        # Calculate estimated correction time (should not exceed 0.5 mEq/L per hour)
        max_safe_rate = 0.5  # mEq/L per hour
        minimum_hours = sodium_diff / max_safe_rate
        
        base_interpretation = (
            f"Free water deficit of {deficit_liters:.2f} L calculated to correct serum sodium from "
            f"{current_sodium:.1f} to {desired_sodium:.1f} mEq/L. "
        )
        
        safety_info = (
            f"Correction should not exceed 0.5 mEq/L per hour to prevent cerebral edema "
            f"(minimum {minimum_hours:.1f} hours for safe correction). "
        )
        
        if deficit_liters < 2:
            return {
                "stage": "Mild Deficit",
                "description": "Mild free water deficit",
                "interpretation": (
                    base_interpretation + 
                    "Mild deficit that may be managed with oral hydration if patient can tolerate. " +
                    safety_info +
                    "Monitor serum sodium every 12 hours during correction. Add 1L per day for insensible losses."
                )
            }
        elif deficit_liters < 5:
            return {
                "stage": "Moderate Deficit",
                "description": "Moderate free water deficit",
                "interpretation": (
                    base_interpretation +
                    "Moderate deficit requiring IV fluid replacement. Use 5% dextrose or hypotonic saline. " +
                    safety_info +
                    "Target correction of 10 mEq/L in first 24 hours. Monitor electrolytes every 12 hours. "
                    "Add additional fluid for ongoing losses (insensible, urine output)."
                )
            }
        elif deficit_liters < 10:
            return {
                "stage": "Severe Deficit",
                "description": "Severe free water deficit",
                "interpretation": (
                    base_interpretation +
                    "Severe deficit requiring careful IV fluid management with close monitoring. " +
                    safety_info +
                    "Use 5% dextrose or hypotonic solutions. Consider ICU monitoring. "
                    "Target maximum 10 mEq/L correction in 24 hours, then 10 mEq/L per day. "
                    "Account for ongoing losses and insensible losses."
                )
            }
        else:
            return {
                "stage": "Critical Deficit",
                "description": "Critical free water deficit",
                "interpretation": (
                    base_interpretation +
                    "Critical deficit requiring intensive monitoring and nephrology consultation. " +
                    safety_info +
                    "Recommend ICU management with hourly electrolyte monitoring initially. "
                    "Use extreme caution with correction rate. Consider dialysis if renal function compromised. "
                    "Must account for all ongoing fluid losses and adjust replacement accordingly."
                )
            }


def calculate_free_water_deficit(sex: str, age_category: str, weight: float, 
                                current_sodium: float, desired_sodium: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_free_water_deficit pattern
    """
    calculator = FreeWaterDeficitCalculator()
    return calculator.calculate(sex, age_category, weight, current_sodium, desired_sodium)