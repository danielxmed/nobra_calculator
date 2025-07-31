"""
GCS-Pupils Score Router

Endpoint for calculating GCS-Pupils Score for traumatic brain injury assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.gcs_pupils_score import (
    GcsPupilsScoreRequest,
    GcsPupilsScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gcs_pupils_score",
    response_model=GcsPupilsScoreResponse,
    summary="Calculate GCS-Pupils Score",
    description="The GCS-Pupils Score (GCS-P) combines the Glasgow Coma Scale with pupillary reactivity assessment to provide enhanced prognostic accuracy in traumatic brain injury patients. This extended index offers improved prediction of 6-month mortality and unfavorable outcomes, particularly in patients with severe brain injury where standard GCS may be limited.",
    response_description="The calculated gcs pupils score with interpretation",
    operation_id="gcs_pupils_score"
)
async def calculate_gcs_pupils_score(request: GcsPupilsScoreRequest):
    """
    Calculates GCS-Pupils Score for Traumatic Brain Injury Assessment
    
    The GCS-Pupils Score (GCS-P) combines the Glasgow Coma Scale with pupillary reactivity 
    assessment to provide enhanced prognostic accuracy in traumatic brain injury patients. 
    This extended index offers improved prediction of 6-month mortality and unfavorable outcomes, 
    particularly in patients with severe brain injury where standard GCS may be limited.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    Enhanced prognostic assessment in traumatic brain injury through integration of consciousness 
    level (GCS) and brainstem function (pupillary reactivity) into a single, evidence-based score.
    
    **Key Clinical Advantages**:
    
    **Enhanced Prognostic Discrimination**:
    - Extends prognostic range from GCS 3-15 to GCS-P 1-17 points
    - Provides better discrimination in severe TBI where GCS scores cluster at low values
    - Incorporates brainstem function assessment through pupillary reactivity
    - Offers continuous relationship between score and outcomes
    
    **Evidence-Based Risk Stratification**:
    - Derived from large international databases (IMPACT and CRASH)
    - Validated 6-month mortality and unfavorable outcome predictions
    - Population-based risk estimates for informed clinical decision-making
    - Quantitative support for family counseling and goals of care discussions
    
    **Clinical Practicality**:
    - Uses readily available bedside assessments
    - Simple arithmetic combination of standard neurological evaluations
    - No additional equipment or specialized training required
    - Can be calculated repeatedly for monitoring progression
    
    **Assessment Components and Clinical Interpretation**:
    
    **Glasgow Coma Scale Components**:
    
    **Eye Opening Response (1-4 points)**:
    - **4 - Spontaneous**: Normal arousal and brainstem function
    - **3 - To voice**: Mild arousal impairment, requires verbal stimulation
    - **2 - To pain**: Significant arousal impairment, requires painful stimulation
    - **1 - None**: Severe brainstem dysfunction or mechanical obstruction
    
    **Verbal Response (1-5 points)**:
    - **5 - Oriented**: Normal cognitive function and language processing
    - **4 - Confused**: Mild cognitive impairment with preserved language
    - **3 - Inappropriate words**: Moderate language dysfunction
    - **2 - Incomprehensible sounds**: Severe language impairment
    - **1 - None**: Complete absence of vocalization
    
    **Motor Response (1-6 points)**:
    - **6 - Obeys commands**: Normal motor pathways and comprehension
    - **5 - Localizes pain**: Purposeful response to painful stimuli
    - **4 - Withdrawal from pain**: Appropriate but non-purposeful response
    - **3 - Flexion to pain**: Abnormal flexor response (decorticate posturing)
    - **2 - Extension to pain**: Abnormal extensor response (decerebrate posturing)
    - **1 - None**: Complete absence of motor response
    
    **Pupillary Reactivity Assessment**:
    - **Both reactive (0 points)**: Normal brainstem function and cranial nerve III integrity
    - **One unreactive (1 point)**: Unilateral brainstem dysfunction or focal pathology
    - **Both unreactive (2 points)**: Bilateral brainstem dysfunction or severe ICP
    
    **Clinical Decision Support Framework**:
    
    **Risk Stratification and Management**:
    
    **Extremely Severe (GCS-P 1-3)**:
    - **6-Month Mortality**: 40-75%
    - **Management**: Intensive monitoring, family meetings, goals of care discussions
    - **Focus**: Secondary brain injury prevention, supportive care decisions
    
    **Severe (GCS-P 4-6)**:
    - **6-Month Mortality**: 25-40%
    - **Management**: Aggressive supportive care, early rehabilitation planning
    - **Focus**: Comprehensive monitoring, family support, recovery optimization
    
    **Moderate (GCS-P 7-9)**:
    - **6-Month Mortality**: 17-20%
    - **Management**: Close monitoring, early rehabilitation intervention
    - **Focus**: Prevention of complications, functional outcome optimization
    
    **Mild-Moderate (GCS-P 10-12)**:
    - **6-Month Mortality**: 9-17%
    - **Management**: Regular monitoring, comprehensive rehabilitation
    - **Focus**: Symptom management, return to function planning
    
    **Mild (GCS-P 13-17)**:
    - **6-Month Mortality**: 3-7%
    - **Management**: Symptom monitoring, outpatient follow-up
    - **Focus**: Post-concussive syndrome prevention, quality of life
    
    **Clinical Applications and Use Cases**:
    
    **Acute Care Decision-Making**:
    - Treatment intensity and resource allocation decisions
    - Intensive care admission and monitoring level determination
    - Neurosurgical intervention timing and candidacy assessment
    - Family communication and prognostic counseling support
    
    **Research and Quality Improvement**:
    - Clinical trial stratification and endpoint prediction
    - Trauma center outcome benchmarking and quality metrics
    - Population-based TBI surveillance and epidemiological studies
    - Healthcare resource planning and utilization optimization
    
    **Long-term Care Planning**:
    - Rehabilitation potential assessment and program selection
    - Discharge planning and care transition coordination
    - Family education and support service connection
    - Long-term outcome monitoring and follow-up planning
    
    **Important Clinical Considerations**:
    
    **Assessment Limitations**:
    - Population-based predictions may not apply to individual patients
    - Confounding factors (medications, intubation, trauma) may affect accuracy
    - Serial assessments more valuable than single time-point evaluation
    - Should supplement, not replace, comprehensive clinical judgment
    
    **Prognostic Communication**:
    - Use quantitative estimates to inform, not dictate, clinical decisions
    - Emphasize that outcomes exist on a spectrum with individual variation
    - Maintain appropriate hope while providing realistic expectations
    - Support shared decision-making with evidence-based information
    
    **Quality Assurance**:
    - Ensure standardized assessment techniques across providers
    - Document timing, examiner, and any confounding factors
    - Consider inter-rater reliability and training needs
    - Regular calibration of assessment accuracy and consistency
    
    Args:
        request: Patient neurological assessment data including Glasgow Coma Scale components 
                (eye opening, verbal response, motor response) and pupillary reactivity status
        
    Returns:
        GcsPupilsScoreResponse: GCS-Pupils score with component breakdown, evidence-based 
                               6-month outcome predictions, and comprehensive clinical 
                               interpretation with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gcs_pupils_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GCS-Pupils Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GcsPupilsScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GCS-Pupils Score calculation",
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
                "message": "Internal error in GCS-Pupils Score calculation",
                "details": {"error": str(e)}
            }
        )