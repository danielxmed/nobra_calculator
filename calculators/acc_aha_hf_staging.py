"""
ACC/AHA Heart Failure Staging Calculator

Describes heart failure stages and provides stage-specific therapy
recommendations, based on ACC/AHA/HFSA 2022 guidelines.
"""

from typing import Dict, Any, Optional


class AccAhaHfStagingCalculator:
    """Calculator for ACC/AHA Heart Failure Staging"""
    
    def calculate(self, risk_factors: str, structural_disease: str, 
                 current_symptoms: str, advanced_symptoms: str,
                 hospitalization_frequency: str, 
                 ejection_fraction: Optional[float] = None) -> Dict[str, Any]:
        """
        Determines the ACC/AHA heart failure stage
        
        Args:
            risk_factors (str): Risk factors for HF ("yes" or "no")
            structural_disease (str): Structural heart disease ("yes" or "no")
            current_symptoms (str): Current/previous HF symptoms ("yes" or "no")
            advanced_symptoms (str): Refractory severe symptoms ("yes" or "no")
            hospitalization_frequency (str): Hospitalization frequency ("frequent", "rare", "none")
            ejection_fraction (Optional[float]): LV ejection fraction (%)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(
            risk_factors, structural_disease, current_symptoms, 
            advanced_symptoms, hospitalization_frequency, ejection_fraction
        )
        
        # Determine stage based on hierarchical logic
        stage = self._determine_stage(
            risk_factors, structural_disease, current_symptoms, 
            advanced_symptoms, hospitalization_frequency
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(stage)
        
        # Get specific therapeutic recommendations
        therapy_recommendations = self._get_therapy_recommendations(stage, ejection_fraction)
        
        # Assess prognosis
        prognosis = self._assess_prognosis(stage, ejection_fraction)
        
        return {
            "result": stage,
            "unit": "stage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "therapy_recommendations": therapy_recommendations,
            "prognosis": prognosis,
            "ejection_fraction": ejection_fraction,
            "can_regress": False  # Important characteristic of the ACC/AHA system
        }
    
    def _validate_inputs(self, risk_factors, structural_disease, current_symptoms,
                        advanced_symptoms, hospitalization_frequency, ejection_fraction):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_hospitalization = ["frequent", "rare", "none"]
        
        if risk_factors not in valid_yes_no:
            raise ValueError(f"risk_factors must be: {', '.join(valid_yes_no)}")
        
        if structural_disease not in valid_yes_no:
            raise ValueError(f"structural_disease must be: {', '.join(valid_yes_no)}")
        
        if current_symptoms not in valid_yes_no:
            raise ValueError(f"current_symptoms must be: {', '.join(valid_yes_no)}")
        
        if advanced_symptoms not in valid_yes_no:
            raise ValueError(f"advanced_symptoms must be: {', '.join(valid_yes_no)}")
        
        if hospitalization_frequency not in valid_hospitalization:
            raise ValueError(f"hospitalization_frequency must be: {', '.join(valid_hospitalization)}")
        
        if ejection_fraction is not None:
            if not isinstance(ejection_fraction, (int, float)) or ejection_fraction < 0.0 or ejection_fraction > 100.0:
                raise ValueError("Ejection fraction must be between 0.0 and 100.0%")
    
    def _determine_stage(self, risk_factors, structural_disease, current_symptoms,
                        advanced_symptoms, hospitalization_frequency):
        """
        Determines the stage based on ACC/AHA hierarchical logic
        
        Returns:
            str: Determined stage (A, B, C or D)
        """
        
        # Stage D: Refractory advanced symptoms
        if (advanced_symptoms == "yes" or 
            hospitalization_frequency == "frequent"):
            return "D"
        
        # Stage C: Current or previous HF symptoms
        if current_symptoms == "yes":
            return "C"
        
        # Stage B: Structural disease without symptoms
        if structural_disease == "yes":
            return "B"
        
        # Stage A: Only risk factors
        if risk_factors == "yes":
            return "A"
        
        # If no criteria, consider stage A (primary prevention)
        return "A"
    
    def _get_therapy_recommendations(self, stage: str, ejection_fraction: Optional[float]) -> Dict[str, Any]:
        """
        Gets specific therapeutic recommendations by stage
        
        Args:
            stage (str): HF stage
            ejection_fraction (Optional[float]): Ejection fraction
            
        Returns:
            Dict with therapeutic recommendations
        """
        
        recommendations = {
            "A": {
                "primary": [
                    "Hypertension control",
                    "Dyslipidemia control",
                    "ACEI or ARB if hypertensive or diabetic",
                    "Lifestyle modifications"
                ],
                "lifestyle": [
                    "Regular exercise",
                    "Maintain normal weight",
                    "Healthy diet",
                    "Smoking cessation"
                ],
                "medications": [
                    "SGLT2i in diabetics with high CV risk",
                    "Statins if indicated"
                ]
            },
            "B": {
                "primary": [
                    "ACEI or ARB (LVEF ≤40%)",
                    "Evidence-based beta-blockers",
                    "Statins",
                    "All measures from Stage A"
                ],
                "devices": [
                    "ICD if LVEF ≤30% post-MI (>40 days)",
                    "ICD in asymptomatic ischemic cardiomyopathy"
                ],
                "monitoring": [
                    "Follow-up echocardiogram",
                    "Renal function monitoring"
                ]
            },
            "C": {
                "primary": [
                    "ACEI or ARB",
                    "Beta-blockers",
                    "Diuretics (if fluid retention)",
                    "All measures from Stages A and B"
                ],
                "additional": [
                    "Aldosterone antagonists (LVEF ≤35%)",
                    "Sodium restriction (<3g/day)",
                    "Supervised exercise",
                    "Isosorbide + hydralazine (if indicated)"
                ],
                "devices": [
                    "ICD if LVEF ≤35%",
                    "CRT if indicated"
                ]
            },
            "D": {
                "primary": [
                    "All optimized measures from Stage C",
                    "Referral to specialized team",
                    "Evaluation for advanced therapies"
                ],
                "advanced": [
                    "Ventricular assist device (VAD)",
                    "Heart transplant",
                    "Palliative inotropes",
                    "Palliative care"
                ],
                "palliation": [
                    "Symptom control",
                    "Discussion about care goals",
                    "Psychosocial support"
                ]
            }
        }
        
        return recommendations.get(stage, {})
    
    def _assess_prognosis(self, stage: str, ejection_fraction: Optional[float]) -> Dict[str, str]:
        """
        Assesses prognosis based on stage and LVEF
        
        Args:
            stage (str): HF stage
            ejection_fraction (Optional[float]): Ejection fraction
            
        Returns:
            Dict with prognostic assessment
        """
        
        prognosis_map = {
            "A": {
                "outlook": "Excellent with appropriate treatment",
                "mortality": "Low",
                "progression": "Preventable with appropriate measures"
            },
            "B": {
                "outlook": "Good with optimized treatment",
                "mortality": "Low to moderate",
                "progression": "Prevention of symptoms is the goal"
            },
            "C": {
                "outlook": "Moderate, dependent on control",
                "mortality": "Moderate to high",
                "progression": "Focus on symptom and hospitalization control"
            },
            "D": {
                "outlook": "Reserved",
                "mortality": "High",
                "progression": "Palliative care and advanced therapies"
            }
        }
        
        prognosis = prognosis_map.get(stage, {})
        
        # Modify prognosis based on LVEF if available
        if ejection_fraction is not None and stage in ["B", "C", "D"]:
            if ejection_fraction <= 35:
                prognosis["ef_note"] = "Reduced LVEF - higher risk"
            elif ejection_fraction <= 40:
                prognosis["ef_note"] = "Slightly reduced LVEF"
            else:
                prognosis["ef_note"] = "Preserved LVEF"
        
        return prognosis
    
    def _get_interpretation(self, stage: str) -> Dict[str, str]:
        """
        Gets stage interpretation
        
        Args:
            stage (str): Determined stage
            
        Returns:
            Dict with interpretation
        """
        
        interpretations = {
            "A": {
                "stage": "Stage A",
                "description": "At risk for heart failure",
                "interpretation": "Patients with risk factors but no structural disease or symptoms. Recommendations: hypertension and dyslipidemia control, ACEI/ARB, lifestyle modifications, SGLT2i in diabetics. Goal: prevent HF development."
            },
            "B": {
                "stage": "Stage B",
                "description": "Pre-heart failure",
                "interpretation": "Structural disease without symptoms. Recommendations: ACEI/ARB, beta-blockers, statins, ICD if indicated (LVEF ≤30% post-MI). Goal: prevent progression to symptomatic HF."
            },
            "C": {
                "stage": "Stage C",
                "description": "Symptomatic heart failure",
                "interpretation": "Structural disease with current/previous symptoms. Recommendations: ACEI/ARB, beta-blockers, diuretics, aldosterone antagonists (LVEF ≤35%), supervised exercise, sodium restriction. Goal: symptom control and hospitalization prevention."
            },
            "D": {
                "stage": "Stage D",
                "description": "Advanced heart failure",
                "interpretation": "Refractory severe symptoms. Recommendations: specialized HF team, evaluation for advanced therapies (VAD, transplant), palliative care, palliative inotropes. Goal: symptom improvement and quality of life."
            }
        }
        
        return interpretations.get(stage, interpretations["A"])


def calculate_acc_aha_hf_staging(risk_factors: str, structural_disease: str, 
                                current_symptoms: str, advanced_symptoms: str,
                                hospitalization_frequency: str, 
                                ejection_fraction: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AccAhaHfStagingCalculator()
    return calculator.calculate(
        risk_factors, structural_disease, current_symptoms, 
        advanced_symptoms, hospitalization_frequency, ejection_fraction
    )
