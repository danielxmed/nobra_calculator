"""
United Kingdom Model for End-Stage Liver Disease (UKELD) Router

Endpoint for calculating UKELD score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.ukeld import (
    UkeldRequest,
    UkeldResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ukeld",
    response_model=UkeldResponse,
    summary="Calculate UKELD Score",
    description="Calculates the United Kingdom Model for End-Stage Liver Disease (UKELD) score for predicting "
                "mortality in end-stage liver disease patients and determining liver transplant eligibility. "
                "This validated scoring system uses four laboratory parameters (INR, creatinine, bilirubin, and sodium) "
                "to estimate 1-year mortality risk without transplantation. Developed specifically for the UK population, "
                "a score ≥49 indicates transplant eligibility (>9% 1-year mortality risk), while a score ≥60 predicts "
                "approximately 50% 1-year mortality. The UKELD score is used to prioritize patients on liver transplant "
                "waiting lists and guide clinical decision-making in end-stage liver disease management.",
    response_description="The calculated UKELD score with transplant eligibility determination and clinical management recommendations",
    operation_id="ukeld"
)
async def calculate_ukeld(request: UkeldRequest):
    """
    Calculates United Kingdom Model for End-Stage Liver Disease (UKELD) Score
    
    The UKELD is a validated scoring system that predicts mortality risk in patients with 
    end-stage liver disease and determines eligibility for liver transplantation in the UK. 
    It uses four readily available laboratory parameters:
    
    - INR (International Normalized Ratio): Reflects liver synthetic function
    - Serum Creatinine (µmol/L): Indicates kidney function, often impaired in advanced liver disease
    - Serum Bilirubin (µmol/L): Marker of liver function and bilirubin metabolism
    - Serum Sodium (mmol/L): Electrolyte balance, hyponatremia indicates poor prognosis
    
    The UKELD formula:
    UKELD = 5.395×ln(INR) + 1.485×ln(creatinine) + 3.13×ln(bilirubin) - 81.565×ln(sodium) + 435
    
    Score interpretation for UK transplant system:
    - <49: Below transplant threshold (<9% 1-year mortality risk)
    - 49-59: Transplant eligible (>9% 1-year mortality risk)
    - ≥60: High priority transplant (~50% 1-year mortality risk)
    
    The UKELD was developed from UK liver transplantation center data (2003-2007) and 
    is specifically calibrated for the UK population. It excludes patients with 
    hepatocellular carcinoma who may qualify through other criteria.
    
    Args:
        request: Laboratory parameters for UKELD calculation
        
    Returns:
        UkeldResponse: UKELD score with transplant eligibility and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ukeld", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating UKELD score",
                    "details": {"parameters": parameters}
                }
            )
        
        return UkeldResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for UKELD calculation",
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