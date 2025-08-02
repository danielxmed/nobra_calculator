"""
LACE Index for Readmission Router

Endpoint for calculating LACE Index readmission risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.lace_index_readmission import (
    LaceIndexReadmissionRequest,
    LaceIndexReadmissionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lace_index_readmission",
    response_model=LaceIndexReadmissionResponse,
    summary="Calculate LACE Index for Readmission",
    description="Calculates the LACE Index to predict 30-day readmission or death risk in medical and "
                "surgical ward patients. This validated clinical prediction tool uses four key factors: "
                "Length of stay, Acuity of admission, Comorbidities (Charlson index), and Emergency "
                "department visits. The index helps healthcare teams identify high-risk patients who "
                "would benefit from enhanced discharge planning, care coordination, and early follow-up "
                "interventions to reduce preventable readmissions and improve patient outcomes.",
    response_description="The calculated LACE Index score with risk stratification and specific clinical recommendations for discharge planning and care coordination",
    operation_id="lace_index_readmission"
)
async def calculate_lace_index_readmission(request: LaceIndexReadmissionRequest):
    """
    Calculates LACE Index for Readmission Risk Assessment
    
    The LACE Index is a validated tool that predicts 30-day readmission or death 
    risk using readily available administrative and clinical data. It combines 
    four evidence-based predictors to stratify patients into risk categories 
    that guide targeted interventions.
    
    Clinical Applications:
    - Discharge planning and resource allocation
    - Identification of patients for care transitions programs
    - Quality improvement and population health management
    - Risk-stratified follow-up scheduling
    - Care coordination and case management prioritization
    
    Risk Stratification and Interventions:
    - Low Risk (0-4 points): Standard discharge planning and routine follow-up
    - Moderate Risk (5-9 points): Enhanced discharge planning with structured follow-up
    - High Risk (≥10 points): Intensive care coordination and early post-discharge contact
    
    Implementation Considerations:
    - Validated for adults ≥18 years in medical and surgical populations
    - Based on objective data available at discharge
    - Should complement clinical judgment and institutional protocols
    - Requires accurate Charlson Comorbidity Index calculation
    - ED visits should include all visits in prior 6 months
    
    Args:
        request: Parameters including length of stay, admission acuity, 
                comorbidity index, and recent emergency department utilization
        
    Returns:
        LaceIndexReadmissionResponse: LACE score with risk assessment and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lace_index_readmission", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating LACE Index for Readmission",
                    "details": {"parameters": parameters}
                }
            )
        
        return LaceIndexReadmissionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for LACE Index calculation",
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
                "message": "Internal error in LACE Index calculation",
                "details": {"error": str(e)}
            }
        )