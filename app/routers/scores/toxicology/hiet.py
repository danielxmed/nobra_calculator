"""
High-dose Insulin Euglycemia Therapy (HIET) Router

Endpoint for calculating HIET dosing protocol.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.toxicology.hiet import (
    HietRequest,
    HietResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hiet",
    response_model=HietResponse,
    summary="Calculate High-dose Insulin Euglycemia Therapy (HIET) Protocol",
    description="Calculates insulin and dextrose dosing for High-dose Insulin Euglycemia Therapy "
                "in the treatment of calcium channel blocker or beta blocker overdose. HIET is an "
                "advanced treatment modality that overcomes the metabolic dysfunction caused by these "
                "overdoses, improving myocardial contractility and cellular metabolism. The calculator "
                "provides weight-based dosing for insulin bolus (1 unit/kg), insulin infusion "
                "(0.5-1 unit/kg/hr), and dextrose requirements to maintain euglycemia. This therapy "
                "requires intensive monitoring of glucose and potassium levels, and is typically "
                "continued for 1-2 days until hemodynamic improvement is achieved.",
    response_description="Complete HIET dosing protocol with insulin and dextrose calculations and monitoring guidance",
    operation_id="hiet"
)
async def calculate_hiet(request: HietRequest):
    """
    Calculates High-dose Insulin Euglycemia Therapy (HIET) dosing protocol
    
    HIET is used for severe calcium channel blocker and beta blocker overdoses
    that cause cardiogenic shock. It provides metabolic support to overcome
    toxin-induced myocardial dysfunction.
    
    Args:
        request: Patient weight and initial infusion rate selection
        
    Returns:
        HietResponse: Complete dosing protocol with monitoring guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hiet", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HIET protocol",
                    "details": {"parameters": parameters}
                }
            )
        
        return HietResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HIET calculation",
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
                "message": "Internal error in HIET calculation",
                "details": {"error": str(e)}
            }
        )