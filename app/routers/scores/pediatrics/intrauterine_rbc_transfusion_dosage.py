"""
Intrauterine RBC Transfusion Dosage Router

Endpoint for calculating intrauterine RBC transfusion dosage.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.intrauterine_rbc_transfusion_dosage import (
    IntrauterineRbcTransfusionDosageRequest,
    IntrauterineRbcTransfusionDosageResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/intrauterine_rbc_transfusion_dosage",
    response_model=IntrauterineRbcTransfusionDosageResponse,
    summary="Calculate Intrauterine RBC Transfusion Dosage",
    description="Calculates the volume of donor RBCs needed for intrauterine transfusion (IUT) in cases of fetal anemia, primarily hemolytic disease of the fetus and newborn (HDFN). This evidence-based calculator uses fetal weight, current and target hematocrit levels, and donor RBC characteristics to determine precise transfusion volumes. The calculation minimizes risks of over- or under-transfusion while optimizing fetal outcomes. Used by maternal-fetal medicine specialists for managing severe fetal anemia requiring intrauterine intervention.",
    response_description="The calculated transfusion volume in mL with clinical interpretation and procedural recommendations based on volume category",
    operation_id="intrauterine_rbc_transfusion_dosage"
)
async def calculate_intrauterine_rbc_transfusion_dosage(request: IntrauterineRbcTransfusionDosageRequest):
    """
    Calculates Intrauterine RBC Transfusion Dosage
    
    Estimates the volume of donor RBCs needed for intrauterine transfusion in fetal anemia cases.
    Used primarily for severe fetal anemia in hemolytic disease of the fetus and newborn when 
    maternal RBC alloantibodies threaten fetal health.
    
    Args:
        request: Parameters including fetal weight, initial hematocrit, goal hematocrit, and donor RBC hematocrit
        
    Returns:
        IntrauterineRbcTransfusionDosageResponse: Transfusion volume with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("intrauterine_rbc_transfusion_dosage", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Intrauterine RBC Transfusion Dosage",
                    "details": {"parameters": parameters}
                }
            )
        
        return IntrauterineRbcTransfusionDosageResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Intrauterine RBC Transfusion Dosage",
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