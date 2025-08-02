"""
Immune-Related Adverse Events for Lung Toxicity - Pneumonitis Router

Endpoint for grading pneumonitis severity in immune checkpoint inhibitor therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.immune_related_adverse_events_lung_pneumonitis import (
    ImmuneRelatedAdverseEventsLungPneumonitisRequest,
    ImmuneRelatedAdverseEventsLungPneumonitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immune_related_adverse_events_lung_pneumonitis",
    response_model=ImmuneRelatedAdverseEventsLungPneumonitisResponse,
    summary="Grade Immune-Related Adverse Events for Lung Pneumonitis",
    description="Grades severity of pneumonitis secondary to immune checkpoint inhibitor (ICPi) therapy "
                "based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria. "
                "This standardized grading system evaluates respiratory symptoms, oxygen requirements, "
                "and functional impact to determine the severity of immune-mediated pneumonitis and guide "
                "clinical management decisions including ICPi therapy continuation, corticosteroid treatment, "
                "pulmonology consultation needs, and monitoring for life-threatening respiratory complications. "
                "ICPi-induced pneumonitis has an incidence of 2.7% for all-grade and 0.8% for high-grade "
                "pneumonitis in single-agent therapy, with onset typically occurring 2-24 weeks after "
                "treatment initiation. Grade 1 (mild): Continue ICPi with close monitoring. Grade 2 "
                "(moderate): Hold ICPi, corticosteroids, pulmonology consultation. Grade 3-4 "
                "(severe/life-threatening): Permanently discontinue ICPi, high-dose steroids, hospitalization, "
                "ICU admission for Grade 4. Essential for oncologists, pulmonologists, and critical care "
                "teams managing patients on immunotherapy to prevent respiratory failure and death.",
    response_description="The calculated irAE grade with detailed management recommendations for pneumonitis secondary to immune checkpoint inhibitor therapy",
    operation_id="immune_related_adverse_events_lung_pneumonitis"
)
async def calculate_immune_related_adverse_events_lung_pneumonitis(request: ImmuneRelatedAdverseEventsLungPneumonitisRequest):
    """
    Calculates Immune-Related Adverse Events for Lung Toxicity - Pneumonitis
    
    Grades severity of pneumonitis secondary to immune checkpoint inhibitor therapy
    and provides standardized management recommendations based on CTCAE v5.0 criteria.
    
    Args:
        request: Clinical parameters including respiratory symptoms, functional impact, oxygen requirements, radiographic findings, and hospitalization needs
        
    Returns:
        ImmuneRelatedAdverseEventsLungPneumonitisResponse: irAE grade with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immune_related_adverse_events_lung_pneumonitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immune-Related Adverse Events for Lung Pneumonitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmuneRelatedAdverseEventsLungPneumonitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immune-Related Adverse Events lung pneumonitis grading",
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