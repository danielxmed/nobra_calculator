"""
Fetal Biophysical Profile (BPP) Score Calculator

Predicts need for urgent delivery based on sonographic and non-stress test. 
Assesses for fetal distress in high-risk pregnancies.

References:
- Manning FA, et al. Antepartum fetal evaluation: development of a fetal 
  biophysical profile. Am J Obstet Gynecol. 1980;136(6):787-95.
"""

import math
from typing import Dict, Any


class FetalBppScoreCalculator:
    """Calculator for Fetal Biophysical Profile Score"""
    
    def __init__(self):
        # No constants needed for this calculator
        pass
    
    def calculate(self, fetal_breathing: int, fetal_movement: int, fetal_tone: int, 
                 amniotic_fluid: int, nonstress_test: int) -> Dict[str, Any]:
        """
        Calculates the BPP score using the provided parameters
        
        Args:
            fetal_breathing (int): Fetal breathing movements (0 or 2)
            fetal_movement (int): Gross body movements (0 or 2)
            fetal_tone (int): Fetal muscle tone (0 or 2)
            amniotic_fluid (int): Amniotic fluid volume (0 or 2)
            nonstress_test (int): Non-stress test result (0 or 2)
            
        Returns:
            Dict with the BPP score and interpretation
        """
        
        # Validations
        self._validate_inputs(fetal_breathing, fetal_movement, fetal_tone, 
                           amniotic_fluid, nonstress_test)
        
        # Calculate BPP score
        result = self._calculate_bpp(fetal_breathing, fetal_movement, fetal_tone,
                                    amniotic_fluid, nonstress_test)
        
        # Get interpretation
        interpretation = self._get_interpretation(result, amniotic_fluid)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, fetal_breathing, fetal_movement, fetal_tone, 
                        amniotic_fluid, nonstress_test):
        """Validates input parameters"""
        
        # All parameters must be either 0 or 2
        valid_values = [0, 2]
        
        if fetal_breathing not in valid_values:
            raise ValueError("Fetal breathing must be 0 or 2")
        
        if fetal_movement not in valid_values:
            raise ValueError("Fetal movement must be 0 or 2")
        
        if fetal_tone not in valid_values:
            raise ValueError("Fetal tone must be 0 or 2")
        
        if amniotic_fluid not in valid_values:
            raise ValueError("Amniotic fluid must be 0 or 2")
        
        if nonstress_test not in valid_values:
            raise ValueError("Non-stress test must be 0 or 2")
    
    def _calculate_bpp(self, fetal_breathing, fetal_movement, fetal_tone,
                      amniotic_fluid, nonstress_test):
        """Calculates the BPP score by summing all parameters"""
        
        # Simple sum of all parameters
        result = fetal_breathing + fetal_movement + fetal_tone + amniotic_fluid + nonstress_test
        
        return result
    
    def _get_interpretation(self, result: int, amniotic_fluid: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the BPP score
        
        Args:
            result (int): BPP score (0-10)
            amniotic_fluid (int): Amniotic fluid score (0 or 2)
            
        Returns:
            Dict with interpretation
        """
        
        if result == 10:
            return {
                "stage": "Normal",
                "description": "Low risk",
                "interpretation": "Normal, non-asphyxiated fetus. No intervention required. Repeat test weekly."
            }
        elif result == 8:
            # Special case for score of 8 depends on amniotic fluid
            if amniotic_fluid == 0:
                return {
                    "stage": "Normal with Oligohydramnios",
                    "description": "Low risk with caution",
                    "interpretation": "Normal, non-asphyxiated fetus but with oligohydramnios. Consider delivery evaluation. Repeat test per protocol."
                }
            else:
                return {
                    "stage": "Normal",
                    "description": "Low risk",
                    "interpretation": "Normal, non-asphyxiated fetus. No intervention required. Repeat test per protocol."
                }
        elif result == 6:
            return {
                "stage": "Possible Asphyxia",
                "description": "Equivocal",
                "interpretation": "Possible fetal asphyxia. If abnormal fluid, delivery indicated. If normal fluid, repeat test in 24 hours."
            }
        elif result == 4:
            return {
                "stage": "Probable Asphyxia",
                "description": "High risk",
                "interpretation": "Probable fetal asphyxia. Repeat testing immediately. If persistent, delivery indicated."
            }
        else:  # result <= 2
            return {
                "stage": "Almost Certain Asphyxia",
                "description": "High risk",
                "interpretation": "Almost certain fetal asphyxia. Immediate delivery indicated."
            }


def calculate_fetal_bpp_score(fetal_breathing, fetal_movement, fetal_tone, 
                             amniotic_fluid, nonstress_test) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FetalBppScoreCalculator()
    return calculator.calculate(fetal_breathing, fetal_movement, fetal_tone,
                              amniotic_fluid, nonstress_test)