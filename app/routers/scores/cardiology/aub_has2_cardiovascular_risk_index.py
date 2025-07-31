"""
American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index Router

Endpoint for calculating AUB-HAS2 cardiovascular risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.aub_has2_cardiovascular_risk_index import (
    AubHas2CardiovascularRiskIndexRequest,
    AubHas2CardiovascularRiskIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/aub_has2_cardiovascular_risk_index",
    response_model=AubHas2CardiovascularRiskIndexResponse,
    summary="Calculate American University of Beirut (AUB)-H...",
    description="Stratifies cardiovascular risk of patients undergoing noncardiac surgery using 6 easily obtainable clinical variables with superior discriminatory power compared to other risk indices.",
    response_description="The calculated aub has2 cardiovascular risk index with interpretation",
    operation_id="calculate_aub_has2_cardiovascular_risk_index"
)
async def calculate_aub_has2_cardiovascular_risk_index(request: AubHas2CardiovascularRiskIndexRequest):
    """
    Calculates American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index
    
    The AUB-HAS2 index is a simple, powerful preoperative risk stratification tool 
    that uses 6 easily obtainable clinical variables to predict major cardiovascular 
    events (death, myocardial infarction, or stroke) within 30 days after noncardiac 
    surgery. It demonstrates superior discriminatory power compared to other established 
    risk indices.
    
    The score uses the HAS2 framework:
    - **H**eart disease history (1 point)
    - **A**ge ≥75 years (1 point) 
    - **S**ymptoms of angina or dyspnea (1 point)
    - **2** additional factors: anemia (Hgb <12 mg/dL, 1 point) and surgery type 
      (vascular surgery 1 point, emergency surgery 1 point)
    
    Risk stratification:
    - Low Risk (0-1 points): <1% event rate, routine care
    - Intermediate Risk (2-3 points): 5-11% event rate, enhanced monitoring
    - High Risk (≥4 points): >15% event rate, intensive management
    
    Args:
        request: Clinical parameters including cardiac history, age, symptoms, 
                anemia status, and surgery characteristics
        
    Returns:
        AubHas2CardiovascularRiskIndexResponse: Risk score with clinical interpretation 
        and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("aub_has2_cardiovascular_risk_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return AubHas2CardiovascularRiskIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index",
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