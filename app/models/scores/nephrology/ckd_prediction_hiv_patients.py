"""
CKD Prediction in HIV+ Patients Models

Request and response models for CKD prediction in HIV-positive patients.

References (Vancouver style):
1. Scherzer R, Gandhi M, Estrella MM, Tien PC, Deeks SG, Grunfeld C, Peralta CA, Shlipak MG. 
   A chronic kidney disease risk score to determine tenofovir safety in a prospective cohort of 
   HIV-positive male veterans. AIDS. 2014;28(9):1289-95.
2. Mocroft A, Lundgren JD, Ross M, Law M, Reiss P, Kirk O, Smith C, Wentworth D, Neuhaus J, 
   Fux CA, Moranne O, Morlat P, Johnson MA, Ryom L; D:A:D Study Group. Development and 
   validation of a risk score for chronic kidney disease in HIV infection using prospective 
   cohort data from the D:A:D study. PLoS Med. 2015;12(3):e1001809.

The CKD Prediction Calculator for HIV+ Patients is a validated risk assessment tool that 
estimates the 5-year probability of developing chronic kidney disease in HIV-infected 
individuals. This calculator is particularly valuable for guiding clinical decision-making 
regarding tenofovir disoproxil fumarate (TDF) use, a commonly prescribed antiretroviral 
medication with known nephrotoxic potential.

Clinical Background and Development:

The calculator was developed using data from a prospective cohort study of HIV-positive 
male veterans within the Veterans Health Administration system. The study followed 10,841 
HIV-infected patients over a median of 9 years, during which 1,474 CKD events occurred. 
The overall 5-year CKD event rate was 7.7% in tenofovir users compared to 3.8% in 
non-users, representing a 2-fold increased risk (adjusted hazard ratio 2.0, 95% CI 1.8-2.2).

Risk Score Development and Validation:

The risk score incorporates seven key variables that were identified as significant predictors 
of CKD development in multivariable analysis. Traditional kidney disease risk factors 
(age, glucose, blood pressure, hypertension, triglycerides, proteinuria) were the dominant 
contributors, while HIV-specific factors were represented by CD4+ cell count. Notably, 
HIV RNA viral load was not included as it did not significantly contribute to CKD risk 
prediction in the final model.

The scoring system assigns points based on the relative contribution of each risk factor:
- Age represents the strongest predictor, with points increasing with each decade (0-6 points)
- Traditional cardiovascular risk factors contribute 1-2 points each
- Low CD4+ count (<200 cells/µL) adds 1 point, reflecting HIV disease severity

Clinical Applications and Decision-Making:

The calculator provides personalized risk estimates that can inform several clinical decisions:

1. Tenofovir Safety Assessment:
   The tool quantifies individual CKD risk both with and without tenofovir use, enabling 
   clinicians to weigh the benefits of effective HIV treatment against potential kidney 
   toxicity. This is particularly valuable given tenofovir's role as a backbone agent 
   in many first-line HIV regimens.

2. Alternative Regimen Consideration:
   For patients at high CKD risk, the calculator supports decisions to use alternative 
   antiretroviral agents such as tenofovir alafenamide (TAF), abacavir, or integrase 
   inhibitor-based regimens that may have less nephrotoxic potential.

3. Monitoring Intensity:
   Risk scores guide the frequency of kidney function monitoring, with higher-risk 
   patients requiring more frequent assessment (every 3 months vs. standard 6-12 months).

4. Number Needed to Harm (NNH) Estimates:
   The calculator provides NNH estimates ranging from 108 for low-risk patients (0 points) 
   to 20 for high-risk patients (≥9 points), helping quantify the absolute risk increase 
   attributable to tenofovir use.

Risk Stratification and Clinical Interpretation:

Low Risk (0-4% 5-year CKD risk):
- Tenofovir use is reasonable with routine monitoring
- Standard HIV care monitoring intervals (every 6-12 months)
- Focus on maintaining good control of traditional risk factors

Moderate Risk (5-14% 5-year CKD risk):
- Careful consideration of tenofovir risks and benefits
- Enhanced monitoring every 3-6 months if using tenofovir
- Consider alternatives if equally effective options available

High Risk (≥15% 5-year CKD risk):
- Strong consideration for tenofovir alternatives
- If tenofovir continued, monitor kidney function every 3 months
- Nephrology consultation for declining eGFR
- Aggressive management of modifiable risk factors

Implementation Considerations:

Patient Population:
The original validation was performed in HIV-positive male veterans, and subsequent 
validation in the international D:A:D cohort (which included women and diverse populations) 
confirmed the tool's broader applicability. However, clinicians should consider population-
specific factors when applying the calculator.

Baseline Kidney Function:
The calculator assumes normal baseline kidney function and should be interpreted cautiously 
in patients with pre-existing CKD. Additional factors such as baseline eGFR, rate of 
kidney function decline, and presence of active urinary sediment should inform decision-making.

Concurrent Risk Factors:
The calculator focuses on traditional and HIV-specific risk factors but does not account 
for all potential contributors to CKD risk. Clinicians should consider additional factors 
such as:
- Concurrent nephrotoxic medications
- Hepatitis B or C coinfection
- Family history of kidney disease
- Recent acute kidney injury episodes

Limitations and Clinical Judgment:

While the calculator provides valuable risk stratification, it should supplement rather 
than replace clinical judgment. Important limitations include:

1. The tool was developed primarily in male veterans and may not fully capture risk 
   in other populations
2. Dynamic factors such as changes in HIV control, medication adherence, or development 
   of new comorbidities are not incorporated
3. The calculator provides population-based estimates that may not reflect individual 
   patient trajectories

Clinical Integration:

For optimal use, the calculator should be integrated into routine HIV care workflows:
- Calculate baseline CKD risk at HIV diagnosis or when considering tenofovir initiation
- Reassess risk periodically as patient factors change
- Use risk estimates to guide shared decision-making about antiretroviral regimen selection
- Adjust monitoring intensity based on risk stratification
- Consider nephrology referral for high-risk patients or those with declining kidney function

The CKD Prediction Calculator for HIV+ Patients represents an important advance in 
personalized HIV care, enabling clinicians to balance the benefits of effective 
antiretroviral therapy with the potential risks of kidney toxicity. By providing 
quantitative risk estimates, the tool supports evidence-based decision-making and 
helps optimize long-term outcomes for HIV-infected patients.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CkdPredictionHivPatientsRequest(BaseModel):
    """
    Request model for CKD Prediction in HIV+ Patients
    
    This calculator estimates the 5-year probability of developing chronic kidney disease 
    (CKD) in HIV-infected patients, with particular focus on the impact of tenofovir 
    disoproxil fumarate (TDF) use. The tool incorporates seven validated risk factors 
    to provide personalized risk estimates that guide clinical decision-making.
    
    Risk Factor Assessment Guidelines:
    
    Age Categories:
    The strongest predictor of CKD development, with risk increasing substantially 
    with each decade of life:
    - 19-39 years: Baseline risk category (0 points)
    - 40-49 years: Moderate risk increase (2 points)
    - 50-59 years: Substantial risk increase (4 points)
    - 60-90 years: Highest risk category (6 points)
    
    Glucose Elevation (>140 mg/dL):
    Indicates diabetes or pre-diabetes, a major risk factor for CKD development. 
    This threshold captures patients with significant glucose intolerance who may 
    benefit from diabetes screening and management. Consider both fasting and 
    random glucose measurements, and correlation with HbA1c when available.
    
    Systolic Blood Pressure Elevation (>140 mmHg):
    Reflects vascular damage and increased cardiovascular risk. This threshold 
    aligns with traditional hypertension definitions and captures patients who 
    may benefit from blood pressure optimization. Consider both clinic and 
    ambulatory measurements when available.
    
    Hypertension Diagnosis:
    Formal diagnosis of hypertension, typically based on sustained blood pressure 
    elevation or current antihypertensive medication use. This carries the highest 
    point value among modifiable risk factors, reflecting its dominant role in 
    CKD progression. Include patients currently managed with lifestyle or 
    pharmacological interventions.
    
    Triglycerides Elevation (>200 mg/dL):
    Indicates metabolic dysfunction and increased cardiovascular risk. Elevated 
    triglycerides often cluster with other metabolic abnormalities and may reflect 
    insulin resistance, diabetes risk, or HIV/antiretroviral medication effects. 
    Consider fasting measurements when possible.
    
    Proteinuria:
    Presence of protein in urine, indicating existing kidney damage or dysfunction. 
    This is a strong predictor of CKD progression and may be detected through 
    dipstick testing, spot urine protein/creatinine ratio, or 24-hour urine 
    collection. Any degree of persistent proteinuria should be considered positive.
    
    CD4+ Count (<200 cells/µL):
    Reflects HIV disease severity and degree of immunosuppression. Low CD4+ counts 
    indicate advanced HIV disease and increased risk for complications, including 
    kidney disease. Consider both current and nadir CD4+ counts, with current 
    count typically more relevant for ongoing risk assessment.
    
    Tenofovir Use:
    Current or planned use of tenofovir disoproxil fumarate (TDF), a nucleotide 
    reverse transcriptase inhibitor with established nephrotoxic potential. This 
    parameter modifies the final risk calculation, typically doubling the baseline 
    CKD risk. Consider both current use and planned initiation.
    
    Clinical Assessment Context:
    
    Timing of Assessment:
    - Perform baseline assessment at HIV diagnosis
    - Reassess when considering antiretroviral regimen changes
    - Re-evaluate periodically as risk factors evolve
    - Consider before initiating potentially nephrotoxic medications
    
    Risk Factor Optimization:
    Use the calculator to identify modifiable risk factors that could reduce 
    overall CKD risk:
    - Blood pressure control to <140/90 mmHg (or <130/80 in diabetes)
    - Diabetes management with HbA1c <7% when appropriate
    - Lipid management with triglycerides <200 mg/dL
    - HIV viral suppression to optimize CD4+ recovery
    
    Integration with HIV Care:
    - Coordinate with HIV providers for optimal antiretroviral selection
    - Consider baseline kidney function (eGFR, urinalysis) interpretation
    - Plan monitoring frequency based on calculated risk
    - Identify patients who may benefit from nephrology consultation
    
    References (Vancouver style):
    1. Scherzer R, Gandhi M, Estrella MM, Tien PC, Deeks SG, Grunfeld C, Peralta CA, 
    Shlipak MG. A chronic kidney disease risk score to determine tenofovir safety in a 
    prospective cohort of HIV-positive male veterans. AIDS. 2014;28(9):1289-95.
    2. Mocroft A, Lundgren JD, Ross M, Law M, Reiss P, Kirk O, Smith C, Wentworth D, 
    Neuhaus J, Fux CA, Moranne O, Morlat P, Johnson MA, Ryom L; D:A:D Study Group. 
    Development and validation of a risk score for chronic kidney disease in HIV infection 
    using prospective cohort data from the D:A:D study. PLoS Med. 2015;12(3):e1001809.
    """
    
    age_category: Literal["19_to_39", "40_to_49", "50_to_59", "60_to_90"] = Field(
        ...,
        description="Patient age category. 19-39 years (0 points), 40-49 years (2 points), 50-59 years (4 points), 60-90 years (6 points)",
        example="50_to_59"
    )
    
    glucose_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Glucose >140 mg/dL (indicates diabetes/pre-diabetes risk). 2 points if yes",
        example="no"
    )
    
    systolic_bp_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure >140 mmHg (indicates vascular damage). 1 point if yes",
        example="yes"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Formal diagnosis of hypertension or current antihypertensive medication use. 2 points if yes",
        example="yes"
    )
    
    triglycerides_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Triglycerides >200 mg/dL (indicates metabolic dysfunction). 1 point if yes",
        example="no"
    )
    
    proteinuria: Literal["yes", "no"] = Field(
        ...,
        description="Presence of proteinuria (any degree, indicates existing kidney damage). 2 points if yes",
        example="no"
    )
    
    cd4_low: Literal["yes", "no"] = Field(
        ...,
        description="CD4+ count <200 cells/µL (indicates HIV disease severity and immunosuppression). 1 point if yes",
        example="no"
    )
    
    tenofovir_use: Literal["yes", "no"] = Field(
        ...,
        description="Current or planned tenofovir disoproxil fumarate (TDF) use. Modifies final CKD risk calculation",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "50_to_59",
                "glucose_elevated": "no",
                "systolic_bp_elevated": "yes",
                "hypertension": "yes",
                "triglycerides_elevated": "no",
                "proteinuria": "no",
                "cd4_low": "no",
                "tenofovir_use": "yes"
            }
        }


class CkdPredictionHivPatientsResponse(BaseModel):
    """
    Response model for CKD Prediction in HIV+ Patients
    
    Provides comprehensive 5-year CKD risk assessment with evidence-based clinical 
    recommendations for HIV-infected patients. The response includes personalized 
    risk estimates, treatment guidance, and monitoring recommendations based on 
    validated risk stratification.
    
    Risk Interpretation and Clinical Management:
    
    Low Risk (<5% 5-year CKD risk):
    
    Clinical Characteristics:
    - Predominantly younger patients with few traditional risk factors
    - Well-controlled HIV disease with preserved immune function
    - Minimal cardiovascular or metabolic comorbidities
    - Normal baseline kidney function
    
    Management Approach:
    - Tenofovir use is reasonable with standard monitoring
    - Routine kidney function assessment every 6-12 months
    - Focus on maintaining good control of modifiable risk factors
    - Standard HIV care protocols appropriate
    - Patient education on kidney health maintenance
    
    Monitoring Requirements:
    - Annual serum creatinine and eGFR calculation
    - Annual urinalysis with microscopy
    - Blood pressure monitoring at each clinic visit
    - Periodic assessment for diabetes development
    
    Moderate Risk (5-14% 5-year CKD risk):
    
    Clinical Characteristics:
    - Middle-aged patients with some traditional risk factors
    - May have controlled hypertension or pre-diabetes
    - HIV disease generally well-controlled
    - Multiple modifiable risk factors present
    
    Management Approach:
    - Careful consideration of tenofovir risks versus benefits
    - Enhanced monitoring if tenofovir continued (every 3-6 months)
    - Consider alternatives if equally effective options available
    - Aggressive management of modifiable risk factors
    - Patient counseling on risk reduction strategies
    
    Monitoring Requirements:
    - Serum creatinine and eGFR every 3-6 months if using tenofovir
    - Semi-annual urinalysis with attention to proteinuria development
    - Blood pressure optimization to <140/90 mmHg
    - Diabetes screening and management if glucose elevated
    - Lipid management if triglycerides elevated
    
    High Risk (≥15% 5-year CKD risk):
    
    Clinical Characteristics:
    - Older patients with multiple traditional risk factors
    - Established hypertension, diabetes, or cardiovascular disease
    - May have advanced HIV disease history
    - Significant cumulative risk factor burden
    
    Management Approach:
    - Strong consideration for tenofovir alternatives (TAF, abacavir, INSTI-based)
    - If tenofovir continued, intensive monitoring every 3 months
    - Nephrology consultation for declining eGFR
    - Multidisciplinary approach to risk factor management
    - Consider ACE inhibitor/ARB for cardiovascular protection
    
    Monitoring Requirements:
    - Serum creatinine and eGFR every 3 months
    - Quarterly urinalysis with quantitative proteinuria assessment
    - Blood pressure optimization to <130/80 mmHg if diabetic
    - Diabetes management with HbA1c monitoring
    - Cardiovascular risk assessment and management
    - Bone health monitoring if continued tenofovir use
    
    Alternative Antiretroviral Considerations:
    
    Tenofovir Alafenamide (TAF):
    - Lower systemic tenofovir exposure with preserved efficacy
    - Reduced nephrotoxicity compared to TDF
    - Preferred option for patients with CKD risk factors
    - May be suitable for moderate to high-risk patients
    
    Abacavir-Based Regimens:
    - No direct nephrotoxicity
    - Requires HLA-B*5701 testing before initiation
    - Consider for patients with significant CKD risk
    - Monitor for cardiovascular effects in high-risk patients
    
    Integrase Inhibitor-Based Regimens:
    - Excellent efficacy with minimal kidney effects
    - Can be combined with various backbone agents
    - Suitable for patients requiring tenofovir avoidance
    - Consider drug interactions and resistance patterns
    
    Quality Assurance and Follow-up:
    
    Risk Reassessment:
    - Re-calculate risk annually or when clinical status changes
    - Consider dynamic changes in HIV control, comorbidities, or medications
    - Adjust monitoring and treatment plans based on updated risk estimates
    - Document rationale for antiretroviral regimen selection
    
    Patient Education Components:
    - Explanation of individual CKD risk factors and modification strategies
    - Importance of medication adherence and monitoring compliance
    - Recognition of symptoms that warrant immediate medical attention
    - Lifestyle modifications to reduce kidney disease progression
    
    The CKD Prediction Calculator provides essential risk stratification that enables 
    personalized HIV care while minimizing long-term kidney complications. When properly 
    implemented with appropriate clinical context and regular reassessment, this tool 
    significantly improves treatment decision-making and patient outcomes.
    
    Reference: Scherzer R, et al. AIDS. 2014;28(9):1289-95.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="5-year chronic kidney disease development risk percentage",
        example=11.9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk percentage",
        example="percent"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and treatment recommendations",
        example="5-year CKD risk: 11.9% with tenofovir. Moderate risk - careful monitoring every 3-6 months and consideration of alternative agents if CKD progression occurs."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate risk for CKD development"
    )
    
    scoring_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of risk factors, scoring, clinical guidance, and comparative risk analysis",
        example={
            "risk_factors": {
                "age": {
                    "category": "50-59 years",
                    "points": 4,
                    "rationale": "Older age is a dominant risk factor for CKD development"
                },
                "hypertension": {
                    "present": True,
                    "points": 2,
                    "rationale": "Hypertension diagnosis is strongest traditional CKD risk factor"
                }
            },
            "score_summary": {
                "total_score": 7,
                "max_possible_score": 15,
                "risk_category": "Moderate risk"
            },
            "risk_comparison": {
                "without_tenofovir": "6.2%",
                "with_tenofovir": "11.9%",
                "absolute_risk_increase": "5.7%",
                "number_needed_to_harm": 29
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 11.9,
                "unit": "percent",
                "interpretation": "5-year CKD risk: 11.9% with tenofovir. Moderate risk - careful monitoring every 3-6 months and consideration of alternative agents if CKD progression occurs.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk for CKD development",
                "scoring_breakdown": {
                    "risk_factors": {
                        "age": {
                            "category": "50-59 years", 
                            "points": 4,
                            "rationale": "Older age is a dominant risk factor for CKD development"
                        },
                        "hypertension": {
                            "present": True,
                            "points": 2,
                            "rationale": "Hypertension diagnosis is strongest traditional CKD risk factor"
                        }
                    },
                    "score_summary": {
                        "total_score": 7,
                        "max_possible_score": 15,
                        "risk_category": "Moderate risk"
                    },
                    "risk_comparison": {
                        "without_tenofovir": "6.2%",
                        "with_tenofovir": "11.9%",
                        "number_needed_to_harm": 29
                    }
                }
            }
        }