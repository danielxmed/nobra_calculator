"""
Modified Response Evaluation Criteria in Solid Tumors (mRECIST) Router

Endpoint for calculating mRECIST assessment for hepatocellular carcinoma treatment response.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.modified_recist import (
    ModifiedRecistRequest,
    ModifiedRecistResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_recist",
    response_model=ModifiedRecistResponse,
    summary="Calculate Modified Response Evaluation Criteria in Solid Tumors (mRECIST)",
    description="Calculates the Modified Response Evaluation Criteria in Solid Tumors (mRECIST) for "
                "assessing treatment response in hepatocellular carcinoma (HCC) patients. This validated "
                "assessment tool evaluates viable tumor burden based on arterial phase enhancement on "
                "contrast-enhanced CT or MRI imaging. mRECIST is specifically designed for HCC and is "
                "superior to standard RECIST 1.1 for evaluating response to targeted therapies, "
                "locoregional treatments, and immunotherapies. The assessment categorizes response as "
                "Complete Response (disappearance of arterial enhancement), Partial Response (≥30% "
                "decrease in viable tumor), Stable Disease (neither PR nor PD criteria), or Progressive "
                "Disease (≥20% increase or new lesions). Results correlate with overall survival and "
                "guide treatment decisions in clinical practice and research trials.",
    response_description="The calculated mRECIST response category with clinical interpretation and treatment recommendations",
    operation_id="modified_recist"
)
async def calculate_modified_recist(request: ModifiedRecistRequest):
    """
    Calculates Modified Response Evaluation Criteria in Solid Tumors (mRECIST) for HCC treatment response assessment
    
    Provides standardized assessment of treatment response in hepatocellular carcinoma 
    based on viable tumor enhancement patterns. The mRECIST criteria account for tumor 
    necrosis induced by treatment and focus on metabolically active tumor tissue.
    
    Args:
        request: Parameters needed for mRECIST calculation including baseline and current 
                tumor measurements and enhancement status
        
    Returns:
        ModifiedRecistResponse: mRECIST response category with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_recist", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Response Evaluation Criteria in Solid Tumors (mRECIST)",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedRecistResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Response Evaluation Criteria in Solid Tumors (mRECIST)",
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