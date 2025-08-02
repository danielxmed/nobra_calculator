"""
Lille Model for Alcoholic Hepatitis Router

Endpoint for calculating the Lille Model to predict mortality in alcoholic 
hepatitis patients not responding to steroid therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.lille_model import (
    LilleModelRequest,
    LilleModelResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lille_model",
    response_model=LilleModelResponse,
    summary="Calculate Lille Model for Alcoholic Hepatitis",
    description="Calculates the Lille Model for Alcoholic Hepatitis, a validated prognostic tool "
                "that predicts mortality in patients with severe alcoholic hepatitis not responding "
                "to corticosteroid therapy. Developed by Louvet et al. in 2007, this sophisticated "
                "model enables clinicians to identify steroid non-responders early (at day 7) with "
                "exceptional accuracy (AUROC 0.89). The model uses six clinical parameters including "
                "age, albumin, baseline and day-7 bilirubin, creatinine, and prothrombin time to "
                "calculate a score ranging from 0.0-1.0. The critical threshold of 0.45 divides "
                "patients into responders (score <0.45, 85% 6-month survival) who should continue "
                "steroids, and non-responders (score ≥0.45, 25% 6-month survival) who should "
                "discontinue steroids and be evaluated for alternative therapies including urgent "
                "liver transplantation. Essential for hepatology consultation, ICU management, and "
                "transplant evaluation decisions in severe alcoholic hepatitis.",
    response_description="The calculated Lille Model score with response classification, survival estimates, and evidence-based treatment recommendations for alcoholic hepatitis management",
    operation_id="lille_model"
)
async def calculate_lille_model(request: LilleModelRequest):
    """
    Calculates the Lille Model for alcoholic hepatitis prognosis
    
    The Lille Model is a validated prognostic tool that predicts mortality in patients 
    with severe alcoholic hepatitis undergoing corticosteroid therapy. This model 
    enables early identification of steroid non-responders, facilitating critical 
    decisions about treatment continuation versus alternative therapeutic approaches 
    including liver transplantation evaluation.
    
    Args:
        request: Clinical parameters including age, laboratory values at days 0 and 7 
                of steroid therapy for Lille Model calculation
        
    Returns:
        LilleModelResponse: Prognostic score with response classification and 
                           evidence-based treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lille_model", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Lille Model for Alcoholic Hepatitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return LilleModelResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Lille Model calculation",
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
                "message": "Internal error in Lille Model calculation",
                "details": {"error": str(e)}
            }
        )