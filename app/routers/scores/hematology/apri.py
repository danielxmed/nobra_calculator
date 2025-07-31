"""
AST to Platelet Ratio Index (APRI) Router

Endpoint for calculating APRI score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.apri import (
    ApriRequest,
    ApriResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/apri",
    response_model=ApriResponse,
    summary="Calculate AST to Platelet Ratio Index (APRI)",
    description="Determines the likelihood of hepatic fibrosis and cirrhosis in patients with hepatitis C using readily available laboratory values.",
    response_description="The calculated apri with interpretation",
    operation_id="calculate_apri"
)
async def calculate_apri(request: ApriRequest):
    """
    Calculates AST to Platelet Ratio Index (APRI)
    
    The APRI is a simple, non-invasive index that uses readily available laboratory 
    tests (AST and platelet count) to assess the likelihood of significant hepatic 
    fibrosis and cirrhosis in patients with chronic hepatitis C. It has better 
    negative predictive value than positive predictive value, making it particularly 
    useful for ruling out advanced liver disease.
    
    Key clinical applications:
    - Screening for significant fibrosis in hepatitis C patients
    - Ruling out cirrhosis (high negative predictive value)
    - Determining need for liver biopsy or further evaluation
    - Monitoring disease progression in chronic liver disease
    
    Args:
        request: Parameters needed for APRI calculation including AST level, 
                AST upper limit of normal, and platelet count
        
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
                    "message": "Error calculating APRI score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ApriResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for APRI calculation",
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
