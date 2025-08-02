"""
Modified Bishop Score for Vaginal Delivery and Induction of Labor Router

Endpoint for calculating Modified Bishop Score for cervical favorability assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gynecology.modified_bishop_score import (
    ModifiedBishopScoreRequest,
    ModifiedBishopScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_bishop_score",
    response_model=ModifiedBishopScoreResponse,
    summary="Calculate Modified Bishop Score for Vaginal Delivery and Induction of Labor",
    description="Calculates the Modified Bishop Score to predict likelihood of successful vaginal "
                "delivery and assess cervical favorability for labor induction. The Modified Bishop "
                "Score evaluates five cervical characteristics (dilation, length/effacement, fetal "
                "station, position, consistency) plus clinical modifiers (parity, pre-eclampsia, "
                "postdate pregnancy, nulliparity, PPROM) to provide enhanced predictive accuracy. "
                "Scores ≤5 indicate unfavorable cervix requiring cervical ripening, scores 6-7 are "
                "intermediate requiring clinical judgment, and scores ≥8 indicate favorable cervix "
                "with high likelihood of successful induction. This validated tool helps guide "
                "induction timing, method selection, and patient counseling regarding delivery "
                "expectations and potential need for cesarean section.",
    response_description="Modified Bishop Score with cervical favorability assessment and induction recommendations",
    operation_id="modified_bishop_score"
)
async def calculate_modified_bishop_score(request: ModifiedBishopScoreRequest):
    """
    Calculates Modified Bishop Score for Vaginal Delivery and Induction of Labor
    
    Assesses cervical favorability for labor induction using traditional Bishop 
    score components plus clinical modifiers for enhanced accuracy.
    
    Args:
        request: Cervical assessment parameters and clinical factors
        
    Returns:
        ModifiedBishopScoreResponse: Score with favorability assessment and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_bishop_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Bishop Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedBishopScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Bishop Score",
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