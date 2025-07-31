"""
Bristol Stool Form Scale Router

Endpoint for calculating Bristol Stool Form Scale classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.bristol_stool_form_scale import (
    BristolStoolFormScaleRequest,
    BristolStoolFormScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bristol_stool_form_scale",
    response_model=BristolStoolFormScaleResponse,
    summary="Calculate Bristol Stool Form Scale",
    description="Classifies stool form and correlates with intestinal transit time to assess bowel health and identify constipation or diarrhea",
    response_description="The calculated bristol stool form scale with interpretation",
    operation_id="bristol_stool_form_scale"
)
async def calculate_bristol_stool_form_scale(request: BristolStoolFormScaleRequest):
    """
    Calculates Bristol Stool Form Scale classification
    
    Classifies stool form and correlates with intestinal transit time to assess 
    bowel health and identify constipation or diarrhea. Developed at Bristol Royal 
    Infirmary in 1997 by Stephen Lewis and Ken Heaton.
    
    The scale provides:
    - Visual classification of stool consistency (Types 1-7)
    - Assessment of colonic transit time
    - Clinical recommendations based on stool type
    - Identification of constipation (Types 1-2) or diarrhea (Types 6-7)
    - Normal range identification (Types 3-5, with Type 4 being ideal)
    
    Args:
        request: Parameters needed for Bristol Stool Form Scale classification
        
    Returns:
        BristolStoolFormScaleResponse: Result with classification, transit time assessment, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bristol_stool_form_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bristol Stool Form Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BristolStoolFormScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bristol Stool Form Scale",
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