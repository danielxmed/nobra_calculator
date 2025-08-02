"""
Immune-Related Adverse Events for GI Toxicity - Colitis Router

Endpoint for grading colitis severity in immune checkpoint inhibitor therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.immune_related_adverse_events_gi_colitis import (
    ImmuneRelatedAdverseEventsGiColitisRequest,
    ImmuneRelatedAdverseEventsGiColitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immune_related_adverse_events_gi_colitis",
    response_model=ImmuneRelatedAdverseEventsGiColitisResponse,
    summary="Grade Immune-Related Adverse Events for GI Colitis",
    description="Grades severity of colitis secondary to immune checkpoint inhibitor (ICPi) therapy "
                "based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria. "
                "This standardized grading system evaluates four key clinical parameters: stool frequency "
                "increase over baseline, presence of fecal incontinence, functional impact on activities "
                "of daily living, and hospitalization needs. The calculator provides evidence-based "
                "management recommendations including ICPi therapy decisions, corticosteroid treatment, "
                "gastroenterology consultation needs, and monitoring for life-threatening complications. "
                "ICPi-induced colitis most frequently occurs 5-10 weeks after treatment initiation and "
                "is more common with anti-CTLA-4 agents (ipilimumab) than anti-PD-1/PD-L1 therapy. "
                "Grade 1 (mild): Continue ICPi with dietary modifications. Grade 2 (moderate): Hold ICPi, "
                "corticosteroids, gastroenterology consultation. Grade 3-4 (severe/life-threatening): "
                "Consider permanent CTLA-4 discontinuation, hospitalization, high-dose steroids, infliximab. "
                "Mortality rate up to 1-2% for severe cases mainly from perforation/sepsis complications. "
                "Essential for oncologists, gastroenterologists, and multidisciplinary teams managing "
                "patients on immunotherapy.",
    response_description="The calculated irAE grade with detailed management recommendations for colitis secondary to immune checkpoint inhibitor therapy",
    operation_id="immune_related_adverse_events_gi_colitis"
)
async def calculate_immune_related_adverse_events_gi_colitis(request: ImmuneRelatedAdverseEventsGiColitisRequest):
    """
    Calculates Immune-Related Adverse Events for GI Toxicity - Colitis
    
    Grades severity of colitis secondary to immune checkpoint inhibitor therapy
    and provides standardized management recommendations based on CTCAE v5.0 criteria.
    
    Args:
        request: Clinical parameters including stool frequency, incontinence, functional impact, and hospitalization needs
        
    Returns:
        ImmuneRelatedAdverseEventsGiColitisResponse: irAE grade with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immune_related_adverse_events_gi_colitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immune-Related Adverse Events for GI Colitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmuneRelatedAdverseEventsGiColitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immune-Related Adverse Events GI colitis grading",
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