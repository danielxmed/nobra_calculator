"""
Oxygenation Index Router

Endpoint for calculating Oxygenation Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.oxygenation_index import (
    OxygenationIndexRequest,
    OxygenationIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/oxygenation_index",
    response_model=OxygenationIndexResponse,
    summary="Calculate Oxygenation Index",
    description="Calculates the Oxygenation Index, a validated tool for assessing the severity of "
                "respiratory failure in pediatric patients and determining the need for extracorporeal "
                "membrane oxygenation (ECMO). The index is calculated as (FiO₂ × Mean Airway Pressure) ÷ PaO₂ "
                "and provides critical guidance for treatment decisions in acute lung injury and ARDS. "
                "Values <25 indicate good outcome with conventional therapy, values 25-40 represent high "
                "risk with >40% mortality requiring optimization, and values ≥40 indicate severe failure "
                "with strong consideration for ECMO. This tool was developed by Dr. Robert Bartlett and "
                "has been extensively validated in pediatric critical care settings for outcome prediction "
                "and ECMO decision-making.",
    response_description="The calculated Oxygenation Index with detailed risk stratification and ECMO guidance",
    operation_id="oxygenation_index"
)
async def calculate_oxygenation_index(request: OxygenationIndexRequest):
    """
    Calculates Oxygenation Index
    
    This validated tool helps assess respiratory failure severity and guides
    ECMO decision-making in pediatric patients with acute lung injury.
    
    Args:
        request: FiO2, mean airway pressure, and PaO2 values
        
    Returns:
        OxygenationIndexResponse: Result with ECMO guidance and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("oxygenation_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Oxygenation Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return OxygenationIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Oxygenation Index",
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