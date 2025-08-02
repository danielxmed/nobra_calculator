"""
Truelove and Witts Severity Index for Ulcerative Colitis Router

Endpoint for calculating the Truelove and Witts Severity Index for ulcerative colitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.truelove_witts_severity_index import (
    TrueloveWittsSeverityIndexRequest,
    TrueloveWittsSeverityIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/truelove_witts_severity_index",
    response_model=TrueloveWittsSeverityIndexResponse,
    summary="Calculate Truelove and Witts Severity Index for Ulcerative Colitis",
    description="Calculates the Truelove and Witts Severity Index to stratify ulcerative colitis "
                "severity into mild, moderate, or severe categories. This classic index, developed "
                "in 1955, evaluates six clinical and laboratory parameters: bowel movement frequency, "
                "blood in stool, fever, tachycardia, anemia, and ESR. The classification guides "
                "treatment decisions - mild disease can often be managed outpatient with "
                "aminosalicylates, while severe disease requires immediate hospitalization and "
                "intensive medical therapy with corticosteroids, biologics, or surgical consultation. "
                "This scoring system remains widely used in clinical practice and research for "
                "initial assessment and monitoring treatment response in ulcerative colitis patients.",
    response_description="The calculated severity classification with clinical interpretation and management recommendations",
    operation_id="truelove_witts_severity_index"
)
async def calculate_truelove_witts_severity_index(request: TrueloveWittsSeverityIndexRequest):
    """
    Calculates the Truelove and Witts Severity Index for Ulcerative Colitis
    
    The Truelove and Witts Severity Index is a validated clinical tool that stratifies 
    ulcerative colitis severity based on six parameters. It was developed in 1955 as 
    part of the first clinical trial demonstrating cortisone effectiveness in UC.
    
    Classification Logic:
    - Mild: All six criteria for mild severity are met
    - Severe: ≥6 bowel movements AND ≥1 systemic feature (fever, tachycardia, anemia)  
    - Moderate: Between mild and severe criteria
    
    Args:
        request: Parameters including bowel movements, blood in stool, fever, 
                tachycardia, anemia, and ESR status
        
    Returns:
        TrueloveWittsSeverityIndexResponse: Severity classification with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("truelove_witts_severity_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Truelove and Witts Severity Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return TrueloveWittsSeverityIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Truelove and Witts Severity Index",
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