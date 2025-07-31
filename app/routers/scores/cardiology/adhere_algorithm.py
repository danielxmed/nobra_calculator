"""
Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm Router

Endpoint for calculating ADHERE Algorithm for heart failure mortality prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.adhere_algorithm import (
    AdhereAlgorithmRequest,
    AdhereAlgorithmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/adhere_algorithm", response_model=AdhereAlgorithmResponse, summary="Calculate ADHERE Algorithm", description="Calculates ADHERE Algorithm for heart failure mortality prediction", response_description="Risk level with clinical interpretation and recommended management approach", operation_id="adhere_algorithm")
async def calculate_adhere_algorithm(request: AdhereAlgorithmRequest):
    """
    Calculates Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm
    
    This calculator implements the ADHERE Algorithm, a simple decision tree-based 
    risk stratification tool that predicts in-hospital mortality in patients 
    hospitalized with acute decompensated heart failure. The algorithm was derived 
    from analysis of over 65,000 hospitalizations in the ADHERE registry.
    
    The algorithm uses three readily available clinical parameters at admission:
    - Blood urea nitrogen (BUN)
    - Systolic blood pressure (SBP)
    - Serum creatinine
    
    Clinical Applications:
    - Risk stratification for hospitalized heart failure patients
    - Guidance for level of care decisions (general ward vs. telemetry vs. ICU)
    - Resource allocation and care planning
    - Identification of high-risk patients requiring intensive monitoring
    - Clinical decision-making regarding therapeutic interventions
    
    Risk Categories and Management:
    - Low Risk (2.1-2.3% mortality): Standard heart failure management on general ward
    - Intermediate Risk (5.5-6.4% mortality): Enhanced monitoring on telemetry unit
    - Intermediate-High Risk (12.4-12.8% mortality): Consider ICU or step-down unit care
    - High Risk (19.8-21.9% mortality): Strong consideration for ICU admission
    
    Decision Tree Logic:
    1. If BUN <43 mg/dL → Low Risk
    2. If BUN ≥43 mg/dL and SBP ≥115 mmHg → Intermediate Risk
    3. If BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine <2.75 mg/dL → Intermediate-High Risk
    4. If BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine ≥2.75 mg/dL → High Risk
    
    Important Notes:
    - BUN was identified as the strongest single predictor of mortality in the registry
    - The algorithm uses a simple decision tree rather than a complex scoring system
    - Should be used in conjunction with clinical judgment and other prognostic factors
    - Not validated in patients with acute heart failure secondary to acute coronary syndromes
    - May not be applicable to patients with end-stage renal disease or those on dialysis
    - Mortality rates are based on the original ADHERE registry and may vary in different populations
    
    Args:
        request: Parameters including BUN level, systolic blood pressure, and 
                serum creatinine level at admission
        
    Returns:
        AdhereAlgorithmResponse: Risk level with clinical interpretation and 
                               recommended management approach
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("adhere_algorithm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm",
                    "details": {"parameters": parameters}
                }
            )
        
        return AdhereAlgorithmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm",
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