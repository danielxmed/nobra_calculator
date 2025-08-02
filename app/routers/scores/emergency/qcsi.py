"""
Quick COVID-19 Severity Index (qCSI) Router

Endpoint for calculating qCSI.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.qcsi import (
    QcsiRequest,
    QcsiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/qcsi",
    response_model=QcsiResponse,
    summary="Calculate Quick COVID-19 Severity Index (qCSI)",
    description="Predicts 24-hour risk of critical respiratory failure in emergency department "
                "admitted COVID-19 patients using three simple bedside measurements: respiratory "
                "rate, lowest oxygen saturation in first 4 hours, and current oxygen flow rate. "
                "This validated prognostic tool, developed during the COVID-19 pandemic, enables "
                "rapid risk stratification and appropriate resource allocation for hospitalized "
                "COVID-19 patients. The qCSI score ranges from 0-12 points and stratifies patients "
                "into three risk categories: Low Risk (≤3 points, <5% respiratory failure risk), "
                "Intermediate Risk (4-6 points, moderate risk), and High Risk (≥7 points, high "
                "risk). Derived from a large cohort of 1,792 COVID-19 patients with 35% "
                "experiencing respiratory failure, the qCSI demonstrated sensitivity of 79% and "
                "specificity of 78% for predicting respiratory decompensation. The tool showed "
                "superior performance (AUC 0.761) compared to CURB-65 for ICU admission prediction. "
                "Low-risk patients may be suitable for standard ward monitoring, while intermediate "
                "and high-risk patients require enhanced monitoring, frequent assessments, and "
                "preparation for advanced respiratory support including high-flow oxygen, "
                "noninvasive ventilation, or mechanical ventilation. The qCSI enables proactive "
                "clinical decision-making, optimal resource utilization, and improved patient "
                "outcomes through early identification of patients at risk for respiratory "
                "deterioration.",
    response_description="The calculated qCSI score with respiratory failure risk category and comprehensive COVID-19 management recommendations",
    operation_id="qcsi"
)
async def calculate_qcsi(request: QcsiRequest):
    """
    Calculates Quick COVID-19 Severity Index (qCSI)
    
    This validated prognostic tool predicts 24-hour risk of critical respiratory failure
    in COVID-19 patients to guide monitoring intensity and resource allocation.
    
    Args:
        request: Clinical parameters including respiratory rate, lowest oxygen saturation
                in first 4 hours, and current oxygen flow rate for qCSI calculation
        
    Returns:
        QcsiResponse: Result with respiratory failure risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("qcsi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating qCSI",
                    "details": {"parameters": parameters}
                }
            )
        
        return QcsiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for qCSI",
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