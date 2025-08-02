"""
Hypoglycemia Risk Score Models

Request and response models for Hypoglycemia Risk Score calculation.

References (Vancouver style):
1. Karter AJ, Warton EM, Lipska KJ, Moffet HH, Adler N, Schillinger D, et al. 
   Development and Validation of a Tool to Identify Patients With Type 2 Diabetes at High Risk 
   of Hypoglycemia-Related Emergency Department or Hospital Use. JAMA Intern Med. 
   2017 Oct 1;177(10):1461-1470. doi: 10.1001/jamainternmed.2017.3844.
2. Lipska KJ, Warton EM, Huang ES, Moffet HH, Inzucchi SE, Krumholz HM, et al. 
   HbA1c and risk of severe hypoglycemia in type 2 diabetes: the Diabetes and Aging Study. 
   Diabetes Care. 2013 Nov;36(11):3535-42. doi: 10.2337/dc13-0610.
3. Geller AI, Shehab N, Lovegrove MC, Kegler SR, Weidenbach KN, Ryan GJ, et al. 
   National estimates of insulin-related hypoglycemia and errors leading to emergency 
   department visits and hospitalizations. JAMA Intern Med. 2014 May;174(5):678-86. 
   doi: 10.1001/jamainternmed.2014.136.

The Hypoglycemia Risk Score predicts 12-month risk of hypoglycemic episodes requiring 
emergency department visits or hospitalizations in Type 2 Diabetes Mellitus (T2DM) patients. 
This tool was developed for population management to identify high-risk patients who would 
benefit from targeted interventions such as medication simplification, continuous glucose 
monitoring, and specialized diabetes care coordination.
"""

from pydantic import BaseModel, Field
from typing import Literal, List


class HypoglycemiaRiskScoreRequest(BaseModel):
    """
    Request model for Hypoglycemia Risk Score
    
    The Hypoglycemia Risk Score uses six key clinical parameters to stratify T2DM patients 
    into risk categories for hypoglycemia-related emergency care:
    
    1. Previous Hypoglycemia Admissions: The strongest predictor of future hypoglycemia risk
       - 0: No previous hypoglycemia-related hospitalizations
       - 1-2: One to two previous hypoglycemia-related hospitalizations
       - 3+: Three or more previous hypoglycemia-related hospitalizations (highest risk)
    
    2. Emergency Department Visits: General healthcare utilization in past 12 months
       - <2 visits: Lower healthcare utilization pattern
       - ≥2 visits: Higher healthcare utilization pattern
    
    3. Insulin Use: Current insulin therapy (any type)
       - Insulin users have significantly higher hypoglycemia risk
       - Includes basal, bolus, premixed, and continuous subcutaneous insulin infusion
    
    4. Sulfonylurea Use: Current sulfonylurea therapy
       - Second-generation sulfonylureas (glyburide, glipizide, glimepiride)
       - Higher hypoglycemia risk compared to other oral antidiabetic agents
    
    5. Severe Kidney Disease: Advanced chronic kidney disease
       - eGFR ≤29 mL/min/1.73 m² (CKD stages 4-5)
       - Impaired drug clearance increases hypoglycemia risk
    
    6. Advanced Age: Age-related physiologic changes
       - ≥77 years: Increased vulnerability to hypoglycemia
       - Associated with cognitive impairment, polypharmacy, and frailty
    
    Risk Stratification:
    - High Risk (>5%): ≥3 previous admissions OR 1-2 admissions with insulin use
    - Low Risk (<1%): No previous admissions, no insulin/sulfonylurea, age <77, no severe CKD
    - Intermediate Risk (1-5%): All other combinations
    
    Clinical Application:
    This tool is designed for population management rather than individual patient risk assessment. 
    It helps healthcare systems identify patients who would benefit from:
    - Medication regimen simplification
    - Continuous glucose monitoring
    - Enhanced patient education
    - Specialist referrals (endocrinology, clinical pharmacy)
    - Psychosocial support services
    
    References (Vancouver style):
    1. Karter AJ, Warton EM, Lipska KJ, Moffet HH, Adler N, Schillinger D, et al. 
       Development and Validation of a Tool to Identify Patients With Type 2 Diabetes at High Risk 
       of Hypoglycemia-Related Emergency Department or Hospital Use. JAMA Intern Med. 
       2017 Oct 1;177(10):1461-1470. doi: 10.1001/jamainternmed.2017.3844.
    2. Lipska KJ, Warton EM, Huang ES, Moffet HH, Inzucchi SE, Krumholz HM, et al. 
       HbA1c and risk of severe hypoglycemia in type 2 diabetes: the Diabetes and Aging Study. 
       Diabetes Care. 2013 Nov;36(11):3535-42. doi: 10.2337/dc13-0610.
    """
    
    hypoglycemia_admissions: Literal["0", "1-2", "3_or_more"] = Field(
        ...,
        description="Number of previous hypoglycemia-related hospital admissions. "
                   "0: No previous admissions. "
                   "1-2: One to two previous admissions (moderate risk factor). "
                   "3_or_more: Three or more previous admissions (strongest risk predictor).",
        example="0"
    )
    
    ed_visits_12_months: Literal["less_than_2", "2_or_more"] = Field(
        ...,
        description="Number of emergency department visits in the last 12 months (any cause). "
                   "less_than_2: Fewer than 2 ED visits (lower healthcare utilization). "
                   "2_or_more: Two or more ED visits (higher healthcare utilization pattern).",
        example="less_than_2"
    )
    
    insulin_use: Literal["yes", "no"] = Field(
        ...,
        description="Current insulin therapy of any type (basal, bolus, premixed, or CSII). "
                   "yes: Currently using insulin therapy (significant hypoglycemia risk factor). "
                   "no: No current insulin use.",
        example="no"
    )
    
    sulfonylurea_use: Literal["yes", "no"] = Field(
        ...,
        description="Current sulfonylurea therapy (glyburide, glipizide, glimepiride, etc.). "
                   "yes: Currently using sulfonylurea medications (moderate hypoglycemia risk). "
                   "no: No current sulfonylurea use.",
        example="no"
    )
    
    severe_kidney_disease: Literal["yes", "no"] = Field(
        ...,
        description="Severe kidney disease defined as eGFR ≤29 mL/min/1.73 m² (CKD stages 4-5). "
                   "yes: eGFR ≤29 (impaired drug clearance increases hypoglycemia risk). "
                   "no: eGFR >29 mL/min/1.73 m² or no known kidney disease.",
        example="no"
    )
    
    age_77_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age 77 years or older (age-related increased hypoglycemia vulnerability). "
                   "yes: Age ≥77 years (increased risk due to physiologic changes). "
                   "no: Age <77 years.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hypoglycemia_admissions": "0",
                "ed_visits_12_months": "less_than_2",
                "insulin_use": "no",
                "sulfonylurea_use": "no", 
                "severe_kidney_disease": "no",
                "age_77_or_older": "no"
            }
        }


