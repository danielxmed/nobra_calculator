"""
National Comprehensive Cancer Network International Prognostic Index (NCCN-IPI) Router

Endpoint for calculating NCCN-IPI for diffuse large B-cell lymphoma (DLBCL).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.nccn_ipi import (
    NccnIpiRequest,
    NccnIpiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/nccn_ipi",
    response_model=NccnIpiResponse,
    summary="Calculate National Comprehensive Cancer Network Internati...",
    description="Predicts survival in patients with diffuse large B-cell lymphoma (DLBCL) using age, LDH levels, extranodal involvement, Ann Arbor stage, and ECOG performance status. Developed for the rituximab era with enhanced prognostic discrimination.",
    response_description="The calculated nccn ipi with interpretation",
    operation_id="calculate_nccn_ipi"
)
async def calculate_nccn_ipi(request: NccnIpiRequest):
    """
    Calculates National Comprehensive Cancer Network International Prognostic Index (NCCN-IPI)
    
    The NCCN-IPI is an enhanced prognostic index for patients with diffuse large B-cell 
    lymphoma (DLBCL) treated in the rituximab era. It provides superior prognostic 
    discrimination compared to the conventional IPI, particularly for identifying patients 
    with excellent prognosis (low risk) and poor prognosis (high risk).
    
    Risk Groups:
    - Low (0-1 points): Excellent prognosis, 5-year OS ~96%
    - Low-intermediate (2-3 points): Good prognosis, 5-year OS ~82%
    - High-intermediate (4-5 points): Moderate prognosis, 5-year OS ~64%
    - High (6-8 points): Poor prognosis, 5-year OS ~33%
    
    Clinical Use:
    - Risk stratification at diagnosis
    - Treatment selection (standard vs. intensified therapy)
    - Clinical trial eligibility
    - Prognosis communication
    
    Args:
        request: Parameters needed for calculation (age, LDH ratio, extranodal sites,
                Ann Arbor stage, ECOG performance status)
        
    Returns:
        NccnIpiResponse: Result with risk group and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nccn_ipi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NCCN-IPI",
                    "details": {"parameters": parameters}
                }
            )
        
        return NccnIpiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NCCN-IPI",
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