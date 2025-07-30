"""
Central Nervous System International Prognostic Index (CNS-IPI) Calculator

Prognostic scoring system that predicts the risk of CNS relapse in patients 
with diffuse large B-cell lymphoma (DLBCL) treated with R-CHOP chemotherapy.

References:
1. Schmitz N, Zeynalova S, Nickelsen M, Kansara R, Villa D, Sehn LH, et al. 
   CNS International Prognostic Index: A Risk Model for CNS Relapse in Patients 
   With Diffuse Large B-Cell Lymphoma Treated With R-CHOP. J Clin Oncol. 
   2016 Sep 10;34(26):3150-3156. doi: 10.1200/JCO.2015.65.6520.
2. Ma'koseh M, Rahahleh N, Abdel-Razeq H. Impact of Central Nervous System 
   International Prognostic Index on the Treatment of Diffuse Large B Cell 
   Lymphoma. Cureus. 2021 Aug 13;13(8):e17016. doi: 10.7759/cureus.17016.
"""

from typing import Dict, Any


class CnsIpiCalculator:
    """Calculator for Central Nervous System International Prognostic Index (CNS-IPI)"""
    
    def __init__(self):
        # Risk categories with patient distribution and relapse rates
        self.risk_categories = {
            "low": {
                "score_range": (0, 1),
                "patient_distribution": 46,
                "relapse_rate": 0.6,
                "confidence_interval": "0%-1.2%",
                "description": "Very low CNS relapse risk",
                "recommendation": "CNS prophylaxis generally not recommended"
            },
            "intermediate": {
                "score_range": (2, 3),
                "patient_distribution": 41,
                "relapse_rate": 3.4,
                "confidence_interval": "2.2%-4.4%",
                "description": "Low to moderate CNS relapse risk",
                "recommendation": "CNS prophylaxis may be considered based on additional risk factors"
            },
            "high": {
                "score_range": (4, 6),
                "patient_distribution": 12,
                "relapse_rate": 10.2,
                "confidence_interval": "6.3%-14.1%",
                "description": "High CNS relapse risk",
                "recommendation": "CNS prophylaxis strongly recommended"
            }
        }
    
    def calculate(
        self,
        age_over_60: str,
        elevated_ldh: str,
        ecog_performance_status_over_1: str,
        advanced_stage: str,
        multiple_extranodal_sites: str,
        kidney_adrenal_involvement: str
    ) -> Dict[str, Any]:
        """
        Calculates CNS-IPI score for CNS relapse risk in DLBCL patients
        
        Args:
            age_over_60: Patient age greater than 60 years
            elevated_ldh: LDH level above normal laboratory range
            ecog_performance_status_over_1: ECOG PS >1 (moderate to severe limitation)
            advanced_stage: Ann Arbor stage III or IV disease
            multiple_extranodal_sites: More than 1 extranodal disease site
            kidney_adrenal_involvement: Involvement of kidney and/or adrenal gland
            
        Returns:
            Dict with CNS-IPI score, risk category, and prophylaxis recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            age_over_60, elevated_ldh, ecog_performance_status_over_1,
            advanced_stage, multiple_extranodal_sites, kidney_adrenal_involvement
        )
        
        # Calculate total score
        total_score = self._calculate_total_score(
            age_over_60, elevated_ldh, ecog_performance_status_over_1,
            advanced_stage, multiple_extranodal_sites, kidney_adrenal_involvement
        )
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            age_over_60, elevated_ldh, ecog_performance_status_over_1,
            advanced_stage, multiple_extranodal_sites, kidney_adrenal_involvement
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, age_over_60, elevated_ldh, ecog_ps, advanced_stage, 
                        multiple_extranodal, kidney_adrenal):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        
        parameters = [
            ("age_over_60", age_over_60),
            ("elevated_ldh", elevated_ldh),
            ("ecog_performance_status_over_1", ecog_ps),
            ("advanced_stage", advanced_stage),
            ("multiple_extranodal_sites", multiple_extranodal),
            ("kidney_adrenal_involvement", kidney_adrenal)
        ]
        
        for param_name, param_value in parameters:
            if param_value not in valid_yes_no:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, age_over_60, elevated_ldh, ecog_ps, 
                              advanced_stage, multiple_extranodal, kidney_adrenal):
        """Calculates total CNS-IPI score (0-6 points)"""
        
        score = 0
        
        # Each parameter contributes 1 point if "yes"
        if age_over_60 == "yes":
            score += 1
        
        if elevated_ldh == "yes":
            score += 1
        
        if ecog_ps == "yes":
            score += 1
        
        if advanced_stage == "yes":
            score += 1
        
        if multiple_extranodal == "yes":
            score += 1
        
        if kidney_adrenal == "yes":
            score += 1
        
        return score
    
    def _get_risk_assessment(self, score: int) -> Dict[str, Any]:
        """Gets risk assessment based on CNS-IPI score"""
        
        for risk_level, risk_data in self.risk_categories.items():
            min_score, max_score = risk_data["score_range"]
            if min_score <= score <= max_score:
                return self._format_risk_assessment(risk_level, risk_data, score)
        
        # Fallback (should not occur with valid scores 0-6)
        return {
            "category": "Unknown",
            "stage": "Unknown Risk",
            "description": "Score outside validated range",
            "relapse_rate": "Unknown",
            "confidence_interval": "Unknown",
            "patient_distribution": "Unknown",
            "recommendation": "Clinical assessment required",
            "interpretation": f"CNS-IPI Score {score}: Score outside validated range. Clinical assessment required."
        }
    
    def _format_risk_assessment(self, risk_level: str, risk_data: Dict, score: int) -> Dict[str, Any]:
        """Formats risk assessment with detailed interpretation"""
        
        stage_mapping = {
            "low": "Low Risk",
            "intermediate": "Intermediate Risk", 
            "high": "High Risk"
        }
        
        interpretation_mapping = {
            "low": f"CNS-IPI Score {score}: Very low risk of CNS relapse ({risk_data['relapse_rate']}% at 2 years, 95% CI: {risk_data['confidence_interval']}). CNS prophylaxis generally not recommended. Standard treatment with R-CHOP is appropriate. Represents {risk_data['patient_distribution']}% of DLBCL patients.",
            "intermediate": f"CNS-IPI Score {score}: Low to moderate risk of CNS relapse ({risk_data['relapse_rate']}% at 2 years, 95% CI: {risk_data['confidence_interval']}). CNS prophylaxis may be considered based on additional high-risk features and clinical judgment. Represents {risk_data['patient_distribution']}% of DLBCL patients.",
            "high": f"CNS-IPI Score {score}: High risk of CNS relapse ({risk_data['relapse_rate']}% at 2 years, 95% CI: {risk_data['confidence_interval']}). CNS prophylaxis strongly recommended. Consider intrathecal chemotherapy or high-dose methotrexate. Represents {risk_data['patient_distribution']}% of DLBCL patients."
        }
        
        return {
            "category": risk_level.title(),
            "stage": stage_mapping[risk_level],
            "description": risk_data["description"],
            "relapse_rate": risk_data["relapse_rate"],
            "confidence_interval": risk_data["confidence_interval"],
            "patient_distribution": risk_data["patient_distribution"],
            "recommendation": risk_data["recommendation"],
            "interpretation": interpretation_mapping[risk_level]
        }
    
    def _get_scoring_breakdown(self, age_over_60, elevated_ldh, ecog_ps, 
                              advanced_stage, multiple_extranodal, kidney_adrenal):
        """Provides detailed scoring breakdown"""
        
        breakdown = {
            "parameters": {
                "age_over_60": {
                    "present": age_over_60 == "yes",
                    "points": 1 if age_over_60 == "yes" else 0,
                    "description": "Age greater than 60 years"
                },
                "elevated_ldh": {
                    "present": elevated_ldh == "yes",
                    "points": 1 if elevated_ldh == "yes" else 0,
                    "description": "LDH above normal laboratory range"
                },
                "ecog_performance_status_over_1": {
                    "present": ecog_ps == "yes",
                    "points": 1 if ecog_ps == "yes" else 0,
                    "description": "ECOG Performance Status >1 (moderate to severe limitation)"
                },
                "advanced_stage": {
                    "present": advanced_stage == "yes",
                    "points": 1 if advanced_stage == "yes" else 0,
                    "description": "Ann Arbor stage III or IV disease"
                },
                "multiple_extranodal_sites": {
                    "present": multiple_extranodal == "yes",
                    "points": 1 if multiple_extranodal == "yes" else 0,
                    "description": "More than 1 extranodal disease site"
                },
                "kidney_adrenal_involvement": {
                    "present": kidney_adrenal == "yes",
                    "points": 1 if kidney_adrenal == "yes" else 0,
                    "description": "Involvement of kidney and/or adrenal gland"
                }
            },
            "additional_considerations": [
                "Additional high-risk features not captured by CNS-IPI:",
                "- Involvement of breast, uterus, testis, or epidural space",
                "- Bone marrow involvement",
                "- Double-hit or triple-hit lymphomas",
                "- MYC/BCL2 dual expression by immunohistochemistry",
                "- Consider these factors in clinical decision-making"
            ]
        }
        
        return breakdown


def calculate_cns_ipi(
    age_over_60: str,
    elevated_ldh: str,
    ecog_performance_status_over_1: str,
    advanced_stage: str,
    multiple_extranodal_sites: str,
    kidney_adrenal_involvement: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CnsIpiCalculator()
    return calculator.calculate(
        age_over_60=age_over_60,
        elevated_ldh=elevated_ldh,
        ecog_performance_status_over_1=ecog_performance_status_over_1,
        advanced_stage=advanced_stage,
        multiple_extranodal_sites=multiple_extranodal_sites,
        kidney_adrenal_involvement=kidney_adrenal_involvement
    )