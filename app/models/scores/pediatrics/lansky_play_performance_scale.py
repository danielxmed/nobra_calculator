"""
Lansky Play-Performance Scale for Pediatric Functional Status Models

Request and response models for Lansky Play-Performance Scale calculation.

References (Vancouver style):
1. Lansky SB, List MA, Lansky LL, Ritter-Sterr C, Miller DR. The measurement of 
   performance in childhood cancer patients. Cancer. 1987 Oct 1;60(7):1651-6. 
   doi: 10.1002/1097-0142(19871001)60:7<1651::aid-cncr2820600738>3.0.co;2-j.
2. Lansky LL, Cairns NU, Clark GM, Lowman J, Miller L, Trueworthy R. Childhood 
   leukemia: nonrandomized therapy with adriamycin. Cancer. 1975 Jan;35(1):306-17. 
   doi: 10.1002/1097-0142(197501)35:1<306::aid-cncr2820350138>3.0.co;2-0.
3. Steineck A, Bradford MC, Erickson JM, Johnson G, Klages KL, Words B, et al. 
   Patients, caregivers, and clinicians differ in performance status ratings: 
   implications for pediatric cancer clinical trials. Cancer Med. 2021 Sep;10(17):6181-92. 
   doi: 10.1002/cam4.4155.
4. Chung OK, Li HC, Chiu SY, Ho KY, Lopez V. The impact of cancer and its treatment 
   on physical activity levels and behavior in Hong Kong Chinese childhood cancer 
   survivors. Cancer Nurs. 2014 May-Jun;37(3):E43-51. doi: 10.1097/NCC.0000000000000152.

The Lansky Play-Performance Scale is a validated functional assessment tool specifically 
designed for pediatric patients, particularly those with cancer or chronic illnesses. 
It evaluates a child's ability to perform normal activities and participate in play, 
which are crucial indicators of functional status and quality of life in children.

Key Features:
- Age Range: Designed for children under 16 years of age
- Assessment Method: Parent/caregiver report of child's typical functional performance
- Scale Range: 0-100 points in increments of 10
- Primary Use: Pediatric oncology and chronic illness monitoring

Clinical Applications:
- Treatment response monitoring in pediatric cancer patients
- Functional status assessment for clinical trial eligibility
- Quality of life evaluation during treatment
- Prognosis assessment and care planning
- Communication tool between healthcare providers and families

Performance Categories:
- 100-80 points: Normal to minimal disability - able to carry on normal activity
- 70-50 points: Mild to moderate disability - some activity restrictions
- 40-20 points: Moderate to severe disability - significant limitations
- 10-0 points: Severe to complete disability - extensive care needs

Clinical Significance:
The scale helps healthcare providers:
- Monitor disease progression and treatment effects
- Make informed decisions about treatment intensity
- Plan appropriate supportive care interventions
- Communicate functional status objectively to multidisciplinary teams
- Assess eligibility for clinical trials and research studies

Important Considerations:
- Should be used in conjunction with other clinical assessments
- Parent/caregiver input is essential for accurate evaluation
- Cultural and developmental factors should be considered
- Regular reassessment is important for monitoring changes over time
- Not intended as the sole criterion for major treatment decisions
"""

from pydantic import BaseModel, Field
from typing import Literal


class LanskyPlayPerformanceScaleRequest(BaseModel):
    """
    Request model for Lansky Play-Performance Scale for Pediatric Functional Status
    
    The Lansky Play-Performance Scale assesses functional status in pediatric patients 
    under 16 years of age based on their ability to engage in normal activities and play. 
    The assessment relies primarily on parent/caregiver observations of the child's 
    typical performance over the recent period.
    
    Performance Status Categories:
    
    100 points - Fully active, normal:
    - Complete participation in all age-appropriate activities
    - No restrictions in play or daily activities
    - Normal energy levels and stamina
    
    90 points - Minor restrictions in strenuous physical activity:
    - Able to participate in most activities with slight limitations
    - May avoid very strenuous sports or activities
    - Generally maintains normal routine
    
    80 points - Active, but gets tired more quickly:
    - Participates in normal activities but with reduced endurance
    - May need more rest periods during activities
    - Overall good functional capacity with minor fatigue
    
    70 points - Greater restriction of play and less time spent in play activity:
    - Noticeable reduction in play time and activity level
    - May avoid certain activities due to limitations
    - Requires modifications to normal routine
    
    60 points - Up and around, but active play minimal:
    - Able to move around independently but limited active play
    - Prefers quiet activities over active ones
    - Significant reduction in energy and activity tolerance
    
    50 points - Lying around much of the day, but gets dressed:
    - Spends considerable time resting but maintains some independence
    - Able to dress and perform basic self-care with minimal assistance
    - Very limited activity tolerance
    
    40 points - Mainly in bed; participates in quiet activities:
    - Primarily bed-bound but can engage in quiet activities
    - Requires assistance with many daily activities
    - Limited to sedentary activities only
    
    30 points - Bedbound; needing assistance even for quiet play:
    - Confined to bed with minimal independent activity
    - Requires help even for simple quiet activities
    - Significant functional impairment
    
    20 points - Sleeping often; play entirely limited to very passive activities:
    - Spends most time sleeping or resting
    - Very limited engagement even in passive activities
    - Requires extensive care and supervision
    
    10 points - Doesn't play; does not get out of bed:
    - Completely bed-bound with no play activity
    - Requires total assistance for all activities
    - Severe functional impairment
    
    0 points - Unresponsive:
    - No response to environment or stimuli
    - Requires complete care for all needs
    - Most severe functional impairment
    
    Assessment Guidelines:
    - Consider the child's typical performance over the past week
    - Base assessment on the child's actual abilities, not potential
    - Include parent/caregiver input as primary source of information
    - Consider age-appropriate expectations for activities and play
    - Account for cultural differences in play and activity patterns
    - Reassess regularly to monitor changes over time
    
    Clinical Context:
    - Primarily used in pediatric oncology and chronic illness settings
    - Essential for clinical trial eligibility determination
    - Helps guide treatment intensity and supportive care decisions
    - Facilitates communication between healthcare providers and families
    - Should be used alongside other clinical assessments for comprehensive care
    
    References (Vancouver style):
    1. Lansky SB, List MA, Lansky LL, Ritter-Sterr C, Miller DR. The measurement of 
    performance in childhood cancer patients. Cancer. 1987 Oct 1;60(7):1651-6.
    2. Steineck A, Bradford MC, Erickson JM, Johnson G, Klages KL, Words B, et al. 
    Patients, caregivers, and clinicians differ in performance status ratings: 
    implications for pediatric cancer clinical trials. Cancer Med. 2021 Sep;10(17):6181-92.
    """
    
    performance_status: Literal[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] = Field(
        ...,
        description="Child's current functional performance status based on activity level and play capacity. "
                   "Select the score that best describes the child's typical performance over the recent period. "
                   "Assessment should be based on parent/caregiver observation and child's actual abilities. "
                   "Scores range from 0 (unresponsive) to 100 (fully active, normal) in increments of 10.",
        example=80
    )
    
    class Config:
        schema_extra = {
            "example": {
                "performance_status": 80
            }
        }


