"""
Denver HIV Risk Score Models

Request and response models for Denver HIV Risk Score calculation.

References (Vancouver style):
1. Haukoos JS, Hopkins E, Conroy AA, et al. Derivation and validation of the Denver 
   Human Immunodeficiency Virus (HIV) risk score for targeted HIV screening. Am J 
   Epidemiol. 2012;175(8):838-846. doi: 10.1093/aje/kwr389.
2. Hsieh YH, Jung JJ, Shahan JB, et al. Validation of an abbreviated version of the 
   Denver HIV risk score for prediction of HIV infection in an urban emergency 
   department. Acad Emerg Med. 2014;21(7):757-767. doi: 10.1111/acem.12413.
3. Centers for Disease Control and Prevention. Screening for HIV infection: US 
   Preventive Services Task Force recommendation statement. JAMA. 2019;321(23):2326-2336. 
   doi: 10.1001/jama.2019.6587.

The Denver HIV Risk Score is a validated clinical decision tool that predicts the 
probability of undiagnosed HIV infection in patients aged 13 and older. It uses 
demographic and behavioral risk factors to stratify patients into risk categories, 
enabling targeted HIV screening in clinical settings and optimizing resource allocation 
for testing programs.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any


class DenverHivRiskScoreRequest(BaseModel):
    """
    Request model for Denver HIV Risk Score
    
    The Denver HIV Risk Score uses demographic and behavioral factors to predict 
    undiagnosed HIV infection probability:
    
    Age Categories:
    - under_22: Age <22 years (2 points)
    - 22_25: Age 22-25 years (4 points)
    - 26_32: Age 26-32 years (6 points)  
    - 33_46: Age 33-46 years (12 points)
    - 47_54: Age 47-54 years (8 points)
    - 55_60: Age 55-60 years (3 points)
    - over_60: Age >60 years (0 points)
    
    Gender:
    - male: Male gender (21 points)
    - female: Female gender (0 points)
    
    Sexual Practices:
    - sex_with_male: Sex with male partner (22 points)
    - receptive_anal_intercourse: Receptive anal intercourse (8 points)
    - vaginal_intercourse: Vaginal intercourse (-10 points)
    - none: No specified sexual practices (0 points)
    
    Injection Drug Use:
    - yes: History of injection drug use (9 points)
    - no: No injection drug use (0 points)
    
    Past HIV Testing:
    - yes: Previous HIV testing (-4 points)
    - no: No previous testing (0 points)
    
    Race/Ethnicity (Optional):
    - black: Black/African American (9 points)
    - hispanic: Hispanic/Latino (3 points)
    - white: White/Caucasian (0 points)
    - asian: Asian/Pacific Islander (0 points)
    - other: Other ethnicity (1 point)

    Score ranges from -14 to +81 points with five risk categories:
    - Very Low (<20): 0.31% HIV prevalence
    - Low (20-29): 0.41% HIV prevalence
    - Moderate (30-39): 0.99% HIV prevalence
    - High (40-49): 1.59% HIV prevalence
    - Very High (≥50): 3.59% HIV prevalence

    References:
    1. Haukoos JS, et al. Am J Epidemiol. 2012;175(8):838-846.
    2. Hsieh YH, et al. Acad Emerg Med. 2014;21(7):757-767.
    3. CDC. JAMA. 2019;321(23):2326-2336.
    """
    
    age_group: Literal["under_22", "22_25", "26_32", "33_46", "47_54", "55_60", "over_60"] = Field(
        ...,
        description="Patient age category. Points: <22y(2), 22-25y(4), 26-32y(6), 33-46y(12), 47-54y(8), 55-60y(3), >60y(0)",
        example="26_32"
    )
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Male gender scores 21 points, female scores 0 points",
        example="male"
    )
    
    sexual_practices: Literal["sex_with_male", "receptive_anal_intercourse", "vaginal_intercourse", "none"] = Field(
        ...,
        description="Sexual behavior risk factors. Points: sex with male(22), receptive anal(-10), vaginal(-10), none(0)",
        example="vaginal_intercourse"
    )
    
    injection_drug_use: Literal["yes", "no"] = Field(
        ...,
        description="History of injection drug use. Yes scores 9 points, no scores 0 points",
        example="no"
    )
    
    past_hiv_testing: Literal["yes", "no"] = Field(
        ...,
        description="History of previous HIV testing. Yes scores -4 points (protective), no scores 0 points",
        example="yes"
    )
    
    race_ethnicity: Optional[Literal["black", "hispanic", "white", "asian", "other"]] = Field(
        None,
        description="Race/ethnicity (optional). Points: Black(9), Hispanic(3), White(0), Asian(0), Other(1)",
        example="white"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_group": "26_32",
                "gender": "male",
                "sexual_practices": "vaginal_intercourse",
                "injection_drug_use": "no",
                "past_hiv_testing": "yes",
                "race_ethnicity": "white"
            }
        }


class DenverHivRiskScoreResponse(BaseModel):
    """
    Response model for Denver HIV Risk Score
    
    The Denver HIV Risk Score provides comprehensive HIV risk assessment including:
    - Calculated risk score (-14 to +81 points)
    - Risk category classification (Very Low to Very High)
    - HIV prevalence estimates for similar populations
    - Targeted screening recommendations
    - Prevention guidance and PrEP considerations
    - Clinical assessment and follow-up recommendations
    
    Risk Categories:
    - Very Low (<20 points): 0.31% prevalence, routine screening
    - Low (20-29 points): 0.41% prevalence, offer testing
    - Moderate (30-39 points): 0.99% prevalence, strongly recommend testing
    - High (40-49 points): 1.59% prevalence, urgent testing
    - Very High (≥50 points): 3.59% prevalence, immediate testing
    
    Reference: Haukoos JS, et al. Am J Epidemiol. 2012;175(8):838-846.
    """
    
    result: int = Field(
        ...,
        description="Denver HIV Risk Score calculated from risk factors (range: -14 to +81 points)",
        example=13
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="Denver HIV Risk Score"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with screening recommendations and risk context",
        example="Denver HIV Risk Score of 13 indicates Very Low Risk with approximately 0.31% HIV prevalence in similar populations. Routine screening may be considered based on clinical judgment and standard guidelines."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Very Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Very low probability of undiagnosed HIV infection"
    )
    
    hiv_risk_score: int = Field(
        ...,
        description="The calculated Denver HIV Risk Score",
        example=13
    )
    
    risk_category: str = Field(
        ...,
        description="Risk category identifier (very_low, low, moderate, high, very_high)",
        example="very_low"
    )
    
    hiv_prevalence: str = Field(
        ...,
        description="Estimated HIV prevalence percentage for this risk category",
        example="0.31%"
    )
    
    prevalence_numeric: float = Field(
        ...,
        description="Numeric HIV prevalence value for calculations",
        example=0.31
    )
    
    recommendation: str = Field(
        ...,
        description="Primary screening recommendation based on risk level",
        example="Consider routine screening per guidelines"
    )
    
    clinical_assessment: Dict[str, Any] = Field(
        ...,
        description="Detailed clinical assessment including score breakdown and risk factors",
        example={
            "hiv_risk_score": 13,
            "risk_category": "very_low",
            "score_components": ["Age 26-32 years (6 points)", "Male gender (21 points)"],
            "risk_factors": ["Male gender associated with higher HIV acquisition risk"],
            "protective_factors": ["Previous HIV testing indicates health-seeking behavior"],
            "clinical_considerations": ["Patient assessed with Denver HIV Risk Score of 13"]
        }
    )
    
    screening_recommendations: Dict[str, Any] = Field(
        ...,
        description="Comprehensive screening recommendations including frequency and counseling",
        example={
            "primary_recommendations": ["Consider routine screening per CDC guidelines"],
            "specific_considerations": [],
            "testing_frequency": "Follow standard CDC guidelines",
            "counseling_requirements": ["Basic HIV prevention education"]
        }
    )
    
    prevention_guidance: Dict[str, List[str]] = Field(
        ...,
        description="Prevention guidance including general measures and specific interventions",
        example={
            "general_prevention": ["Consistent condom use during sexual activity"],
            "specific_interventions": [],
            "harm_reduction": [],
            "prep_considerations": []
        }
    )
    
    score_components: List[Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of score components with points and descriptions",
        example=[
            {"component": "Age Group", "value": "26_32", "points": 6, "description": "Age group risk factor"}
        ]
    )
    
    testing_guidance: Dict[str, Any] = Field(
        ...,
        description="Specific testing guidance including test types and timing",
        example={
            "test_types": ["Standard HIV testing (laboratory-based or rapid)"],
            "timing": "Routine testing schedule",
            "result_management": ["Standard result notification procedures"]
        }
    )
    
    follow_up_recommendations: Dict[str, Any] = Field(
        ...,
        description="Follow-up recommendations including timing and components",
        example={
            "timing": "Annual or per standard guidelines",
            "components": ["Risk reassessment", "Repeat testing if indicated"]
        }
    )
    
    prep_considerations: Dict[str, Any] = Field(
        ...,
        description="PrEP candidacy assessment and considerations",
        example={
            "candidacy": "PrEP generally not indicated based on current risk assessment",
            "evaluation_needed": False,
            "specific_factors": []
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 13,
                "unit": "Denver HIV Risk Score",
                "interpretation": "Denver HIV Risk Score of 13 indicates Very Low Risk with approximately 0.31% HIV prevalence in similar populations. Routine screening may be considered based on clinical judgment and standard guidelines.",
                "stage": "Very Low Risk",
                "stage_description": "Very low probability of undiagnosed HIV infection",
                "hiv_risk_score": 13,
                "risk_category": "very_low",
                "hiv_prevalence": "0.31%",
                "prevalence_numeric": 0.31,
                "recommendation": "Consider routine screening per guidelines",
                "clinical_assessment": {
                    "hiv_risk_score": 13,
                    "risk_category": "very_low",
                    "score_components": [
                        "Age 26-32 years (6 points)",
                        "Male gender (21 points)",
                        "Vaginal intercourse (-10 points)",
                        "Injection drug use: no (0 points)",
                        "Past HIV testing: yes (-4 points)",
                        "Race/ethnicity: white (0 points)"
                    ],
                    "risk_factors": ["Male gender associated with higher HIV acquisition risk"],
                    "protective_factors": [
                        "Previous HIV testing indicates health-seeking behavior and awareness",
                        "Vaginal intercourse carries lower transmission risk than anal intercourse"
                    ],
                    "clinical_considerations": [
                        "Patient assessed with Denver HIV Risk Score of 13",
                        "Risk category: very_low with 0.31% estimated prevalence",
                        "Screening approach: consider routine screening per guidelines"
                    ]
                },
                "screening_recommendations": {
                    "primary_recommendations": [
                        "Consider routine screening per CDC guidelines",
                        "Provide general HIV prevention education",
                        "Document risk assessment in medical record",
                        "Follow standard screening intervals if no risk factors"
                    ],
                    "specific_considerations": [],
                    "testing_frequency": "Follow standard CDC guidelines (typically annual if sexually active)",
                    "counseling_requirements": [
                        "Basic HIV prevention education",
                        "Information about transmission routes",
                        "Safe sex practices discussion"
                    ]
                },
                "prevention_guidance": {
                    "general_prevention": [
                        "Consistent condom use during sexual activity",
                        "Limiting number of sexual partners",
                        "Regular STD screening and treatment",
                        "Open communication with partners about HIV status"
                    ],
                    "specific_interventions": [],
                    "harm_reduction": [],
                    "prep_considerations": []
                },
                "score_components": [
                    {"component": "Age Group", "value": "26_32", "points": 6, "description": "Age group risk factor"},
                    {"component": "Gender", "value": "male", "points": 21, "description": "Gender-based risk factor"},
                    {"component": "Sexual Practices", "value": "vaginal_intercourse", "points": -10, "description": "Sexual behavior risk factor"},
                    {"component": "Injection Drug Use", "value": "no", "points": 0, "description": "Substance use risk factor"},
                    {"component": "Past HIV Testing", "value": "yes", "points": -4, "description": "Previous testing history"},
                    {"component": "Race/Ethnicity", "value": "white", "points": 0, "description": "Demographic risk factor"}
                ],
                "testing_guidance": {
                    "test_types": ["Standard HIV testing (laboratory-based or rapid)"],
                    "timing": "Routine testing schedule",
                    "result_management": [
                        "Standard result notification procedures",
                        "Basic prevention counseling with results"
                    ]
                },
                "follow_up_recommendations": {
                    "timing": "Annual or per standard guidelines",
                    "components": [
                        "Risk reassessment",
                        "Repeat testing if indicated",
                        "General prevention education"
                    ]
                },
                "prep_considerations": {
                    "candidacy": "PrEP generally not indicated based on current risk assessment",
                    "evaluation_needed": False,
                    "specific_factors": []
                }
            }
        }