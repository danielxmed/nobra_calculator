"""
Neutrophil-Lymphocyte Ratio (NLR) Calculator

Calculates the ratio of neutrophils to lymphocytes as a marker of physiological stress.

References:
1. Zahorec R. Bratisl Lek Listy. 2001;102(1):5-14.
2. Yang AP, et al. Int Immunopharmacol. 2020;84:106504.
"""

import math
from typing import Dict, Any


class NeutrophilLymphocyteRatioCalculator:
    """Calculator for Neutrophil-Lymphocyte Ratio (NLR)"""
    
    def __init__(self):
        # No specific constants needed for this simple ratio
        pass
    
    def calculate(self, count_type: str, neutrophil_count: float, 
                  lymphocyte_count: float) -> Dict[str, Any]:
        """
        Calculates the NLR
        
        Args:
            count_type (str): "absolute" or "percentage"
            neutrophil_count (float): Neutrophil count (cells/μL) or percentage
            lymphocyte_count (float): Lymphocyte count (cells/μL) or percentage
            
        Returns:
            Dict with the NLR and interpretation
        """
        
        # Validations
        self._validate_inputs(count_type, neutrophil_count, lymphocyte_count)
        
        # Calculate NLR - simple division
        nlr = neutrophil_count / lymphocyte_count
        
        # Round to 2 decimal places
        nlr = round(nlr, 2)
        
        # Get interpretation
        interpretation = self._get_interpretation(nlr)
        
        return {
            "result": nlr,
            "unit": "ratio",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, count_type: str, neutrophil_count: float, 
                        lymphocyte_count: float):
        """Validates input parameters"""
        
        # Count type validation
        if count_type not in ["absolute", "percentage"]:
            raise ValueError("Count type must be 'absolute' or 'percentage'")
        
        # Neutrophil count validation
        if not isinstance(neutrophil_count, (int, float)):
            raise ValueError("Neutrophil count must be a number")
        if neutrophil_count < 0:
            raise ValueError("Neutrophil count must be non-negative")
        
        # Lymphocyte count validation
        if not isinstance(lymphocyte_count, (int, float)):
            raise ValueError("Lymphocyte count must be a number")
        if lymphocyte_count <= 0:
            raise ValueError("Lymphocyte count must be greater than 0")
        
        # Additional validations based on count type
        if count_type == "percentage":
            if neutrophil_count > 100:
                raise ValueError("Neutrophil percentage cannot exceed 100%")
            if lymphocyte_count > 100:
                raise ValueError("Lymphocyte percentage cannot exceed 100%")
        else:  # absolute
            if neutrophil_count > 50000:
                raise ValueError("Neutrophil count seems too high (>50,000 cells/μL)")
            if lymphocyte_count > 50000:
                raise ValueError("Lymphocyte count seems too high (>50,000 cells/μL)")
    
    def _get_interpretation(self, nlr: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the NLR
        
        Args:
            nlr (float): Calculated neutrophil-lymphocyte ratio
            
        Returns:
            Dict with interpretation
        """
        
        if nlr <= 3:
            return {
                "stage": "Normal",
                "description": "Normal NLR",
                "interpretation": (
                    f"NLR of {nlr} is within normal range (1-3), indicating no significant "
                    "physiological stress. This is a reassuring finding suggesting adequate "
                    "immune balance."
                )
            }
        elif nlr <= 6:
            return {
                "stage": "Mildly Elevated",
                "description": "Mildly elevated NLR",
                "interpretation": (
                    f"NLR of {nlr} is mildly elevated (normal: 1-3), suggesting low-level "
                    "physiological stress. This may be seen in early infection, mild inflammation, "
                    "or minor stress response. Monitor clinical status and consider trending over time."
                )
            }
        elif nlr <= 9:
            return {
                "stage": "Mild Stress",
                "description": "Mild physiological stress",
                "interpretation": (
                    f"NLR of {nlr} indicates mild physiological stress (reference: 6-8). "
                    "This level may be seen in mild infections, minor inflammatory conditions, "
                    "or early stress response. Consider clinical context and trending values."
                )
            }
        elif nlr <= 18:
            return {
                "stage": "Moderate Stress",
                "description": "Moderate physiological stress",
                "interpretation": (
                    f"NLR of {nlr} indicates moderate physiological stress (reference: 9-18). "
                    "Often seen in bacterial infections, significant inflammation, or moderate "
                    "severity illness. This warrants careful clinical evaluation and monitoring."
                )
            }
        else:
            return {
                "stage": "Severe Stress",
                "description": "Severe physiological stress",
                "interpretation": (
                    f"NLR of {nlr} indicates severe physiological stress (>18). "
                    "This may indicate severe infection, sepsis, critical illness, or significant "
                    "inflammatory conditions. High NLR correlates with poor prognosis and requires "
                    "immediate clinical attention."
                )
            }


def calculate_neutrophil_lymphocyte_ratio(count_type: str, neutrophil_count: float,
                                         lymphocyte_count: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NeutrophilLymphocyteRatioCalculator()
    return calculator.calculate(count_type, neutrophil_count, lymphocyte_count)