"""
Bush-Francis Catatonia Rating Scale Router

Endpoint for calculating Bush-Francis Catatonia Rating Scale score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.bush_francis_catatonia_rating_scale import (
    BushFrancisCatatoniaRatingScaleRequest,
    BushFrancisCatatoniaRatingScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bush_francis_catatonia_rating_scale",
    response_model=BushFrancisCatatoniaRatingScaleResponse,
    summary="Calculate Bush-Francis Catatonia Rating Scale",
    description="Assesses severity of catatonia and screens for catatonia in psychiatric and neurological conditions. The first 14 items comprise the screening instrument. If 2 or more of the first 14 items are positive, this indicates a positive screening and should prompt completion of 9 additional items.",
    response_description="The calculated bush francis catatonia rating scale with interpretation",
    operation_id="bush_francis_catatonia_rating_scale"
)
async def calculate_bush_francis_catatonia_rating_scale(request: BushFrancisCatatoniaRatingScaleRequest):
    """
    Calculates Bush-Francis Catatonia Rating Scale
    
    Assesses severity of catatonia and screens for catatonia in psychiatric and 
    neurological conditions. The BFCRS is considered the gold standard for clinical 
    and research purposes for catatonia screening and diagnosis.
    
    The scale consists of 23 items:
    - Items 1-14: Bush-Francis Catatonia Screening Instrument (BFCSI)
    - Items 15-23: Additional items assessed if screening is positive (≥2 items)
    
    Scoring:
    - Items 14, 17-21 are binary (0=absent or 3=present)
    - All other items: 0=absent, 1=occasional, 2=frequent, 3=constant
    - Total score range: 0-69 points
    - Screening positive if ≥2 of first 14 items score ≥1
    
    Clinical utility:
    - Aids in diagnosis of catatonia across psychiatric and medical conditions
    - Monitors treatment response (particularly to benzodiazepines)
    - Identifies malignant catatonia requiring urgent intervention
    - Guides decision for ECT in benzodiazepine-resistant cases
    
    Args:
        request: Parameters needed for BFCRS calculation
        
    Returns:
        BushFrancisCatatoniaRatingScaleResponse: Result with total score, screening result, 
        severity interpretation, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict(exclude_none=True)
        
        # Execute calculation
        result = calculator_service.calculate_score("bush_francis_catatonia_rating_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bush-Francis Catatonia Rating Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BushFrancisCatatoniaRatingScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bush-Francis Catatonia Rating Scale",
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