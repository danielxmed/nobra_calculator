"""
Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis Calculator

Determines severity of rheumatoid arthritis using only clinical data, without laboratory tests.
The CDAI provides immediate assessment of RA disease activity for clinical decision-making.

References:
1. Aletaha D, Nell VP, Stamm T, Uffmann M, Pflugbeil S, Machold K, Smolen JS. Acute phase 
   reactants add little to composite disease activity indices for rheumatoid arthritis: 
   validation of a clinical activity score. Arthritis Res Ther. 2005;7(4):R796-806.
2. Smolen JS, Breedveld FC, Schiff MH, Kalden JR, Emery P, Eberl G, van Riel PL, Tugwell P. 
   A simplified disease activity index for rheumatoid arthritis for use in clinical practice. 
   Rheumatology (Oxford). 2003;42(2):244-57.
3. Aletaha D, Smolen JS. The Simplified Disease Activity Index (SDAI) and the Clinical 
   Disease Activity Index (CDAI): a review of their usefulness and validity in rheumatoid 
   arthritis. Clin Exp Rheumatol. 2005;23(5 Suppl 39):S100-8.
"""

from typing import Dict, Any


class CdaiRheumatoidArthritisCalculator:
    """Calculator for Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis"""
    
    def __init__(self):
        # Disease activity categories and thresholds
        self.activity_categories = {
            "remission": {
                "threshold": 2.8,
                "description": "Disease in remission",
                "treatment_goal": "Maintain current therapy",
                "clinical_significance": "Excellent disease control with minimal inflammatory activity"
            },
            "low": {
                "threshold": 10.0,
                "description": "Low disease activity",
                "treatment_goal": "Consider maintaining or tapering therapy",
                "clinical_significance": "Good disease control with acceptable inflammatory activity"
            },
            "moderate": {
                "threshold": 22.0,
                "description": "Moderate disease activity",
                "treatment_goal": "Consider intensifying therapy",
                "clinical_significance": "Suboptimal control with significant inflammatory activity"
            },
            "high": {
                "threshold": float('inf'),
                "description": "High disease activity",
                "treatment_goal": "Urgent need to intensify therapy",
                "clinical_significance": "Poor control with severe inflammatory activity"
            }
        }
        
        # Joint assessment information
        self.joint_assessment_info = {
            "tender_joints": {
                "assessment_method": "28-joint count including shoulders, elbows, wrists, MCPs, PIPs, knees",
                "clinical_significance": "Reflects pain and inflammation from patient perspective"
            },
            "swollen_joints": {
                "assessment_method": "28-joint count assessed by palpation and visual inspection",
                "clinical_significance": "Objective measure of inflammatory joint involvement"
            }
        }
        
        # Global assessment information
        self.global_assessment_info = {
            "patient_global": {
                "scale": "0-10 visual analog scale",
                "anchors": "0 = very well, 10 = very poor",
                "assessment": "Patient's overall assessment of disease impact"
            },
            "provider_global": {
                "scale": "0-10 visual analog scale", 
                "anchors": "0 = very well, 10 = very poor",
                "assessment": "Physician's overall assessment of disease activity"
            }
        }
    
    def calculate(
        self,
        tender_joint_count: int,
        swollen_joint_count: int,
        patient_global_activity: float,
        provider_global_activity: float
    ) -> Dict[str, Any]:
        """
        Calculates CDAI score for rheumatoid arthritis disease activity assessment
        
        Args:
            tender_joint_count: Number of tender joints (0-28)
            swollen_joint_count: Number of swollen joints (0-28)
            patient_global_activity: Patient global assessment (0-10 scale)
            provider_global_activity: Provider global assessment (0-10 scale)
            
        Returns:
            Dict with CDAI score, disease activity category, and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(tender_joint_count, swollen_joint_count,
                            patient_global_activity, provider_global_activity)
        
        # Calculate CDAI score
        cdai_score = self._calculate_cdai_score(
            tender_joint_count, swollen_joint_count,
            patient_global_activity, provider_global_activity
        )
        
        # Get disease activity assessment
        activity_assessment = self._get_activity_assessment(cdai_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            tender_joint_count, swollen_joint_count,
            patient_global_activity, provider_global_activity,
            cdai_score
        )
        
        return {
            "result": cdai_score,
            "unit": "points",
            "interpretation": activity_assessment["interpretation"],
            "stage": activity_assessment["stage"],
            "stage_description": activity_assessment["description"],
            "scoring_breakdown": scoring_breakdown
        }
    
    def _validate_inputs(self, tender_joint_count, swollen_joint_count,
                        patient_global_activity, provider_global_activity):
        """Validates input parameters for CDAI calculation"""
        
        # Validate joint counts
        if not isinstance(tender_joint_count, int) or not (0 <= tender_joint_count <= 28):
            raise ValueError("Tender joint count must be an integer between 0 and 28")
        
        if not isinstance(swollen_joint_count, int) or not (0 <= swollen_joint_count <= 28):
            raise ValueError("Swollen joint count must be an integer between 0 and 28")
        
        # Validate global assessments
        if not (0 <= patient_global_activity <= 10):
            raise ValueError("Patient global activity must be between 0 and 10")
        
        if not (0 <= provider_global_activity <= 10):
            raise ValueError("Provider global activity must be between 0 and 10")
    
    def _calculate_cdai_score(self, tender_joint_count, swollen_joint_count,
                            patient_global_activity, provider_global_activity) -> float:
        """Calculates the CDAI score using the simple additive formula"""
        
        # CDAI = TJC + SJC + PGA + PhGA
        cdai_score = (tender_joint_count + swollen_joint_count + 
                     patient_global_activity + provider_global_activity)
        
        return round(cdai_score, 1)
    
    def _get_activity_assessment(self, cdai_score: float) -> Dict[str, str]:
        """
        Determines disease activity category and clinical recommendations
        
        Args:
            cdai_score: CDAI score
            
        Returns:
            Dict with activity assessment and treatment recommendations
        """
        
        if cdai_score <= 2.8:
            stage = "Remission"
            description = "Disease in remission"
            interpretation = f"CDAI Score {cdai_score}: Disease in remission. Excellent disease control with minimal inflammatory activity. Maintain current therapy and monitor for sustained remission."
            
        elif cdai_score <= 10.0:
            stage = "Low Disease Activity"
            description = "Low disease activity"
            interpretation = f"CDAI Score {cdai_score}: Low disease activity. Good disease control with acceptable inflammatory activity. Consider maintaining current therapy or carefully tapering if in sustained low activity."
            
        elif cdai_score <= 22.0:
            stage = "Moderate Disease Activity"
            description = "Moderate disease activity"
            interpretation = f"CDAI Score {cdai_score}: Moderate disease activity. Suboptimal control with significant inflammatory activity. Consider intensifying therapy to achieve low disease activity or remission."
            
        else:  # cdai_score > 22.0
            stage = "High Disease Activity"
            description = "High disease activity"
            interpretation = f"CDAI Score {cdai_score}: High disease activity. Poor control with severe inflammatory activity. Urgent need to intensify therapy. Consider combination DMARDs or biologics."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, tender_joint_count, swollen_joint_count,
                             patient_global_activity, provider_global_activity,
                             cdai_score) -> Dict[str, Any]:
        """Provides detailed scoring breakdown and clinical context"""
        
        breakdown = {
            "score_components": {
                "tender_joint_count": {
                    "value": tender_joint_count,
                    "max_value": 28,
                    "contribution": tender_joint_count,
                    "percentage": f"{(tender_joint_count / cdai_score * 100):.1f}%" if cdai_score > 0 else "0%",
                    "clinical_significance": "Reflects subjective pain and inflammation from patient perspective",
                    "assessment_method": "28-joint count including shoulders, elbows, wrists, MCPs, PIPs, knees"
                },
                "swollen_joint_count": {
                    "value": swollen_joint_count,
                    "max_value": 28,
                    "contribution": swollen_joint_count,
                    "percentage": f"{(swollen_joint_count / cdai_score * 100):.1f}%" if cdai_score > 0 else "0%",
                    "clinical_significance": "Objective measure of inflammatory joint involvement",
                    "assessment_method": "28-joint count assessed by palpation and visual inspection"
                },
                "patient_global_activity": {
                    "value": patient_global_activity,
                    "max_value": 10,
                    "contribution": patient_global_activity,
                    "percentage": f"{(patient_global_activity / cdai_score * 100):.1f}%" if cdai_score > 0 else "0%",
                    "clinical_significance": "Patient's overall assessment of disease impact on daily life",
                    "assessment_method": "0-10 visual analog scale (0 = very well, 10 = very poor)"
                },
                "provider_global_activity": {
                    "value": provider_global_activity,
                    "max_value": 10,
                    "contribution": provider_global_activity,
                    "percentage": f"{(provider_global_activity / cdai_score * 100):.1f}%" if cdai_score > 0 else "0%",
                    "clinical_significance": "Physician's overall assessment of disease activity",
                    "assessment_method": "0-10 visual analog scale (0 = very well, 10 = very poor)"
                }
            },
            "score_summary": {
                "total_cdai_score": cdai_score,
                "max_possible_score": 76,  # 28 + 28 + 10 + 10
                "activity_category": self._get_activity_category(cdai_score),
                "target_score": "≤2.8 for remission, ≤10 for low disease activity"
            },
            "clinical_guidance": {
                "treatment_recommendations": self._get_treatment_recommendations(cdai_score),
                "monitoring_frequency": self._get_monitoring_recommendations(cdai_score),
                "treatment_targets": self._get_treatment_targets(cdai_score)
            },
            "assessment_advantages": {
                "immediate_availability": "No laboratory tests required - results available immediately",
                "clinical_practicality": "More practical than DAS-28 for routine clinical use",
                "cost_effectiveness": "No additional laboratory costs",
                "patient_engagement": "Incorporates patient perspective in disease assessment"
            },
            "comparison_with_other_indices": {
                "vs_das28": "CDAI shows moderate to good correlation with DAS-28 (Kappa = 0.533)",
                "vs_sdai": "CDAI is SDAI without acute phase reactant (CRP/ESR)",
                "advantages": "Immediate results, no lab dependency, practical for routine use",
                "validation": "Extensively validated and widely accepted in clinical practice"
            },
            "clinical_context": {
                "assessment_timing": "Assess at each clinic visit to monitor treatment response",
                "treat_to_target": "Aim for remission (≤2.8) or low disease activity (≤10)",
                "shared_decision_making": "Include patient perspective in treatment decisions",
                "long_term_outcomes": "Sustained low disease activity prevents joint damage"
            }
        }
        
        return breakdown
    
    def _get_activity_category(self, cdai_score: float) -> str:
        """Returns activity category description"""
        if cdai_score <= 2.8:
            return "Remission"
        elif cdai_score <= 10.0:
            return "Low disease activity"
        elif cdai_score <= 22.0:
            return "Moderate disease activity"
        else:
            return "High disease activity"
    
    def _get_treatment_recommendations(self, cdai_score: float) -> list:
        """Returns treatment recommendations based on CDAI score"""
        if cdai_score <= 2.8:
            return [
                "Maintain current therapy - excellent disease control",
                "Monitor for sustained remission over time",
                "Consider gradual tapering if sustained remission >6 months",
                "Continue regular monitoring to ensure remission maintenance"
            ]
        elif cdai_score <= 10.0:
            return [
                "Continue current therapy - good disease control",
                "Consider maintaining current dose or careful tapering",
                "Monitor closely if considering dose reduction",
                "Aim for achieving and maintaining remission if possible"
            ]
        elif cdai_score <= 22.0:
            return [
                "Consider intensifying therapy - suboptimal control",
                "Evaluate current DMARD therapy effectiveness",
                "Consider combination DMARD therapy or biologic agents",
                "Assess for barriers to treatment adherence"
            ]
        else:
            return [
                "Urgent need to intensify therapy - poor control",
                "Consider combination DMARDs or biologic therapy",
                "Evaluate for rapidly acting interventions",
                "Consider referral to rheumatology specialist if not already involved"
            ]
    
    def _get_monitoring_recommendations(self, cdai_score: float) -> str:
        """Returns monitoring frequency recommendations"""
        if cdai_score <= 2.8:
            return "Every 3-6 months - monitor for sustained remission"
        elif cdai_score <= 10.0:
            return "Every 2-3 months - ensure sustained low disease activity"
        elif cdai_score <= 22.0:
            return "Every 1-2 months - monitor response to therapy intensification"
        else:
            return "Every 2-4 weeks - close monitoring until disease control achieved"
    
    def _get_treatment_targets(self, cdai_score: float) -> Dict[str, str]:
        """Returns treatment targets based on current activity level"""
        if cdai_score <= 2.8:
            return {
                "primary_target": "Maintain remission (CDAI ≤2.8)",
                "secondary_target": "Prevent disease flares and joint damage",
                "long_term_goal": "Sustained drug-free remission if possible"
            }
        elif cdai_score <= 10.0:
            return {
                "primary_target": "Achieve remission (CDAI ≤2.8)",
                "secondary_target": "Maintain low disease activity (CDAI ≤10)",
                "long_term_goal": "Prevent disease progression and joint damage"
            }
        else:
            return {
                "primary_target": "Achieve low disease activity (CDAI ≤10)",
                "secondary_target": "Achieve remission (CDAI ≤2.8) if possible",
                "long_term_goal": "Prevent irreversible joint damage and disability"
            }


def calculate_cdai_rheumatoid_arthritis(
    tender_joint_count: int,
    swollen_joint_count: int,
    patient_global_activity: float,
    provider_global_activity: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CdaiRheumatoidArthritisCalculator()
    return calculator.calculate(
        tender_joint_count=tender_joint_count,
        swollen_joint_count=swollen_joint_count,
        patient_global_activity=patient_global_activity,
        provider_global_activity=provider_global_activity
    )