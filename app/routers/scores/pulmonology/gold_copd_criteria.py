"""
Global Initiative for Obstructive Lung Disease (GOLD) Criteria for COPD Router

Endpoint for calculating GOLD COPD Criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.gold_copd_criteria import (
    GoldCopdCriteriaRequest,
    GoldCopdCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gold_copd_criteria",
    response_model=GoldCopdCriteriaResponse,
    summary="Calculate Global Initiative for Obstructive Lung Disease",
    description="Clinical assessment and staging system for chronic obstructive pulmonary disease (COPD) based on spirometry, symptoms, and exacerbation risk. Provides comprehensive evaluation using FEV1 percentage predicted, symptom assessment, and treatment recommendations according to GOLD 2024-2025 guidelines.",
    response_description="The calculated gold copd criteria with interpretation",
    operation_id="calculate_gold_copd_criteria"
)
async def calculate_gold_copd_criteria(request: GoldCopdCriteriaRequest):
    """
    Calculates Global Initiative for Obstructive Lung Disease (GOLD) Criteria for COPD
    
    The GOLD criteria provide a standardized framework for the diagnosis, assessment, and 
    management of chronic obstructive pulmonary disease (COPD). The GOLD 2025 guidelines 
    use a comprehensive approach combining spirometric assessment, symptom evaluation, 
    and exacerbation risk to classify COPD severity and guide evidence-based treatment decisions.
    
    Key Components:
    - Spirometric confirmation: FEV1/FVC <0.70 post-bronchodilator
    - Severity staging: GOLD stages 1-4 based on FEV1 percentage predicted
    - Symptom assessment: mMRC dyspnea scale and/or CAT score
    - Exacerbation risk: History of exacerbations and hospitalizations
    - Group classification: A, B, E for treatment selection
    
    The system emphasizes individualized treatment using the ABE framework (Assessment, 
    Bronchodilator, Exacerbation) with focus on smoking cessation, bronchodilator therapy, 
    pulmonary rehabilitation, and exacerbation prevention.
    
    Args:
        request: Parameters including FEV1% predicted, FEV1/FVC ratio, mMRC dyspnea, exacerbation history, and optional CAT score
        
    Returns:
        GoldCopdCriteriaResponse: GOLD classification with stage, group, and comprehensive treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gold_copd_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GOLD COPD Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return GoldCopdCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GOLD COPD Criteria",
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