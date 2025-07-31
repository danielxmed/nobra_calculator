"""
European System for Cardiac Operative Risk Evaluation (EuroSCORE) II Router

Endpoint for calculating EuroSCORE II to predict in-hospital mortality after cardiac surgery.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.euroscore_ii import (
    EuroScoreIIRequest,
    EuroScoreIIResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/euroscore_ii", response_model=EuroScoreIIResponse)
async def calculate_euroscore_ii(request: EuroScoreIIRequest):
    """
    Calculates European System for Cardiac Operative Risk Evaluation (EuroSCORE) II
    
    The EuroSCORE II predicts in-hospital mortality risk after major cardiac surgery using 
    a logistic regression model with 18 validated variables across patient-related, 
    cardiac-related, and operation-related factors.
    
    Key Features:
    - Logistic regression model: mortality = e^y / (1 + e^y) × 100%
    - Constant term: -5.324537
    - 18 variables with specific coefficients
    - Excellent discrimination (AUC 0.8095)
    - Well calibrated in validation studies
    
    Variable Categories:
    
    Patient-Related Factors (7 variables):
    - Age (coefficient increases after 60 years)
    - Sex (female has higher coefficient)
    - Insulin-dependent diabetes
    - Chronic pulmonary dysfunction
    - Neurological/musculoskeletal mobility dysfunction
    - Creatinine clearance (4 categories)
    - Critical preoperative state
    
    Cardiac-Related Factors (8 variables):
    - NYHA functional class (I-IV)
    - CCS Class 4 angina
    - Extracardiac arteriopathy
    - Previous cardiac surgery
    - Active endocarditis
    - Left ventricular function (4 categories)
    - Recent MI ≤90 days
    - Pulmonary hypertension
    
    Operation-Related Factors (3 variables):
    - Surgery urgency (elective to salvage)
    - Weight/complexity of intervention
    - Surgery on thoracic aorta
    
    Risk Stratification:
    - Low Risk (<2%): Standard care
    - Medium Risk (2-5%): Enhanced monitoring
    - High Risk (5-10%): Intensive care planning
    - Very High Risk (>10%): Consider alternatives
    
    Clinical Applications:
    - Preoperative risk assessment and informed consent
    - Surgical planning and resource allocation
    - Quality improvement and outcome benchmarking
    - Patient and family counseling
    - Multidisciplinary team decision-making
    
    Model Development:
    - Based on 22,381 patients in 154 hospitals across 43 countries
    - Contemporary data from May-July 2010
    - Significant improvement over original EuroSCORE
    - Reduces overestimation by approximately 50%
    
    Performance Characteristics:
    - Area under ROC curve: 0.8095
    - Predicted mortality: 3.95% vs actual: 4.18%
    - Well calibrated across risk categories
    - Superior to original EuroSCORE models
    
    Important Limitations:
    - Designed for in-hospital mortality only
    - May require local calibration
    - Not applicable to transcatheter procedures
    - Should complement clinical judgment
    - Based on 2010 data; outcomes continue to improve
    
    Args:
        request: Parameters including all 18 EuroSCORE II variables
        
    Returns:
        EuroScoreIIResponse: Mortality percentage, risk category, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("euroscore_ii", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EuroSCORE II",
                    "details": {"parameters": parameters}
                }
            )
        
        return EuroScoreIIResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EuroSCORE II",
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