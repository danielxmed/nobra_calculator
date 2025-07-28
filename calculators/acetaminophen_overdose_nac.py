"""
Acetaminophen Overdose and NAC Dosing Calculator

Calculates N-acetylcysteine (NAC) dosing for acetaminophen overdose and assesses
toxicity using the Rumack-Matthew nomogram.

References:
- Rumack BH, Matthew H. Pediatrics. 1975;55(6):871-6.
- Prescott LF, et al. Br Med J. 1979;2(6198):1097-100.
"""

import math
from typing import Dict, Any, Optional


class AcetaminophenOverdoseNacCalculator:
    """Calculator for Acetaminophen Overdose and NAC Dosing"""
    
    def __init__(self):
        # Rumack-Matthew nomogram parameters
        # The treatment line at 4 hours is 150 mcg/mL
        # The line follows: concentration = 150 * (4/hours)^0.785
        self.NOMOGRAM_4HR_LEVEL = 150  # mcg/mL at 4 hours
        self.NOMOGRAM_SLOPE = 0.785  # logarithmic decline rate
        
        # Maximum doses for safety
        self.MAX_IV_LOADING_DOSE = 15000  # mg
        self.MAX_IV_SECOND_DOSE = 5000  # mg
        self.MAX_IV_THIRD_DOSE = 10000  # mg
    
    def calculate(self, route: str, weight: float, 
                  hours_since_ingestion: Optional[float] = None,
                  acetaminophen_level: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates NAC dosing regimen and assesses toxicity if nomogram data provided
        
        Args:
            route (str): Route of administration ("IV" or "PO")
            weight (float): Patient weight in kg
            hours_since_ingestion (float, optional): Hours since ingestion (4-24)
            acetaminophen_level (float, optional): Serum acetaminophen level in mcg/mL
            
        Returns:
            Dict with dosing regimen and toxicity assessment
        """
        
        # Validate inputs
        self._validate_inputs(route, weight, hours_since_ingestion, acetaminophen_level)
        
        # Calculate dosing based on route
        if route == "IV":
            dosing = self._calculate_iv_dosing(weight)
        else:  # PO
            dosing = self._calculate_po_dosing(weight)
        
        # Assess toxicity if nomogram data provided
        toxicity_assessment = None
        if hours_since_ingestion is not None and acetaminophen_level is not None:
            toxicity_assessment = self._assess_toxicity(hours_since_ingestion, acetaminophen_level)
        
        # Combine results
        result = {
            "dosing_regimen": dosing,
            "toxicity_assessment": toxicity_assessment
        }
        
        # Generate interpretation
        interpretation = self._get_interpretation(route, toxicity_assessment)
        
        return {
            "result": result,
            "unit": "complex",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, route: str, weight: float, 
                        hours_since_ingestion: Optional[float],
                        acetaminophen_level: Optional[float]):
        """Validates input parameters"""
        
        if route not in ["IV", "PO"]:
            raise ValueError("Route must be either 'IV' or 'PO'")
        
        if weight < 1 or weight > 500:
            raise ValueError("Weight must be between 1 and 500 kg")
        
        if hours_since_ingestion is not None:
            if hours_since_ingestion < 4 or hours_since_ingestion > 24:
                raise ValueError("Hours since ingestion must be between 4 and 24 for nomogram use")
        
        if acetaminophen_level is not None:
            if acetaminophen_level < 0 or acetaminophen_level > 1000:
                raise ValueError("Acetaminophen level must be between 0 and 1000 mcg/mL")
        
        # Both nomogram parameters must be provided together
        if (hours_since_ingestion is None) != (acetaminophen_level is None):
            raise ValueError("Both hours since ingestion and acetaminophen level must be provided for nomogram assessment")
    
    def _calculate_iv_dosing(self, weight: float) -> Dict[str, Any]:
        """Calculates 21-hour IV NAC protocol dosing"""
        
        # Loading dose: 150 mg/kg over 60 minutes
        loading_dose = min(150 * weight, self.MAX_IV_LOADING_DOSE)
        
        # Second dose: 50 mg/kg over 4 hours
        second_dose = min(50 * weight, self.MAX_IV_SECOND_DOSE)
        
        # Third dose: 100 mg/kg over 16 hours
        third_dose = min(100 * weight, self.MAX_IV_THIRD_DOSE)
        
        # Total dose
        total_dose = loading_dose + second_dose + third_dose
        
        return {
            "protocol": "21-hour IV protocol",
            "loading_dose": {
                "dose_mg": round(loading_dose, 1),
                "duration": "60 minutes",
                "volume": "200 mL D5W",
                "rate": f"{round(loading_dose, 1)} mg over 60 min"
            },
            "second_dose": {
                "dose_mg": round(second_dose, 1),
                "duration": "4 hours",
                "volume": "500 mL D5W",
                "rate": f"{round(second_dose/4, 1)} mg/hr"
            },
            "third_dose": {
                "dose_mg": round(third_dose, 1),
                "duration": "16 hours",
                "volume": "1000 mL D5W",
                "rate": f"{round(third_dose/16, 1)} mg/hr"
            },
            "total_dose_mg": round(total_dose, 1),
            "total_duration": "21 hours"
        }
    
    def _calculate_po_dosing(self, weight: float) -> Dict[str, Any]:
        """Calculates 72-hour oral NAC protocol dosing"""
        
        # Loading dose: 140 mg/kg
        loading_dose = 140 * weight
        
        # Maintenance dose: 70 mg/kg every 4 hours for 17 doses
        maintenance_dose = 70 * weight
        
        # Total dose
        total_dose = loading_dose + (maintenance_dose * 17)
        
        return {
            "protocol": "72-hour oral protocol",
            "loading_dose": {
                "dose_mg": round(loading_dose, 1),
                "timing": "Immediately"
            },
            "maintenance_dose": {
                "dose_mg": round(maintenance_dose, 1),
                "frequency": "Every 4 hours",
                "number_of_doses": 17,
                "start": "4 hours after loading dose"
            },
            "total_dose_mg": round(total_dose, 1),
            "total_duration": "72 hours",
            "administration_note": "Dilute to 5% solution and mix with juice for palatability"
        }
    
    def _assess_toxicity(self, hours: float, level: float) -> Dict[str, Any]:
        """Assesses toxicity using the Rumack-Matthew nomogram"""
        
        # Calculate the treatment line level at the given time
        # Formula: treatment_level = 150 * (4/hours)^0.785
        treatment_line_level = self.NOMOGRAM_4HR_LEVEL * math.pow(4/hours, self.NOMOGRAM_SLOPE)
        
        # Determine if above or below treatment line
        is_toxic = level >= treatment_line_level
        
        return {
            "hours_post_ingestion": hours,
            "acetaminophen_level": level,
            "treatment_line_level": round(treatment_line_level, 1),
            "above_treatment_line": is_toxic,
            "toxicity_risk": "Probable hepatotoxicity" if is_toxic else "Hepatotoxicity unlikely"
        }
    
    def _get_interpretation(self, route: str, toxicity_assessment: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """
        Generates interpretation based on route and toxicity assessment
        
        Args:
            route (str): Route of administration
            toxicity_assessment (dict, optional): Nomogram assessment results
            
        Returns:
            Dict with interpretation
        """
        
        base_interpretation = f"NAC dosing calculated for {route} route. "
        
        if route == "IV":
            base_interpretation += "Use 21-hour protocol with careful monitoring for anaphylactoid reactions (up to 18% incidence). "
        else:
            base_interpretation += "Use 72-hour protocol. Ensure doses are not vomited; re-administer if necessary. "
        
        if toxicity_assessment:
            if toxicity_assessment["above_treatment_line"]:
                return {
                    "stage": "Toxic",
                    "description": "Above treatment line - Probable hepatotoxicity",
                    "interpretation": base_interpretation + 
                    f"Patient's acetaminophen level ({toxicity_assessment['acetaminophen_level']} mcg/mL) " +
                    f"is ABOVE the treatment line ({toxicity_assessment['treatment_line_level']} mcg/mL) " +
                    f"at {toxicity_assessment['hours_post_ingestion']} hours post-ingestion. " +
                    "Immediate NAC treatment is indicated. Continue NAC until acetaminophen undetectable " +
                    "and transaminases normalizing."
                }
            else:
                return {
                    "stage": "Non-toxic",
                    "description": "Below treatment line - Hepatotoxicity unlikely",
                    "interpretation": base_interpretation + 
                    f"Patient's acetaminophen level ({toxicity_assessment['acetaminophen_level']} mcg/mL) " +
                    f"is BELOW the treatment line ({toxicity_assessment['treatment_line_level']} mcg/mL) " +
                    f"at {toxicity_assessment['hours_post_ingestion']} hours post-ingestion. " +
                    "NAC treatment typically not needed unless clinical concern or risk factors present."
                }
        else:
            return {
                "stage": "Dosing Only",
                "description": "NAC dosing calculated without toxicity assessment",
                "interpretation": base_interpretation + 
                "No nomogram assessment performed. Consider obtaining acetaminophen level " +
                "and time of ingestion for toxicity assessment if single acute ingestion."
            }


def calculate_acetaminophen_overdose_nac(route: str, weight: float,
                                       hours_since_ingestion: Optional[float] = None,
                                       acetaminophen_level: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AcetaminophenOverdoseNacCalculator()
    return calculator.calculate(route, weight, hours_since_ingestion, acetaminophen_level)