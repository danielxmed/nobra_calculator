"""
IMDC (International Metastatic RCC Database Consortium) Risk Model Router

Endpoint for calculating IMDC Risk Model for metastatic renal cell carcinoma.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.imdc_risk_model import (
    ImdcRiskModelRequest,
    ImdcRiskModelResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/imdc_risk_model",
    response_model=ImdcRiskModelResponse,
    summary="Calculate IMDC Risk Model for Metastatic Renal Cell Carcinoma",
    description="Calculates the IMDC (International Metastatic RCC Database Consortium) Risk Model, "
                "the gold standard for risk stratification in patients with metastatic renal cell carcinoma "
                "treated with systemic therapy. This validated clinical prediction tool uses 6 prognostic "
                "factors to predict overall survival and guide treatment selection. The model stratifies "
                "patients into three risk categories: Favorable (0 factors, median OS 43.2 months), "
                "Intermediate (1-2 factors, median OS 22.5 months), and Poor (3-6 factors, median OS 7.8 months). "
                "Treatment recommendations include VEGF-targeted monotherapy for favorable risk patients and "
                "combination immunotherapy (ipilimumab + nivolumab) or cabozantinib for intermediate/poor risk patients. "
                "The model has been validated across multiple treatment settings including modern immunotherapy combinations "
                "and is used for clinical trial stratification, treatment sequencing, and patient counseling.",
    response_description="The calculated IMDC risk score with survival estimates and treatment recommendations based on risk stratification",
    operation_id="imdc_risk_model"
)
async def calculate_imdc_risk_model(request: ImdcRiskModelRequest):
    """
    Calculates IMDC (International Metastatic RCC Database Consortium) Risk Model
    
    Predicts survival in patients with metastatic renal cell carcinoma treated with 
    systemic therapy using 6 validated prognostic factors. Also known as Heng criteria 
    or IMDC criteria.
    
    Args:
        request: Clinical and laboratory parameters for risk assessment
        
    Returns:
        ImdcRiskModelResponse: Risk score with survival estimates and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("imdc_risk_model", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IMDC Risk Model",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImdcRiskModelResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IMDC Risk Model",
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