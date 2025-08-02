"""
Montgomery-Asberg Depression Rating Scale (MADRS) Router

Endpoint for calculating MADRS depression severity score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.madrs import (
    MadrsRequest,
    MadrsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/madrs",
    response_model=MadrsResponse,
    summary="Calculate Montgomery-Asberg Depression Rating Scale (MADRS)",
    description="Calculates the MADRS score for assessing severity of depressive episodes in adults using 10 core mood symptoms. "
                "The MADRS is particularly sensitive to treatment-induced changes in depression severity, making it valuable for "
                "monitoring antidepressant treatment response. Each item is scored 0-6, with total scores ranging from 0-60. "
                "The scale focuses on core mood symptoms rather than somatic symptoms, providing more accurate assessment of "
                "depression severity and treatment response. Scores are interpreted as: Normal (0-6), Mild Depression (7-19), "
                "Moderate Depression (20-34), and Severe Depression (35-60). Response to treatment is defined as ≥50% reduction "
                "from baseline, while remission is typically achieved at scores ≤7-9 points.",
    response_description="The calculated MADRS score with depression severity classification and clinical recommendations",
    operation_id="madrs"
)
async def calculate_madrs(request: MadrsRequest):
    """
    Calculates Montgomery-Asberg Depression Rating Scale (MADRS)
    
    The MADRS is a 10-item depression rating scale designed to be sensitive to changes 
    from antidepressant treatment. It assesses core mood symptoms including apparent 
    sadness, reported sadness, inner tension, sleep disturbances, appetite changes, 
    concentration difficulties, lassitude, inability to feel, pessimistic thoughts, 
    and suicidal ideation.
    
    Each item is scored from 0-6:
    - 0: No symptoms/normal
    - 1-2: Mild symptoms
    - 3-4: Moderate symptoms  
    - 5-6: Severe symptoms
    
    Total score interpretation:
    - 0-6: Normal mood or minimal depressive symptoms
    - 7-19: Mild depression
    - 20-34: Moderate depression requiring treatment
    - 35-60: Severe depression requiring intensive treatment
    
    Args:
        request: MADRS assessment parameters including all 10 items
        
    Returns:
        MadrsResponse: MADRS score with depression severity and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("madrs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MADRS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MadrsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MADRS calculation",
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
                "message": "Internal error in MADRS calculation",
                "details": {"error": str(e)}
            }
        )