"""
CHADS-65 (Canadian Society of Cardiology Guideline) Calculator

Clinical decision algorithm developed by the Canadian Cardiovascular Society 
to guide antithrombotic therapy for patients with nonvalvular atrial fibrillation.

References:
1. Andrade JG, Aguilar M, Atzema C, Bell A, Cairns JA, Cheung CC, et al. 
   The 2020 Canadian Cardiovascular Society/Canadian Heart Rhythm Society 
   Comprehensive Guidelines for the Management of Atrial Fibrillation. 
   Can J Cardiol. 2020 Dec;36(12):1847-1948. doi: 10.1016/j.cjca.2020.09.001.
2. Verma A, Cairns JA, Mitchell LB, Macle L, Stiell IG, Gladstone D, et al. 
   2014 focused update of the Canadian Cardiovascular Society Guidelines for 
   the management of atrial fibrillation. Can J Cardiol. 2014 Oct;30(10):1114-30. 
   doi: 10.1016/j.cjca.2014.08.001.
"""

from typing import Dict, Any


class Chads65Calculator:
    """Calculator for CHADS-65 Decision Algorithm"""
    
    def __init__(self):
        # Treatment recommendations
        self.recommendations = {
            "oral_anticoagulation": {
                "therapy": "Oral Anticoagulation (OAC)",
                "medication": "Direct oral anticoagulants (DOACs) preferred over warfarin",
                "indication": "Stroke prevention in nonvalvular atrial fibrillation",
                "monitoring": "Regular follow-up for efficacy and bleeding complications",
                "contraindications": "Assess bleeding risk, drug interactions, and patient preferences"
            },
            "antiplatelet_therapy": {
                "therapy": "Antiplatelet Therapy",
                "medication": "ASA 81mg daily",
                "indication": "Stroke prevention in patients with vascular disease but low CHADS₂ risk",
                "monitoring": "Annual reassessment and bleeding risk evaluation",
                "contraindications": "History of major bleeding, peptic ulcer disease"
            },
            "no_therapy": {
                "therapy": "No Antithrombotic Therapy",
                "medication": "No anticoagulation or antiplatelet therapy recommended",
                "indication": "Very low stroke risk based on age and comorbidities",
                "monitoring": "Annual reassessment as risk factors may change with time",
                "contraindications": "N/A"
            }
        }
    
    def calculate(
        self,
        age_65_or_older: str,
        congestive_heart_failure: str,
        hypertension: str,
        diabetes_mellitus: str,
        stroke_tia_history: str,
        coronary_artery_disease: str,
        peripheral_artery_disease: str
    ) -> Dict[str, Any]:
        """
        Applies CHADS-65 decision algorithm for antithrombotic therapy
        
        Args:
            age_65_or_older: Patient age 65 years or older
            congestive_heart_failure: History of CHF or LV dysfunction
            hypertension: History of hypertension or current treatment
            diabetes_mellitus: History of diabetes or current treatment
            stroke_tia_history: Previous stroke, TIA, or thromboembolism
            coronary_artery_disease: CAD including MI or revascularization
            peripheral_artery_disease: PAD including amputation, bypass, or angioplasty
            
        Returns:
            Dict with algorithm result, therapy recommendation, and clinical guidance
        """
        
        # Validate inputs
        self._validate_inputs(
            age_65_or_older, congestive_heart_failure, hypertension,
            diabetes_mellitus, stroke_tia_history, coronary_artery_disease,
            peripheral_artery_disease
        )
        
        # Apply decision algorithm
        decision_result = self._apply_algorithm(
            age_65_or_older, congestive_heart_failure, hypertension,
            diabetes_mellitus, stroke_tia_history, coronary_artery_disease,
            peripheral_artery_disease
        )
        
        # Get detailed recommendation
        recommendation = self._get_recommendation(decision_result["therapy_type"])
        
        # Get algorithm breakdown
        algorithm_breakdown = self._get_algorithm_breakdown(
            age_65_or_older, congestive_heart_failure, hypertension,
            diabetes_mellitus, stroke_tia_history, coronary_artery_disease,
            peripheral_artery_disease, decision_result
        )
        
        return {
            "result": {
                "therapy_recommendation": decision_result["therapy_type"],
                "decision_step": decision_result["decision_step"],
                "rationale": decision_result["rationale"],
                "medication_details": recommendation["medication"],
                "indication": recommendation["indication"],
                "monitoring_requirements": recommendation["monitoring"],
                "clinical_considerations": recommendation["contraindications"],
                "algorithm_breakdown": algorithm_breakdown
            },
            "unit": "algorithm",
            "interpretation": decision_result["interpretation"],
            "stage": decision_result["therapy_type"],
            "stage_description": decision_result["description"]
        }
    
    def _validate_inputs(self, age_65, chf, htn, dm, stroke, cad, pad):
        """Validates input parameters"""
        
        parameters = [
            ("age_65_or_older", age_65),
            ("congestive_heart_failure", chf),
            ("hypertension", htn),
            ("diabetes_mellitus", dm),
            ("stroke_tia_history", stroke),
            ("coronary_artery_disease", cad),
            ("peripheral_artery_disease", pad)
        ]
        
        valid_yes_no = ["yes", "no"]
        
        for param_name, param_value in parameters:
            if param_value not in valid_yes_no:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _apply_algorithm(self, age_65, chf, htn, dm, stroke, cad, pad):
        """Applies the CHADS-65 decision algorithm"""
        
        # Step 1: Age ≥65 assessment
        if age_65 == "yes":
            return {
                "therapy_type": "Oral Anticoagulation",
                "decision_step": "Step 1: Age Assessment",
                "rationale": "Age ≥65 years qualifies for oral anticoagulation",
                "description": "Age ≥65 or CHADS₂ risk factors present",
                "interpretation": "CHADS-65 Algorithm - Step 1: Age ≥65 years. Oral anticoagulation recommended. Direct oral anticoagulants (DOACs) preferred over warfarin for stroke prevention in nonvalvular atrial fibrillation. Annual stroke risk: 2.1% for ages 65-74, 4.4% for ages ≥75."
            }
        
        # Step 2: CHADS₂ risk factors assessment (excluding age)
        chads2_risk_factors = [chf, htn, dm, stroke]
        if any(factor == "yes" for factor in chads2_risk_factors):
            present_factors = []
            if chf == "yes":
                present_factors.append("Congestive Heart Failure")
            if htn == "yes":
                present_factors.append("Hypertension")
            if dm == "yes":
                present_factors.append("Diabetes Mellitus")
            if stroke == "yes":
                present_factors.append("Stroke/TIA History")
            
            return {
                "therapy_type": "Oral Anticoagulation",
                "decision_step": "Step 2: CHADS₂ Risk Factor Assessment",
                "rationale": f"CHADS₂ risk factors present: {', '.join(present_factors)}",
                "description": "Age ≥65 or CHADS₂ risk factors present",
                "interpretation": f"CHADS-65 Algorithm - Step 2: CHADS₂ risk factors present ({', '.join(present_factors)}). Oral anticoagulation recommended despite age <65 years. These risk factors significantly increase stroke risk and warrant anticoagulation therapy."
            }
        
        # Step 3: Vascular disease assessment
        if cad == "yes" or pad == "yes":
            vascular_diseases = []
            if cad == "yes":
                vascular_diseases.append("Coronary Artery Disease")
            if pad == "yes":
                vascular_diseases.append("Peripheral Artery Disease")
            
            return {
                "therapy_type": "Antiplatelet Therapy",
                "decision_step": "Step 3: Vascular Disease Assessment",
                "rationale": f"Vascular disease present: {', '.join(vascular_diseases)}",
                "description": "Age <65, no CHADS₂ risk factors, vascular disease present",
                "interpretation": f"CHADS-65 Algorithm - Step 3: Vascular disease present ({', '.join(vascular_diseases)}) in patient <65 years without CHADS₂ risk factors. Antiplatelet therapy with ASA 81mg daily recommended for stroke prevention."
            }
        
        # No therapy recommended
        return {
            "therapy_type": "No Antithrombotic Therapy",
            "decision_step": "Step 3: No High-Risk Features",
            "rationale": "Age <65 years, no CHADS₂ risk factors, no vascular disease",
            "description": "Age <65, no CHADS₂ risk factors, no vascular disease",
            "interpretation": "CHADS-65 Algorithm - No high-risk features: Age <65 years, no CHADS₂ risk factors, and no vascular disease. No antithrombotic therapy recommended. Annual reassessment advised as patient age and risk factors may change."
        }
    
    def _get_recommendation(self, therapy_type: str) -> Dict[str, str]:
        """Gets detailed recommendation based on therapy type"""
        
        therapy_mapping = {
            "Oral Anticoagulation": "oral_anticoagulation",
            "Antiplatelet Therapy": "antiplatelet_therapy",
            "No Antithrombotic Therapy": "no_therapy"
        }
        
        return self.recommendations.get(
            therapy_mapping.get(therapy_type, "no_therapy"),
            self.recommendations["no_therapy"]
        )
    
    def _get_algorithm_breakdown(self, age_65, chf, htn, dm, stroke, cad, pad, decision):
        """Provides detailed algorithm breakdown"""
        
        return {
            "algorithm_steps": {
                "step_1_age_assessment": {
                    "question": "Is patient ≥65 years old?",
                    "answer": "Yes" if age_65 == "yes" else "No",
                    "result": "Proceed to OAC" if age_65 == "yes" else "Proceed to Step 2"
                },
                "step_2_chads2_assessment": {
                    "question": "Any CHADS₂ risk factors present?",
                    "risk_factors": {
                        "congestive_heart_failure": chf == "yes",
                        "hypertension": htn == "yes",
                        "diabetes_mellitus": dm == "yes",
                        "stroke_tia_history": stroke == "yes"
                    },
                    "any_present": any([chf == "yes", htn == "yes", dm == "yes", stroke == "yes"]),
                    "result": "Proceed to OAC" if any([chf == "yes", htn == "yes", dm == "yes", stroke == "yes"]) else "Proceed to Step 3"
                },
                "step_3_vascular_assessment": {
                    "question": "Coronary or peripheral artery disease present?",
                    "vascular_diseases": {
                        "coronary_artery_disease": cad == "yes",
                        "peripheral_artery_disease": pad == "yes"
                    },
                    "any_present": cad == "yes" or pad == "yes",
                    "result": "ASA therapy" if (cad == "yes" or pad == "yes") else "No therapy"
                }
            },
            "final_decision": {
                "decision_step": decision["decision_step"],
                "therapy_recommendation": decision["therapy_type"],
                "rationale": decision["rationale"]
            },
            "clinical_context": {
                "algorithm_type": "Sequential decision tree (not numerical scoring)",
                "primary_endpoint": "Stroke prevention in nonvalvular atrial fibrillation",
                "evidence_level": "Strong Recommendation, High-Quality Evidence (CCS 2020)",
                "key_principle": "Age ≥65 years alone is sufficient for anticoagulation"
            }
        }


def calculate_chads_65(
    age_65_or_older: str,
    congestive_heart_failure: str,
    hypertension: str,
    diabetes_mellitus: str,
    stroke_tia_history: str,
    coronary_artery_disease: str,
    peripheral_artery_disease: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Chads65Calculator()
    return calculator.calculate(
        age_65_or_older=age_65_or_older,
        congestive_heart_failure=congestive_heart_failure,
        hypertension=hypertension,
        diabetes_mellitus=diabetes_mellitus,
        stroke_tia_history=stroke_tia_history,
        coronary_artery_disease=coronary_artery_disease,
        peripheral_artery_disease=peripheral_artery_disease
    )