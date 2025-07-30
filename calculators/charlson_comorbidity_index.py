"""
Charlson Comorbidity Index (CCI) Calculator

Predicts 10-year survival in patients with multiple comorbidities using weighted comorbidity 
categories plus age adjustment to estimate mortality risk.

References:
1. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic 
   comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-83.
2. Charlson M, Szatrowski TP, Peterson J, Gold J. Validation of a combined comorbidity index. 
   J Clin Epidemiol. 1994;47(11):1245-51.
3. Deyo RA, Cherkin DC, Ciol MA. Adapting a clinical comorbidity index for use with ICD-9-CM 
   administrative databases. J Clin Epidemiol. 1992;45(6):613-9.
"""

import math
from typing import Dict, Any


class CharlsonComorbidityIndexCalculator:
    """Calculator for Charlson Comorbidity Index (CCI)"""
    
    def __init__(self):
        # Comorbidity point values
        self.comorbidity_points = {
            # 1 point conditions
            "myocardial_infarction": 1,
            "congestive_heart_failure": 1,
            "peripheral_vascular_disease": 1,
            "cerebrovascular_disease": 1,
            "dementia": 1,
            "chronic_pulmonary_disease": 1,
            "connective_tissue_disease": 1,
            "peptic_ulcer_disease": 1,
            # liver_disease handled separately (1 or 3 points)
            # diabetes handled separately (1 or 2 points)
            
            # 2 point conditions
            "hemiplegia": 2,
            "moderate_severe_ckd": 2,
            "localized_solid_tumor": 2,
            "leukemia": 2,
            "lymphoma": 2,
            
            # 6 point conditions
            "metastatic_solid_tumor": 6,
            "aids": 6
        }
        
        # Age adjustment points
        self.age_points = {
            range(0, 50): 0,
            range(50, 60): 1,
            range(60, 70): 2,
            range(70, 80): 3,
            range(80, 121): 4  # Maximum 4 points for age ≥80
        }
        
        # Liver disease points
        self.liver_disease_points = {
            "none": 0,
            "mild": 1,
            "moderate_severe": 3
        }
        
        # Diabetes points
        self.diabetes_points = {
            "none": 0,
            "uncomplicated": 1,
            "with_end_organ_damage": 2
        }
    
    def calculate(
        self,
        age: int,
        myocardial_infarction: str,
        congestive_heart_failure: str,
        peripheral_vascular_disease: str,
        cerebrovascular_disease: str,
        dementia: str,
        chronic_pulmonary_disease: str,
        connective_tissue_disease: str,
        peptic_ulcer_disease: str,
        liver_disease: str,
        diabetes: str,
        hemiplegia: str,
        moderate_severe_ckd: str,
        localized_solid_tumor: str,
        leukemia: str,
        lymphoma: str,
        metastatic_solid_tumor: str,
        aids: str
    ) -> Dict[str, Any]:
        """
        Calculates Charlson Comorbidity Index for 10-year survival prediction
        
        Args:
            age: Patient age in years
            myocardial_infarction: History of MI (yes/no)
            congestive_heart_failure: CHF present (yes/no)
            peripheral_vascular_disease: PVD present (yes/no)
            cerebrovascular_disease: CVA/TIA present (yes/no)
            dementia: Dementia present (yes/no)
            chronic_pulmonary_disease: COPD present (yes/no)
            connective_tissue_disease: CTD present (yes/no)
            peptic_ulcer_disease: PUD present (yes/no)
            liver_disease: Liver disease severity (none/mild/moderate_severe)
            diabetes: Diabetes severity (none/uncomplicated/with_end_organ_damage)
            hemiplegia: Hemiplegia present (yes/no)
            moderate_severe_ckd: Moderate-severe CKD present (yes/no)
            localized_solid_tumor: Localized solid tumor present (yes/no)
            leukemia: Leukemia present (yes/no)
            lymphoma: Lymphoma present (yes/no)
            metastatic_solid_tumor: Metastatic solid tumor present (yes/no)
            aids: AIDS present (yes/no)
            
        Returns:
            Dict with CCI score, 10-year survival probability, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age, myocardial_infarction, congestive_heart_failure, peripheral_vascular_disease,
            cerebrovascular_disease, dementia, chronic_pulmonary_disease, connective_tissue_disease,
            peptic_ulcer_disease, liver_disease, diabetes, hemiplegia, moderate_severe_ckd,
            localized_solid_tumor, leukemia, lymphoma, metastatic_solid_tumor, aids
        )
        
        # Calculate age adjustment points
        age_points = self._get_age_points(age)
        
        # Calculate comorbidity points
        comorbidity_points = self._calculate_comorbidity_points(
            myocardial_infarction, congestive_heart_failure, peripheral_vascular_disease,
            cerebrovascular_disease, dementia, chronic_pulmonary_disease, connective_tissue_disease,
            peptic_ulcer_disease, liver_disease, diabetes, hemiplegia, moderate_severe_ckd,
            localized_solid_tumor, leukemia, lymphoma, metastatic_solid_tumor, aids
        )
        
        # Calculate total CCI score
        total_score = age_points + comorbidity_points
        
        # Calculate 10-year survival probability
        survival_probability = self._calculate_10_year_survival(total_score)
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(total_score, survival_probability)
        
        # Get detailed breakdown
        breakdown = self._get_score_breakdown(
            age, age_points, myocardial_infarction, congestive_heart_failure, peripheral_vascular_disease,
            cerebrovascular_disease, dementia, chronic_pulmonary_disease, connective_tissue_disease,
            peptic_ulcer_disease, liver_disease, diabetes, hemiplegia, moderate_severe_ckd,
            localized_solid_tumor, leukemia, lymphoma, metastatic_solid_tumor, aids, comorbidity_points=comorbidity_points
        )
        
        return {
            "result": {
                "total_score": total_score,
                "age_points": age_points,
                "comorbidity_points": comorbidity_points,
                "ten_year_survival_probability": round(survival_probability, 2),
                "ten_year_survival_percentage": f"{round(survival_probability, 2)}%",
                "risk_category": risk_assessment["category"],
                "risk_description": risk_assessment["description"],
                "clinical_interpretation": risk_assessment["interpretation"],
                "score_breakdown": breakdown
            },
            "unit": "points",
            "interpretation": risk_assessment["detailed_interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["stage_description"]
        }
    
    def _validate_inputs(self, age, *comorbidity_params):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120")
        
        # Parameter names for validation
        param_names = [
            "myocardial_infarction", "congestive_heart_failure", "peripheral_vascular_disease",
            "cerebrovascular_disease", "dementia", "chronic_pulmonary_disease", "connective_tissue_disease",
            "peptic_ulcer_disease", "liver_disease", "diabetes", "hemiplegia", "moderate_severe_ckd",
            "localized_solid_tumor", "leukemia", "lymphoma", "metastatic_solid_tumor", "aids"
        ]
        
        # Validate yes/no parameters
        yes_no_params = param_names[:-2]  # All except liver_disease and diabetes
        yes_no_params = param_names[:8] + param_names[10:]  # Remove liver_disease and diabetes indices
        
        for i, param_value in enumerate(comorbidity_params):
            param_name = param_names[i]
            
            if param_name == "liver_disease":
                if param_value not in ["none", "mild", "moderate_severe"]:
                    raise ValueError("liver_disease must be 'none', 'mild', or 'moderate_severe'")
            elif param_name == "diabetes":
                if param_value not in ["none", "uncomplicated", "with_end_organ_damage"]:
                    raise ValueError("diabetes must be 'none', 'uncomplicated', or 'with_end_organ_damage'")
            else:
                if param_value not in ["yes", "no"]:
                    raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _get_age_points(self, age: int) -> int:
        """Calculates age adjustment points"""
        
        for age_range, points in self.age_points.items():
            if age in age_range:
                return points
        
        # Fallback (should not occur with valid ages)
        return 4 if age >= 80 else 0
    
    def _calculate_comorbidity_points(self, *comorbidity_params) -> int:
        """Calculates total comorbidity points"""
        
        total_points = 0
        param_names = [
            "myocardial_infarction", "congestive_heart_failure", "peripheral_vascular_disease",
            "cerebrovascular_disease", "dementia", "chronic_pulmonary_disease", "connective_tissue_disease",
            "peptic_ulcer_disease", "liver_disease", "diabetes", "hemiplegia", "moderate_severe_ckd",
            "localized_solid_tumor", "leukemia", "lymphoma", "metastatic_solid_tumor", "aids"
        ]
        
        for i, param_value in enumerate(comorbidity_params):
            param_name = param_names[i]
            
            if param_name == "liver_disease":
                total_points += self.liver_disease_points[param_value]
            elif param_name == "diabetes":
                total_points += self.diabetes_points[param_value]
            elif param_value == "yes" and param_name in self.comorbidity_points:
                total_points += self.comorbidity_points[param_name]
        
        return total_points
    
    def _calculate_10_year_survival(self, cci_score: int) -> float:
        """Calculates 10-year survival probability using CCI formula"""
        
        # Formula: 10-year survival = 0.983^(CCI × 0.9)
        # This assumes a theoretical low-risk population with 98.3% 10-year survival
        survival_probability = (0.983 ** (cci_score * 0.9)) * 100
        
        return max(0.0, min(100.0, survival_probability))  # Bound between 0-100%
    
    def _get_risk_assessment(self, score: int, survival_probability: float) -> Dict[str, str]:
        """Determines risk category and clinical interpretation based on survival probability"""
        
        # Prioritize survival probability for more clinically relevant assessment
        if survival_probability >= 90:
            category = "Low Risk"
            stage = "Minimal Comorbidity"
            description = "Minimal comorbidity burden with excellent prognosis"
            interpretation = "Excellent 10-year survival (≥90%). Minimal impact from comorbidities."
        elif survival_probability >= 70:
            category = "Moderate Risk"
            stage = "Moderate Comorbidity"
            description = "Moderate comorbidity burden with good prognosis"
            interpretation = "Good 10-year survival (70-89%). Moderate impact from comorbidities."
        elif survival_probability >= 30:
            category = "High Risk"
            stage = "Significant Comorbidity"
            description = "Significant comorbidity burden with reduced survival"
            interpretation = "Reduced 10-year survival (30-69%). Significant impact from comorbidities."
        else:  # survival_probability < 30
            category = "Very High Risk"
            stage = "Severe Comorbidity"
            description = "Severe comorbidity burden with poor prognosis"
            interpretation = "Poor 10-year survival (<30%). Severe impact from comorbidities."
        
        detailed_interpretation = (
            f"Charlson Comorbidity Index Score: {score} points. "
            f"Predicted 10-year survival: {survival_probability:.1f}%. "
            f"{interpretation} Consider individual patient factors and treatment goals "
            f"when making clinical decisions based on this assessment."
        )
        
        return {
            "category": category,
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "detailed_interpretation": detailed_interpretation,
            "stage_description": description
        }
    
    def _get_score_breakdown(self, age, age_points, *comorbidity_params, comorbidity_points):
        """Creates detailed breakdown of scoring"""
        
        param_names = [
            "myocardial_infarction", "congestive_heart_failure", "peripheral_vascular_disease",
            "cerebrovascular_disease", "dementia", "chronic_pulmonary_disease", "connective_tissue_disease",
            "peptic_ulcer_disease", "liver_disease", "diabetes", "hemiplegia", "moderate_severe_ckd",
            "localized_solid_tumor", "leukemia", "lymphoma", "metastatic_solid_tumor", "aids"
        ]
        
        condition_descriptions = {
            "myocardial_infarction": "Myocardial infarction (1 point)",
            "congestive_heart_failure": "Congestive heart failure (1 point)",
            "peripheral_vascular_disease": "Peripheral vascular disease (1 point)",
            "cerebrovascular_disease": "Cerebrovascular disease/TIA (1 point)",
            "dementia": "Dementia (1 point)",
            "chronic_pulmonary_disease": "Chronic pulmonary disease (1 point)",
            "connective_tissue_disease": "Connective tissue disease (1 point)",
            "peptic_ulcer_disease": "Peptic ulcer disease (1 point)",
            "liver_disease": "Liver disease (1-3 points based on severity)",
            "diabetes": "Diabetes mellitus (1-2 points based on severity)",
            "hemiplegia": "Hemiplegia (2 points)",
            "moderate_severe_ckd": "Moderate to severe CKD (2 points)",
            "localized_solid_tumor": "Localized solid tumor (2 points)",
            "leukemia": "Leukemia (2 points)",
            "lymphoma": "Lymphoma (2 points)",
            "metastatic_solid_tumor": "Metastatic solid tumor (6 points)",
            "aids": "AIDS (6 points)"
        }
        
        # Age breakdown
        age_category = "≥80 years" if age >= 80 else f"{age} years"
        if age < 50:
            age_description = f"Age {age_category} (0 points)"
        elif age < 60:
            age_description = f"Age {age_category} (1 point)"
        elif age < 70:
            age_description = f"Age {age_category} (2 points)"
        elif age < 80:
            age_description = f"Age {age_category} (3 points)"
        else:
            age_description = f"Age {age_category} (4 points)"
        
        # Comorbidity breakdown
        comorbidity_breakdown = {}
        
        for i, param_value in enumerate(comorbidity_params[:-1]):  # Exclude comorbidity_points parameter
            param_name = param_names[i]
            
            if param_name == "liver_disease":
                points_awarded = self.liver_disease_points[param_value]
                comorbidity_breakdown[param_name] = {
                    "present": param_value != "none",
                    "severity": param_value,
                    "points": points_awarded,
                    "description": condition_descriptions[param_name]
                }
            elif param_name == "diabetes":
                points_awarded = self.diabetes_points[param_value]
                comorbidity_breakdown[param_name] = {
                    "present": param_value != "none",
                    "severity": param_value,
                    "points": points_awarded,
                    "description": condition_descriptions[param_name]
                }
            else:
                points_awarded = self.comorbidity_points.get(param_name, 0) if param_value == "yes" else 0
                comorbidity_breakdown[param_name] = {
                    "present": param_value == "yes",
                    "points": points_awarded,
                    "description": condition_descriptions[param_name]
                }
        
        return {
            "age_assessment": {
                "age": age,
                "points": age_points,
                "description": age_description
            },
            "comorbidity_assessment": comorbidity_breakdown,
            "scoring_summary": {
                "total_comorbidity_points": comorbidity_points,
                "age_adjustment_points": age_points,
                "maximum_possible_score": 37,
                "formula": "10-year survival = 0.983^(CCI × 0.9)"
            }
        }


def calculate_charlson_comorbidity_index(
    age: int,
    myocardial_infarction: str,
    congestive_heart_failure: str,
    peripheral_vascular_disease: str,
    cerebrovascular_disease: str,
    dementia: str,
    chronic_pulmonary_disease: str,
    connective_tissue_disease: str,
    peptic_ulcer_disease: str,
    liver_disease: str,
    diabetes: str,
    hemiplegia: str,
    moderate_severe_ckd: str,
    localized_solid_tumor: str,
    leukemia: str,
    lymphoma: str,
    metastatic_solid_tumor: str,
    aids: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CharlsonComorbidityIndexCalculator()
    return calculator.calculate(
        age=age,
        myocardial_infarction=myocardial_infarction,
        congestive_heart_failure=congestive_heart_failure,
        peripheral_vascular_disease=peripheral_vascular_disease,
        cerebrovascular_disease=cerebrovascular_disease,
        dementia=dementia,
        chronic_pulmonary_disease=chronic_pulmonary_disease,
        connective_tissue_disease=connective_tissue_disease,
        peptic_ulcer_disease=peptic_ulcer_disease,
        liver_disease=liver_disease,
        diabetes=diabetes,
        hemiplegia=hemiplegia,
        moderate_severe_ckd=moderate_severe_ckd,
        localized_solid_tumor=localized_solid_tumor,
        leukemia=leukemia,
        lymphoma=lymphoma,
        metastatic_solid_tumor=metastatic_solid_tumor,
        aids=aids
    )