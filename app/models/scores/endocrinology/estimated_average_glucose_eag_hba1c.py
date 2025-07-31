"""
Estimated Average Glucose (eAG) From HbA1C Models

Request and response models for eAG calculation from HbA1c.

References (Vancouver style):
1. Nathan DM, Kuenen J, Borg R, Zheng H, Schoenfeld D, Heine RJ. Translating 
   the A1C assay into estimated average glucose values. Diabetes Care. 
   2008;31(8):1473-8. doi: 10.2337/dc08-0545.
2. American Diabetes Association. 6. Glycemic Targets: Standards of Medical Care 
   in Diabetes-2021. Diabetes Care. 2021;44(Suppl 1):S73-S84. doi: 10.2337/dc21-S006.
3. International Expert Committee. International Expert Committee report on the 
   role of the A1C assay in the diagnosis of diabetes. Diabetes Care. 2009;32(7):1327-34. 
   doi: 10.2337/dc09-9033.
4. Rohlfing CL, Wiedmeyer HM, Little RR, England JD, Tennill A, Goldstein DE. 
   Defining the relationship between plasma glucose and HbA(1c): analysis of glucose 
   profiles and HbA(1c) in the Diabetes Control and Complications Trial. Diabetes Care. 
   2002;25(2):275-8. doi: 10.2337/diacare.25.2.275.

The Estimated Average Glucose (eAG) calculation provides a way to translate HbA1c 
values into estimated average glucose levels that correspond to everyday glucose 
meter readings. This relationship was established by the A1c-Derived Average 
Glucose (ADAG) Study Group using the formula: eAG (mg/dL) = (28.7 × HbA1c %) - 46.7.

The eAG represents an average of glucose levels 24 hours a day over 2-3 months, 
reflecting the average lifespan of red blood cells. This tool helps patients and 
healthcare providers better understand HbA1c results in the context of daily 
glucose monitoring values.

Clinical applications include diabetes diagnosis, monitoring glycemic control, 
setting treatment targets, patient education, and assessing diabetes management 
effectiveness over time.
"""

from pydantic import BaseModel, Field
from typing import Union


class EstimatedAverageGlucoseEagHba1cRequest(BaseModel):
    """
    Request model for Estimated Average Glucose (eAG) From HbA1C
    
    The estimated average glucose (eAG) calculation converts HbA1c percentage 
    values into estimated average glucose levels using the linear relationship 
    established by the A1c-Derived Average Glucose (ADAG) Study Group.
    
    Formula: eAG (mg/dL) = (28.7 × HbA1c %) - 46.7
    
    This relationship has a correlation coefficient (r²) of 0.84 and was derived 
    from a comprehensive study involving continuous glucose monitoring data.
    
    Clinical Context and Applications:
    
    HbA1c Measurement:
    - Reflects average blood glucose levels over 2-3 months
    - Based on glycation of hemoglobin in red blood cells
    - More recent glucose levels have greater influence on the result
    - Not affected by short-term glucose fluctuations
    
    Diagnostic Criteria (American Diabetes Association):
    - Normal: HbA1c <5.7% (eAG <117 mg/dL)
    - Prediabetes: HbA1c 5.7-6.4% (eAG 117-137 mg/dL)
    - Diabetes: HbA1c ≥6.5% (eAG ≥140 mg/dL)
    
    Treatment Targets:
    - Most adults with diabetes: HbA1c <7% (eAG <154 mg/dL)
    - More stringent: HbA1c <6.5% (eAG <140 mg/dL) if achievable without hypoglycemia
    - Less stringent: HbA1c <8% (eAG <183 mg/dL) for patients with comorbidities
    
    Important Considerations:
    
    eAG vs Meter Averages:
    The eAG is NOT the same as the average of glucose meter readings because:
    - eAG reflects 24-hour glucose patterns including periods not typically monitored
    - Patients often check glucose more frequently when levels are low
    - Post-meal glucose peaks are typically not captured in routine monitoring
    - eAG includes overnight glucose patterns
    
    Factors Affecting Accuracy:
    - Conditions altering red blood cell lifespan (anemia, hemolysis, bleeding)
    - Hemoglobin variants (HbS, HbC, HbE)
    - Recent blood transfusions
    - Iron deficiency
    - Chronic kidney disease
    - Certain medications
    
    Patient Education Benefits:
    - Helps patients understand HbA1c results in familiar glucose units
    - Connects long-term control (HbA1c) with daily monitoring values
    - Facilitates diabetes self-management discussions
    - Provides context for treatment goals and adjustments
    
    Clinical Decision Making:
    - Assists in diabetes diagnosis and staging
    - Guides treatment intensification decisions
    - Helps set individualized glycemic targets
    - Supports patient counseling and education
    - Facilitates communication between patients and providers
    
    Quality Assurance:
    - HbA1c assays should be NGSP-certified and standardized
    - Point-of-care devices should meet accuracy standards
    - Results should be interpreted in clinical context
    - Consider complementary glucose monitoring data
    
    References (Vancouver style):
    1. Nathan DM, Kuenen J, Borg R, Zheng H, Schoenfeld D, Heine RJ. Translating 
    the A1C assay into estimated average glucose values. Diabetes Care. 
    2008;31(8):1473-8. doi: 10.2337/dc08-0545.
    2. American Diabetes Association. 6. Glycemic Targets: Standards of Medical Care 
    in Diabetes-2021. Diabetes Care. 2021;44(Suppl 1):S73-S84. doi: 10.2337/dc21-S006.
    3. International Expert Committee. International Expert Committee report on the 
    role of the A1C assay in the diagnosis of diabetes. Diabetes Care. 2009;32(7):1327-34. 
    doi: 10.2337/dc09-9033.
    4. Rohlfing CL, Wiedmeyer HM, Little RR, England JD, Tennill A, Goldstein DE. 
    Defining the relationship between plasma glucose and HbA(1c): analysis of glucose 
    profiles and HbA(1c) in the Diabetes Control and Complications Trial. Diabetes Care. 
    2002;25(2):275-8. doi: 10.2337/diacare.25.2.275.
    """
    
    hba1c_percent: float = Field(
        ...,
        description="Hemoglobin A1C value as a percentage (3.0-20.0%). Reflects average blood glucose over 2-3 months",
        ge=3.0,
        le=20.0,
        example=7.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "hba1c_percent": 7.0
            }
        }


