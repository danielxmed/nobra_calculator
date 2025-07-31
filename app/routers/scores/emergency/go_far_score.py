"""
GO-FAR (Good Outcome Following Attempted Resuscitation) Score Router

Endpoint for calculating GO-FAR score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.go_far_score import (
    GoFarScoreRequest,
    GoFarScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/go_far_score",
    response_model=GoFarScoreResponse,
    summary="Calculate GO-FAR",
    description="Predicts survival to discharge with good neurological outcome after in-hospital cardiac arrest. Uses 13 pre-arrest variables to stratify patients into risk categories for shared decision-making regarding resuscitation preferences.",
    response_description="The calculated go far score with interpretation",
    operation_id="go_far_score"
)
async def calculate_go_far_score(request: GoFarScoreRequest):
    """
    Calculates GO-FAR (Good Outcome Following Attempted Resuscitation) Score
    
    The GO-FAR score is an evidence-based tool that predicts survival to discharge 
    with good neurological outcome after in-hospital cardiac arrest. It uses 13 
    pre-arrest clinical variables to stratify patients into risk categories, 
    enabling healthcare providers to have informed discussions with patients and 
    families about resuscitation preferences and code status decisions.
    
    **Clinical Applications**:
    - Shared decision-making regarding resuscitation preferences
    - Risk stratification for in-hospital cardiac arrest outcomes
    - Code status discussions with evidence-based framework
    - Quality improvement in critical care resource allocation
    - Family counseling with realistic outcome expectations
    
    **Scoring System**:
    The score uses 13 weighted variables ranging from -15 to +11 points:
    - Age categories (0-11 points)
    - Neurologically intact at admission (-15 points if yes - protective factor)
    - Major trauma (+10 points if yes)
    - Acute stroke (+8 points if yes)
    - Metastatic/hematologic cancer (+7 points if yes)
    - Septicemia (+7 points if yes)
    - Medical non-cardiac diagnosis (+7 points if yes)
    - Hepatic insufficiency (+6 points if yes)
    - Skilled nursing facility admission (+6 points if yes)
    - Hypotension/hypoperfusion (+5 points if yes)
    - Renal insufficiency/dialysis (+4 points if yes)
    - Respiratory insufficiency (+4 points if yes)
    - Pneumonia (+1 point if yes)
    
    **Survival Probability Categories**:
    - Above Average (-15 to -6 points): >15% probability
    - Average (-5 to 13 points): 3-15% probability
    - Low (14 to 23 points): 1-3% probability  
    - Very Low (≥24 points): <1% probability
    
    **Important Notes**:
    - Developed specifically for in-hospital cardiac arrests
    - Should be used as part of comprehensive clinical assessment
    - Supports shared decision-making, not mandated care decisions
    - Consider patient autonomy, cultural factors, and individual circumstances
    - Neurologically intact survival defined as CPC score of 1 at discharge
    
    Args:
        request: GO-FAR score parameters including age category and 12 clinical variables
        
    Returns:
        GoFarScoreResponse: GO-FAR score with survival probability category and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("go_far_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GO-FAR Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GoFarScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GO-FAR Score",
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