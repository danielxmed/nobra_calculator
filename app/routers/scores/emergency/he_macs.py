"""
History and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS) Router

Endpoint for calculating HE-MACS score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.he_macs import (
    HeMacsRequest,
    HeMacsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/he_macs",
    response_model=HeMacsResponse,
    summary="Calculate HE-MACS Score",
    description="Calculates the History and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS) score "
                "for rapid risk stratification of patients with suspected acute coronary syndrome. This decision aid "
                "uses only clinical history and ECG findings to predict the probability of ACS or major adverse cardiac "
                "events within 30 days, without requiring troponin results. The score helps identify very low risk "
                "patients who may be suitable for discharge, as well as high risk patients requiring urgent intervention.",
    response_description="The calculated probability of ACS or MACE within 30 days with risk stratification and clinical recommendations",
    operation_id="he_macs"
)
async def calculate_he_macs(request: HeMacsRequest):
    """
    Calculates HE-MACS Score
    
    The HE-MACS decision aid provides rapid risk stratification for acute coronary 
    syndrome using only history and ECG findings, allowing for immediate triage 
    decisions in the emergency department without waiting for troponin results.
    
    Args:
        request: Clinical parameters including age, sex, symptoms, and ECG findings
        
    Returns:
        HeMacsResponse: Probability percentage with risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("he_macs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HE-MACS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HeMacsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HE-MACS score",
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