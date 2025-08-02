"""
International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI) Router

Endpoint for calculating DLBCL IPI.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.dlbcl_ipi import (
    DlbclIpiRequest,
    DlbclIpiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dlbcl_ipi",
    response_model=DlbclIpiResponse,
    summary="Calculate International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI)",
    description="Calculates the International Prognostic Index (IPI) for diffuse large B-cell lymphoma (DLBCL) to predict overall survival and stratify patients into risk groups. This validated prognostic model uses five independent risk factors (age >60 years, elevated LDH, advanced Ann Arbor stage III-IV, ECOG performance status ≥2, and >1 extranodal site) to calculate a score from 0-5 points. The original IPI identifies four risk groups with 5-year overall survival rates: Low Risk (0-1 points, ~73% OS), Low-Intermediate Risk (2 points, ~51% OS), High-Intermediate Risk (3 points, ~43% OS), and High Risk (4-5 points, ~26% OS). The Revised IPI (R-IPI) redistributes patients into three groups for better discrimination in the rituximab era: Very Good (0-1 points, 4-year PFS/OS 94%), Good (2 points, intermediate outcomes), and Poor (3-5 points, lowest survival rates). This prognostic tool enables risk-adapted treatment planning, clinical trial stratification, and patient counseling. High-risk patients should be considered for intensified treatment approaches, clinical trial enrollment, or novel therapeutic strategies, while low-risk patients may be candidates for standard R-CHOP therapy or less intensive approaches in clinical trials.",
    response_description="The calculated IPI score with both original IPI and R-IPI risk stratification and treatment recommendations",
    operation_id="dlbcl_ipi"
)
async def calculate_dlbcl_ipi(request: DlbclIpiRequest):
    """
    Calculates IPI for prognosis prediction in diffuse large B-cell lymphoma
    
    Predicts overall survival using five independent risk factors to stratify 
    DLBCL patients into risk groups for personalized treatment planning.
    
    Args:
        request: Clinical parameters for IPI calculation (5 risk factors)
        
    Returns:
        DlbclIpiResponse: IPI score with risk stratification and survival predictions
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dlbcl_ipi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DLBCL IPI",
                    "details": {"parameters": parameters}
                }
            )
        
        return DlbclIpiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DLBCL IPI",
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