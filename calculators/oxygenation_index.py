"""
Oxygenation Index Calculator

Predicts outcomes and assists in treatment decisions for pediatric patients 
with acute respiratory failure. This tool helps determine the need for 
extracorporeal membrane oxygenation (ECMO) and assesses respiratory failure severity.

References:
1. Ortega M, Ramos AD, Platzker AC, Atkinson JB, Bowman CM, Laks H, et al. 
   Early prediction of ultimate outcome in newborn infants with severe 
   respiratory failure. J Pediatr. 1988;113(4):744-7. 
   doi: 10.1016/s0022-3476(88)80394-8.
2. Bartlett RH, Roloff DW, Custer JR, Younger JG, Hirschl RB. Extracorporeal 
   life support: the University of Michigan experience. JAMA. 2000;283(7):904-8. 
   doi: 10.1001/jama.283.7.904.
"""

from typing import Dict, Any


class OxygenationIndexCalculator:
    """Calculator for Oxygenation Index"""
    
    def __init__(self):
        # Interpretation thresholds
        self.GOOD_OUTCOME_THRESHOLD = 25
        self.ECMO_CONSIDERATION_THRESHOLD = 40
        
        # Validation ranges
        self.MIN_FIO2 = 21.0
        self.MAX_FIO2 = 100.0
        self.MIN_MEAN_AIRWAY_PRESSURE = 1.0
        self.MAX_MEAN_AIRWAY_PRESSURE = 50.0
        self.MIN_PAO2 = 20.0
        self.MAX_PAO2 = 600.0
    
    def calculate(self, fio2: float, mean_airway_pressure: float, pao2: float) -> Dict[str, Any]:
        """
        Calculates the Oxygenation Index
        
        Args:
            fio2 (float): Fraction of inspired oxygen as percentage (21-100%)
            mean_airway_pressure (float): Mean airway pressure in cmH2O
            pao2 (float): Partial pressure of arterial oxygen in mmHg
            
        Returns:
            Dict with the oxygenation index and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(fio2, mean_airway_pressure, pao2)
        
        # Calculate oxygenation index
        # Formula: OI = (FiO2 × Mean Airway Pressure) ÷ PaO2
        oxygenation_index = (fio2 * mean_airway_pressure) / pao2
        
        # Round to 1 decimal place
        oxygenation_index = round(oxygenation_index, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(oxygenation_index)
        
        return {
            "result": oxygenation_index,
            "unit": "index",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fio2: float, mean_airway_pressure: float, pao2: float):
        """Validates input parameters"""
        
        if not isinstance(fio2, (int, float)):
            raise ValueError("FiO2 must be a number")
        
        if not isinstance(mean_airway_pressure, (int, float)):
            raise ValueError("Mean airway pressure must be a number")
        
        if not isinstance(pao2, (int, float)):
            raise ValueError("PaO2 must be a number")
        
        if fio2 < self.MIN_FIO2 or fio2 > self.MAX_FIO2:
            raise ValueError(f"FiO2 must be between {self.MIN_FIO2}% and {self.MAX_FIO2}%")
        
        if mean_airway_pressure < self.MIN_MEAN_AIRWAY_PRESSURE or mean_airway_pressure > self.MAX_MEAN_AIRWAY_PRESSURE:
            raise ValueError(f"Mean airway pressure must be between {self.MIN_MEAN_AIRWAY_PRESSURE} and {self.MAX_MEAN_AIRWAY_PRESSURE} cmH2O")
        
        if pao2 < self.MIN_PAO2 or pao2 > self.MAX_PAO2:
            raise ValueError(f"PaO2 must be between {self.MIN_PAO2} and {self.MAX_PAO2} mmHg")
        
        if pao2 <= 0:
            raise ValueError("PaO2 must be greater than 0 to avoid division by zero")
    
    def _get_interpretation(self, oxygenation_index: float) -> Dict[str, str]:
        """
        Determines the interpretation based on oxygenation index value
        
        Args:
            oxygenation_index (float): Calculated oxygenation index
            
        Returns:
            Dict with interpretation details
        """
        
        if oxygenation_index < self.GOOD_OUTCOME_THRESHOLD:
            return {
                "stage": "Good Outcome",
                "description": "Low risk respiratory failure",
                "interpretation": f"GOOD OUTCOME PREDICTED (OI: {oxygenation_index}): Low-risk respiratory failure "
                                f"with good prognosis. MANAGEMENT: Continue conventional mechanical ventilation "
                                f"and standard medical management. Monitor closely for improvement. "
                                f"PROGNOSIS: Excellent with conventional therapy. Weaning and extubation "
                                f"planning appropriate. MONITORING: Serial OI measurements to track progress. "
                                f"Consider lung protective ventilation strategies and supportive care optimization."
            }
        elif oxygenation_index < self.ECMO_CONSIDERATION_THRESHOLD:
            return {
                "stage": "High Risk",
                "description": "Moderate to severe respiratory failure",
                "interpretation": f"HIGH-RISK RESPIRATORY FAILURE (OI: {oxygenation_index}): Mortality risk >40%. "
                                f"MANAGEMENT: Optimize mechanical ventilation with lung protective strategies, "
                                f"consider advanced modes (HFOV, pressure control), maximize medical management. "
                                f"PREPARATION: Prepare for potential ECMO consultation if OI trends upward. "
                                f"MONITORING: Serial measurements every 6-12 hours, assess for reversible causes. "
                                f"CONSULTATION: Consider ECMO center consultation for guidance and transfer planning."
            }
        else:  # OI >= 40
            return {
                "stage": "ECMO Consideration",
                "description": "Severe respiratory failure",
                "interpretation": f"SEVERE RESPIRATORY FAILURE - ECMO CONSIDERATION (OI: {oxygenation_index}): "
                                f"Strong indication for ECMO evaluation. IMMEDIATE ACTION: Contact ECMO center "
                                f"for urgent consultation and possible transfer. CRITERIA: Sustained OI ≥40 "
                                f"(typically 3 of 5 measurements over 30-60 minutes) meets standard ECMO criteria. "
                                f"MANAGEMENT: Optimize current support while arranging ECMO evaluation. "
                                f"TIMING: Early ECMO consultation critical - outcomes better with earlier intervention. "
                                f"MONITORING: Continuous assessment of reversibility and other organ function."
            }


def calculate_oxygenation_index(fio2: float, mean_airway_pressure: float, pao2: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OxygenationIndexCalculator()
    return calculator.calculate(fio2, mean_airway_pressure, pao2)