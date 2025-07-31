"""
Cornell Assessment of Pediatric Delirium (CAPD) Models

Request and response models for CAPD pediatric delirium screening calculation.

References (Vancouver style):
1. Traube C, Silver G, Kearney J, Patel A, Atkinson TM, Yoon MJ, et al. Cornell Assessment 
   of Pediatric Delirium: a valid, rapid, observational tool for screening delirium in the PICU. 
   Crit Care Med. 2014 Mar;42(3):656-63. doi: 10.1097/CCM.0b013e3182a66b76.
2. Silver G, Traube C, Gerber LM, Sun X, Kearney J, Patel A, et al. Pediatric delirium and 
   associated risk factors: a single-center prospective observational study. Pediatr Crit Care Med. 
   2015 May;16(4):303-9. doi: 10.1097/PCC.0000000000000356.
3. Traube C, Silver G, Gerber LM, Kaur S, Mauer EA, Kerson A, et al. Delirium and mortality in 
   critically ill children: epidemiology and outcomes of pediatric delirium. Crit Care Med. 
   2017 May;45(5):891-898. doi: 10.1097/CCM.0000000000002324.
4. Smith HA, Boyd J, Fuchs DC, Melvin K, Berry P, Shintani A, et al. Diagnosing delirium in 
   critically ill children: Validity and reliability of the Pediatric Confusion Assessment Method 
   for the Intensive Care Unit. Crit Care Med. 2011 Jan;39(1):150-7. doi: 10.1097/CCM.0b013e3181feb489.

The CAPD is a validated, rapid observational tool for screening delirium in pediatric patients 
aged 0-21 years. It assesses eight behavioral domains through routine nursing observations, 
requiring no patient participation and taking less than 2 minutes to complete.

Clinical Background:

Pediatric Delirium Epidemiology:
- Affects 20-25% of pediatric ICU patients
- Associated with increased mortality, longer ICU stays, and functional disability
- Often under-recognized without systematic screening tools
- Can occur across all pediatric age groups from neonates to young adults
- Risk factors include critical illness, mechanical ventilation, and medications

CAPD Development and Validation:
- Developed specifically for pediatric populations with developmental considerations
- Based on DSM-5 diagnostic criteria for delirium
- Validated across age groups from 0-21 years with developmental anchor points
- Sensitivity 94.1% overall, with age-specific performance variations
- Can be used in both developmentally normal and delayed children

Eight Assessment Domains:

Domain Structure:
Each domain is scored 0-4 points based on frequency of observed behaviors:
- 0 points = Always/Never (most typical behavior)
- 1 point = Often/Rarely  
- 2 points = Sometimes
- 3 points = Rarely/Often
- 4 points = Never/Always (most atypical behavior)

Domain 1 - Makes Eye Contact with Caregiver:
Assesses social engagement and awareness of interpersonal environment.
- Scored: Always (0) to Never (4)
- Clinical Significance: Eye contact reflects attention and social awareness
- Developmental Context: Varies by age from basic visual tracking to complex social interaction
- Assessment Method: Observe during routine care interactions

Domain 2 - Actions are Purposeful:
Evaluates goal-directed behavior and cognitive organization.
- Scored: Always (0) to Never (4)  
- Clinical Significance: Purposeful actions indicate intact cognitive function
- Developmental Context: Age-appropriate purposeful behavior varies significantly
- Assessment Method: Observe during play, feeding, and care activities

Domain 3 - Aware of Surroundings:
Assesses environmental awareness and orientation.
- Scored: Always (0) to Never (4)
- Clinical Significance: Environmental awareness reflects attention and consciousness level
- Developmental Context: Developmentally appropriate environmental responses
- Assessment Method: Note responses to people, sounds, and environmental changes

Domain 4 - Communicates Needs and Wants:
Evaluates communication effectiveness and clarity.
- Scored: Always (0) to Never (4)
- Clinical Significance: Communication reflects cognitive organization and attention
- Developmental Context: Age-appropriate communication methods (crying, gestures, words)
- Assessment Method: Observe during care needs and comfort provision

Domain 5 - Restless:
Assesses psychomotor agitation and hyperactive behaviors.
- Scored: Never (0) to Always (4)
- Clinical Significance: Restlessness may indicate hyperactive delirium subtype
- Developmental Context: Normal activity levels vary significantly by age
- Assessment Method: Observe during awake periods and care interactions

Domain 6 - Inconsolable:
Evaluates emotional regulation and response to comfort measures.
- Scored: Never (0) to Always (4)
- Clinical Significance: Inconsolability reflects emotional dysregulation in delirium
- Developmental Context: Age-appropriate comfort responses and self-soothing
- Assessment Method: Observe responses to comfort measures and caregiver interaction

Domain 7 - Underactive (Very Little Movement While Awake):
Assesses psychomotor retardation and hypoactive behaviors.
- Scored: Never (0) to Always (4)
- Clinical Significance: Underactivity may indicate hypoactive delirium subtype
- Developmental Context: Normal activity patterns vary by age and developmental stage
- Assessment Method: Observe movement patterns during awake periods

Domain 8 - Takes Long Time to Respond to Interactions:
Evaluates response time and processing speed.
- Scored: Never (0) to Always (4)
- Clinical Significance: Delayed responses reflect cognitive processing difficulties
- Developmental Context: Expected response times vary by developmental stage
- Assessment Method: Observe latency to respond during interactions and care

Scoring and Interpretation:

Scoring Method:
- Total score: Sum of all 8 domains (0-32 points)
- Delirium threshold: ≥9 points indicates positive screen
- Score optimization: Threshold chosen to maximize sensitivity (94.1%)
- Clinical context: Higher scores indicate more severe delirium symptoms

Age-Specific Performance:
- Ages 0-13 years: High sensitivity and specificity
- Ages 13-21 years: Reduced sensitivity (50%), high specificity (98.1%)
- Developmental considerations: Anchor points guide age-appropriate assessment
- Special populations: Validated in both normal and developmentally delayed children

Clinical Implementation:

Assessment Requirements:
- Performed by bedside nurses during routine care
- No patient participation required (observational only)
- Takes less than 2 minutes to complete
- Should be performed every nursing shift
- Excludes deeply sedated patients (similar to adult tools)

Training and Competency:
- Requires brief training on developmental anchor points
- Inter-rater reliability improved with standardized training
- Reference charts available for bedside use
- Practice with diverse age groups recommended

Quality Assurance:
- Document assessment timing and clinical context
- Note factors that may influence behavioral observations
- Consider developmental stage and baseline function
- Record interventions and response to treatment

Clinical Applications:

Screening Programs:
- Universal screening for all pediatric ICU patients
- Integration with pediatric early warning systems  
- Quality improvement initiatives for delirium reduction
- Research applications for pediatric delirium studies

Management Integration:
- Triggers pediatric delirium management protocols
- Guides medication review and optimization
- Informs family education and support needs
- Supports discharge planning and follow-up care

Special Considerations:

Developmental Factors:
- Premature infants: Adjusted for corrected gestational age
- Developmental delays: Assess relative to individual baseline
- Cultural considerations: Account for cultural differences in behavior
- Language barriers: Focus on non-verbal behavioral observations

Environmental Context:
- ICU setting may alter normal behavioral patterns
- Separation from family affects behavioral assessment
- Medical devices and procedures influence behavior
- Medication effects on behavior and cognition

Limitations and Considerations:
- Observational tool requiring clinical judgment
- May be less sensitive in certain age groups
- Requires understanding of normal developmental patterns
- Should be used as part of comprehensive delirium assessment

References (Vancouver style):
1. Traube C, Silver G, Kearney J, Patel A, Atkinson TM, Yoon MJ, et al. Cornell Assessment 
of Pediatric Delirium: a valid, rapid, observational tool for screening delirium in the PICU. 
Crit Care Med. 2014 Mar;42(3):656-63. doi: 10.1097/CCM.0b013e3182a66b76.
2. Silver G, Traube C, Gerber LM, Sun X, Kearney J, Patel A, et al. Pediatric delirium and 
associated risk factors: a single-center prospective observational study. Pediatr Crit Care Med. 
2015 May;16(4):303-9. doi: 10.1097/PCC.0000000000000356.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CapdRequest(BaseModel):
    """
    Request model for Cornell Assessment of Pediatric Delirium (CAPD)
    
    The CAPD is a validated observational tool for screening delirium in pediatric patients 
    aged 0-21 years. Assessment is based on behavioral observations during routine nursing 
    care and requires no patient participation. Each of the eight domains is scored from 
    0-4 points based on frequency of observed behaviors.
    
    Scoring Guidelines by Domain:
    
    Awareness and Cognitive Domains (scored 0-4, where 0=best function):
    
    Makes Eye Contact with Caregiver:
    - 0 = Always: Consistently makes appropriate eye contact during interactions
    - 1 = Often: Usually makes eye contact, occasional lapses
    - 2 = Sometimes: Intermittent eye contact, noticeable reduction
    - 3 = Rarely: Infrequent eye contact despite attempts to engage
    - 4 = Never: No eye contact observed during assessment period
    
    Actions are Purposeful:
    - 0 = Always: All observed actions are goal-directed and appropriate
    - 1 = Often: Most actions purposeful, occasional aimless behavior
    - 2 = Sometimes: Mix of purposeful and aimless actions
    - 3 = Rarely: Few purposeful actions, mostly disorganized behavior
    - 4 = Never: No purposeful actions observed
    
    Aware of Surroundings:
    - 0 = Always: Fully aware of environment, people, and situation
    - 1 = Often: Usually aware, occasional disorientation
    - 2 = Sometimes: Intermittent awareness, periods of confusion
    - 3 = Rarely: Limited awareness of surroundings
    - 4 = Never: No apparent awareness of environment
    
    Communicates Needs and Wants:
    - 0 = Always: Effectively communicates through age-appropriate methods
    - 1 = Often: Usually communicates clearly, occasional difficulties
    - 2 = Sometimes: Intermittent communication, some needs unclear
    - 3 = Rarely: Minimal communication, difficulty expressing needs
    - 4 = Never: Unable to communicate needs and wants
    
    Psychomotor Domains (scored 0-4, where 0=no abnormal behavior):
    
    Restless:
    - 0 = Never: No restless behavior, calm and settled
    - 1 = Rarely: Occasional restlessness, easily settled
    - 2 = Sometimes: Intermittent restless behavior
    - 3 = Often: Frequent restlessness, difficult to settle
    - 4 = Always: Constant restless behavior throughout assessment
    
    Inconsolable:
    - 0 = Never: Easily comforted when distressed, responds to caregivers
    - 1 = Rarely: Occasionally difficult to console
    - 2 = Sometimes: Intermittently inconsolable
    - 3 = Often: Frequently inconsolable, comfort measures partially effective
    - 4 = Always: Constantly inconsolable, no response to comfort measures
    
    Underactive (Very Little Movement While Awake):
    - 0 = Never: Normal activity level for age and condition
    - 1 = Rarely: Occasional periods of reduced activity
    - 2 = Sometimes: Intermittent underactivity
    - 3 = Often: Frequently underactive, minimal spontaneous movement
    - 4 = Always: Very little movement while awake, markedly underactive
    
    Takes Long Time to Respond to Interactions:
    - 0 = Never: Normal response time for age and condition
    - 1 = Rarely: Occasionally slow to respond
    - 2 = Sometimes: Intermittent delayed responses
    - 3 = Often: Frequently slow to respond to interactions
    - 4 = Always: Very slow or no response to interactions
    
    Developmental Considerations:
    
    Age-Specific Assessment Guidelines:
    - Newborns (0-1 month): Focus on basic reflexes and physiologic responses
    - Infants (1-12 months): Consider developmental milestones and social responses
    - Toddlers (1-3 years): Account for normal oppositional behavior and stranger anxiety
    - Preschoolers (3-6 years): Consider fantasy play and developing language skills
    - School-age (6-13 years): Evaluate concrete thinking and peer interactions
    - Adolescents (13-21 years): Consider identity development and independence seeking
    
    Assessment Context:
    - Observe during routine nursing care activities
    - Consider baseline developmental level and medical condition
    - Account for effects of medical devices, medications, and environment
    - Use family input to establish baseline behavior patterns
    - Document timing relative to procedures, medications, and sleep cycles
    
    Clinical Implementation:
    - Complete assessment every nursing shift
    - Takes less than 2 minutes to complete
    - Based on behavioral observations over assessment period
    - No patient participation required
    - Consider developmental anchor points for age-appropriate expectations
    
    References (Vancouver style):
    1. Traube C, Silver G, Kearney J, Patel A, Atkinson TM, Yoon MJ, et al. Cornell Assessment 
    of Pediatric Delirium: a valid, rapid, observational tool for screening delirium in the PICU. 
    Crit Care Med. 2014 Mar;42(3):656-63. doi: 10.1097/CCM.0b013e3182a66b76.
    2. Silver G, Traube C, Gerber LM, Sun X, Kearney J, Patel A, et al. Pediatric delirium and 
    associated risk factors: a single-center prospective observational study. Pediatr Crit Care Med. 
    2015 May;16(4):303-9. doi: 10.1097/PCC.0000000000000356.
    """
    
    eye_contact: int = Field(
        ...,
        ge=0,
        le=4,
        description="Makes eye contact with caregiver. Score 0=Always, 1=Often, 2=Sometimes, 3=Rarely, 4=Never. Consider age-appropriate eye contact patterns and social development",
        example=1
    )
    
    purposeful_actions: int = Field(
        ...,
        ge=0,
        le=4,
        description="Actions are purposeful and goal-directed. Score 0=Always, 1=Often, 2=Sometimes, 3=Rarely, 4=Never. Assess based on age-appropriate purposeful behaviors",
        example=0
    )
    
    aware_surroundings: int = Field(
        ...,
        ge=0,
        le=4,
        description="Aware of surroundings and environment. Score 0=Always, 1=Often, 2=Sometimes, 3=Rarely, 4=Never. Consider developmental capacity for environmental awareness",
        example=2
    )
    
    communicates_needs: int = Field(
        ...,
        ge=0,
        le=4,
        description="Communicates needs and wants effectively. Score 0=Always, 1=Often, 2=Sometimes, 3=Rarely, 4=Never. Use age-appropriate communication expectations",
        example=1
    )
    
    restless: int = Field(
        ...,
        ge=0,
        le=4,
        description="Restless behavior observed. Score 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Always. Consider normal activity levels for age and medical condition",
        example=3
    )
    
    inconsolable: int = Field(
        ...,
        ge=0,
        le=4,
        description="Inconsolable when distressed. Score 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Always. Assess response to age-appropriate comfort measures",
        example=2
    )
    
    underactive: int = Field(
        ...,
        ge=0,
        le=4,
        description="Underactive with very little movement while awake. Score 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Always. Compare to expected activity for age",
        example=0
    )
    
    slow_response: int = Field(
        ...,
        ge=0,
        le=4,
        description="Takes long time to respond to interactions. Score 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Always. Consider developmental response times",
        example=1
    )
    
    patient_age: int = Field(
        ...,
        ge=0,
        le=21,
        description="Patient age in years. Used for developmental context and age-specific interpretation. CAPD is validated for ages 0-21 years",
        example=5
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "eye_contact": 1,
                "purposeful_actions": 0,
                "aware_surroundings": 2,
                "communicates_needs": 1,
                "restless": 3,
                "inconsolable": 2,
                "underactive": 0,
                "slow_response": 1,
                "patient_age": 5
            }
        }


class CapdResponse(BaseModel):
    """
    Response model for Cornell Assessment of Pediatric Delirium (CAPD)
    
    Provides comprehensive pediatric delirium screening results with domain analysis, 
    clinical interpretation, age-specific considerations, and evidence-based management 
    recommendations for pediatric patients.
    
    CAPD Interpretation Framework:
    
    Scoring and Thresholds:
    - Total Score Range: 0-32 points (8 domains × 4 points each)
    - Delirium Threshold: ≥9 points indicates positive screen
    - Severity Classification: Higher scores suggest more severe symptoms
    - Age Considerations: Performance varies by developmental stage
    
    Clinical Significance by Result:
    
    CAPD Positive (≥9 points):
    - Delirium likely present, requiring immediate evaluation
    - Associated with increased morbidity and mortality in pediatric patients
    - May indicate hyperactive, hypoactive, or mixed delirium subtypes
    - Triggers comprehensive medical evaluation and intervention protocols
    
    CAPD Negative (<9 points):
    - Delirium unlikely at time of assessment
    - Continue preventive measures and regular monitoring
    - Reassess regularly as delirium can fluctuate or develop rapidly
    - Consider other causes of behavioral changes if clinically indicated
    
    Domain-Specific Clinical Insights:
    
    Awareness and Cognitive Domains:
    - Eye Contact: Reflects social engagement and interpersonal awareness
    - Purposeful Actions: Indicates cognitive organization and goal-directed behavior
    - Environmental Awareness: Suggests attention and consciousness level
    - Communication: Reflects cognitive clarity and expressive abilities
    
    Psychomotor Domains:
    - Restlessness: May indicate hyperactive delirium subtype
    - Inconsolability: Reflects emotional dysregulation and comfort responsiveness
    - Underactivity: May suggest hypoactive delirium subtype
    - Slow Response: Indicates processing speed and cognitive efficiency
    
    Age-Specific Performance Characteristics:
    
    Pediatric Age Groups (0-13 years):
    - High sensitivity (94.1%) for delirium detection
    - Good specificity across most pediatric age ranges
    - Developmental anchor points guide appropriate assessment
    - Validated in both normal and developmentally delayed children
    
    Adolescent Age Group (13-21 years):
    - Reduced sensitivity (50%) but high specificity (98.1%)
    - May require additional assessment tools for comprehensive evaluation
    - Consider adult delirium tools as complementary assessment
    - Developmental factors affecting cooperation and behavior expression
    
    Management Framework by Assessment Outcome:
    
    Immediate Actions for Positive Results:
    - Implement pediatric delirium management protocols
    - Comprehensive medical evaluation for underlying causes
    - Medication review with focus on deliriogenic agents
    - Environmental modifications for age-appropriate comfort
    - Family involvement in care planning and comfort provision
    
    Ongoing Monitoring Requirements:
    - Continue CAPD assessments every nursing shift
    - Monitor for delirium-related complications and safety issues
    - Track response to interventions and behavioral changes
    - Document developmental considerations and family observations
    
    Prevention Strategies (All Patients):
    - Maintain age-appropriate sleep-wake cycles
    - Provide familiar comfort objects and family presence
    - Minimize unnecessary procedures and medications
    - Support developmental needs and activities
    - Optimize pain management and comfort measures
    
    Age-Specific Management Considerations:
    
    Infants and Toddlers:
    - Focus on maintaining parent-child bonding and attachment
    - Provide age-appropriate sensory stimulation and comfort
    - Support normal feeding and sleep routines
    - Use non-pharmacological comfort measures primarily
    
    Preschool and School-Age:
    - Provide age-appropriate explanations and reassurance
    - Use play therapy and creative expression for coping
    - Maintain educational activities and peer contact when possible
    - Involve child life specialists for developmental support
    
    Adolescents:
    - Respect privacy and autonomy needs
    - Involve in care planning and decision-making appropriately
    - Address concerns about body image and peer relationships
    - Provide technology access and social connections when possible
    
    Family-Centered Care Considerations:
    
    Family Education Priorities:
    - Explain pediatric delirium as treatable medical condition
    - Provide reassurance about temporary nature of symptoms
    - Teach age-appropriate comfort and interaction strategies
    - Support family coping with behavioral changes and stress
    
    Family Involvement Strategies:
    - Encourage consistent family presence and participation in care
    - Provide familiar objects and photos from home
    - Support family in providing age-appropriate stimulation
    - Include family observations in assessment and care planning
    
    Quality Improvement Applications:
    
    Clinical Metrics:
    - Delirium incidence rates by age group and unit
    - Time to delirium recognition and intervention
    - CAPD compliance rates and assessment frequency
    - Correlation with clinical outcomes and length of stay
    
    Performance Indicators:
    - Healthcare provider training completion and competency
    - Inter-rater reliability scores for CAPD assessments
    - Protocol adherence for pediatric delirium prevention and management
    - Family satisfaction with delirium care and communication
    
    Research Applications:
    - Pediatric delirium prevention and intervention studies
    - Developmental considerations in delirium presentation
    - Family-centered care approaches in delirium management
    - Long-term neurodevelopmental outcomes following pediatric delirium
    
    Special Populations and Considerations:
    
    Developmental Delays:
    - Assess relative to individual baseline function
    - Consider adaptive behaviors and communication methods
    - May require modified scoring based on developmental level
    - Involve specialized developmental teams in assessment
    
    Cultural Considerations:
    - Account for cultural differences in behavior expression
    - Consider family cultural practices and comfort measures
    - Use culturally appropriate communication and interaction styles
    - Involve cultural liaisons when language barriers exist
    
    Medical Complexity:
    - Consider effects of medical devices on behavior and mobility
    - Account for medication effects on behavior and cognition
    - Assess in context of underlying medical conditions
    - Coordinate with multidisciplinary team for comprehensive care
    
    Reference: Traube C, et al. Crit Care Med. 2014;42(3):656-63. doi: 10.1097/CCM.0b013e3182a66b76.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CAPD assessment including domain analysis, clinical interpretation, and age-specific management recommendations",
        example={
            "capd_positive": True,
            "total_score": 10,
            "max_possible_score": 32,
            "delirium_threshold": 9,
            "domain_scores": {
                "eye_contact": {
                    "score": 1,
                    "max_score": 4,
                    "description": "Makes eye contact with caregiver",
                    "severity": "Mild",
                    "clinical_significance": "Slightly reduced eye contact"
                },
                "purposeful_actions": {
                    "score": 0,
                    "max_score": 4,
                    "description": "Actions are purposeful",
                    "severity": "Normal",
                    "clinical_significance": "All actions appear purposeful and goal-directed"
                }
            },
            "age_group": {
                "group": "Preschool",
                "age_range": "3-6 years",
                "developmental_considerations": [
                    "Improved verbal communication abilities",
                    "Fantasy play and imagination may affect reality testing"
                ]
            },
            "clinical_interpretation": {
                "stage": "CAPD Positive",
                "description": "Delirium present",
                "severity": "mild",
                "interpretation": "Patient meets CAPD criteria for delirium with a score of 10/32, suggesting mild delirium symptoms.",
                "age_considerations": "Assessment performed in preschool age group"
            },
            "management_recommendations": {
                "immediate_actions": [
                    "Implement pediatric delirium management protocol",
                    "Evaluate for underlying causes"
                ],
                "ongoing_monitoring": [
                    "Continue CAPD assessments every nursing shift"
                ],
                "prevention_strategies": [
                    "Minimize environmental stimulation during rest periods"
                ],
                "family_involvement": [
                    "Educate family about pediatric delirium"
                ],
                "age_specific_considerations": [
                    "Provide age-appropriate explanations about medical care"
                ],
                "reassessment_timing": "Every nursing shift and with any significant clinical changes"
            },
            "screening_performance": {
                "sensitivity": "94.1%",
                "specificity": "Variable by age group",
                "note": "High sensitivity across pediatric age groups"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="assessment"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with assessment results and evidence-based recommendations",
        example="Patient meets CAPD criteria for delirium with a score of 10/32, suggesting mild delirium symptoms. Early intervention may prevent progression."
    )
    
    stage: str = Field(
        ...,
        description="Overall delirium status classification (CAPD Positive, CAPD Negative)",
        example="CAPD Positive"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the delirium assessment result",
        example="Delirium present"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "capd_positive": True,
                    "total_score": 10,
                    "max_possible_score": 32,
                    "delirium_threshold": 9,
                    "domain_scores": {
                        "eye_contact": {
                            "score": 1,
                            "max_score": 4,
                            "description": "Makes eye contact with caregiver",
                            "severity": "Mild",
                            "clinical_significance": "Slightly reduced eye contact"
                        },
                        "purposeful_actions": {
                            "score": 0,
                            "max_score": 4,
                            "description": "Actions are purposeful",
                            "severity": "Normal",
                            "clinical_significance": "All actions appear purposeful and goal-directed"
                        }
                    },
                    "age_group": {
                        "group": "Preschool",
                        "age_range": "3-6 years",
                        "developmental_considerations": [
                            "Improved verbal communication abilities",
                            "Fantasy play and imagination may affect reality testing"
                        ]
                    },
                    "clinical_interpretation": {
                        "stage": "CAPD Positive",
                        "description": "Delirium present",
                        "severity": "mild",
                        "interpretation": "Patient meets CAPD criteria for delirium with a score of 10/32, suggesting mild delirium symptoms.",
                        "age_considerations": "Assessment performed in preschool age group"
                    },
                    "management_recommendations": {
                        "immediate_actions": [
                            "Implement pediatric delirium management protocol",
                            "Evaluate for underlying causes"
                        ],
                        "ongoing_monitoring": [
                            "Continue CAPD assessments every nursing shift"
                        ],
                        "prevention_strategies": [
                            "Minimize environmental stimulation during rest periods"
                        ],
                        "family_involvement": [
                            "Educate family about pediatric delirium"
                        ],
                        "age_specific_considerations": [
                            "Provide age-appropriate explanations about medical care"
                        ],
                        "reassessment_timing": "Every nursing shift and with any significant clinical changes"
                    },
                    "screening_performance": {
                        "sensitivity": "94.1%",
                        "specificity": "Variable by age group",
                        "note": "High sensitivity across pediatric age groups"
                    }
                },
                "unit": "assessment",
                "interpretation": "Patient meets CAPD criteria for delirium with a score of 10/32, suggesting mild delirium symptoms. Early intervention may prevent progression.",
                "stage": "CAPD Positive",
                "stage_description": "Delirium present"
            }
        }