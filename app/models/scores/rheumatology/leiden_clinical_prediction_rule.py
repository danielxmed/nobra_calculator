"""
Leiden Clinical Prediction Rule for Undifferentiated Arthritis Models

Request and response models for the Leiden Clinical Prediction Rule calculation.

References (Vancouver style):
1. van der Helm-van Mil AHM, le Cessie S, van Dongen H, Breedveld FC, Toes REM, 
   Huizinga TWJ. A prediction rule for disease outcome in patients with recent-onset 
   undifferentiated arthritis: how to guide individual treatment decisions. Arthritis 
   Rheum. 2007 Feb;56(2):433-40. doi: 10.1002/art.22401.
2. Kuriya B, Cheng CK, Chen HM, Bykerk VP. Validation of a prediction rule for 
   development of rheumatoid arthritis in patients with early undifferentiated arthritis. 
   Ann Rheum Dis. 2009 Sep;68(9):1482-5. doi: 10.1136/ard.2008.098012.
3. Tamai M, Kawakami A, Uetani M, Fukushima A, Arima K, Iwanaga N, et al. A prediction 
   rule for disease outcome in patients with undifferentiated arthritis using magnetic 
   resonance imaging of the wrists and finger joints and serologic autoantibodies. 
   Arthritis Rheum. 2009 Oct 15;61(10):1324-31. doi: 10.1002/art.24595.

The Leiden Clinical Prediction Rule was developed to help clinicians predict which patients 
with recent-onset undifferentiated arthritis will progress to rheumatoid arthritis within 
one year. This evidence-based tool combines clinical features, laboratory markers, and 
serological tests to provide risk stratification that guides early treatment decisions.

Clinical Background:
Undifferentiated arthritis refers to inflammatory joint disease that does not fulfill 
classification criteria for any specific rheumatologic condition. Approximately 40-60% 
of patients with undifferentiated arthritis will eventually develop rheumatoid arthritis 
or another defined arthropathy, while others may achieve spontaneous remission.

Early identification of patients likely to progress to rheumatoid arthritis is crucial 
because early intervention with disease-modifying antirheumatic drugs (DMARDs) can prevent 
joint damage, preserve function, and improve long-term outcomes. Conversely, avoiding 
unnecessary treatment in patients who will achieve remission prevents potential adverse 
effects and reduces healthcare costs.

Predictive Variables:
The Leiden rule incorporates nine clinical and laboratory variables:

1. Age: Continuously weighted (age × 0.02), recognizing higher progression risk with advancing age
2. Sex: Female patients have higher risk (1 point vs 0 for males)
3. Joint Distribution: Pattern of affected joints, with small joints of hands/feet and 
   bilateral involvement carrying higher risk
4. Symmetric Distribution: Bilateral symmetric involvement (0.5 points) suggests autoimmune etiology
5. Morning Stiffness: Duration reflects inflammatory burden, with ≥60 minutes carrying highest risk
6. Tender Joint Count: Reflects disease activity and inflammation extent (0-68 joint assessment)
7. Swollen Joint Count: Objective measure of active synovitis (0-66 joint assessment)
8. C-Reactive Protein: Acute-phase reactant indicating systemic inflammation
9. Rheumatoid Factor: Classical autoantibody associated with RA (1 point if positive)
10. Anti-CCP Antibodies: Highly specific for RA, strongest single predictor (2 points if positive)

Risk Stratification:
- Low Risk (≤6.0 points): <20% progression rate, conservative management appropriate
- Indeterminate Risk (6.01-7.99 points): 20-60% progression rate, individualized decision-making
- High Risk (≥8.0 points): >60% progression rate, early DMARD therapy strongly recommended

Clinical Validation:
The rule has been validated across multiple populations and healthcare settings, demonstrating 
good discriminative ability (AUC 0.80-0.85) and clinical utility. High specificity ensures 
that most patients classified as high-risk will indeed progress to RA, while maintaining 
reasonable sensitivity for identifying at-risk patients.

Implementation Considerations:
- Most accurate when applied within 6 months of symptom onset
- Should complement, not replace, comprehensive rheumatological assessment
- Serial assessments may be valuable for patients in intermediate risk category
- Cultural and population differences may affect performance
- Consider alongside patient preferences and comorbidities when making treatment decisions

Treatment Implications:
- Low Risk: Watchful waiting with regular monitoring (3-6 month intervals)
- Indeterminate Risk: Close monitoring with potential early intervention based on clinical judgment
- High Risk: Strong consideration for early DMARD therapy, preferably methotrexate
- All patients benefit from patient education, lifestyle counseling, and rheumatology consultation
"""

from pydantic import BaseModel, Field
from typing import Literal


