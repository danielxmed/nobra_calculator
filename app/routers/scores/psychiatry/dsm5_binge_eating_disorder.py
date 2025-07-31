"""
DSM-5 Criteria for Binge Eating Disorder Router

Endpoint for evaluating DSM-5 Binge Eating Disorder diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.dsm5_binge_eating_disorder import (
    Dsm5BingeEatingDisorderRequest,
    Dsm5BingeEatingDisorderResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/dsm5_binge_eating_disorder", response_model=Dsm5BingeEatingDisorderResponse)
async def calculate_dsm5_binge_eating_disorder(request: Dsm5BingeEatingDisorderRequest):
    """
    Evaluates DSM-5 Criteria for Binge Eating Disorder
    
    The DSM-5 diagnostic criteria for Binge Eating Disorder requires all of the following:
    
    Criterion A: Recurrent episodes of binge eating characterized by eating unusually 
    large amounts of food while experiencing a feeling of loss of control
    
    Criterion B: Binge eating episodes include at least 3 of the following 5 features:
    - Eating much more rapidly than normal
    - Eating until feeling uncomfortably full
    - Eating large amounts when not feeling physically hungry
    - Eating alone due to embarrassment about eating behavior
    - Feeling disgusted, depressed, or very guilty afterward
    
    Criterion C: Marked distress regarding binge eating is present
    
    Criterion D: Binge eating occurs, on average, at least once a week for 3 months
    
    Criterion E: Exclusion criteria (both must be met):
    - Binge eating is NOT associated with recurrent compensatory behavior
    - Does NOT occur exclusively during anorexia nervosa, bulimia nervosa, or ARFID
    
    Severity Levels (based on episode frequency per week):
    - Mild: 1-3 episodes per week
    - Moderate: 4-7 episodes per week
    - Severe: 8-13 episodes per week
    - Extreme: 14 or more episodes per week
    
    Important Notes:
    - Weight or appearance is NOT part of the diagnostic criteria
    - This is a diagnostic aid, not a substitute for comprehensive clinical evaluation
    - Requires evaluation by qualified mental health professional
    
    Args:
        request: DSM-5 BED criteria parameters (11 diagnostic criteria)
        
    Returns:
        Dsm5BingeEatingDisorderResponse: Diagnostic result with severity and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dsm5_binge_eating_disorder", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating DSM-5 Criteria for Binge Eating Disorder",
                    "details": {"parameters": parameters}
                }
            )
        
        return Dsm5BingeEatingDisorderResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DSM-5 Criteria for Binge Eating Disorder",
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
                "message": "Internal error in evaluation",
                "details": {"error": str(e)}
            }
        )