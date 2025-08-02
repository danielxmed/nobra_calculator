"""
Milan Criteria for Liver Transplantation Router

Endpoint for calculating Milan criteria eligibility for liver transplantation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.milan_criteria import (
    MilanCriteriaRequest,
    MilanCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/milan_criteria",
    response_model=MilanCriteriaResponse,
    summary="Calculate Milan Criteria for Liver Transplantation",
    description="Assesses suitability of patients with hepatocellular carcinoma (HCC) and cirrhosis for liver transplantation "
                "based on tumor burden and absence of extrahepatic disease or major vascular invasion. The Milan criteria "
                "define transplant eligibility as: single tumor ≤5 cm OR 2-3 tumors each ≤3 cm, with no extrahepatic "
                "involvement and no major vessel involvement. Patients meeting criteria have excellent post-transplant "
                "outcomes with 4-year survival rates around 75%. This validated tool is recommended by AASLD guidelines "
                "and determines MELD exception eligibility after 6-month waiting period.",
    response_description="Milan criteria eligibility determination with transplant recommendations and management guidance",
    operation_id="milan_criteria"
)
async def calculate_milan_criteria(request: MilanCriteriaRequest):
    """
    Calculates Milan Criteria for Liver Transplantation
    
    Determines transplant eligibility for patients with hepatocellular carcinoma
    and cirrhosis based on established criteria that predict excellent outcomes.
    
    Args:
        request: Tumor characteristics and staging parameters
        
    Returns:
        MilanCriteriaResponse: Eligibility determination with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("milan_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Milan Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return MilanCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Milan Criteria",
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