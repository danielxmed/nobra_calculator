"""
AST to Platelet Ratio Index (APRI) Router

Endpoint for calculating AST to Platelet Ratio Index (APRI).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.apri import (
    ApriRequest,
    ApriResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/apri", response_model=ApriResponse)
async def calculate_apri(request: ApriRequest):
    """
    Calculates AST to Platelet Ratio Index (APRI)
    
    The APRI is a non-invasive serum marker that uses AST levels and platelet count 
    to assess liver fibrosis and cirrhosis risk in patients with chronic hepatitis C. 
    The score is calculated as [(AST/upper limit of normal) × 100] / platelet count.
    
    APRI values ≤0.5 have high negative predictive value for ruling out significant 
    fibrosis, while values ≥1.5 have high positive predictive value for ruling in 
    cirrhosis. The score has been validated primarily in hepatitis C patients but 
    can be used with caution in other chronic liver diseases.
    
    Args:
        request: Parameters needed for APRI calculation including AST level, 
                AST upper limit normal, and platelet count
        
    Returns:
        ApriResponse: APRI score with clinical interpretation and risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("apri", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AST to Platelet Ratio Index (APRI)",
                    "details": {"parameters": parameters}
                }
            )
        
        return ApriResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AST to Platelet Ratio Index (APRI)",
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
                "message": "Internal error in APRI calculation",
                "details": {"error": str(e)}
            }
        )