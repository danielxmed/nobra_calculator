"""
Modified Sequential Organ Failure Assessment (mSOFA) Score Router

Endpoint for calculating mSOFA assessment for ICU mortality risk prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.modified_sofa import (
    ModifiedSofaRequest,
    ModifiedSofaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_sofa",
    response_model=ModifiedSofaResponse,
    summary="Calculate Modified Sequential Organ Failure Assessment (mSOFA) Score",
    description="Calculates the Modified Sequential Organ Failure Assessment (mSOFA) Score for "
                "predicting ICU mortality risk using mostly clinical variables and fewer laboratory "
                "tests compared to the original SOFA Score. This validated tool was designed for "
                "resource-constrained critical care environments during disasters or pandemics while "
                "maintaining similar predictive accuracy (AUC 0.84 vs 0.83 for SOFA). The mSOFA "
                "evaluates five organ systems: respiratory (SpO₂/FiO₂ ratio), liver (scleral icterus), "
                "cardiovascular (MAP and vasopressors), central nervous system (Glasgow Coma Scale), "
                "and renal (creatinine). Scores range from 0-20 points with three risk categories: "
                "Low Risk (0-7 points, 4% 30-day mortality), Moderate Risk (8-11 points, 31% mortality), "
                "and High Risk (>11 points, 58% mortality). The threshold of 9 provides 85.6% sensitivity "
                "and 74.6% specificity for mortality prediction.",
    response_description="The calculated mSOFA score with mortality risk assessment and clinical management recommendations",
    operation_id="modified_sofa"
)
async def calculate_modified_sofa(request: ModifiedSofaRequest):
    """
    Calculates Modified Sequential Organ Failure Assessment (mSOFA) Score for ICU mortality risk prediction
    
    Provides standardized multi-organ dysfunction assessment for critically ill patients 
    using mostly clinical variables. The mSOFA score offers similar predictive accuracy 
    to the original SOFA score while requiring fewer laboratory parameters.
    
    Args:
        request: Parameters needed for mSOFA calculation including respiratory, liver, 
                cardiovascular, CNS, and renal system assessments
        
    Returns:
        ModifiedSofaResponse: mSOFA score with mortality risk stratification and clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_sofa", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Sequential Organ Failure Assessment (mSOFA) Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedSofaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Sequential Organ Failure Assessment (mSOFA) Score",
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