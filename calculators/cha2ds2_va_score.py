"""
CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk Calculator

Calculates stroke risk for patients with atrial fibrillation; similar to CHA₂DS₂-VASc Score 
but without considering sex. Simplified version recommended in 2024 ESC guidelines.

References:
1. Lip GYH, Keshishian A, Li X, Hamilton M, Masseria C, Gupta K, Mardekian J, Friend K, 
   Nadkarni A, Pan X, Baser O, Deitelzweig S. Effectiveness and Safety of Oral Anticoagulants 
   Among Nonvalvular Atrial Fibrillation Patients. Stroke. 2018;49(12):2933-2944.
2. Hindricks G, Potpara T, Dagres N, et al. 2020 ESC Guidelines for the diagnosis and 
   management of atrial fibrillation developed in collaboration with the European Association 
   for Cardio-Thoracic Surgery (EACTS). Eur Heart J. 2021;42(5):373-498.
3. Romiti GF, Pastori D, Rivera-Caravaca JM, et al. Adherence to the 'Atrial Fibrillation 
   Better Care' pathway in patients with atrial fibrillation: impact on clinical outcomes-a 
   systematic review and meta-analysis of 285,000 patients. Thromb Haemost. 2022;122(3):406-414.
"""

from typing import Dict, Any


class Cha2ds2VaScoreCalculator:
    """Calculator for CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk"""
    
    def __init__(self):
        # Annual stroke risk rates by CHA₂DS₂-VA score
        self.stroke_risk_rates = {
            0: {"rate": 0.5, "risk_level": "Very Low"},
            1: {"rate": 1.5, "risk_level": "Low-Moderate"},
            2: {"rate": 2.9, "risk_level": "High"},
            3: {"rate": 4.6, "risk_level": "High"},
            4: {"rate": 6.7, "risk_level": "High"},
            5: {"rate": 9.2, "risk_level": "Very High"},
            6: {"rate": 11.9, "risk_level": "Very High"},
            7: {"rate": 15.2, "risk_level": "Very High"},
            8: {"rate": 19.5, "risk_level": "Very High"}
        }
        
        # Anticoagulation recommendations by score
        self.anticoagulation_recommendations = {
            0: {
                "recommendation": "No Anticoagulation",
                "details": "Anticoagulation is not recommended. Consider bleeding risk assessment.",
                "strength": "Strong recommendation against",
                "rationale": "Very low stroke risk (0.5 per 100 patient-years) does not justify anticoagulation risks"
            },
            1: {
                "recommendation": "Clinical Judgment Required",
                "details": "Use clinical judgment to weigh risks and benefits of anticoagulation. Consider individual patient factors.",
                "strength": "Weak recommendation",
                "rationale": "Low-moderate stroke risk (1.5 per 100 patient-years) requires individualized assessment"
            }
        }
        
        # Default for scores ≥2
        self.high_risk_recommendation = {
            "recommendation": "Oral Anticoagulation Recommended",
            "details": "Oral anticoagulation is recommended to reduce stroke risk unless contraindicated.",
            "strength": "Strong recommendation for",
            "rationale": "High stroke risk justifies anticoagulation therapy benefits over bleeding risks"
        }
    
    def calculate(
        self,
        age: int,
        congestive_heart_failure: str,
        hypertension: str,
        diabetes_mellitus: str,
        stroke_tia_thromboembolism: str,
        vascular_disease: str
    ) -> Dict[str, Any]:
        """
        Calculates CHA₂DS₂-VA score for stroke risk in atrial fibrillation patients
        
        Args:
            age: Patient age in years
            congestive_heart_failure: History of CHF or LV dysfunction (yes/no)
            hypertension: History of hypertension or current treatment (yes/no)
            diabetes_mellitus: Diabetes mellitus present (yes/no)
            stroke_tia_thromboembolism: Prior stroke, TIA, or thromboembolism (yes/no)
            vascular_disease: Vascular disease present (yes/no)
            
        Returns:
            Dict with CHA₂DS₂-VA score, stroke risk, and anticoagulation recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            age, congestive_heart_failure, hypertension, diabetes_mellitus,
            stroke_tia_thromboembolism, vascular_disease
        )
        
        # Calculate individual component scores
        age_points = self._calculate_age_points(age)
        chf_points = 1 if congestive_heart_failure == "yes" else 0
        htn_points = 1 if hypertension == "yes" else 0
        dm_points = 1 if diabetes_mellitus == "yes" else 0
        stroke_points = 2 if stroke_tia_thromboembolism == "yes" else 0
        vascular_points = 1 if vascular_disease == "yes" else 0
        
        # Calculate total score
        total_score = age_points + chf_points + htn_points + dm_points + stroke_points + vascular_points
        
        # Get stroke risk assessment
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Get anticoagulation recommendation
        anticoag_recommendation = self._get_anticoagulation_recommendation(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            age, age_points, congestive_heart_failure, hypertension, diabetes_mellitus,
            stroke_tia_thromboembolism, vascular_disease
        )
        
        return {
            "result": {
                "total_score": total_score,
                "annual_stroke_risk_percent": risk_assessment["rate"],
                "risk_level": risk_assessment["risk_level"],
                "stroke_incidence": f"{risk_assessment['rate']} per 100 patient-years",
                "anticoagulation_recommendation": anticoag_recommendation["recommendation"],
                "recommendation_details": anticoag_recommendation["details"],
                "recommendation_strength": anticoag_recommendation["strength"],
                "clinical_rationale": anticoag_recommendation["rationale"],
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, age, chf, htn, dm, stroke, vascular):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("congestive_heart_failure", chf),
            ("hypertension", htn),
            ("diabetes_mellitus", dm),
            ("stroke_tia_thromboembolism", stroke),
            ("vascular_disease", vascular)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_age_points(self, age: int) -> int:
        """Calculates age-based points for CHA₂DS₂-VA score"""
        
        if age < 65:
            return 0
        elif age < 75:
            return 1  # Age 65-74 years
        else:
            return 2  # Age ≥75 years
    
    def _get_risk_assessment(self, score: int) -> Dict[str, Any]:
        """Gets stroke risk assessment based on CHA₂DS₂-VA score"""
        
        if score in self.stroke_risk_rates:
            risk_data = self.stroke_risk_rates[score]
        else:
            # Fallback for scores > 8 (should not occur)
            risk_data = {"rate": 19.5, "risk_level": "Very High"}
        
        # Determine stage and description based on score
        if score == 0:
            stage = "Low Risk"
            description = "Very low stroke risk"
            interpretation = f"CHA₂DS₂-VA Score {score}: Very low stroke risk ({risk_data['rate']} strokes per 100 patient-years). Anticoagulation is not recommended. Consider bleeding risk assessment."
        elif score == 1:
            stage = "Moderate Risk"
            description = "Low-moderate stroke risk"
            interpretation = f"CHA₂DS₂-VA Score {score}: Low-moderate stroke risk ({risk_data['rate']} strokes per 100 patient-years). Use clinical judgment to weigh risks and benefits of anticoagulation. Consider individual patient factors."
        else:  # score >= 2
            stage = "High Risk"
            description = "High stroke risk"
            interpretation = f"CHA₂DS₂-VA Score {score}: High stroke risk ({risk_data['rate']} strokes per 100 patient-years). Oral anticoagulation is recommended to reduce stroke risk unless contraindicated."
        
        return {
            "rate": risk_data["rate"],
            "risk_level": risk_data["risk_level"],
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_anticoagulation_recommendation(self, score: int) -> Dict[str, str]:
        """Gets anticoagulation recommendation based on score"""
        
        if score in self.anticoagulation_recommendations:
            return self.anticoagulation_recommendations[score]
        else:
            # For scores ≥2, use high-risk recommendation
            return self.high_risk_recommendation
    
    def _get_scoring_breakdown(self, age, age_points, chf, htn, dm, stroke, vascular):
        """Provides detailed scoring breakdown"""
        
        age_category = ""
        if age < 65:
            age_category = f"Age {age} years (<65)"
        elif age < 75:
            age_category = f"Age {age} years (65-74)"
        else:
            age_category = f"Age {age} years (≥75)"
        
        breakdown = {
            "component_scores": {
                "age": {
                    "category": age_category,
                    "points": age_points,
                    "description": "Age-based scoring: <65y (0 pts), 65-74y (1 pt), ≥75y (2 pts)"
                },
                "congestive_heart_failure": {
                    "present": chf == "yes",
                    "points": 1 if chf == "yes" else 0,
                    "description": "Congestive heart failure or left ventricular dysfunction"
                },
                "hypertension": {
                    "present": htn == "yes",
                    "points": 1 if htn == "yes" else 0,
                    "description": "History of hypertension or current antihypertensive treatment"
                },
                "diabetes_mellitus": {
                    "present": dm == "yes",
                    "points": 1 if dm == "yes" else 0,
                    "description": "Diabetes mellitus"
                },
                "stroke_tia_thromboembolism": {
                    "present": stroke == "yes",
                    "points": 2 if stroke == "yes" else 0,
                    "description": "Prior stroke, TIA, or arterial thromboembolism (worth 2 points)"
                },
                "vascular_disease": {
                    "present": vascular == "yes",
                    "points": 1 if vascular == "yes" else 0,
                    "description": "Vascular disease (MI, peripheral artery disease, aortic plaque)"
                }
            },
            "score_acronym": {
                "C": "Congestive heart failure (1 point)",
                "H": "Hypertension (1 point)",
                "A2": "Age ≥75 years (2 points)",
                "D": "Diabetes mellitus (1 point)",
                "S2": "Prior Stroke/TIA/thromboembolism (2 points)",
                "V": "Vascular disease (1 point)",
                "A": "Age 65-74 years (1 point)"
            },
            "clinical_context": {
                "development": "Simplified version of CHA₂DS₂-VASc removing sex category",
                "guideline": "Recommended in 2024 ESC guidelines",
                "rationale": "Female sex as age-dependent rather than independent risk factor",
                "inclusivity": "Includes non-binary and transgender individuals without gender bias",
                "performance": "Discrimination ability comparable to CHA₂DS₂-VASc score"
            },
            "score_range": {
                "minimum": 0,
                "maximum": 8,
                "current_score": age_points + (1 if chf == "yes" else 0) + (1 if htn == "yes" else 0) + (1 if dm == "yes" else 0) + (2 if stroke == "yes" else 0) + (1 if vascular == "yes" else 0)
            }
        }
        
        return breakdown


def calculate_cha2ds2_va_score(
    age: int,
    congestive_heart_failure: str,
    hypertension: str,
    diabetes_mellitus: str,
    stroke_tia_thromboembolism: str,
    vascular_disease: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Cha2ds2VaScoreCalculator()
    return calculator.calculate(
        age=age,
        congestive_heart_failure=congestive_heart_failure,
        hypertension=hypertension,
        diabetes_mellitus=diabetes_mellitus,
        stroke_tia_thromboembolism=stroke_tia_thromboembolism,
        vascular_disease=vascular_disease
    )