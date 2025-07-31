"""
BWH Egg Freezing Counseling Tool (EFCT) Router

Endpoint for calculating BWH Egg Freezing Counseling Tool predictions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gynecology.bwh_egg_freezing_counseling_tool import (
    BwhEggFreezingCounselingToolRequest,
    BwhEggFreezingCounselingToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bwh_egg_freezing_counseling_tool",
    response_model=BwhEggFreezingCounselingToolResponse,
    summary="Calculate BWH Egg Freezing Counseling Tool (EFCT)",
    description="Predicts likelihood of live birth for elective egg freezing in women. Developed by Brigham and Women's Hospital to provide evidence-based counseling for women considering elective egg freezing by predicting the probability of at least one, two, or three live births based on age and number of mature eggs.",
    response_description="The calculated bwh egg freezing counseling tool with interpretation",
    operation_id="calculate_bwh_egg_freezing_counseling_tool"
)
async def calculate_bwh_egg_freezing_counseling_tool(request: BwhEggFreezingCounselingToolRequest):
    """
    Calculates BWH Egg Freezing Counseling Tool (EFCT)
    
    Predicts likelihood of live birth for elective egg freezing in women based on age 
    and number of mature eggs retrieved. This evidence-based tool was developed at 
    Brigham and Women's Hospital to help counsel women considering elective egg freezing.
    
    The calculator provides probabilities for achieving:
    - At least one live birth
    - At least two live births  
    - At least three live births
    
    Key factors:
    - Age: Women's age at time of egg freezing (24-44 years)
    - Number of mature eggs: Total mature (MII) oocytes retrieved and frozen (1-100)
    
    The model accounts for:
    - Age-specific blastocyst formation rates
    - Age-specific rates of chromosomally normal (euploid) embryos
    - Live birth rate per euploid blastocyst (~60%)
    
    Important notes:
    - Designed for elective egg freezing in healthy women
    - May overestimate rates for medical egg freezing (e.g., cancer patients)
    - Less reliable for women ≥39 years due to limited data
    - Assumes standard vitrification techniques and experienced laboratory
    - Results are probabilities for counseling, not guarantees
    
    Args:
        request: Parameters needed for EFCT calculation (age and number of mature eggs)
        
    Returns:
        BwhEggFreezingCounselingToolResponse: Calculated probabilities with clinical 
        interpretation and counseling guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bwh_egg_freezing_counseling_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BWH Egg Freezing Counseling Tool",
                    "details": {"parameters": parameters}
                }
            )
        
        return BwhEggFreezingCounselingToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BWH Egg Freezing Counseling Tool",
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