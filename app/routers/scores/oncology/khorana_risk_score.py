"""
Khorana Risk Score for VTE in Cancer Patients Router

Endpoint for calculating Khorana Risk Score for venous thromboembolism.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.khorana_risk_score import (
    KhoranaRiskScoreRequest,
    KhoranaRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/khorana_risk_score",
    response_model=KhoranaRiskScoreResponse,
    summary="Calculate Khorana Risk Score for VTE in Cancer Patients",
    description="Calculates the Khorana Risk Score to predict venous thromboembolism (VTE) risk in cancer "
                "patients starting chemotherapy. This validated tool uses five clinical and laboratory "
                "variables: cancer type (very high-risk cancers like stomach/pancreas score 2 points), "
                "elevated platelet count (≥350×10⁹/L), low hemoglobin (<10 g/dL) or EPO use, elevated "
                "leukocyte count (>11×10⁹/L), and BMI ≥35 kg/m². The score stratifies patients into "
                "risk categories: low (0 points, ~5% VTE risk), intermediate (1-2 points, ~6.6% risk), "
                "and high (≥3 points, ~11% risk). High-risk patients benefit from thromboprophylaxis "
                "with LMWH, which reduces VTE risk by 64%. Not for use in brain tumor or myeloma patients.",
    response_description="VTE risk assessment with thromboprophylaxis recommendations based on the Khorana score",
    operation_id="khorana_risk_score"
)
async def calculate_khorana_risk_score(request: KhoranaRiskScoreRequest):
    """
    Calculates Khorana Risk Score for VTE in Cancer Patients
    
    The Khorana score is a validated tool for predicting VTE risk in cancer patients 
    receiving chemotherapy. It helps identify high-risk patients who may benefit from 
    thromboprophylaxis.
    
    Score Components:
    - Cancer type: Very high-risk (2 pts), high-risk (1 pt), standard (0 pts)
    - Platelet count ≥350×10⁹/L: 1 point
    - Hemoglobin <10 g/dL or EPO use: 1 point
    - Leukocyte count >11×10⁹/L: 1 point
    - BMI ≥35 kg/m²: 1 point
    
    Risk Categories and 6-Month VTE Incidence:
    - Low Risk (0 points): ~5.0%
    - Intermediate Risk (1-2 points): ~6.6%
    - High Risk (≥3 points): ~11.0%
    
    Clinical Recommendations:
    - High-risk patients: Consider LMWH thromboprophylaxis
    - Recent evidence suggests ≥2 points may be optimal cutoff
    - Risk-benefit discussion considering bleeding risk
    - Reassess with clinical changes
    
    Limitations:
    - Do NOT use for brain tumors or multiple myeloma
    - Limited sensitivity (23.4% of VTE patients classified as high risk)
    - Performance varies by cancer type
    
    Args:
        request: Khorana Risk Score parameters
        
    Returns:
        KhoranaRiskScoreResponse: VTE risk assessment with recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("khorana_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Khorana Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return KhoranaRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Khorana Risk Score",
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