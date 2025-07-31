"""
CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk Router

Endpoint for calculating CHA₂DS₂-VA Score for stroke risk assessment in atrial fibrillation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.cha2ds2_va_score import (
    Cha2ds2VaScoreRequest,
    Cha2ds2VaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cha2ds2_va_score",
    response_model=Cha2ds2VaScoreResponse,
    summary="Calculate CHA₂DS₂-VA Score for Atrial Fibrillat...",
    description="Calculates stroke risk for patients with atrial fibrillation; similar to CHA₂DS₂-VASc Score but without considering sex. Simplified version recommended in 2024 ESC guidelines to remove complexity of gender-based scoring.",
    response_description="The calculated cha2ds2 va score with interpretation",
    operation_id="calculate_cha2ds2_va_score"
)
async def calculate_cha2ds2_va_score(request: Cha2ds2VaScoreRequest):
    """
    Calculates CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk Assessment
    
    The CHA₂DS₂-VA Score is a simplified stroke risk assessment tool for atrial fibrillation 
    that removes female sex as a risk factor, introduced in the 2024 ESC guidelines. This 
    modification addresses clinical complexity while maintaining comparable predictive 
    performance to the original CHA₂DS₂-VASc score.
    
    **Background and Development**:
    
    **Historical Context**:
    - Evolution from CHADS₂ (2001) → CHA₂DS₂-VASc (2010) → CHA₂DS₂-VA (2024)
    - Original CHA₂DS₂-VASc included female sex based on early epidemiological data
    - Contemporary evidence shows female sex as age-dependent rather than independent risk factor
    - 2024 ESC guidelines recommend CHA₂DS₂-VA to simplify clinical practice
    
    **Rationale for Removing Female Sex**:
    - Incremental stroke risk in women has decreased over time (2007-2018)
    - Female sex risk becomes non-significant in recent cohorts
    - Simplifies clinical decision-making for healthcare providers and patients
    - Improves inclusivity for non-binary, transgender, and gender-diverse individuals
    - Removes potential gender bias in anticoagulation decisions
    
    **Clinical Performance**:
    - Discrimination ability comparable to CHA₂DS₂-VASc score
    - Maintains accuracy for identifying truly low-risk patients
    - No significant impact on thromboembolic event prediction
    - Validated across multiple contemporary atrial fibrillation cohorts
    
    **CHA₂DS₂-VA Scoring System**:
    
    **Age Component (Progressive Risk)**:
    
    **Age <65 years (0 points)**:
    - Baseline stroke risk category
    - Lower threshold for considering anticoagulation
    - Individual risk factors more influential
    
    **Age 65-74 years (1 point)**:
    - Moderate age-related stroke risk
    - Intermediate risk requiring clinical judgment
    - Consider comorbidities and patient preferences
    
    **Age ≥75 years (2 points)**:
    - High age-related stroke risk
    - Strong indication for anticoagulation
    - Maximum age adjustment in scoring system
    
    **Clinical Risk Factors (1 point each)**:
    
    **C - Congestive Heart Failure**:
    - Clinical syndrome of heart failure (systolic or diastolic)
    - Left ventricular dysfunction on echocardiography
    - History of heart failure hospitalization
    - Current or prior heart failure medications
    - Associated with increased stroke risk due to cardiac remodeling
    
    **H - Hypertension**:
    - Diagnosed hypertension by healthcare provider
    - Blood pressure ≥140/90 mmHg on repeated measurements
    - Current use of antihypertensive medications
    - Well-controlled hypertension on treatment counts
    - Major modifiable stroke risk factor
    
    **D - Diabetes Mellitus**:
    - Type 1 or Type 2 diabetes mellitus
    - Fasting glucose ≥126 mg/dL or HbA1c ≥6.5%
    - Current antidiabetic medication use
    - Diet-controlled diabetes qualifies
    - Associated with accelerated atherosclerosis
    
    **V - Vascular Disease**:
    - Myocardial infarction (current or historical)
    - Peripheral artery disease with symptoms or intervention
    - Complex aortic plaque or atherosclerotic disease
    - History of coronary, carotid, or peripheral revascularization
    - Reflects systemic atherothrombotic burden
    
    **High-Impact Risk Factor (2 points)**:
    
    **S₂ - Prior Stroke/TIA/Thromboembolism**:
    - Previous ischemic or hemorrhagic stroke
    - Transient ischemic attack with neurological symptoms
    - Arterial thromboembolism (excluding venous events)
    - Worth 2 points due to very high recurrence risk
    - Most powerful predictor of future stroke events
    
    **Risk Stratification and Clinical Decision-Making**:
    
    **Score 0 (Very Low Risk)**:
    - **Annual Stroke Rate**: 0.5 per 100 patient-years
    - **Recommendation**: No anticoagulation recommended
    - **Rationale**: Very low stroke risk does not justify bleeding risks
    - **Management**: Patient education, risk factor modification
    - **Follow-up**: Annual reassessment of stroke risk factors
    
    **Score 1 (Low-Moderate Risk)**:
    - **Annual Stroke Rate**: 1.5 per 100 patient-years
    - **Recommendation**: Clinical judgment required
    - **Considerations**: Patient preferences, bleeding risk, comorbidities
    - **Options**: Shared decision-making about anticoagulation vs observation
    - **Assessment**: HAS-BLED score, quality of life considerations
    
    **Score ≥2 (High Risk)**:
    - **Annual Stroke Rate**: 2.9-19.5 per 100 patient-years
    - **Recommendation**: Oral anticoagulation recommended
    - **Options**: DOACs preferred over warfarin for most patients
    - **Monitoring**: Regular assessment for efficacy and safety
    - **Duration**: Long-term anticoagulation unless contraindicated
    
    **Anticoagulation Management**:
    
    **Direct Oral Anticoagulants (DOACs) - First-Line**:
    
    **Dabigatran**:
    - Standard dose: 150 mg twice daily
    - Reduced dose: 110 mg twice daily (age ≥80, bleeding risk)
    - Renal adjustment: Avoid if CrCl <30 mL/min
    - Reversal agent: Idarucizumab available
    
    **Rivaroxaban**:
    - Standard dose: 20 mg once daily with food
    - Reduced dose: 15 mg daily if CrCl 30-49 mL/min
    - Avoid if CrCl <30 mL/min
    - Reversal: Andexanet alfa (limited availability)
    
    **Apixaban**:
    - Standard dose: 5 mg twice daily
    - Reduced dose: 2.5 mg twice daily if ≥2 criteria: age ≥80, weight ≤60kg, SCr ≥1.5 mg/dL
    - Safest renal profile, avoid if CrCl <25 mL/min
    - Reversal: Andexanet alfa (limited availability)
    
    **Edoxaban**:
    - Standard dose: 60 mg once daily
    - Reduced dose: 30 mg daily if CrCl 30-50, weight ≤60kg, concomitant P-gp inhibitors
    - Avoid if CrCl >95 mL/min (paradoxically reduced efficacy)
    - Less clinical experience than other DOACs
    
    **Warfarin (Alternative Option)**:
    - Target INR: 2.0-3.0
    - Requires regular INR monitoring
    - Significant drug and food interactions
    - Consider when DOACs contraindicated or unavailable
    - Time in therapeutic range >70% for optimal benefit
    
    **Clinical Implementation Framework**:
    
    **Initial Assessment**:
    1. Calculate CHA₂DS₂-VA score using current clinical status
    2. Assess bleeding risk using HAS-BLED or other validated tools
    3. Evaluate patient preferences and values
    4. Consider contraindications and drug interactions
    5. Discuss benefits and risks of anticoagulation
    
    **Shared Decision-Making Process**:
    - Present stroke risk in understandable terms
    - Explain anticoagulation options and monitoring requirements
    - Address patient concerns and misconceptions
    - Consider quality of life implications
    - Document rationale for treatment decisions
    
    **Ongoing Management**:
    - Reassess stroke risk at regular intervals
    - Monitor for bleeding complications
    - Assess medication adherence
    - Adjust therapy based on changes in clinical status
    - Consider drug interactions with new medications
    
    **Quality Improvement Applications**:
    - Standardized approach to AF stroke prevention
    - Performance metrics for appropriate anticoagulation
    - Population health management of AF patients
    - Clinical decision support integration
    - Outcome tracking and quality reporting
    
    **Advantages of CHA₂DS₂-VA Score**:
    - Simplified compared to CHA₂DS₂-VASc (removes sex complexity)
    - Gender-inclusive approach for diverse patient populations
    - Maintains predictive accuracy for stroke risk
    - Reduces clinical decision-making complexity
    - Aligns with contemporary understanding of stroke risk factors
    - Easier implementation in electronic health records
    
    **Clinical Considerations and Limitations**:
    - Apply only to nonvalvular atrial fibrillation
    - Consider individual patient factors beyond numerical score
    - Bleeding risk assessment equally important as stroke risk
    - Regular reassessment needed as conditions change
    - Score represents population-based risk, not individual certainty
    - Clinical judgment remains essential for optimal care
    
    This calculator provides evidence-based stroke risk assessment to support clinical 
    decision-making and anticoagulation management in atrial fibrillation patients, 
    incorporating the latest guideline recommendations for simplified and inclusive care.
    
    Args:
        request: CHA₂DS₂-VA score parameters for stroke risk assessment
        
    Returns:
        Cha2ds2VaScoreResponse: Score with stroke risk assessment and anticoagulation recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cha2ds2_va_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHA₂DS₂-VA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Cha2ds2VaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHA₂DS₂-VA Score",
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