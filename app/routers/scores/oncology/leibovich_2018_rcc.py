"""
2018 Leibovich Model for Renal Cell Carcinoma (RCC) router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.leibovich_2018_rcc import (
    Leibovich2018RccRequest,
    Leibovich2018RccResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/leibovich_2018_rcc",
             response_model=Leibovich2018RccResponse,
             summary="Calculate 2018 Leibovich Model for RCC",
             description="Predicts progression-free and cancer-specific survival in renal cell carcinoma patients",
             response_description="Prognostic assessment with survival predictions and risk stratification")
async def calculate_leibovich_2018_rcc(request: Leibovich2018RccRequest):
    """
    **Calculate 2018 Leibovich Model for Renal Cell Carcinoma (RCC)**
    
    Comprehensive prognostic model predicting both progression-free survival (PFS) and 
    cancer-specific survival (CSS) in patients with renal cell carcinoma following nephrectomy.
    
    **Clinical Applications:**
    - Post-nephrectomy risk stratification
    - Surveillance intensity planning
    - Adjuvant therapy decision-making
    - Clinical trial enrollment consideration
    - Patient and family counseling regarding prognosis
    - Quality metrics for oncological care
    
    **Model Components:**
    **Clinical Factors:**
    - Age at surgery (≥60 years affects CSS)
    - ECOG Performance Status (≥1 affects CSS)
    - Constitutional symptoms (fever, night sweats, weight loss)
    
    **Surgical Factors:**
    - Adrenalectomy performed (affects CSS)
    - Surgical margin status (positive margins affect CSS)
    
    **Pathologic Factors:**
    - Tumor grade (Fuhrman/WHO-ISUP: 1-4)
    - Coagulative necrosis presence
    - Sarcomatoid differentiation (affects CSS)
    - Tumor size in centimeters
    - Perinephric/renal sinus fat invasion
    - Tumor thrombus level (0, 1-4, or none)
    - Extension beyond kidney capsule (affects PFS)
    
    **Risk Stratification:**
    - **Low Risk (0-4 points)**: Excellent prognosis, standard surveillance
    - **Intermediate Risk (5-9 points)**: Good prognosis, enhanced surveillance
    - **High Risk (10-14 points)**: Poor prognosis, intensive surveillance + adjuvant therapy
    - **Very High Risk (≥15 points)**: Very poor prognosis, aggressive management
    
    **Surveillance Recommendations:**
    - Low risk: Annual imaging for 5 years
    - Intermediate risk: Every 6 months for 2 years, then annually
    - High/Very High risk: Every 3-6 months for 3 years, then annually
    
    **Adjuvant Therapy Considerations:**
    - High-risk patients may benefit from adjuvant sunitinib or pembrolizumab
    - Very high-risk patients should be considered for clinical trials
    - Consider comorbidities and patient preferences in decision-making
    
    **Note:** This model is specifically validated for clear cell renal cell carcinoma.
    Separate models exist for papillary and chromophobe subtypes.
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "ecog_status": request.ecog_status,
            "constitutional_symptoms": request.constitutional_symptoms,
            "adrenalectomy": request.adrenalectomy,
            "surgical_margins": request.surgical_margins,
            "tumor_grade": request.tumor_grade,
            "coagulative_necrosis": request.coagulative_necrosis,
            "sarcomatoid_differentiation": request.sarcomatoid_differentiation,
            "tumor_size": request.tumor_size,
            "perinephric_invasion": request.perinephric_invasion,
            "tumor_thrombus": request.tumor_thrombus,
            "extension_beyond_kidney": request.extension_beyond_kidney
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("leibovich_2018_rcc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 2018 Leibovich Model for RCC",
                    "details": {"parameters": parameters}
                }
            )
        
        return Leibovich2018RccResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 2018 Leibovich Model for RCC",
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