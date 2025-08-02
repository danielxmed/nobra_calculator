"""
PROMISE Score for Malignant Pleural Effusion Router

Endpoint for calculating PROMISE Score for Malignant Pleural Effusion.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.promise_score_malignant_pleural_effusion import (
    PromiseScoreMalignantPleuralEffusionRequest,
    PromiseScoreMalignantPleuralEffusionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/promise_score_malignant_pleural_effusion",
    response_model=PromiseScoreMalignantPleuralEffusionResponse,
    summary="Calculate PROMISE Score for Malignant Pleural Effusion",
    description="Calculates the PROMISE Score for Malignant Pleural Effusion, the first prospectively "
                "validated prognostic model that combines clinical and biological parameters to accurately "
                "predict 3-month mortality in patients with malignant pleural effusion. This comprehensive "
                "scoring system uses seven key parameters: previous chemotherapy and radiotherapy history, "
                "hemoglobin level, white blood cell count, C-reactive protein, ECOG performance status, "
                "and cancer type. The score stratifies patients into four distinct risk categories ranging "
                "from <25% to >75% 3-month mortality, enabling clinicians to make informed decisions about "
                "aggressive interventions (such as pleurodesis), palliative procedures (indwelling catheters), "
                "or comfort-focused care. This tool is superior to existing prognostic scores and provides "
                "essential guidance for treatment planning, resource allocation, and prognostic discussions "
                "with patients and families facing malignant pleural effusion.",
    response_description="The calculated PROMISE Score with detailed risk stratification and treatment guidance",
    operation_id="promise_score_malignant_pleural_effusion"
)
async def calculate_promise_score_malignant_pleural_effusion(request: PromiseScoreMalignantPleuralEffusionRequest):
    """
    Calculates PROMISE Score for Malignant Pleural Effusion
    
    This validated tool helps predict 3-month mortality and guide treatment
    decisions for patients with malignant pleural effusion.
    
    Args:
        request: Clinical parameters including treatment history, laboratory values, performance status, and cancer type
        
    Returns:
        PromiseScoreMalignantPleuralEffusionResponse: Result with risk stratification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("promise_score_malignant_pleural_effusion", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating PROMISE Score for Malignant Pleural Effusion",
                    "details": {"parameters": parameters}
                }
            )
        
        return PromiseScoreMalignantPleuralEffusionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for PROMISE Score for Malignant Pleural Effusion",
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