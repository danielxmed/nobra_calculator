"""
COVID-GRAM Critical Illness Risk Score Router

Endpoint for calculating COVID-GRAM Critical Illness Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.covid_gram_critical_illness import (
    CovidGramCriticalIllnessRequest,
    CovidGramCriticalIllnessResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/covid_gram_critical_illness",
    response_model=CovidGramCriticalIllnessResponse,
    summary="Calculate COVID-GRAM Critical Illness Risk Score",
    description="Predicts risk of critical illness (ICU admission, mechanical ventilation, or death) in hospitalized COVID-19 patients",
    response_description="The calculated covid gram critical illness with interpretation",
    operation_id="calculate_covid_gram_critical_illness"
)
async def calculate_covid_gram_critical_illness(request: CovidGramCriticalIllnessRequest):
    """
    Calculates COVID-GRAM Critical Illness Risk Score
    
    Predicts risk of critical illness (ICU admission, mechanical ventilation, or death) 
    in hospitalized COVID-19 patients using 10 clinical variables available at admission.
    
    The COVID-GRAM model was developed from 1590 patients and validated in 710 patients, 
    achieving an AUC of 0.88 (95% CI, 0.85-0.91) in the development cohort. It outperformed 
    the CURB-65 model (AUC 0.75 vs 0.88) for COVID-19 critical illness prediction.
    
    **Clinical Variables:**
    - Chest X-ray abnormality (yes/no)
    - Age (years)
    - Hemoptysis (yes/no)
    - Dyspnea (yes/no)
    - Unconsciousness (yes/no)
    - Number of comorbidities (0-10)
    - Cancer history (yes/no)
    - Neutrophil-lymphocyte ratio
    - Lactate dehydrogenase (U/L)
    - Direct bilirubin (mg/dL)
    
    **Risk Categories:**
    - Low Risk (<1.7%): Standard monitoring and care
    - Medium Risk (1.7-40.4%): Enhanced monitoring with close observation
    - High Risk (>40.4%): Intensive monitoring and ICU consideration
    
    **Clinical Application:**
    The score helps stratify COVID-19 patients at hospital admission to identify 
    those at highest risk for critical illness, enabling appropriate resource 
    allocation and monitoring intensity.
    
    **Reference:**
    Liang W, Liang H, Ou L, Chen B, Chen A, Li C, et al. Development and Validation 
    of a Clinical Risk Score to Predict the Occurrence of Critical Illness in 
    Hospitalized Patients With COVID-19. JAMA Intern Med. 2020;180(8):1081-1089.
    
    Args:
        request: Parameters needed for COVID-GRAM calculation
        
    Returns:
        CovidGramCriticalIllnessResponse: Risk probability with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("covid_gram_critical_illness", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating COVID-GRAM Critical Illness Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CovidGramCriticalIllnessResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for COVID-GRAM Critical Illness Risk Score",
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