class LeidenClinicalPredictionRuleRequest(BaseModel):
    """
    Request model for Leiden Clinical Prediction Rule for Undifferentiated Arthritis
    
    The Leiden Clinical Prediction Rule predicts the likelihood of progression from 
    undifferentiated arthritis to rheumatoid arthritis within one year using nine 
    clinical and laboratory variables. This validated tool helps guide early treatment 
    decisions with disease-modifying antirheumatic drugs (DMARDs).
    
    Clinical Variables:
    
    Age: Calculated as age in years × 0.02, reflecting increased progression risk with 
    advancing age due to immunosenescence and cumulative inflammatory exposure.
    
    Sex: Female patients have approximately 2-3 times higher risk of developing RA, 
    likely due to hormonal influences on immune system function and autoantibody production.
    
    Joint Distribution Patterns:
    - Small joints (hands/feet): Classic RA pattern involving MCPs, PIPs, wrists, MTPs
    - Upper extremities only: Shoulder, elbow, wrist involvement without lower extremity disease
    - Upper and lower extremities: Polyarticular involvement suggesting systemic disease
    - Other: Atypical patterns less suggestive of RA progression
    
    Symmetric Distribution: Bilateral symmetric joint involvement is hallmark of autoimmune 
    arthritis, distinguishing it from mechanical or crystal arthropathies.
    
    Morning Stiffness Duration: Reflects inflammatory burden and cytokine activity:
    - <30 minutes: Minimal inflammatory component
    - 30-59 minutes: Moderate inflammation
    - ≥60 minutes: Significant inflammatory burden typical of RA
    
    Joint Counts: Standardized 68/66 joint assessment for tender/swollen joints respectively:
    - Tender joints reflect pain and inflammation
    - Swollen joints indicate active synovitis and disease activity
    - Higher counts suggest more extensive disease requiring aggressive treatment
    
    C-Reactive Protein: Acute-phase reactant produced by liver in response to IL-6:
    - <5 mg/L: Normal, minimal systemic inflammation
    - 5-50 mg/L: Mild to moderate elevation
    - ≥51 mg/L: Significant systemic inflammation
    
    Rheumatoid Factor: IgM antibody against Fc portion of IgG, positive in 70-80% of RA patients.
    Associated with more aggressive disease, extra-articular manifestations, and joint damage.
    
    Anti-CCP Antibodies: Highly specific autoantibodies (>95% specificity) targeting 
    citrullinated proteins. Strongest single predictor of RA development and aggressive disease course.
    
    Clinical Assessment Guidelines:
    - Apply to adults with recent-onset undifferentiated arthritis (<2 years duration)
    - Most accurate within 6 months of symptom onset
    - Requires comprehensive joint examination by trained assessor
    - Laboratory tests should be performed using standardized methods
    - Consider serial assessments for monitoring disease evolution
    
    Treatment Decision Framework:
    - Low risk (≤6.0): Conservative management with monitoring
    - Indeterminate risk (6.01-7.99): Individualized decision-making
    - High risk (≥8.0): Strong consideration for early DMARD therapy
    
    Quality Assurance:
    - Ensure accurate joint count assessment using standardized technique
    - Verify laboratory result validity and normal ranges
    - Document symptom duration and onset pattern
    - Consider patient factors affecting interpretation (comorbidities, medications)
    
    References (Vancouver style):
    1. van der Helm-van Mil AHM, le Cessie S, van Dongen H, Breedveld FC, Toes REM, 
    Huizinga TWJ. A prediction rule for disease outcome in patients with recent-onset 
    undifferentiated arthritis: how to guide individual treatment decisions. Arthritis 
    Rheum. 2007 Feb;56(2):433-40.
    2. Kuriya B, Cheng CK, Chen HM, Bykerk VP. Validation of a prediction rule for 
    development of rheumatoid arthritis in patients with early undifferentiated arthritis. 
    Ann Rheum Dis. 2009 Sep;68(9):1482-5.
    """
    
    age_years: int = Field(
        ...,
        description="Patient age in years. Age is weighted continuously in the formula (age × 0.02) as older patients "
                   "have higher risk of progressing to rheumatoid arthritis. The relationship reflects cumulative "
                   "exposure to environmental triggers and age-related immune system changes.",
        ge=18,
        le=120,
        example=45
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Female patients receive 1 point (vs 0 for males) due to approximately "
                   "2-3 times higher risk of developing rheumatoid arthritis. This increased risk is attributed to "
                   "hormonal influences on immune function, particularly estrogen effects on B-cell activation and "
                   "autoantibody production.",
        example="female"
    )
    
    joint_distribution: Literal["other", "small_hands_feet", "upper_extremities_only", "upper_and_lower_extremities"] = Field(
        ...,
        description="Pattern of affected joint distribution. 'small_hands_feet' (0.5 pts): classic RA pattern "
                   "involving metacarpophalangeal, proximal interphalangeal, wrist, and metatarsophalangeal joints. "
                   "'upper_extremities_only' (1 pt): shoulder, elbow, wrist involvement. "
                   "'upper_and_lower_extremities' (1.5 pts): polyarticular disease suggesting systemic involvement. "
                   "'other' (0 pts): atypical patterns less suggestive of RA.",
        example="small_hands_feet"
    )
    
    symmetric_distribution: Literal["yes", "no"] = Field(
        ...,
        description="Whether joint involvement follows a symmetric (bilateral) pattern. Symmetric distribution "
                   "(0.5 pts if yes) is characteristic of autoimmune arthritis and helps distinguish from "
                   "mechanical, crystal, or infectious arthropathies which typically show asymmetric patterns.",
        example="yes"
    )
    
    morning_stiffness_duration: Literal["less_than_30_min", "30_to_59_min", "60_min_or_more"] = Field(
        ...,
        description="Duration of morning joint stiffness experienced by the patient. Reflects inflammatory burden "
                   "and cytokine activity: <30 minutes (0 pts) suggests minimal inflammation; 30-59 minutes (0.5 pts) "
                   "indicates moderate inflammation; ≥60 minutes (1 pt) suggests significant inflammatory burden "
                   "typical of rheumatoid arthritis.",
        example="60_min_or_more"
    )
    
    tender_joints_count: int = Field(
        ...,
        description="Number of tender joints on standardized 68-joint assessment. Includes bilateral assessment of "
                   "shoulders, elbows, wrists, MCPs, PIPs, hips, knees, ankles, and MTPs. Tenderness reflects pain "
                   "and inflammation. Scoring: <4 joints (0 pts), 4-10 joints (0.5 pts), ≥11 joints (1 pt). "
                   "Higher counts suggest more extensive disease.",
        ge=0,
        le=68,
        example=8
    )
    
    swollen_joints_count: int = Field(
        ...,
        description="Number of swollen joints on standardized 66-joint assessment (excludes hips due to deep location). "
                   "Swelling indicates active synovitis and is more objective than tenderness. Scoring: <4 joints (0 pts), "
                   "4-10 joints (0.5 pts), ≥11 joints (1 pt). Swollen joint count is strong predictor of disease "
                   "progression and treatment response.",
        ge=0,
        le=66,
        example=6
    )
    
    c_reactive_protein: float = Field(
        ...,
        description="C-reactive protein level in mg/L from fasting blood sample. Acute-phase reactant produced by "
                   "liver in response to IL-6 and other inflammatory cytokines. Scoring: <5 mg/L (0 pts) normal range; "
                   "5-50 mg/L (0.5 pts) mild to moderate elevation; ≥51 mg/L (1.5 pts) significant systemic inflammation. "
                   "Elevated CRP indicates active inflammatory process.",
        ge=0.0,
        le=500.0,
        example=12.5
    )
    
    rheumatoid_factor: Literal["positive", "negative"] = Field(
        ...,
        description="Rheumatoid factor status (IgM antibody against Fc portion of IgG). Positive RF (1 pt) found in "
                   "70-80% of RA patients and associated with more aggressive disease, extra-articular manifestations, "
                   "and joint damage. However, RF can be positive in other conditions and healthy individuals "
                   "(5-10% of population), so must be interpreted in clinical context.",
        example="positive"
    )
    
    anti_ccp_antibodies: Literal["positive", "negative"] = Field(
        ...,
        description="Anti-cyclic citrullinated peptide (anti-CCP) antibody status. Highly specific for rheumatoid "
                   "arthritis (>95% specificity) and strongest single predictor of RA development. Positive anti-CCP "
                   "(2 pts) indicates citrullination process and immune response against modified self-antigens. "
                   "Associated with more aggressive disease course and joint destruction.",
        example="negative"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_years": 45,
                "sex": "female",
                "joint_distribution": "small_hands_feet",
                "symmetric_distribution": "yes",
                "morning_stiffness_duration": "60_min_or_more",
                "tender_joints_count": 8,
                "swollen_joints_count": 6,
                "c_reactive_protein": 12.5,
                "rheumatoid_factor": "positive",
                "anti_ccp_antibodies": "negative"
            }
        }


