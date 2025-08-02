"""
Immune-Related Adverse Events for Endocrine Toxicities - Hypothyroidism Router

Endpoint for grading hypothyroidism severity in immune checkpoint inhibitor therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.immune_related_adverse_events_endocrine_hypothyroidism import (
    ImmuneRelatedAdverseEventsEndocrineHypothyroidismRequest,
    ImmuneRelatedAdverseEventsEndocrineHypothyroidismResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immune_related_adverse_events_endocrine_hypothyroidism",
    response_model=ImmuneRelatedAdverseEventsEndocrineHypothyroidismResponse,
    summary="Grade Immune-Related Adverse Events for Endocrine Hypothyroidism",
    description="Grades severity of hypothyroidism secondary to immune checkpoint inhibitor (ICPi) therapy "
                "based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria. "
                "This standardized grading system evaluates three key clinical parameters: TSH levels, "
                "symptom severity/functional status, and presence of myxedema or life-threatening complications. "
                "The calculator provides evidence-based management recommendations including ICPi therapy decisions, "
                "hormone replacement therapy needs, monitoring requirements, and consultation recommendations. "
                "ICPi-induced hypothyroidism is more common with anti-PD-1/PD-L1 agents than anti-CTLA-4 therapy, "
                "can occur at any time during treatment, and often requires lifelong thyroid hormone replacement. "
                "Grade 1 (mild): Continue ICPi with TSH monitoring every 4-6 weeks. Grade 2 (moderate): "
                "May hold ICPi, consider endocrinology consultation and hormone replacement. "
                "Grade 3-4 (severe/life-threatening): Hold ICPi, urgent consultation, immediate hormone replacement, "
                "hospitalization for myxedema coma. The grading system is essential for oncologists, "
                "endocrinologists, and multidisciplinary teams managing patients on immunotherapy.",
    response_description="The calculated irAE grade with detailed management recommendations for hypothyroidism secondary to immune checkpoint inhibitor therapy",
    operation_id="immune_related_adverse_events_endocrine_hypothyroidism"
)
async def calculate_immune_related_adverse_events_endocrine_hypothyroidism(request: ImmuneRelatedAdverseEventsEndocrineHypothyroidismRequest):
    """
    Calculates Immune-Related Adverse Events for Endocrine Toxicities - Hypothyroidism
    
    Grades severity of hypothyroidism secondary to immune checkpoint inhibitor therapy
    and provides standardized management recommendations based on CTCAE v5.0 criteria.
    
    Args:
        request: Clinical parameters including TSH level, symptom severity, and myxedema signs
        
    Returns:
        ImmuneRelatedAdverseEventsEndocrineHypothyroidismResponse: irAE grade with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immune_related_adverse_events_endocrine_hypothyroidism", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immune-Related Adverse Events for Endocrine Hypothyroidism",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmuneRelatedAdverseEventsEndocrineHypothyroidismResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immune-Related Adverse Events hypothyroidism grading",
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