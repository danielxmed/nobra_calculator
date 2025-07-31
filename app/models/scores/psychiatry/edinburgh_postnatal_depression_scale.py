"""
Edinburgh Postnatal Depression Scale (EPDS) Models

Request and response models for EPDS postpartum depression screening.

References (Vancouver style):
1. Cox JL, Holden JM, Sagovsky R. Detection of postnatal depression. Development of the 
   10-item Edinburgh Postnatal Depression Scale. Br J Psychiatry. 1987;150:782-6. 
   doi: 10.1192/bjp.150.6.782.
2. Levis B, Negeri Z, Sun Y, Benedetti A, Thombs BD; DEPRESsion Screening Data (DEPRESSD) 
   EPDS Group. Accuracy of the Edinburgh Postnatal Depression Scale (EPDS) for screening to 
   detect major depression among pregnant and postpartum women: systematic review and 
   meta-analysis of individual participant data. BMJ. 2020;371:m4022. doi: 10.1136/bmj.m4022.
3. Gibson J, McKenzie-McHarg K, Shakespeare J, Price J, Gray R. A systematic review of 
   studies validating the Edinburgh Postnatal Depression Scale in antepartum and postpartum 
   women. Acta Psychiatr Scand. 2009;119(5):350-64. doi: 10.1111/j.1600-0447.2009.01363.x.
4. Matthey S, Henshaw C, Elliott S, Barnett B. Variability in use of cut-off scores and 
   formats on the Edinburgh Postnatal Depression Scale: implications for clinical and 
   research practice. Arch Womens Ment Health. 2006;9(6):309-15. doi: 10.1007/s00737-006-0152-x.

The Edinburgh Postnatal Depression Scale (EPDS) is the most widely used postpartum 
depression screening tool worldwide. It is a 10-item self-report questionnaire that 
asks women to report how they have felt in the past week. The EPDS is validated for 
use in both antenatal (pregnancy) and postnatal (postpartum) periods and has been 
translated into over 25 languages.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EdinburghPostnatalDepressionScaleRequest(BaseModel):
    """
    Request model for Edinburgh Postnatal Depression Scale (EPDS)
    
    The EPDS is a 10-item self-report questionnaire designed to screen for depression 
    in pregnant and postpartum women. Each item asks about feelings "in the past 7 days" 
    to capture recent mood state. The scale is not diagnostic but serves as a screening 
    tool to identify women who may benefit from follow-up mental health assessment.
    
    Clinical Context and Administration:
    - Can be self-administered or administered by healthcare professionals
    - Takes approximately 5-10 minutes to complete
    - Should be completed at least once in antenatal period and once postpartum (6-12 weeks)
    - Validated for use during pregnancy and up to 1 year postpartum
    - Available in over 25 languages with cultural validation studies
    
    Scoring Instructions:
    - Each item is scored 0-3 points based on symptom severity
    - Items 1, 2, and 4 are REVERSE SCORED (0=3, 1=2, 2=1, 3=0)
    - Items 3, 5, 6, 7, 8, 9, and 10 are scored as marked (0=0, 1=1, 2=2, 3=3)
    - Total score ranges from 0-30 points
    - Higher scores indicate greater likelihood of depression
    
    Question Details (each rated 0-3 for past 7 days):
    
    1. "I have been able to laugh and see the funny side of things" (REVERSE SCORED)
    - 0: As much as I always could
    - 1: Not quite so much now  
    - 2: Definitely not so much now
    - 3: Not at all
    
    2. "I have looked forward with enjoyment to things" (REVERSE SCORED)
    - 0: As much as I ever did
    - 1: Rather less than I used to
    - 2: Definitely less than I used to  
    - 3: Hardly at all
    
    3. "I have blamed myself unnecessarily when things went wrong"
    - 0: No, never
    - 1: Not very often
    - 2: Yes, some of the time
    - 3: Yes, most of the time
    
    4. "I have been anxious or worried for no good reason" (REVERSE SCORED)
    - 0: No, not at all
    - 1: Hardly ever
    - 2: Yes, sometimes
    - 3: Yes, very often
    
    5. "I have felt scared or panicky for no very good reason"
    - 0: No, not at all
    - 1: No, not much
    - 2: Yes, sometimes
    - 3: Yes, quite a lot
    
    6. "Things have been getting on top of me"
    - 0: No, I have been coping as well as ever
    - 1: No, most of the time I have coped quite well
    - 2: Yes, sometimes I have not been coping as well as usual
    - 3: Yes, most of the time I have not been able to cope at all
    
    7. "I have been so unhappy that I have had difficulty sleeping"
    - 0: No, not at all
    - 1: Not very often
    - 2: Yes, sometimes
    - 3: Yes, most of the time
    
    8. "I have felt sad or miserable"
    - 0: No, not at all
    - 1: Not very often
    - 2: Yes, quite often
    - 3: Yes, most of the time
    
    9. "I have been so unhappy that I have been crying"
    - 0: No, never
    - 1: Only occasionally
    - 2: Yes, quite often
    - 3: Yes, most of the time
    
    10. "The thought of harming myself has occurred to me" (CRITICAL ITEM)
    - 0: Never
    - 1: Hardly ever
    - 2: Sometimes
    - 3: Yes, quite often
    * Any score >0 requires immediate safety assessment
    
    Validation and Accuracy (2020 meta-analysis):
    - Cut-off ≥10: Sensitivity 85%, Specificity 84%
    - Cut-off ≥11: Sensitivity 81%, Specificity 88% (optimal balance)
    - Cut-off ≥13: Sensitivity 66%, Specificity 95% (high specificity)
    
    Clinical Implementation Guidelines:
    - Universal screening recommended for all pregnant and postpartum women
    - Repeat screening if initial score ≥13 in 2-4 weeks
    - Question 10 responses >0 require immediate safety evaluation
    - Positive screens should lead to clinical assessment, not automatic diagnosis
    - Consider cultural factors and language barriers in interpretation
    
    Postpartum Depression Epidemiology:
    - Affects approximately 13% of mothers overall
    - Higher rates in women of color (18-22%)
    - Early identification through screening improves outcomes for mothers and children
    - Untreated depression can impact maternal-infant bonding and child development
    
    References (Vancouver style):
    1. Cox JL, Holden JM, Sagovsky R. Detection of postnatal depression. Development of the 
       10-item Edinburgh Postnatal Depression Scale. Br J Psychiatry. 1987;150:782-6.
    2. Levis B, Negeri Z, Sun Y, Benedetti A, Thombs BD; DEPRESsion Screening Data (DEPRESSD) 
       EPDS Group. Accuracy of the Edinburgh Postnatal Depression Scale (EPDS) for screening to 
       detect major depression among pregnant and postpartum women: systematic review and 
       meta-analysis of individual participant data. BMJ. 2020;371:m4022.
    3. Gibson J, McKenzie-McHarg K, Shakespeare J, Price J, Gray R. A systematic review of 
       studies validating the Edinburgh Postnatal Depression Scale in antepartum and postpartum 
       women. Acta Psychiatr Scand. 2009;119(5):350-64.
    """
    
    able_to_laugh: int = Field(
        ...,
        ge=0, le=3,
        description="I have been able to laugh and see the funny side of things (REVERSE SCORED: 0=as much as always, 1=not quite so much, 2=definitely not so much, 3=not at all)",
        example=1
    )
    
    looked_forward: int = Field(
        ...,
        ge=0, le=3,
        description="I have looked forward with enjoyment to things (REVERSE SCORED: 0=as much as ever, 1=rather less, 2=definitely less, 3=hardly at all)",
        example=2
    )
    
    blamed_myself: int = Field(
        ...,
        ge=0, le=3,
        description="I have blamed myself unnecessarily when things went wrong (0=never, 1=not very often, 2=some of the time, 3=most of the time)",
        example=2
    )
    
    anxious_worried: int = Field(
        ...,
        ge=0, le=3,
        description="I have been anxious or worried for no good reason (REVERSE SCORED: 0=not at all, 1=hardly ever, 2=sometimes, 3=very often)",
        example=3
    )
    
    scared_panicky: int = Field(
        ...,
        ge=0, le=3,
        description="I have felt scared or panicky for no very good reason (0=not at all, 1=not much, 2=sometimes, 3=quite a lot)",
        example=2
    )
    
    things_on_top: int = Field(
        ...,
        ge=0, le=3,
        description="Things have been getting on top of me (0=coping well as ever, 1=coped quite well most times, 2=sometimes not coping well, 3=not able to cope at all)",
        example=3
    )
    
    unhappy_sleeping: int = Field(
        ...,
        ge=0, le=3,
        description="I have been so unhappy that I have had difficulty sleeping (0=not at all, 1=not very often, 2=sometimes, 3=most of the time)",
        example=2
    )
    
    sad_miserable: int = Field(
        ...,
        ge=0, le=3,
        description="I have felt sad or miserable (0=not at all, 1=not very often, 2=quite often, 3=most of the time)",
        example=3
    )
    
    unhappy_crying: int = Field(
        ...,
        ge=0, le=3,
        description="I have been so unhappy that I have been crying (0=never, 1=occasionally, 2=quite often, 3=most of the time)",
        example=2
    )
    
    self_harm_thoughts: int = Field(
        ...,
        ge=0, le=3,
        description="The thought of harming myself has occurred to me (0=never, 1=hardly ever, 2=sometimes, 3=quite often) - ANY SCORE >0 REQUIRES IMMEDIATE SAFETY ASSESSMENT",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "able_to_laugh": 1,
                "looked_forward": 2,
                "blamed_myself": 2,
                "anxious_worried": 3,
                "scared_panicky": 2,
                "things_on_top": 3,
                "unhappy_sleeping": 2,
                "sad_miserable": 3,
                "unhappy_crying": 2,
                "self_harm_thoughts": 0
            }
        }


class EdinburghPostnatalDepressionScaleResponse(BaseModel):
    """
    Response model for Edinburgh Postnatal Depression Scale (EPDS)
    
    The EPDS score provides critical information for identifying women who may benefit 
    from mental health assessment and intervention during the perinatal period. Results 
    guide clinical decision-making but are not diagnostic by themselves.
    
    Score Interpretation and Clinical Actions:
    
    Low Risk (0-9 points):
    - Minimal depression symptoms present
    - Clinical Actions:
      * Continue routine prenatal/postpartum care
      * Provide general mental health education and resources
      * Screen again at recommended intervals
      * Document negative screening result
      * Maintain clinical vigilance for changing symptoms
    
    Moderate Risk (10-12 points):
    - Possible depression requiring further evaluation
    - Clinical Actions:
      * Clinical assessment by healthcare provider within 2 weeks
      * Provide mental health resources and educational materials
      * Consider brief counseling or support groups
      * Rescreening in 2-4 weeks recommended
      * Monitor closely for symptom progression
      * Assess psychosocial stressors and support systems
    
    High Risk (13-30 points):
    - Likely depression requiring clinical intervention
    - Clinical Actions:
      * Refer to healthcare provider (GP, psychiatrist) for comprehensive evaluation
      * Consider same-day or urgent appointment scheduling
      * Provide immediate mental health crisis resources
      * Assess need for antidepressant medication or therapy
      * Coordinate with mental health professionals
      * Implement safety planning if indicated
      * Rescreening in 2-4 weeks after clinical assessment
      * Consider impact on infant care and family functioning
    
    Self-Harm Risk Assessment (Question 10):
    
    Score 0 (Never):
    - No immediate safety concerns related to self-harm
    - Continue with routine depression screening and management
    
    Score 1 (Hardly ever):
    - Low-frequency self-harm thoughts present
    - Clinical Actions:
      * Same-day clinical evaluation recommended
      * Safety assessment and planning
      * Provide crisis hotline information
      * Ensure adequate support system is in place
      * Consider more frequent follow-up appointments
    
    Score 2 (Sometimes):
    - Moderate-frequency self-harm thoughts present
    - Clinical Actions:
      * Urgent clinical evaluation within 24 hours
      * Comprehensive safety assessment
      * Consider emergency psychiatric consultation
      * Activate support system and remove potential means
      * Provide immediate crisis resources and hotlines
      * Document safety plan and follow-up arrangements
    
    Score 3 (Quite often):
    - Frequent self-harm thoughts - highest risk
    - Clinical Actions:
      * IMMEDIATE safety assessment and intervention required
      * Consider emergency psychiatric evaluation
      * Do not leave patient alone until safety established
      * Activate crisis protocols and emergency services if needed
      * Comprehensive risk assessment with mental health professional
      * Ensure continuous monitoring and support
    
    Treatment Considerations:
    
    Mild to Moderate Depression:
    - Psychotherapy (cognitive-behavioral therapy, interpersonal therapy)
    - Support groups for postpartum women
    - Lifestyle interventions (exercise, sleep hygiene, nutrition)
    - Partner and family education and involvement
    - Psychosocial support services
    
    Moderate to Severe Depression:
    - Antidepressant medication (consider breastfeeding compatibility)
    - Intensive psychotherapy
    - Psychiatric consultation and management
    - Case management and care coordination
    - Possible partial hospitalization or intensive outpatient programs
    
    Breastfeeding Considerations:
    - Many antidepressants are compatible with breastfeeding
    - Sertraline and paroxetine often preferred choices
    - Benefits of treatment typically outweigh risks
    - Collaborate with pediatrician regarding infant monitoring
    - Support continued breastfeeding when possible and desired
    
    Follow-up and Monitoring:
    - Rescreening with EPDS at regular intervals
    - Assessment of treatment response and side effects
    - Monitoring of maternal-infant bonding and interaction
    - Evaluation of family functioning and support systems
    - Coordination between obstetric, mental health, and pediatric providers
    
    Long-term Considerations:
    - Risk of recurrence in future pregnancies
    - Impact on child development and family relationships
    - Importance of ongoing mental health maintenance
    - Family planning discussions regarding future pregnancies
    - Connection to long-term mental health resources
    
    Quality Improvement and Implementation:
    - Staff training on administration and interpretation
    - Integration with electronic health record systems
    - Standardized protocols for positive screening follow-up
    - Patient education materials in appropriate languages
    - Community resource development and referral pathways
    
    Cultural and Social Considerations:
    - Cultural attitudes toward mental health and help-seeking
    - Language barriers and need for interpreter services
    - Socioeconomic factors affecting access to care
    - Social support systems and family dynamics
    - Stigma related to mental health treatment
    
    Reference: Cox JL, et al. Br J Psychiatry. 1987;150:782-6.
    """
    
    result: int = Field(
        ...,
        description="EPDS total score calculated from all 10 items with appropriate reverse scoring (range: 0-30 points)",
        example=22
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the EPDS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on EPDS score and self-harm risk assessment",
        example="High risk for depression. Score indicates likely depressive symptoms requiring clinical assessment and potential intervention. Refer to healthcare provider, preferably general practitioner or mental health professional, for comprehensive evaluation and treatment planning. Recommend rescreening in 2-4 weeks if clinical assessment indicates ongoing monitoring is appropriate."
    )
    
    stage: str = Field(
        ...,
        description="EPDS risk category (Low Risk, Moderate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the depression risk level",
        example="Likely depression - clinical assessment recommended"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 22,
                "unit": "points",
                "interpretation": "High risk for depression. Score indicates likely depressive symptoms requiring clinical assessment and potential intervention. Refer to healthcare provider, preferably general practitioner or mental health professional, for comprehensive evaluation and treatment planning. Recommend rescreening in 2-4 weeks if clinical assessment indicates ongoing monitoring is appropriate.",
                "stage": "High Risk",
                "stage_description": "Likely depression - clinical assessment recommended"
            }
        }