class HypoglycemiaRiskScoreResponse(BaseModel):
    """
    Response model for Hypoglycemia Risk Score
    
    The Hypoglycemia Risk Score stratifies T2DM patients into three risk categories 
    for hypoglycemia-related emergency department visits or hospitalizations within 12 months:
    
    Risk Categories:
    - Low Risk (<1%): Patients with no previous admissions, no high-risk medications, 
      age <77 years, and no severe kidney disease
    - Intermediate Risk (1-5%): Patients with some risk factors but not meeting 
      high-risk criteria
    - High Risk (>5%): Patients with ≥3 previous hypoglycemia admissions OR 
      1-2 previous admissions with current insulin use
    
    Clinical Implementation:
    This tool is intended for population management to identify patients who would 
    benefit from targeted interventions:
    - Medication regimen review and simplification
    - Continuous glucose monitoring consideration
    - Enhanced diabetes education and self-management support
    - Specialist referrals (endocrinology, clinical pharmacy, social work)
    - Psychosocial and socioeconomic factor assessment
    
    Validation:
    The score has been validated in multiple external cohorts and shows good 
    discrimination for identifying high-risk patients, but prospective 
    implementation studies are still needed.
    
    Reference: Karter AJ, et al. JAMA Intern Med. 2017;177(10):1461-1470.
    """
    
    result: str = Field(
        ...,
        description="Risk category for 12-month hypoglycemia-related emergency care",
        example="Low Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on risk category",
        example="Low risk of hypoglycemia-related hospitalization within 12 months. Standard diabetes care with routine monitoring is appropriate."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk percentage range for the category",
        example="<1% hypoglycemia admission risk"
    )
    
    risk_percentage: str = Field(
        ...,
        description="Estimated 12-month risk percentage range for hypoglycemia-related emergency care",
        example="<1%"
    )
    
    clinical_recommendations: List[str] = Field(
        ...,
        description="List of specific clinical recommendations based on risk category",
        example=[
            "Continue standard diabetes care",
            "Routine diabetes monitoring and follow-up",
            "Patient education on general diabetes management"
        ]
    )
    
    population_management: bool = Field(
        ...,
        description="Boolean indicating this tool is designed for population management (always true)",
        example=True
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Low Risk",
                "unit": "category",
                "interpretation": "Low risk of hypoglycemia-related hospitalization within 12 months. Standard diabetes care with routine monitoring is appropriate. No specific hypoglycemia interventions required at this time.",
                "stage": "Low Risk",
                "stage_description": "<1% hypoglycemia admission risk",
                "risk_percentage": "<1%",
                "clinical_recommendations": [
                    "Continue standard diabetes care",
                    "Routine diabetes monitoring and follow-up",
                    "Patient education on general diabetes management",
                    "Monitor for changes in clinical status",
                    "Standard hypoglycemia awareness education"
                ],
                "population_management": True
            }
        }