"""
CART (Cardiac Arrest Risk Triage) Score Router

Endpoint for calculating CART Score to predict cardiac arrest risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.cart_score import (
    CartScoreRequest,
    CartScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cart_score",
    response_model=CartScoreResponse,
    summary="Calculate CART (Cardiac Arrest Risk Triage) Score",
    description="Predicts risk of in-hospital cardiac arrest within 48 hours using vital signs and age. Developed to identify hospitalized patients at high risk for cardiac arrest who may benefit from intensive monitoring or early intervention.",
    response_description="The calculated cart score with interpretation",
    operation_id="cart_score"
)
async def calculate_cart_score(request: CartScoreRequest):
    """
    Calculates CART (Cardiac Arrest Risk Triage) Score
    
    Predicts the risk of in-hospital cardiac arrest within 48 hours using vital signs 
    and age. The CART score was developed to identify hospitalized patients at high 
    risk for cardiac arrest who may benefit from intensive monitoring or early intervention.
    
    The score uses four parameters:
    - Respiratory Rate: <21 (0 pts), 21-23 (8 pts), 24-25 (12 pts), 26-29 (15 pts), >29 (22 pts)
    - Heart Rate: <110 (0 pts), 110-139 (4 pts), >139 (13 pts)  
    - Diastolic Blood Pressure: >49 (0 pts), 40-49 (4 pts), 35-39 (6 pts), <35 (13 pts)
    - Age: <55 (0 pts), 55-69 (4 pts), >69 (9 pts)
    
    Risk interpretation:
    - Score ≤20: Low risk of cardiac arrest within 48 hours
    - Score >20: High risk (consider intensive monitoring, rapid response team activation)
    
    The CART score has 91.9% specificity for predicting cardiac arrest within 48 hours
    and outperformed MEWS in validation studies.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CartScoreResponse: Result with clinical interpretation and component scores
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cart_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CART Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CartScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CART Score",
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