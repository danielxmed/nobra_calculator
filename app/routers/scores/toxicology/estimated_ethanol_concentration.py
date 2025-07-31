"""
Estimated Ethanol (and Toxic Alcohol) Serum Concentration Based on Ingestion Router

Endpoint for calculating estimated serum concentration of alcohols based on ingestion.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.toxicology.estimated_ethanol_concentration import (
    EstimatedEthanolConcentrationRequest,
    EstimatedEthanolConcentrationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/estimated_ethanol_concentration", response_model=EstimatedEthanolConcentrationResponse)
async def calculate_estimated_ethanol_concentration(request: EstimatedEthanolConcentrationRequest):
    """
    Calculates Estimated Ethanol (and Toxic Alcohol) Serum Concentration Based on Ingestion
    
    This calculator estimates serum concentration of ethanol and toxic alcohols based on 
    the amount ingested and patient weight using volume of distribution principles.
    
    The calculation uses the formula:
    [C] = Dose / (Vd × Weight)
    
    Where:
    - [C] = Serum concentration (mg/L)
    - Dose = Amount ingested (mg)
    - Vd = Volume of distribution (0.6 L/kg)
    - Weight = Patient body weight (kg)
    
    Supported alcohol types:
    - Ethanol: Common alcoholic beverages, hand sanitizers
    - Methanol: Windshield washer fluid, antifreeze, industrial solvents
    - Ethylene Glycol: Automotive antifreeze, brake fluid
    - Isopropanol: Rubbing alcohol, disinfectants
    
    Treatment thresholds:
    - Methanol: ≥20 mg/dL requires treatment
    - Ethylene glycol: ≥20 mg/dL requires treatment
    - Ethanol: >300 mg/dL potentially fatal
    
    Args:
        request: Parameters including alcohol type, amount ingested, weight, and optional alcohol percentage
        
    Returns:
        EstimatedEthanolConcentrationResponse: Result with estimated concentration and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("estimated_ethanol_concentration", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Estimated Ethanol Concentration",
                    "details": {"parameters": parameters}
                }
            )
        
        return EstimatedEthanolConcentrationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Estimated Ethanol Concentration",
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