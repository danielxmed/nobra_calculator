"""
Tokyo Guidelines 2018 for Acute Cholecystitis Calculator

Provides diagnostic criteria and severity grading for acute cholecystitis according to TG18.
Based on the Journal of Hepato-Biliary-Pancreatic Sciences 2018 publication.

References:
1. Yokoe M, et al. Tokyo Guidelines 2018: diagnostic criteria and severity grading 
   of acute cholecystitis. J Hepatobiliary Pancreat Sci. 2018;25(1):41-54.
"""

from typing import Dict, Any


class TokyoGuidelines2018Calculator:
    """Calculator for Tokyo Guidelines 2018 for Acute Cholecystitis"""
    
    def __init__(self):
        # Mortality rates by grade
        self.mortality_rates = {
            "grade_i": 1.1,
            "grade_ii": 5.4,
            "grade_iii": 18.8
        }
    
    def calculate(self, murphys_sign: str, ruq_pain: str, fever: str,
                  elevated_crp: str, elevated_wbc: str, imaging_findings: str,
                  cardiovascular_dysfunction: str, neurological_dysfunction: str,
                  respiratory_dysfunction: str, renal_dysfunction: str,
                  hepatic_dysfunction: str, hematological_dysfunction: str,
                  wbc_over_18000: str, palpable_mass: str,
                  duration_over_72h: str, marked_inflammation: str) -> Dict[str, Any]:
        """
        Calculates Tokyo Guidelines 2018 diagnosis and severity grading
        
        Args:
            All parameters are "yes" or "no" strings
            
        Returns:
            Dict with diagnosis, severity grade, and interpretation
        """
        
        # Validate inputs
        params = {
            "murphys_sign": murphys_sign,
            "ruq_pain": ruq_pain,
            "fever": fever,
            "elevated_crp": elevated_crp,
            "elevated_wbc": elevated_wbc,
            "imaging_findings": imaging_findings,
            "cardiovascular_dysfunction": cardiovascular_dysfunction,
            "neurological_dysfunction": neurological_dysfunction,
            "respiratory_dysfunction": respiratory_dysfunction,
            "renal_dysfunction": renal_dysfunction,
            "hepatic_dysfunction": hepatic_dysfunction,
            "hematological_dysfunction": hematological_dysfunction,
            "wbc_over_18000": wbc_over_18000,
            "palpable_mass": palpable_mass,
            "duration_over_72h": duration_over_72h,
            "marked_inflammation": marked_inflammation
        }
        
        self._validate_inputs(params)
        
        # Check diagnostic criteria
        diagnosis = self._check_diagnosis(params)
        
        if diagnosis == "no_diagnosis":
            return {
                "result": "Not Acute Cholecystitis",
                "unit": "",
                "interpretation": "Does not meet diagnostic criteria for acute cholecystitis. Consider other diagnoses.",
                "stage": "Not Acute Cholecystitis",
                "stage_description": "Entry criteria not met",
                "diagnosis": "negative",
                "severity_grade": "N/A"
            }
        
        # If diagnosed, determine severity grade
        severity = self._determine_severity(params)
        
        # Get interpretation based on diagnosis and severity
        result_data = self._get_interpretation(diagnosis, severity)
        
        return {
            "result": result_data["result"],
            "unit": "",
            "interpretation": result_data["interpretation"],
            "stage": result_data["stage"],
            "stage_description": result_data["description"],
            "diagnosis": diagnosis,
            "severity_grade": severity if severity else "N/A",
            "mortality_rate": result_data.get("mortality", "N/A")
        }
    
    def _validate_inputs(self, params: Dict[str, str]):
        """Validates all input parameters"""
        
        for param, value in params.items():
            if value not in ["yes", "no"]:
                raise ValueError(f"{param} must be 'yes' or 'no'")
    
    def _check_diagnosis(self, params: Dict[str, str]) -> str:
        """
        Checks diagnostic criteria
        
        Part A: Local signs of inflammation
        Part B: Systemic signs of inflammation  
        Part C: Imaging findings
        
        Suspected: Part A + Part B
        Definite: Part A + Part B + Part C
        """
        
        # Part A: Local signs
        part_a = params["murphys_sign"] == "yes" or params["ruq_pain"] == "yes"
        
        # Part B: Systemic signs
        part_b = (params["fever"] == "yes" or 
                  params["elevated_crp"] == "yes" or 
                  params["elevated_wbc"] == "yes")
        
        # Part C: Imaging
        part_c = params["imaging_findings"] == "yes"
        
        if part_a and part_b and part_c:
            return "definite"
        elif part_a and part_b:
            return "suspected"
        else:
            return "no_diagnosis"
    
    def _determine_severity(self, params: Dict[str, str]) -> str:
        """
        Determines severity grade based on criteria
        
        Grade III: Any organ dysfunction
        Grade II: Any moderate criteria (without organ dysfunction)
        Grade I: Neither Grade II nor Grade III criteria
        """
        
        # Grade III criteria - organ dysfunction
        grade_iii_criteria = [
            params["cardiovascular_dysfunction"] == "yes",
            params["neurological_dysfunction"] == "yes",
            params["respiratory_dysfunction"] == "yes",
            params["renal_dysfunction"] == "yes",
            params["hepatic_dysfunction"] == "yes",
            params["hematological_dysfunction"] == "yes"
        ]
        
        if any(grade_iii_criteria):
            return "grade_iii"
        
        # Grade II criteria - moderate inflammation
        grade_ii_criteria = [
            params["wbc_over_18000"] == "yes",
            params["palpable_mass"] == "yes",
            params["duration_over_72h"] == "yes",
            params["marked_inflammation"] == "yes"
        ]
        
        if any(grade_ii_criteria):
            return "grade_ii"
        
        # Grade I - mild (no Grade II or III criteria)
        return "grade_i"
    
    def _get_interpretation(self, diagnosis: str, severity: str) -> Dict[str, str]:
        """
        Returns interpretation based on diagnosis and severity
        """
        
        if diagnosis == "suspected":
            return {
                "result": "Suspected Acute Cholecystitis",
                "stage": "Suspected Acute Cholecystitis", 
                "description": "Suspected diagnosis",
                "interpretation": "Meets diagnostic criteria for suspected acute cholecystitis (Part A + Part B). Further imaging evaluation recommended to confirm diagnosis."
            }
        
        # For definite diagnosis, return based on severity
        if severity == "grade_i":
            return {
                "result": "Grade I (Mild) Acute Cholecystitis",
                "stage": "Grade I (Mild)",
                "description": "Mild acute cholecystitis",
                "interpretation": f"Mild acute cholecystitis without organ dysfunction. {self.mortality_rates['grade_i']}% 30-day mortality. Early laparoscopic cholecystectomy recommended if patient can tolerate surgery.",
                "mortality": f"{self.mortality_rates['grade_i']}%"
            }
        elif severity == "grade_ii":
            return {
                "result": "Grade II (Moderate) Acute Cholecystitis",
                "stage": "Grade II (Moderate)",
                "description": "Moderate acute cholecystitis",
                "interpretation": f"Moderate acute cholecystitis with local inflammation. {self.mortality_rates['grade_ii']}% 30-day mortality. Immediate supportive care, antibiotics, and urgent/early cholecystectomy based on response to treatment.",
                "mortality": f"{self.mortality_rates['grade_ii']}%"
            }
        else:  # grade_iii
            return {
                "result": "Grade III (Severe) Acute Cholecystitis",
                "stage": "Grade III (Severe)",
                "description": "Severe acute cholecystitis",
                "interpretation": f"Severe acute cholecystitis with organ dysfunction. {self.mortality_rates['grade_iii']}% 30-day mortality. ICU admission required, organ support, emergent gallbladder drainage followed by cholecystectomy when stable.",
                "mortality": f"{self.mortality_rates['grade_iii']}%"
            }


def calculate_tokyo_guidelines_2018(murphys_sign, ruq_pain, fever,
                                  elevated_crp, elevated_wbc, imaging_findings,
                                  cardiovascular_dysfunction, neurological_dysfunction,
                                  respiratory_dysfunction, renal_dysfunction,
                                  hepatic_dysfunction, hematological_dysfunction,
                                  wbc_over_18000, palpable_mass,
                                  duration_over_72h, marked_inflammation) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    """
    calculator = TokyoGuidelines2018Calculator()
    return calculator.calculate(
        murphys_sign, ruq_pain, fever,
        elevated_crp, elevated_wbc, imaging_findings,
        cardiovascular_dysfunction, neurological_dysfunction,
        respiratory_dysfunction, renal_dysfunction,
        hepatic_dysfunction, hematological_dysfunction,
        wbc_over_18000, palpable_mass,
        duration_over_72h, marked_inflammation
    )