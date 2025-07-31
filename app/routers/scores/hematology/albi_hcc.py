"""
ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC) Router

Endpoint for calculating ALBI Grade for HCC prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.albi_hcc import (
    AlbiHccRequest,
    AlbiHccResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/albi_hcc",
    response_model=AlbiHccResponse,
    summary="Calculate ALBI",
    description="Predicts survival in hepatocellular carcinoma patients based on serum albumin and bilirubin concentrations",
    response_description="The calculated albi hcc with interpretation",
    operation_id="albi_hcc"
)
async def calculate_albi_hcc(request: AlbiHccRequest):
    """
    Calculates ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC)
    
    An objective model that predicts survival in HCC patients based on serum 
    albumin and bilirubin concentrations. Serves as an alternative to Child-Pugh 
    grade without subjective variables like ascites and encephalopathy.
    
    Args:
        request: ALBI parameters (albumin and bilirubin concentrations)
        
    Returns:
        AlbiHccResponse: ALBI score, grade, and survival prediction
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("albi_hcc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ALBI Grade for HCC",
                    "details": {"parameters": parameters}
                }
            )
        
        return AlbiHccResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ALBI Grade for HCC",
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