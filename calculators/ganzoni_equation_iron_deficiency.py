"""
Ganzoni Equation for Iron Deficiency Anemia Calculator

Assesses total body iron deficit for iron replacement therapy.

References:
1. Ganzoni AM. Intravenous iron-dextran: therapeutic and experimental possibilities. 
   Schweiz Med Wochenschr. 1970;100(7):301-3. (German)
2. Auerbach M, Adamson JW. How we diagnose and treat iron deficiency anemia. 
   Am J Hematol. 2016;91(1):31-8. doi: 10.1002/ajh.24201.
3. Camaschella C. Iron-deficiency anemia. N Engl J Med. 2015;372(19):1832-43. 
   doi: 10.1056/NEJMra1401038.

The Ganzoni equation calculates the precise amount of iron needed to replenish 
body iron stores and correct hemoglobin levels in patients with iron deficiency anemia.
"""

from typing import Dict, Any


class GanzoniEquationIronDeficiencyCalculator:
    """Calculator for Ganzoni Equation Iron Deficiency Assessment"""
    
    def __init__(self):
        # Ganzoni formula constant
        # Factor 2.4 = 0.0034 × 0.07 × 10,000
        # Where: 0.0034 = iron content of Hb (g iron/g Hb)
        #        0.07 = blood volume as 7% of body weight
        #        10,000 = conversion factor from g/dL to mg/L
        self.GANZONI_FACTOR = 2.4
        
        # Standard values
        self.STANDARD_TARGET_HB = 15.0  # g/dL
        self.STANDARD_IRON_STORES = 500  # mg
        self.MINIMUM_WEIGHT = 35  # kg - formula not validated below this weight
    
    def calculate(self, body_weight: float, current_hemoglobin: float, 
                  target_hemoglobin: float, iron_stores: int) -> Dict[str, Any]:
        """
        Calculates total body iron deficit using Ganzoni equation
        
        Args:
            body_weight (float): Patient's body weight in kg (≥35 kg)
            current_hemoglobin (float): Current hemoglobin level in g/dL
            target_hemoglobin (float): Target hemoglobin level in g/dL
            iron_stores (int): Iron stores to be replenished in mg
            
        Returns:
            Dict with iron deficit and clinical recommendations
        """
        
        # Validations
        self._validate_inputs(body_weight, current_hemoglobin, 
                            target_hemoglobin, iron_stores)
        
        # Calculate iron deficit using Ganzoni equation
        iron_deficit = self._calculate_iron_deficit(
            body_weight, current_hemoglobin, target_hemoglobin, iron_stores
        )
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(iron_deficit)
        
        return {
            "result": round(iron_deficit, 1),
            "unit": "mg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, body_weight: float, current_hemoglobin: float, 
                        target_hemoglobin: float, iron_stores: int):
        """Validates input parameters"""
        
        if not isinstance(body_weight, (int, float)) or body_weight < 35 or body_weight > 200:
            raise ValueError("Body weight must be between 35 and 200 kg. Formula not validated for patients <35 kg.")
        
        if not isinstance(current_hemoglobin, (int, float)) or current_hemoglobin < 3.0 or current_hemoglobin > 12.0:
            raise ValueError("Current hemoglobin must be between 3.0 and 12.0 g/dL")
        
        if not isinstance(target_hemoglobin, (int, float)) or target_hemoglobin < 10.0 or target_hemoglobin > 18.0:
            raise ValueError("Target hemoglobin must be between 10.0 and 18.0 g/dL")
        
        if target_hemoglobin <= current_hemoglobin:
            raise ValueError("Target hemoglobin must be higher than current hemoglobin")
        
        if not isinstance(iron_stores, int) or iron_stores < 0 or iron_stores > 1000:
            raise ValueError("Iron stores must be between 0 and 1000 mg")
    
    def _calculate_iron_deficit(self, body_weight: float, current_hemoglobin: float, 
                               target_hemoglobin: float, iron_stores: int) -> float:
        """
        Implements the Ganzoni equation mathematical formula
        
        Formula: Iron deficit (mg) = body weight (kg) × (target Hb - current Hb) (g/dL) × 2.4 + iron stores (mg)
        """
        
        # Calculate hemoglobin difference
        hb_difference = target_hemoglobin - current_hemoglobin
        
        # Apply Ganzoni formula
        iron_deficit = (body_weight * hb_difference * self.GANZONI_FACTOR) + iron_stores
        
        # Ensure minimum positive value
        iron_deficit = max(iron_deficit, 0)
        
        return iron_deficit
    
    def _get_interpretation(self, iron_deficit: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on iron deficit
        
        Args:
            iron_deficit (float): Calculated iron deficit in mg
            
        Returns:
            Dict with interpretation
        """
        
        if iron_deficit < 500:
            return {
                "stage": "Mild Deficit",
                "description": "Small iron deficit",
                "interpretation": (f"Total iron deficit of {iron_deficit:.1f} mg indicates mild iron deficiency. "
                                f"Consider oral iron therapy (ferrous sulfate 325 mg 2-3 times daily) if well tolerated, "
                                f"or single IV iron infusion (iron sucrose 200-300 mg or ferric carboxymaltose 500 mg). "
                                f"Monitor hemoglobin response in 2-4 weeks. Reassess iron parameters after 3 months.")
            }
        elif iron_deficit < 1000:
            return {
                "stage": "Moderate Deficit",
                "description": "Moderate iron deficit",
                "interpretation": (f"Total iron deficit of {iron_deficit:.1f} mg indicates moderate iron deficiency requiring "
                                f"iron replacement therapy. IV iron is preferred if oral iron not tolerated or malabsorption suspected. "
                                f"Consider iron sucrose 200 mg weekly × 3-5 doses, or ferric carboxymaltose 500-1000 mg in 1-2 doses. "
                                f"Monitor hemoglobin every 2 weeks initially, then monthly. Check iron studies after 1 month.")
            }
        elif iron_deficit < 2000:
            return {
                "stage": "Severe Deficit",
                "description": "Significant iron deficit",
                "interpretation": (f"Total iron deficit of {iron_deficit:.1f} mg indicates significant iron deficiency requiring "
                                f"IV iron replacement therapy in divided doses. Oral iron unlikely to be sufficient. "
                                f"Consider high-dose ferric carboxymaltose 1000 mg followed by 500-1000 mg in 1-2 weeks, "
                                f"or iron sucrose 200 mg weekly × 5-8 doses. Monitor for iron overload. Check hemoglobin "
                                f"weekly initially, iron studies monthly.")
            }
        else:
            return {
                "stage": "Very Severe Deficit",
                "description": "Very large iron deficit",
                "interpretation": (f"Total iron deficit of {iron_deficit:.1f} mg indicates very severe iron deficiency requiring "
                                f"high-dose IV iron replacement therapy administered over multiple sessions. Investigate underlying "
                                f"cause of severe iron loss. Consider ferric carboxymaltose 1000 mg every 1-2 weeks × 2-3 doses, "
                                f"or iron sucrose 200 mg twice weekly × 6-10 doses. Close monitoring essential to prevent iron "
                                f"overload. Weekly hemoglobin, monthly iron studies and ferritin. Hematology consultation recommended.")
            }


def calculate_ganzoni_equation_iron_deficiency(body_weight: float, current_hemoglobin: float, 
                                             target_hemoglobin: float, iron_stores: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ganzoni_equation_iron_deficiency pattern
    """
    calculator = GanzoniEquationIronDeficiencyCalculator()
    return calculator.calculate(body_weight, current_hemoglobin, target_hemoglobin, iron_stores)