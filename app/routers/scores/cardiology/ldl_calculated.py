"""
LDL Calculated Router

Endpoint for calculating LDL cholesterol using the Friedewald formula.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.ldl_calculated import (
    LdlCalculatedRequest,
    LdlCalculatedResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ldl_calculated",
    response_model=LdlCalculatedResponse,
    summary="Calculate LDL Cholesterol (Friedewald Formula)",
    description="Calculates LDL cholesterol using the Friedewald formula based on total cholesterol, HDL cholesterol, and triglycerides. "
                "This widely-used formula provides an estimated LDL cholesterol level when direct measurement is not available, "
                "helping healthcare providers assess cardiovascular risk and guide lipid management. The formula is: "
                "LDL = Total Cholesterol - HDL Cholesterol - (Triglycerides/5). Requires fasting triglyceride levels for accuracy. "
                "Inaccurate when triglycerides >400 mg/dL - direct LDL measurement recommended in these cases.",
    response_description="The calculated LDL cholesterol level with comprehensive clinical interpretation, accuracy assessment, and cardiovascular risk management recommendations",
    operation_id="ldl_calculated"
)
async def calculate_ldl_calculated(request: LdlCalculatedRequest):
    """
    Calculates LDL cholesterol using the Friedewald formula
    
    The Friedewald formula estimates LDL cholesterol from a standard lipid panel,
    providing a cost-effective method for cardiovascular risk assessment when 
    direct LDL measurement is not available.
    
    Args:
        request: Parameters including total cholesterol, HDL cholesterol, and triglycerides
        
    Returns:
        LdlCalculatedResponse: LDL cholesterol result with clinical interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ldl_calculated", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating LDL cholesterol using Friedewald formula",
                    "details": {"parameters": parameters}
                }
            )
        
        return LdlCalculatedResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for LDL cholesterol calculation",
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
                "message": "Internal error in LDL cholesterol calculation",
                "details": {"error": str(e)}
            }
        )