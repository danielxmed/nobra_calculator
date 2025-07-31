"""
CHIP (CT in Head Injury Patients) Prediction Rule Router

Endpoint for calculating CHIP prediction rule for CT imaging decisions in minor head trauma.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.chip_prediction_rule import (
    ChipPredictionRuleRequest,
    ChipPredictionRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/chip_prediction_rule",
    response_model=ChipPredictionRuleResponse,
    summary="Calculate CHIP (CT in Head Injury Patients) Prediction Rule",
    description="Predicts need for CT imaging in patients with minor head trauma to detect potential intracranial injuries",
    response_description="The calculated chip prediction rule with interpretation",
    operation_id="calculate_chip_prediction_rule"
)
async def calculate_chip_prediction_rule(request: ChipPredictionRuleRequest):
    """
    Calculates CHIP (CT in Head Injury Patients) Prediction Rule
    
    The CHIP (CT in Head Injury Patients) Prediction Rule is a validated clinical 
    decision tool designed to guide CT imaging decisions in patients with minor head 
    trauma. This evidence-based rule helps emergency physicians optimize resource 
    utilization while maintaining high sensitivity for clinically important 
    intracranial injuries.
    
    **Development and Validation History**:
    
    **Original Development (2007)**:
    - Developed by Smits et al. in the Netherlands
    - Multi-center prospective study across 4 university hospitals
    - 3,181 patients included (February 2002 to August 2004)
    - 243 patients (7.6%) had intracranial traumatic CT findings
    - 17 patients (0.5%) underwent neurosurgical intervention
    - Achieved 100% sensitivity for neurosurgical interventions
    - Specificity of 23-30% for reducing unnecessary CT scans
    
    **External Validation**:
    - Validated against Canadian CT Head Rule and New Orleans Criteria
    - Demonstrated superior performance in European healthcare settings
    - Confirmed high sensitivity for clinically important injuries
    - Established as reliable decision support tool
    
    **Recent Updates (2022)**:
    - Updated model based on multicenter consecutive case series
    - 4,557 patients included with modern CT utilization patterns
    - 383 patients (8.4%) with traumatic findings on CT
    - 73 patients (1.6%) with potential neurosurgical lesions
    - 26 patients (0.6%) actually underwent neurosurgery or died
    - Updated model maintained similar performance to original
    
    **CHIP Rule Clinical Framework**:
    
    **Target Population and Inclusion Criteria**:
    
    **Age Requirements**:
    - Adults ≥16 years of age
    - Pediatric populations require different decision rules (PECARN, CHALICE)
    - Not validated for geriatric-specific considerations beyond age criteria
    
    **Injury Characteristics**:
    - Minor head injury with Glasgow Coma Scale 13-15
    - Blunt trauma mechanism (not penetrating injury)
    - Presentation within 24 hours of injury
    - Patients being considered for CT imaging evaluation
    
    **Clinical Presentation**:
    - Any level of consciousness from GCS 13-15
    - With or without loss of consciousness
    - With or without post-traumatic amnesia
    - May include focal neurological symptoms
    - External signs of head trauma not required
    
    **Two-Tier Criteria System**:
    
    **Major Criteria (Any ONE present → CT recommended)**:
    
    **High-Energy Mechanism Factors**:
    
    **Pedestrian/Cyclist vs. Vehicle Collision**:
    - Motor vehicle collision involving pedestrian or cyclist
    - Represents high-energy transfer mechanism
    - Associated with multiple trauma and severe brain injury
    - High likelihood of intracranial pathology
    - Often involves multiple impact points and acceleration-deceleration
    
    **Ejected from Vehicle**:
    - Patient thrown from motor vehicle during accident
    - Indicates extremely high-energy mechanism
    - Associated with severe multisystem trauma
    - Very high risk for traumatic brain injury
    - Often involves multiple impact surfaces and trajectories
    
    **Neurological Dysfunction Indicators**:
    
    **Post-traumatic Vomiting**:
    - Vomiting following head trauma (not related to other causes)
    - May indicate increased intracranial pressure
    - Can suggest brain stem dysfunction or vestibular injury
    - Associated with moderate to severe brain injury
    - Requires immediate evaluation for space-occupying lesions
    
    **Extended Post-traumatic Amnesia (≥4 hours)**:
    - Memory loss lasting 4 hours or longer after trauma
    - Indicates significant disruption of memory formation
    - Associated with hippocampal and temporal lobe injury
    - Strong predictor of intracranial pathology
    - May include both retrograde and anterograde components
    
    **Depressed Level of Consciousness**:
    
    **Glasgow Coma Scale <15**:
    - Any depression below normal consciousness level
    - Indicates ongoing neurological dysfunction
    - May reflect structural brain injury or increased pressure
    - Requires immediate assessment for treatable pathology
    - Even subtle changes (GCS 14) carry significant risk
    
    **GCS Deterioration ≥2 points**:
    - Significant decline in neurological status
    - Suggests progressive intracranial pathology
    - May indicate expanding hematoma or increasing edema
    - Requires urgent imaging and neurosurgical evaluation
    - Represents evolving brain injury
    
    **Physical Examination Findings**:
    
    **Clinical Signs of Skull Fracture**:
    - Palpable step-off or depression in skull contour
    - Crepitus on palpation of scalp
    - Visible fracture lines or bone fragments
    - Battle's sign or raccoon eyes (basilar skull fracture)
    - Hemotympanum or CSF otorrhea/rhinorrhea
    
    **Post-traumatic Seizure**:
    - Seizure activity following head trauma
    - Indicates cortical irritation or structural damage
    - May be focal or generalized
    - Associated with penetrating injury or contusion
    - Requires evaluation for underlying structural abnormalities
    
    **Patient Risk Factors**:
    
    **Anticoagulant Use**:
    - Current therapeutic anticoagulation therapy
    - Includes warfarin, DOACs, heparin products
    - Significantly increases intracranial hemorrhage risk
    - Even minor trauma mechanisms pose substantial risk
    - Requires lower threshold for imaging
    
    **Advanced Age (≥60 years)**:
    - Age-related brain atrophy increases subdural space
    - Fragile bridging veins more susceptible to tearing
    - Increased risk of anticoagulant-related bleeding
    - Higher likelihood of comorbid conditions
    - Greater vulnerability to minor trauma mechanisms
    
    **Minor Criteria (TWO OR MORE present → CT recommended)**:
    
    **Trauma Mechanism**:
    
    **Fall from Any Elevation**:
    - Fall from standing height or greater
    - Includes falls from chairs, beds, stairs, ladders
    - Mechanism with potential for direct head impact
    - May involve acceleration-deceleration forces
    - Risk varies with surface hardness and impact angle
    
    **Memory and Consciousness Disturbances**:
    
    **Persistent Anterograde Amnesia**:
    - Ongoing difficulty forming new memories
    - Inability to consolidate information post-trauma
    - Indicates hippocampal or widespread dysfunction
    - May persist despite normal level of consciousness
    - Suggests moderate brain injury severity
    
    **Moderate Post-traumatic Amnesia (2-<4 hours)**:
    - Memory loss of intermediate duration
    - Less severe than major criterion threshold
    - Still indicates significant brain dysfunction
    - Combined with other factors increases risk
    - May involve both retrograde and anterograde components
    
    **Loss of Consciousness**:
    - Any period of unconsciousness, regardless of duration
    - Indicates brain dysfunction at time of injury
    - May be witnessed or suspected based on circumstances
    - Duration may not correlate with injury severity
    - Requires careful assessment for associated injuries
    
    **Physical Signs and Neurological Changes**:
    
    **Skull Contusion**:
    - Visible bruising, swelling, or hematoma on scalp
    - Indicates significant impact to head
    - May overlie skull fracture or brain contusion
    - External sign of trauma mechanism severity
    - Requires assessment for underlying injury
    
    **Neurologic Deficit**:
    - Any focal neurological finding on examination
    - Includes motor weakness, sensory loss, coordination problems
    - Cranial nerve dysfunction or abnormal reflexes
    - Speech, language, or cognitive impairments
    - May be subtle and require careful assessment
    
    **Mild Neurological Decline**:
    
    **GCS Deterioration of 1 Point**:
    - Subtle decline in neurological status
    - May indicate developing pathology
    - Requires serial assessments and close monitoring
    - Even minor changes may be clinically significant
    - Often precedes more dramatic deterioration
    
    **Intermediate Age Factor**:
    
    **Age 40-60 Years**:
    - Intermediate risk category between young and elderly
    - Beginning of age-related vulnerability increase
    - Higher risk than younger patients
    - Combined with other factors increases significance
    - Represents transitional risk period
    
    **Clinical Decision Algorithm and Implementation**:
    
    **Risk Stratification Framework**:
    
    **High Risk (Any Major Criterion Present)**:
    - **Recommendation**: CT imaging strongly recommended
    - **Rationale**: High likelihood of intracranial pathology
    - **Management**: Proceed with immediate CT evaluation
    - **Follow-up**: Neurosurgical consultation if positive findings
    - **Disposition**: Based on imaging results and clinical condition
    
    **Moderate-High Risk (≥2 Minor Criteria Present)**:
    - **Recommendation**: CT imaging recommended
    - **Rationale**: Moderate to high risk requiring evaluation
    - **Management**: Proceed with CT imaging
    - **Considerations**: Multiple risk factors compound individual risks
    - **Monitoring**: Close observation during evaluation process
    
    **Low-Moderate Risk (1 Minor Criterion Present)**:
    - **Recommendation**: Clinical judgment required
    - **Rationale**: Individual assessment of risk-benefit ratio
    - **Considerations**: Patient reliability, observation capability, preferences
    - **Alternatives**: Close observation with serial assessments
    - **Follow-up**: Clear return instructions if imaging deferred
    
    **Low Risk (No Criteria Present)**:
    - **Recommendation**: CT imaging not indicated
    - **Rationale**: Very low likelihood of clinically important injury
    - **Management**: Clinical observation and discharge planning
    - **Education**: Head injury precautions and return criteria
    - **Quality**: Appropriate resource utilization
    
    **Integration with Clinical Practice**:
    
    **Emergency Department Workflow**:
    - Systematic evaluation of all CHIP criteria
    - Documentation of present and absent criteria
    - Risk stratification based on criteria analysis
    - Clinical decision-making with rule guidance
    - Patient and family communication about recommendations
    
    **Clinical Judgment Integration**:
    - Rule provides framework, not replacement for assessment
    - Individual patient factors may modify recommendations
    - Physician experience and clinical gestalt remain important
    - Medical-legal considerations in decision-making
    - Shared decision-making when appropriate
    
    **Quality Improvement Applications**:
    - Standardized approach to minor head trauma
    - Reduction in inappropriate CT utilization
    - Performance metrics for emergency department
    - Training tool for residents and advanced practitioners
    - Research applications for trauma outcomes
    
    **Special Considerations and Limitations**:
    
    **Rule Limitations**:
    - Not validated for pediatric populations
    - Based primarily on European healthcare settings
    - May not account for all individual risk factors
    - Requires clinical interpretation and judgment
    - Should be updated with emerging evidence
    
    **Implementation Considerations**:
    - Training required for appropriate application
    - Integration with electronic health records
    - Quality assurance and outcome monitoring
    - Regular review of rule performance
    - Adaptation to local practice patterns
    
    **Patient Communication Framework**:
    - Explanation of risk assessment findings
    - Discussion of CT recommendation rationale
    - Shared decision-making process when appropriate
    - Clear instructions for observation or follow-up
    - Head injury precautions and return criteria
    
    This calculator provides evidence-based decision support for CT imaging 
    in minor head trauma, optimizing patient care while promoting appropriate 
    resource utilization in emergency department settings.
    
    Args:
        request: CHIP clinical criteria assessment parameters
        
    Returns:
        ChipPredictionRuleResponse: CT recommendation with risk stratification and clinical rationale
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("chip_prediction_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHIP Prediction Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return ChipPredictionRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHIP Prediction Rule",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )