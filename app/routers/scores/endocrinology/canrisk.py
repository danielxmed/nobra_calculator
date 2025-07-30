"""
Canadian Diabetes Risk Assessment Questionnaire (CANRISK) Router

Endpoint for calculating CANRISK score for diabetes risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.canrisk import (
    CanriskRequest,
    CanriskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/canrisk", response_model=CanriskResponse)
async def calculate_canrisk(request: CanriskRequest):
    """
    Calculates Canadian Diabetes Risk Assessment Questionnaire (CANRISK) score
    
    CANRISK screens for undiagnosed type 2 diabetes mellitus and prediabetes in 
    Canadian adults aged 18-74 years. It was developed by the Canadian Task Force 
    on Preventive Health Care in partnership with the Public Health Agency of Canada 
    and has been validated in Canada's multi-ethnic population.
    
    Key features:
    - Validated in 6,223 Canadians including 12% Aboriginal people
    - Accounts for Canada's multi-ethnic population
    - Maximum score: 86 points
    - Three risk categories: Low (<21), Moderate (21-32), High (≥33)
    
    Risk factors assessed:
    - Demographics: age, gender
    - Anthropometrics: BMI, waist circumference
    - Lifestyle: physical activity, diet
    - Medical history: blood pressure, blood sugar, large baby delivery
    - Family history: diabetes in first-degree relatives
    - Ethnicity: particularly high risk for South Asian and East Asian populations
    
    Clinical recommendations by risk level:
    - Low risk: Maintain healthy lifestyle, re-assess annually
    - Moderate risk: Discuss with healthcare provider, consider screening
    - High risk: Immediate screening with fasting glucose or HbA1c recommended
    
    Args:
        request: CANRISK parameters including demographics, lifestyle, and medical history
        
    Returns:
        CanriskResponse: Risk score with interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("canrisk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CANRISK score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CanriskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CANRISK",
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