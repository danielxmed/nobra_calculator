"""
Transtubular Potassium Gradient (TTKG) Calculator

Evaluates renal potassium handling in patients with hyperkalemia or hypokalemia.

References:
1. Ethier JH, Kamel KS, Magner PO, Lemann J Jr, Halperin ML. The transtubular 
   potassium concentration in patients with hypokalemia and hyperkalemia. 
   Am J Kidney Dis. 1990 Apr;15(4):309-15.
2. Choi MJ, Ziyadeh FN. The utility of the transtubular potassium gradient 
   in the evaluation of hyperkalemia. J Am Soc Nephrol. 2008 Mar;19(3):424-6.
"""

from typing import Dict, Any


class TtkgCalculator:
    """Calculator for Transtubular Potassium Gradient"""
    
    def __init__(self):
        # Normal serum potassium range
        self.NORMAL_K_MIN = 3.5
        self.NORMAL_K_MAX = 5.0
        
        # TTKG thresholds
        self.NORMAL_TTKG_MIN = 8
        self.NORMAL_TTKG_MAX = 9
        self.HYPERKALEMIA_THRESHOLD = 7
        self.HYPOKALEMIA_THRESHOLD = 3
    
    def calculate(self, urine_potassium: float, serum_potassium: float, 
                  urine_osmolality: float, serum_osmolality: float) -> Dict[str, Any]:
        """
        Calculates the Transtubular Potassium Gradient (TTKG)
        
        Formula: TTKG = (Urine K × Serum osmolality) / (Serum K × Urine osmolality)
        
        Args:
            urine_potassium (float): Urine potassium in mEq/L
            serum_potassium (float): Serum potassium in mEq/L
            urine_osmolality (float): Urine osmolality in mOsm/kg
            serum_osmolality (float): Serum osmolality in mOsm/kg
            
        Returns:
            Dict with TTKG result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(urine_potassium, serum_potassium, 
                            urine_osmolality, serum_osmolality)
        
        # Check validity conditions
        validity_warning = self._check_validity_conditions(urine_osmolality, serum_osmolality)
        
        # Calculate TTKG
        ttkg = self._calculate_ttkg(urine_potassium, serum_potassium, 
                                   urine_osmolality, serum_osmolality)
        
        # Get interpretation based on serum potassium level
        interpretation_data = self._get_interpretation(ttkg, serum_potassium)
        
        # Add validity warning if applicable
        if validity_warning:
            interpretation_data["interpretation"] = (
                f"WARNING: {validity_warning}. " + interpretation_data["interpretation"]
            )
        
        return {
            "result": ttkg,
            "unit": "",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"],
            "potassium_status": interpretation_data["potassium_status"]
        }
    
    def _validate_inputs(self, urine_k: float, serum_k: float, 
                        urine_osm: float, serum_osm: float):
        """Validates input parameters"""
        
        if urine_k <= 0:
            raise ValueError("Urine potassium must be positive")
        
        if serum_k <= 0:
            raise ValueError("Serum potassium must be positive")
        
        if urine_osm <= 0:
            raise ValueError("Urine osmolality must be positive")
        
        if serum_osm <= 0:
            raise ValueError("Serum osmolality must be positive")
        
        # Range validations
        if not 1 <= urine_k <= 200:
            raise ValueError("Urine potassium must be between 1 and 200 mEq/L")
        
        if not 1.5 <= serum_k <= 10:
            raise ValueError("Serum potassium must be between 1.5 and 10 mEq/L")
        
        if not 50 <= urine_osm <= 1400:
            raise ValueError("Urine osmolality must be between 50 and 1400 mOsm/kg")
        
        if not 250 <= serum_osm <= 350:
            raise ValueError("Serum osmolality must be between 250 and 350 mOsm/kg")
    
    def _check_validity_conditions(self, urine_osm: float, serum_osm: float) -> str:
        """Check if conditions for valid TTKG are met"""
        
        if urine_osm <= serum_osm:
            return "Urine osmolality should exceed serum osmolality for accurate TTKG"
        
        return ""
    
    def _calculate_ttkg(self, urine_k: float, serum_k: float, 
                       urine_osm: float, serum_osm: float) -> float:
        """Calculate the TTKG value"""
        
        # TTKG = (Urine K × Serum osmolality) / (Serum K × Urine osmolality)
        ttkg = (urine_k * serum_osm) / (serum_k * urine_osm)
        
        # Round to 1 decimal place
        return round(ttkg, 1)
    
    def _get_interpretation(self, ttkg: float, serum_k: float) -> Dict[str, str]:
        """
        Determine interpretation based on TTKG and serum potassium
        
        Args:
            ttkg (float): Calculated TTKG value
            serum_k (float): Serum potassium level
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine potassium status
        if serum_k > self.NORMAL_K_MAX:
            potassium_status = "hyperkalemia"
            return self._interpret_hyperkalemia(ttkg)
        elif serum_k < self.NORMAL_K_MIN:
            potassium_status = "hypokalemia"
            return self._interpret_hypokalemia(ttkg)
        else:
            potassium_status = "normal"
            return self._interpret_normal(ttkg)
    
    def _interpret_hyperkalemia(self, ttkg: float) -> Dict[str, str]:
        """Interpret TTKG in context of hyperkalemia"""
        
        if ttkg >= self.HYPERKALEMIA_THRESHOLD:
            if ttkg >= 10:
                return {
                    "stage": "Appropriate Response",
                    "description": "Optimal renal K+ excretion in hyperkalemia",
                    "interpretation": (
                        f"TTKG of {ttkg} in hyperkalemia indicates excellent renal potassium "
                        "excretion. The kidneys are responding appropriately to elevated "
                        "potassium levels. Consider non-renal causes of hyperkalemia such as "
                        "increased potassium intake, transcellular shifts, or tissue breakdown."
                    ),
                    "potassium_status": "hyperkalemia"
                }
            else:
                return {
                    "stage": "Appropriate Response",
                    "description": "Normal renal K+ excretion in hyperkalemia",
                    "interpretation": (
                        f"TTKG of {ttkg} (≥7) in hyperkalemia indicates appropriate renal "
                        "potassium excretion. The kidneys are responding normally to elevated "
                        "potassium levels. Consider non-renal causes of hyperkalemia."
                    ),
                    "potassium_status": "hyperkalemia"
                }
        else:
            return {
                "stage": "Hypoaldosteronism",
                "description": "Impaired K+ excretion in hyperkalemia",
                "interpretation": (
                    f"TTKG of {ttkg} (<7) in hyperkalemia suggests hypoaldosteronism or "
                    "aldosterone resistance, indicating impaired renal potassium excretion. "
                    "Consider mineralocorticoid deficiency, medications affecting the RAAS "
                    "system (ACE inhibitors, ARBs, aldosterone antagonists), or type 4 RTA."
                ),
                "potassium_status": "hyperkalemia"
            }
    
    def _interpret_hypokalemia(self, ttkg: float) -> Dict[str, str]:
        """Interpret TTKG in context of hypokalemia"""
        
        if ttkg < self.HYPOKALEMIA_THRESHOLD:
            return {
                "stage": "Appropriate Response",
                "description": "Normal K+ conservation in hypokalemia",
                "interpretation": (
                    f"TTKG of {ttkg} (<3) in hypokalemia indicates appropriate renal "
                    "potassium conservation. The kidneys are responding normally by "
                    "minimizing urinary potassium losses. Consider extrarenal causes "
                    "of hypokalemia such as GI losses, poor intake, or transcellular shifts."
                ),
                "potassium_status": "hypokalemia"
            }
        else:
            return {
                "stage": "Renal K+ Wasting",
                "description": "Inappropriate K+ loss in hypokalemia",
                "interpretation": (
                    f"TTKG of {ttkg} (≥3) in hypokalemia suggests renal potassium wasting, "
                    "indicating inappropriate urinary potassium losses. Consider causes such "
                    "as hyperaldosteronism, diuretic use, magnesium depletion, Bartter/Gitelman "
                    "syndromes, or renal tubular acidosis (type 1 or 2)."
                ),
                "potassium_status": "hypokalemia"
            }
    
    def _interpret_normal(self, ttkg: float) -> Dict[str, str]:
        """Interpret TTKG with normal serum potassium"""
        
        if self.NORMAL_TTKG_MIN <= ttkg <= self.NORMAL_TTKG_MAX:
            return {
                "stage": "Normal",
                "description": "Normal TTKG",
                "interpretation": (
                    f"TTKG of {ttkg} with normal serum potassium is within the expected "
                    "range (8-9) for patients with a normal diet. This indicates appropriate "
                    "renal potassium handling."
                ),
                "potassium_status": "normal"
            }
        elif ttkg < self.NORMAL_TTKG_MIN:
            return {
                "stage": "Low Normal",
                "description": "Below normal TTKG",
                "interpretation": (
                    f"TTKG of {ttkg} with normal serum potassium is below the expected "
                    "range (8-9). This may indicate reduced potassium intake or mild "
                    "aldosterone deficiency. Monitor for development of hyperkalemia."
                ),
                "potassium_status": "normal"
            }
        else:
            return {
                "stage": "High Normal",
                "description": "Above normal TTKG",
                "interpretation": (
                    f"TTKG of {ttkg} with normal serum potassium is above the expected "
                    "range (8-9). This may indicate high potassium intake or increased "
                    "aldosterone activity. Monitor for development of hypokalemia."
                ),
                "potassium_status": "normal"
            }


def calculate_ttkg(urine_potassium: float, serum_potassium: float,
                   urine_osmolality: float, serum_osmolality: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TtkgCalculator()
    return calculator.calculate(urine_potassium, serum_potassium, 
                               urine_osmolality, serum_osmolality)