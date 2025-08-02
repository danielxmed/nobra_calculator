"""
Major Depression Index Router

Endpoint for calculating Major Depression Inventory (MDI) for depression screening and assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.major_depression_index import (
    MajorDepressionIndexRequest,
    MajorDepressionIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/major_depression_index",
    response_model=MajorDepressionIndexResponse,
    summary="Calculate Major Depression Inventory (MDI)",
    description="Calculates the Major Depression Inventory (MDI), a WHO-developed self-report questionnaire "
                "that uniquely provides both diagnostic assessment and severity grading for depression. Based on "
                "ICD-10 and DSM-IV criteria, the MDI consists of 10 items covering core symptoms of major depression "
                "over the past 2 weeks. The calculator assesses both core symptoms (depressed mood, loss of interest) "
                "and additional symptoms (energy, confidence, guilt, suicidal ideation, concentration, psychomotor "
                "changes, sleep). It provides severity classification (No/Mild/Moderate/Severe Depression), diagnostic "
                "criteria assessment, and critical suicide risk flagging. The MDI is available free of charge, "
                "translated into seven languages, and widely used in clinical practice, research, and epidemiological "
                "studies. Essential for depression screening in primary care and mental health settings, monitoring "
                "treatment response, and clinical trial outcome assessment. Results require clinical interpretation "
                "and should be combined with comprehensive clinical interview for formal diagnosis.",
    response_description="The calculated MDI score with severity classification, diagnostic assessment, and clinical recommendations",
    operation_id="major_depression_index"
)
async def calculate_major_depression_index(request: MajorDepressionIndexRequest):
    """
    Calculates Major Depression Inventory (MDI) for comprehensive depression assessment
    
    The Major Depression Inventory is a WHO-developed instrument that provides both diagnostic
    assessment and severity grading for depression using ICD-10 and DSM-IV criteria.
    
    Historical Background:
    Developed by Professor Per Bech in Denmark in collaboration with the WHO, the MDI
    was created to address the need for a standardized, freely available depression
    assessment tool that could provide both diagnostic and severity information.
    Unlike other depression scales, the MDI is specifically designed to align with
    formal diagnostic criteria while remaining practical for clinical use.
    
    Clinical Applications:
    
    Primary Care Settings:
    - Initial depression screening for patients presenting with mood symptoms
    - Routine mental health screening in at-risk populations
    - Monitoring treatment response and medication adjustments
    - Decision-making for referral to mental health specialists
    
    Mental Health Settings:
    - Comprehensive depression assessment and diagnosis
    - Treatment planning and goal setting
    - Outcome measurement for psychotherapy and pharmacotherapy
    - Monitoring for treatment-resistant depression
    
    Research Applications:
    - Epidemiological studies of depression prevalence
    - Clinical trial outcome assessment
    - Population health surveys and screening programs
    - Longitudinal studies of depression course and outcomes
    
    Diagnostic Criteria Assessment:
    
    Core Symptoms (DSM-IV/ICD-10):
    1. Depressed mood most of the day, nearly every day
    2. Markedly diminished interest or pleasure in activities
    
    Additional Symptoms:
    3. Fatigue or loss of energy
    4. Feelings of worthlessness or inappropriate guilt
    5. Diminished ability to think or concentrate
    6. Psychomotor agitation or retardation
    7. Sleep disturbances (insomnia or hypersomnia)
    8. Suicidal ideation or feelings of life not worth living
    
    Diagnostic Algorithm:
    - Requires at least 1 core symptom present most/all of the time
    - Total of at least 5 symptoms present some/most/all of the time
    - Symptoms must persist for at least 2 weeks
    - Symptoms cause clinically significant distress or impairment
    
    Severity Classifications and Treatment Implications:
    
    No Depression (0-13 points):
    - Minimal or no depressive symptoms present
    - Continue routine monitoring and preventive care
    - Focus on mental health promotion and lifestyle factors
    - Consider screening for other mental health conditions if indicated
    
    Mild Depression (14-20 points):
    - Mild depressive symptoms that may benefit from intervention
    - Consider watchful waiting with regular monitoring
    - Psychosocial interventions and counseling may be beneficial
    - Lifestyle modifications (exercise, sleep hygiene, stress management)
    - Brief therapy or cognitive-behavioral interventions
    
    Moderate Depression (21-25 points):
    - Moderate depression requiring active treatment
    - Consider psychotherapy and/or antidepressant medication
    - Regular follow-up essential for monitoring progress
    - Assess for functional impairment in work, social, or personal domains
    - Address comorbid conditions and psychosocial stressors
    
    Severe Depression (26-30 points):
    - Severe depression requiring immediate and intensive treatment
    - Strong indication for combined therapy (psychotherapy + medication)
    - Urgent suicide risk assessment and safety planning
    - Consider psychiatric referral and specialized mental health services
    - Intensive monitoring and frequent follow-up required
    - May require hospitalization if safety concerns are present
    
    Suicide Risk Assessment:
    The MDI includes a critical item assessing feelings that "life is not worth living."
    Any positive response to this item requires immediate suicide risk assessment:
    - Detailed exploration of suicidal ideation, plans, and means
    - Assessment of protective factors and social support
    - Implementation of safety planning and crisis intervention
    - Consideration of hospitalization or intensive outpatient monitoring
    - Family involvement and education about warning signs
    
    Clinical Considerations:
    
    Cultural and Linguistic Factors:
    - Consider cultural expressions of depression and distress
    - Ensure appropriate language version is used (available in 7 languages)
    - Be aware of cultural stigma surrounding mental health
    - Adapt clinical recommendations to cultural context
    
    Comorbidity Assessment:
    - Screen for anxiety disorders, substance use disorders
    - Assess for medical conditions that may contribute to depression
    - Consider personality disorders and trauma history
    - Evaluate medication side effects that may worsen depression
    
    Treatment Monitoring:
    - Administer MDI regularly to track treatment response
    - Expect improvement in scores with effective treatment
    - Consider treatment modifications if no improvement after 6-8 weeks
    - Monitor for emergence of suicidal ideation during treatment
    
    Limitations and Considerations:
    - Self-report measure requiring honest and accurate responses
    - Should be combined with clinical interview for formal diagnosis
    - May not capture all aspects of depression (e.g., seasonal patterns)
    - Requires clinical judgment for interpretation and treatment planning
    - Not suitable as sole diagnostic tool for complex cases
    
    Quality Assurance:
    - Ensure patient privacy and confidentiality during administration
    - Provide clear instructions and adequate time for completion
    - Review responses for inconsistencies or concerning patterns
    - Document results in clinical record with interpretation
    - Follow up on all positive suicide risk indicators immediately
    
    Args:
        request: MDI assessment parameters covering 10 depression symptoms
        
    Returns:
        MajorDepressionIndexResponse: Comprehensive depression assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("major_depression_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Major Depression Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return MajorDepressionIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Major Depression Index",
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
                "message": "Internal error in Major Depression Index calculation",
                "details": {"error": str(e)}
            }
        )