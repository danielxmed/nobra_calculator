"""
Fong Clinical Risk Score Router

Endpoint for calculating the Fong Clinical Risk Score for colorectal cancer recurrence.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.fong_clinical_risk_score import (
    FongClinicalRiskScoreRequest,
    FongClinicalRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fong_clinical_risk_score",
    response_model=FongClinicalRiskScoreResponse,
    summary="Calculate Fong Clinical Risk Score for Colorectal Cancer ...",
    description="Predicts recurrence and survival risk for colorectal cancer patients with liver metastases after hepatic resection. Developed from analysis of 1,001 consecutive cases to identify high-risk patients who may benefit from adjuvant therapy or closer surveillance.",
    response_description="The calculated fong clinical risk score with interpretation",
    operation_id="calculate_fong_clinical_risk_score"
)
async def calculate_fong_clinical_risk_score(request: FongClinicalRiskScoreRequest):
    """
    Calculates Fong Clinical Risk Score for Colorectal Cancer Recurrence
    
    The Fong Clinical Risk Score predicts recurrence and survival risk for colorectal cancer 
    patients with liver metastases after hepatic resection. Developed from analysis of 1,001 
    consecutive cases at Memorial Sloan-Kettering Cancer Center.
    
    **Clinical Parameters (1 point each):**
    - Node-positive primary tumor (lymph node involvement)
    - Disease-free interval <12 months from primary to liver metastasis
    - Multiple (>1) liver metastases
    - Preoperative CEA level >200 ng/mL
    - Largest liver metastasis >5 cm
    
    **Score Range:** 0-5 points
    
    **Risk Stratification:**
    - Score 0-2: Favorable prognosis (5-year survival 30-60%)
    - Score 3-5: Poor prognosis (5-year survival 11-16%)
    
    **Clinical Applications:**
    - Risk stratification for surgical planning
    - Patient counseling regarding prognosis
    - Selection for adjuvant therapy trials
    - Postoperative surveillance planning
    
    **Treatment Implications:**
    - Patients with scores 0-2 are good candidates for hepatic resection
    - Patients with scores ≥3 should be considered for experimental adjuvant therapy
    - High scores may benefit from neoadjuvant chemotherapy before resection
    
    Args:
        request: Fong Clinical Risk Score parameters
        
    Returns:
        FongClinicalRiskScoreResponse: Calculated score with prognostic interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fong_clinical_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fong Clinical Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FongClinicalRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fong Clinical Risk Score",
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
                "message": "Internal error in Fong Clinical Risk Score calculation",
                "details": {"error": str(e)}
            }
        )