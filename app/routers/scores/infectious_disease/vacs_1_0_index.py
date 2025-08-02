"""
Veterans Aging Cohort Study (VACS) 1.0 Index Router

Endpoint for calculating VACS 1.0 Index for 5-year mortality risk in HIV/HCV patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.vacs_1_0_index import (
    Vacs10IndexRequest,
    Vacs10IndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/vacs_1_0_index",
    response_model=Vacs10IndexResponse,
    summary="Calculate Veterans Aging Cohort Study (VACS) 1.0 Index",
    description="Calculates the VACS 1.0 Index to estimate 5-year all-cause mortality risk in patients with "
                "HIV and/or HCV. This validated prognostic tool integrates HIV-specific biomarkers (CD4 count, "
                "HIV-1 RNA) with general health indicators (hemoglobin, liver function via FIB-4, kidney function "
                "via eGFR, and hepatitis C co-infection status). The VACS Index provides better discrimination "
                "than HIV markers alone (C-statistic 0.77 vs 0.74) and has been validated across diverse populations "
                "including veterans, non-veterans, men, women, and different racial groups. Higher scores indicate "
                "increased mortality risk and guide clinical decision-making for treatment intensification, specialist "
                "referrals, and resource allocation. Most accurate in patients with at least 1 year of antiretroviral "
                "therapy exposure.",
    response_description="VACS 1.0 Index score with risk stratification, clinical interpretation, and component breakdown showing individual point contributions",
    operation_id="vacs_1_0_index"
)
async def calculate_vacs_1_0_index(request: Vacs10IndexRequest):
    """
    Calculates Veterans Aging Cohort Study (VACS) 1.0 Index
    
    Estimates 5-year all-cause mortality risk in HIV and/or HCV patients using a 
    comprehensive scoring system that combines HIV-specific and general health biomarkers.
    
    Args:
        request: Patient parameters including age, CD4 count, HIV RNA, hemoglobin, FIB-4 index, eGFR, and HCV status
        
    Returns:
        Vacs10IndexResponse: VACS score with risk category and detailed clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("vacs_1_0_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating VACS 1.0 Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return Vacs10IndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for VACS 1.0 Index",
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