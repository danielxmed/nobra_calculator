"""
ISTH-SCC Bleeding Assessment Tool Router

Endpoint for calculating ISTH-SCC bleeding assessment tool score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.isth_scc_bleeding_assessment_tool import (
    IsthSccBleedingAssessmentToolRequest,
    IsthSccBleedingAssessmentToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/isth_scc_bleeding_assessment_tool",
    response_model=IsthSccBleedingAssessmentToolResponse,
    summary="Calculate ISTH-SCC Bleeding Assessment Tool Score",
    description="Calculates the ISTH-SCC (International Society on Thrombosis and Haemostasis Scientific and Standardization Committee) Bleeding Assessment Tool score for screening patients with suspected inherited bleeding disorders. This standardized 14-domain questionnaire evaluates bleeding symptoms across multiple body systems with demographic-specific interpretation thresholds. The tool provides evidence-based screening for von Willebrand disease, platelet function disorders, and other inherited bleeding conditions, helping identify patients who require comprehensive hematologic evaluation.",
    response_description="The calculated bleeding assessment score with demographic-specific interpretation and recommendations for further evaluation",
    operation_id="isth_scc_bleeding_assessment_tool"
)
async def calculate_isth_scc_bleeding_assessment_tool(request: IsthSccBleedingAssessmentToolRequest):
    """
    Calculates ISTH-SCC Bleeding Assessment Tool Score
    
    Assesses bleeding symptoms across 14 domains to screen for inherited bleeding disorders.
    This standardized tool was developed by the International Society on Thrombosis and 
    Haemostasis to provide consistent evaluation of bleeding symptoms with validated 
    thresholds for different demographic groups.
    
    Args:
        request: Bleeding assessment parameters including 14 bleeding domains, age group, and gender
        
    Returns:
        IsthSccBleedingAssessmentToolResponse: Bleeding score with demographic-specific interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("isth_scc_bleeding_assessment_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ISTH-SCC Bleeding Assessment Tool",
                    "details": {"parameters": parameters}
                }
            )
        
        return IsthSccBleedingAssessmentToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ISTH-SCC Bleeding Assessment Tool",
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