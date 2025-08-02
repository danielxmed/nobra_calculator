"""
Modified Rankin Score 9Q (mRS-9Q) Models

Request and response models for Modified Rankin Score 9Q assessment of neurologic function.

References (Vancouver style):
1. Bruno A, Shah N, Lin C, Close B, Hess DC, Davis K, Baute V, Switzer JA, Waller JL, 
   Nichols FT. Improving modified Rankin Scale assessment with a simplified questionnaire. 
   Stroke. 2010 May;41(5):1048-50. doi: 10.1161/STROKEAHA.109.571562.
2. Bruno A, Close B, Hancock GM, Hess DC, Kahles T, Yeatts SD, Lees KR, Molina CA. 
   Standardized modified rankin scale assessment by telephone: reliability in the ALIAS 
   pilot trial. Stroke. 2012 Aug;43(8):2086-90. doi: 10.1161/STROKEAHA.112.657130.
3. Bruno A, Akinwuntan AE, Lin C, Close B, Davis K, Baute V, Aryal R, Brooks D, Hess DC, 
   Switzer JA, Waller JL. Simplified modified rankin scale questionnaire: reproducibility 
   over the telephone and validation with quality of life. Stroke. 2011 Aug;42(8):2276-9. 
   doi: 10.1161/STROKEAHA.111.613273.

The Modified Rankin Score 9Q (mRS-9Q) is a structured 9-question interview that 
provides simple and reliable determination of the modified Rankin Scale score in 
neurosurgical and neurological patients. It reduces subjectivity and can be 
administered by medical or non-medical personnel with excellent reliability.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedRankinScore9QRequest(BaseModel):
    """
    Request model for Modified Rankin Score 9Q (mRS-9Q)
    
    The mRS-9Q uses 9 yes/no questions to systematically determine the mRS score:
    
    **Assessment Structure:**
    
    **Question 1 - Symptom Presence:**
    "Do you have any symptoms that are bothering you?"
    - Determines mRS 0 (no symptoms) vs ≥1 (symptoms present)
    - Foundation question that guides subsequent assessments
    - Consider physical, cognitive, emotional, or functional symptoms
    
    **Questions 2-4 - Activity and Social Function:**
    "Are you able to do the same work as before?"
    "Are you able to keep up with your hobbies?"
    "Have you maintained your ties to friends and family?"
    - Assess preservation of pre-illness activities and relationships
    - Work includes employment, volunteer activities, or usual productive tasks
    - Hobbies encompass leisure activities, sports, recreational pursuits
    - Social ties include family relationships, friendships, community involvement
    
    **Questions 5-6 - Instrumental Activities of Daily Living:**
    "Do you need help making a simple meal, doing household chores, or balancing a checkbook?"
    "Do you need help with shopping or traveling close to home?"
    - Assess complex daily living skills requiring cognitive and physical function
    - Meal preparation includes planning, cooking, and food safety
    - Household chores include cleaning, laundry, home maintenance
    - Financial management includes budgeting, bill paying, banking
    - Shopping includes grocery shopping, errands, consumer decisions
    - Local travel includes driving, public transportation, navigation
    
    **Questions 7-9 - Basic Activities and Care Needs:**
    "Do you need another person to help you walk?"
    "Do you need help with eating, going to the toilet, or bathing?"
    "Do you stay in bed most of the day and need constant nursing care?"
    - Assess fundamental mobility and self-care capabilities
    - Walking includes indoor/outdoor mobility, transfers, balance
    - Personal care includes feeding, toileting, bathing, dressing, grooming
    - Constant care indicates complete dependence and skilled nursing needs
    
    **Algorithm Logic:**
    - Higher disability levels take precedence in scoring
    - Q9 (bedridden/nursing care) → mRS 5
    - Q8 (personal care help) OR Q7 (walking help) → mRS 4
    - Q5 (basic tasks) OR Q6 (shopping/travel) → mRS 3
    - Q2, Q3, or Q4 inability → mRS 2
    - Q1 symptoms present → mRS 1
    - No positive responses → mRS 0
    
    **Administration Guidelines:**
    
    **Interview Setting:**
    - Can be administered in-person, by telephone, or via electronic survey
    - Quiet, private environment to ensure accurate responses
    - Allow adequate time for patient to consider each question
    - Encourage honest, specific responses about current functional status
    
    **Question Clarification:**
    - Define "work" broadly to include any productive activities
    - "Hobbies" includes any leisure activities patient previously enjoyed
    - "Help" means requiring another person's assistance, not just adaptive equipment
    - Focus on current abilities, not potential for improvement
    
    **Interviewer Training:**
    - Medical and non-medical personnel can administer with equal reliability
    - Standardized question wording improves consistency
    - Avoid leading questions or suggesting responses
    - Document specific examples that support responses
    
    **Special Considerations:**
    - For cognitive impairment, use caregiver input when patient responses unreliable
    - Consider pre-illness functional level when interpreting responses
    - Account for temporary vs. permanent functional changes
    - Address language or cultural barriers that may affect responses
    
    **Quality Assurance:**
    - Web-based calculators provide automated error checking
    - Cross-reference responses for internal consistency
    - Follow up on unexpected response patterns
    - Consider repeat assessment if responses seem inconsistent with clinical presentation
    
    **Clinical Applications:**
    - Stroke outcome assessment and monitoring
    - Traumatic brain injury functional evaluation
    - Neurological disease progression tracking
    - Clinical trial endpoint measurement
    - Quality improvement initiatives
    - Rehabilitation planning and goal setting
    
    References (Vancouver style):
    1. Bruno A, Shah N, Lin C, Close B, Hess DC, Davis K, Baute V, Switzer JA, Waller JL, 
       Nichols FT. Improving modified Rankin Scale assessment with a simplified questionnaire. 
       Stroke. 2010;41(5):1048-50.
    2. Bruno A, Close B, Hancock GM, Hess DC, Kahles T, Yeatts SD, Lees KR, Molina CA. 
       Standardized modified rankin scale assessment by telephone: reliability in the ALIAS 
       pilot trial. Stroke. 2012;43(8):2086-90.
    """
    
    symptoms_bothering: Literal["yes", "no"] = Field(
        ...,
        description="Do you have any symptoms that are bothering you? This includes any physical, cognitive, emotional, or functional symptoms that affect your daily life.",
        example="yes"
    )
    
    same_work: Literal["yes", "no"] = Field(
        ...,
        description="Are you able to do the same work as before? Work includes employment, volunteer activities, or usual productive tasks at your previous level.",
        example="no"
    )
    
    keep_hobbies: Literal["yes", "no"] = Field(
        ...,
        description="Are you able to keep up with your hobbies? This includes leisure activities, sports, recreational pursuits, or interests you previously enjoyed.",
        example="no"
    )
    
    maintain_social_ties: Literal["yes", "no"] = Field(
        ...,
        description="Have you maintained your ties to friends and family? This refers to your ability to continue relationships and social connections at your previous level.",
        example="yes"
    )
    
    need_help_basic_tasks: Literal["yes", "no"] = Field(
        ...,
        description="Do you need help making a simple meal, doing household chores, or balancing a checkbook? This assesses instrumental activities requiring cognitive and physical function.",
        example="no"
    )
    
    need_help_shopping_travel: Literal["yes", "no"] = Field(
        ...,
        description="Do you need help with shopping or traveling close to home? This includes grocery shopping, errands, driving, or using public transportation locally.",
        example="no"
    )
    
    need_help_walking: Literal["yes", "no"] = Field(
        ...,
        description="Do you need another person to help you walk? This refers to needing human assistance for mobility, not just using assistive devices independently.",
        example="no"
    )
    
    need_help_personal_care: Literal["yes", "no"] = Field(
        ...,
        description="Do you need help with eating, going to the toilet, or bathing? This assesses basic activities of daily living and personal self-care abilities.",
        example="no"
    )
    
    bedridden_nursing_care: Literal["yes", "no"] = Field(
        ...,
        description="Do you stay in bed most of the day and need constant nursing care? This indicates complete dependence requiring skilled nursing or intensive home care.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "symptoms_bothering": "yes",
                "same_work": "no",
                "keep_hobbies": "no", 
                "maintain_social_ties": "yes",
                "need_help_basic_tasks": "no",
                "need_help_shopping_travel": "no",
                "need_help_walking": "no",
                "need_help_personal_care": "no",
                "bedridden_nursing_care": "no"
            }
        }


class ModifiedRankinScore9QResponse(BaseModel):
    """
    Response model for Modified Rankin Score 9Q (mRS-9Q)
    
    The mRS-9Q score ranges from 0-5 and corresponds to standard mRS levels:
    
    **Score Interpretation and Functional Status:**
    
    **Score 0 - No Symptoms:**
    - Perfect functional recovery with no residual symptoms
    - Complete independence in all activities
    - Return to pre-illness level of function
    - No healthcare services or accommodations needed
    - Excellent quality of life and patient satisfaction
    
    **Score 1 - No Significant Disability:**
    - Minor symptoms present but do not interfere with function
    - Able to maintain work, hobbies, and social relationships
    - Independent living with preserved autonomy
    - May need minor accommodations but essentially normal function
    - Very good functional outcome with minimal impact on daily life
    
    **Score 2 - Slight Disability:**  
    - Unable to perform all previous activities but maintains independence
    - May require work modifications or give up some leisure activities
    - Difficulty with some social connections but core relationships preserved
    - Independent in basic and instrumental activities of daily living
    - Good functional outcome requiring lifestyle adjustments
    
    **Score 3 - Moderate Disability:**
    - Requires assistance with complex daily living tasks
    - Needs help with meal preparation, household management, or finances
    - May need help with shopping, transportation, or community activities
    - Maintains mobility independence but needs instrumental support
    - Benefits from community services and rehabilitation programs
    
    **Score 4 - Moderately Severe Disability:**
    - Requires assistance with basic activities of daily living
    - Needs help with mobility, personal care, or both
    - Cannot walk independently or care for bodily needs without assistance
    - Significant functional impairment affecting independence
    - Requires regular caregiver support and possible assisted living
    
    **Score 5 - Severe Disability:**
    - Complete dependence requiring constant supervision and care
    - Bedridden or chair-bound for majority of day
    - Requires skilled nursing care for all basic needs
    - May need skilled nursing facility or intensive home care
    - Focus on comfort, dignity, and prevention of complications
    
    **Clinical Utility and Applications:**
    
    **Advantages over Traditional mRS:**
    - Standardized question format reduces inter-rater variability
    - Can be administered by non-medical personnel with training
    - Excellent reliability for telephone or remote administration
    - Algorithm-based scoring eliminates subjective interpretation
    - Takes 5-10 minutes to complete with good patient acceptance
    
    **Research and Quality Applications:**
    - Primary endpoint in stroke and neurological trials
    - Quality indicator for stroke care programs
    - Outcome tracking for rehabilitation services
    - Population health surveillance tool
    - Health economics and resource utilization studies
    
    **Clinical Decision Support:**
    - Guides discharge planning and care transitions
    - Informs rehabilitation intensity and duration decisions
    - Assists with long-term care placement discussions
    - Supports disability determination and benefit applications
    - Facilitates prognostic discussions with patients and families
    
    **Reliability and Validity:**
    - Excellent inter-rater reliability (κ > 0.8) across settings
    - Strong test-retest reproducibility over 2-week period
    - Validated across multiple neurological conditions
    - Correlates well with quality of life measures
    - Maintains validity when administered by telephone
    
    **Implementation Considerations:**
    - Web-based calculators available with error checking
    - Training materials and certification programs available
    - Can be integrated into electronic health records
    - Suitable for both clinical care and research applications
    - Cost-effective compared to traditional assessment methods
    
    Reference: Bruno A, et al. Stroke. 2010;41(5):1048-50.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=5,
        description="Modified Rankin Score 9Q result indicating neurological functional status (0-5 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with functional status assessment and management recommendations based on mRS-9Q score",
        example="mRS-9Q Score 2: Slight disability. The patient is unable to carry out all previous activities but remains able to look after their own affairs without assistance. This may include inability to perform the same work as before, difficulty keeping up with hobbies, or challenges maintaining all social connections. However, basic and instrumental activities of daily living remain independent. Good functional outcome with lifestyle adjustments."
    )
    
    stage: str = Field(
        ...,
        description="Functional disability category",
        example="Slight Disability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of functional level",
        example="Unable to carry out all previous activities but independent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "mRS-9Q Score 2: Slight disability. The patient is unable to carry out all previous activities but remains able to look after their own affairs without assistance. This may include inability to perform the same work as before, difficulty keeping up with hobbies, or challenges maintaining all social connections. However, basic and instrumental activities of daily living remain independent. Good functional outcome with lifestyle adjustments.",
                "stage": "Slight Disability",
                "stage_description": "Unable to carry out all previous activities but independent"
            }
        }