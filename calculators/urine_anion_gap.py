"""
Urine Anion Gap Calculator

Detects urinary acidosis for evaluation of non-anion gap metabolic acidosis.
Helps differentiate between renal and extrarenal causes of normal anion gap 
metabolic acidosis by assessing urinary ammonium excretion capacity.

References:
- Goldstein MB, Bear R, Richardson RM, Marsden PA, Halperin ML. The urine anion gap: 
  a clinically useful index of ammonium excretion. Am J Med Sci. 1986;292(4):198-202.
- Kim GH, Han JS, Kim YS, Joo KW, Kim S, Lee JS. Evaluation of urine acidification 
  by urine anion gap versus urine osmolal gap in chronic metabolic acidosis. 
  Am J Kidney Dis. 2002;40(4):778-84.
"""

from typing import Dict, Any


class UrineAnionGapCalculator:
    """Calculator for Urine Anion Gap"""
    
    def __init__(self):
        # Clinical thresholds for interpretation (mEq/L)
        self.NEGATIVE_THRESHOLD = -10
        self.POSITIVE_THRESHOLD = 20
    
    def calculate(self, urine_sodium_meq_l: float, urine_potassium_meq_l: float, urine_chloride_meq_l: float) -> Dict[str, Any]:
        """
        Calculates the urine anion gap using urinary electrolyte concentrations
        
        Args:
            urine_sodium_meq_l (float): Urine sodium concentration in mEq/L (5-300)
            urine_potassium_meq_l (float): Urine potassium concentration in mEq/L (5-200)
            urine_chloride_meq_l (float): Urine chloride concentration in mEq/L (5-400)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(urine_sodium_meq_l, urine_potassium_meq_l, urine_chloride_meq_l)
        
        # Calculate urine anion gap
        urine_anion_gap = self._calculate_formula(urine_sodium_meq_l, urine_potassium_meq_l, urine_chloride_meq_l)
        
        # Get interpretation
        interpretation = self._get_interpretation(urine_anion_gap)
        
        return {
            "result": urine_anion_gap,
            "unit": "mEq/L",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, urine_sodium_meq_l: float, urine_potassium_meq_l: float, urine_chloride_meq_l: float):
        """Validates input parameters"""
        
        # Validate urine sodium
        if not isinstance(urine_sodium_meq_l, (int, float)) or urine_sodium_meq_l <= 0:
            raise ValueError("Urine sodium must be a positive number")
        if urine_sodium_meq_l < 5 or urine_sodium_meq_l > 300:
            raise ValueError("Urine sodium must be between 5 and 300 mEq/L")
        
        # Validate urine potassium
        if not isinstance(urine_potassium_meq_l, (int, float)) or urine_potassium_meq_l <= 0:
            raise ValueError("Urine potassium must be a positive number")
        if urine_potassium_meq_l < 5 or urine_potassium_meq_l > 200:
            raise ValueError("Urine potassium must be between 5 and 200 mEq/L")
        
        # Validate urine chloride
        if not isinstance(urine_chloride_meq_l, (int, float)) or urine_chloride_meq_l <= 0:
            raise ValueError("Urine chloride must be a positive number")
        if urine_chloride_meq_l < 5 or urine_chloride_meq_l > 400:
            raise ValueError("Urine chloride must be between 5 and 400 mEq/L")
    
    def _calculate_formula(self, urine_sodium_meq_l: float, urine_potassium_meq_l: float, urine_chloride_meq_l: float) -> float:
        """
        Implements the urine anion gap formula
        
        Formula: Urine Anion Gap = Na+ + K+ - Cl-
        
        The urine anion gap is an indirect measure of urinary ammonium excretion.
        A negative gap suggests high ammonium excretion (normal renal response to acidosis).
        A positive gap suggests low ammonium excretion (impaired renal acidification).
        """
        
        # Calculate urine anion gap
        urine_anion_gap = urine_sodium_meq_l + urine_potassium_meq_l - urine_chloride_meq_l
        
        # Round to 1 decimal place
        return round(urine_anion_gap, 1)
    
    def _get_interpretation(self, urine_anion_gap: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the urine anion gap value
        
        Args:
            urine_anion_gap (float): Calculated urine anion gap in mEq/L
            
        Returns:
            Dict with interpretation details
        """
        
        if urine_anion_gap < self.NEGATIVE_THRESHOLD:
            return {
                "stage": "Negative UAG",
                "description": "Extrarenal cause likely",
                "interpretation": f"Negative urine anion gap of {urine_anion_gap} mEq/L suggests an extrarenal cause of non-anion gap metabolic acidosis. This indicates adequate renal ammonium excretion, typically seen in GI bicarbonate losses (diarrhea, ureteroenteric fistulas). The kidney is appropriately responding to acidosis by increasing ammonium excretion to regenerate bicarbonate."
            }
        elif urine_anion_gap <= self.POSITIVE_THRESHOLD:
            return {
                "stage": "Normal UAG",
                "description": "Normal range",
                "interpretation": f"Normal urine anion gap of {urine_anion_gap} mEq/L (typical range -10 to +20 mEq/L). This range may be seen in healthy individuals or early stages of acid-base disorders. Clinical correlation is essential to determine significance in the context of metabolic acidosis."
            }
        else:
            return {
                "stage": "Positive UAG",
                "description": "Renal cause likely",
                "interpretation": f"Positive urine anion gap of {urine_anion_gap} mEq/L suggests a renal cause of non-anion gap metabolic acidosis. This indicates impaired renal ammonium excretion, typically seen in renal tubular acidosis (Type 1 distal RTA, Type 2 proximal RTA, Type 4 hyperkalemic RTA). The kidney is unable to adequately acidify urine or excrete ammonium despite systemic acidosis."
            }


def calculate_urine_anion_gap(urine_sodium_meq_l: float, urine_potassium_meq_l: float, urine_chloride_meq_l: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = UrineAnionGapCalculator()
    return calculator.calculate(urine_sodium_meq_l, urine_potassium_meq_l, urine_chloride_meq_l)