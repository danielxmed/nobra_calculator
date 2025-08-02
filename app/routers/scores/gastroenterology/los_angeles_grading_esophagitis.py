"""
Los Angeles (LA) Grading of Esophagitis Router

Endpoint for calculating Los Angeles Grading of Esophagitis classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.los_angeles_grading_esophagitis import (
    LosAngelesGradingEsophagitisRequest,
    LosAngelesGradingEsophagitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/los_angeles_grading_esophagitis",
    response_model=LosAngelesGradingEsophagitisResponse,
    summary="Calculate Los Angeles (LA) Grading of Esophagitis",
    description="Classifies severity of erosive esophagitis based on endoscopic findings using the Los Angeles Classification system. "
                "This gold standard classification provides standardized criteria for grading mucosal breaks into four categories (A-D) "
                "based on size and circumferential extent. The system shows excellent inter-observer agreement and clinical correlation "
                "with symptoms and treatment response. Grades A-B represent mild esophagitis requiring 4 weeks of PPI therapy, while "
                "grades C-D represent severe esophagitis requiring 8 weeks of therapy and closer monitoring for complications. "
                "This classification is recommended by ACG guidelines and widely used for GERD management and research.",
    response_description="The calculated LA grade with comprehensive treatment recommendations and clinical management guidelines",
    operation_id="los_angeles_grading_esophagitis"
)
async def calculate_los_angeles_grading_esophagitis(request: LosAngelesGradingEsophagitisRequest):
    """
    Calculates Los Angeles (LA) Grading of Esophagitis
    
    Provides standardized endoscopic classification of erosive esophagitis severity
    based on mucosal break characteristics, with evidence-based treatment recommendations
    and clinical management guidelines according to ACG guidelines.
    
    Args:
        request: Endoscopic findings of mucosal break characteristics
        
    Returns:
        LosAngelesGradingEsophagitisResponse: LA grade with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("los_angeles_grading_esophagitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Los Angeles Grading of Esophagitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return LosAngelesGradingEsophagitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Los Angeles Grading of Esophagitis",
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