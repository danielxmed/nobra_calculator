"""
MACOCHA Score Router

Endpoint for calculating MACOCHA Score to predict difficult intubation in ICU patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.macocha_score import (
    MacochaScoreRequest,
    MacochaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/macocha_score",
    response_model=MacochaScoreResponse,
    summary="Calculate MACOCHA Score",
    description="Calculates the MACOCHA Score to predict difficult intubation in ICU patients. "
                "This validated clinical tool uses seven factors across patient-related (Mallampati score, "
                "obstructive sleep apnea, cervical mobility, mouth opening), pathology-related (coma, severe hypoxemia), "
                "and operator-related (non-anesthesiologist) domains. The score helps identify patients at risk for "
                "difficult intubation, allowing for appropriate preparation with equipment and personnel. It has excellent "
                "negative predictive value (98%) for ruling out difficult intubation and guides airway management strategy.",
    response_description="The calculated MACOCHA score with risk category and comprehensive intubation preparation recommendations",
    operation_id="macocha_score"
)
async def calculate_macocha_score(request: MacochaScoreRequest):
    """
    Calculates MACOCHA Score for difficult intubation prediction in ICU patients
    
    The MACOCHA Score identifies patients at risk for difficult intubation using seven
    validated clinical factors. It was developed and validated in multicenter studies
    involving over 1,000 ICU intubations from 42 centers.
    
    Clinical Applications:
    - Pre-intubation risk stratification for all ICU patients
    - Equipment preparation and resource allocation planning
    - Personnel assignment and backup planning
    - Quality improvement and patient safety protocols
    - Decision support for intubation approach selection
    
    Risk Categories:
    - Low Risk (0-2 points): <10% difficult intubation probability, standard preparation
    - Intermediate Risk (3-5 points): 10-30% probability, enhanced preparation needed
    - High Risk (6-12 points): >30% probability, comprehensive difficult airway preparation
    
    Performance Characteristics:
    - Area under curve: 0.89 (development), 0.86 (validation)
    - Sensitivity: 73% for difficult intubation identification
    - Specificity: 89% for excluding difficult intubation
    - Negative predictive value: 98% (excellent for ruling out)
    - Positive predictive value: 36%
    
    Clinical Impact:
    Difficult intubation is associated with 51% vs 36% severe life-threatening
    complications including severe hypoxia, cardiovascular collapse, cardiac arrest,
    and death. Early identification allows appropriate preparation to minimize risks.
    
    Args:
        request: MACOCHA Score calculation parameters including patient, pathology, and operator factors
        
    Returns:
        MacochaScoreResponse: MACOCHA score with risk category and preparation recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("macocha_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MACOCHA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MacochaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MACOCHA Score",
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
                "message": "Internal error in MACOCHA Score calculation",
                "details": {"error": str(e)}
            }
        )