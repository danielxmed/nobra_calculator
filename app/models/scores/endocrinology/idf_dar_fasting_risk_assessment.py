"""
International Diabetes Federation-Diabetes and Ramadan Alliance (IDF-DAR) Fasting Risk Assessment Models

Request and response models for IDF-DAR fasting risk assessment calculation.

References (Vancouver style):
1. Hassanein M, Sahay BK, Hafidh K, Djaballah K, Li H, Rahim MA, et al. Diabetes and Ramadan: 
   Practical guidelines 2021. Diabetes Res Clin Pract. 2022 Mar;185:109185. doi: 10.1016/j.diabres.2021.109185.
2. Ibrahim M, Al Magd MA, Annabi FA, Assaad-Khalil S, Ba-Essa EM, Fahdil I, et al. Recommendations 
   for management of diabetes during Ramadan: update 2020, applying evidence from a decade of research. 
   BMJ Open Diabetes Res Care. 2020 May;8(1):e001248. doi: 10.1136/bmjdrc-2020-001248.
3. Alam F, Oubari S, Ahmad J, Eba-Alkhayri A, Almadani A, Babineaux S, et al. Validity of the 
   International Diabetes Federation risk stratification score of Ramadan fasting in individuals 
   with diabetes mellitus. Saudi Med J. 2024 Jan;45(1):86-92. doi: 10.15537/smj.2024.45.1.20230497.

The International Diabetes Federation-Diabetes and Ramadan Alliance (IDF-DAR) Fasting Risk Assessment 
is a validated tool that stratifies risk of fasting during Ramadan in diabetic patients. The assessment 
evaluates 14 key risk factors across multiple domains including diabetes type, glycemic control, 
hypoglycemia history, treatment regimen, complications, and social factors. The tool provides 
evidence-based guidance for healthcare providers and patients to make informed decisions about the 
safety of fasting during Ramadan, with risk categories ranging from low risk (fasting probably safe) 
to high risk (fasting probably unsafe).
"""

from pydantic import BaseModel, Field
from typing import Literal


class IdfDarFastingRiskAssessmentRequest(BaseModel):
    """
    Request model for IDF-DAR Fasting Risk Assessment
    
    The IDF-DAR tool evaluates 14 key risk factors across multiple domains:
    
    Primary Risk Factors:
    - Diabetes type and duration
    - Hypoglycemia frequency and severity
    - Glycemic control (HbA1c level)
    - Current treatment regimen
    - Self-monitoring of blood glucose
    
    Complication Risk Factors:
    - Recent acute complications (DKA, HHS)
    - Macrovascular disease (CAD, CVD, PAD)
    - Diabetic nephropathy/CKD stage 4-5
    
    Social and Environmental Factors:
    - Pregnancy/breastfeeding status
    - Frailty or cognitive impairment
    - Physical labor intensity
    - Previous Ramadan fasting experience
    - Daily fasting duration (geographic location)
    
    Risk Categories:
    - Low Risk (0-3 points): Fasting probably safe
    - Moderate Risk (3.5-6 points): Fasting safety uncertain
    - High Risk (>6 points): Fasting probably unsafe
    
    References (Vancouver style):
    1. Hassanein M, Sahay BK, Hafidh K, Djaballah K, Li H, Rahim MA, et al. Diabetes and Ramadan: 
    Practical guidelines 2021. Diabetes Res Clin Pract. 2022 Mar;185:109185. doi: 10.1016/j.diabres.2021.109185.
    2. Ibrahim M, Al Magd MA, Annabi FA, Assaad-Khalil S, Ba-Essa EM, Fahdil I, et al. Recommendations 
    for management of diabetes during Ramadan: update 2020, applying evidence from a decade of research. 
    BMJ Open Diabetes Res Care. 2020 May;8(1):e001248. doi: 10.1136/bmjdrc-2020-001248.
    3. Alam F, Oubari S, Ahmad J, Eba-Alkhayri A, Almadani A, Babineaux S, et al. Validity of the 
    International Diabetes Federation risk stratification score of Ramadan fasting in individuals 
    with diabetes mellitus. Saudi Med J. 2024 Jan;45(1):86-92. doi: 10.15537/smj.2024.45.1.20230497.
    """
    
    diabetes_type: Literal["type_1", "type_2"] = Field(
        ...,
        description="Type of diabetes mellitus. Type 1 diabetes carries higher baseline fasting risk due to insulin dependence and greater glycemic variability. Type 2 diabetes generally has lower baseline risk",
        example="type_2"
    )
    
    years_since_diagnosis: Literal["less_than_10", "10_or_more"] = Field(
        ...,
        description="Duration of diabetes diagnosis. Longer duration (≥10 years) is associated with increased risk of complications and glucose variability during fasting",
        example="less_than_10"
    )
    
    hypoglycemia_frequency: Literal["none", "less_than_weekly", "multiple_weekly", "recent_severe", "unawareness"] = Field(
        ...,
        description="Frequency and severity of hypoglycemic episodes. Recent severe hypoglycemia or hypoglycemia unawareness significantly increases fasting risk due to impaired counter-regulatory responses",
        example="none"
    )
    
    hba1c_level: Literal["less_than_7_5", "7_5_to_9", "greater_than_9"] = Field(
        ...,
        description="Glycemic control measured by HbA1c percentage. Poor control (>9%) indicates higher risk of acute complications during fasting including DKA and severe hyperglycemia",
        example="less_than_7_5"
    )
    
    treatment_type: Literal["other_therapy", "short_acting_sulfonylurea", "long_acting_sulfonylurea", "basal_insulin", "mixed_insulin", "intensive_insulin"] = Field(
        ...,
        description="Current diabetes treatment regimen. Insulin therapy and certain sulfonylureas increase hypoglycemia risk during fasting. Other therapies include metformin, DPP-4 inhibitors, GLP-1 agonists, SGLT-2 inhibitors",
        example="other_therapy"
    )
    
    self_monitoring_frequency: Literal["regular", "irregular", "none"] = Field(
        ...,
        description="Blood glucose self-monitoring frequency. Regular monitoring enables safer fasting through early detection of glucose abnormalities and appropriate intervention",
        example="regular"
    )
    
    acute_complications: Literal["yes", "no"] = Field(
        ...,
        description="History of acute diabetic complications including diabetic ketoacidosis (DKA) or hyperosmolar hyperglycemic state (HHS) within the past 3 months",
        example="no"
    )
    
    macrovascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Presence of macrovascular complications including coronary artery disease, cerebrovascular disease (stroke/TIA), or peripheral arterial disease",
        example="no"
    )
    
    renal_complications: Literal["yes", "no"] = Field(
        ...,
        description="Diabetic nephropathy or chronic kidney disease stage 4-5 (eGFR <30 mL/min/1.73m²). Advanced kidney disease increases risk of electrolyte imbalances and medication toxicity during fasting",
        example="no"
    )
    
    pregnancy_status: Literal["pregnant_breastfeeding", "not_applicable"] = Field(
        ...,
        description="Pregnancy or breastfeeding status. Pregnant and breastfeeding women with diabetes are generally advised against fasting due to increased metabolic demands and risk to maternal and fetal health",
        example="not_applicable"
    )
    
    frailty_cognitive_function: Literal["impaired", "normal"] = Field(
        ...,
        description="Frailty or cognitive impairment that may impair ability to recognize or respond appropriately to hypoglycemia symptoms or other complications during fasting",
        example="normal"
    )
    
    physical_labor: Literal["intense", "moderate", "light"] = Field(
        ...,
        description="Occupation or daily activities involving physical labor. Intense physical activity increases metabolic demands and hypoglycemia risk during fasting periods",
        example="light"
    )
    
    previous_ramadan_experience: Literal["successful", "unsuccessful", "never_fasted"] = Field(
        ...,
        description="Experience with previous Ramadan fasting. Prior successful fasting may indicate better tolerance and risk management, while unsuccessful attempts or lack of experience increase risk",
        example="successful"
    )
    
    fasting_hours: Literal["less_than_15", "15_or_more"] = Field(
        ...,
        description="Duration of daily fasting hours based on geographic location and season. Longer fasting periods (≥15 hours) increase dehydration and hypoglycemia risk",
        example="less_than_15"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "diabetes_type": "type_2",
                "years_since_diagnosis": "less_than_10",
                "hypoglycemia_frequency": "none",
                "hba1c_level": "less_than_7_5",
                "treatment_type": "other_therapy",
                "self_monitoring_frequency": "regular",
                "acute_complications": "no",
                "macrovascular_disease": "no",
                "renal_complications": "no",
                "pregnancy_status": "not_applicable",
                "frailty_cognitive_function": "normal",
                "physical_labor": "light",
                "previous_ramadan_experience": "successful",
                "fasting_hours": "less_than_15"
            }
        }


