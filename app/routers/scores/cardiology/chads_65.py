"""
CHADS-65 (Canadian Society of Cardiology Guideline) Router

Endpoint for CHADS-65 decision algorithm for antithrombotic therapy in atrial fibrillation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.chads_65 import (
    Chads65Request,
    Chads65Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/chads_65",
    response_model=Chads65Response,
    summary="Calculate CHADS-65 (Canadian Society of Cardiol...",
    description="Clinical decision algorithm developed by the Canadian Cardiovascular Society to guide antithrombotic therapy for patients with nonvalvular atrial fibrillation or atrial flutter. Uses age-based approach to determine whether patients should receive oral anticoagulation, antiplatelet therapy, or no antithrombotic therapy for stroke prevention.",
    response_description="The calculated chads 65 with interpretation",
    operation_id="chads_65"
)
async def calculate_chads_65(request: Chads65Request):
    """
    Calculates CHADS-65 (Canadian Society of Cardiology Guideline)
    
    The CHADS-65 is a clinical decision algorithm (not a numerical scoring system) 
    developed by the Canadian Cardiovascular Society to guide antithrombotic therapy 
    for patients with nonvalvular atrial fibrillation or atrial flutter. This evidence-based 
    tool uses age as the primary decision point to determine appropriate stroke prevention therapy.
    
    **Algorithm Structure** (Sequential Decision Tree):
    
    **Step 1: Age Assessment**
    - Age ≥65 years? → YES: Oral Anticoagulation (OAC) → END
    - Age ≥65 years? → NO: Proceed to Step 2
    
    **Step 2: CHADS₂ Risk Factor Assessment**
    - Any CHADS₂ risk factors present?
      - Congestive heart failure
      - Hypertension  
      - Diabetes mellitus
      - Stroke/TIA history
    - YES: Oral Anticoagulation (OAC) → END
    - NO: Proceed to Step 3
    
    **Step 3: Vascular Disease Assessment**
    - Coronary artery disease OR Peripheral artery disease?
    - YES: Antiplatelet therapy (ASA 81mg daily) → END
    - NO: No antithrombotic therapy → END
    
    **Treatment Recommendations**:
    
    **Oral Anticoagulation (OAC)**:
    - Indications: Age ≥65 years OR any CHADS₂ risk factor present
    - Preferred agents: Direct oral anticoagulants (DOACs) over warfarin
    - Clinical rationale: Annual stroke risk 2.1% (ages 65-74), 4.4% (ages ≥75)
    - Monitoring: Regular follow-up for efficacy and bleeding complications
    
    **Antiplatelet Therapy**: 
    - Indications: Age <65, no CHADS₂ factors, but vascular disease present
    - Medication: ASA 81mg daily
    - Clinical rationale: Stroke prevention in patients with vascular disease
    - Monitoring: Annual reassessment and bleeding risk evaluation
    
    **No Antithrombotic Therapy**:
    - Indications: Age <65, no CHADS₂ factors, no vascular disease
    - Clinical rationale: Very low stroke risk based on current assessment
    - Monitoring: Annual reassessment as risk factors may change
    
    **Clinical Applications**:
    - **Primary Care**: Rapid decision-making for AF stroke prevention
    - **Emergency Medicine**: Streamlined approach for AF patients
    - **Cardiology**: Evidence-based therapy selection
    - **Quality Improvement**: Standardized approach reducing practice variation
    
    **Key Clinical Principles**:
    - Age ≥65 years alone is sufficient indication for anticoagulation
    - Simplifies decision-making compared to complex numerical risk scores
    - Based on Canadian national data and validated CHADS₂ components
    - Combination ASA + OAC beyond 1 year not recommended (bleeding risk)
    - For recent coronary stents, consult interventional cardiologist
    
    **Evidence Base**:
    - Endorsed with Strong Recommendation, High-Quality Evidence (CCS 2020)
    - Based on Danish national cohort study data
    - Designed for emergency departments and primary care settings
    - Emphasizes age as reliable, easily determined risk factor
    
    **Important Considerations**:
    - Apply only to nonvalvular atrial fibrillation and atrial flutter
    - Assess bleeding risk, drug interactions, and patient preferences
    - Consider individual patient factors and comorbidities  
    - Annual reassessment recommended as risk profile may change
    - Algorithm provides framework but clinical judgment remains important
    
    This algorithm represents a paradigm shift in AF management, emphasizing that 
    age-based risk stratification can effectively guide therapy selection while 
    simplifying clinical decision-making.
    
    Args:
        request: Clinical parameters needed for CHADS-65 algorithm
        
    Returns:
        Chads65Response: Algorithm result with evidence-based therapy recommendation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("chads_65", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHADS-65 algorithm",
                    "details": {"parameters": parameters}
                }
            )
        
        return Chads65Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHADS-65 algorithm",
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