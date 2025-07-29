"""
Asthma Predictive Index (API) Router

Endpoint for calculating Asthma Predictive Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.asthma_predictive_index import (
    AsthmaPreductiveIndexRequest,
    AsthmaPreductiveIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/asthma_predictive_index", response_model=AsthmaPreductiveIndexResponse)
async def calculate_asthma_predictive_index(request: AsthmaPreductiveIndexRequest):
    """
    Calculates Asthma Predictive Index (API)
    
    Determines likelihood of pediatric patients developing childhood asthma in children 
    ≤3 years old with recurrent wheezing episodes. The API uses 6 clinical variables 
    to classify patients into three risk categories:
    
    - Positive Stringent (77% asthma risk): ≥3 wheezing episodes + criteria met
    - Positive Loose (59% asthma risk): <3 wheezing episodes + criteria met  
    - Negative (<3% asthma risk): Criteria not met
    
    Criteria are met with either 1 major criterion OR 2 minor criteria.
    Major criteria: Family history of asthma, Eczema diagnosis
    Minor criteria: Air allergen sensitivity, Wheezing apart from colds, >4% eosinophils
    
    Args:
        request: Parameters needed for API calculation
        
    Returns:
        AsthmaPreductiveIndexResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asthma_predictive_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Asthma Predictive Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsthmaPreductiveIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Asthma Predictive Index",
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
