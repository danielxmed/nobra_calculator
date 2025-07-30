"""
CHADS₂ Score for Atrial Fibrillation Stroke Risk Router

Endpoint for calculating CHADS₂ Score for stroke risk assessment in atrial fibrillation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.chads2_score import (
    Chads2ScoreRequest,
    Chads2ScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/chads2_score", response_model=Chads2ScoreResponse)
async def calculate_chads2_score(request: Chads2ScoreRequest):
    """
    Calculates CHADS₂ Score for Atrial Fibrillation Stroke Risk
    
    The CHADS₂ score is a clinical prediction tool that estimates annual stroke risk 
    in patients with atrial fibrillation to guide anticoagulation therapy decisions. 
    Developed from the National Registry of Atrial Fibrillation in 2001, it has been 
    validated across multiple populations and healthcare systems worldwide.
    
    **CHADS₂ Components** (Acronym with Point Values):
    
    **C - Congestive Heart Failure (1 point)**:
    - History of heart failure or left ventricular dysfunction
    - Includes both systolic and diastolic heart failure
    - Based on clinical diagnosis or echocardiographic evidence
    
    **H - Hypertension (1 point)**:
    - History of hypertension or current antihypertensive treatment
    - Blood pressure >140/90 mmHg on repeated measurements
    - Includes well-controlled hypertension on medication
    
    **A - Age ≥75 years (1 point)**:
    - Advanced age as an independent stroke risk factor
    - Threshold reflects significantly increased risk in elderly patients
    
    **D - Diabetes Mellitus (1 point)**:
    - History of diabetes or current antidiabetic treatment
    - Type 1 or Type 2 diabetes mellitus
    - Includes diet-controlled and medication-controlled diabetes
    
    **S₂ - Stroke/TIA/Thromboembolism (2 points)**:
    - Previous ischemic stroke, hemorrhagic stroke, or TIA
    - History of systemic thromboembolism
    - Worth 2 points due to very high recurrence risk
    
    **Risk Categories and Annual Stroke Rates**:
    
    - **Score 0**: 1.9% annual risk (Low) - Consider CHA₂DS₂-VASc or aspirin
    - **Score 1**: 2.8% annual risk (Low-Intermediate) - Consider further stratification
    - **Score 2**: 4.0% annual risk (Intermediate) - Anticoagulation generally recommended
    - **Score 3**: 5.9% annual risk (High) - Strong anticoagulation recommendation
    - **Score 4**: 8.5% annual risk (High) - Strong anticoagulation recommendation
    - **Score 5**: 12.5% annual risk (Very High) - Strong anticoagulation recommendation
    - **Score 6**: 18.2% annual risk (Very High) - Strong anticoagulation recommendation
    
    **Anticoagulation Recommendations**:
    
    **Score 0-1**: 
    - Consider further risk stratification with CHA₂DS₂-VASc score
    - May consider aspirin based on bleeding risk assessment
    - Individual decision-making important
    
    **Score ≥2**: 
    - Generally recommended for anticoagulation therapy
    - Benefit typically outweighs bleeding risk
    - Options include warfarin (INR 2.0-3.0) or DOACs
    
    **Score ≥3**: 
    - Strong recommendation for anticoagulation
    - Direct oral anticoagulants (DOACs) often preferred over warfarin
    - Careful adherence and monitoring critical
    
    **Clinical Applications**:
    - **Primary Care**: Rapid stroke risk assessment for AF patients
    - **Cardiology**: Anticoagulation decision-making
    - **Emergency Medicine**: Risk stratification for newly diagnosed AF
    - **Quality Improvement**: Standardized approach to stroke prevention
    
    **Clinical Performance**:
    - C-statistic: ~0.68 for stroke prediction
    - Simple bedside calculation enables rapid assessment
    - Validated across diverse populations and healthcare systems
    - Better at identifying high-risk than truly low-risk patients
    
    **Historical Context and Evolution**:
    - Developed 2001 from National Registry of Atrial Fibrillation
    - Landmark study establishing stroke risk stratification in AF
    - Largely superseded by CHA₂DS₂-VASc (2010) for more comprehensive assessment
    - CHA₂DS₂-VASc includes additional factors: vascular disease, age 65-74, female sex
    
    **Important Considerations**:
    - Apply only to nonvalvular atrial fibrillation
    - Consider bleeding risk assessment (HAS-BLED) alongside stroke risk
    - Individual patient factors and preferences important
    - Among patients 65-95 years, <7% classified as truly low risk
    - Current guidelines generally recommend CHA₂DS₂-VASc for more accurate stratification
    
    This calculator provides the foundational CHADS₂ assessment while noting that 
    contemporary practice often utilizes the more comprehensive CHA₂DS₂-VASc score 
    for enhanced risk stratification.
    
    Args:
        request: Clinical parameters needed for CHADS₂ score calculation
        
    Returns:
        Chads2ScoreResponse: Score with stroke risk assessment and anticoagulation recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("chads2_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHADS₂ Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Chads2ScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHADS₂ Score",
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