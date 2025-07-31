"""
Harmless Acute Pancreatitis Score (HAPS) Router

Endpoint for calculating Harmless Acute Pancreatitis Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.haps import (
    HapsRequest,
    HapsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/haps",
    response_model=HapsResponse,
    summary="Calculate Harmless Acute Pancreatitis Score (HAPS)",
    description="Calculates the Harmless Acute Pancreatitis Score (HAPS) to identify patients with acute "
                "pancreatitis who will have a mild disease course and do not require intensive care unit admission. "
                "The score assesses three parameters at admission: presence of peritonitis, serum creatinine ≥2 mg/dL, "
                "and elevated hematocrit (≥43% for males, ≥39.6% for females). A score of 0 indicates 'harmless' "
                "acute pancreatitis with 97% specificity and 98% positive predictive value for non-severe disease. "
                "This rapid assessment tool can be completed within 30-60 minutes of admission and may help identify "
                "patients suitable for management on general wards or early discharge.",
    response_description="The calculated HAPS score with risk stratification and clinical management recommendations",
    operation_id="haps"
)
async def calculate_haps(request: HapsRequest):
    """
    Calculates Harmless Acute Pancreatitis Score (HAPS)
    
    The HAPS identifies patients with acute pancreatitis who will have a mild disease course
    and can be safely managed without ICU admission.
    
    Args:
        request: Parameters needed for HAPS calculation
        
    Returns:
        HapsResponse: Result with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("haps", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Harmless Acute Pancreatitis Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HapsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HAPS calculation",
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