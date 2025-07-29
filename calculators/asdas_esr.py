"""
Ankylosing Spondylitis Disease Activity Score with ESR (ASDAS-ESR) Calculator

Stratifies severity of ankylosing spondylitis (AS) using clinical and laboratory data, specifically ESR.

References:
- Lukas C, et al. Development of an ASAS-endorsed disease activity score (ASDAS) in patients with ankylosing spondylitis. Ann Rheum Dis. 2009;68(1):18-24.
- van der Heijde D, et al. ASDAS, a highly discriminatory ASAS-endorsed disease activity score in patients with ankylosing spondylitis. Ann Rheum Dis. 2009;68(12):1811-8.
- Machado P, et al. Ankylosing Spondylitis Disease Activity Score (ASDAS): defining cut-off values for disease activity states and improvement scores. Ann Rheum Dis. 2011;70(1):47-53.
"""

import math
from typing import Dict, Any


class AsdasEsrCalculator:
    """Calculator for ASDAS-ESR (Ankylosing Spondylitis Disease Activity Score with ESR)"""
    
    def __init__(self):
        # Formula coefficients
        self.BACK_PAIN_COEFF = 0.08
        self.MORNING_STIFFNESS_COEFF = 0.07
        self.PATIENT_GLOBAL_COEFF = 0.11
        self.PERIPHERAL_PAIN_COEFF = 0.09
        self.ESR_COEFF = 0.29
    
    def calculate(self, back_pain: int, morning_stiffness: int, patient_global: int, 
                 peripheral_pain: int, esr: int) -> Dict[str, Any]:
        """
        Calculates the ASDAS-ESR score using the provided parameters
        
        Args:
            back_pain (int): Overall level of AS neck, back, or hip pain (0-10)
            morning_stiffness (int): Overall level of morning stiffness (0-10)
            patient_global (int): Patient global assessment of disease activity (0-10)
            peripheral_pain (int): Overall level of peripheral pain/swelling (0-10)
            esr (int): Erythrocyte Sedimentation Rate (mm/hr)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(back_pain, morning_stiffness, patient_global, peripheral_pain, esr)
        
        # Calculation logic
        result = self._calculate_formula(back_pain, morning_stiffness, patient_global, peripheral_pain, esr)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, back_pain: int, morning_stiffness: int, patient_global: int, 
                        peripheral_pain: int, esr: int):
        """Validates input parameters"""
        
        # Validate back pain
        if not isinstance(back_pain, int) or back_pain < 0 or back_pain > 10:
            raise ValueError("Back pain must be an integer between 0 and 10")
        
        # Validate morning stiffness
        if not isinstance(morning_stiffness, int) or morning_stiffness < 0 or morning_stiffness > 10:
            raise ValueError("Morning stiffness must be an integer between 0 and 10")
        
        # Validate patient global
        if not isinstance(patient_global, int) or patient_global < 0 or patient_global > 10:
            raise ValueError("Patient global assessment must be an integer between 0 and 10")
        
        # Validate peripheral pain
        if not isinstance(peripheral_pain, int) or peripheral_pain < 0 or peripheral_pain > 10:
            raise ValueError("Peripheral pain must be an integer between 0 and 10")
        
        # Validate ESR
        if not isinstance(esr, int) or esr < 0 or esr > 200:
            raise ValueError("ESR must be an integer between 0 and 200 mm/hr")
    
    def _calculate_formula(self, back_pain: int, morning_stiffness: int, patient_global: int, 
                          peripheral_pain: int, esr: int) -> float:
        """Implements the ASDAS-ESR mathematical formula"""
        
        # ASDAS-ESR = 0.08 × Back Pain + 0.07 × Duration of Morning Stiffness + 
        #             0.11 × Patient Global + 0.09 × Peripheral Pain/Swelling + 0.29 × √(ESR)
        
        result = (self.BACK_PAIN_COEFF * back_pain + 
                 self.MORNING_STIFFNESS_COEFF * morning_stiffness + 
                 self.PATIENT_GLOBAL_COEFF * patient_global + 
                 self.PERIPHERAL_PAIN_COEFF * peripheral_pain + 
                 self.ESR_COEFF * math.sqrt(esr))
        
        # Round to 2 decimal places
        return round(result, 2)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (float): Calculated ASDAS-ESR value
            
        Returns:
            Dict with interpretation
        """
        
        if result < 1.3:
            return {
                "stage": "Inactive",
                "description": "Inactive disease",
                "interpretation": "Disease activity is inactive. Patient has minimal symptoms and inflammation markers are low. Continue current management and monitor regularly."
            }
        elif result < 2.1:
            return {
                "stage": "Moderate",
                "description": "Moderate disease activity",
                "interpretation": "Disease activity is moderate. Consider optimization of current therapy or initiation of biological therapy if not already on treatment. Monitor closely for response."
            }
        elif result < 3.5:
            return {
                "stage": "High",
                "description": "High disease activity",
                "interpretation": "Disease activity is high. Strongly consider biological therapy if not already initiated. Increase monitoring frequency and assess treatment response regularly."
            }
        else:
            return {
                "stage": "Very High",
                "description": "Very high disease activity",
                "interpretation": "Disease activity is very high. Urgent consideration for biological therapy or switching to alternative biological agent if already on treatment. Close monitoring and rapid treatment optimization required."
            }


def calculate_asdas_esr(back_pain: int, morning_stiffness: int, patient_global: int, 
                       peripheral_pain: int, esr: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_asdas_esr pattern
    """
    calculator = AsdasEsrCalculator()
    return calculator.calculate(back_pain, morning_stiffness, patient_global, peripheral_pain, esr)