"""
Light's Criteria for Exudative Effusions Router

Endpoint for calculating Light's Criteria to determine if pleural fluid is 
exudative or transudative.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.lights_criteria import (
    LightsCriteriaRequest,
    LightsCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lights_criteria",
    response_model=LightsCriteriaResponse,
    summary="Calculate Light's Criteria for Exudative Effusions",
    description="Calculates Light's Criteria for Exudative Effusions, the gold standard diagnostic tool "
                "for differentiating between exudative and transudative pleural effusions. Developed by "
                "Richard Light in 1972, these criteria have been the cornerstone of pleural effusion "
                "evaluation for over 50 years. The calculator evaluates three key parameters: pleural "
                "fluid to serum protein ratio (>0.5), pleural fluid to serum LDH ratio (>0.6), and "
                "pleural fluid LDH greater than two-thirds of the upper limit of normal serum LDH. "
                "Any single positive criterion classifies the effusion as exudative (98% sensitivity), "
                "indicating an inflammatory process requiring comprehensive diagnostic workup. All "
                "negative criteria suggest transudative effusion, focusing treatment on underlying "
                "systemic conditions like heart failure or cirrhosis. Essential for emergency department "
                "evaluation, inpatient management, and guiding appropriate specialist referrals.",
    response_description="The calculated Light's criteria results with effusion classification, detailed criterion analysis, and evidence-based recommendations for diagnostic workup and clinical management",
    operation_id="lights_criteria"
)
async def calculate_lights_criteria(request: LightsCriteriaRequest):
    """
    Calculates Light's Criteria for pleural effusion classification
    
    Light's Criteria represent the gold standard for differentiating between exudative 
    and transudative pleural effusions. This validated diagnostic framework guides 
    appropriate clinical management by distinguishing inflammatory processes requiring 
    comprehensive workup from systemic conditions treated with medical optimization.
    
    Args:
        request: Laboratory parameters including serum and pleural fluid protein and 
                LDH levels, with optional institutional LDH upper normal limit
        
    Returns:
        LightsCriteriaResponse: Effusion classification with detailed criterion analysis 
                               and evidence-based management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lights_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Light's Criteria for Exudative Effusions",
                    "details": {"parameters": parameters}
                }
            )
        
        return LightsCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Light's Criteria calculation",
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
                "message": "Internal error in Light's Criteria calculation",
                "details": {"error": str(e)}
            }
        )