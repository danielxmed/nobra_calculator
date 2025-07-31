"""
Framingham Risk Score for Hard Coronary Heart Disease Models

Request and response models for Framingham Risk Score calculation.

References (Vancouver style):
1. Wilson PW, D'Agostino RB, Levy D, Belanger AM, Silbershatz H, Kannel WB. 
   Prediction of coronary heart disease using risk factor categories. Circulation. 
   1998;97(18):1837-47. doi: 10.1161/01.cir.97.18.1837.
2. D'Agostino RB Sr, Vasan RS, Pencina MJ, Wolf PA, Cobain M, Massaro JM, Kannel WB. 
   General cardiovascular risk profile for use in primary care: the Framingham Heart Study. 
   Circulation. 2008;117(6):743-53. doi: 10.1161/CIRCULATIONAHA.107.699579.
3. Expert Panel on Detection, Evaluation, and Treatment of High Blood Cholesterol in Adults. 
   Executive Summary of The Third Report of The National Cholesterol Education Program (NCEP) 
   Expert Panel on Detection, Evaluation, And Treatment of High Blood Cholesterol In Adults 
   (Adult Treatment Panel III). JAMA. 2001;285(19):2486-97. doi: 10.1001/jama.285.19.2486.

The Framingham Risk Score for Hard Coronary Heart Disease was developed from the landmark 
Framingham Heart Study to estimate 10-year risk of myocardial infarction and coronary death 
in primary prevention patients. This calculator uses gender-specific equations with multiple 
cardiovascular risk factors to provide personalized risk assessment.

Key Features:
- Developed from Framingham Heart Study (1998)
- Gender-specific regression equations with established coefficients
- Estimates 10-year risk of "hard" CHD events (MI, coronary death)
- Validated for ages 30-79 years without known CHD or diabetes
- Uses readily available clinical parameters

Risk Factors Included:
- Age (30-79 years)
- Sex (male/female with different risk profiles)
- Total cholesterol (mg/dL)
- HDL cholesterol (mg/dL) - protective factor
- Systolic blood pressure (mmHg)
- Blood pressure treatment status
- Current smoking status

Risk Categories:
- Low Risk: <5% 10-year risk
- Borderline Risk: 5-10% 10-year risk  
- Intermediate Risk: 10-20% 10-year risk
- High Risk: ≥20% 10-year risk

Clinical Applications:
- Primary prevention risk stratification
- Statin therapy decision-making per ATP III guidelines
- Patient counseling and shared decision-making
- Population health screening and management
- Research studies requiring standardized CHD risk prediction

Important Limitations:
- Not recommended for patients with diabetes (use diabetes-specific calculators)
- Not recommended for patients with known coronary heart disease
- Based on predominantly white population from Framingham
- May overestimate risk in some contemporary populations
- Newer calculators (ASCVD 2013) may be more appropriate for current practice

Treatment Implications:
- Low Risk: Lifestyle modifications, standard preventive care
- Borderline Risk: Consider additional risk factors, possible statin therapy
- Intermediate Risk: Strong consideration for statin therapy
- High Risk: Definite indication for pharmacotherapy and aggressive risk modification
"""

from pydantic import BaseModel, Field
from typing import Literal


