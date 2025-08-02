"""
Modified Minnesota Detoxification Scale (mMINDS) Router

Endpoint for calculating Modified Minnesota Detoxification Scale for alcohol withdrawal assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.modified_minnesota_detoxification_scale import (
    ModifiedMinnesotaDetoxificationScaleRequest,
    ModifiedMinnesotaDetoxificationScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_minnesota_detoxification_scale",
    response_model=ModifiedMinnesotaDetoxificationScaleResponse,
    summary="Calculate Modified Minnesota Detoxification Scale (mMINDS)",
    description="Calculates the Modified Minnesota Detoxification Scale (mMINDS) for assessment of alcohol withdrawal syndrome. "
                "This objective clinical scale is particularly valuable in critically ill patients and ICU settings where "
                "subjective assessment tools like CIWA-Ar may be inappropriate. The scale evaluates 9 clinical parameters "
                "to provide guidance for benzodiazepine therapy protocols and withdrawal severity stratification. "
                "mMINDS has been shown to result in shorter ICU stays, reduced benzodiazepine use, and improved clinical outcomes "
                "compared to traditional subjective assessment tools.",
    response_description="The calculated mMINDS score with alcohol withdrawal severity assessment and treatment recommendations",
    operation_id="modified_minnesota_detoxification_scale"
)
async def calculate_modified_minnesota_detoxification_scale(request: ModifiedMinnesotaDetoxificationScaleRequest):
    """
    Calculates Modified Minnesota Detoxification Scale (mMINDS) for alcohol withdrawal assessment
    
    Provides objective assessment of alcohol withdrawal severity through evaluation of 
    9 clinical parameters including vital signs, physical signs, and neuropsychiatric 
    symptoms. Particularly useful in critically ill patients where subjective 
    assessment may be challenging or impossible.
    
    Args:
        request: Parameters needed for mMINDS calculation
        
    Returns:
        ModifiedMinnesotaDetoxificationScaleResponse: mMINDS score with clinical interpretation and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_minnesota_detoxification_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Minnesota Detoxification Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedMinnesotaDetoxificationScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Minnesota Detoxification Scale",
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