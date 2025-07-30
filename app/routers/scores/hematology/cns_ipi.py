"""
Central Nervous System International Prognostic Index (CNS-IPI) Router

Endpoint for calculating CNS-IPI for CNS relapse risk assessment in DLBCL patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.cns_ipi import (
    CnsIpiRequest,
    CnsIpiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cns_ipi", response_model=CnsIpiResponse)
async def calculate_cns_ipi(request: CnsIpiRequest):
    """
    Calculates Central Nervous System International Prognostic Index (CNS-IPI)
    
    The CNS-IPI is a validated prognostic scoring system that predicts the risk of 
    central nervous system relapse in patients with diffuse large B-cell lymphoma 
    (DLBCL) treated with R-CHOP chemotherapy. This tool helps identify patients who 
    may benefit from CNS-directed prophylaxis and guides treatment planning decisions.
    
    The CNS-IPI uses 6 clinical and laboratory parameters (each scoring 0 or 1 point):
    
    CLINICAL PARAMETERS:
    - Age >60 years: Advanced age associated with increased CNS relapse risk
    - Elevated LDH: Lactate dehydrogenase above normal (marker of tumor burden)
    - ECOG Performance Status >1: Moderate to severe functional limitation
    - Advanced stage (III/IV): Ann Arbor staging with extensive disease distribution
    - >1 extranodal site: Multiple organ involvement beyond lymph nodes
    - Kidney/adrenal involvement: Specific high-risk anatomical locations
    
    RISK STRATIFICATION:
    - Low Risk (0-1 points): 0.6% CNS relapse rate at 2 years (46% of patients)
    - Intermediate Risk (2-3 points): 3.4% CNS relapse rate at 2 years (41% of patients)
    - High Risk (4-6 points): 10.2% CNS relapse rate at 2 years (12% of patients)
    
    CLINICAL MANAGEMENT RECOMMENDATIONS:
    - **Low Risk**: CNS prophylaxis generally not recommended, standard R-CHOP appropriate
    - **Intermediate Risk**: CNS prophylaxis may be considered based on additional risk factors
    - **High Risk**: CNS prophylaxis strongly recommended (intrathecal chemotherapy or high-dose MTX)
    
    Clinical Applications:
    - **Risk Stratification**: Objective assessment of CNS relapse risk at diagnosis
    - **Treatment Planning**: Evidence-based guidance for CNS prophylaxis decisions
    - **Patient Counseling**: Accurate prognostic information for informed consent
    - **Clinical Trials**: Standardized risk stratification for research protocols
    
    Validation Features:
    - Developed and validated in over 2,000 DLBCL patients
    - Validated across multiple international populations
    - Specifically designed for patients treated with R-CHOP
    - Helps optimize resource utilization by avoiding unnecessary prophylaxis
    
    Important Considerations:
    The CNS-IPI does not capture all high-risk patients. Additional features that may 
    increase CNS risk include involvement of breast, uterus, testis, epidural space, 
    bone marrow involvement, double-hit/triple-hit lymphomas, and MYC/BCL2 dual expression. 
    These factors should be considered alongside the CNS-IPI in clinical decision-making.
    
    Args:
        request: Parameters needed for CNS-IPI calculation
        
    Returns:
        CnsIpiResponse: Score with risk stratification and prophylaxis recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cns_ipi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CNS-IPI",
                    "details": {"parameters": parameters}
                }
            )
        
        return CnsIpiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CNS-IPI",
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