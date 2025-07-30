"""
Brain Metastasis Velocity (BMV) Model Calculator

Calculates rate of distant brain failure after stereotactic radiosurgery 
to predict overall survival.

References:
1. Farris M, McTyre ER, Cramer CK, et al. Brain Metastasis Velocity: A Novel 
   Prognostic Metric Predictive of Overall Survival and Freedom From Whole-Brain 
   Radiation Therapy After Distant Brain Failure Following Upfront Radiosurgery 
   Alone. Int J Radiat Oncol Biol Phys. 2017;98(1):131-141.
2. Yamamoto M, Aiyama H, Koiso T, et al. Validity of a Recently Proposed 
   Prognostic Grading Index, Brain Metastasis Velocity, for Patients With Brain 
   Metastasis Undergoing Multiple Radiosurgical Procedures. Int J Radiat Oncol 
   Biol Phys. 2019;103(3):631-637.
"""

from typing import Dict, Any


class BmvModelCalculator:
    """Calculator for Brain Metastasis Velocity (BMV) Model"""
    
    def __init__(self):
        # BMV thresholds for risk stratification
        self.LOW_BMV_THRESHOLD = 4
        self.HIGH_BMV_THRESHOLD = 13
        
    def calculate(self, new_metastases: int, time_interval: float) -> Dict[str, Any]:
        """
        Calculates the Brain Metastasis Velocity
        
        Args:
            new_metastases (int): Number of new brain metastases since initial SRS
            time_interval (float): Time interval in years between initial SRS and new metastases
            
        Returns:
            Dict with BMV value, unit, risk category, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(new_metastases, time_interval)
        
        # Calculate BMV
        bmv = new_metastases / time_interval
        
        # Round to 2 decimal places
        bmv = round(bmv, 2)
        
        # Get risk stratification
        interpretation = self._get_interpretation(bmv)
        
        return {
            "result": bmv,
            "unit": "metastases/year",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, new_metastases: int, time_interval: float):
        """Validates input parameters"""
        
        # Validate new_metastases
        if not isinstance(new_metastases, int):
            raise ValueError("Number of new metastases must be an integer")
        if new_metastases < 1:
            raise ValueError("Number of new metastases must be at least 1")
        if new_metastases > 100:
            raise ValueError("Number of new metastases must be ≤100")
        
        # Validate time_interval
        if not isinstance(time_interval, (int, float)):
            raise ValueError("Time interval must be a number")
        if time_interval <= 0:
            raise ValueError("Time interval must be greater than 0")
        if time_interval > 10:
            raise ValueError("Time interval must be ≤10 years")
    
    def _get_interpretation(self, bmv: float) -> Dict[str, str]:
        """
        Determines risk category and interpretation based on BMV
        
        Args:
            bmv (float): Calculated brain metastasis velocity
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if bmv < self.LOW_BMV_THRESHOLD:
            return {
                "stage": "Low BMV",
                "description": "Low brain metastasis velocity",
                "interpretation": f"Low BMV (<4 metastases/year). Median overall survival: 12.4 months. Localized therapy such as stereotactic radiosurgery (SRS) might be most appropriate for managing new brain metastases."
            }
        elif bmv <= self.HIGH_BMV_THRESHOLD:
            return {
                "stage": "Intermediate BMV",
                "description": "Intermediate brain metastasis velocity",
                "interpretation": f"Intermediate BMV (4-13 metastases/year). Median overall survival: 8.2 months. Consider patient factors including performance status, systemic disease control, and tumor histology when deciding between localized vs. whole brain radiation therapy."
            }
        else:
            return {
                "stage": "High BMV",
                "description": "High brain metastasis velocity",
                "interpretation": f"High BMV (>13 metastases/year). Median overall survival: 4.3 months. Increased risk of needing additional therapies. Whole brain radiation therapy should be considered, though treatment decisions should incorporate tumor histology and extracranial disease control."
            }


def calculate_bmv_model(new_metastases: int, time_interval: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BmvModelCalculator()
    return calculator.calculate(new_metastases, time_interval)