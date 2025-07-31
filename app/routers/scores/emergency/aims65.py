"""
AIMS65 Score for Upper GI Bleeding Mortality Router

Endpoint for calculating AIMS65 Score for predicting in-hospital mortality.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.aims65 import (
    Aims65Request,
    Aims65Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/aims65",
    response_model=Aims65Response,
    summary="Calculate AIMS65 Score for Upper GI Bleeding Mortality",
    description="Predicts in-hospital mortality in patients with acute upper gastrointestinal bleeding using 5 simple clinical variables",
    response_description="The calculated aims65 with interpretation",
    operation_id="aims65"
)
async def calculate_aims65(request: Aims65Request):
    """
    Calculates AIMS65 Score for Upper GI Bleeding Mortality
    
    Predicts in-hospital mortality in patients with acute upper gastrointestinal 
    bleeding using 5 simple clinical variables that can be rapidly assessed in 
    the emergency department. The AIMS65 score is a validated, non-endoscopic 
    risk stratification tool superior to other scoring systems for mortality prediction.
    
    The score consists of 5 components (each worth 1 point):
    - A: Albumin <3.0 g/dL
    - I: INR >1.5  
    - M: Mental status altered
    - S: Systolic BP ≤90 mmHg
    - 65: Age ≥65 years
    
    Score Interpretation:
    - 0-1: Low risk (0.3-7.8% mortality) - Consider outpatient management
    - 2: Moderate risk (~20% mortality) - Inpatient monitoring, early endoscopy
    - 3-5: High risk (36-50% mortality) - Intensive monitoring, urgent endoscopy
    
    Key Advantages:
    - Simple and rapid calculation
    - No endoscopic findings required
    - Can be applied within 12 hours of admission
    - Superior mortality prediction compared to other scores
    - Helps guide triage and resource allocation decisions
    
    Clinical Applications:
    - Emergency department triage
    - Risk stratification for upper GI bleeding
    - Timing of endoscopic intervention
    - ICU admission decisions
    - Resource allocation
    
    Args:
        request: Parameters needed for AIMS65 calculation
        
    Returns:
        Aims65Response: AIMS65 score with clinical interpretation and risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("aims65", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AIMS65 Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Aims65Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AIMS65 Score",
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