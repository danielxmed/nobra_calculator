"""
qSOFA (Quick SOFA) Score for Sepsis Router

Endpoint for calculating qSOFA Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.qsofa_score import (
    QsofaScoreRequest,
    QsofaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/qsofa_score",
    response_model=QsofaScoreResponse,
    summary="Calculate qSOFA (Quick SOFA) Score for Sepsis",
    description="Rapidly identifies high-risk patients for in-hospital mortality with suspected "
                "infection outside the ICU using three simple bedside criteria: respiratory rate "
                "≥22 breaths/min, altered mental status (GCS <15), and systolic blood pressure "
                "≤100 mmHg. This validated clinical decision tool, introduced by the Sepsis-3 "
                "task force in 2016, provides immediate risk stratification without requiring "
                "laboratory tests. The qSOFA score ranges from 0-3 points, with scores ≥2 "
                "indicating a 3- to 14-fold increase in in-hospital mortality risk and triggering "
                "immediate sepsis management protocols. Derived and validated in over 148,000 "
                "patients with suspected infection, the qSOFA demonstrates superior predictive "
                "validity for mortality outside ICU settings compared to traditional criteria. "
                "Low-risk patients (qSOFA <2) continue standard infection management with close "
                "monitoring, while high-risk patients (qSOFA ≥2) require immediate implementation "
                "of sepsis bundles including blood cultures, broad-spectrum antibiotics within "
                "1 hour, aggressive fluid resuscitation, and consideration for ICU admission. "
                "The tool enables rapid sepsis recognition and timely intervention, supporting "
                "evidence-based clinical decision-making to improve patient outcomes.",
    response_description="The calculated qSOFA score with mortality risk category and comprehensive sepsis management recommendations",
    operation_id="qsofa_score"
)
async def calculate_qsofa_score(request: QsofaScoreRequest):
    """
    Calculates qSOFA (Quick SOFA) Score for Sepsis
    
    This rapid bedside assessment tool identifies patients with suspected infection
    at higher risk for poor outcomes and guides sepsis management decisions.
    
    Args:
        request: Clinical criteria including respiratory rate ≥22/min, altered mental 
                status (GCS <15), and systolic BP ≤100 mmHg for qSOFA calculation
        
    Returns:
        QsofaScoreResponse: Result with mortality risk category and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("qsofa_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating qSOFA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return QsofaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for qSOFA Score",
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