class FraminghamRiskScoreRequest(BaseModel):
    """
    Request model for Framingham Risk Score for Hard Coronary Heart Disease
    
    The Framingham Risk Score estimates 10-year risk of myocardial infarction and coronary 
    death using gender-specific equations with multiple cardiovascular risk factors. This 
    calculator is intended for primary prevention in patients aged 30-79 without known 
    coronary heart disease or diabetes.
    
    **RISK FACTORS**:
    
    **Demographics**:
    - **Age**: 30-79 years (validation range from original study)
    - **Sex**: Male vs female (different risk profiles and coefficients)
    
    **Lipid Profile**:
    - **Total Cholesterol**: Complete lipid panel measurement in mg/dL
    - **HDL Cholesterol**: "Good" cholesterol - higher levels are protective
    
    **Blood Pressure**:
    - **Systolic BP**: Upper blood pressure reading in mmHg
    - **BP Treatment**: Whether currently taking antihypertensive medications
    
    **Lifestyle Factor**:
    - **Smoking**: Current smoking status (major modifiable risk factor)
    
    **CALCULATION METHOD**:
    Uses gender-specific logarithmic regression equations with established coefficients:
    - Men: Risk = 1 - (0.88936)^exp(ΣβX - 23.9802)
    - Women: Risk = 1 - (0.95012)^exp(ΣβX - 26.1931)
    Where β = regression coefficient and X = risk factor level
    
    **RISK INTERPRETATION**:
    - **Low Risk (<5%)**: Standard preventive measures, lifestyle counseling
    - **Borderline Risk (5-10%)**: Consider additional risk factors, possible statin therapy
    - **Intermediate Risk (10-20%)**: Strong consideration for statin therapy per ATP III
    - **High Risk (≥20%)**: Definite indication for pharmacotherapy and aggressive management
    
    **CLINICAL APPLICATIONS**:
    - Primary prevention risk stratification
    - Statin therapy decision-making per NCEP ATP III guidelines
    - Patient education and shared decision-making
    - Population health screening programs
    - Clinical research requiring standardized CHD risk assessment
    
    **IMPORTANT EXCLUSIONS**:
    - Patients with diabetes mellitus (use diabetes-specific risk calculators)
    - Patients with known coronary heart disease (secondary prevention)
    - Patients with peripheral arterial disease or stroke
    - Ages outside 30-79 years (not validated)
    
    **LIMITATIONS**:
    - Based on predominantly white Framingham population (1970s-1990s)
    - May overestimate risk in some contemporary populations
    - Consider newer risk calculators (ASCVD 2013) for more diverse populations
    - Does not include newer risk factors (family history, inflammatory markers)
    
    References (Vancouver style):
    1. Wilson PW, D'Agostino RB, Levy D, Belanger AM, Silbershatz H, Kannel WB. 
       Prediction of coronary heart disease using risk factor categories. Circulation. 
       1998;97(18):1837-47.
    2. Expert Panel on Detection, Evaluation, and Treatment of High Blood Cholesterol in Adults. 
       Executive Summary of The Third Report of The National Cholesterol Education Program (NCEP) 
       Expert Panel on Detection, Evaluation, And Treatment of High Blood Cholesterol In Adults 
       (Adult Treatment Panel III). JAMA. 2001;285(19):2486-97.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Valid range: 30-79 years (original study validation range)",
        ge=30,
        le=79,
        example=55
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Uses gender-specific regression coefficients with different risk profiles for men and women",
        example="male"
    )
    
    total_cholesterol: float = Field(
        ...,
        description="Total cholesterol level in mg/dL. Standard lipid panel measurement. Valid range: 100-400 mg/dL",
        ge=100,
        le=400,
        example=220.0
    )
    
    hdl_cholesterol: float = Field(
        ...,
        description="HDL cholesterol (good cholesterol) in mg/dL. Higher levels are protective against CHD. Valid range: 20-100 mg/dL",
        ge=20,
        le=100,
        example=45.0
    )
    
    systolic_bp: int = Field(
        ...,
        description="Systolic blood pressure in mmHg. Upper reading from blood pressure measurement. Valid range: 90-200 mmHg",
        ge=90,
        le=200,
        example=140
    )
    
    bp_treatment: Literal["yes", "no"] = Field(
        ...,
        description="Currently taking blood pressure medication. Affects the coefficient used for systolic BP in risk calculation",
        example="yes"
    )
    
    smoking: Literal["yes", "no"] = Field(
        ...,
        description="Current smoking status. Major modifiable risk factor that significantly increases CHD risk",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 55,
                "sex": "male",
                "total_cholesterol": 220.0,
                "hdl_cholesterol": 45.0,
                "systolic_bp": 140,
                "bp_treatment": "yes",
                "smoking": "no"
            }
        }


class FraminghamRiskScoreResponse(BaseModel):
    """
    Response model for Framingham Risk Score for Hard Coronary Heart Disease
    
    The response provides the calculated 10-year risk of hard coronary heart disease events 
    (myocardial infarction and coronary death) along with risk category classification and 
    clinical management recommendations based on established guidelines.
    
    **RISK CATEGORIES AND MANAGEMENT**:
    
    **Low Risk (<5% 10-year risk)**:
    - **Management**: Standard preventive measures, lifestyle modifications
    - **Interventions**: Diet counseling, exercise prescription, smoking cessation
    - **Monitoring**: Routine cardiovascular risk factor screening
    - **Pharmacotherapy**: Generally not indicated based on risk alone
    
    **Borderline Risk (5-10% 10-year risk)**:
    - **Management**: Intensive lifestyle modifications, consider additional risk factors
    - **Interventions**: Structured diet and exercise programs, weight management
    - **Additional Testing**: Consider coronary artery calcium scoring for further stratification
    - **Pharmacotherapy**: May benefit from statin therapy based on clinical judgment
    
    **Intermediate Risk (10-20% 10-year risk)**:
    - **Management**: Strong consideration for pharmacotherapy plus lifestyle modifications
    - **Primary Treatment**: Statin therapy recommended per ATP III guidelines
    - **Target Goals**: LDL-C <100 mg/dL, consider <70 mg/dL for higher-risk patients
    - **Additional Therapy**: Consider other cardioprotective medications as appropriate
    
    **High Risk (≥20% 10-year risk)**:
    - **Management**: Definite indication for aggressive pharmacotherapy and risk modification
    - **Primary Treatment**: High-intensity statin therapy
    - **Target Goals**: LDL-C <70 mg/dL, consider <50 mg/dL for very high-risk patients
    - **Additional Therapy**: Consider antiplatelet therapy, ACE inhibitors, other medications
    - **Monitoring**: Intensive follow-up and aggressive risk factor management
    
    **CLINICAL DECISION-MAKING**:
    
    **Statin Therapy Considerations**:
    - ATP III guidelines recommend statin therapy for 10-year risk ≥10%
    - Consider statin therapy for 5-10% risk with additional risk factors
    - Shared decision-making important for borderline risk patients
    - Consider patient preferences, life expectancy, and comorbidities
    
    **Additional Risk Stratification**:
    - Family history of premature CHD
    - Inflammatory markers (hs-CRP, if available)
    - Coronary artery calcium scoring for intermediate risk
    - Ankle-brachial index if peripheral disease suspected
    
    **Lifestyle Interventions (All Risk Categories)**:
    - Dietary modifications (Mediterranean diet, DASH diet)
    - Regular aerobic exercise (≥150 minutes/week moderate intensity)
    - Weight management (BMI <25 kg/m², waist circumference goals)
    - Smoking cessation programs and support
    - Stress management and adequate sleep
    
    **Follow-up Recommendations**:
    - Low Risk: Annual to biennial screening
    - Borderline Risk: Annual evaluation with lifestyle reinforcement
    - Intermediate Risk: 6-12 month follow-up, monitor therapy response
    - High Risk: 3-6 month follow-up initially, then according to stability
    
    **Quality Measures**:
    - Validated in multiple populations and clinical settings
    - Incorporated into major clinical practice guidelines
    - Widely used in clinical practice and research
    - Foundation for contemporary risk assessment tools
    
    Reference: Wilson PW, et al. Circulation. 1998;97(18):1837-47.
    """
    
    result: float = Field(
        ...,
        description="10-year risk of hard coronary heart disease events as a percentage (0.0-50.0%)",
        example=12.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk calculation",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk category, clinical significance, and evidence-based management recommendations",
        example="Intermediate risk with 12.5% 10-year risk of hard coronary heart disease events. Strong consideration for pharmacotherapy (statins) in addition to intensive lifestyle modifications. Consider additional risk stratification tools if treatment decision uncertain. Target LDL-C <100 mg/dL, consider <70 mg/dL."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Borderline Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate 10-year CHD risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12.5,
                "unit": "%",
                "interpretation": "Intermediate risk with 12.5% 10-year risk of hard coronary heart disease events. Strong consideration for pharmacotherapy (statins) in addition to intensive lifestyle modifications. Consider additional risk stratification tools if treatment decision uncertain. Target LDL-C <100 mg/dL, consider <70 mg/dL.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate 10-year CHD risk"
            }
        }