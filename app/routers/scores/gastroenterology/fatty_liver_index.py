"""
Fatty Liver Index Router

Endpoint for calculating Fatty Liver Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.fatty_liver_index import (
    FattyLiverIndexRequest,
    FattyLiverIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fatty_liver_index",
    response_model=FattyLiverIndexResponse,
    summary="Calculate Fatty Liver Index",
    description="Diagnoses fatty liver using lab and exam findings. A simple and accurate predictor of hepatic steatosis in the general population.",
    response_description="The calculated fatty liver index with interpretation",
    operation_id="fatty_liver_index"
)
async def calculate_fatty_liver_index(request: FattyLiverIndexRequest):
    """
    Calculates Fatty Liver Index
    
    The FLI is a simple algorithm based on waist circumference, BMI, triglycerides 
    and GGT to predict fatty liver disease. It helps identify patients who should 
    undergo liver ultrasonography and those who do not need it.
    
    Args:
        request: Parameters needed for FLI calculation
        
    Returns:
        FattyLiverIndexResponse: FLI score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fatty_liver_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fatty Liver Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return FattyLiverIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fatty Liver Index",
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