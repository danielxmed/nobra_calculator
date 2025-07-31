"""
Acc Aha Hf Staging router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology import AccAhaHfStagingRequest, AccAhaHfStagingResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/acc_aha_hf_staging", response_model=AccAhaHfStagingResponse, summary="Calculate ACC/AHA HF Staging", description="Calculates ACC/AHA Heart Failure Staging", response_description="HF stage and recommendations", operation_id="calculate_acc_aha_hf_staging")
async def calculate_acc_aha_hf_staging(request: AccAhaHfStagingRequest):
    """
    Calculates ACC/AHA Heart Failure Staging
    
    Args:
        request: Parameters for classification (risk factors, structural disease, symptoms)
        
    Returns:
        AccAhaHfStagingResponse: Result with HF stage and recommendations
    """
    try:
        parameters = {
            "risk_factors": request.risk_factors.value,
            "structural_disease": request.structural_disease.value,
            "current_symptoms": request.current_symptoms.value,
            "advanced_symptoms": request.advanced_symptoms.value,
            "hospitalization_frequency": request.hospitalization_frequency.value,
            "ejection_fraction": request.ejection_fraction
        }
        
        result = calculator_service.calculate_score("acc_aha_hf_staging", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACC/AHA HF Staging",
                    "details": {"parameters": parameters}
                }
            )
        
        return AccAhaHfStagingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ACC/AHA HF Staging",
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