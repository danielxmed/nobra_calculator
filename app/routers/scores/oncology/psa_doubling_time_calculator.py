"""
PSA Doubling Time (PSADT) Calculator Router

Endpoint for calculating PSA Doubling Time.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.psa_doubling_time_calculator import (
    PsaDoublingTimeCalculatorRequest,
    PsaDoublingTimeCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/psa_doubling_time_calculator",
    response_model=PsaDoublingTimeCalculatorResponse,
    summary="Calculate PSA Doubling Time (PSADT)",
    description="Calculates PSA doubling rate in prostate cancer patients with biochemical recurrence "
                "after treatment. This critical prognostic tool uses longitudinal PSA measurements to "
                "determine the rate of PSA increase over time, which strongly correlates with survival "
                "outcomes and guides treatment decisions. The calculator employs linear regression "
                "analysis of ln(PSA) versus time to compute doubling time using the formula: "
                "PSADT = ln(2) / slope. Risk stratification includes very high risk (<3 months), "
                "high risk (3-6 months), intermediate risk (6-12 months), low risk (12-36 months), "
                "and very low risk (>36 months) categories. Clinical applications include risk "
                "stratification for metastatic disease, treatment planning for salvage therapy, "
                "timing of imaging studies, monitoring during active surveillance, guidance for "
                "androgen deprivation therapy, and evaluation of castration-resistant disease "
                "progression. The tool requires minimum 2 PSA measurements with corresponding "
                "time points, though 3-5 measurements provide superior accuracy. Results should "
                "be interpreted alongside Gleason score, time to recurrence, and other clinical "
                "factors to optimize patient management and treatment selection.",
    response_description="The calculated PSA doubling time with comprehensive risk stratification and clinical guidance",
    operation_id="psa_doubling_time_calculator"
)
async def calculate_psa_doubling_time_calculator(request: PsaDoublingTimeCalculatorRequest):
    """
    Calculates PSA Doubling Time (PSADT)
    
    This prognostic tool calculates the rate of PSA increase in prostate cancer
    patients with biochemical recurrence to guide treatment decisions.
    
    Args:
        request: PSA measurements and time points for doubling time calculation
        
    Returns:
        PsaDoublingTimeCalculatorResponse: Result with doubling time and risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("psa_doubling_time_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating PSA Doubling Time",
                    "details": {"parameters": parameters}
                }
            )
        
        return PsaDoublingTimeCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for PSA Doubling Time Calculator",
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