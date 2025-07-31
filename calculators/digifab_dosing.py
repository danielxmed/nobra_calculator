"""
DigiFab (Digibind) Dosing for Digoxin Poisoning Calculator

Doses DigiFab in patients with confirmed digoxin poisoning or overdose.

References:
1. Lapostolle F, Borron SW, Verdier C, et al. Digoxin-specific Fab fragments as single 
   first-line therapy in digitalis poisoning. Crit Care Med. 2008;36(11):3014-8.
2. Antman EM, Wenger TL, Butler VP Jr, Haber E, Smith TW. Treatment of 150 cases of 
   life-threatening digitalis intoxication with digoxin-specific Fab antibody fragments. 
   Final report of a multicenter study. Circulation. 1990;81(6):1744-52.
"""

import math
from typing import Dict, Any


class DigifabDosingCalculator:
    """Calculator for DigiFab (Digibind) Dosing for Digoxin Poisoning"""
    
    def __init__(self):
        # Constants for calculation
        self.DIGIFAB_BINDING_CAPACITY = 100  # Divisor for serum level method
        self.DIGOXIN_VIAL_CONTENT = 0.5  # mg of digoxin neutralized per vial
        self.BIOAVAILABILITY = 0.8  # 80% bioavailability for oral digoxin
    
    def calculate(self, method: str, weight_kg: float = None, serum_digoxin_level: float = None, 
                  amount_ingested_mg: float = None) -> Dict[str, Any]:
        """
        Calculates the number of DigiFab vials needed
        
        Args:
            method (str): Calculation method - "serum_level" or "amount_ingested"
            weight_kg (float, optional): Patient weight in kg (required for serum level method)
            serum_digoxin_level (float, optional): Serum digoxin level in ng/mL (required for serum level method)
            amount_ingested_mg (float, optional): Amount of digoxin ingested in mg (required for amount ingested method)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs based on method
        if method == "serum_level":
            self._validate_serum_level_inputs(weight_kg, serum_digoxin_level)
            result = self._calculate_serum_level_method(weight_kg, serum_digoxin_level)
        elif method == "amount_ingested":
            self._validate_amount_ingested_inputs(amount_ingested_mg)
            result = self._calculate_amount_ingested_method(amount_ingested_mg)
        else:
            raise ValueError("Method must be either 'serum_level' or 'amount_ingested'")
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "vials",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_serum_level_inputs(self, weight_kg: float, serum_digoxin_level: float):
        """Validates input parameters for serum level method"""
        
        if weight_kg is None:
            raise ValueError("Weight is required for serum level method")
        
        if serum_digoxin_level is None:
            raise ValueError("Serum digoxin level is required for serum level method")
        
        if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
            raise ValueError("Weight must be a positive number")
        
        if weight_kg < 0.5 or weight_kg > 620:
            raise ValueError("Weight must be between 0.5 and 620 kg")
        
        if not isinstance(serum_digoxin_level, (int, float)) or serum_digoxin_level < 0:
            raise ValueError("Serum digoxin level must be a non-negative number")
        
        if serum_digoxin_level > 100:
            raise ValueError("Serum digoxin level must be ≤100 ng/mL")
    
    def _validate_amount_ingested_inputs(self, amount_ingested_mg: float):
        """Validates input parameters for amount ingested method"""
        
        if amount_ingested_mg is None:
            raise ValueError("Amount ingested is required for amount ingested method")
        
        if not isinstance(amount_ingested_mg, (int, float)) or amount_ingested_mg < 0:
            raise ValueError("Amount ingested must be a non-negative number")
        
        if amount_ingested_mg > 100:
            raise ValueError("Amount ingested must be ≤100 mg")
    
    def _calculate_serum_level_method(self, weight_kg: float, serum_digoxin_level: float) -> int:
        """
        Calculates number of vials using serum digoxin level method
        
        Formula: Number of vials = (serum digoxin level × weight) / 100
        """
        
        vials = (serum_digoxin_level * weight_kg) / self.DIGIFAB_BINDING_CAPACITY
        
        # Always round up to the next whole number
        return math.ceil(vials)
    
    def _calculate_amount_ingested_method(self, amount_ingested_mg: float) -> int:
        """
        Calculates number of vials using amount ingested method
        
        Formula: Number of vials = (amount ingested / 0.5) × 0.8
        """
        
        vials = (amount_ingested_mg / self.DIGOXIN_VIAL_CONTENT) * self.BIOAVAILABILITY
        
        # Always round up to the next whole number
        return math.ceil(vials)
    
    def _get_interpretation(self, vials: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the number of vials
        
        Args:
            vials (int): Number of DigiFab vials calculated
            
        Returns:
            Dict with interpretation
        """
        
        if vials <= 2:
            return {
                "stage": "Low dose",
                "description": "Low dose requirement",
                "interpretation": "Administer calculated number of vials. Consider slow infusion over 2 hours if rhythm disturbances are not life-threatening."
            }
        elif vials <= 6:
            return {
                "stage": "Moderate dose", 
                "description": "Moderate dose requirement",
                "interpretation": "Administer calculated number of vials. Typical dose for chronic toxicity in adults. Monitor patient closely for response."
            }
        elif vials <= 10:
            return {
                "stage": "High dose",
                "description": "High dose requirement",
                "interpretation": "Administer calculated number of vials. This suggests significant toxicity. Consider rapid infusion if life-threatening dysrhythmias present."
            }
        elif vials <= 20:
            return {
                "stage": "Very high dose",
                "description": "Very high dose requirement",
                "interpretation": "Administer calculated number of vials urgently. This indicates severe toxicity. For acute poisoning with serum digoxin >10 ng/mL, empiric dosing of 10-20 vials may be appropriate."
            }
        else:
            return {
                "stage": "Extreme dose",
                "description": "Extreme dose requirement",
                "interpretation": "Critical toxicity requiring immediate intervention. Verify calculation and consider empiric maximum dosing. Consult toxicology immediately."
            }


def calculate_digifab_dosing(method: str, weight_kg: float = None, serum_digoxin_level: float = None,
                             amount_ingested_mg: float = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DigifabDosingCalculator()
    return calculator.calculate(method, weight_kg, serum_digoxin_level, amount_ingested_mg)