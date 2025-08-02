"""
Indications for Paxlovid Router

Endpoint for determining Paxlovid eligibility.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.indications_for_paxlovid import (
    IndicationsForPaxlovidRequest,
    IndicationsForPaxlovidResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/indications_for_paxlovid",
    response_model=IndicationsForPaxlovidResponse,
    summary="Assess Paxlovid Eligibility and Prescribing Indications",
    description="Determines if Paxlovid (nirmatrelvir-ritonavir) is appropriate therapy for a "
                "COVID-19 positive patient based on FDA guidelines and clinical criteria. "
                "Paxlovid is an oral antiviral treatment authorized for mild-to-moderate COVID-19 "
                "in patients at high risk for progression to severe disease, hospitalization, or death. "
                "The assessment evaluates essential eligibility requirements including age (>12 years), "
                "weight (>40 kg), disease severity (mild-moderate only), symptom timing (≤5 days), "
                "renal function (eGFR >30), and absence of severe hepatic impairment. At least one "
                "high-risk factor must be present (age >50, diabetes, heart disease, lung disease, "
                "obesity, immunocompromised state, pregnancy, inadequate vaccination, or other CDC "
                "conditions). The tool screens for contraindications including significant drug "
                "interactions with ritonavir, which is a strong CYP3A4 inhibitor. Provides specific "
                "dosing recommendations with standard dosing (nirmatrelvir 300mg + ritonavir 100mg "
                "twice daily) or reduced dosing for moderate renal impairment. Critical for ensuring "
                "appropriate patient selection and optimizing therapeutic outcomes while minimizing "
                "adverse drug interactions in this time-sensitive antiviral therapy.",
    response_description="Paxlovid prescribing recommendation with dosing guidance and clinical considerations",
    operation_id="indications_for_paxlovid"
)
async def calculate_indications_for_paxlovid(request: IndicationsForPaxlovidRequest):
    """
    Assesses Paxlovid eligibility and prescribing indications
    
    Systematically evaluates FDA-approved criteria for Paxlovid therapy including 
    basic eligibility requirements, high-risk factors, and contraindications to 
    provide evidence-based prescribing recommendations.
    
    Args:
        request: Parameters needed for Paxlovid eligibility assessment
        
    Returns:
        IndicationsForPaxlovidResponse: Prescribing recommendation with dosing guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("indications_for_paxlovid", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error assessing Paxlovid eligibility",
                    "details": {"parameters": parameters}
                }
            )
        
        return IndicationsForPaxlovidResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Paxlovid eligibility assessment",
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