"""
Dutch Criteria for Familial Hypercholesterolemia Router

Endpoint for calculating Dutch Criteria for Familial Hypercholesterolemia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.dutch_criteria_familial_hypercholesterolemia import (
    DutchCriteriaFamilialHypercholesterolemiaRequest,
    DutchCriteriaFamilialHypercholesterolemiaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/dutch_criteria_familial_hypercholesterolemia", response_model=DutchCriteriaFamilialHypercholesterolemiaResponse)
async def calculate_dutch_criteria_familial_hypercholesterolemia(request: DutchCriteriaFamilialHypercholesterolemiaRequest):
    """
    Calculates Dutch Criteria for Familial Hypercholesterolemia
    
    Dutch Lipid Clinic Network (DLCN) criteria for diagnosing familial hypercholesterolemia
    using a comprehensive point-based scoring system that evaluates clinical findings,
    family history, and genetic testing results to classify FH likelihood.
    
    Args:
        request: Parameters needed for calculation including LDL cholesterol level,
                clinical signs, family/personal history, and genetic testing results
        
    Returns:
        DutchCriteriaFamilialHypercholesterolemiaResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dutch_criteria_familial_hypercholesterolemia", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Dutch Criteria for Familial Hypercholesterolemia",
                    "details": {"parameters": parameters}
                }
            )
        
        return DutchCriteriaFamilialHypercholesterolemiaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Dutch Criteria for Familial Hypercholesterolemia",
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