class IdfDarFastingRiskAssessmentResponse(BaseModel):
    """
    Response model for IDF-DAR Fasting Risk Assessment
    
    The risk score ranges from 0 to >15 points and categorizes patients into:
    - Low Risk (0-3 points): Fasting probably safe with appropriate education and monitoring
    - Moderate Risk (3.5-6 points): Fasting safety uncertain, requires enhanced monitoring
    - High Risk (>6 points): Fasting probably unsafe, generally advised against
    
    Clinical Decision-Making:
    - Low Risk: Can fast with standard precautions and education
    - Moderate Risk: May fast with medical supervision and intensive monitoring
    - High Risk: Should avoid fasting due to significant complication risk
    
    Key Validation Studies:
    - UAE Study: 94.3%, 81.1%, and 76.9% of patients completed 30-day fast in low, moderate, and high-risk groups
    - Bahrain Study: 92.4%, 89.3%, and 74.7% successful completion rates respectively
    - Bangladesh Study: 3.74-fold and 3.86-fold higher hypoglycemia and hyperglycemia risks in high-risk group
    
    Reference: Hassanein M, et al. Diabetes Res Clin Pract. 2022;185:109185.
    """
    
    result: float = Field(
        ...,
        description="IDF-DAR fasting risk score calculated from clinical risk factors (range: 0-15+ points)",
        example=1.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the risk score and category",
        example="Low risk for complications during Ramadan fasting. Patient can likely fast safely with appropriate education and monitoring. Recommend pre-Ramadan counseling on meal timing, glucose monitoring, and recognition of hypoglycemia symptoms. Consider adjusting medication timing but major therapy changes usually not required. Monitor for breakthrough hypoglycemia and maintain regular follow-up."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Moderate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Fasting probably safe"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1.5,
                "unit": "points",
                "interpretation": "Low risk for complications during Ramadan fasting. Patient can likely fast safely with appropriate education and monitoring. Recommend pre-Ramadan counseling on meal timing, glucose monitoring, and recognition of hypoglycemia symptoms. Consider adjusting medication timing but major therapy changes usually not required. Monitor for breakthrough hypoglycemia and maintain regular follow-up.",
                "stage": "Low Risk",
                "stage_description": "Fasting probably safe"
            }
        }