"""
CATCH (Canadian Assessment of Tomography for Childhood Head injury) Rule Calculator

Predicts clinically significant head injuries in children aged 0-16 years to guide CT imaging decisions.
Identifies high-risk factors for neurologic intervention and medium-risk factors for brain injury on CT.

References:
1. Osmond MH, Klassen TP, Wells GA, Correll R, Jarvis A, Joubert G, et al; Pediatric Emergency 
   Research Canada (PERC). CATCH: a clinical decision rule for the use of computed tomography 
   in children with minor head injury. CMAJ. 2010 Mar 9;182(4):341-8. doi: 10.1503/cmaj.091421.
2. Lyttle MD, Crowe L, Oakley E, Dunning J, Babl FE. Comparing CATCH, CHALICE and PECARN 
   clinical decision rules for paediatric head injuries. Emerg Med J. 2012 Oct;29(10):785-94. 
   doi: 10.1136/emermed-2011-200225.
3. Easter JS, Bakes K, Dhaliwal J, Miller M, Caruso E, Haukoos JS. Comparison of PECARN, CATCH, 
   and CHALICE rules for children with minor head injury: a prospective cohort study. 
   Ann Emerg Med. 2014 Aug;64(2):145-52, 152.e1-5. doi: 10.1016/j.annemergmed.2014.01.030.
"""

from typing import Dict, Any, List


