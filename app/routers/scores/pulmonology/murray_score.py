"""
Murray Score for Acute Lung Injury Router

Endpoint for calculating Murray Score to stratify acute lung injury severity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.murray_score import (
    MurrayScoreRequest,
    MurrayScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/murray_score",
    response_model=MurrayScoreResponse,
    summary="Calculate Murray Score for Acute Lung Injury",
    description="Stratifies severity of acute lung injury (ALI) and acute respiratory distress syndrome (ARDS) "
                "using four objective physiological parameters: chest X-ray consolidation, oxygenation status, "
                "PEEP requirements, and lung compliance. The Murray Score provides standardized assessment "
                "of lung injury severity and is used for clinical decision-making, including evaluation for "
                "extracorporeal membrane oxygenation (ECMO) candidacy in severe cases. This validated tool "
                "enables objective communication about disease severity, guides treatment intensity, and "
                "helps stratify patients for research and quality improvement purposes. The score ranges "
                "from 0 to 4, with higher scores indicating more severe lung injury requiring intensive "
                "interventions and associated with worse prognosis.",
    response_description="The calculated Murray Score with lung injury severity classification and comprehensive management recommendations",
    operation_id="murray_score"
)
async def calculate_murray_score(request: MurrayScoreRequest):
    """
    Calculates Murray Score for Acute Lung Injury
    
    The Murray Score is a validated tool for stratifying acute lung injury severity
    using four objective physiological parameters, providing standardized assessment
    to guide clinical management and research applications.
    
    Args:
        request: Four component scores including chest X-ray consolidation,
                hypoxemia severity, PEEP requirements, and lung compliance
        
    Returns:
        MurrayScoreResponse: Lung injury severity classification with detailed management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("murray_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Murray Score for Acute Lung Injury",
                    "details": {"parameters": parameters}
                }
            )
        
        return MurrayScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Murray Score",
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