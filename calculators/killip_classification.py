"""
Killip Classification for Heart Failure Calculator

Quantifies heart failure severity in acute coronary syndrome (ACS) and predicts 
30-day mortality based on physical examination findings.

References:
1. Killip T 3rd, Kimball JT. Treatment of myocardial infarction in a coronary 
   care unit. A two year experience with 250 patients. Am J Cardiol. 1967 
   Oct;20(4):457-64.
2. Khot UN, Jia G, Moliterno DJ, Lincoff AM, Khot MB, Harrington RA, Topol EJ. 
   Prognostic importance of physical examination for heart failure in non-ST-elevation 
   acute coronary syndromes: the enduring value of Killip classification. JAMA. 
   2003 Oct 22;290(16):2174-81.
"""

from typing import Dict, Any


class KillipClassificationCalculator:
    """Calculator for Killip Classification for Heart Failure"""
    
    def __init__(self):
        # Killip class definitions and mortality data
        self.killip_classes = {
            "class_i": {
                "class": "I",
                "description": "No signs of congestion",
                "clinical_findings": "No clinical signs of heart failure",
                "mortality_30_day_min": 2,
                "mortality_30_day_max": 3,
                "in_hospital_mortality": 6
            },
            "class_ii": {
                "class": "II", 
                "description": "S3 and basal rales on auscultation",
                "clinical_findings": "Rales in the lungs, third heart sound (S3), and/or elevated jugular venous pressure",
                "mortality_30_day_min": 5,
                "mortality_30_day_max": 12,
                "in_hospital_mortality": 17
            },
            "class_iii": {
                "class": "III",
                "description": "Acute pulmonary edema",
                "clinical_findings": "Overt pulmonary edema with rales throughout lung fields",
                "mortality_30_day_min": 10,
                "mortality_30_day_max": 20,
                "in_hospital_mortality": 38
            },
            "class_iv": {
                "class": "IV",
                "description": "Cardiogenic shock", 
                "clinical_findings": "Cardiogenic shock with hypotension (SBP <90 mmHg) and evidence of peripheral vasoconstriction",
                "mortality_30_day_min": 10,
                "mortality_30_day_max": 20,
                "in_hospital_mortality": 81
            }
        }
    
    def calculate(self, killip_class: str) -> Dict[str, Any]:
        """
        Calculates Killip Classification result with mortality risk
        
        Args:
            killip_class (str): The Killip class (class_i, class_ii, class_iii, class_iv)
            
        Returns:
            Dict with classification result and interpretation
        """
        
        # Validate input
        self._validate_inputs(killip_class)
        
        # Get class information
        class_info = self.killip_classes[killip_class]
        
        # Format mortality ranges
        mortality_30_day = f"{class_info['mortality_30_day_min']}-{class_info['mortality_30_day_max']}%"
        if class_info['mortality_30_day_min'] == class_info['mortality_30_day_max']:
            mortality_30_day = f"{class_info['mortality_30_day_min']}%"
        
        in_hospital_mortality = f"<{class_info['in_hospital_mortality']}%"
        if class_info['in_hospital_mortality'] > 50:
            in_hospital_mortality = f"{class_info['in_hospital_mortality']}%"
        
        # Create result object
        result = {
            "class": class_info["class"],
            "description": class_info["description"],
            "mortality_30_day": mortality_30_day,
            "in_hospital_mortality": in_hospital_mortality
        }
        
        # Get interpretation
        interpretation = self._get_interpretation(killip_class, class_info, 
                                                mortality_30_day, in_hospital_mortality)
        
        return {
            "result": result,
            "unit": "classification",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, killip_class: str):
        """Validates input parameters"""
        
        if not isinstance(killip_class, str):
            raise ValueError("Killip class must be a string")
        
        valid_classes = ["class_i", "class_ii", "class_iii", "class_iv"]
        if killip_class not in valid_classes:
            raise ValueError(f"Invalid Killip class. Must be one of: {', '.join(valid_classes)}")
    
    def _get_interpretation(self, killip_class: str, class_info: Dict[str, Any],
                          mortality_30_day: str, in_hospital_mortality: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Killip class
        
        Args:
            killip_class (str): The Killip class
            class_info (Dict): Class information
            mortality_30_day (str): 30-day mortality rate
            in_hospital_mortality (str): In-hospital mortality rate
            
        Returns:
            Dict with interpretation details
        """
        
        base_interpretation = (
            f"Killip Class {class_info['class']}: {class_info['description']}. "
            f"30-day mortality: {mortality_30_day}, In-hospital mortality: {in_hospital_mortality}. "
        )
        
        if killip_class == "class_i":
            stage = "Low Risk"
            stage_description = "No heart failure"
            specific_interpretation = (
                "Low risk patient with no clinical signs of heart failure. "
                "Standard acute coronary syndrome management is appropriate. "
                "Continue monitoring for signs of decompensation."
            )
        
        elif killip_class == "class_ii":
            stage = "Moderate Risk"
            stage_description = "Mild-moderate heart failure"
            specific_interpretation = (
                "Moderate risk with evidence of mild to moderate heart failure. "
                "Consider diuretics for congestion, optimize medical therapy, "
                "and maintain close hemodynamic monitoring. May benefit from "
                "early invasive strategy if NSTEMI."
            )
        
        elif killip_class == "class_iii":
            stage = "High Risk"
            stage_description = "Severe heart failure"
            specific_interpretation = (
                "High risk patient with acute pulmonary edema. Requires aggressive "
                "treatment including IV diuretics, vasodilators (if blood pressure allows), "
                "and consideration of non-invasive ventilation. Consider mechanical "
                "circulatory support if not responding to medical therapy. "
                "Urgent cardiac catheterization recommended."
            )
        
        else:  # class_iv
            stage = "Very High Risk"
            stage_description = "Cardiogenic shock"
            specific_interpretation = (
                "Very high risk patient in cardiogenic shock. Requires immediate "
                "intervention including inotropic support, mechanical circulatory "
                "support (IABP, Impella, or ECMO), and emergent revascularization. "
                "Consider transfer to a center with advanced heart failure capabilities. "
                "Monitor for multi-organ dysfunction."
            )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": base_interpretation + specific_interpretation
        }


def calculate_killip_classification(killip_class: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_killip_classification pattern
    """
    calculator = KillipClassificationCalculator()
    return calculator.calculate(killip_class)