"""
International Diabetes Federation-Diabetes and Ramadan Alliance (IDF-DAR) Fasting Risk Assessment Router

Endpoint for IDF-DAR fasting risk assessment calculation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.idf_dar_fasting_risk_assessment import (
    IdfDarFastingRiskAssessmentRequest,
    IdfDarFastingRiskAssessmentResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/idf_dar_fasting_risk_assessment",
    response_model=IdfDarFastingRiskAssessmentResponse,
    summary="Calculate IDF-DAR Fasting Risk Assessment",
    description="Stratifies risk of fasting during Ramadan in diabetic patients using the validated International Diabetes Federation-Diabetes and Ramadan Alliance (IDF-DAR) tool published in 2021. This evidence-based assessment evaluates 14 key risk factors across multiple domains including diabetes type and duration, hypoglycemia history, glycemic control, treatment regimen, diabetic complications, and social factors such as pregnancy status, physical activity, and previous fasting experience. The tool provides systematic risk stratification into three categories: low risk (0-3 points, fasting probably safe), moderate risk (3.5-6 points, fasting safety uncertain), and high risk (>6 points, fasting probably unsafe). This assessment has been validated across multiple populations and enables healthcare providers to make informed, evidence-based recommendations about the safety of Ramadan fasting for individual diabetic patients. The tool facilitates personalized patient counseling, appropriate monitoring strategies, medication adjustments, and emergency preparedness planning based on individual risk profiles. This calculator is particularly valuable for endocrinologists, family physicians, and diabetes educators managing diabetic patients during Ramadan.",
    response_description="The calculated IDF-DAR risk score with risk category classification and clinical management recommendations",
    operation_id="idf_dar_fasting_risk_assessment"
)
async def calculate_idf_dar_fasting_risk_assessment(request: IdfDarFastingRiskAssessmentRequest):
    """
    Calculates IDF-DAR Fasting Risk Assessment
    
    Systematically evaluates 14 risk factors to determine the safety of Ramadan fasting 
    in diabetic patients according to international consensus guidelines.
    
    Args:
        request: Clinical parameters for IDF-DAR risk assessment (14 risk factors)
        
    Returns:
        IdfDarFastingRiskAssessmentResponse: Risk score with category and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("idf_dar_fasting_risk_assessment", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IDF-DAR Fasting Risk Assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return IdfDarFastingRiskAssessmentResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IDF-DAR Fasting Risk Assessment",
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
                "message": "Internal error in risk assessment calculation",
                "details": {"error": str(e)}
            }
        )