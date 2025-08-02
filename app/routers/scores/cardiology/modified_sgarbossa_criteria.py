"""
Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block Router

Endpoint for diagnosing acute myocardial infarction in patients with prior LBBB.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.modified_sgarbossa_criteria import (
    ModifiedSgarbossaCriteriaRequest,
    ModifiedSgarbossaCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_sgarbossa_criteria",
    response_model=ModifiedSgarbossaCriteriaResponse,
    summary="Calculate Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block",
    description="Diagnoses acute myocardial infarction in patients with prior left bundle branch block "
                "using improved ECG criteria. The Modified Sgarbossa criteria significantly improve upon "
                "the original criteria by replacing the third criterion (excessive discordance ≥5 mm) "
                "with a proportional measurement (ST/S ratio ≥-0.25), increasing sensitivity from 36% "
                "to 80% while maintaining 99% specificity. The criteria evaluate three ECG findings: "
                "1) Concordant ST elevation ≥1 mm in leads with positive QRS complex, 2) Concordant "
                "ST depression ≥1 mm in leads V1-V3, and 3) Discordant ST elevation with ST/S ratio "
                "≥-0.25. Any single positive criterion indicates acute STEMI and warrants emergent "
                "cardiac catheterization. This tool is essential for emergency departments managing "
                "patients with chest pain and LBBB, where traditional STEMI criteria are unreliable.",
    response_description="The Modified Sgarbossa criteria result with specific criteria met and clinical management recommendations",
    operation_id="modified_sgarbossa_criteria"
)
async def calculate_modified_sgarbossa_criteria(request: ModifiedSgarbossaCriteriaRequest):
    """
    Calculates Modified Sgarbossa's Criteria for diagnosing acute MI in patients with LBBB
    
    Evaluates three ECG criteria specifically designed to diagnose acute myocardial infarction 
    in patients with pre-existing left bundle branch block, where traditional STEMI criteria 
    are unreliable.
    
    Args:
        request: ECG criteria parameters including concordant ST elevation, concordant ST depression, 
                and discordant ST elevation with proportional measurement
        
    Returns:
        ModifiedSgarbossaCriteriaResponse: Diagnostic result with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_sgarbossa_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedSgarbossaCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block",
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