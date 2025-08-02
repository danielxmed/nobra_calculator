"""
Hypoglycemia Risk Score Calculator

Predicts 12-month risk of hypoglycemic episodes in Type 2 Diabetes Mellitus (T2DM) patients 
for population management and targeted interventions.

References:
- Karter AJ, Warton EM, Lipska KJ, et al. Development and Validation of a Tool to Identify 
  Patients With Type 2 Diabetes at High Risk of Hypoglycemia-Related Emergency Department or 
  Hospital Use. JAMA Intern Med. 2017;177(10):1461-1470.
- Lipska KJ, Warton EM, Huang ES, et al. HbA1c and risk of severe hypoglycemia in type 2 
  diabetes: the Diabetes and Aging Study. Diabetes Care. 2013;36(11):3535-42.
"""

from typing import Dict, Any


class HypoglycemiaRiskScoreCalculator:
    """Calculator for Hypoglycemia Risk Score"""
    
    def __init__(self):
        # Risk stratification logic based on Karter et al. study
        pass
    
    def calculate(self, hypoglycemia_admissions: str, ed_visits_12_months: str, 
                 insulin_use: str, sulfonylurea_use: str, severe_kidney_disease: str, 
                 age_77_or_older: str) -> Dict[str, Any]:
        """
        Calculates hypoglycemia risk category for T2DM patients
        
        Args:
            hypoglycemia_admissions (str): Previous hypoglycemia admissions ("0", "1-2", "3_or_more")
            ed_visits_12_months (str): ED visits in last 12 months ("less_than_2", "2_or_more")
            insulin_use (str): Current insulin use ("yes", "no")
            sulfonylurea_use (str): Current sulfonylurea use ("yes", "no")
            severe_kidney_disease (str): eGFR ≤29 ("yes", "no")
            age_77_or_older (str): Age ≥77 years ("yes", "no")
            
        Returns:
            Dict with risk category and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(hypoglycemia_admissions, ed_visits_12_months, insulin_use, 
                            sulfonylurea_use, severe_kidney_disease, age_77_or_older)
        
        # Determine risk category using validated criteria
        risk_category = self._calculate_risk_category(
            hypoglycemia_admissions, ed_visits_12_months, insulin_use, 
            sulfonylurea_use, severe_kidney_disease, age_77_or_older
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_category)
        
        return {
            "result": risk_category,
            "unit": "category",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "risk_percentage": interpretation["risk_percentage"],
            "clinical_recommendations": interpretation["recommendations"],
            "population_management": True
        }
    
    def _validate_inputs(self, hypoglycemia_admissions: str, ed_visits_12_months: str,
                        insulin_use: str, sulfonylurea_use: str, severe_kidney_disease: str,
                        age_77_or_older: str):
        """Validates input parameters"""
        
        valid_admissions = ["0", "1-2", "3_or_more"]
        if hypoglycemia_admissions not in valid_admissions:
            raise ValueError(f"Hypoglycemia admissions must be one of: {valid_admissions}")
        
        valid_ed_visits = ["less_than_2", "2_or_more"]
        if ed_visits_12_months not in valid_ed_visits:
            raise ValueError(f"ED visits must be one of: {valid_ed_visits}")
        
        valid_yes_no = ["yes", "no"]
        for param, name in [
            (insulin_use, "insulin_use"),
            (sulfonylurea_use, "sulfonylurea_use"), 
            (severe_kidney_disease, "severe_kidney_disease"),
            (age_77_or_older, "age_77_or_older")
        ]:
            if param not in valid_yes_no:
                raise ValueError(f"{name} must be one of: {valid_yes_no}")
    
    def _calculate_risk_category(self, hypoglycemia_admissions: str, ed_visits_12_months: str,
                               insulin_use: str, sulfonylurea_use: str, severe_kidney_disease: str,
                               age_77_or_older: str) -> str:
        """
        Calculates risk category based on validated criteria from Karter et al.
        
        Args:
            All input parameters
            
        Returns:
            str: Risk category ("High Risk", "Low Risk", or "Intermediate Risk")
        """
        
        # High Risk Criteria (>5% risk)
        # 1. ≥3 previous hypoglycemia admissions
        if hypoglycemia_admissions == "3_or_more":
            return "High Risk"
        
        # 2. 1-2 previous admissions + insulin use
        if hypoglycemia_admissions == "1-2" and insulin_use == "yes":
            return "High Risk"
        
        # Low Risk Criteria (<1% risk)
        # No previous admissions + no high-risk medications + age <77 + no severe kidney disease
        if (hypoglycemia_admissions == "0" and 
            insulin_use == "no" and 
            sulfonylurea_use == "no" and 
            age_77_or_older == "no" and 
            severe_kidney_disease == "no"):
            return "Low Risk"
        
        # All other combinations are Intermediate Risk (1-5% risk)
        return "Intermediate Risk"
    
    def _get_interpretation(self, risk_category: str) -> Dict[str, Any]:
        """
        Determines the interpretation based on risk category
        
        Args:
            risk_category (str): Risk category
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_category == "High Risk":
            return {
                "stage": "High Risk",
                "description": ">5% hypoglycemia admission risk",
                "risk_percentage": ">5%",
                "interpretation": "High risk of hypoglycemia-related hospitalization within 12 months. Priority for targeted interventions including medication review, continuous glucose monitoring, and specialized care coordination. Consider endocrinology referral and comprehensive diabetes management review.",
                "recommendations": [
                    "Immediate clinical review of hypoglycemia risk factors",
                    "Consider medication regimen simplification",
                    "Evaluate for continuous glucose monitoring (CGM)",
                    "Endocrinology/diabetes specialist referral",
                    "Patient education on hypoglycemia recognition and treatment",
                    "Review psychosocial and socioeconomic factors",
                    "Consider clinical pharmacy consultation"
                ]
            }
        
        elif risk_category == "Low Risk":
            return {
                "stage": "Low Risk", 
                "description": "<1% hypoglycemia admission risk",
                "risk_percentage": "<1%",
                "interpretation": "Low risk of hypoglycemia-related hospitalization within 12 months. Standard diabetes care with routine monitoring is appropriate. No specific hypoglycemia interventions required at this time.",
                "recommendations": [
                    "Continue standard diabetes care",
                    "Routine diabetes monitoring and follow-up",
                    "Patient education on general diabetes management", 
                    "Monitor for changes in clinical status",
                    "Standard hypoglycemia awareness education"
                ]
            }
        
        else:  # Intermediate Risk
            return {
                "stage": "Intermediate Risk",
                "description": "1-5% hypoglycemia admission risk", 
                "risk_percentage": "1-5%",
                "interpretation": "Moderate risk of hypoglycemia-related hospitalization within 12 months. Consider targeted interventions based on individual risk factors. Clinical review recommended to identify modifiable risk factors.",
                "recommendations": [
                    "Clinical review of diabetes management",
                    "Assess need for medication adjustment",
                    "Consider simplified medication regimens if appropriate",
                    "Enhanced patient education on hypoglycemia prevention",
                    "Monitor kidney function if applicable",
                    "Consider diabetes self-management education",
                    "Regular follow-up with primary care or diabetes specialist"
                ]
            }


def calculate_hypoglycemia_risk_score(hypoglycemia_admissions: str, ed_visits_12_months: str,
                                    insulin_use: str, sulfonylurea_use: str,
                                    severe_kidney_disease: str, age_77_or_older: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HypoglycemiaRiskScoreCalculator()
    return calculator.calculate(hypoglycemia_admissions, ed_visits_12_months, 
                              insulin_use, sulfonylurea_use, severe_kidney_disease, 
                              age_77_or_older)