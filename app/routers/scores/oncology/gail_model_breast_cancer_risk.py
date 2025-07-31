"""
Gail Model for Breast Cancer Risk Router

Endpoint for calculating Gail Model breast cancer risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.gail_model_breast_cancer_risk import (
    GailModelBreastCancerRiskRequest,
    GailModelBreastCancerRiskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gail_model_breast_cancer_risk",
    response_model=GailModelBreastCancerRiskResponse,
    summary="Calculate Gail Model for Breast Cancer Risk",
    description="Estimates risk for breast cancer based on demographic and clinical data. The Gail Model calculates a woman's absolute risk of developing invasive breast cancer over the next 5 years and up to age 90 (lifetime risk) using personal medical and reproductive history and family history of breast cancer among first-degree relatives.",
    response_description="The calculated gail model breast cancer risk with interpretation",
    operation_id="calculate_gail_model_breast_cancer_risk"
)
async def calculate_gail_model_breast_cancer_risk(request: GailModelBreastCancerRiskRequest):
    """
    Calculates Gail Model for Breast Cancer Risk
    
    Estimates risk for breast cancer based on demographic and clinical data. The Gail Model 
    calculates a woman's absolute risk of developing invasive breast cancer over the next 
    5 years using personal medical and reproductive history and family history of breast 
    cancer among first-degree relatives.
    
    The model uses 7 key risk factors: age, race/ethnicity, age at menarche, age at first 
    live birth, family history, breast biopsy history, and atypical hyperplasia. A 5-year 
    risk ≥1.67% meets the FDA threshold for chemoprevention consideration.
    
    Valid for women aged 35-85 years without personal history of breast cancer. The model 
    has been validated for White, African-American, Hispanic, and Asian/Pacific Islander 
    women in the United States.
    
    Args:
        request: Parameters needed for Gail Model calculation including demographic data,
                reproductive history, family history, and breast biopsy history
        
    Returns:
        GailModelBreastCancerRiskResponse: Result with 5-year breast cancer risk and 
                                         clinical interpretation including chemoprevention 
                                         and screening recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gail_model_breast_cancer_risk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Gail Model for Breast Cancer Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return GailModelBreastCancerRiskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Gail Model for Breast Cancer Risk",
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