"""
Mumtaz Score for Readmission in Cirrhosis Router

Endpoint for calculating 30-day readmission risk in patients with decompensated cirrhosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.mumtaz_score import (
    MumtazScoreRequest,
    MumtazScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mumtaz_score",
    response_model=MumtazScoreResponse,
    summary="Calculate Mumtaz Score for Readmission in Cirrhosis",
    description="Predicts 30-day readmission risk in patients with decompensated cirrhosis following hospital "
                "discharge. This validated prognostic tool incorporates clinical and laboratory parameters "
                "available at discharge to identify high-risk patients who may benefit from enhanced "
                "transitional care interventions and close outpatient follow-up. The score uses eight "
                "variables including age, serum sodium, albumin, length of stay, previous admissions, "
                "MELD score, hepatic encephalopathy, and ascites to calculate readmission probability. "
                "Risk stratification enables targeted resource allocation and care coordination to reduce "
                "preventable readmissions and improve patient outcomes in this vulnerable population.",
    response_description="The calculated 30-day readmission risk with detailed management recommendations and care coordination guidance",
    operation_id="mumtaz_score"
)
async def calculate_mumtaz_score(request: MumtazScoreRequest):
    """
    Calculates Mumtaz Score for Readmission in Cirrhosis
    
    The Mumtaz Score is a validated prognostic tool that predicts 30-day readmission
    risk in patients with decompensated cirrhosis, enabling targeted interventions
    and improved care coordination during the vulnerable post-discharge period.
    
    Args:
        request: Clinical and laboratory parameters including age, serum sodium,
                albumin, length of stay, previous admissions, MELD score, and
                presence of complications (hepatic encephalopathy and ascites)
        
    Returns:
        MumtazScoreResponse: Readmission risk percentage with clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mumtaz_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mumtaz Score for Readmission in Cirrhosis",
                    "details": {"parameters": parameters}
                }
            )
        
        return MumtazScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mumtaz Score",
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