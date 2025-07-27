"""
A-a O₂ Gradient Calculator

Assesses degree of shunt and V/Q mismatch through the alveolar-arterial oxygen gradient.
Reference: Alveolar gas equation and respiratory physiology
"""

from typing import Dict, Any, Optional


class AAO2GradientCalculator:
    """Calculator for A-a O₂ Gradient"""
    
    def __init__(self):
        # Physiological constants
        self.DEFAULT_PATM = 760.0  # Atmospheric pressure at sea level (mmHg)
        self.PH2O = 47.0  # Water vapor pressure at 37°C (mmHg)
        self.DEFAULT_RQ = 0.8  # Standard respiratory quotient
    
    def calculate(self, age: int, fio2: float, paco2: float, pao2: float,
                 patm: Optional[float] = None, respiratory_quotient: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the alveolar-arterial oxygen gradient
        
        Args:
            age: Age in years
            fio2: Inspired oxygen fraction (0.21 for room air)
            paco2: Arterial CO₂ partial pressure (mmHg)
            pao2: Arterial O₂ partial pressure (mmHg)
            patm: Atmospheric pressure (default: 760 mmHg)
            respiratory_quotient: Respiratory quotient (default: 0.8)
            
        Returns:
            Dict with gradient result and interpretation
        """
        
        # Use default values if not provided
        if patm is None:
            patm = self.DEFAULT_PATM
        if respiratory_quotient is None:
            respiratory_quotient = self.DEFAULT_RQ
        
        # Validations
        self._validate_inputs(age, fio2, paco2, pao2, patm, respiratory_quotient)
        
        # Calculate PAO₂ (alveolar oxygen pressure) using alveolar gas equation
        pao2_alveolar = self._calculate_alveolar_oxygen(fio2, paco2, patm, respiratory_quotient)
        
        # Calculate A-a gradient
        aa_gradient = pao2_alveolar - pao2
        
        # Calculate age-adjusted normal gradient
        normal_gradient_age_adjusted = (age / 4.0) + 4.0
        
        # Get interpretation
        interpretation = self._get_interpretation(aa_gradient, age, normal_gradient_age_adjusted)
        
        return {
            "result": round(aa_gradient, 1),
            "unit": "mmHg",
            "pao2_alveolar": round(pao2_alveolar, 1),
            "age_adjusted_normal": round(normal_gradient_age_adjusted, 1),
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, fio2: float, paco2: float, pao2: float,
                        patm: float, respiratory_quotient: float):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 1 or age > 120:
            raise ValueError("Age must be an integer between 1 and 120 years")
        
        if not isinstance(fio2, (int, float)) or fio2 < 0.21 or fio2 > 1.0:
            raise ValueError("FiO₂ must be between 0.21 and 1.0")
        
        if not isinstance(paco2, (int, float)) or paco2 < 10.0 or paco2 > 100.0:
            raise ValueError("PaCO₂ must be between 10.0 and 100.0 mmHg")
        
        if not isinstance(pao2, (int, float)) or pao2 < 30.0 or pao2 > 600.0:
            raise ValueError("PaO₂ must be between 30.0 and 600.0 mmHg")
        
        if not isinstance(patm, (int, float)) or patm < 500.0 or patm > 800.0:
            raise ValueError("Atmospheric pressure must be between 500.0 and 800.0 mmHg")
        
        if not isinstance(respiratory_quotient, (int, float)) or respiratory_quotient < 0.7 or respiratory_quotient > 1.0:
            raise ValueError("Respiratory quotient must be between 0.7 and 1.0")
    
    def _calculate_alveolar_oxygen(self, fio2: float, paco2: float, patm: float, rq: float) -> float:
        """
        Calculates alveolar oxygen pressure using the alveolar gas equation
        
        PAO₂ = (Patm - PH₂O) × FiO₂ - PaCO₂/RQ
        
        Args:
            fio2: Inspired oxygen fraction
            paco2: Arterial CO₂ partial pressure
            patm: Atmospheric pressure
            rq: Respiratory quotient
            
        Returns:
            Alveolar oxygen pressure in mmHg
        """
        
        # Alveolar gas equation
        pao2_alveolar = (patm - self.PH2O) * fio2 - (paco2 / rq)
        
        return max(pao2_alveolar, 0.0)  # Ensure non-negative value
    
    def _get_interpretation(self, aa_gradient: float, age: int, 
                          normal_gradient_age_adjusted: float) -> Dict[str, str]:
        """
        Interprets the A-a gradient based on value and age
        
        Args:
            aa_gradient: Calculated gradient
            age: Patient's age
            normal_gradient_age_adjusted: Age-adjusted normal gradient
            
        Returns:
            Dict with interpretation
        """
        
        # Determine if it's within normal for age
        is_normal_for_age = aa_gradient <= normal_gradient_age_adjusted
        
        # Classification based on absolute ranges and age adjustment
        if aa_gradient <= 15 and is_normal_for_age:
            return {
                "stage": "Normal",
                "description": "Normal A-a gradient",
                "interpretation": f"A-a gradient of {aa_gradient:.1f} mmHg is within normal limits for age {age} years (expected ≤{normal_gradient_age_adjusted:.1f} mmHg). Preserved alveolar function."
            }
        elif aa_gradient <= 25 or (aa_gradient <= normal_gradient_age_adjusted * 1.5):
            return {
                "stage": "Slightly Elevated",
                "description": "Slightly elevated A-a gradient",
                "interpretation": f"A-a gradient of {aa_gradient:.1f} mmHg is slightly elevated (normal for age: ≤{normal_gradient_age_adjusted:.1f} mmHg). Suggests mild V/Q mismatch or minimal shunt. Consider mild atelectasis or early pulmonary edema."
            }
        elif aa_gradient <= 50:
            return {
                "stage": "Moderately Elevated",
                "description": "Moderately elevated A-a gradient",
                "interpretation": f"A-a gradient of {aa_gradient:.1f} mmHg is moderately elevated. Indicates moderate V/Q mismatch or shunt. Suggests significant lung disease such as pneumonia, pulmonary edema, or pulmonary embolism."
            }
        else:
            return {
                "stage": "Severely Elevated",
                "description": "Severely elevated A-a gradient",
                "interpretation": f"A-a gradient of {aa_gradient:.1f} mmHg is severely elevated. Indicates severe V/Q mismatch or significant shunt. Suggests severe lung disease such as ARDS, extensive pneumonia, or intracardiac shunt."
            }


def calculate_a_a_o2_gradient(age: int, fio2: float, paco2: float, pao2: float,
                             patm: Optional[float] = None, 
                             respiratory_quotient: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AAO2GradientCalculator()
    return calculator.calculate(age, fio2, paco2, pao2, patm, respiratory_quotient)
