"""
VACO Index COVID-19 Mortality Risk Router

Endpoint for calculating VACO Index COVID-19 mortality risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.vaco_index_covid19 import (
    VacoIndexCovid19Request,
    VacoIndexCovid19Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/vaco_index_covid19",
    response_model=VacoIndexCovid19Response,
    summary="Calculate For Patients: VACO Index COVID-19 Mortality Risk",
    description="Estimates 30-day mortality risk after COVID-19 infection using pre-existing health conditions and demographics. Developed by researchers from Yale University and VA Connecticut Healthcare System in collaboration with the US Department of Health and Human Services.",
    response_description="The calculated vaco index covid19 with interpretation",
    operation_id="vaco_index_covid19"
)
async def calculate_vaco_index_covid19(request: VacoIndexCovid19Request):
    """
    Calculates VACO Index COVID-19 Mortality Risk
    
    The VACO Index COVID-19 Mortality Risk calculator estimates 30-day mortality risk 
    after COVID-19 infection using pre-existing health conditions and demographics. 
    Developed by researchers from Yale University and VA Connecticut Healthcare System 
    in collaboration with the US Department of Health and Human Services.
    
    **Key Features:**
    - Uses age-specific coefficients and Charlson Comorbidity Index
    - Stratifies patients into four risk categories
    - Patient-facing tool for informed decision-making
    - Based on analysis of 13,323 COVID-19 patients
    
    **Risk Categories:**
    - **Lower Risk (0-8.7%)**: Standard preventive measures
    - **Moderate Risk (8.8-16.0%)**: Enhanced preventive measures recommended
    - **High Risk (16.1-21.2%)**: Strict preventive measures, additional protection
    - **Extreme Risk (>21.3%)**: Maximum preventive measures, medical consultation
    
    **Clinical Applications:**
    - Patient risk stratification for preventive measures
    - Healthcare provider-patient risk discussions
    - Vaccination prioritization considerations
    - Public health guidance for high-risk populations
    - Informed decision-making about protective behaviors
    
    **Input Parameters:**
    - Age (20-115 years) with age-specific risk coefficients
    - Sex (higher risk for males)
    - 14 comorbidity conditions based on Charlson Comorbidity Index
    
    **Important Notes:**
    - Estimates mortality risk, not infection risk
    - Mortality risk is 8-12 times higher than seasonal influenza
    - Based on veterans data, may not fully generalize to all populations
    - Should be interpreted in consultation with healthcare professionals
    - Does not account for vaccination status or treatment advances
    
    Args:
        request: VACO Index COVID-19 parameters including age, sex, and comorbidities
        
    Returns:
        VacoIndexCovid19Response: 30-day mortality risk percentage with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("vaco_index_covid19", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating VACO Index COVID-19 Mortality Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return VacoIndexCovid19Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for VACO Index COVID-19 Mortality Risk",
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
                "message": "Internal error in VACO Index COVID-19 calculation",
                "details": {"error": str(e)}
            }
        )