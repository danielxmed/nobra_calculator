"""
du Bois Score for Idiopathic Pulmonary Fibrosis (IPF) Mortality Router

Endpoint for calculating du Bois IPF mortality risk score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.du_bois_ipf_mortality import (
    DuBoisIpfMortalityRequest,
    DuBoisIpfMortalityResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/du_bois_ipf_mortality", response_model=DuBoisIpfMortalityResponse)
async def calculate_du_bois_ipf_mortality(request: DuBoisIpfMortalityRequest):
    """
    Calculates du Bois Score for Idiopathic Pulmonary Fibrosis (IPF) Mortality
    
    Determines 1-year mortality risk in IPF patients using PFT and clinical indicators.
    Developed from two clinical trials (n=1,099) to identify independent predictors 
    of 1-year mortality in idiopathic pulmonary fibrosis.
    
    Args:
        request: du Bois IPF mortality risk parameters
        
    Returns:
        DuBoisIpfMortalityResponse: Risk score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("du_bois_ipf_mortality", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating du Bois IPF mortality score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DuBoisIpfMortalityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for du Bois IPF mortality score",
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