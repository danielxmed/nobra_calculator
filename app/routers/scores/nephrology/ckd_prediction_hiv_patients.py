"""
CKD Prediction in HIV+ Patients Router

Endpoint for calculating CKD prediction risk in HIV-positive patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.ckd_prediction_hiv_patients import (
    CkdPredictionHivPatientsRequest,
    CkdPredictionHivPatientsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ckd_prediction_hiv_patients", response_model=CkdPredictionHivPatientsResponse)
async def calculate_ckd_prediction_hiv_patients(request: CkdPredictionHivPatientsRequest):
    """
    Calculates CKD Prediction Risk in HIV+ Patients
    
    This calculator estimates the 5-year probability of developing chronic kidney disease 
    (CKD) in HIV-infected patients based on a validated risk score developed from a 
    prospective cohort study of HIV-positive male veterans. The tool is particularly 
    valuable for guiding clinical decision-making regarding tenofovir disoproxil 
    fumarate (TDF) use.
    
    The calculator incorporates seven key risk factors:
    - Age (strongest predictor: 0-6 points based on decade)
    - Glucose elevation >140 mg/dL (diabetes/pre-diabetes risk: 2 points)
    - Systolic blood pressure >140 mmHg (vascular damage: 1 point)
    - Hypertension diagnosis (strongest traditional risk factor: 2 points)
    - Triglycerides >200 mg/dL (metabolic dysfunction: 1 point)
    - Proteinuria (existing kidney damage: 2 points)
    - CD4+ count <200 cells/µL (HIV disease severity: 1 point)
    
    Risk Assessment Categories:
    - Low Risk (<5%): Tenofovir reasonable with routine monitoring
    - Moderate Risk (5-14%): Careful consideration of alternatives
    - High Risk (≥15%): Strong consideration for tenofovir alternatives
    
    Clinical Applications:
    - Personalized risk assessment for tenofovir safety
    - Guide antiretroviral regimen selection
    - Determine kidney function monitoring frequency
    - Support shared decision-making with patients
    - Identify candidates for nephrology consultation
    
    Number Needed to Harm (NNH):
    The calculator provides NNH estimates for tenofovir use, ranging from 108 for 
    low-risk patients to 20 for highest-risk patients, helping quantify absolute 
    risk increases.
    
    Args:
        request: CKD risk assessment parameters including age, traditional risk factors,
                HIV-specific factors, and tenofovir use status
        
    Returns:
        CkdPredictionHivPatientsResponse: Comprehensive risk assessment with 5-year 
        CKD probability, risk stratification, treatment recommendations, and detailed 
        clinical guidance for HIV patient management
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ckd_prediction_hiv_patients", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CKD Prediction in HIV+ Patients",
                    "details": {"parameters": parameters}
                }
            )
        
        return CkdPredictionHivPatientsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CKD Prediction in HIV+ Patients",
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
                "message": "Internal error in CKD prediction calculation",
                "details": {"error": str(e)}
            }
        )