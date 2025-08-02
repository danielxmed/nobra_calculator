"""
International Ovarian Tumor Analysis (IOTA) Simple Rules Risk Assessment Router

Endpoint for calculating IOTA Simple Rules Risk Assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gynecology.iota_simple_rules import (
    IotaSimpleRulesRequest,
    IotaSimpleRulesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/iota_simple_rules",
    response_model=IotaSimpleRulesResponse,
    summary="Calculate IOTA Simple Rules Risk Assessment for Ovarian Masses",
    description="Calculates the International Ovarian Tumor Analysis (IOTA) Simple Rules risk assessment for predicting malignancy "
                "in adnexal masses using ultrasonographic features. This validated clinical prediction tool uses 10 ultrasound "
                "features (5 benign B-rules and 5 malignant M-rules) to classify ovarian masses as benign, malignant, or inconclusive. "
                "The system achieves 86.8% sensitivity, 95.6% specificity, and 92.3% accuracy, successfully classifying 76-80% of "
                "adnexal masses. Benign features include: unilocular cyst (B1), solid components <7mm (B2), acoustic shadows (B3), "
                "smooth multilocular tumor <100mm (B4), and no blood flow (B5). Malignant features include: irregular solid tumor (M1), "
                "ascites (M2), ≥4 papillary structures (M3), irregular multilocular solid tumor ≥100mm (M4), and very strong blood flow (M5). "
                "Classification logic: B-features only = Benign, M-features only = Malignant, both or neither = Inconclusive. This tool "
                "is designed for preoperative evaluation of persistent adnexal masses in women considered for surgery, excluding classical "
                "masses with pathognomonic features (corpus luteum, endometrioma, dermoid cyst). Requires adequate ultrasound training "
                "and quality equipment for optimal performance.",
    response_description="The calculated IOTA Simple Rules classification with risk assessment and management recommendations",
    operation_id="iota_simple_rules"
)
async def calculate_iota_simple_rules(request: IotaSimpleRulesRequest):
    """
    Calculates IOTA Simple Rules risk assessment for ovarian mass malignancy
    
    Predicts malignancy risk in adnexal masses using 10 standardized ultrasound features.
    Helps guide clinical decision-making for surgical planning and oncology referrals.
    
    Args:
        request: Ultrasound features for IOTA Simple Rules assessment (10 B and M features)
        
    Returns:
        IotaSimpleRulesResponse: IOTA classification with risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("iota_simple_rules", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IOTA Simple Rules Risk Assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return IotaSimpleRulesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IOTA Simple Rules Risk Assessment",
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