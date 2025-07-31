"""
DSM-5 Criteria for Bipolar Disorder Router

Endpoint for evaluating DSM-5 Bipolar Disorder diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.dsm5_bipolar_disorder import (
    Dsm5BipolarDisorderRequest,
    Dsm5BipolarDisorderResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dsm5_bipolar_disorder",
    response_model=Dsm5BipolarDisorderResponse,
    summary="Calculate DSM-5 Criteria for Bipolar Disorder",
    description="Diagnostic criteria for bipolar disorder based on DSM-5. Evaluates criteria for manic episodes, hypomanic episodes, and major depressive episodes to determine bipolar I, bipolar II, or other specified bipolar disorders.",
    response_description="The calculated dsm5 bipolar disorder with interpretation",
    operation_id="calculate_dsm5_bipolar_disorder"
)
async def calculate_dsm5_bipolar_disorder(request: Dsm5BipolarDisorderRequest):
    """
    Evaluates DSM-5 Criteria for Bipolar Disorder
    
    The DSM-5 diagnostic criteria for Bipolar Disorder evaluates episodes of mania or hypomania:
    
    Core Criteria (both must be present):
    A. Elevated, expansive, or irritable mood, present most of the day, nearly every day
    B. Abnormally and persistently increased goal-directed activity or energy
    
    Additional Symptoms (at least 3 of 7 required):
    1. Inflated self-esteem or grandiosity
    2. Decreased need for sleep (feels rested after only 3 hours)
    3. More talkative than usual or pressure to keep talking
    4. Flight of ideas or racing thoughts
    5. Distractibility (attention easily drawn to unimportant stimuli)
    6. Increase in goal-directed activity or psychomotor agitation
    7. Excessive involvement in risky activities with high potential for consequences
    
    Duration and Impairment Requirements:
    - Manic Episode: ≥7 days duration (or hospitalization required) + marked impairment
    - Hypomanic Episode: 4-6 days duration + observable change but less impairment
    
    Bipolar Disorder Types:
    - Bipolar I: At least one manic episode (lifetime)
    - Bipolar II: At least one hypomanic episode + at least one major depressive episode
    
    Key DSM-5 Changes:
    - Added "increased activity/energy" as core requirement alongside mood symptoms
    - This addition reduced prevalence estimates by approximately 48%
    - Mixed features specifier can be applied to any mood episode
    
    Important Clinical Considerations:
    - This is a diagnostic aid for clinical evaluation, not a substitute for assessment
    - Risk assessment for suicide and psychotic features is essential
    - Consider hospitalization for manic episodes with significant impairment
    - Comprehensive psychiatric evaluation required for definitive diagnosis
    
    Args:
        request: DSM-5 bipolar disorder criteria parameters (13 diagnostic elements)
        
    Returns:
        Dsm5BipolarDisorderResponse: Diagnostic result with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dsm5_bipolar_disorder", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating DSM-5 Criteria for Bipolar Disorder",
                    "details": {"parameters": parameters}
                }
            )
        
        return Dsm5BipolarDisorderResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DSM-5 Criteria for Bipolar Disorder",
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
                "message": "Internal error in evaluation",
                "details": {"error": str(e)}
            }
        )