"""
Main router for medical scores related endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.models.scores import (
    ScoreListResponse,
    ScoreMetadataResponse,
    ErrorResponse
)
from app.services.score_service import score_service
from app.services.calculator_service import calculator_service

# Import the specialty scores router
# NOTE: Temporarily commenting to fix API routes conflict
# from .scores import router as specialty_scores_router

router = APIRouter(
    prefix="/api",
    tags=["scores"],
    responses={
        404: {"model": ErrorResponse, "description": "Score not found"},
        422: {"model": ErrorResponse, "description": "Invalid parameters"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

# NOTE: Individual score endpoints are available at root level
# Individual calculator endpoints like /duke_iscvid_2023 continue to work
# Main API management routes are available here with /api prefix


@router.get("/scores", 
           response_model=ScoreListResponse,
           summary="List Available Medical Scores",
           description="Retrieve all available medical calculators and scores with optional filtering",
           response_description="Comprehensive list of available medical scores and calculators",
           operation_id="list_scores")
async def list_scores(
    category: Optional[str] = Query(
        None, 
        description="Filter by medical specialty (e.g., 'cardiology', 'nephrology', 'neurology')",
        example="cardiology"
    ),
    search: Optional[str] = Query(
        None, 
        description="Search scores by keywords in title or description",
        example="stroke risk"
    )
):
    """
    **List All Available Medical Scores and Calculators**
    
    Comprehensive catalog of medical scores, calculators, and assessment tools 
    available in the nobra_calculator API.
    
    **Available Categories:**
    - **Cardiology**: CHA₂DS₂-VASc, heart failure staging
    - **Nephrology**: CKD-EPI 2021, ABIC score
    - **Pulmonology**: CURB-65, 6-minute walk test, A-a gradient
    - **Neurology**: ABCD² score, 4AT delirium screen
    - **Hematology**: 4Ts HIT score
    - **Emergency Medicine**: COVID-19 4C mortality
    - **Pediatrics**: AAP hypertension guidelines
    - **Geriatrics**: Abbey pain scale
    - **Psychiatry**: AIMS tardive dyskinesia
    - **General Medicine**: AAS abuse screening
    
    **Search Functionality:**
    - Search by score name or abbreviation
    - Search by clinical condition
    - Search by medical specialty
    - Search by keywords in descriptions
    
    **Usage Examples:**
    - `/api/scores` - List all available scores
    - `/api/scores?category=cardiology` - Cardiology scores only
    - `/api/scores?search=stroke` - All stroke-related scores
    - `/api/scores?search=risk` - All risk assessment tools
    
    **Response Information:**
    Each score includes ID, title, description, category, and version information
    for easy identification and selection.
    """
    try:
        if search:
            # Search by term
            scores = score_service.search_scores(search)
        elif category:
            # Filter by category
            scores = score_service.get_scores_by_category(category)
        else:
            # List all scores
            scores = score_service.get_available_scores()
        
        return ScoreListResponse(
            scores=scores,
            total=len(scores)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error listing scores",
                "details": {"error": str(e)}
            }
        )


@router.get("/scores/{score_id}", 
           response_model=ScoreMetadataResponse,
           summary="Get Score Metadata",
           description="Retrieve comprehensive metadata for a specific medical score",
           response_description="Complete score information including parameters, interpretation ranges, and references",
           operation_id="get_score_metadata")
async def get_score_metadata(score_id: str):
    """
    **Get Comprehensive Metadata for a Specific Medical Score**
    
    Retrieves detailed information about a medical score including parameters,
    validation rules, interpretation ranges, clinical references, and usage notes.
    
    **Metadata Components:**
    - **Basic Information**: ID, title, description, category, version
    - **Parameters**: Required inputs with validation rules and units
    - **Result Information**: Output format and measurement units
    - **Interpretation Ranges**: Clinical thresholds and recommendations
    - **Scientific References**: Peer-reviewed citations and guidelines
    - **Mathematical Formula**: Calculation algorithm description
    - **Clinical Notes**: Important usage considerations and limitations
    
    **Use Cases:**
    - Understanding score requirements before calculation
    - Validating input parameters and ranges
    - Interpreting calculation results clinically
    - Implementing scores in other systems
    - Academic research and citation purposes
    - Quality assurance and validation
    
    **Parameter Information:**
    Each parameter includes data type, validation rules, clinical significance,
    measurement units, and example values for proper implementation.
    
    **Interpretation Guidance:**
    Detailed clinical interpretation ranges with specific recommendations
    for each score level, helping translate numerical results into
    actionable clinical decisions.
    """
    try:
        metadata = score_service.get_score_metadata(score_id)
        
        if metadata is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' not found",
                    "details": {"score_id": score_id}
                }
            )
        
        return metadata
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error getting score metadata",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )


@router.post("/{score_id}/calculate", summary="Calculate a Score", description="Calculate a score using the provided parameters", response_description="Calculation result with interpretation", operation_id="calculate_score_generic")
async def calculate_score_generic(score_id: str, parameters: Dict[str, Any]):
    """
    Generic endpoint to calculate any available score
    
    Args:
        score_id: ID of the score to be calculated
        parameters: Dictionary with the parameters required for calculation
        
    Returns:
        Dict: Calculation result with interpretation
    """
    try:
        # Check if the score exists
        if not score_service.score_exists(score_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' not found",
                    "details": {"score_id": score_id}
                }
            )
        
        # Check if the calculator is available
        if not calculator_service.is_calculator_available(score_id):
            raise HTTPException(
                status_code=501,
                detail={
                    "error": "CalculatorNotImplemented",
                    "message": f"Calculator for '{score_id}' not yet implemented",
                    "details": {"score_id": score_id}
                }
            )
        
        # Execute calculation
        result = calculator_service.calculate_score(score_id, parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": f"Error calculating {score_id}",
                    "details": {"parameters": parameters}
                }
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": f"Invalid parameters for {score_id}",
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


@router.get("/categories", summary="List Available Medical Categories", description="Retrieve all available medical categories", response_description="List of unique categories", operation_id="list_scores_categories")
async def list_categories():
    """
    Lists available medical categories
    
    Returns:
        Dict: List of unique categories
    """
    try:
        scores = score_service.get_available_scores()
        categories = list(set(score.category for score in scores))
        categories.sort()
        
        return {
            "categories": categories,
            "total": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error listing categories",
                "details": {"error": str(e)}
            }
        )


@router.post("/reload", summary="Reload Scores and Calculators", description="Reload all scores and calculators in the system", response_description="Status of the reload operation", operation_id="reload_scores")
async def reload_scores():
    """
    Reloads all scores and calculators in the system
    (Useful for development and updates)
    
    Returns:
        Dict: Status of the reload operation
    """
    try:
        # Reload scores and calculators
        score_service.reload_scores()
        calculator_service.reload_calculators()
        
        # Count how many scores were loaded
        scores = score_service.get_available_scores()
        
        return {
            "status": "success",
            "message": "Scores and calculators reloaded successfully",
            "scores_loaded": len(scores),
            "scores": [score.id for score in scores]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError", 
                "message": "Error reloading scores",
                "details": {"error": str(e)}
            }
        )


@router.get("/scores/{score_id}/validate", summary="Validate Score Calculator", description="Check if a calculator is available for the score", response_description="Validation status", operation_id="validate_score_calculator")
async def validate_score_calculator(score_id: str):
    """
    Validates if a calculator is available for the score
    
    Args:
        score_id: ID of the score
        
    Returns:
        Dict: Validation status
    """
    try:
        # Check if the score exists
        if not score_service.score_exists(score_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' not found",
                    "details": {"score_id": score_id}
                }
            )
        
        # Check if the calculator is available
        calculator_available = calculator_service.is_calculator_available(score_id)
        
        return {
            "score_id": score_id,
            "score_exists": True,
            "calculator_available": calculator_available,
            "status": "ready" if calculator_available else "no_calculator"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error validating score",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )