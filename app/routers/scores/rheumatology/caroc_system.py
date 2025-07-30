"""
CAROC System Router

Endpoint for calculating Canadian Association of Radiologists and 
Osteoporosis Canada (CAROC) System.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.caroc_system import (
    CAROCSystemRequest,
    CAROCSystemResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/caroc_system", response_model=CAROCSystemResponse)
async def calculate_caroc_system(request: CAROCSystemRequest):
    """
    Calculates CAROC System for fracture risk assessment
    
    The Canadian Association of Radiologists and Osteoporosis Canada (CAROC) 
    System provides a simplified approach to assess 10-year absolute fracture 
    risk for major osteoporotic fractures. It stratifies patients into low 
    (<10%), moderate (10-20%), or high (>20%) risk categories.
    
    Key features:
    - Based on age, sex, and femoral neck T-score
    - Two major clinical risk factors: fragility fracture and glucocorticoid use
    - Does not require computer access (paper-based tables available)
    - High concordance (88-89%) with Canadian FRAX tool
    
    Risk elevation rules:
    - T-score ≤-2.5 at any site = at least moderate risk
    - Either risk factor elevates risk by one category
    - Both risk factors = automatic high risk
    
    The tool is primarily validated for Canadian populations aged 50-85 years
    and may not generalize to other ethnic groups.
    
    Args:
        request: Demographics, BMD, and clinical risk factors
        
    Returns:
        CAROCSystemResponse: Risk category with treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("caroc_system", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAROC System",
                    "details": {"parameters": parameters}
                }
            )
        
        return CAROCSystemResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAROC System",
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