class LeidenClinicalPredictionRuleResponse(BaseModel):
    """
    Response model for Leiden Clinical Prediction Rule for Undifferentiated Arthritis
    
    Provides calculated risk score with evidence-based interpretation and clinical 
    recommendations for patients with undifferentiated arthritis. The score predicts 
    likelihood of progression to rheumatoid arthritis within one year and guides 
    early treatment decisions with disease-modifying antirheumatic drugs (DMARDs).
    
    Risk Stratification and Clinical Implications:
    
    Low Risk (≤6.0 points):
    - Progression rate: <20% within one year
    - Management: Conservative approach with watchful waiting
    - Monitoring: Regular follow-up every 3-6 months
    - Intervention threshold: Symptom worsening or new features
    - Prognosis: High likelihood of spontaneous remission or stable disease
    
    Indeterminate Risk (6.01-7.99 points):
    - Progression rate: 20-60% within one year
    - Management: Individualized decision-making based on clinical factors
    - Monitoring: Close surveillance with serial assessments
    - Considerations: Patient preferences, comorbidities, symptom severity
    - Options: Early intervention vs. continued monitoring with low-threshold for treatment
    
    High Risk (≥8.0 points):
    - Progression rate: >60% within one year
    - Management: Strong consideration for early DMARD therapy
    - Timing: Preferably within 3-6 months of symptom onset
    - First-line therapy: Methotrexate (unless contraindicated)
    - Monitoring: Regular assessment for treatment response and adverse effects
    
    Treatment Recommendations by Risk Category:
    
    Early Intervention Benefits:
    - Prevention of joint damage and erosions
    - Preservation of functional capacity
    - Improved long-term outcomes and quality of life
    - Reduced healthcare utilization and costs
    - Lower risk of extra-articular manifestations
    
    DMARD Therapy Considerations:
    - Methotrexate: First-line agent, well-established efficacy and safety profile
    - Sulfasalazine: Alternative for methotrexate-intolerant patients
    - Hydroxychloroquine: Milder option for low-moderate disease activity
    - Combination therapy: May be considered for high-risk patients
    - Biologics: Reserved for established RA with inadequate conventional DMARD response
    
    Monitoring Parameters:
    - Disease activity: Joint counts, patient global assessment, inflammatory markers
    - Functional status: Health Assessment Questionnaire (HAQ)
    - Laboratory monitoring: Complete blood count, liver function, creatinine
    - Radiographic assessment: Baseline and annual imaging for established disease
    - Patient-reported outcomes: Pain, fatigue, morning stiffness duration
    
    Shared Decision-Making Elements:
    - Patient understanding of prognosis and treatment options
    - Discussion of benefits and risks of early intervention
    - Consideration of patient values and preferences
    - Assessment of treatment adherence likelihood
    - Planning for regular monitoring and follow-up
    
    Quality Measures:
    - Time from symptom onset to rheumatology consultation (<3 months preferred)
    - Appropriate use of prediction rule in eligible patients
    - Treatment initiation within recommended timeframes for high-risk patients
    - Regular monitoring and dose optimization
    - Patient education and engagement in care
    
    Reference: van der Helm-van Mil AHM, et al. Arthritis Rheum. 2007;56(2):433-40.
    """
    
    result: float = Field(
        ...,
        description="Leiden Clinical Prediction Rule score calculated from clinical and laboratory variables (range: approximately 0-13 points)",
        example=6.4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the prediction rule score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk assessment, progression likelihood, "
                   "evidence-based management recommendations, and treatment decision guidance",
        example="Leiden Clinical Prediction Rule score: 6.4 points. Risk category: Indeterminate Risk. Intermediate likelihood of progression to rheumatoid arthritis. Clinical judgment and additional factors should guide treatment decisions. Consider close monitoring with serial assessments. Early intervention may be considered depending on patient characteristics, symptom severity, and clinical presentation. Rheumatology consultation recommended. Key contributing factors include: older age, female sex, typical joint distribution pattern, symmetric joint involvement, prolonged morning stiffness, positive rheumatoid factor. This prediction rule is designed for adults with recent-onset undifferentiated arthritis (symptom duration typically <6 months) to guide early treatment decisions. The tool should be used in conjunction with comprehensive clinical assessment and is not intended to replace rheumatological evaluation."
    )
    
    stage: str = Field(
        ...,
        description="Risk category for progression to rheumatoid arthritis (Low Risk, Indeterminate Risk, High Risk)",
        example="Indeterminate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Indeterminate risk of progression to rheumatoid arthritis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6.4,
                "unit": "points",
                "interpretation": "Leiden Clinical Prediction Rule score: 6.4 points. Risk category: Indeterminate Risk. Intermediate likelihood of progression to rheumatoid arthritis. Clinical judgment and additional factors should guide treatment decisions. Consider close monitoring with serial assessments. Early intervention may be considered depending on patient characteristics, symptom severity, and clinical presentation. Rheumatology consultation recommended. Key contributing factors include: older age, female sex, typical joint distribution pattern, symmetric joint involvement, prolonged morning stiffness, positive rheumatoid factor. This prediction rule is designed for adults with recent-onset undifferentiated arthritis (symptom duration typically <6 months) to guide early treatment decisions. The tool should be used in conjunction with comprehensive clinical assessment and is not intended to replace rheumatological evaluation.",
                "stage": "Indeterminate Risk",
                "stage_description": "Indeterminate risk of progression to rheumatoid arthritis"
            }
        }