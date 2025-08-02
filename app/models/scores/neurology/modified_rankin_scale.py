"""
Modified Rankin Scale (mRS) Models

Request and response models for Modified Rankin Scale assessment of neurologic disability.

References (Vancouver style):
1. Rankin J. Cerebral vascular accidents in patients over the age of 60. II. Prognosis. 
   Scott Med J. 1957 Jul;2(7):200-15. doi: 10.1177/003693305700200704.
2. Warlow C, Dennis M, van Gijn J, et al. Stroke: A Practical Guide to Management. 
   Oxford: Blackwell Scientific Publications; 2001.
3. Bruno A, Shah N, Lin C, Close B, Hess DC, Davis K, Baute V, Switzer JA, Waller JL, 
   Nichols FT. Improving modified Rankin Scale assessment with a simplified questionnaire. 
   Stroke. 2010 May;41(5):1048-50. doi: 10.1161/STROKEAHA.109.571562.
4. Banks JL, Marotta CA. Outcomes validity and reliability of the modified Rankin scale: 
   implications for stroke clinical trials: a literature review and synthesis. 
   Stroke. 2007 Mar;38(3):1091-6. doi: 10.1161/01.STR.0000258355.23810.c6.

The Modified Rankin Scale (mRS) is the most widely used functional outcome measure 
in stroke research and clinical practice. It provides a common language for describing 
the degree of disability or dependence after neurological events, particularly stroke.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedRankinScaleRequest(BaseModel):
    """
    Request model for Modified Rankin Scale (mRS)
    
    The mRS assesses functional disability and dependence through a single ordinal scale:
    
    **Assessment Guidelines:**
    
    **Score 0 - No Symptoms:**
    - Patient has no symptoms at all
    - Complete functional recovery
    - No residual deficits from neurological event
    - Perfect health status
    - No limitations in any activities
    
    **Score 1 - No Significant Disability:**
    - Able to carry out all usual duties and activities
    - Some symptoms present but do not interfere with function
    - Can work, maintain social relationships, and live independently
    - Minor symptoms that don't impact daily life
    - May have mild weakness, sensory changes, or cognitive effects
    
    **Score 2 - Slight Disability:**
    - Unable to carry out all previous activities
    - Can look after own affairs without assistance
    - May need to modify work duties or give up some leisure activities
    - Independent in basic and instrumental ADLs
    - Slight restriction in lifestyle but maintains autonomy
    
    **Score 3 - Moderate Disability:**
    - Requires some help with activities
    - Able to walk without assistance
    - Needs help with complex tasks (shopping, finances, medication management)
    - May require assistance with transportation
    - Maintains mobility independence but needs support for some activities
    
    **Score 4 - Moderately Severe Disability:**
    - Unable to walk without assistance
    - Unable to attend to bodily needs without assistance
    - Requires help with ADLs (bathing, dressing, toileting)
    - May use mobility aids or wheelchair
    - Needs regular caregiver support
    
    **Score 5 - Severe Disability:**
    - Bedridden
    - Incontinent
    - Requires constant nursing care and attention
    - Complete dependence for all activities
    - May need skilled nursing facility or intensive home care
    
    **Score 6 - Dead:**
    - Patient has died
    - Most severe outcome
    - May result from primary neurological event or complications
    
    **Clinical Assessment Process:**
    
    **Structured Interview Approach:**
    - Use standardized questions to reduce subjectivity
    - Ask about specific functional domains:
      - Work and employment status
      - Leisure activities and hobbies
      - Social relationships and community participation
      - Independence in daily activities
      - Need for assistance or supervision
    
    **Key Assessment Areas:**
    - **Mobility**: Walking, transfers, use of assistive devices
    - **Self-Care**: Bathing, dressing, toileting, feeding
    - **Cognitive Function**: Memory, problem-solving, judgment
    - **Communication**: Speech, language, comprehension
    - **Social Function**: Relationships, community participation
    
    **Assessment Considerations:**
    - Consider patient's pre-stroke functional level
    - Account for comorbid conditions that may affect function
    - Use caregiver input when patient has cognitive impairment
    - Focus on current functional status, not potential for improvement
    - Consider cultural and social factors affecting activity participation
    
    **Inter-rater Reliability:**
    - Use structured interview protocols to improve consistency
    - Consider using mRS-9Q (9-question structured interview)
    - Training and certification can improve reliability
    - Video-based training materials available
    -Focus on observable functional limitations rather than symptoms
    
    **Clinical Applications:**
    - Primary endpoint in acute stroke trials
    - Quality metric for stroke care programs
    - Guides rehabilitation planning and resource allocation
    - Assists with discharge planning and care transitions
    - Important for prognosis discussions with families
    - Used for determining disability benefits and services
    
    References (Vancouver style):
    1. Rankin J. Cerebral vascular accidents in patients over the age of 60. II. Prognosis. 
       Scott Med J. 1957;2(7):200-15.
    2. Bruno A, Shah N, Lin C, Close B, Hess DC, Davis K, Baute V, Switzer JA, Waller JL, 
       Nichols FT. Improving modified Rankin Scale assessment with a simplified questionnaire. 
       Stroke. 2010;41(5):1048-50.
    """
    
    functional_status: Literal["no_symptoms", "no_significant_disability", "slight_disability", "moderate_disability", "moderately_severe_disability", "severe_disability", "dead"] = Field(
        ...,
        description="Patient's current functional status level. no_symptoms (0), no_significant_disability (1), slight_disability (2), moderate_disability (3), moderately_severe_disability (4), severe_disability (5), dead (6)",
        example="slight_disability"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "functional_status": "slight_disability"
            }
        }


class ModifiedRankinScaleResponse(BaseModel):
    """
    Response model for Modified Rankin Scale (mRS)
    
    The mRS score ranges from 0-6 and stratifies functional disability:
    
    **Functional Independence (mRS 0-2):**
    
    **Score 0 - No Symptoms:**
    - Complete functional recovery with no residual deficits
    - Return to all pre-stroke activities without limitation
    - Excellent outcome with normal quality of life
    - No healthcare services or accommodations needed
    
    **Score 1 - No Significant Disability:**
    - Minor symptoms that don't interfere with daily function
    - Able to maintain employment and social relationships
    - Independent living with good quality of life
    - May need minor accommodations but essentially normal function
    
    **Score 2 - Slight Disability:**
    - Some lifestyle modifications but maintains independence
    - May need work accommodations or activity modifications
    - Good functional outcome with preserved autonomy
    - Independent in self-care and basic daily activities
    
    **Functional Dependence (mRS 3-5):**
    
    **Score 3 - Moderate Disability:**
    - Partial independence with need for some assistance
    - Benefits from rehabilitation and community support services
    - May live independently with support or in assisted living
    - Requires help with complex instrumental activities
    
    **Score 4 - Moderately Severe Disability:**
    - Significant functional impairment requiring regular assistance
    - Benefits from comprehensive rehabilitation services
    - May need home modifications and assistive technology
    - Often requires assisted living or family caregiver support
    
    **Score 5 - Severe Disability:**
    - Complete dependence requiring intensive care
    - Needs skilled nursing facility or intensive home care
    - Focus on comfort, dignity, and prevention of complications
    - Significant caregiver burden and healthcare resource utilization
    
    **Score 6 - Death:**
    - Most severe outcome following neurological injury
    - Emphasizes importance of prevention and acute intervention
    
    **Clinical Implications by Score Range:**
    
    **Excellent Outcome (mRS 0-1):**
    - Functional independence achieved
    - Return to productive activities
    - Minimal healthcare service needs
    - High patient and family satisfaction
    
    **Good Outcome (mRS 0-2):**
    - Functional independence maintained
    - Acceptable quality of life
    - Community dwelling possible
    - Cost-effective care outcomes
    
    **Poor Outcome (mRS 3-6):**
    - Significant disability or death
    - High healthcare resource utilization
    - Need for long-term care services
    - Major impact on patient and family
    
    **Prognostic Value:**
    - Strong predictor of long-term functional outcomes
    - Correlates with quality of life measures
    - Predicts healthcare resource utilization
    - Important for rehabilitation planning and goal setting
    
    **Research Applications:**
    - Primary efficacy endpoint in stroke trials
    - Dichotomized outcomes: mRS 0-2 vs 3-6 (independence vs dependence)
    - Shift analysis across all mRS levels
    - Quality indicator for stroke care programs
    
    **Quality of Life Correlations:**
    - mRS 0-2: Generally good to excellent quality of life
    - mRS 3: Variable quality of life, often acceptable with support
    - mRS 4-5: Generally poor quality of life, significant burden
    - Strong correlation with patient and caregiver well-being
    
    Reference: Rankin J. Scott Med J. 1957;2(7):200-15.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=6,
        description="Modified Rankin Scale score indicating degree of neurologic disability (0-6 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the scale",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with functional status assessment and care recommendations based on mRS score",
        example="Modified Rankin Scale 2: Slight disability. The patient is unable to carry out all previous activities but is able to look after their own affairs without assistance. This may include loss of some leisure activities or work modifications, but maintains independence in basic and instrumental activities of daily living. Good functional outcome with some lifestyle adjustments. May benefit from occupational therapy for activity modification."
    )
    
    stage: str = Field(
        ...,
        description="Functional status category",
        example="Slight Disability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of functional level",
        example="Unable to carry out all previous activities but can look after own affairs"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Modified Rankin Scale 2: Slight disability. The patient is unable to carry out all previous activities but is able to look after their own affairs without assistance. This may include loss of some leisure activities or work modifications, but maintains independence in basic and instrumental activities of daily living. Good functional outcome with some lifestyle adjustments. May benefit from occupational therapy for activity modification.",
                "stage": "Slight Disability",
                "stage_description": "Unable to carry out all previous activities but can look after own affairs"
            }
        }