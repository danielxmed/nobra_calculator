"""
Geriatric Depression Scale (GDS-15) Router

Endpoint for calculating GDS-15 depression screening score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.gds_15 import (
    Gds15Request,
    Gds15Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gds_15",
    response_model=Gds15Response,
    summary="Calculate Geriatric Depression Scale (GDS-15)",
    description="Identifies possible depression in older adults aged 55 and older. The 15-item version is a brief, reliable screening tool that uses simple yes/no questions to assess depressive symptoms specific to the geriatric population over the past week",
    response_description="The calculated gds 15 with interpretation",
    operation_id="calculate_gds_15"
)
async def calculate_gds_15(request: Gds15Request):
    """
    Calculates Geriatric Depression Scale (GDS-15)
    
    The Geriatric Depression Scale (GDS-15) is a validated screening instrument specifically 
    designed for identifying possible depression in adults aged 55 and older. This brief, 
    15-item version provides reliable assessment using simple yes/no questions that focus 
    on psychological rather than somatic symptoms, making it particularly suitable for 
    the geriatric population where medical illness may confound other depression screening tools.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    Depression screening and severity assessment in older adults to facilitate early 
    identification, appropriate referral, and treatment monitoring in various healthcare 
    settings including primary care, geriatric clinics, and residential care facilities.
    
    **Key Clinical Advantages**:
    
    **Age-Specific Design and Validation**:
    - Specifically developed and extensively validated for adults aged 55 and older
    - Avoids somatic symptoms that may be confounded by medical comorbidities common in aging
    - Uses simple yes/no response format that accommodates cognitive changes in older adults
    - Can be self-administered or clinician-administered with equal effectiveness
    
    **Psychometric Excellence**:
    - Demonstrated sensitivity of 81% and specificity of 78% for identifying late-life depression
    - Strong internal consistency and test-retest reliability across diverse geriatric populations
    - Validated across multiple clinical settings and cultural contexts
    - Excellent performance characteristics compared to longer depression screening instruments
    
    **Clinical Utility Framework**:
    - Brief administration time (5-10 minutes) suitable for busy clinical settings
    - Clear interpretation guidelines with established cutoff scores for severity levels
    - Useful for initial screening, treatment monitoring, and population health assessment
    - Integration capability with electronic health records and clinical decision support systems
    
    **Evidence-Based Risk Stratification**:
    
    **Normal Range (0-4 points)**:
    - Represents absence of clinically significant depressive symptoms
    - Found in approximately 60-70% of community-dwelling older adults
    - Supports routine care approach with annual screening and health promotion
    - Allows focus on prevention strategies and maintaining psychological well-being
    
    **Mild Depression (5-7 points)**:
    - Indicates subthreshold depression requiring attention and monitoring
    - Present in approximately 15-20% of older adults in primary care settings
    - May represent early depression or adjustment difficulties that could progress
    - Benefits from counseling, supportive interventions, and close follow-up
    
    **Moderate Depression (8-9 points)**:
    - Suggests clinically significant depression requiring active treatment
    - Found in approximately 8-12% of older adults in clinical settings
    - Associated with functional impairment and reduced quality of life
    - Indicates need for psychiatric evaluation and evidence-based treatment interventions
    
    **Severe Depression (10-15 points)**:
    - Indicates severe depression requiring urgent comprehensive evaluation
    - Present in approximately 3-5% of community-dwelling older adults
    - Associated with high suicide risk, major functional impairment, and potential hospitalization needs
    - Requires immediate psychiatric consultation and intensive treatment approaches
    
    **Clinical Decision Support Applications**:
    
    **Primary Care Integration**:
    - Systematic screening protocol for older adult patients during routine visits
    - Risk stratification to guide referral decisions and treatment intensity
    - Monitoring tool for patients receiving depression treatment
    - Quality improvement metrics for geriatric mental health care
    
    **Specialized Geriatric Settings**:
    - Admission screening in geriatric psychiatry and psychology services
    - Pre-treatment assessment and outcome monitoring in mental health programs
    - Research tool for epidemiological studies and clinical trials
    - Population health screening in community and residential care settings
    
    **Special Clinical Considerations**:
    
    **Medical Comorbidity Interface**:
    - Particularly valuable because it avoids somatic symptoms that may be due to medical illness
    - Can be used effectively in patients with chronic medical conditions
    - Helps distinguish depression from medical illness-related symptoms
    - Useful in hospitalized patients and those receiving medical treatment
    
    **Cognitive Impairment Considerations**:
    - May be administered to patients with mild cognitive impairment
    - Results should be interpreted cautiously in patients with moderate to severe cognitive impairment
    - Consider informant input for validation in patients with cognitive limitations
    - May require simplified administration or repetition of questions
    
    **Suicide Risk Assessment Integration**:
    - Questions 11 and 14 are particularly important indicators of suicide risk
    - Any concerning responses should trigger immediate comprehensive suicide risk assessment
    - Have crisis intervention protocols and resources readily available
    - Consider immediate referral and safety planning for high-risk patients
    
    **Cultural and Language Adaptations**:
    - Available in multiple validated language translations
    - Consider cultural concepts of depression and emotional expression
    - May require cultural adaptation for different ethnic and cultural groups
    - Use qualified interpreters when language barriers exist
    
    **Quality Improvement and Population Health**:
    
    **Healthcare System Applications**:
    - Standardized screening protocols across healthcare organizations
    - Performance metrics for depression screening and treatment rates
    - Resource allocation planning for geriatric mental health services
    - Cost-effectiveness analysis of depression screening and treatment programs
    
    **Research and Epidemiological Studies**:
    - Population health surveillance for late-life depression prevalence
    - Evaluation of depression prevention and treatment interventions
    - Health services research on access to geriatric mental health care
    - Longitudinal studies of depression trajectories in aging populations
    
    **Clinical Training and Education**:
    - Training tool for healthcare providers in geriatric depression assessment
    - Educational resource for understanding late-life depression presentation
    - Quality assurance for consistent depression screening practices
    - Professional development in geriatric mental health competencies
    
    Args:
        request: Patient responses to 15 questions about mood, interest, energy, 
                self-worth, and outlook covering the past week, using simple yes/no 
                format suitable for older adults
        
    Returns:
        Gds15Response: GDS-15 total score with detailed severity assessment, 
                      evidence-based clinical recommendations, and comprehensive 
                      management guidance based on validated cutoff thresholds 
                      for geriatric depression screening
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gds_15", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Geriatric Depression Scale (GDS-15)",
                    "details": {"parameters": parameters}
                }
            )
        
        return Gds15Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GDS-15 calculation",
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
                "message": "Internal error in GDS-15 calculation",
                "details": {"error": str(e)}
            }
        )