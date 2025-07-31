"""
Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk Calculator Router

Endpoint for calculating CP-AKI risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.cisplatin_aki import (
    CisplatinAkiRequest,
    CisplatinAkiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cisplatin_aki",
    response_model=CisplatinAkiResponse,
    summary="Calculate Cisplatin-Associated Acute Kidney Injury",
    description="Predicts the risk of acute kidney injury in patients treated with intravenous cisplatin. This calculator estimates the probability of moderate to severe AKI (≥2-fold rise in serum creatinine or need for kidney replacement therapy within 14 days of cisplatin administration).",
    response_description="The calculated cisplatin aki with interpretation",
    operation_id="cisplatin_aki"
)
async def calculate_cisplatin_aki(request: CisplatinAkiRequest):
    """
    Calculates Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk
    
    Predicts the risk of moderate to severe acute kidney injury (≥2-fold rise 
    in serum creatinine or need for kidney replacement therapy within 14 days) 
    in patients treated with intravenous cisplatin. This tool helps identify 
    high-risk patients who may benefit from closer monitoring or alternative 
    treatment strategies.
    
    Args:
        request: Parameters needed for calculation including demographics,
                comorbidities, cisplatin dose, and laboratory values
        
    Returns:
        CisplatinAkiResponse: Risk percentage with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cisplatin_aki", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CP-AKI risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return CisplatinAkiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CP-AKI risk calculator",
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