class CatchRuleCalculator:
    """Calculator for CATCH (Canadian Assessment of Tomography for Childhood Head injury) Rule"""
    
    def __init__(self):
        # High-risk factors (predict need for neurologic intervention)
        self.high_risk_factors = [
            "gcs_less_than_15",
            "suspected_skull_fracture", 
            "worsening_headache",
            "irritability_on_exam"
        ]
        
        # Medium-risk factors (predict brain injury on CT)
        self.medium_risk_factors = [
            "basal_skull_fracture_signs",
            "large_scalp_hematoma",
            "dangerous_mechanism"
        ]
    
    def calculate(
        self,
        gcs_less_than_15: str,
        suspected_skull_fracture: str,
        worsening_headache: str,
        irritability_on_exam: str,
        basal_skull_fracture_signs: str,
        large_scalp_hematoma: str,
        dangerous_mechanism: str
    ) -> Dict[str, Any]:
        """
        Calculates CATCH Rule assessment for pediatric head injury
        
        Args:
            gcs_less_than_15: GCS <15 at 2 hours after injury
            suspected_skull_fracture: Suspected open or depressed skull fracture
            worsening_headache: History of worsening headache
            irritability_on_exam: Irritability on examination
            basal_skull_fracture_signs: Signs of basal skull fracture
            large_scalp_hematoma: Large, boggy scalp hematoma
            dangerous_mechanism: Dangerous mechanism of injury
            
        Returns:
            Dict with CATCH assessment and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            gcs_less_than_15, suspected_skull_fracture, worsening_headache,
            irritability_on_exam, basal_skull_fracture_signs, large_scalp_hematoma,
            dangerous_mechanism
        )
        
        # Create parameter dictionary
        params = {
            "gcs_less_than_15": gcs_less_than_15,
            "suspected_skull_fracture": suspected_skull_fracture,
            "worsening_headache": worsening_headache,
            "irritability_on_exam": irritability_on_exam,
            "basal_skull_fracture_signs": basal_skull_fracture_signs,
            "large_scalp_hematoma": large_scalp_hematoma,
            "dangerous_mechanism": dangerous_mechanism
        }
        
        # Assess risk factors
        high_risk_present = self._assess_high_risk_factors(params)
        medium_risk_present = self._assess_medium_risk_factors(params)
        
        # Get detailed assessment
        factor_assessment = self._get_factor_assessment(params)
        
        # Determine overall risk and recommendations
        risk_assessment = self._determine_risk_level(high_risk_present, medium_risk_present)
        
        return {
            "result": {
                "high_risk_factors_present": high_risk_present,
                "medium_risk_factors_present": medium_risk_present,
                "any_risk_factors_present": high_risk_present or medium_risk_present,
                "risk_level": risk_assessment["risk_level"],
                "ct_recommendation": risk_assessment["ct_recommendation"],
                "factor_assessment": factor_assessment
            },
            "unit": "risk_level",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        for arg in args:
            if arg not in valid_options:
                raise ValueError("All parameters must be 'yes' or 'no'")
    
    def _assess_high_risk_factors(self, params: Dict[str, str]) -> bool:
        """Assesses presence of any high-risk factors"""
        
        return any(params[factor] == "yes" for factor in self.high_risk_factors)
    
    def _assess_medium_risk_factors(self, params: Dict[str, str]) -> bool:
        """Assesses presence of any medium-risk factors"""
        
        return any(params[factor] == "yes" for factor in self.medium_risk_factors)
    
    def _get_factor_assessment(self, params: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        """Provides detailed assessment of each factor"""
        
        assessment = {}
        
        # High-risk factors
        assessment["high_risk"] = {
            "gcs_less_than_15": {
                "present": params["gcs_less_than_15"] == "yes",
                "description": "GCS <15 at 2 hours after injury"
            },
            "suspected_skull_fracture": {
                "present": params["suspected_skull_fracture"] == "yes",
                "description": "Suspected open or depressed skull fracture"
            },
            "worsening_headache": {
                "present": params["worsening_headache"] == "yes",
                "description": "History of worsening headache"
            },
            "irritability_on_exam": {
                "present": params["irritability_on_exam"] == "yes",
                "description": "Irritability on examination"
            }
        }
        
        # Medium-risk factors
        assessment["medium_risk"] = {
            "basal_skull_fracture_signs": {
                "present": params["basal_skull_fracture_signs"] == "yes",
                "description": "Signs of basal skull fracture (hemotympanum, raccoon eyes, CSF leak)"
            },
            "large_scalp_hematoma": {
                "present": params["large_scalp_hematoma"] == "yes",
                "description": "Large, boggy scalp hematoma (frontal, temporal, or parietal)"
            },
            "dangerous_mechanism": {
                "present": params["dangerous_mechanism"] == "yes",
                "description": "Dangerous mechanism (MVC >60 km/h, fall >3 feet/5 stairs, axial load)"
            }
        }
        
        return assessment
    
    def _determine_risk_level(self, high_risk: bool, medium_risk: bool) -> Dict[str, str]:
        """Determines overall risk level and recommendations"""
        
        if high_risk:
            return {
                "risk_level": "High Risk",
                "stage": "High Risk",
                "description": "High-risk factors present",
                "ct_recommendation": "CT imaging strongly recommended",
                "interpretation": "High risk for neurologic intervention required. CT imaging strongly recommended. High-risk factors predict need for neurologic intervention with 100% sensitivity (95% CI: 86.2%-100%). Consider urgent neurosurgical consultation if CT shows abnormalities."
            }
        elif medium_risk:
            return {
                "risk_level": "Medium Risk", 
                "stage": "Medium Risk",
                "description": "Medium-risk factors present",
                "ct_recommendation": "Consider CT imaging",
                "interpretation": "Medium risk for brain injury on CT. Consider CT imaging based on clinical judgment. Medium-risk factors identify brain injury on CT with 98.1% sensitivity (95% CI: 94.6%-99.4%). Absence of medium-risk factors has high negative predictive value."
            }
        else:
            return {
                "risk_level": "Low Risk",
                "stage": "Low Risk", 
                "description": "No high-risk or medium-risk factors",
                "ct_recommendation": "CT not routinely indicated",
                "interpretation": "Low risk for clinically significant head injury. CT not routinely indicated. Consider clinical observation and discharge planning per institutional protocols. However, clinical judgment should always supplement decision rules in pediatric head trauma."
            }


def calculate_catch_rule(
    gcs_less_than_15: str,
    suspected_skull_fracture: str,
    worsening_headache: str,
    irritability_on_exam: str,
    basal_skull_fracture_signs: str,
    large_scalp_hematoma: str,
    dangerous_mechanism: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CatchRuleCalculator()
    return calculator.calculate(
        gcs_less_than_15=gcs_less_than_15,
        suspected_skull_fracture=suspected_skull_fracture,
        worsening_headache=worsening_headache,
        irritability_on_exam=irritability_on_exam,
        basal_skull_fracture_signs=basal_skull_fracture_signs,
        large_scalp_hematoma=large_scalp_hematoma,
        dangerous_mechanism=dangerous_mechanism
    )