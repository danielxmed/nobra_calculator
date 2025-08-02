"""
Immune-Related Adverse Events for GI Toxicity - Hepatitis Router

Endpoint for grading hepatitis severity in immune checkpoint inhibitor therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.immune_related_adverse_events_gi_hepatitis import (
    ImmuneRelatedAdverseEventsGiHepatitisRequest,
    ImmuneRelatedAdverseEventsGiHepatitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immune_related_adverse_events_gi_hepatitis",
    response_model=ImmuneRelatedAdverseEventsGiHepatitisResponse,
    summary="Grade Immune-Related Adverse Events for GI Hepatitis",
    description="Grades severity of hepatitis secondary to immune checkpoint inhibitor (ICPi) therapy "
                "based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria. "
                "This standardized grading system evaluates liver function tests including AST, ALT, and "
                "total bilirubin levels to determine the severity of immune-mediated hepatitis and guide "
                "clinical management decisions including ICPi therapy continuation, corticosteroid treatment, "
                "hepatology consultation needs, and monitoring for life-threatening complications. "
                "ICPi-induced hepatitis has an incidence of 5-10% in single-agent therapy but severe "
                "toxicity occurs in less than 2% of cases, requiring immediate recognition and appropriate "
                "management. Grade 1 (mild): Continue ICPi with close monitoring. Grade 2 (moderate): "
                "Hold ICPi, corticosteroids, hepatology consultation. Grade 3-4 (severe/life-threatening): "
                "Permanently discontinue ICPi, high-dose steroids, hospitalization, intensive care consultation "
                "for Grade 4. Essential for oncologists, hepatologists, and multidisciplinary teams managing "
                "patients on immunotherapy to prevent fulminant hepatic failure and death.",
    response_description="The calculated irAE grade with detailed management recommendations for hepatitis secondary to immune checkpoint inhibitor therapy",
    operation_id="immune_related_adverse_events_gi_hepatitis"
)
async def calculate_immune_related_adverse_events_gi_hepatitis(request: ImmuneRelatedAdverseEventsGiHepatitisRequest):
    """
    Calculates Immune-Related Adverse Events for GI Toxicity - Hepatitis
    
    Grades severity of hepatitis secondary to immune checkpoint inhibitor therapy
    and provides standardized management recommendations based on CTCAE v5.0 criteria.
    
    Args:
        request: Laboratory parameters including AST, ALT, bilirubin levels with ULN values and hepatic decompensation status
        
    Returns:
        ImmuneRelatedAdverseEventsGiHepatitisResponse: irAE grade with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immune_related_adverse_events_gi_hepatitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immune-Related Adverse Events for GI Hepatitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmuneRelatedAdverseEventsGiHepatitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immune-Related Adverse Events GI hepatitis grading",
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