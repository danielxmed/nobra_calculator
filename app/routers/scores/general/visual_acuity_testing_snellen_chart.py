"""
Visual Acuity Testing (Snellen Chart) Router

Endpoint for calculating Visual Acuity Testing (Snellen Chart) assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.visual_acuity_testing_snellen_chart import (
    VisualAcuityTestingSnellenChartRequest,
    VisualAcuityTestingSnellenChartResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/visual_acuity_testing_snellen_chart",
    response_model=VisualAcuityTestingSnellenChartResponse,
    summary="Calculate Visual Acuity Testing (Snellen Chart)",
    description="Assesses binocular and monocular visual acuity using standardized Snellen optotypes. "
                "This fundamental ophthalmologic and neurologic test evaluates the clarity of vision by "
                "determining the smallest line of letters a patient can accurately read on a standardized "
                "chart at a specific distance. The Snellen chart, developed by Herman Snellen in 1862, "
                "remains the gold standard for visual acuity assessment in clinical practice. The test "
                "is essential for routine vision screening, ophthalmologic examinations, neurologic "
                "assessments (cranial nerve II evaluation), pre-operative evaluation, and legal/disability "
                "determination. Visual acuity is expressed in standard notation (e.g., 20/20, 20/40) where "
                "the numerator represents testing distance and denominator represents the distance at which "
                "a normal eye can read the same line. Results guide clinical decision-making from routine "
                "care for normal vision (20/20) to urgent evaluation for severe impairment (20/200 or worse, "
                "which constitutes legal blindness in the United States). For patients unable to read letters, "
                "sequential testing includes counting fingers, hand motion, light perception, and no light "
                "perception assessments.",
    response_description="Visual acuity measurement with clinical interpretation, impairment classification, and detailed assessment including follow-up recommendations",
    operation_id="visual_acuity_testing_snellen_chart"
)
async def calculate_visual_acuity_testing_snellen_chart(request: VisualAcuityTestingSnellenChartRequest):
    """
    Calculates Visual Acuity Testing (Snellen Chart)
    
    Assesses visual acuity using standardized Snellen optotypes to evaluate 
    clarity of vision and detect visual impairment requiring intervention.
    
    Args:
        request: Eye tested, line read, testing distance, and corrective lens status
        
    Returns:
        VisualAcuityTestingSnellenChartResponse: Visual acuity with clinical interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("visual_acuity_testing_snellen_chart", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Visual Acuity Testing (Snellen Chart)",
                    "details": {"parameters": parameters}
                }
            )
        
        return VisualAcuityTestingSnellenChartResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Visual Acuity Testing (Snellen Chart)",
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