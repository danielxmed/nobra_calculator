"""
HEMORR₂HAGES Score for Major Bleeding Risk Router

Endpoint for calculating HEMORR₂HAGES bleeding risk score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.hemorr2hages import (
    Hemorr2hagesRequest,
    Hemorr2hagesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hemorr2hages",
    response_model=Hemorr2hagesResponse,
    summary="Calculate HEMORR₂HAGES Score",
    description="Calculates the HEMORR₂HAGES Score for Major Bleeding Risk in elderly patients "
                "with atrial fibrillation who are candidates for anticoagulation therapy. "
                "The score evaluates 11 clinical risk factors (with 'Rebleeding' worth 2 points, "
                "all others worth 1 point) to stratify patients into low (0-1), intermediate (2-3), "
                "or high (≥4) bleeding risk categories. This validated tool helps clinicians balance "
                "the benefits of stroke prevention against bleeding risks when considering anticoagulation. "
                "Should be used alongside stroke risk assessment tools like CHA₂DS₂-VASc for comprehensive "
                "risk-benefit analysis.",
    response_description="The calculated HEMORR₂HAGES score with bleeding risk stratification and clinical recommendations",
    operation_id="hemorr2hages"
)
async def calculate_hemorr2hages(request: Hemorr2hagesRequest):
    """
    Calculates HEMORR₂HAGES Score for Major Bleeding Risk
    
    The HEMORR₂HAGES score is designed specifically for elderly patients (>75 years)
    with atrial fibrillation to assess their bleeding risk on anticoagulation.
    It provides a systematic approach to evaluating bleeding risk factors and helps
    guide clinical decision-making regarding anticoagulation therapy.
    
    Args:
        request: Parameters including 11 bleeding risk factors
        
    Returns:
        Hemorr2hagesResponse: HEMORR₂HAGES score with risk stratification and interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hemorr2hages", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HEMORR₂HAGES score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Hemorr2hagesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HEMORR₂HAGES calculation",
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
                "message": "Internal error in HEMORR₂HAGES calculation",
                "details": {"error": str(e)}
            }
        )