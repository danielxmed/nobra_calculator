"""
Modified Mallampati Classification Router

Endpoint for calculating Modified Mallampati Classification for airway assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.modified_mallampati_classification import (
    ModifiedMallampatiClassificationRequest,
    ModifiedMallampatiClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_mallampati_classification",
    response_model=ModifiedMallampatiClassificationResponse,
    summary="Calculate Modified Mallampati Classification",
    description="Calculates the Modified Mallampati Classification for predicting difficult intubation based on visible oropharyngeal structures. "
                "This bedside assessment tool stratifies patients into 4 classes based on anatomical visibility during oral examination. "
                "The classification helps predict intubation difficulty and guides airway management strategies. Higher classes "
                "(III-IV) are associated with increased difficulty and may require alternative intubation techniques or specialist involvement.",
    response_description="The calculated Mallampati class with intubation difficulty prediction and airway management recommendations",
    operation_id="modified_mallampati_classification"
)
async def calculate_modified_mallampati_classification(request: ModifiedMallampatiClassificationRequest):
    """
    Calculates Modified Mallampati Classification for airway assessment
    
    Assesses predicted difficulty of endotracheal intubation based on visible 
    oropharyngeal structures during oral examination. The modified 4-class system 
    provides stratified risk assessment for airway management planning.
    
    Args:
        request: Parameters needed for Mallampati classification
        
    Returns:
        ModifiedMallampatiClassificationResponse: Classification with clinical interpretation and airway management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_mallampati_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Mallampati Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedMallampatiClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Mallampati Classification",
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