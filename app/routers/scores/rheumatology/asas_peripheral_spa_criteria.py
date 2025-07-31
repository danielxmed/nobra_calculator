"""
ASAS Criteria for Peripheral SpondyloArthritis (SpA) Router

Endpoint for calculating ASAS Criteria for Peripheral SpondyloArthritis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.asas_peripheral_spa_criteria import (
    AsasPeripheralSpaCriteriaRequest,
    AsasPeripheralSpaCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/asas_peripheral_spa_criteria",
    response_model=AsasPeripheralSpaCriteriaResponse,
    summary="Calculate ASAS Criteria for Peripheral SpondyloArthritis",
    description="Classifies peripheral spondyloarthritis according to the Assessment of SpondyloArthritis International Society (ASAS) criteria",
    response_description="The calculated asas peripheral spa criteria with interpretation",
    operation_id="asas_peripheral_spa_criteria"
)
async def calculate_asas_peripheral_spa_criteria(request: AsasPeripheralSpaCriteriaRequest):
    """
    Calculates ASAS Criteria for Peripheral SpondyloArthritis (SpA)
    
    The Assessment of SpondyloArthritis International Society (ASAS) classification 
    criteria for peripheral spondyloarthritis are intended for patients with 
    predominant peripheral manifestations including peripheral arthritis, enthesitis, 
    and dactylitis.
    
    Classification requires:
    - Entry criterion: arthritis and/or enthesitis and/or dactylitis
    - Plus either ≥1 Group A feature OR ≥2 Group B features
    
    Group A features: psoriasis, IBD, preceding infection, HLA-B27, uveitis, sacroiliitis
    Group B features: arthritis, enthesitis, dactylitis, IBP past, family history SpA
    
    Sensitivity: 77.8%, Specificity: 82.9%
    
    Args:
        request: Parameters needed for ASAS peripheral SpA criteria calculation
        
    Returns:
        AsasPeripheralSpaCriteriaResponse: Classification result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asas_peripheral_spa_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASAS Criteria for Peripheral SpondyloArthritis",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsasPeripheralSpaCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASAS Criteria for Peripheral SpondyloArthritis",
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
