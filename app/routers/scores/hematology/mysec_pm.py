"""
Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM) Router

Endpoint for calculating MYSEC-PM for secondary myelofibrosis risk stratification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.mysec_pm import (
    MysecPmRequest,
    MysecPmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mysec_pm",
    response_model=MysecPmResponse,
    summary="Calculate MYSEC-PM Score",
    description="Calculates the Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM) for risk stratification in patients with myelofibrosis secondary to polycythemia vera (PV) or essential thrombocythemia (ET). This specialized prognostic model incorporates clinical parameters (age, hemoglobin, circulating blasts, platelet count, constitutional symptoms) and molecular genetics (CALR mutation status) to provide superior risk stratification compared to models designed for primary myelofibrosis. The score stratifies patients into four risk categories (Low, Intermediate-1, Intermediate-2, High) with significantly different survival outcomes (median survival: not reached, 9.3 years, 4.4 years, and 2.0 years, respectively). Adopted by NCCN and European guidelines for secondary myelofibrosis management.",
    response_description="The calculated MYSEC-PM score with risk stratification, survival prediction, and comprehensive treatment recommendations for secondary myelofibrosis",
    operation_id="mysec_pm"
)
async def calculate_mysec_pm(request: MysecPmRequest):
    """
    Calculates Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM)
    
    Specialized prognostic model for secondary myelofibrosis incorporating clinical
    and molecular parameters to guide treatment decisions and transplantation timing.
    
    Args:
        request: Clinical and molecular parameters for secondary myelofibrosis assessment
        
    Returns:
        MysecPmResponse: Score with detailed risk stratification and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mysec_pm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MYSEC-PM Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MysecPmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MYSEC-PM Score",
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