"""
Trauma Score and Injury Severity Score (TRISS) Calculator

Estimates the probability of survival for trauma patients based on physiological 
and anatomical parameters.

References:
1. Boyd CR, Tolson MA, Copes WS. Evaluating trauma care: the TRISS method. 
   Trauma Score and the Injury Severity Score. J Trauma. 1987;27(4):370-378.
2. Champion HR, Copes WS, Sacco WJ, et al. The Major Trauma Outcome Study: 
   establishing national norms for trauma care. J Trauma. 1990;30(11):1356-65.
"""

import math
from typing import Dict, Any


class TrissCalculator:
    """Calculator for Trauma Score and Injury Severity Score (TRISS)"""
    
    def __init__(self):
        # Coefficients for blunt trauma
        self.BLUNT_B0 = -1.2470
        self.BLUNT_B1 = 0.9544
        self.BLUNT_B2 = -0.0768
        self.BLUNT_B3 = -1.9052
        
        # Coefficients for penetrating trauma
        self.PENETRATING_B0 = -0.6029
        self.PENETRATING_B1 = 1.1430
        self.PENETRATING_B2 = -0.1516
        self.PENETRATING_B3 = -2.6676
    
    def calculate(self, trauma_type: str, rts_score: float, 
                  iss_score: int, age_over_54: str) -> Dict[str, Any]:
        """
        Calculates the probability of survival using TRISS
        
        Formula: Probability = 1/(1 + e^(-b))
        where b = b0 + b1(RTS) + b2(ISS) + b3(A)
        
        Args:
            trauma_type (str): Type of trauma (blunt or penetrating)
            rts_score (float): Revised Trauma Score (0-8)
            iss_score (int): Injury Severity Score (0-75)
            age_over_54 (str): Whether patient is over 54 years (yes/no)
            
        Returns:
            Dict with survival probability and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(trauma_type, rts_score, iss_score, age_over_54)
        
        # Calculate TRISS
        probability = self._calculate_probability(
            trauma_type, rts_score, iss_score, age_over_54
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(probability)
        
        return {
            "result": probability,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, trauma_type: str, rts_score: float, 
                        iss_score: int, age_over_54: str):
        """Validates input parameters"""
        
        # Validate trauma type
        if trauma_type not in ["blunt", "penetrating"]:
            raise ValueError("Trauma type must be 'blunt' or 'penetrating'")
        
        # Validate RTS score
        if not isinstance(rts_score, (int, float)):
            raise ValueError("RTS score must be a number")
        
        if not 0 <= rts_score <= 8:
            raise ValueError("RTS score must be between 0 and 8")
        
        # Validate ISS score
        if not isinstance(iss_score, int):
            raise ValueError("ISS score must be an integer")
        
        if not 0 <= iss_score <= 75:
            raise ValueError("ISS score must be between 0 and 75")
        
        # Validate age
        if age_over_54 not in ["yes", "no"]:
            raise ValueError("Age over 54 must be 'yes' or 'no'")
    
    def _calculate_probability(self, trauma_type: str, rts_score: float, 
                             iss_score: int, age_over_54: str) -> float:
        """Calculate the survival probability"""
        
        # Determine age factor
        age_factor = 1 if age_over_54 == "yes" else 0
        
        # Select coefficients based on trauma type
        if trauma_type == "blunt":
            b0 = self.BLUNT_B0
            b1 = self.BLUNT_B1
            b2 = self.BLUNT_B2
            b3 = self.BLUNT_B3
        else:  # penetrating
            b0 = self.PENETRATING_B0
            b1 = self.PENETRATING_B1
            b2 = self.PENETRATING_B2
            b3 = self.PENETRATING_B3
        
        # Calculate b value
        b = b0 + (b1 * rts_score) + (b2 * iss_score) + (b3 * age_factor)
        
        # Calculate probability of survival
        try:
            probability = 1 / (1 + math.exp(-b))
        except OverflowError:
            # Handle extreme values
            if b > 0:
                probability = 1.0
            else:
                probability = 0.0
        
        # Convert to percentage and round to 1 decimal place
        return round(probability * 100, 1)
    
    def _get_interpretation(self, probability: float) -> Dict[str, str]:
        """
        Determine interpretation based on survival probability
        
        Args:
            probability (float): Survival probability percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if probability >= 90:
            return {
                "stage": "Very High",
                "description": "Very high probability of survival",
                "interpretation": (
                    f"Patient has {probability}% probability of survival based on TRISS "
                    "calculation. Continue aggressive trauma care as indicated."
                )
            }
        elif probability >= 75:
            return {
                "stage": "High",
                "description": "High probability of survival",
                "interpretation": (
                    f"Patient has {probability}% probability of survival. Continue full "
                    "trauma resuscitation and care."
                )
            }
        elif probability >= 50:
            return {
                "stage": "Moderate",
                "description": "Moderate probability of survival",
                "interpretation": (
                    f"Patient has {probability}% probability of survival. Aggressive care "
                    "is warranted with close monitoring."
                )
            }
        elif probability >= 25:
            return {
                "stage": "Low",
                "description": "Low probability of survival",
                "interpretation": (
                    f"Patient has {probability}% probability of survival. Consider goals "
                    "of care discussion while continuing resuscitation efforts."
                )
            }
        else:
            return {
                "stage": "Very Low",
                "description": "Very low probability of survival",
                "interpretation": (
                    f"Patient has {probability}% probability of survival. Critical condition "
                    "requiring immediate intervention. Consider resource allocation and "
                    "family discussion."
                )
            }


def calculate_triss(trauma_type: str, rts_score: float, 
                   iss_score: int, age_over_54: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TrissCalculator()
    return calculator.calculate(trauma_type, rts_score, iss_score, age_over_54)