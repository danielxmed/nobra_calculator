"""
Immune-Related Adverse Events for Endocrine Toxicities - Diabetes Mellitus Router

Endpoint for grading hyperglycemia severity in immune checkpoint inhibitor therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.immune_related_adverse_events_endocrine_diabetes import (
    ImmuneRelatedAdverseEventsEndocrineDiabetesRequest,
    ImmuneRelatedAdverseEventsEndocrineDiabetesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immune_related_adverse_events_endocrine_diabetes",
    response_model=ImmuneRelatedAdverseEventsEndocrineDiabetesResponse,
    summary="Grade Immune-Related Adverse Events for Endocrine Diabetes Mellitus",
    description="Grades severity of hyperglycemia secondary to immune checkpoint inhibitor (ICPi) therapy "
                "based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria. "
                "This standardized grading system evaluates three key clinical parameters: fasting glucose levels, "
                "evidence of ketosis or Type 1 diabetes mellitus, and symptom severity/functional status. "
                "The calculator provides evidence-based management recommendations including ICPi therapy decisions, "
                "monitoring requirements, treatment interventions, and consultation needs. "
                "ICPi-induced diabetes mellitus often presents as fulminant Type 1 diabetes with diabetic "
                "ketoacidosis (DKA) in 67.4% of cases, requiring immediate recognition and appropriate management. "
                "Grade 1 (mild): Continue ICPi with close monitoring. Grade 2 (moderate): May hold ICPi, "
                "urgent endocrine consultation. Grade 3-4 (severe/life-threatening): Hold ICPi, insulin therapy, "
                "hospitalization. The grading system is essential for oncologists, endocrinologists, and "
                "multidisciplinary teams managing patients on immunotherapy.",
    response_description="The calculated irAE grade with detailed management recommendations for hyperglycemia secondary to immune checkpoint inhibitor therapy",
    operation_id="immune_related_adverse_events_endocrine_diabetes"
)
async def calculate_immune_related_adverse_events_endocrine_diabetes(request: ImmuneRelatedAdverseEventsEndocrineDiabetesRequest):
    """
    Calculates Immune-Related Adverse Events for Endocrine Toxicities - Diabetes Mellitus
    
    Grades severity of hyperglycemia secondary to immune checkpoint inhibitor therapy
    and provides standardized management recommendations based on CTCAE v5.0 criteria.
    
    Args:
        request: Clinical parameters including glucose level, ketosis/T1DM evidence, and symptoms
        
    Returns:
        ImmuneRelatedAdverseEventsEndocrineDiabetesResponse: irAE grade with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immune_related_adverse_events_endocrine_diabetes", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immune-Related Adverse Events for Endocrine Diabetes Mellitus",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmuneRelatedAdverseEventsEndocrineDiabetesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immune-Related Adverse Events grading",
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