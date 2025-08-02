"""
Modified Hoehn and Yahr Scale for Parkinson's Disease Router

Endpoint for assessing Parkinson's disease severity and staging motor symptoms and functional disability.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_hoehn_and_yahr_scale import (
    ModifiedHoehnAndYahrScaleRequest,
    ModifiedHoehnAndYahrScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_hoehn_and_yahr_scale",
    response_model=ModifiedHoehnAndYahrScaleResponse,
    summary="Calculate Modified Hoehn and Yahr Scale for Parkinson's Disease",
    description="""Calculates the Modified Hoehn and Yahr Scale for assessing Parkinson's disease severity using the most widely used staging system in movement disorders.

The Modified Hoehn and Yahr Scale provides a global measure of Parkinson's disease progression based on motor symptoms and functional disability. This validated clinical staging tool helps healthcare providers:

- Stage disease severity from early unilateral involvement to end-stage disability
- Track disease progression over time with intermediate stages for better granularity
- Guide clinical decision-making for medication management and interventions
- Determine candidacy for advanced therapies like deep brain stimulation
- Assess functional capacity and care needs for patients and families

**Staging System (1967 Original + Modified Intermediate Stages):**
- **Stage 1**: Unilateral involvement only - minimal/no functional disability
- **Stage 1.5**: Unilateral and axial involvement - midline symptoms added
- **Stage 2**: Bilateral involvement without balance impairment - minimal disability
- **Stage 2.5**: Mild bilateral disease with recovery on pull test - early balance issues
- **Stage 3**: Bilateral disease with postural instability - first significant balance impairment
- **Stage 4**: Severe disability but can walk/stand unassisted - markedly incapacitated
- **Stage 5**: Wheelchair/bed-bound unless aided - complete invalidism requiring constant care

**Clinical Assessment Guidelines:**
- Assess during patient's typical "on" medication state when possible
- Pull test: Examiner stands behind patient and pulls backward on shoulders
- Stage represents overall functional capacity, not just worst symptoms
- Consider motor fluctuations and timing of assessment

**Clinical Decision Applications:**
- **Stages 1-3**: Minimally disabling - focus on exercise, education, symptom management
- **Stages 4-5**: Severely disabling - complex care planning, advanced therapies, caregiver support
- **Deep Brain Stimulation**: Typically considered at stages 3-4 with medication complications
- **Therapy Referrals**: Physical/occupational therapy needs increase with higher stages
- **Safety Planning**: Fall prevention and home modifications based on postural stability

**Disease Progression Insights:**
- Higher stages correlate with greater disability and reduced quality of life
- Progression varies widely between individuals (months to years per stage)
- Useful for prognosis counseling and resource planning
- Complements other assessments (UPDRS, cognitive testing, quality of life measures)

**Limitations:**
- Focuses primarily on motor symptoms, doesn't assess cognitive or psychiatric features
- Inter-rater reliability can vary, especially for intermediate stages (1.5, 2.5)
- Movement Disorder Society recommends original 1-5 scale due to limited validation of 0.5 increments
- Should not be used as sole assessment tool for comprehensive Parkinson's care""",
    response_description="The calculated Modified Hoehn and Yahr stage with clinical interpretation and evidence-based management recommendations",
    operation_id="modified_hoehn_and_yahr_scale"
)
async def calculate_modified_hoehn_and_yahr_scale(request: ModifiedHoehnAndYahrScaleRequest):
    """
    Calculates Modified Hoehn and Yahr Scale for Parkinson's Disease
    
    Assesses Parkinson's disease severity through clinical staging based on motor 
    symptoms and functional disability to guide treatment decisions and care planning.
    
    Args:
        request: Clinical stage assessment based on motor symptoms and functional capacity
        
    Returns:
        ModifiedHoehnAndYahrScaleResponse: Hoehn and Yahr stage with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_hoehn_and_yahr_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Hoehn and Yahr Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedHoehnAndYahrScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Hoehn and Yahr Scale",
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