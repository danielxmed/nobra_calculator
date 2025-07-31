"""
CLIF-C ACLF (Acute-on-Chronic Liver Failure) Router

Endpoint for calculating CLIF-C ACLF mortality prediction score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.clif_c_aclf import (
    ClifCAclfRequest,
    ClifCAclfResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/clif_c_aclf",
    response_model=ClifCAclfResponse,
    summary="Calculate CLIF-C ACLF (Acute-on-Chronic Liver Failure)",
    description="Predicts mortality in acute-on-chronic liver failure patients",
    response_description="The calculated clif c aclf with interpretation",
    operation_id="calculate_clif_c_aclf"
)
async def calculate_clif_c_aclf(request: ClifCAclfRequest):
    """
    Calculates CLIF-C ACLF (Acute-on-Chronic Liver Failure) Score
    
    The CLIF-C ACLF score is a validated prognostic tool specifically designed to 
    predict mortality in patients with acute-on-chronic liver failure (ACLF). This 
    score provides superior mortality prediction compared to traditional liver disease 
    scores such as MELD, MELD-Na, and Child-Pugh in the ACLF population.
    
    Key Features:
    - Superior prognostic accuracy with AUROC 0.8 for 28-day mortality
    - Integrates organ failure assessment across 6 systems
    - Incorporates age and inflammatory markers (WBC count)
    - Provides critical risk thresholds for clinical decision-making
    
    Scoring Formula:
    CLIF-C ACLF Score = 10 × [0.33 × CLIF-C OF Score + 0.04 × age + 0.63 × ln(WBC) - 2]
    
    Organ Failure Assessment (CLIF-C OF Score):
    1. Liver: Total bilirubin (<6, 6-12, ≥12 mg/dL = 1-3 points)
    2. Kidney: Creatinine (<2, 2-3.5, ≥3.5 mg/dL or RRT = 1-3 points)
    3. Brain: Hepatic encephalopathy (Grade 0, 1-2, 3-4 = 1-3 points)
    4. Coagulation: INR (<2.0, 2.0-2.5, ≥2.5 = 1-3 points)
    5. Circulatory: MAP/vasopressors (≥70, <70, any+vasopressors = 1-3 points)
    6. Respiratory: PaO2/FiO2 or SpO2/FiO2 ratios (>300/357, 200-300/214-357, ≤200/214 = 1-3 points)
    
    Critical Risk Thresholds:
    - Score ≥70: Associated with 100% mortality at 28 days
    - Score ≥65 at 3-7 days: Indicates extremely poor prognosis
    - Score 45-64: Moderate risk requiring intensive monitoring
    - Score <45: Lower risk with potential for improvement
    
    Clinical Applications:
    - ICU admission and resource allocation decisions
    - Liver transplantation evaluation timing and urgency
    - Treatment intensity and goals of care discussions
    - Objective prognostic communication with families
    - Superior to MELD/Child-Pugh for ACLF mortality prediction
    
    Based on the CANONIC study from the EASL-CLIF consortium, this calculator 
    provides evidence-based risk stratification to guide optimal management of 
    patients with acute-on-chronic liver failure.
    
    Args:
        request: CLIF-C ACLF assessment parameters including age, WBC count, and 
                detailed organ failure assessment across liver, kidney, brain, 
                coagulation, circulatory, and respiratory systems
        
    Returns:
        ClifCAclfResponse: Comprehensive mortality risk assessment with score, 
        risk stratification, treatment recommendations, and detailed clinical 
        guidance for ACLF patient management
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("clif_c_aclf", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CLIF-C ACLF score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ClifCAclfResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CLIF-C ACLF calculation",
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
                "message": "Internal error in CLIF-C ACLF calculation",
                "details": {"error": str(e)}
            }
        )