class LanskyPlayPerformanceScaleResponse(BaseModel):
    """
    Response model for Lansky Play-Performance Scale for Pediatric Functional Status
    
    Provides comprehensive functional status assessment with clinical interpretation 
    and recommendations for pediatric patients. The response includes the performance 
    score, functional category, and detailed clinical guidance for care planning.
    
    Functional Status Categories:
    
    Normal Function (100 points):
    - Excellent functional status with no activity limitations
    - Child can participate fully in all age-appropriate activities
    - Optimal quality of life and independence
    - No special accommodations needed
    
    Minimal Disability (80-90 points):
    - Good functional status with minor limitations
    - Able to carry on most normal activities
    - May have restrictions in strenuous activities
    - Generally able to attend school and participate in social activities
    
    Mild Disability (70 points):
    - Mild functional impairment with some activity restrictions
    - May require modifications to normal activities
    - School attendance may be affected
    - Consider adaptive strategies and energy conservation
    
    Mild-Moderate Disability (50-60 points):
    - Moderate functional impairment requiring support
    - Limited ability to engage in normal activities
    - May need assistance with some daily tasks
    - Consider educational accommodations and supportive services
    
    Moderate Disability (40 points):
    - Significant functional impairment with activity limitations
    - Requires assistance with many daily activities
    - Limited to quiet, sedentary activities
    - Focus on comfort and symptom management
    
    Moderate-Severe Disability (30 points):
    - Severe functional impairment with extensive care needs
    - Requires assistance even for simple activities
    - Consider palliative care consultation and family support
    
    Severe Disability (10-20 points):
    - Profound functional limitations requiring complete care
    - Focus on comfort measures and quality of life
    - Comprehensive family support services needed
    
    Unresponsive (0 points):
    - Complete functional impairment requiring total care
    - End-of-life care considerations may be appropriate
    
    Clinical Applications:
    - Monitor treatment response and disease progression
    - Assess eligibility for clinical trials and research studies
    - Guide treatment intensity and supportive care decisions
    - Facilitate communication among healthcare team members
    - Support care planning and resource allocation decisions
    
    Performance Characteristics:
    - Validated specifically for pediatric populations under 16 years
    - Good inter-rater reliability when used by trained assessors
    - Sensitive to changes in functional status over time
    - Correlates well with other measures of quality of life and disease severity
    
    Implementation Considerations:
    - Regular reassessment recommended to monitor changes
    - Consider combining with other functional assessments
    - Account for developmental stage and cultural factors
    - Ensure parent/caregiver input in assessment process
    - Use as part of comprehensive clinical evaluation
    
    Reference: Lansky SB, et al. Cancer. 1987;60(7):1651-6.
    """
    
    result: int = Field(
        ...,
        description="Lansky Play-Performance Scale score reflecting pediatric functional status (0-100 points)",
        example=80
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the Lansky scale score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including functional assessment, activity recommendations, "
                   "and care planning guidance specific to the child's performance level",
        example="Lansky Play-Performance Scale score: 80 points - Active, but gets tired more quickly. Good functional status with minimal limitations. Child can carry on most normal activities with some restrictions in strenuous activities. Generally able to attend school and participate in most age-appropriate activities. Monitor for fatigue and provide support as needed. The Lansky Play-Performance Scale should be assessed regularly to monitor disease progression and treatment response. This assessment reflects the child's functional status over the recent period and should consider parent/caregiver input. Use in conjunction with other clinical measures for comprehensive care planning."
    )
    
    stage: str = Field(
        ...,
        description="Functional status category based on the Lansky score",
        example="Minimal Disability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the functional status level",
        example="Active but with some limitations"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 80,
                "unit": "points",
                "interpretation": "Lansky Play-Performance Scale score: 80 points - Active, but gets tired more quickly. Good functional status with minimal limitations. Child can carry on most normal activities with some restrictions in strenuous activities. Generally able to attend school and participate in most age-appropriate activities. Monitor for fatigue and provide support as needed. The Lansky Play-Performance Scale should be assessed regularly to monitor disease progression and treatment response. This assessment reflects the child's functional status over the recent period and should consider parent/caregiver input. Use in conjunction with other clinical measures for comprehensive care planning.",
                "stage": "Minimal Disability",
                "stage_description": "Active but with some limitations"
            }
        }