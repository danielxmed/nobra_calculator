"""
IMPEDE-VTE Router

Endpoint for calculating IMPEDE-VTE score for multiple myeloma VTE risk prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.impede_vte import (
    ImpedeVteRequest,
    ImpedeVteResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/impede_vte",
    response_model=ImpedeVteResponse,
    summary="Calculate IMPEDE-VTE Score",
    description="Predicts risk of venous thromboembolism (VTE) in patients with multiple myeloma receiving treatment. The IMPEDE-VTE score was developed and validated in large cohorts (4,446 patients in derivation, 4,256 in validation) to identify multiple myeloma patients at highest risk for VTE during treatment. Patients with multiple myeloma have a 9-fold increased risk of VTE compared to the general population. This validated score helps clinicians identify patients who would benefit most from thromboprophylaxis and is incorporated into National Comprehensive Cancer Network (NCCN) guidelines. The model stratifies patients into low, intermediate, and high-risk categories with cumulative 6-month VTE incidences ranging from 3.8-5.0% (low risk) to 24.1-40.5% (high risk) across validation studies. Essential for evidence-based thromboprophylaxis decisions in multiple myeloma care.",
    response_description="The calculated IMPEDE-VTE score with VTE risk stratification and thromboprophylaxis recommendations",
    operation_id="impede_vte"
)
async def calculate_impede_vte(request: ImpedeVteRequest):
    """
    Calculates IMPEDE-VTE Score
    
    Predicts venous thromboembolism risk in multiple myeloma patients receiving
    treatment. Helps identify patients who would benefit from thromboprophylaxis
    based on treatment regimen, patient factors, and disease characteristics.
    
    Args:
        request: Parameters including IMiD use, BMI, fractures, medications,
                ethnicity, VTE history, vascular access, and anticoagulation status
        
    Returns:
        ImpedeVteResponse: IMPEDE-VTE score with risk stratification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("impede_vte", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IMPEDE-VTE Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImpedeVteResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IMPEDE-VTE Score",
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