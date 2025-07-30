"""
Brugada Criteria for Ventricular Tachycardia Calculator

Distinguishes ventricular tachycardia from supraventricular tachycardia with 
aberrancy using ECG morphology criteria. This is a four-step sequential algorithm 
where any positive criterion indicates VT.

References:
- Brugada P, Brugada J, Mont L, Smeets J, Andries EW. A new approach to the 
  differential diagnosis of a regular tachycardia with a wide QRS complex. 
  Circulation. 1991;83(5):1649-59.
- Isenhour JL, Craig S, Gibbs M, et al. Wide-complex tachycardia: continued 
  evaluation of diagnostic criteria. Acad Emerg Med. 2000;7(7):769-73.
"""

from typing import Dict, Any


class BrugadaCriteriaVtCalculator:
    """Calculator for Brugada Criteria for Ventricular Tachycardia"""
    
    def __init__(self):
        # Algorithm steps and their diagnostic implications
        self.criteria_steps = {
            1: {
                "criterion": "absence_rs_precordial",
                "description": "Absence of RS complex in all precordial leads (V1-V6)",
                "interpretation": "No RS complex in any precordial lead suggests VT"
            },
            2: {
                "criterion": "r_to_s_interval_100ms",
                "description": "R to S interval >100 ms in any precordial lead",
                "interpretation": "R-S interval >100ms (Brugada's sign) suggests VT"
            },
            3: {
                "criterion": "av_dissociation",
                "description": "Atrioventricular dissociation present",
                "interpretation": "AV dissociation with independent P waves suggests VT"
            },
            4: {
                "criterion": "morphology_criteria_vt",
                "description": "Morphology criteria for VT present in V1-V2 and V6",
                "interpretation": "VT morphology patterns in leads V1-V2 and V6 suggest VT"
            }
        }
    
    def calculate(self, absence_rs_precordial: str, r_to_s_interval_100ms: str,
                 av_dissociation: str, morphology_criteria_vt: str) -> Dict[str, Any]:
        """
        Applies Brugada Criteria for VT diagnosis
        
        Args:
            absence_rs_precordial (str): Absence of RS complex in all precordial leads ("yes"/"no")
            r_to_s_interval_100ms (str): R to S interval >100 ms in any precordial lead ("yes"/"no")
            av_dissociation (str): Atrioventricular dissociation present ("yes"/"no")
            morphology_criteria_vt (str): Morphology criteria for VT present ("yes"/"no")
            
        Returns:
            Dict with diagnosis and step-by-step analysis
        """
        
        # Validate inputs
        self._validate_inputs(absence_rs_precordial, r_to_s_interval_100ms,
                            av_dissociation, morphology_criteria_vt)
        
        # Apply Brugada algorithm sequentially
        criteria_results = {
            "absence_rs_precordial": absence_rs_precordial.lower() == "yes",
            "r_to_s_interval_100ms": r_to_s_interval_100ms.lower() == "yes",
            "av_dissociation": av_dissociation.lower() == "yes",
            "morphology_criteria_vt": morphology_criteria_vt.lower() == "yes"
        }
        
        # Determine diagnosis using sequential algorithm
        diagnosis_result = self._apply_brugada_algorithm(criteria_results)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(diagnosis_result)
        
        return {
            "result": diagnosis_result["diagnosis"],
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "positive_criterion": diagnosis_result["positive_criterion"],
            "positive_step": diagnosis_result["positive_step"],
            "algorithm_summary": self._get_algorithm_summary(criteria_results),
            "clinical_recommendations": self._get_clinical_recommendations(diagnosis_result["diagnosis"])
        }
    
    def _validate_inputs(self, absence_rs_precordial: str, r_to_s_interval_100ms: str,
                        av_dissociation: str, morphology_criteria_vt: str):
        """Validates input parameters"""
        
        parameters = [
            ("absence_rs_precordial", absence_rs_precordial),
            ("r_to_s_interval_100ms", r_to_s_interval_100ms),
            ("av_dissociation", av_dissociation),
            ("morphology_criteria_vt", morphology_criteria_vt)
        ]
        
        for param_name, param_value in parameters:
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value.lower() not in ['yes', 'no']:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _apply_brugada_algorithm(self, criteria_results: Dict[str, bool]) -> Dict[str, Any]:
        """Applies Brugada algorithm sequentially"""
        
        # Check each criterion in order - first positive = VT
        for step, criterion_info in self.criteria_steps.items():
            criterion_name = criterion_info["criterion"]
            if criteria_results[criterion_name]:
                return {
                    "diagnosis": "VT",
                    "positive_criterion": criterion_info["description"],
                    "positive_step": step,
                    "rationale": criterion_info["interpretation"]
                }
        
        # If all criteria are negative, suggests SVT with aberrancy
        return {
            "diagnosis": "SVT with Aberrancy",
            "positive_criterion": None,
            "positive_step": None,
            "rationale": "All Brugada criteria negative, more consistent with SVT with aberrancy"
        }
    
    def _get_interpretation(self, diagnosis_result: Dict[str, Any]) -> Dict[str, str]:
        """Determines clinical interpretation based on diagnosis"""
        
        if diagnosis_result["diagnosis"] == "VT":
            return {
                "stage": "VT",
                "description": "Ventricular Tachycardia",
                "interpretation": "The ECG findings are consistent with ventricular tachycardia. This is a life-threatening arrhythmia requiring immediate cardioversion or antiarrhythmic therapy. Do not treat with medications intended for SVT (adenosine, calcium channel blockers) as they may worsen the condition."
            }
        else:
            return {
                "stage": "SVT with Aberrancy",
                "description": "Supraventricular Tachycardia with Aberrancy",
                "interpretation": "The ECG findings are more consistent with supraventricular tachycardia with aberrant conduction. However, when in doubt, treat as VT. Consider vagal maneuvers, adenosine, or calcium channel blockers as appropriate for SVT management, but maintain high suspicion for VT."
            }
    
    def _get_algorithm_summary(self, criteria_results: Dict[str, bool]) -> Dict[str, Any]:
        """Provides step-by-step algorithm summary"""
        
        summary = {}
        for step, criterion_info in self.criteria_steps.items():
            criterion_name = criterion_info["criterion"]
            summary[f"step_{step}"] = {
                "criterion": criterion_info["description"],
                "result": "Positive" if criteria_results[criterion_name] else "Negative",
                "interpretation": criterion_info["interpretation"] if criteria_results[criterion_name] else "Does not support VT diagnosis"
            }
        
        return summary
    
    def _get_clinical_recommendations(self, diagnosis: str) -> Dict[str, Any]:
        """Provides clinical recommendations based on diagnosis"""
        
        if diagnosis == "VT":
            return {
                "immediate_actions": [
                    "Assess hemodynamic stability",
                    "Prepare for immediate cardioversion if unstable",
                    "Consider antiarrhythmic therapy if stable"
                ],
                "medications": [
                    "Amiodarone 150mg IV over 10 minutes if stable VT",
                    "Lidocaine 1-1.5mg/kg IV if amiodarone unavailable",
                    "Avoid adenosine and calcium channel blockers"
                ],
                "monitoring": [
                    "Continuous cardiac monitoring",
                    "Blood pressure monitoring",
                    "Prepare for defibrillation"
                ],
                "contraindications": [
                    "Do not give adenosine",
                    "Avoid calcium channel blockers",
                    "Do not use beta-blockers acutely"
                ]
            }
        else:
            return {
                "immediate_actions": [
                    "Assess hemodynamic stability",
                    "Consider vagal maneuvers if stable",
                    "Monitor for response to treatment"
                ],
                "medications": [
                    "Adenosine 6mg IV rapid push, then 12mg if no response",
                    "Diltiazem or verapamil if adenosine fails",
                    "Maintain high suspicion for VT"
                ],
                "monitoring": [
                    "Continuous cardiac monitoring",
                    "Reassess if treatment fails",
                    "Consider VT if no response to SVT treatment"
                ],
                "precautions": [
                    "When in doubt, treat as VT",
                    "Be prepared to switch to VT treatment",
                    "Consider electrophysiology consultation"
                ]
            }


def calculate_brugada_criteria_vt(absence_rs_precordial: str, r_to_s_interval_100ms: str,
                                av_dissociation: str, morphology_criteria_vt: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_brugada_criteria_vt pattern
    """
    calculator = BrugadaCriteriaVtCalculator()
    return calculator.calculate(absence_rs_precordial, r_to_s_interval_100ms,
                              av_dissociation, morphology_criteria_vt)