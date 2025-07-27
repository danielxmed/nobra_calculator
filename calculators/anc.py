"""
Absolute Neutrophil Count (ANC) Calculator

Frequently used to assess febrile neutropenia in chemotherapy patients,
by calculating the total number of mature and immature neutrophils.
"""

from typing import Dict, Any


class AncCalculator:
    """Calculator for Absolute Neutrophil Count (ANC)"""
    
    def __init__(self):
        # Cutoff points for neutropenia classification
        self.SEVERE_NEUTROPENIA_CUTOFF = 500
        self.MODERATE_NEUTROPENIA_CUTOFF = 1000
        self.MILD_NEUTROPENIA_CUTOFF = 1500
        
        # Normal ANC range
        self.NORMAL_ANC_MIN = 1500
        self.NORMAL_ANC_MAX = 8000
    
    def calculate(self, wbc_count: float, segmented_neutrophils: float, 
                 band_neutrophils: float) -> Dict[str, Any]:
        """
        Calculates the Absolute Neutrophil Count (ANC)
        
        Args:
            wbc_count (float): White blood cell count in x 10³/mm³
            segmented_neutrophils (float): Percentage of segmented neutrophils (0-100%)
            band_neutrophils (float): Percentage of band neutrophils (0-100%)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(wbc_count, segmented_neutrophils, band_neutrophils)
        
        # Calculate ANC using the formula:
        # ANC = WBC × [(% Segmented Neutrophils + % Band Neutrophils) / 100]
        total_neutrophil_percent = segmented_neutrophils + band_neutrophils
        anc_count = wbc_count * 1000 * (total_neutrophil_percent / 100)
        
        # Round to 1 decimal place
        anc_count = round(anc_count, 1)
        
        # Determine if it's in the normal range
        is_normal = self.NORMAL_ANC_MIN <= anc_count <= self.NORMAL_ANC_MAX
        
        # Classify neutropenia
        neutropenia_classification = self._classify_neutropenia(anc_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(anc_count)
        
        # Assess infection risk
        infection_risk = self._assess_infection_risk(anc_count)
        
        return {
            "result": anc_count,
            "unit": "cells/mm³",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "is_normal_range": is_normal,
            "neutropenia_classification": neutropenia_classification,
            "infection_risk": infection_risk["level"],
            "total_neutrophil_percent": total_neutrophil_percent
        }
    
    def _validate_inputs(self, wbc_count, segmented_neutrophils, band_neutrophils):
        """Validates input parameters"""
        
        if not isinstance(wbc_count, (int, float)) or wbc_count < 0.1 or wbc_count > 100.0:
            raise ValueError("WBC count must be between 0.1 and 100.0 x 10³/mm³")
        
        if not isinstance(segmented_neutrophils, (int, float)) or segmented_neutrophils < 0.0 or segmented_neutrophils > 100.0:
            raise ValueError("Percentage of segmented neutrophils must be between 0.0 and 100.0%")
        
        if not isinstance(band_neutrophils, (int, float)) or band_neutrophils < 0.0 or band_neutrophils > 100.0:
            raise ValueError("Percentage of band neutrophils must be between 0.0 and 100.0%")
        
        # Validate that the sum of percentages does not exceed 100%
        total_percent = segmented_neutrophils + band_neutrophils
        if total_percent > 100.0:
            raise ValueError("The sum of neutrophil percentages cannot exceed 100%")
    
    def _classify_neutropenia(self, anc_count: float) -> Dict[str, Any]:
        """
        Classifies the degree of neutropenia
        
        Args:
            anc_count (float): Absolute neutrophil count
            
        Returns:
            Dict with neutropenia classification
        """
        
        if anc_count < self.SEVERE_NEUTROPENIA_CUTOFF:
            return {
                "has_neutropenia": True,
                "severity": "severe",
                "grade": 4,
                "description": "Severe neutropenia (grade 4)"
            }
        elif anc_count < self.MODERATE_NEUTROPENIA_CUTOFF:
            return {
                "has_neutropenia": True,
                "severity": "moderate",
                "grade": 3,
                "description": "Moderate neutropenia (grade 3)"
            }
        elif anc_count < self.MILD_NEUTROPENIA_CUTOFF:
            return {
                "has_neutropenia": True,
                "severity": "mild",
                "grade": 2,
                "description": "Mild neutropenia (grade 2)"
            }
        else:
            return {
                "has_neutropenia": False,
                "severity": "absent",
                "grade": 0,
                "description": "No neutropenia"
            }
    
    def _assess_infection_risk(self, anc_count: float) -> Dict[str, str]:
        """
        Assesses infection risk based on ANC
        
        Args:
            anc_count (float): Absolute neutrophil count
            
        Returns:
            Dict with infection risk assessment
        """
        
        if anc_count < self.SEVERE_NEUTROPENIA_CUTOFF:
            return {
                "level": "very high",
                "description": "Very high risk of severe infections",
                "recommendation": "Protective isolation, antimicrobial prophylaxis"
            }
        elif anc_count < self.MODERATE_NEUTROPENIA_CUTOFF:
            return {
                "level": "high",
                "description": "High risk of infections",
                "recommendation": "Strict precautions, consider prophylaxis"
            }
        elif anc_count < self.MILD_NEUTROPENIA_CUTOFF:
            return {
                "level": "moderate",
                "description": "Moderately increased risk",
                "recommendation": "Basic precautions, monitoring"
            }
        else:
            return {
                "level": "normal",
                "description": "Infection risk not increased",
                "recommendation": "Routine care"
            }
    
    def _get_interpretation(self, anc_count: float) -> Dict[str, str]:
        """
        Determines the interpretation based on ANC
        
        Args:
            anc_count (float): Absolute neutrophil count
            
        Returns:
            Dict with clinical interpretation
        """
        
        if anc_count < self.SEVERE_NEUTROPENIA_CUTOFF:
            return {
                "stage": "Severe Neutropenia",
                "description": "High infection risk",
                "interpretation": "Severe neutropenia. Very high risk of severe bacterial infections and sepsis. Requires protective isolation, antimicrobial prophylaxis, and intensive monitoring."
            }
        elif anc_count < self.MODERATE_NEUTROPENIA_CUTOFF:
            return {
                "stage": "Moderate Neutropenia",
                "description": "Moderate infection risk",
                "interpretation": "Moderate neutropenia. Increased risk of infections. Avoid unnecessary exposures, consider prophylaxis in some cases."
            }
        elif anc_count < self.MILD_NEUTROPENIA_CUTOFF:
            return {
                "stage": "Mild Neutropenia",
                "description": "Mild infection risk",
                "interpretation": "Mild neutropenia. Small increase in infection risk. Regular monitoring and basic hygiene precautions."
            }
        else:
            return {
                "stage": "Normal",
                "description": "Normal count",
                "interpretation": "Neutrophil count within normal range (1500-8000 cells/mm³). Infection risk not increased by neutropenia."
            }


def calculate_anc(wbc_count: float, segmented_neutrophils: float, 
                 band_neutrophils: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AncCalculator()
    return calculator.calculate(wbc_count, segmented_neutrophils, band_neutrophils)
