"""
Utah COVID-19 Risk Score Router

Endpoint for calculating Utah COVID-19 Risk Score to identify high-risk individuals 
appropriate for COVID-19 treatment and prioritize oral antiviral treatment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.utah_covid19_risk_score import (
    UtahCovid19RiskScoreRequest,
    UtahCovid19RiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/utah_covid19_risk_score",
    response_model=UtahCovid19RiskScoreResponse,
    summary="Calculate Utah COVID-19 Risk Score",
    description="Calculates the Utah COVID-19 Risk Score to identify high-risk individuals appropriate for COVID-19 treatment and help prioritize oral antiviral treatment during medication shortages. This evidence-based calculator was developed by Utah Department of Health and Intermountain Healthcare to optimize treatment allocation based on hospitalization risk factors. The score uses age, comorbidities, and symptoms to determine treatment eligibility with different thresholds based on vaccination status: vaccinated patients require ≥8 points, unvaccinated patients require ≥6 points, and unvaccinated pregnant patients require ≥4 points. Updated in February 2022 to remove race/ethnicity and gender criteria while maintaining evidence-based risk stratification. Should be used within 10 days of symptom onset and complement clinical judgment rather than replace comprehensive medical evaluation.",
    response_description="The calculated Utah COVID-19 Risk Score with treatment eligibility determination, vaccination status-specific thresholds, component score breakdown, clinical recommendations, and important safety considerations",
    operation_id="utah_covid19_risk_score"
)
async def calculate_utah_covid19_risk_score(request: UtahCovid19RiskScoreRequest):
    """
    Calculates Utah COVID-19 Risk Score for treatment prioritization
    
    The Utah COVID-19 Risk Score identifies high-risk individuals appropriate for COVID-19 
    treatment and helps prioritize oral antiviral treatment during medication shortages. 
    Developed by Utah Department of Health and Intermountain Healthcare, this calculator 
    uses evidence-based risk factors including age, comorbidities, and symptoms to determine 
    treatment eligibility.
    
    **SCORING SYSTEM:**
    - **Age Points**: Progressive risk from 1.0 (16-20 years) to 5.5 (≥101 years)
    - **Highest Risk Comorbidities (2 points each)**: Diabetes mellitus, obesity (BMI >30)
    - **Other High-Risk Comorbidities (1 point each)**: Active cancer, immunosuppression, 
      cardiovascular conditions, chronic organ diseases
    - **Symptom Risk Factor (1 point)**: New shortness of breath
    
    **TREATMENT THRESHOLDS:**
    - **Vaccinated**: ≥8 points
    - **Unvaccinated/Incomplete vaccination**: ≥6 points  
    - **Unvaccinated/Incomplete vaccination + Pregnant**: ≥4 points
    
    **CLINICAL USE:**
    - Use within 10 days of COVID-19 symptom onset
    - Helps prioritize limited antiviral resources
    - Should complement clinical judgment, not replace evaluation
    - Consider individual patient factors and local resource availability
    
    **IMPORTANT LIMITATIONS:**
    - Developed during COVID-19 crisis, not externally validated
    - Based on Intermountain Healthcare system data
    - Updated February 2022 to address health equity concerns
    - May need adjustment based on evolving viral variants
    
    Args:
        request: Utah COVID-19 Risk Score parameters including age, comorbidities, 
                symptoms, and vaccination status
        
    Returns:
        UtahCovid19RiskScoreResponse: Risk score with treatment eligibility, clinical 
        recommendations, and safety considerations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("utah_covid19_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Utah COVID-19 Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return UtahCovid19RiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Utah COVID-19 Risk Score",
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
                "message": "Internal error in Utah COVID-19 Risk Score calculation",
                "details": {"error": str(e)}
            }
        )