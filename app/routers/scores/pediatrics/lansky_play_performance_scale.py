"""
Lansky Play-Performance Scale for Pediatric Functional Status Router

Endpoint for calculating Lansky Play-Performance Scale functional assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.lansky_play_performance_scale import (
    LanskyPlayPerformanceScaleRequest,
    LanskyPlayPerformanceScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lansky_play_performance_scale",
    response_model=LanskyPlayPerformanceScaleResponse,
    summary="Calculate Lansky Play-Performance Scale for Pediatric Functional Status",
    description="Assesses functional status in pediatric patients (under 16 years) using the validated "
                "Lansky Play-Performance Scale. This parent-reported assessment evaluates a child's ability "
                "to perform normal activities and participate in play, providing crucial information about "
                "functional capacity and quality of life. Primarily used in pediatric oncology settings "
                "to monitor treatment response, assess clinical trial eligibility, and guide care planning. "
                "The scale ranges from 0 (unresponsive) to 100 (fully active, normal) in increments of 10.",
    response_description="The Lansky Play-Performance Scale score with functional status assessment and clinical recommendations for pediatric care planning",
    operation_id="lansky_play_performance_scale"
)
async def calculate_lansky_play_performance_scale(request: LanskyPlayPerformanceScaleRequest):
    """
    Calculates Lansky Play-Performance Scale for Pediatric Functional Status
    
    The Lansky Play-Performance Scale is a validated tool specifically designed 
    for assessing functional status in pediatric patients, particularly those 
    with cancer or chronic illnesses. It provides a standardized method for 
    evaluating a child's ability to perform age-appropriate activities and 
    participate in play.
    
    Clinical Applications:
    - Pediatric oncology treatment monitoring and response assessment
    - Clinical trial eligibility determination for pediatric studies
    - Functional status evaluation in chronic pediatric conditions
    - Quality of life assessment during treatment and recovery
    - Communication tool for multidisciplinary care teams
    - Prognosis assessment and long-term care planning
    
    Assessment Method:
    - Parent/caregiver report of child's typical functional performance
    - Observation-based evaluation of activity and play capacity
    - Consideration of age-appropriate developmental expectations
    - Regular reassessment to monitor changes over time
    
    Score Interpretation:
    - 100-80 points: Normal to minimal disability (able to carry on normal activity)
    - 70-50 points: Mild to moderate disability (some activity restrictions)
    - 40-20 points: Moderate to severe disability (significant limitations)
    - 10-0 points: Severe to complete disability (extensive care needs)
    
    Important Considerations:
    - Designed specifically for children under 16 years of age
    - Should be used in conjunction with other clinical assessments
    - Requires parent/caregiver input for accurate evaluation
    - Cultural and developmental factors should be considered
    - Not intended as sole criterion for major treatment decisions
    
    Args:
        request: Performance status score (0-100 in increments of 10) representing 
                the child's current functional capacity based on activity level and play ability
        
    Returns:
        LanskyPlayPerformanceScaleResponse: Functional status score with detailed assessment and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lansky_play_performance_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Lansky Play-Performance Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return LanskyPlayPerformanceScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Lansky Play-Performance Scale calculation",
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
                "message": "Internal error in Lansky Play-Performance Scale calculation",
                "details": {"error": str(e)}
            }
        )