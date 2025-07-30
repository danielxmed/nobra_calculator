"""
Cardiac Power Output (CPO) Calculator

Calculates cardiac power output, the rate of energy output of the heart.
Integrates both pressure and flow components of cardiac work.

References:
1. Tan LB. Cardiac pumping capability and prognosis in heart failure. 
   Lancet. 1986 Dec 13;2(8520):1360-3. doi: 10.1016/s0140-6736(86)92002-6.
2. Fincke R, Hochman JS, Lowe AM, et al. Cardiac power is the strongest 
   hemodynamic correlate of mortality in cardiogenic shock: a report from 
   the SHOCK trial registry. J Am Coll Cardiol. 2004 Jul 21;44(2):340-8.
3. Mendoza DD, Cooper HA, Panza JA. Cardiac power output predicts mortality 
   across a broad spectrum of patients with acute cardiac disease. 
   Am Heart J. 2007 Mar;153(3):366-70.
"""

from typing import Dict, Any, Optional


class CardiacPowerOutputCalculator:
    """Calculator for Cardiac Power Output"""
    
    def __init__(self):
        # Conversion constant for CPO calculation
        self.CONVERSION_CONSTANT = 451
        
        # Clinical thresholds
        self.SEVERE_DYSFUNCTION_THRESHOLD = 0.6  # Watts
        self.NORMAL_RESTING_CPO = 1.0  # Watts
        self.MAX_EXERCISE_CPO = 6.0  # Watts
    
    def calculate(
        self,
        mean_arterial_pressure: float,
        cardiac_output: float,
        right_atrial_pressure: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates cardiac power output using standard and original formulas
        
        Args:
            mean_arterial_pressure: Mean arterial pressure in mmHg
            cardiac_output: Cardiac output in L/min
            right_atrial_pressure: Right atrial pressure in mmHg (optional)
            
        Returns:
            Dict with CPO results and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(mean_arterial_pressure, cardiac_output, right_atrial_pressure)
        
        # Calculate standard CPO (without RAP)
        cpo_standard = self._calculate_standard_cpo(mean_arterial_pressure, cardiac_output)
        
        # Calculate original Tan CPO (with RAP) if RAP provided
        cpo_original = None
        if right_atrial_pressure is not None:
            cpo_original = self._calculate_original_cpo(
                mean_arterial_pressure, cardiac_output, right_atrial_pressure
            )
        
        # Get clinical interpretation
        primary_cpo = cpo_original if cpo_original is not None else cpo_standard
        interpretation = self._get_interpretation(primary_cpo)
        
        # Prepare results
        result = {
            "cpo_standard": round(cpo_standard, 3),
            "cpo_original": round(cpo_original, 3) if cpo_original is not None else None,
            "primary_cpo": round(primary_cpo, 3),
            "formula_used": "Original Tan (with RAP)" if cpo_original is not None else "Standard (without RAP)"
        }
        
        return {
            "result": result,
            "unit": "Watts",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, map_value: float, co: float, rap: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(map_value, (int, float)):
            raise ValueError("Mean arterial pressure must be a number")
        
        if not isinstance(co, (int, float)):
            raise ValueError("Cardiac output must be a number")
        
        if not (30.0 <= map_value <= 200.0):
            raise ValueError("Mean arterial pressure must be between 30-200 mmHg")
        
        if not (1.0 <= co <= 15.0):
            raise ValueError("Cardiac output must be between 1.0-15.0 L/min")
        
        if rap is not None:
            if not isinstance(rap, (int, float)):
                raise ValueError("Right atrial pressure must be a number")
            
            if not (0.0 <= rap <= 30.0):
                raise ValueError("Right atrial pressure must be between 0-30 mmHg")
            
            if rap >= map_value:
                raise ValueError("Right atrial pressure must be less than mean arterial pressure")
    
    def _calculate_standard_cpo(self, map_value: float, co: float) -> float:
        """Calculates standard CPO without RAP component"""
        return (map_value * co) / self.CONVERSION_CONSTANT
    
    def _calculate_original_cpo(self, map_value: float, co: float, rap: float) -> float:
        """Calculates original Tan CPO with RAP component"""
        return ((map_value - rap) * co) / self.CONVERSION_CONSTANT
    
    def _get_interpretation(self, cpo: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on CPO value
        
        Args:
            cpo: Cardiac power output in Watts
            
        Returns:
            Dict with clinical interpretation
        """
        
        if cpo < self.SEVERE_DYSFUNCTION_THRESHOLD:
            return {
                "stage": "Severe dysfunction",
                "description": "Severe ventricular dysfunction",
                "interpretation": f"CPO {cpo:.3f}W indicates severe ventricular dysfunction with poor prognosis. High risk for mortality in cardiogenic shock. Consider aggressive interventions including mechanical circulatory support, inotropic therapy, and close hemodynamic monitoring."
            }
        elif cpo < self.NORMAL_RESTING_CPO:
            return {
                "stage": "Moderately reduced",
                "description": "Moderately reduced cardiac power",
                "interpretation": f"CPO {cpo:.3f}W indicates moderately reduced cardiac function. Monitor closely and optimize medical therapy. Consider inotropic support and evaluate for underlying causes of reduced cardiac performance."
            }
        else:
            if cpo <= self.MAX_EXERCISE_CPO:
                return {
                    "stage": "Normal to high",
                    "description": "Normal to high cardiac power",
                    "interpretation": f"CPO {cpo:.3f}W indicates adequate cardiac function. Normal resting CPO is approximately 1.0W. This level suggests good cardiac reserve and adequate hemodynamic function."
                }
            else:
                return {
                    "stage": "Very high",
                    "description": "Very high cardiac power",
                    "interpretation": f"CPO {cpo:.3f}W is exceptionally high (>6W typical exercise maximum). Consider hyperdynamic state, measurement error, or extreme physiological conditions."
                }


def calculate_cardiac_power_output(
    mean_arterial_pressure: float,
    cardiac_output: float,
    right_atrial_pressure: Optional[float] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CardiacPowerOutputCalculator()
    return calculator.calculate(
        mean_arterial_pressure=mean_arterial_pressure,
        cardiac_output=cardiac_output,
        right_atrial_pressure=right_atrial_pressure
    )