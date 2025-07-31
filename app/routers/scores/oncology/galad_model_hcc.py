"""
GALAD Model for Hepatocellular Carcinoma (HCC) Router

Endpoint for calculating GALAD Model HCC detection score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.galad_model_hcc import (
    GaladModelHccRequest,
    GaladModelHccResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/galad_model_hcc",
    response_model=GaladModelHccResponse,
    summary="Calculate GALAD Model for Hepatocellular Carcinoma (HCC)",
    description="Diagnoses HCC based on serum biomarkers in patients with chronic liver disease (CLD). The GALAD model combines Gender, Age, AFP-L3, AFP, and DCP (des-gamma-carboxy prothrombin) to provide superior diagnostic accuracy compared to individual biomarkers.",
    response_description="The calculated galad model hcc with interpretation",
    operation_id="galad_model_hcc"
)
async def calculate_galad_model_hcc(request: GaladModelHccRequest):
    """
    Calculates GALAD Model for Hepatocellular Carcinoma Detection
    
    The GALAD model combines Gender, Age, AFP-L3, AFP, and DCP (des-gamma-carboxy 
    prothrombin) to provide superior diagnostic accuracy for HCC detection in patients 
    with chronic liver disease. This validated model outperforms individual biomarkers 
    and ultrasound screening for early HCC detection.
    
    **Clinical Applications**:
    - HCC screening in high-risk patients with chronic liver disease
    - Early detection of hepatocellular carcinoma (BCLC stage 0/A)
    - Risk stratification for patients with cirrhosis, hepatitis B/C, or NASH
    - Decision support for diagnostic imaging in suspected HCC
    - Surveillance monitoring in liver transplant candidates
    
    **Performance Characteristics**:
    - Overall HCC detection: AUC 0.95 (superior to AFP: 0.88, AFP-L3: 0.86, DCP: 0.87)
    - Early-stage HCC detection: AUC 0.92
    - At threshold ≥-0.63: Sensitivity 85.6%, Specificity 93.3%
    - Superior to ultrasound alone: AUC 0.95 vs 0.82 (p<0.01)
    
    **Required Biomarkers**:
    - **AFP**: Alpha-fetoprotein in ng/mL (normal <10, suspicious >20)
    - **AFP-L3**: AFP-L3 percentage 0-100% (≥10% high risk for HCC)
    - **DCP**: Des-gamma-carboxy prothrombin in mAU/mL (normal <40, suspicious >100)
    
    **Interpretation**:
    - **GALAD <-0.63**: Low HCC probability - continue routine surveillance
    - **GALAD ≥-0.63**: High HCC probability - urgent imaging and specialist referral
    
    Args:
        request: Patient demographics and serum biomarker values required for 
                GALAD calculation (age, sex, AFP, AFP-L3%, DCP)
        
    Returns:
        GaladModelHccResponse: GALAD score with risk stratification and detailed 
                              clinical management recommendations including surveillance 
                              or urgent evaluation protocols
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("galad_model_hcc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GALAD Model for HCC",
                    "details": {"parameters": parameters}
                }
            )
        
        return GaladModelHccResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GALAD Model HCC calculation",
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
                "message": "Internal error in GALAD Model calculation",
                "details": {"error": str(e)}
            }
        )