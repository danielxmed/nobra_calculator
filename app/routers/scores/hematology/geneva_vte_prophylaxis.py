"""
Geneva Risk Score for Venous Thromboembolism (VTE) Prophylaxis Router

Endpoint for calculating Geneva VTE Risk Score for hospitalized patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.geneva_vte_prophylaxis import (
    GenevaVteProphylaxisRequest,
    GenevaVteProphylaxisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/geneva_vte_prophylaxis",
    response_model=GenevaVteProphylaxisResponse,
    summary="Calculate Geneva Risk Score for Venous Thromboembolism",
    description="Predicts the need for venous thromboembolism (VTE) prophylaxis in hospitalized medical patients by assessing risk factors to identify patients who would benefit from thromboprophylaxis versus those at low risk who may not require anticoagulation",
    response_description="The calculated geneva vte prophylaxis with interpretation",
    operation_id="geneva_vte_prophylaxis"
)
async def calculate_geneva_vte_prophylaxis(request: GenevaVteProphylaxisRequest):
    """
    Calculates Geneva Risk Score for Venous Thromboembolism (VTE) Prophylaxis
    
    The Geneva Risk Score for VTE Prophylaxis is a validated clinical decision tool for 
    predicting the need for venous thromboembolism prophylaxis in hospitalized medical 
    patients. This evidence-based score helps clinicians identify patients at high risk 
    for VTE who would benefit from thromboprophylaxis and those at low risk who may 
    not require anticoagulation, optimizing prophylaxis decisions while minimizing 
    unnecessary interventions and associated risks.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    VTE risk stratification in hospitalized medical patients to guide evidence-based 
    thromboprophylaxis decisions and optimize the balance between VTE prevention 
    efficacy and bleeding safety.
    
    **Key Clinical Advantages**:
    
    **Evidence-Based Decision Making**:
    - Derived and validated through multicenter studies including the ESTIMATE trial
    - Superior negative predictive value compared to other risk assessment tools
    - Standardized approach reducing variability in prophylaxis decisions
    - Cost-effective identification of patients who can safely avoid anticoagulation
    
    **Clinical Validation and Performance**:
    - Validated in 1,478 hospitalized medical patients across multiple centers
    - Low-risk patients (<3 points): 0.6% VTE rate (95% CI: 0.2-1.9%)
    - High-risk patients (≥3 points): 3.2% VTE rate (95% CI: 2.2-4.6%)
    - Negative likelihood ratio: 0.28 (95% CI: 0.10-0.83)
    - Superior accuracy for identifying low-risk patients compared to Padua Prediction Score
    
    **Risk Assessment Framework**:
    - Incorporates 19 clinical risk factors with differential weighting
    - Major risk factors (2 points each): cardiac failure, respiratory failure, stroke, MI, 
      infection, malignancy, hypercoagulable states
    - Minor risk factors (1 point each): age >60, immobilization, obesity, travel, 
      hormonal therapy
    - Binary risk stratification with validated threshold of ≥3 points
    
    **Clinical Decision Support**:
    
    **Low Risk Management (<3 points)**:
    - **VTE Incidence**: 0.6% three-month VTE rate
    - **Prophylaxis Approach**: Mechanical prophylaxis preferred (sequential compression, mobilization)
    - **Monitoring Strategy**: Daily reassessment for risk factor changes
    - **Cost-Effectiveness**: Avoids unnecessary pharmacological prophylaxis
    - **Patient Safety**: Minimizes bleeding risks and injection burden
    
    **High Risk Management (≥3 points)**:
    - **VTE Incidence**: 3.2% three-month VTE rate warranting intervention
    - **Prophylaxis Options**: LMWH, UFH, or fondaparinux based on clinical factors
    - **Dosing Considerations**: Adjust for renal function, weight, and bleeding risk
    - **Duration**: Throughout hospitalization with consideration for extended prophylaxis
    - **Monitoring**: Daily assessment for efficacy and safety
    
    **Special Clinical Considerations**:
    
    **Contraindication Assessment**:
    - Active bleeding, severe thrombocytopenia, high bleeding risk procedures
    - Alternative mechanical prophylaxis when anticoagulation contraindicated
    - Individual risk-benefit analysis for complex patients
    
    **Quality Improvement Applications**:
    - Hospital VTE prevention protocols and order sets
    - Performance metrics for appropriate prophylaxis utilization
    - Clinical decision support system integration
    - Educational tool for training and standardization
    
    **Integration with Clinical Workflow**:
    - Assessment at admission and daily during hospitalization
    - Documentation of risk factors and prophylaxis decisions
    - Communication with patients and families about VTE prevention
    - Coordination with pharmacy and nursing for implementation
    
    **Research and Validation Context**:
    
    **ESTIMATE Trial Findings**:
    - 1,478 hospitalized medical patients enrolled across multiple centers
    - 43% of patients did not receive thromboprophylaxis, allowing natural history assessment
    - Geneva Risk Score demonstrated superior discrimination compared to clinical judgment
    - Validated threshold of ≥3 points optimally balanced sensitivity and specificity
    
    **Comparative Performance**:
    - Superior to Padua Prediction Score for identifying low-risk patients
    - Better negative likelihood ratio (0.28 vs 0.51) for ruling out VTE risk
    - More effective at reducing unnecessary anticoagulation in low-risk patients
    - Comparable positive predictive value for identifying high-risk patients
    
    **Clinical Implementation Evidence**:
    - Successful integration into hospital VTE prevention protocols
    - Reduction in inappropriate prophylaxis utilization
    - Maintained VTE prevention efficacy while improving safety
    - Cost savings through optimized prophylaxis targeting
    
    Args:
        request: Patient clinical risk factors including major conditions (cardiac failure, 
                respiratory failure, malignancy, infection) and minor factors (age, mobility, 
                obesity) required for Geneva VTE Risk Score calculation
        
    Returns:
        GenevaVteProphylaxisResponse: Geneva VTE Risk Score with detailed risk factor 
                                     analysis, evidence-based thromboprophylaxis 
                                     recommendations, and clinical management guidance 
                                     based on validated risk stratification thresholds
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("geneva_vte_prophylaxis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Geneva VTE Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GenevaVteProphylaxisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Geneva VTE Risk Score calculation",
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
                "message": "Internal error in Geneva VTE Risk Score calculation",
                "details": {"error": str(e)}
            }
        )