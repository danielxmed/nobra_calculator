"""
Dutch Criteria for Familial Hypercholesterolemia (FH) Models

Request and response models for Dutch Criteria for Familial Hypercholesterolemia calculation.

References (Vancouver style):
1. The diagnosis and management of familial hypercholesterolaemia. Dutch Health Care 
   Insurance Board. 1999. Available from: https://www.lipidclinic.org/
2. Nordestgaard BG, Chapman MJ, Humphries SE, Ginsberg HN, Masana L, Descamps OS, et al. 
   Familial hypercholesterolaemia is underdiagnosed and undertreated in the general 
   population: guidance for clinicians to prevent coronary heart disease: consensus 
   statement of the European Atherosclerosis Society. Eur Heart J. 2013;34(45):3478-90a. 
   doi: 10.1093/eurheartj/eht273.
3. Cuchel M, Bruckert E, Ginsberg HN, Raal FJ, Santos RD, Hegele RA, et al. Homozygous 
   familial hypercholesterolaemia: new insights and guidance for clinicians to improve 
   detection and clinical management. A position paper from the Consensus Panel on 
   Familial Hypercholesterolaemia of the European Atherosclerosis Society. Eur Heart J. 
   2014;35(32):2146-57. doi: 10.1093/eurheartj/ehu274.

The Dutch Lipid Clinic Network (DLCN) Criteria for Familial Hypercholesterolemia 
is a comprehensive point-based diagnostic tool developed in 1999. It evaluates multiple 
clinical, biochemical, and genetic factors to provide graduated likelihood assessment 
(possible, probable, or definite FH) rather than binary diagnosis. This system is 
widely recommended by international guidelines and allows for systematic cascade 
screening of family members.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DutchCriteriaFamilialHypercholesterolemiaRequest(BaseModel):
    """
    Request model for Dutch Criteria for Familial Hypercholesterolemia
    
    The Dutch Lipid Clinic Network (DLCN) criteria uses a point-based system evaluating:
    
    LDL Cholesterol Levels (0-8 points):
    - ≥8.5 mmol/L (≥330 mg/dL): 8 points
    - 6.5-8.4 mmol/L (250-329 mg/dL): 5 points
    - 5.0-6.4 mmol/L (190-249 mg/dL): 3 points
    - 4.0-4.9 mmol/L (155-189 mg/dL): 1 point
    - <4.0 mmol/L (<155 mg/dL): 0 points
    
    Clinical Signs:
    - Tendon xanthomas (Achilles tendon or dorsum of hand): 6 points
    - Corneal arcus in patient <45 years: 4 points
    
    Family History:
    - LDL cholesterol >4.9 mmol/L (190 mg/dL) in adult first-degree relative 
      OR >4.0 mmol/L (155 mg/dL) in child/sibling <18 years: 1 point
    - Premature CHD in first-degree relative (men <55 years, women <60 years): 1 point
    
    Personal History:
    - Premature CHD (men <55 years, women <60 years): 2 points
    - Premature cerebral or peripheral vascular disease (men <55 years, women <60 years): 1 point
    
    Genetic Testing:
    - Functional mutation in LDLR, APOB, or PCSK9 gene: 8 points
    - No mutation found: 0 points
    - Not performed: 0 points
    
    Diagnostic Categories:
    - Definite FH (≥8 points): Requires immediate specialist referral and aggressive treatment
    - Probable FH (6-7 points): Strong indication for genetic testing and cascade screening
    - Possible FH (3-5 points): Consider genetic testing and family screening
    - Unlikely FH (0-2 points): Consider other causes of hypercholesterolemia
    
    Clinical Significance:
    - FH is an autosomal dominant disorder affecting 1 in 250-500 individuals
    - Early diagnosis and treatment prevent premature cardiovascular disease
    - Cascade screening of family members is mandatory for all diagnosed cases
    - High-intensity statin therapy is first-line treatment with LDL goal <1.8 mmol/L (70 mg/dL)
    - Combination therapy often required to achieve target levels
    
    Conversion Factors:
    - mmol/L to mg/dL: multiply by 38.67
    - mg/dL to mmol/L: divide by 38.67
    
    References (Vancouver style):
    1. The diagnosis and management of familial hypercholesterolaemia. Dutch Health Care 
       Insurance Board. 1999.
    2. Nordestgaard BG, Chapman MJ, Humphries SE, Ginsberg HN, Masana L, Descamps OS, et al. 
       Familial hypercholesterolaemia is underdiagnosed and undertreated in the general 
       population. Eur Heart J. 2013;34(45):3478-90a.
    3. Cuchel M, Bruckert E, Ginsberg HN, Raal FJ, Santos RD, Hegele RA, et al. Homozygous 
       familial hypercholesterolaemia: new insights and guidance for clinicians. Eur Heart J. 
       2014;35(32):2146-57.
    """
    
    ldl_cholesterol_mmol: float = Field(
        ...,
        description="LDL cholesterol level in mmol/L. Use conversion: mg/dL ÷ 38.67 = mmol/L. Scoring: ≥8.5 mmol/L = 8 points, 6.5-8.4 = 5 points, 5.0-6.4 = 3 points, 4.0-4.9 = 1 point",
        example=7.5,
        ge=0.0,
        le=30.0
    )
    
    tendon_xanthomas: Literal["yes", "no"] = Field(
        ...,
        description="Presence of tendon xanthomas on Achilles tendon or dorsum of hand (pathognomonic for FH). Scores 6 points if present",
        example="no"
    )
    
    corneal_arcus: Literal["yes", "no"] = Field(
        ...,
        description="Corneal arcus in patient younger than 45 years old (highly suggestive of FH in young patients). Scores 4 points if present",
        example="no"
    )
    
    family_history_ldl: Literal["yes", "no"] = Field(
        ...,
        description="Family history of LDL cholesterol >4.9 mmol/L (190 mg/dL) in adult first-degree relative OR >4.0 mmol/L (155 mg/dL) in child/sibling <18 years. Scores 1 point if present",
        example="yes"
    )
    
    family_history_chd: Literal["yes", "no"] = Field(
        ...,
        description="Family history of premature coronary heart disease in first-degree relative (men <55 years, women <60 years). Scores 1 point if present",
        example="yes"
    )
    
    personal_chd: Literal["yes", "no"] = Field(
        ...,
        description="Personal history of premature coronary heart disease (myocardial infarction, angina, revascularization in men <55 years, women <60 years). Scores 2 points if present",
        example="no"
    )
    
    personal_cvd: Literal["yes", "no"] = Field(
        ...,
        description="Personal history of premature cerebral or peripheral vascular disease (stroke, TIA, PAD in men <55 years, women <60 years). Scores 1 point if present",
        example="no"
    )
    
    dna_analysis: Literal["positive", "negative", "not_performed"] = Field(
        ...,
        description="DNA analysis results for functional mutations in LDLR, APOB, or PCSK9 genes. Positive mutation scores 8 points (definitive diagnosis)",
        example="not_performed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "ldl_cholesterol_mmol": 7.5,
                "tendon_xanthomas": "no",
                "corneal_arcus": "no",
                "family_history_ldl": "yes",
                "family_history_chd": "yes",
                "personal_chd": "no",
                "personal_cvd": "no",
                "dna_analysis": "not_performed"
            }
        }


class DutchCriteriaFamilialHypercholesterolemiaResponse(BaseModel):
    """
    Response model for Dutch Criteria for Familial Hypercholesterolemia
    
    The Dutch Lipid Clinic Network score provides graduated FH likelihood assessment:
    
    Definite FH (≥8 points):
    - Diagnosis: Familial hypercholesterolemia confirmed
    - Management: Immediate specialist referral required
    - Treatment: Aggressive combination therapy (statin + ezetimibe ± PCSK9 inhibitor)
    - Target: LDL <1.8 mmol/L (70 mg/dL) or <1.4 mmol/L (55 mg/dL) if very high risk
    - Screening: Mandatory cascade screening of all first-degree relatives
    - Follow-up: Specialist lipid clinic management with regular monitoring
    - Prognosis: High risk of premature CVD without treatment, excellent with early intervention
    
    Probable FH (6-7 points):
    - Diagnosis: High likelihood of familial hypercholesterolemia
    - Management: Strong indication for genetic testing and specialist referral
    - Treatment: High-intensity statin therapy as first-line
    - Target: LDL <1.8 mmol/L (70 mg/dL)
    - Screening: Cascade screening of first-degree relatives recommended
    - Follow-up: Consider specialist consultation if treatment goals not achieved
    - Additional: May require combination therapy to achieve targets
    
    Possible FH (3-5 points):
    - Diagnosis: Possible familial hypercholesterolemia
    - Management: Consider genetic testing if available and appropriate
    - Treatment: High-intensity statin therapy initiated
    - Target: Standard cardiovascular risk-based targets initially
    - Screening: Screen first-degree relatives for elevated cholesterol
    - Follow-up: Monitor response to therapy and reassess based on family screening
    - Considerations: May represent polygenic hypercholesterolemia
    
    Unlikely FH (0-2 points):
    - Diagnosis: Familial hypercholesterolemia unlikely
    - Management: Investigate secondary causes of hypercholesterolemia
    - Secondary causes: Hypothyroidism, diabetes, nephrotic syndrome, medications
    - Treatment: Standard cardiovascular risk-based approach
    - Screening: Routine family history and standard risk assessment
    - Follow-up: Standard lipid monitoring and cardiovascular risk management
    
    Treatment Considerations:
    - First-line: High-intensity statin (atorvastatin 40-80mg or rosuvastatin 20-40mg)
    - Second-line: Add ezetimibe 10mg if statin alone insufficient
    - Third-line: PCSK9 inhibitor if combination therapy inadequate
    - Lifestyle: Mediterranean diet, regular exercise, smoking cessation
    - Monitoring: Lipid profile every 6-12 weeks until stable, then annually
    
    Cascade Screening Protocol:
    - Screen all first-degree relatives (parents, siblings, children)
    - Children should be screened from age 5-10 years
    - Use age-appropriate LDL thresholds for diagnosis
    - Genetic testing facilitates family screening when mutation identified
    - Consider screening of extended family if multiple affected relatives
    
    Special Populations:
    - Pregnancy: Discontinue statins, consider bile acid sequestrants
    - Pediatrics: Lifestyle intervention first, statins from age 8-10 if severe
    - Elderly: Consider comorbidities and life expectancy in treatment decisions
    
    Reference: Dutch Health Care Insurance Board. 1999.
    """
    
    result: int = Field(
        ...,
        description="Dutch Lipid Clinic Network score (0-15+ points)",
        example=7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on FH likelihood",
        example="Probable familial hypercholesterolemia (Dutch score = 7). Strong indication for genetic testing and specialist referral. Initiate high-intensity statin therapy with goal LDL <1.8 mmol/L (70 mg/dL). Mandatory cascade screening of first-degree relatives. Consider additional lipid-lowering therapy if statin alone insufficient."
    )
    
    stage: str = Field(
        ...,
        description="FH likelihood category (Unlikely FH, Possible FH, Probable FH, Definite FH)",
        example="Probable FH"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the FH likelihood level",
        example="Probable familial hypercholesterolemia"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "Probable familial hypercholesterolemia (Dutch score = 7). Strong indication for genetic testing and specialist referral. Initiate high-intensity statin therapy with goal LDL <1.8 mmol/L (70 mg/dL). Mandatory cascade screening of first-degree relatives. Consider additional lipid-lowering therapy if statin alone insufficient.",
                "stage": "Probable FH",
                "stage_description": "Probable familial hypercholesterolemia"
            }
        }