"""
ISTH Criteria for Disseminated Intravascular Coagulation (DIC) Router

Endpoint for calculating ISTH DIC criteria score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.isth_dic_criteria import (
    IsthDicCriteriaRequest,
    IsthDicCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/isth_dic_criteria",
    response_model=IsthDicCriteriaResponse,
    summary="Calculate ISTH DIC Criteria Score",
    description="Calculates the ISTH (International Society on Thrombosis and Haemostasis) criteria score for diagnosing overt disseminated intravascular coagulation (DIC). This validated scoring system uses four readily available laboratory parameters (platelet count, fibrin-related markers, PT prolongation, and fibrinogen level) to standardize DIC diagnosis. The score has 91-93% sensitivity and 97-98% specificity for overt DIC. Use only in patients with clinical suspicion for DIC in appropriate settings such as sepsis, malignancy, obstetric complications, or trauma.",
    response_description="The calculated ISTH DIC score with clinical interpretation and management recommendations based on overt DIC likelihood",
    operation_id="isth_dic_criteria"
)
async def calculate_isth_dic_criteria(request: IsthDicCriteriaRequest):
    """
    Calculates ISTH Criteria for Disseminated Intravascular Coagulation (DIC)
    
    Diagnoses overt disseminated intravascular coagulation using the International Society
    on Thrombosis and Haemostasis scoring system. This evidence-based tool provides
    standardized DIC diagnosis using routine laboratory tests with excellent diagnostic
    performance characteristics.
    
    Args:
        request: Laboratory parameters including platelet count, fibrin markers, PT prolongation, and fibrinogen level
        
    Returns:
        IsthDicCriteriaResponse: DIC score with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("isth_dic_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ISTH DIC Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return IsthDicCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ISTH DIC Criteria",
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