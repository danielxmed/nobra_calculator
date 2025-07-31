"""
GAP Index for Idiopathic Pulmonary Fibrosis (IPF) Mortality Router

Endpoint for calculating GAP Index mortality risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.gap_index_ipf_mortality import (
    GapIndexIpfMortalityRequest,
    GapIndexIpfMortalityResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gap_index_ipf_mortality",
    response_model=GapIndexIpfMortalityResponse,
    summary="Calculate GAP Index for Idiopathic Pulmonary Fibrosis",
    description="Provides 1, 2, and 3-year mortality estimates for IPF patients. The GAP Index uses Gender, Age, and Physiology (FVC and DLCO) to predict mortality risk and guide clinical management decisions.",
    response_description="The calculated gap index ipf mortality with interpretation",
    operation_id="gap_index_ipf_mortality"
)
async def calculate_gap_index_ipf_mortality(request: GapIndexIpfMortalityRequest):
    """
    Calculates GAP Index for IPF Mortality Risk Assessment
    
    The GAP Index is a validated prognostic tool that stratifies IPF patients into 
    three mortality risk categories using Gender, Age, and Physiology (FVC and DLCO). 
    This enables clinicians to optimize management decisions, determine monitoring 
    frequency, and guide lung transplant evaluation timing.
    
    **Scoring Components**:
    - **Gender**: Female (0 points), Male (1 point)
    - **Age**: ≤60y (0), 61-65y (1), >65y (2 points)
    - **FVC % predicted**: >75% (0), 50-75% (1), <50% (2 points)
    - **DLCO % predicted**: >55% (0), 36-55% (1), ≤35% (2), Cannot perform (3 points)
    
    **Stage Classification and Management**:
    - **Stage I (0-3 points)**: Low risk - monitor every 6 months
    - **Stage II (4-5 points)**: Intermediate risk - monitor every 3-6 months, consider transplant
    - **Stage III (6-8 points)**: High risk - monitor every 3 months, urgent transplant evaluation
    
    **Clinical Applications**:
    - IPF prognosis and mortality risk stratification
    - Lung transplant evaluation timing decisions
    - Treatment planning and monitoring frequency
    - Patient counseling and advance care planning
    - Clinical trial stratification
    
    Args:
        request: Patient demographics and pulmonary function data required for 
                GAP Index calculation (gender, age, FVC %, DLCO %)
        
    Returns:
        GapIndexIpfMortalityResponse: GAP score with stage classification and 
                                    comprehensive management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gap_index_ipf_mortality", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GAP Index for IPF Mortality",
                    "details": {"parameters": parameters}
                }
            )
        
        return GapIndexIpfMortalityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GAP Index calculation",
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
                "message": "Internal error in GAP Index calculation",
                "details": {"error": str(e)}
            }
        )