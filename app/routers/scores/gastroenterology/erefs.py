"""
Eosinophilic Esophagitis Endoscopic Reference Score (EREFS) Router

Endpoint for calculating EREFS score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.erefs import (
    ErefsRequest,
    ErefsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/erefs",
    response_model=ErefsResponse,
    summary="Calculate Eosinophilic Esophagitis Endoscopic Reference S...",
    description="Assesses severity of endoscopic findings in patients with eosinophilic esophagitis (EoE) using standardized scoring of five major endoscopic features: edema, rings, exudates, furrows, and strictures.",
    response_description="The calculated erefs with interpretation",
    operation_id="erefs"
)
async def calculate_erefs(request: ErefsRequest):
    """
    Calculates Eosinophilic Esophagitis Endoscopic Reference Score (EREFS)
    
    Assesses severity of endoscopic findings in patients with eosinophilic esophagitis 
    using standardized scoring of five major endoscopic features: edema, rings, 
    exudates, furrows, and strictures. Provides standardized assessment for disease 
    severity and treatment monitoring.
    
    Args:
        request: Parameters including the five endoscopic features with their severity grades
        
    Returns:
        ErefsResponse: EREFS score with clinical interpretation and disease severity
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("erefs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EREFS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ErefsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EREFS calculation",
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