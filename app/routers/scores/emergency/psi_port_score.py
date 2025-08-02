"""
PSI/PORT Score: Pneumonia Severity Index for CAP Router

Endpoint for calculating PSI/PORT Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.psi_port_score import (
    PsiPortScoreRequest,
    PsiPortScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/psi_port_score",
    response_model=PsiPortScoreResponse,
    summary="Calculate PSI/PORT Score: Pneumonia Severity Index for CAP",
    description="Estimates mortality for adult patients with community-acquired pneumonia (CAP) "
                "and guides hospitalization decisions. This extensively validated clinical prediction "
                "rule is the gold standard for pneumonia severity assessment, recommended in the "
                "2019 ATS/IDSA guidelines over other scoring systems. The PSI uses 20 clinical "
                "variables including demographics, comorbidities, physical examination findings, "
                "and laboratory results to stratify patients into five risk classes (I-V) with "
                "corresponding 30-day mortality rates: Class I (<1%), Class II (≤3%), Class III "
                "(≤3%), Class IV (8-9%), and Class V (27-31%). Risk stratification guides critical "
                "decisions about outpatient treatment, observation admission, standard hospitalization, "
                "or ICU-level care. The tool has been validated on over 50,000 patients and "
                "demonstrates superior performance in identifying low-risk patients suitable for "
                "outpatient management while ensuring appropriate hospitalization for higher-risk "
                "cases. Clinical applications include emergency department triage, primary care "
                "assessment, quality improvement initiatives, and healthcare resource optimization. "
                "The score incorporates age as absolute points, provides female sex protection "
                "(-10 points), and weights comorbidities and clinical findings based on mortality "
                "impact. Laboratory values including arterial blood gas measurements are optional "
                "but improve accuracy when available.",
    response_description="The calculated PSI/PORT score with risk class and comprehensive disposition guidance",
    operation_id="psi_port_score"
)
async def calculate_psi_port_score(request: PsiPortScoreRequest):
    """
    Calculates PSI/PORT Score: Pneumonia Severity Index for CAP
    
    This clinical prediction rule estimates 30-day mortality risk in adults
    with community-acquired pneumonia to guide hospitalization decisions.
    
    Args:
        request: Clinical parameters including demographics, comorbidities, 
                physical examination findings, and laboratory results
        
    Returns:
        PsiPortScoreResponse: Result with risk class and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("psi_port_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating PSI/PORT Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return PsiPortScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for PSI/PORT Score",
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