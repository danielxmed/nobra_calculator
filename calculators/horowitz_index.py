"""
Horowitz Index for Lung Function (P/F Ratio) Calculator

Assesses lung function by calculating the ratio of arterial oxygen partial pressure 
to fraction of inspired oxygen, particularly useful in intubated patients.

References:
- Horovitz JH, et al. Arch Surg. 1974;108(3):349-55.
- ARDS Definition Task Force, Ranieri VM, et al. JAMA. 2012;307(23):2526-33.
"""

from typing import Dict, Any


class HorowitzIndexCalculator:
    """Calculator for Horowitz Index (P/F Ratio)"""
    
    def calculate(self, pao2: float, fio2: float) -> Dict[str, Any]:
        """
        Calculates the Horowitz Index (P/F ratio)
        
        Args:
            pao2 (float): Partial pressure of oxygen in arterial blood (mmHg)
            fio2 (float): Fraction of inspired oxygen (as decimal, e.g., 0.5 for 50%)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pao2, fio2)
        
        # Calculate P/F ratio
        pf_ratio = pao2 / fio2
        
        # Round to 1 decimal place
        pf_ratio = round(pf_ratio, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(pf_ratio)
        
        return {
            "result": pf_ratio,
            "unit": "mmHg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, pao2: float, fio2: float):
        """Validates input parameters"""
        
        if not isinstance(pao2, (int, float)):
            raise ValueError("PaO2 must be a number")
        
        if not isinstance(fio2, (int, float)):
            raise ValueError("FiO2 must be a number")
        
        if pao2 < 10 or pao2 > 700:
            raise ValueError("PaO2 must be between 10 and 700 mmHg")
        
        if fio2 < 0.21 or fio2 > 1.0:
            raise ValueError("FiO2 must be between 0.21 and 1.0 (as fraction, not percentage)")
    
    def _get_interpretation(self, pf_ratio: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the P/F ratio
        
        Args:
            pf_ratio (float): Calculated P/F ratio
            
        Returns:
            Dict with interpretation
        """
        
        if pf_ratio > 400:
            return {
                "stage": "Normal",
                "description": "P/F ratio >400",
                "interpretation": "Normal lung function. P/F ratio above 400 mmHg indicates "
                                "adequate oxygenation."
            }
        elif pf_ratio > 300:
            return {
                "stage": "Mild Impairment",
                "description": "P/F ratio 300-400",
                "interpretation": "Mild oxygenation impairment. Not consistent with ARDS but "
                                "indicates some degree of lung dysfunction."
            }
        elif pf_ratio > 200:
            return {
                "stage": "Mild ARDS",
                "description": "P/F ratio 200-300",
                "interpretation": "Mild ARDS according to Berlin criteria. Associated with "
                                "approximately 27% mortality. Consider lung protective "
                                "ventilation strategies."
            }
        elif pf_ratio > 100:
            return {
                "stage": "Moderate ARDS",
                "description": "P/F ratio 100-200",
                "interpretation": "Moderate ARDS according to Berlin criteria. Associated with "
                                "approximately 32% mortality. Implement lung protective "
                                "ventilation and consider prone positioning."
            }
        else:
            return {
                "stage": "Severe ARDS",
                "description": "P/F ratio ≤100",
                "interpretation": "Severe ARDS according to Berlin criteria. Associated with "
                                "approximately 45% mortality. Consider advanced therapies "
                                "including prone positioning, neuromuscular blockade, and "
                                "ECMO evaluation."
            }


def calculate_horowitz_index(pao2: float, fio2: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HorowitzIndexCalculator()
    return calculator.calculate(pao2, fio2)