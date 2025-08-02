"""
Liver Decompensation Risk after Hepatectomy for HCC Router

Endpoint for calculating liver decompensation risk after hepatectomy for hepatocellular carcinoma.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.liver_decompensation_risk_hcc import (
    LiverDecompensationRiskHccRequest,
    LiverDecompensationRiskHccResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/liver_decompensation_risk_hcc",
    response_model=LiverDecompensationRiskHccResponse,
    summary="Calculate Liver Decompensation Risk after Hepatectomy for HCC",
    description="Calculates the Liver Decompensation Risk after Hepatectomy for Hepatocellular Carcinoma (HCC), "
                "a validated clinical prediction tool that stratifies patients into risk categories for post-operative "
                "liver decompensation. This evidence-based model was developed from analysis of 543 patients with HCC "
                "undergoing hepatectomy and enables informed surgical decision-making by identifying patients at low "
                "(4.9% decompensation rate), intermediate (28.6% rate), and high risk (60.0% rate) for adverse outcomes. "
                "The calculator uses hierarchical interaction of three key factors: portal hypertension (most significant "
                "predictor with OR 2.99), extent of hepatectomy (major vs minor resection with OR 2.41), and MELD score "
                "category (>9 vs ≤9 with OR 2.26). Clinical applications include preoperative risk assessment, surgical "
                "planning, perioperative management optimization, alternative treatment consideration, and patient counseling "
                "for informed consent. High-risk patients (major resection + portal hypertension) should be carefully "
                "evaluated for alternative treatments including liver transplantation, ablative therapies, or TACE.",
    response_description="The calculated liver decompensation risk percentage with risk category classification and comprehensive management recommendations",
    operation_id="liver_decompensation_risk_hcc"
)
async def calculate_liver_decompensation_risk_hcc(request: LiverDecompensationRiskHccRequest):
    """
    Calculates liver decompensation risk after hepatectomy for HCC
    
    The Liver Decompensation Risk calculator is a validated clinical decision tool 
    that predicts the probability of post-operative liver decompensation in patients 
    with hepatocellular carcinoma undergoing hepatic resection. This evidence-based 
    model stratifies patients into three risk categories based on hierarchical 
    interaction of portal hypertension, hepatectomy extent, and MELD score.
    
    Args:
        request: Clinical parameters including portal hypertension status, 
                planned hepatectomy extent, and MELD score category for risk calculation
        
    Returns:
        LiverDecompensationRiskHccResponse: Risk percentage with clinical interpretation 
                                           and evidence-based management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("liver_decompensation_risk_hcc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Liver Decompensation Risk after Hepatectomy for HCC",
                    "details": {"parameters": parameters}
                }
            )
        
        return LiverDecompensationRiskHccResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Liver Decompensation Risk calculation",
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
                "message": "Internal error in Liver Decompensation Risk calculation",
                "details": {"error": str(e)}
            }
        )