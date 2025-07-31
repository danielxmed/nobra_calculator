"""
Naloxone Drip Dosing Calculator

Calculates continuous IV infusion rate for naloxone in acute opioid overdose,
based on the initial effective bolus dose.
"""

from typing import Dict, Any


class NaloxoneDripDosingCalculator:
    """Calculator for Naloxone Drip Dosing"""
    
    def __init__(self):
        # Formula constant - 2/3 of bolus dose per hour
        self.INFUSION_FACTOR = 2.0 / 3.0
        
        # Validation limits
        self.MIN_BOLUS_DOSE = 0.1  # mg
        self.MAX_BOLUS_DOSE = 10.0  # mg
    
    def calculate(self, bolus_dose: float) -> Dict[str, Any]:
        """
        Calculates naloxone continuous IV infusion rate
        
        Args:
            bolus_dose (float): Total naloxone dose required in the first hour
                               to achieve adequate reversal (mg)
            
        Returns:
            Dict with infusion rate and additional clinical guidance
        """
        
        # Validate input
        self._validate_inputs(bolus_dose)
        
        # Calculate infusion rate
        infusion_rate = self._calculate_infusion_rate(bolus_dose)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(infusion_rate, bolus_dose)
        
        # Calculate additional bolus dose (half of initial dose at 15 minutes)
        additional_bolus = round(bolus_dose / 2, 2)
        
        return {
            "result": infusion_rate,
            "unit": "mg/hr",
            "interpretation": interpretation,
            "additional_bolus_at_15_min": additional_bolus,
            "additional_bolus_unit": "mg"
        }
    
    def _validate_inputs(self, bolus_dose: float):
        """Validates input parameters"""
        
        if not isinstance(bolus_dose, (int, float)):
            raise ValueError("Bolus dose must be a number")
        
        if bolus_dose < self.MIN_BOLUS_DOSE or bolus_dose > self.MAX_BOLUS_DOSE:
            raise ValueError(
                f"Bolus dose must be between {self.MIN_BOLUS_DOSE} and "
                f"{self.MAX_BOLUS_DOSE} mg"
            )
    
    def _calculate_infusion_rate(self, bolus_dose: float) -> float:
        """
        Calculates the continuous IV infusion rate
        
        Formula: Infusion rate (mg/hr) = (2/3) × bolus dose (mg)
        """
        
        infusion_rate = self.INFUSION_FACTOR * bolus_dose
        
        # Round to 2 decimal places for practical dosing
        return round(infusion_rate, 2)
    
    def _get_interpretation(self, infusion_rate: float, bolus_dose: float) -> str:
        """
        Provides clinical interpretation and guidance
        
        Args:
            infusion_rate (float): Calculated infusion rate in mg/hr
            bolus_dose (float): Initial bolus dose in mg
            
        Returns:
            str: Clinical interpretation and management guidance
        """
        
        additional_bolus = round(bolus_dose / 2, 2)
        
        interpretation = (
            f"Start continuous IV infusion at {infusion_rate} mg/hr. "
            f"Administer {additional_bolus} mg bolus (half of initial dose) "
            f"15 minutes after starting the infusion to prevent drop in naloxone levels. "
            f"Titrate infusion rate based on:\n"
            f"- Respiratory rate (maintain >12/min)\n"
            f"- Oxygen saturation\n"
            f"- Level of consciousness\n\n"
            f"Decrease rate if withdrawal symptoms occur. "
            f"Monitor closely as naloxone half-life (30-100 min) is shorter than most opioids. "
            f"Consider ICU admission for continuous monitoring."
        )
        
        # Add high-dose warning if appropriate
        if bolus_dose >= 2:
            interpretation += (
                f"\n\nNote: High initial bolus dose ({bolus_dose} mg) suggests "
                f"possible synthetic opioid exposure (e.g., fentanyl). "
                f"Be prepared for prolonged infusion requirements and potential "
                f"need for dose escalation."
            )
        
        return interpretation


def calculate_naloxone_drip_dosing(bolus_dose: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NaloxoneDripDosingCalculator()
    return calculator.calculate(bolus_dose)