"""
Modified Asthma Predictive Index (mAPI) Router

Endpoint for calculating mAPI in pediatric patients with recurrent wheezing.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.modified_asthma_predictive_index import (
    ModifiedAsthmaPredictiveIndexRequest,
    ModifiedAsthmaPredictiveIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_asthma_predictive_index",
    response_model=ModifiedAsthmaPredictiveIndexResponse,
    summary="Calculate Modified Asthma Predictive Index (mAPI)",
    description="Calculates the Modified Asthma Predictive Index (mAPI) to predict future asthma onset "
                "probability in pediatric patients ≤3 years old with recurrent wheezing episodes. "
                "The mAPI requires ≥4 wheezing episodes per year for applicability and evaluates "
                "3 major criteria (parental asthma, atopic dermatitis, aeroallergen sensitivity) and "
                "3 minor criteria (wheezing unrelated to colds, eosinophils ≥4%, food allergies). "
                "A positive mAPI indicates increased risk when ≥1 major OR ≥2 minor criteria are present. "
                "This validated tool has high specificity (98-100%) but variable sensitivity (8.2-19%) "
                "and helps identify children at higher risk for future asthma development, though it "
                "does not guarantee diagnosis. The key modification from the original API is the "
                "addition of food allergies as a minor criterion.",
    response_description="mAPI result with risk assessment and clinical management recommendations",
    operation_id="modified_asthma_predictive_index"
)
async def calculate_modified_asthma_predictive_index(request: ModifiedAsthmaPredictiveIndexRequest):
    """
    Calculates Modified Asthma Predictive Index (mAPI)
    
    Predicts future asthma onset probability in children ≤3 years old 
    with recurrent wheezing episodes based on clinical criteria.
    
    Args:
        request: Clinical parameters for mAPI assessment
        
    Returns:
        ModifiedAsthmaPredictiveIndexResponse: mAPI result with risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_asthma_predictive_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Asthma Predictive Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedAsthmaPredictiveIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Asthma Predictive Index",
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