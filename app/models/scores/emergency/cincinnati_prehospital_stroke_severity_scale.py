"""
Cincinnati Prehospital Stroke Severity Scale (CP-SSS) Models

Request and response models for Cincinnati Prehospital Stroke Severity Scale calculation.

References (Vancouver style):
1. Katz BS, McMullan JT, Sucharew H, Adeoye O, Broderick JP. Design and validation of a 
   prehospital scale to predict stroke severity: the Cincinnati Prehospital Stroke 
   Severity Scale. Stroke. 2015 Jun;46(6):1508-12.
2. McMullan JT, Katz B, Broderick J, Schmit P, Sucharew H, Adeoye O. Prospective 
   prehospital evaluation of the Cincinnati stroke triage assessment tool. Prehosp 
   Emerg Care. 2017 Jan-Feb;21(1):68-75.
3. Zhao H, Coote S, Pesavento L, Churilov L, Dewey HM, Davis SM, et al. Large vessel 
   occlusion scales increase delivery to endovascular centers without excessive harm 
   from misclassifications. Stroke. 2017 Mar;48(3):568-573.

The Cincinnati Prehospital Stroke Severity Scale (CP-SSS) is a validated tool designed 
to predict large vessel occlusion (LVO) and severe stroke in patients presenting with 
acute stroke symptoms. This scale was specifically developed for use by emergency 
medical services (EMS) personnel to enhance prehospital stroke triage and guide 
transport decisions to appropriate stroke care facilities.

Clinical Background and Development:

The CP-SSS was developed to address the critical need for accurate prehospital 
identification of patients with severe strokes who would benefit from direct transport 
to comprehensive stroke centers capable of performing endovascular thrombectomy. The 
scale was derived and validated using data from landmark stroke trials including the 
National Institute of Neurological Disorders and Stroke (NINDS) tissue-type 
plasminogen activator Stroke Study trials and the Interventional Management of 
Stroke III (IMS III) Trial.

Scale Development Methodology:

The CP-SSS was developed using regression tree analysis with specific design criteria:
- Objectivity in assessment parameters
- Anticipated ease of administration by EMS personnel
- Focus on cortical signs predictive of large vessel involvement
- Rapid assessment capability in prehospital settings
- High predictive value for severe stroke (NIHSS ≥15)

Four-Component Assessment Framework:

1. Conjugate Gaze Deviation (0-2 points):
Conjugate gaze deviation is a powerful predictor of cortical involvement and large 
vessel occlusion. This finding indicates damage to cortical gaze centers or their 
connections, commonly seen in anterior circulation large vessel strokes.

Clinical Assessment:
- Present (2 points): Eyes deviated to one side, typically toward the side of the lesion
- Absent (0 points): Normal eye movements or ability to overcome gaze preference

Clinical Significance:
- Strong predictor of large vessel occlusion
- Indicates cortical involvement rather than small vessel disease
- Associated with higher NIHSS scores and worse functional outcomes
- Guides need for advanced stroke interventions

2. Level of Consciousness - Questions (0-2 points):
This component assesses the patient's alertness and cognitive function through 
standardized questions, typically asking for the patient's age and the current month.

Scoring Methodology:
- Both questions answered correctly (0 points): Normal cognitive function
- One question answered correctly (1 point): Mild cognitive impairment
- Neither question answered correctly (2 points): Significant cognitive impairment

Clinical Interpretation:
- Assesses cortical function and arousal
- Reflects severity of cerebral dysfunction
- Important predictor of stroke severity
- Helps differentiate stroke from stroke mimics

3. Level of Consciousness - Commands (0-2 points):
This component evaluates the patient's ability to follow simple motor commands, 
typically asking the patient to open and close their eyes and grip and release 
their non-paretic hand.

Scoring Framework:
- Follows both commands (0 points): Normal comprehension and motor function
- Follows one command (1 point): Partial comprehension or motor impairment
- Follows neither command (2 points): Severe comprehension or motor deficit

Clinical Applications:
- Evaluates comprehension and motor response pathways
- Assesses severity of cortical dysfunction
- Differentiates cortical from subcortical strokes
- Predicts functional outcome potential

4. Arm Weakness Assessment (0-1 point):
This component evaluates motor function by testing the patient's ability to hold 
their arm in an elevated position for 10 seconds without drift or fall.

Assessment Protocol:
- Can hold arm up (0 points): Normal or minimal motor impairment
- Cannot hold arm up (1 point): Significant motor weakness or paralysis

Clinical Relevance:
- Simple, rapid assessment of motor function
- Reliable indicator of stroke presence
- Correlates with stroke severity
- Easy to perform in prehospital settings

Scoring and Risk Stratification:

Total Score Range: 0-4 points

Low Risk (0-1 points): LVO and Severe Stroke Less Likely
- Clinical significance: Lower probability of large vessel occlusion
- Stroke severity: Typically NIHSS <15
- Management approach: Standard stroke protocol with transport to nearest stroke-capable facility
- Clinical outcomes: Better prognosis for functional recovery
- Resource allocation: Standard stroke team activation

High Risk (2-4 points): LVO and Severe Stroke Likely
- Clinical significance: Higher probability of large vessel occlusion
- Stroke severity: Typically NIHSS ≥15
- Management approach: Consider direct transport to comprehensive stroke center
- Clinical outcomes: Higher risk for severe disability without intervention
- Resource allocation: Enhanced stroke team and interventional service activation

Performance Characteristics and Validation:

Severe Stroke Prediction (NIHSS ≥15):
- Sensitivity: 89% (at cutpoint ≥2)
- Specificity: 78% (at cutpoint ≥2)
- Area Under Curve (AUC): 0.89
- Positive Likelihood Ratio: 4.0
- Negative Likelihood Ratio: 0.14

Large Vessel Occlusion Prediction:
- Sensitivity: 83% (at cutpoint ≥2)
- Specificity: 40% (at cutpoint ≥2)
- Area Under Curve (AUC): 0.67
- Positive Likelihood Ratio: 1.4
- Negative Likelihood Ratio: 0.4

External Validation Studies:
Multiple external validation studies have confirmed the CP-SSS performance:
- C-statistic for LVO prediction: 0.85 in some validation cohorts
- Consistent performance across diverse populations
- Maintained accuracy when used by EMS personnel
- Effective in reducing time to treatment for appropriate patients

Clinical Implementation and Stroke Systems of Care:

Prehospital Triage Decision Making:
The CP-SSS supports evidence-based prehospital triage decisions by:
- Identifying patients who may benefit from direct transport to comprehensive stroke centers
- Reducing delays in accessing endovascular therapy
- Optimizing resource utilization across stroke care networks
- Maintaining access to IV thrombolysis while enhancing thrombectomy access

EMS Protocol Integration:
- Rapid assessment tool suitable for prehospital environment
- Minimal training requirements for EMS personnel
- Compatible with existing stroke assessment protocols
- Enhances decision-making without delaying care

Stroke Center Activation:
- Enables pre-notification of interventional teams
- Supports resource mobilization and preparation
- Facilitates parallel processing of IV thrombolysis and thrombectomy evaluation
- Improves door-to-treatment times

Quality Improvement Applications:

Performance Monitoring:
- Standardized assessment for quality metrics
- Supports outcome tracking and benchmarking
- Enables evaluation of stroke system performance
- Facilitates continuous improvement initiatives

Training and Education:
- Structured approach to stroke severity assessment
- Supports EMS education and competency development
- Provides objective framework for case review
- Enhances inter-rater reliability

Research Applications:
- Standardized tool for clinical research
- Enables stratification in stroke studies
- Supports health services research
- Facilitates multi-center collaboration

Implementation Considerations and Limitations:

Appropriate Use Cases:
- Patients with acute stroke symptoms
- Prehospital and emergency department settings
- Adults presenting within stroke treatment windows
- Systems with access to comprehensive stroke centers

Clinical Limitations:
- Should not delay IV thrombolysis when indicated
- Does not replace comprehensive neurological assessment
- Limited validation in posterior circulation strokes
- Requires clinical correlation and judgment

System Requirements:
- Access to comprehensive stroke centers
- Established stroke care protocols
- EMS training and competency maintenance
- Quality assurance and outcome monitoring

The Cincinnati Prehospital Stroke Severity Scale represents a significant advancement 
in stroke care by providing emergency medical services with an evidence-based tool 
for identifying patients with severe strokes who may benefit from direct transport 
to comprehensive stroke centers. This scale enhances stroke systems of care by 
optimizing patient triage while maintaining the critical principle of rapid access 
to appropriate stroke interventions.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CincinnatiPrehospitalStrokeSeverityScaleRequest(BaseModel):
    """
    Request model for Cincinnati Prehospital Stroke Severity Scale (CP-SSS)
    
    The Cincinnati Prehospital Stroke Severity Scale is a validated 4-component 
    assessment tool designed to predict large vessel occlusion (LVO) and severe 
    stroke in patients presenting with acute stroke symptoms. This tool was 
    specifically developed for use by emergency medical services personnel to 
    enhance prehospital stroke triage and guide transport decisions.
    
    Assessment Components and Clinical Significance:
    
    1. Conjugate Gaze Deviation Assessment:
    This component evaluates for horizontal conjugate gaze deviation, a powerful 
    predictor of cortical involvement and large vessel occlusion.
    
    Clinical Assessment Protocol:
    - Observe the patient's spontaneous eye position
    - Note any persistent deviation of both eyes to one side
    - Assess ability to overcome gaze preference when prompted
    - Document presence or absence of conjugate gaze deviation
    
    Scoring and Clinical Significance:
    - Present (2 points): Eyes deviated to one side, cannot overcome deviation
      * Strong predictor of large vessel occlusion
      * Indicates cortical gaze center involvement
      * Associated with anterior circulation strokes
      * Correlates with higher NIHSS scores
    
    - Absent (0 points): Normal eye movements or can overcome gaze preference
      * Lower likelihood of large vessel involvement
      * May indicate subcortical or smaller strokes
      * Better prognosis for functional outcomes
    
    2. Level of Consciousness - Questions Component:
    This assessment evaluates cognitive function and alertness through standardized 
    questions, providing insight into the severity of cerebral dysfunction.
    
    Standard Assessment Questions:
    - "How old are you?" or "What is your age?"
    - "What month is it?" or "What month are we in?"
    
    Scoring Framework:
    - Both questions answered correctly (0 points):
      * Normal cognitive function and alertness
      * Minimal cortical involvement
      * Better prognosis for recovery
      * Lower stroke severity likely
    
    - One question answered correctly (1 point):
      * Mild cognitive impairment or confusion
      * Moderate cortical dysfunction
      * Intermediate stroke severity
      * May indicate evolving stroke
    
    - Neither question answered correctly (2 points):
      * Significant cognitive impairment
      * Severe cortical dysfunction
      * High stroke severity likely
      * Strong predictor of poor outcomes without intervention
    
    3. Level of Consciousness - Commands Component:
    This component assesses comprehension and motor response through simple 
    commands, evaluating both cognitive and motor pathways.
    
    Standard Assessment Commands:
    - "Open and close your eyes"
    - "Grip and release your hand" (use non-paretic hand if weakness evident)
    
    Scoring and Interpretation:
    - Follows both commands (0 points):
      * Normal comprehension and motor function
      * Minimal cortical involvement
      * Lower stroke severity
      * Better functional prognosis
    
    - Follows one command (1 point):
      * Partial comprehension or motor impairment
      * Moderate cortical dysfunction
      * Intermediate stroke severity
      * May indicate selective pathway involvement
    
    - Follows neither command (2 points):
      * Severe comprehension deficit or motor impairment
      * Significant cortical dysfunction
      * High stroke severity
      * Strong predictor of severe disability
    
    4. Arm Weakness Assessment:
    This component provides a rapid evaluation of motor function by testing 
    arm strength and coordination.
    
    Assessment Protocol:
    - Have patient hold arm up at 90 degrees (sitting) or 45 degrees (lying)
    - Maintain position for 10 seconds
    - Observe for drift, weakness, or inability to maintain position
    - Test both arms if possible, document worst performance
    
    Scoring and Clinical Implications:
    - Can hold arm up (0 points):
      * Normal or minimal motor impairment
      * Lower stroke severity
      * Better functional prognosis
      * May indicate non-motor stroke or mild involvement
    
    - Cannot hold arm up (1 point):
      * Significant motor weakness or paralysis
      * Moderate to severe stroke likely
      * Motor pathway involvement
      * Higher risk for functional disability
    
    Clinical Decision Making and Risk Stratification:
    
    Low Risk (Total Score 0-1 points):
    - Clinical significance: Lower probability of large vessel occlusion
    - Expected stroke severity: Typically NIHSS <15
    - Transport decision: Transport to nearest stroke-capable facility
    - Management approach: Standard stroke protocol activation
    - Resource allocation: Routine stroke team notification
    - Prognosis: Better outcomes with standard stroke care
    
    High Risk (Total Score 2-4 points):
    - Clinical significance: Higher probability of large vessel occlusion
    - Expected stroke severity: Typically NIHSS ≥15
    - Transport decision: Consider direct transport to comprehensive stroke center
    - Management approach: Enhanced stroke protocol with thrombectomy preparation
    - Resource allocation: Immediate interventional team notification
    - Prognosis: Requires advanced interventions for optimal outcomes
    
    Implementation in EMS Protocols:
    
    Assessment Timing:
    - Perform after initial stroke screening (Cincinnati Prehospital Stroke Scale)
    - Complete within 2-3 minutes of patient contact
    - Document findings clearly for receiving facility
    - Communicate results during hospital notification
    
    Training Requirements:
    - Standardized assessment techniques
    - Recognition of positive findings
    - Understanding of clinical implications
    - Integration with transport protocols
    
    Quality Assurance:
    - Regular competency validation
    - Case review and feedback
    - Outcome tracking and analysis
    - Continuous protocol refinement
    
    References (Vancouver style):
    1. Katz BS, McMullan JT, Sucharew H, Adeoye O, Broderick JP. Design and validation of a 
    prehospital scale to predict stroke severity: the Cincinnati Prehospital Stroke 
    Severity Scale. Stroke. 2015 Jun;46(6):1508-12.
    2. McMullan JT, Katz B, Broderick J, Schmit P, Sucharew H, Adeoye O. Prospective 
    prehospital evaluation of the Cincinnati stroke triage assessment tool. Prehosp 
    Emerg Care. 2017 Jan-Feb;21(1):68-75.
    """
    
    conjugate_gaze_deviation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of conjugate gaze deviation. Present (2 pts): Eyes deviated to one side, strong predictor of LVO. Absent (0 pts): Normal eye movements",
        example="no"
    )
    
    level_of_consciousness_questions: Literal["both_correct", "one_correct", "neither_correct"] = Field(
        ...,
        description="Patient's ability to answer LOC questions (age and current month). Both correct (0 pts), One correct (1 pt), Neither correct (2 pts)",
        example="both_correct"
    )
    
    following_commands: Literal["both_commands", "one_command", "neither_command"] = Field(
        ...,
        description="Patient's ability to follow simple commands (open/close eyes, grip/release hand). Both commands (0 pts), One command (1 pt), Neither command (2 pts)",
        example="both_commands"
    )
    
    arm_holding_ability: Literal["can_hold", "cannot_hold"] = Field(
        ...,
        description="Patient's ability to hold arm up for 10 seconds without drift. Can hold (0 pts), Cannot hold (1 pt)",
        example="can_hold"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "conjugate_gaze_deviation": "no",
                "level_of_consciousness_questions": "both_correct",
                "following_commands": "both_commands",
                "arm_holding_ability": "can_hold"
            }
        }


class CincinnatiPrehospitalStrokeSeverityScaleResponse(BaseModel):
    """
    Response model for Cincinnati Prehospital Stroke Severity Scale (CP-SSS)
    
    The CP-SSS response provides comprehensive stroke severity assessment with 
    evidence-based risk stratification to guide prehospital triage and transport 
    decisions. The scale predicts large vessel occlusion (LVO) and severe stroke 
    (NIHSS ≥15) with high accuracy, enabling optimal patient placement within 
    stroke systems of care.
    
    Risk Stratification and Clinical Decision Making:
    
    Low Risk Category (Score 0-1 points): LVO and Severe Stroke Less Likely
    
    Clinical Characteristics:
    - Lower probability of large vessel occlusion (sensitivity 83% for cutpoint ≥2)
    - Expected stroke severity typically NIHSS <15
    - May represent smaller vessel strokes or less severe presentations
    - Better prognosis for functional recovery with standard stroke care
    - Lower risk for severe disability or death
    
    Transport and Management Recommendations:
    - Transport to nearest stroke-capable facility appropriate
    - Standard stroke protocol activation sufficient
    - IV thrombolysis evaluation within appropriate time windows
    - Routine stroke team notification and resource allocation
    - Consider transfer if large vessel occlusion identified on imaging
    
    Clinical Outcomes:
    - Higher likelihood of good functional outcomes (mRS 0-2)
    - Lower mortality risk compared to severe strokes
    - Shorter hospital length of stay typical
    - Less resource-intensive care requirements
    
    High Risk Category (Score 2-4 points): LVO and Severe Stroke Likely
    
    Clinical Characteristics:
    - Higher probability of large vessel occlusion requiring thrombectomy
    - Expected stroke severity typically NIHSS ≥15 (89% sensitivity)
    - Strong predictor of cortical involvement and significant deficits
    - Higher risk for severe disability without advanced interventions
    - Time-sensitive need for comprehensive stroke care
    
    Transport and Management Recommendations:
    - Strong consideration for direct transport to comprehensive stroke center
    - Pre-notification of interventional radiology/neurology teams
    - Expedited imaging and evaluation protocols
    - Parallel processing for IV thrombolysis and thrombectomy preparation
    - Enhanced resource mobilization and team activation
    
    Advanced Care Considerations:
    - Immediate vascular imaging (CTA or perfusion studies)
    - Rapid evaluation for endovascular therapy eligibility
    - Coordination between emergency, stroke, and interventional teams
    - Family notification and counseling regarding severity
    - Potential for extended care needs and rehabilitation planning
    
    Performance Characteristics and Validation:
    
    Severe Stroke Prediction Accuracy:
    - Sensitivity: 89% for detecting NIHSS ≥15 (at cutpoint ≥2)
    - Specificity: 78% for excluding NIHSS <15 (at cutpoint ≥2)
    - Area Under Curve (AUC): 0.89 for severe stroke prediction
    - Positive Predictive Value: Variable based on stroke prevalence
    - Negative Predictive Value: High for excluding severe strokes
    
    Large Vessel Occlusion Detection:
    - Sensitivity: 83% for detecting LVO (at cutpoint ≥2)
    - Specificity: 40% for excluding LVO (at cutpoint ≥2)
    - Area Under Curve (AUC): 0.67 for LVO prediction
    - Clinical utility: Better sensitivity than specificity for LVO detection
    - External validation: Consistent performance across multiple studies
    
    Stroke Systems of Care Integration:
    
    Prehospital Applications:
    - Rapid assessment tool for emergency medical services
    - Standardized approach to stroke severity evaluation
    - Evidence-based transport decision support
    - Quality improvement metric for stroke care systems
    - Training tool for EMS education programs
    
    Emergency Department Utilization:
    - Triage support for stroke team activation levels
    - Resource allocation guidance for imaging and interventions
    - Communication tool with consulting services
    - Documentation standard for stroke quality measures
    - Research tool for stroke outcome studies
    
    Healthcare System Benefits:
    - Optimized patient flow within stroke networks
    - Improved access to appropriate levels of care
    - Enhanced coordination between care facilities
    - Better resource utilization and cost-effectiveness
    - Reduced time to definitive treatment
    
    Quality Assurance and Continuous Improvement:
    
    Performance Monitoring:
    - Correlation between CP-SSS scores and actual stroke severity
    - Transport decision accuracy and patient outcomes
    - Time to treatment metrics for high-risk patients
    - Resource utilization analysis and optimization
    - Comparative effectiveness with other screening tools
    
    Training and Competency:
    - Standardized assessment techniques for reliability
    - Inter-rater agreement monitoring and improvement
    - Continuing education requirements and updates
    - Case-based learning and skill development
    - Integration with stroke certification programs
    
    Clinical Research Applications:
    - Risk stratification for stroke research studies
    - Outcome prediction modeling and validation
    - Health services research and policy development
    - Cost-effectiveness analysis of stroke care interventions
    - Population health assessment and planning
    
    Implementation Considerations and Limitations:
    
    Appropriate Clinical Context:
    - Designed for patients with acute stroke symptoms
    - Most applicable within first few hours of symptom onset
    - Requires trained healthcare providers for accurate assessment
    - Should complement rather than replace clinical judgment
    - Best utilized within established stroke care systems
    
    Clinical Limitations:
    - Should not delay IV thrombolysis when indicated
    - Limited validation in posterior circulation strokes
    - May have reduced accuracy in certain patient populations
    - Requires correlation with imaging findings
    - Does not predict all aspects of stroke prognosis
    
    System Requirements:
    - Access to comprehensive stroke centers for high-risk patients
    - Established protocols for transport and triage decisions
    - Training programs for consistent implementation
    - Quality assurance mechanisms and outcome tracking
    - Integration with electronic health records and reporting systems
    
    The Cincinnati Prehospital Stroke Severity Scale represents a valuable advancement 
    in stroke care by providing evidence-based decision support for identifying 
    patients with severe strokes who require specialized care. This tool enhances 
    the efficiency and effectiveness of stroke systems while maintaining the 
    fundamental principle of rapid access to appropriate stroke treatments.
    
    Reference: Katz BS, et al. Stroke. 2015;46(6):1508-12.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=7,
        description="Cincinnati Prehospital Stroke Severity Scale score (0-7 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and transport recommendations",
        example="CP-SSS Score 1: Low probability of large vessel occlusion and severe stroke (NIHSS <15). Standard stroke protocol appropriate with transport to nearest stroke-capable facility."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="LVO and severe stroke less likely"
    )
    
    scoring_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of component scores, performance characteristics, and clinical guidance",
        example={
            "component_scores": {
                "conjugate_gaze_deviation": {
                    "finding": "Absent",
                    "points": 0,
                    "max_points": 2,
                    "description": "Horizontal conjugate gaze deviation",
                    "clinical_significance": "Strong predictor of cortical involvement and large vessel occlusion"
                },
                "level_of_consciousness_questions": {
                    "finding": "Both questions answered correctly",
                    "points": 0,
                    "max_points": 2,
                    "description": "Level of consciousness - questions component",
                    "clinical_significance": "Assesses alertness and cognitive function"
                },
                "following_commands": {
                    "finding": "Follows both commands",
                    "points": 0,
                    "max_points": 2,
                    "description": "Level of consciousness - commands component",
                    "clinical_significance": "Evaluates comprehension and motor response"
                },
                "arm_holding_ability": {
                    "finding": "Can hold arm up for 10 seconds",
                    "points": 0,
                    "max_points": 1,
                    "description": "Arm weakness assessment",
                    "clinical_significance": "Motor function indicator"
                }
            },
            "score_summary": {
                "total_score": 1,
                "max_possible_score": 4,
                "cutpoint_threshold": 2,
                "risk_category": "Low Risk"
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "CP-SSS Score 1: Low probability of large vessel occlusion and severe stroke (NIHSS <15). Standard stroke protocol appropriate with transport to nearest stroke-capable facility.",
                "stage": "Low Risk",
                "stage_description": "LVO and severe stroke less likely",
                "scoring_breakdown": {
                    "component_scores": {
                        "conjugate_gaze_deviation": {
                            "finding": "Absent",
                            "points": 0,
                            "max_points": 2,
                            "description": "Horizontal conjugate gaze deviation"
                        },
                        "level_of_consciousness_questions": {
                            "finding": "Both questions answered correctly",
                            "points": 0,
                            "max_points": 2,
                            "description": "Level of consciousness - questions component"
                        }
                    },
                    "score_summary": {
                        "total_score": 1,
                        "max_possible_score": 4,
                        "cutpoint_threshold": 2,
                        "risk_category": "Low Risk"
                    }
                }
            }
        }