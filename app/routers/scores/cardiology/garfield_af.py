"""
GARFIELD-AF Risk Score Router

Endpoint for calculating GARFIELD-AF risk score for atrial fibrillation patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.garfield_af import (
    GarfieldAfRequest,
    GarfieldAfResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/garfield_af",
    response_model=GarfieldAfResponse,
    summary="Calculate GARFIELD-AF Risk Score",
    description="The GARFIELD-AF risk score simultaneously predicts 1- and 2-year risks of mortality, ischemic stroke/systemic embolism, and major bleeding in patients with atrial fibrillation. This contemporary risk stratification tool incorporates 16 clinical variables and has been validated across diverse international populations with both anticoagulated and non-anticoagulated patients.",
    response_description="The calculated garfield af with interpretation",
    operation_id="calculate_garfield_af"
)
async def calculate_garfield_af(request: GarfieldAfRequest):
    """
    Calculates GARFIELD-AF Risk Score for Atrial Fibrillation Patients
    
    The GARFIELD-AF risk score simultaneously predicts 1- and 2-year risks of mortality, 
    ischemic stroke/systemic embolism, and major bleeding in patients with atrial fibrillation. 
    This contemporary, evidence-based tool supports individualized anticoagulation decisions 
    by providing integrated multi-outcome risk assessment.
    
    **Clinical Context and Applications**:
    
    **Primary Purpose**: 
    Comprehensive risk stratification for patients with atrial fibrillation requiring 
    anticoagulation decision-making support.
    
    **Key Advantages over Traditional Single-Outcome Scores**:
    - **Integrated Assessment**: Simultaneously predicts mortality, stroke/SE, and bleeding
    - **Contemporary Derivation**: Based on modern AF management and patient populations
    - **International Validation**: Validated across 35 countries with diverse populations
    - **Dual Time Horizons**: Provides both 1-year and 2-year risk predictions
    - **Comprehensive Variables**: Uses 16 readily available clinical parameters
    - **Evidence-Based**: Derived from >52,000 patients in GARFIELD-AF registry
    
    **Clinical Decision Support Framework**:
    
    **Risk Stratification Categories**:
    - **Low Risk (<2% max annual risk)**: Standard management approach
    - **Moderate Risk (2-5% max annual risk)**: Individualized approach with careful monitoring
    - **High Risk (>5% max annual risk)**: Intensive monitoring and specialist consultation
    
    **Anticoagulation Decision Integration**:
    
    **Balanced Risk Profile** (Similar stroke and bleeding risks):
    - Emphasize patient preferences and quality of life considerations
    - Consider alternative strategies (rhythm control, lifestyle modification)
    - Regular reassessment as risk profile may change over time
    
    **High Stroke, Low Bleeding Risk**:
    - Strong indication for anticoagulation
    - Standard dosing and monitoring approaches
    - Focus on adherence optimization and stroke prevention
    
    **High Stroke, High Bleeding Risk**:
    - Complex decision requiring specialist input
    - Consider alternative strategies: reduced-dose anticoagulation, LAAO
    - Intensive monitoring with frequent reassessment
    - Multidisciplinary approach (cardiology, hematology)
    
    **Low Stroke, High Bleeding Risk**:
    - Anticoagulation may not provide net clinical benefit
    - Focus on rhythm control and lifestyle interventions
    - Monitor for changes in stroke risk over time
    
    **Multi-Outcome Risk Interpretation**:
    
    **Mortality Risk Assessment**:
    - **Low (<2%)**: Good prognosis, focus on stroke prevention and quality of life
    - **Intermediate (2-8%)**: Balance aggressive treatment with potential risks
    - **High (>8%)**: Limited prognosis, consider goals of care and comfort focus
    
    **Stroke/Systemic Embolism Risk Assessment**:
    - **Low (<1%)**: Minimal stroke risk, anticoagulation benefit may be limited
    - **Intermediate (1-4%)**: Clear benefit from anticoagulation if bleeding risk acceptable
    - **High (>4%)**: Strong indication for anticoagulation unless major contraindications
    
    **Major Bleeding Risk Assessment**:
    - **Low (<1%)**: Minimal bleeding concern, standard anticoagulation approach
    - **Intermediate (1-3%)**: Careful monitoring, consider bleeding risk reduction strategies
    - **High (>3%)**: Major bleeding concern, consider alternatives or intensive monitoring
    
    **Clinical Workflow Integration**:
    
    **Initial Assessment**:
    1. Calculate baseline GARFIELD-AF scores for all three outcomes
    2. Identify highest risk category to guide overall management approach
    3. Discuss individualized risks and benefits with patient
    4. Consider patient preferences, functional status, and life expectancy
    5. Make shared decision about anticoagulation strategy
    
    **Ongoing Management**:
    1. Reassess scores annually or with significant clinical changes
    2. Monitor for medication adherence and side effects
    3. Adjust management based on changing risk profile
    4. Consider specialist referral for high-risk or complex cases
    
    **Quality Improvement Applications**:
    - **Population Health**: Risk stratification for AF management programs
    - **Clinical Pathways**: Standardized approaches based on risk categories
    - **Performance Metrics**: Outcomes tracking and quality improvement initiatives
    - **Patient Safety**: Bleeding event prevention and monitoring protocols
    
    **Research and Clinical Trial Applications**:
    - **Patient Stratification**: Enroll appropriate risk groups for studies
    - **Endpoint Prediction**: Estimate event rates for power calculations
    - **Comparative Effectiveness**: Evaluate interventions across risk strata
    - **Real-World Evidence**: Monitor outcomes in clinical practice
    
    **Limitations and Considerations**:
    - **Dynamic Risk**: Risks change over time with aging and comorbidity evolution
    - **Individual Variation**: Population-based predictions may not apply to individuals
    - **Clinical Context**: Should supplement, not replace, clinical judgment
    - **Treatment Effects**: Scores predict untreated risks; treatment modifies outcomes
    
    Args:
        request: Patient clinical data including demographics, vital signs, comorbidities, 
                and medication history required for GARFIELD-AF risk calculation
        
    Returns:
        GarfieldAfResponse: Comprehensive risk predictions for mortality, stroke/systemic 
                           embolism, and major bleeding at 1 and 2 years with integrated 
                           clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("garfield_af", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GARFIELD-AF Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GarfieldAfResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GARFIELD-AF calculation",
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
                "message": "Internal error in GARFIELD-AF calculation",
                "details": {"error": str(e)}
            }
        )