class EstimatedAverageGlucoseEagHba1cResponse(BaseModel):
    """
    Response model for Estimated Average Glucose (eAG) From HbA1C
    
    The eAG result provides an estimated average glucose level in mg/dL that 
    corresponds to the input HbA1c percentage. This value represents what the 
    average glucose meter reading would be if glucose were measured continuously 
    over the 2-3 month period reflected by the HbA1c.
    
    Clinical Interpretation Guidelines:
    
    Normal Range (eAG ≤125 mg/dL, HbA1c <5.7%):
    - Indicates normal glucose metabolism
    - Low risk for diabetes development
    - Continue healthy lifestyle practices
    - Routine screening intervals appropriate
    
    Prediabetes Range (eAG 126-153 mg/dL, HbA1c 5.7-6.4%):
    - Increased risk for developing type 2 diabetes
    - Lifestyle interventions strongly recommended
    - Weight loss of 5-10% if overweight
    - Increased physical activity (150 minutes/week)
    - Consider diabetes prevention programs
    - Annual monitoring recommended
    
    Diabetes - Good Control (eAG 154-182 mg/dL, HbA1c 6.5-7.4%):
    - Diabetes diagnosis confirmed
    - Generally good glycemic control achieved
    - Continue current management plan
    - Regular monitoring and provider follow-up
    - Assess for complications as appropriate
    
    Diabetes - Moderate Control (eAG 183-239 mg/dL, HbA1c 7.5-9.0%):
    - Suboptimal glycemic control
    - Treatment intensification may be needed
    - Medication adjustment consideration
    - Enhanced lifestyle interventions
    - Diabetes education referral
    - More frequent monitoring
    
    Diabetes - Poor Control (eAG ≥240 mg/dL, HbA1c >9.0%):
    - Significantly elevated glucose levels
    - Urgent treatment intensification needed
    - High risk for complications
    - Comprehensive diabetes management review
    - Consider specialist referral
    - Intensive monitoring and support
    
    Management Considerations:
    
    Individualized Targets:
    - Younger, healthier patients: More stringent goals (HbA1c <6.5%)
    - Older patients with comorbidities: Less stringent goals (HbA1c <8%)
    - Pregnancy: Very tight control (HbA1c <6%)
    - Consider hypoglycemia risk and patient preferences
    
    Treatment Approaches:
    - Lifestyle modifications (diet, exercise, weight management)
    - Oral medications (metformin, sulfonylureas, etc.)
    - Injectable medications (GLP-1 agonists, insulin)
    - Combination therapy as needed
    - Regular monitoring and adjustments
    
    Monitoring Frequency:
    - Well-controlled diabetes: Every 6 months
    - Poorly controlled or changing therapy: Every 3 months
    - Newly diagnosed: More frequent initially
    - Consider continuous glucose monitoring when appropriate
    
    Patient Education Topics:
    - Understanding the eAG and HbA1c relationship
    - Target goals and their importance
    - Relationship to daily glucose readings
    - Lifestyle factors affecting glucose control
    - Medication adherence and timing
    - When to contact healthcare providers
    
    Reference: Nathan DM, et al. Diabetes Care. 2008;31(8):1473-8.
    """
    
    result: float = Field(
        ...,
        description="Estimated average glucose level in mg/dL calculated from HbA1c using the ADAG formula",
        example=154.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for estimated average glucose",
        example="mg/dL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on eAG and HbA1c values",
        example="Estimated average glucose indicates diabetes (HbA1c 7.0%) with relatively good glycemic control. The American Diabetes Association suggests target HbA1c <7% (eAG <154 mg/dL) for most nonpregnant adults with diabetes."
    )
    
    stage: str = Field(
        ...,
        description="Clinical category (Normal, Prediabetes, Diabetes - Good Control, Diabetes - Moderate Control, or Diabetes - Poor Control)",
        example="Diabetes - Good Control"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical category",
        example="Diabetic range with good control"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 154.0,
                "unit": "mg/dL",
                "interpretation": "Estimated average glucose indicates diabetes (HbA1c 7.0%) with relatively good glycemic control. The American Diabetes Association suggests target HbA1c <7% (eAG <154 mg/dL) for most nonpregnant adults with diabetes. Continue current diabetes management plan with regular monitoring and healthcare provider follow-up.",
                "stage": "Diabetes - Good Control",
                "stage_description": "Diabetic range with good control"
            }
        }