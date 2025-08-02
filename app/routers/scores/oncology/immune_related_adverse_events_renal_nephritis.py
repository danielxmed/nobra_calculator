"""
Immune-Related Adverse Events for Renal Toxicities - Nephritis Router

Endpoint for calculating immune-related nephritis grading based on CTCAE Version 5.0 criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.immune_related_adverse_events_renal_nephritis import (
    ImmuneRelatedAdverseEventsRenalNephritisRequest,
    ImmuneRelatedAdverseEventsRenalNephritisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immune_related_adverse_events_renal_nephritis",
    response_model=ImmuneRelatedAdverseEventsRenalNephritisResponse,
    summary="Calculate Immune-Related Adverse Events for Renal Toxicities - Nephritis",
    description="Grades severity of nephritis secondary to immune checkpoint inhibitor (ICPi) therapy based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria. This standardized grading system evaluates serum creatinine levels, renal function changes, and clinical symptoms to determine the severity of immune-mediated nephritis and guide clinical management decisions including ICPi therapy continuation, corticosteroid treatment, nephrology consultation needs, and monitoring for life-threatening renal complications. ICPi-induced nephritis has an incidence of 1-2% in single-agent therapy and 4.5% in combination therapy, with median onset at 14 weeks. The calculator provides evidence-based management recommendations essential for oncologists, nephrologists, and multidisciplinary teams managing patients on immunotherapy.",
    response_description="The calculated CTCAE grade for immune-related nephritis with severity classification and clinical management recommendations",
    operation_id="immune_related_adverse_events_renal_nephritis"
)
async def calculate_immune_related_adverse_events_renal_nephritis(request: ImmuneRelatedAdverseEventsRenalNephritisRequest):
    """
    Calculates Immune-Related Adverse Events for Renal Toxicities - Nephritis
    
    Grades severity of nephritis secondary to immune checkpoint inhibitor therapy
    using CTCAE Version 5.0 criteria. Evaluates creatinine fold increase over baseline
    along with clinical symptoms to determine grade (1-4) and provide evidence-based
    management recommendations for ICPi therapy decisions.
    
    Args:
        request: Parameters including baseline and current creatinine, proteinuria,
                hematuria, clinical symptoms, fluid retention, and dialysis requirement
        
    Returns:
        ImmuneRelatedAdverseEventsRenalNephritisResponse: CTCAE grade with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immune_related_adverse_events_renal_nephritis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immune-Related Adverse Events for Renal Toxicities - Nephritis",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmuneRelatedAdverseEventsRenalNephritisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immune-Related Adverse Events for Renal Toxicities - Nephritis",
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