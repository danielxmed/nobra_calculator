"""
Fibrosis-4 (FIB-4) Index for Liver Fibrosis Router

Endpoint for calculating FIB-4 Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.fibrosis_4_index import (
    Fibrosis4IndexRequest,
    Fibrosis4IndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fibrosis_4_index",
    response_model=Fibrosis4IndexResponse,
    summary="Calculate Fibrosis-4 (FIB-4) Index for Liver Fibrosis",
    description="Non-invasive estimate of liver scarring in HCV and HBV patients, to assess need for biopsy. Calculated as (Age × AST) / (Platelet count × √ALT)",
    response_description="The calculated fibrosis 4 index with interpretation",
    operation_id="fibrosis_4_index"
)
async def calculate_fibrosis_4_index(request: Fibrosis4IndexRequest):
    """
    Calculates Fibrosis-4 (FIB-4) Index for Liver Fibrosis
    
    The FIB-4 Index is a non-invasive scoring system that uses routine laboratory 
    values (age, AST, ALT, and platelet count) to estimate the degree of liver 
    fibrosis. It helps identify patients who can avoid liver biopsy (low risk) 
    and those who need further evaluation (high risk).
    
    Args:
        request: Parameters needed for FIB-4 calculation
        
    Returns:
        Fibrosis4IndexResponse: FIB-4 score with risk category and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fibrosis_4_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FIB-4 Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return Fibrosis4IndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FIB-4 Index",
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