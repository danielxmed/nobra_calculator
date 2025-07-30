"""
Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis Models

Request and response models for CDAI rheumatoid arthritis disease activity assessment.

References (Vancouver style):
1. Aletaha D, Nell VP, Stamm T, Uffmann M, Pflugbeil S, Machold K, Smolen JS. Acute phase 
   reactants add little to composite disease activity indices for rheumatoid arthritis: 
   validation of a clinical activity score. Arthritis Res Ther. 2005;7(4):R796-806.
2. Smolen JS, Breedveld FC, Schiff MH, Kalden JR, Emery P, Eberl G, van Riel PL, Tugwell P. 
   A simplified disease activity index for rheumatoid arthritis for use in clinical practice. 
   Rheumatology (Oxford). 2003;42(2):244-57.
3. Aletaha D, Smolen JS. The Simplified Disease Activity Index (SDAI) and the Clinical 
   Disease Activity Index (CDAI): a review of their usefulness and validity in rheumatoid 
   arthritis. Clin Exp Rheumatol. 2005;23(5 Suppl 39):S100-8.

The Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis is a validated 
composite measure designed to assess disease activity in patients with rheumatoid 
arthritis using only clinical parameters, without requiring laboratory tests. This 
makes the CDAI particularly practical for routine clinical use, as it allows 
immediate treatment decisions to be made based entirely on clinical criteria.

Clinical Background and Development:

Rheumatoid arthritis (RA) is a chronic inflammatory autoimmune disease that primarily 
affects the synovial joints, causing pain, swelling, stiffness, and progressive joint 
destruction if inadequately treated. Accurate assessment of disease activity is 
essential for optimal management, as it guides treatment decisions and helps monitor 
therapeutic response.

The CDAI was developed as a simplification of the Simple Disease Activity Index (SDAI), 
removing the need for acute phase reactant measurement (C-reactive protein or 
erythrocyte sedimentation rate). This innovation makes the CDAI immediately available 
at the point of care, eliminating delays associated with laboratory testing.

Composite Disease Activity Assessment:

The CDAI integrates four key components of rheumatoid arthritis disease activity:

1. Tender Joint Count (28-joint assessment):
   The tender joint count evaluates subjective joint involvement from the patient's 
   perspective, reflecting pain and discomfort associated with joint inflammation. 
   The 28-joint count includes bilateral assessment of shoulders, elbows, wrists, 
   metacarpophalangeal (MCP) joints 1-5, proximal interphalangeal (PIP) joints 1-5, 
   and knees.

2. Swollen Joint Count (28-joint assessment):
   The swollen joint count provides an objective measure of inflammatory joint 
   involvement, assessed through palpation and visual inspection. Swelling indicates 
   active synovial inflammation and is a key target for anti-inflammatory therapy.

3. Patient Global Assessment:
   This component captures the patient's overall perspective on their disease impact, 
   using a 0-10 visual analog scale where 0 represents "very well" and 10 represents 
   "very poor." This patient-reported outcome measure ensures that the patient's 
   experience is incorporated into disease activity assessment.

4. Provider Global Assessment:
   The healthcare provider's overall assessment of disease activity using the same 
   0-10 scale reflects clinical expertise and objective evaluation of the patient's 
   condition. This component integrates the clinician's interpretation of all 
   available clinical information.

Scoring System and Interpretation:

The CDAI employs a simple additive formula:
CDAI = Tender Joint Count + Swollen Joint Count + Patient Global Assessment + Provider Global Assessment

The resulting score ranges from 0 to 76 points and is categorized into four 
disease activity levels:

Remission (CDAI ≤ 2.8):
- Represents minimal or absent disease activity
- Associated with excellent long-term outcomes
- Primary treatment target for all patients
- Indicates effective suppression of inflammatory activity

Low Disease Activity (CDAI > 2.8 to ≤ 10):
- Represents acceptable disease control
- Associated with reduced risk of joint damage progression
- Secondary treatment target if remission not achievable
- Indicates good therapeutic response

Moderate Disease Activity (CDAI > 10 to ≤ 22):
- Represents suboptimal disease control
- Associated with ongoing inflammatory activity
- Indicates need for treatment intensification
- Risk for progressive joint damage if sustained

High Disease Activity (CDAI > 22):
- Represents poor disease control
- Associated with significant inflammatory burden
- Urgent need for aggressive treatment modification
- High risk for rapid joint damage progression

Clinical Applications and Advantages:

Immediate Availability:
The CDAI's greatest advantage is its immediate availability at the point of care. 
Unlike other disease activity measures that require laboratory results, the CDAI 
can be calculated during the clinical encounter, enabling real-time treatment 
decision-making.

Practical Implementation:
The CDAI is more practical than complex indices like the DAS-28, which requires 
mathematical calculations or computer assistance. The simple additive formula 
makes mental calculation possible, facilitating routine clinical use.

Cost-Effectiveness:
By eliminating the need for laboratory testing, the CDAI reduces healthcare costs 
while maintaining clinical validity. This is particularly valuable in resource-
limited settings or for frequent monitoring.

Patient Engagement:
The inclusion of patient global assessment ensures that the patient's perspective 
is integral to disease activity measurement. This promotes shared decision-making 
and patient-centered care.

Treatment Monitoring:
The CDAI provides a standardized approach to monitoring treatment response, 
facilitating objective assessment of therapeutic interventions and supporting 
evidence-based treatment modifications.

Validation and Clinical Evidence:

The CDAI has been extensively validated in clinical practice and research settings. 
Studies have demonstrated moderate to good correlation with the DAS-28 (Kappa = 0.533), 
confirming its validity as a disease activity measure. The CDAI has been widely 
adopted in clinical practice and is recommended by international rheumatology 
organizations for routine RA monitoring.

Treat-to-Target Strategy Integration:

The CDAI plays a crucial role in treat-to-target strategies for rheumatoid arthritis 
management. These evidence-based approaches recommend:

- Primary target: Remission (CDAI ≤ 2.8)
- Alternative target: Low disease activity (CDAI ≤ 10) if remission not achievable
- Regular monitoring: Every 1-3 months depending on disease activity level
- Treatment modification: If target not achieved within 3-6 months

Implementation Considerations:

Joint Assessment Standardization:
Proper implementation requires standardized joint examination techniques and 
consistent application of the 28-joint count methodology. Healthcare providers 
should be trained in systematic joint assessment to ensure reliability.

Global Assessment Consistency:
Both patient and provider global assessments should be performed using validated 
visual analog scales with clear anchoring statements (0 = very well, 10 = very poor). 
Consistency in scale administration is essential for reliable results.

Clinical Context Integration:
While the CDAI provides valuable objective assessment, it should be interpreted 
within the broader clinical context, considering factors such as comorbidities, 
medication side effects, and patient preferences.

Longitudinal Monitoring:
The CDAI is most valuable when used for longitudinal monitoring rather than 
single-point assessment. Trends over time provide more meaningful information 
about treatment response and disease progression.

Limitations and Considerations:

The CDAI has several important limitations that clinicians should consider:

- Does not include acute phase reactants, which may provide additional information 
  about systemic inflammation
- Joint assessment requires clinical expertise and may have inter-observer variability
- Global assessments are subjective and may be influenced by factors beyond 
  arthritis activity
- May not capture all aspects of disease impact, such as fatigue or functional disability

Future Directions:

Ongoing research continues to refine the application of CDAI in rheumatoid arthritis 
management, including:

- Integration with patient-reported outcome measures
- Use in telemedicine and remote monitoring applications
- Incorporation into electronic health record systems
- Validation in diverse patient populations

The Clinical Disease Activity Index represents a significant advancement in 
rheumatoid arthritis care, providing a practical, validated tool for disease 
activity assessment that supports evidence-based treatment decisions and 
improved patient outcomes. When properly implemented with appropriate training 
and clinical context, the CDAI significantly enhances the quality of 
rheumatoid arthritis management in routine clinical practice.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CdaiRheumatoidArthritisRequest(BaseModel):
    """
    Request model for Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis
    
    The CDAI is a validated composite measure for assessing rheumatoid arthritis disease 
    activity using only clinical parameters, without requiring laboratory tests. This 
    practical tool enables immediate treatment decision-making at the point of care.
    
    Assessment Component Guidelines:
    
    28-Joint Count Assessment:
    The CDAI uses the standardized 28-joint count, which includes bilateral assessment 
    of the following joints:
    - Shoulders (glenohumeral joints)
    - Elbows
    - Wrists (radiocarpal/midcarpal joints)
    - Metacarpophalangeal (MCP) joints 1-5
    - Proximal interphalangeal (PIP) joints 1-5
    - Knees
    
    Tender Joint Count (0-28 joints):
    Assessment of joint tenderness reflects the patient's subjective experience of 
    pain and discomfort associated with joint inflammation. Tenderness is assessed 
    by applying gentle pressure to the joint and asking the patient about pain or 
    discomfort. A joint is considered tender if the patient reports pain upon 
    palpation or movement.
    
    Clinical Assessment Technique:
    - Apply consistent, gentle pressure during palpation
    - Assess both active and passive range of motion
    - Document patient's verbal and non-verbal pain responses
    - Consider functional limitations during joint assessment
    - Ensure patient comfort and explain the examination process
    
    Swollen Joint Count (0-28 joints):
    Assessment of joint swelling provides an objective measure of inflammatory 
    joint involvement. Swelling indicates active synovial inflammation and is 
    evaluated through both palpation and visual inspection.
    
    Clinical Assessment Technique:
    - Visually inspect joints for obvious swelling or deformity
    - Palpate for synovial thickening and joint effusion
    - Compare bilateral joints for asymmetry
    - Distinguish between soft tissue swelling and bony enlargement
    - Document presence of warmth or erythema
    
    Patient Global Assessment (0-10 scale):
    This patient-reported outcome measure captures the patient's overall perspective 
    on their disease impact and current well-being. The assessment uses a visual 
    analog scale where patients rate their overall condition.
    
    Scale Anchors:
    - 0.0: "Very well" - Patient feels excellent with minimal disease impact
    - 5.0: "Moderate" - Noticeable disease impact but manageable
    - 10.0: "Very poor" - Severe disease impact significantly affecting daily life
    
    Assessment Instructions for Patients:
    "Considering all the ways your arthritis affects you, how would you rate how 
    you are doing today on a scale from 0 to 10, where 0 is very well and 10 is very poor?"
    
    Provider Global Assessment (0-10 scale):
    The healthcare provider's overall assessment of disease activity integrates 
    clinical expertise with objective evaluation of the patient's condition. This 
    assessment reflects the clinician's interpretation of all available clinical 
    information.
    
    Scale Anchors:
    - 0.0: "Very well" - Minimal or no evidence of active disease
    - 5.0: "Moderate" - Noticeable disease activity requiring attention
    - 10.0: "Very poor" - Severe disease activity requiring urgent intervention
    
    Clinical Considerations for Provider Assessment:
    - Integrate joint examination findings with patient symptoms
    - Consider functional limitations and disability
    - Assess response to current therapy
    - Evaluate disease progression or improvement
    - Account for extra-articular manifestations if present
    
    Clinical Assessment Context:
    
    Timing and Frequency:
    - Assess at each routine rheumatology visit
    - More frequent assessment during active treatment changes
    - Monitor response to therapy every 1-3 months depending on disease activity
    - Use for treatment decision-making and target achievement
    
    Standardization Requirements:
    - Use consistent joint examination techniques
    - Ensure proper training in 28-joint count methodology
    - Maintain standardized visual analog scale administration
    - Document assessment conditions and patient factors
    
    Integration with Clinical Care:
    - Use CDAI results to guide treat-to-target strategies
    - Combine with patient preferences for shared decision-making
    - Consider in context of comorbidities and treatment tolerability
    - Monitor trends over time rather than single-point assessments
    
    References (Vancouver style):
    1. Aletaha D, Nell VP, Stamm T, Uffmann M, Pflugbeil S, Machold K, Smolen JS. 
    Acute phase reactants add little to composite disease activity indices for 
    rheumatoid arthritis: validation of a clinical activity score. Arthritis Res Ther. 
    2005;7(4):R796-806.
    2. Smolen JS, Breedveld FC, Schiff MH, Kalden JR, Emery P, Eberl G, van Riel PL, 
    Tugwell P. A simplified disease activity index for rheumatoid arthritis for use 
    in clinical practice. Rheumatology (Oxford). 2003;42(2):244-57.
    """
    
    tender_joint_count: int = Field(
        ...,
        ge=0,
        le=28,
        description="Number of tender joints on 28-joint count examination. Reflects subjective pain and inflammation from patient perspective",
        example=8
    )
    
    swollen_joint_count: int = Field(
        ...,
        ge=0,
        le=28,
        description="Number of swollen joints on 28-joint count examination. Objective measure of inflammatory joint involvement",
        example=5
    )
    
    patient_global_activity: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Patient global assessment of disease activity (0-10 scale). 0=very well, 10=very poor. Patient's overall perspective on disease impact",
        example=6.5
    )
    
    provider_global_activity: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Provider global assessment of disease activity (0-10 scale). 0=very well, 10=very poor. Clinician's overall assessment of disease activity",
        example=5.8
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tender_joint_count": 8,
                "swollen_joint_count": 5,
                "patient_global_activity": 6.5,
                "provider_global_activity": 5.8
            }
        }


class CdaiRheumatoidArthritisResponse(BaseModel):
    """
    Response model for Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis
    
    Provides comprehensive rheumatoid arthritis disease activity assessment with 
    evidence-based treatment recommendations and clinical guidance. The CDAI response 
    enables immediate clinical decision-making and supports treat-to-target strategies 
    for optimal RA management.
    
    Disease Activity Categories and Clinical Management:
    
    Remission (CDAI ≤ 2.8 points):
    
    Clinical Characteristics:
    - Minimal or absent disease activity
    - Excellent suppression of inflammatory activity
    - Associated with best long-term outcomes
    - Primary treatment target for all patients
    - Indicates effective disease control
    
    Management Approach:
    - Maintain current therapy - excellent disease control achieved
    - Monitor for sustained remission over time
    - Consider gradual dose tapering if sustained remission >6 months
    - Continue regular monitoring to ensure remission maintenance
    - Focus on preventing disease flares and maintaining quality of life
    
    Monitoring Requirements:
    - Assess every 3-6 months to monitor for sustained remission
    - Watch for early signs of disease flare
    - Maintain patient education about symptoms to report
    - Consider dose optimization while maintaining remission
    
    Long-term Prognosis:
    - Excellent long-term outcomes with sustained remission
    - Minimal risk of progressive joint damage
    - Optimal functional outcomes and quality of life
    - Potential for sustained drug-free remission in some patients
    
    Low Disease Activity (CDAI > 2.8 to ≤ 10 points):
    
    Clinical Characteristics:
    - Acceptable disease control with minimal inflammatory activity
    - Good therapeutic response to current treatment
    - Associated with reduced risk of joint damage progression
    - Secondary treatment target if remission not immediately achievable
    - Represents significant improvement from higher activity states
    
    Management Approach:
    - Continue current therapy - good disease control maintained
    - Aim for achieving remission if clinically appropriate
    - Consider maintaining current dose or careful treatment optimization
    - Monitor closely for opportunities to advance to remission
    - Assess for barriers preventing achievement of remission
    
    Monitoring Requirements:
    - Assess every 2-3 months to ensure sustained low disease activity
    - Monitor for potential advancement to remission
    - Evaluate treatment response and optimize therapy
    - Maintain regular assessment of treatment goals
    
    Long-term Prognosis:
    - Good long-term outcomes with low disease activity
    - Reduced risk of progressive joint damage
    - Acceptable functional outcomes and quality of life
    - Lower risk of cardiovascular and other comorbidities
    
    Moderate Disease Activity (CDAI > 10 to ≤ 22 points):
    
    Clinical Characteristics:
    - Suboptimal disease control with significant inflammatory activity
    - Ongoing symptoms affecting daily function
    - Risk for progressive joint damage if sustained
    - Indicates need for treatment intensification
    - May be associated with increased comorbidity risk
    
    Management Approach:
    - Consider intensifying therapy - current control inadequate
    - Evaluate current DMARD therapy effectiveness and adherence
    - Consider combination DMARD therapy or biologic agents
    - Assess for barriers to treatment adherence or response
    - Review treatment goals and expectations with patient
    
    Monitoring Requirements:
    - Assess every 1-2 months to monitor response to therapy intensification
    - Evaluate treatment modifications and optimize regimen
    - Monitor for side effects of intensified therapy
    - Assess functional status and quality of life impacts
    
    Treatment Modifications:
    - Consider adding or switching DMARDs
    - Evaluate candidacy for biologic or targeted synthetic DMARDs
    - Optimize conventional DMARD dosing and combinations
    - Address comorbidities that may affect treatment response
    
    High Disease Activity (CDAI > 22 points):
    
    Clinical Characteristics:
    - Poor disease control with severe inflammatory activity
    - Significant symptoms and functional impairment
    - High risk for rapid joint damage progression
    - Associated with increased mortality and comorbidity risk
    - Urgent need for aggressive treatment modification
    
    Management Approach:
    - Urgent need to intensify therapy - poor control requiring immediate action
    - Consider combination DMARDs or biologic therapy promptly
    - Evaluate for rapidly acting interventions (corticosteroids, biologics)
    - Consider referral to rheumatology specialist if not already involved
    - Address psychosocial impacts and provide comprehensive support
    
    Monitoring Requirements:
    - Assess every 2-4 weeks until disease control achieved
    - Close monitoring for treatment response and side effects
    - Evaluate functional status and disability progression
    - Monitor for extra-articular manifestations
    
    Emergency Considerations:
    - Evaluate for complications requiring immediate intervention
    - Consider short-term corticosteroid bridge therapy
    - Assess for treatment-related adverse events
    - Provide comprehensive patient education and support
    
    Clinical Decision Support Features:
    
    Treat-to-Target Implementation:
    The CDAI provides clear targets for treat-to-target strategies:
    - Primary target: Remission (CDAI ≤ 2.8)
    - Alternative target: Low disease activity (CDAI ≤ 10)
    - Treatment modification timeline: If target not achieved within 3-6 months
    - Regular reassessment: Every 1-3 months depending on activity level
    
    Immediate Clinical Utility:
    The CDAI's laboratory-free design enables immediate treatment decision-making:
    - Real-time assessment during clinical encounters
    - No delays waiting for laboratory results
    - Cost-effective monitoring approach
    - Practical for frequent assessment and telemedicine
    
    Patient Engagement:
    The inclusion of patient global assessment promotes:
    - Shared decision-making in treatment planning
    - Patient-centered care approaches
    - Improved treatment adherence through engagement
    - Recognition of patient perspectives in disease management
    
    Quality Assurance and Implementation:
    
    Standardization Requirements:
    - Consistent joint examination techniques across providers
    - Standardized visual analog scale administration
    - Regular training and competency assessment
    - Documentation of assessment conditions and patient factors
    
    Clinical Integration:
    - Integration with electronic health record systems
    - Trending analysis for longitudinal monitoring
    - Treatment response evaluation and documentation
    - Quality improvement and outcome measurement
    
    The Clinical Disease Activity Index provides essential, practical assessment 
    capabilities that support evidence-based rheumatoid arthritis management. When 
    properly implemented with appropriate clinical context and regular monitoring, 
    the CDAI significantly enhances treatment decision-making and patient outcomes 
    in routine rheumatology practice.
    
    Reference: Aletaha D, et al. Arthritis Res Ther. 2005;7(4):R796-806.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=76.0,
        description="CDAI score calculated from four clinical components (0-76 points). Higher scores indicate greater disease activity",
        example=25.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CDAI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with disease activity category and treatment recommendations",
        example="CDAI Score 25.3: Moderate disease activity. Suboptimal control with significant inflammatory activity. Consider intensifying therapy to achieve low disease activity or remission."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity category (Remission, Low Disease Activity, Moderate Disease Activity, High Disease Activity)",
        example="Moderate Disease Activity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity category",
        example="Moderate disease activity"
    )
    
    scoring_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of CDAI components, clinical guidance, and treatment recommendations",
        example={
            "score_components": {
                "tender_joint_count": {
                    "value": 8,
                    "contribution": 8,
                    "percentage": "31.6%",
                    "clinical_significance": "Reflects subjective pain and inflammation from patient perspective"
                },
                "swollen_joint_count": {
                    "value": 5,
                    "contribution": 5,
                    "percentage": "19.8%",
                    "clinical_significance": "Objective measure of inflammatory joint involvement"
                }
            },
            "score_summary": {
                "total_cdai_score": 25.3,
                "activity_category": "Moderate disease activity",
                "target_score": "≤2.8 for remission, ≤10 for low disease activity"
            },
            "clinical_guidance": {
                "treatment_recommendations": [
                    "Consider intensifying therapy - suboptimal control",
                    "Evaluate current DMARD therapy effectiveness"
                ]
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 25.3,
                "unit": "points",
                "interpretation": "CDAI Score 25.3: Moderate disease activity. Suboptimal control with significant inflammatory activity. Consider intensifying therapy to achieve low disease activity or remission.",
                "stage": "Moderate Disease Activity",
                "stage_description": "Moderate disease activity",
                "scoring_breakdown": {
                    "score_components": {
                        "tender_joint_count": {
                            "value": 8,
                            "contribution": 8,
                            "clinical_significance": "Reflects subjective pain and inflammation from patient perspective"
                        }
                    },
                    "score_summary": {
                        "total_cdai_score": 25.3,
                        "activity_category": "Moderate disease activity"
                    }
                }
            }
        }