"""
Montreal Cognitive Assessment (MoCA) Router

Endpoint for calculating MoCA cognitive screening score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.moca import (
    MocaRequest,
    MocaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/moca",
    response_model=MocaResponse,
    summary="Calculate Montreal Cognitive Assessment (MoCA)",
    description="Calculates the MoCA score for screening mild cognitive impairment across multiple cognitive domains. "
                "The MoCA is a 30-point cognitive screening tool that assesses visuospatial/executive function, naming, "
                "attention, language, abstraction, delayed recall, and orientation. It is more sensitive than the MMSE "
                "for detecting mild cognitive impairment and takes approximately 10-15 minutes to administer. The assessment "
                "includes an education adjustment factor (add 1 point if ≤12 years formal education). Scores ≥26 indicate "
                "normal cognition, 18-25 suggest possible mild cognitive impairment, 10-17 indicate moderate impairment, "
                "and <10 suggest severe cognitive impairment. The tool is widely validated across multiple populations and "
                "available in many languages, making it an essential screening instrument in clinical practice.",
    response_description="The calculated MoCA score with cognitive status classification and clinical recommendations",
    operation_id="moca"
)
async def calculate_moca(request: MocaRequest):
    """
    Calculates Montreal Cognitive Assessment (MoCA)
    
    The MoCA assesses 8 cognitive domains:
    
    1. Visuospatial/Executive (5 pts): Trail making, cube copy, clock drawing
    2. Naming (3 pts): Lion, rhinoceros, camel identification
    3. Memory Registration (5 pts): Not counted in total, used for delayed recall
    4. Attention (6 pts): Digit spans, vigilance, serial 7 subtraction
    5. Language (3 pts): Sentence repetition, phonemic fluency
    6. Abstraction (2 pts): Similarities between word pairs
    7. Delayed Recall (5 pts): Free recall of 5 words without cues
    8. Orientation (6 pts): Date, month, year, day, place, city
    
    Education adjustment:
    - Add 1 point if formal education ≤12 years
    - Maximum total remains 30 points
    
    Score interpretation:
    - ≥26: Normal cognition
    - 18-25: Possible mild cognitive impairment (MCI)
    - 10-17: Moderate cognitive impairment
    - <10: Severe cognitive impairment
    
    Clinical significance:
    - More sensitive than MMSE for detecting MCI
    - Cut-off <26 indicates need for further evaluation
    - Validated across diverse populations and languages
    - Essential tool for early detection of cognitive decline
    
    Args:
        request: MoCA assessment parameters including all cognitive domain scores and education level
        
    Returns:
        MocaResponse: MoCA total score with cognitive status and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("moca", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MoCA score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MocaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MoCA calculation",
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
                "message": "Internal error in MoCA calculation",
                "details": {"error": str(e)}
            }
        )