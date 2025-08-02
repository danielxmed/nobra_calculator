"""
Marburg Heart Score (MHS) Router

Endpoint for calculating Marburg Heart Score for CAD risk assessment in primary care.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.marburg_heart_score import (
    MarburgHeartScoreRequest,
    MarburgHeartScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/marburg_heart_score",
    response_model=MarburgHeartScoreResponse,
    summary="Calculate Marburg Heart Score (MHS)",
    description="Calculates the Marburg Heart Score for ruling out coronary artery disease "
                "in primary care patients aged 35 years and older presenting with chest pain. "
                "This validated clinical prediction rule uses five equally weighted criteria "
                "to stratify patients into low-risk (score 0-2, ~3% CAD risk) or higher-risk "
                "(score ≥3, ~23% CAD risk) categories. The score demonstrated 87.1% sensitivity "
                "and 80.8% specificity for CAD detection, helping primary care physicians make "
                "evidence-based decisions about urgent referral versus outpatient management. "
                "Designed specifically for primary care settings to reduce unnecessary urgent "
                "evaluations while maintaining diagnostic safety. The tool evaluates age/sex "
                "criteria, known vascular disease history, exercise-related pain patterns, "
                "pain reproducibility with palpation, and patient's clinical intuition about "
                "cardiac origin. NOT recommended for emergency department use or as a positive "
                "diagnostic tool for CAD.",
    response_description="The calculated Marburg Heart Score with risk stratification, CAD probability estimates, and comprehensive management recommendations",
    operation_id="marburg_heart_score"
)
async def calculate_marburg_heart_score(request: MarburgHeartScoreRequest):
    """
    Calculates Marburg Heart Score for Coronary Artery Disease Risk Assessment
    
    The Marburg Heart Score (MHS) is a validated clinical prediction rule developed 
    specifically for primary care physicians to rule out coronary artery disease (CAD) 
    in patients aged 35 years and older presenting with chest pain.
    
    **Five Clinical Criteria (1 point each):**
    
    1. **Age/Sex Criteria**: Female ≥65 years OR Male ≥55 years
       - Based on established cardiovascular risk epidemiology
       - Reflects age-related and sex-specific CAD risk patterns
       - Critical threshold where CAD risk significantly increases
    
    2. **Known Vascular Disease**: History of CAD, cerebrovascular disease, or PVD
       - Previous vascular disease strongly predicts additional CAD
       - Indicates systemic atherosclerotic disease process
       - Includes prior MI, stroke, or peripheral arterial disease
    
    3. **Exercise-Related Pain**: Chest pain worsens with physical exercise
       - Classic feature of angina pectoris
       - Reflects supply-demand mismatch during increased oxygen needs
       - Strong predictor of obstructive coronary disease
    
    4. **Non-Reproducible Pain**: Pain is NOT reproducible with palpation
       - Distinguishes cardiac from musculoskeletal chest pain
       - Reproducible pain typically indicates chest wall etiology
       - Non-reproducible pain more likely visceral/cardiac origin
    
    5. **Patient's Clinical Intuition**: Patient assumes pain is cardiac
       - Patient's subjective assessment has demonstrated diagnostic value
       - Reflects patient's awareness of symptom characteristics
       - Important component of clinical history assessment
    
    **Risk Stratification and Management:**
    
    **Low Risk (0-2 points):**
    - **CAD Probability**: Approximately 3%
    - **Clinical Significance**: Highly unlikely to have unstable CAD
    - **Management Approach**: Outpatient evaluation as clinically indicated
    - **Follow-up Strategy**: 
      - Routine primary care follow-up
      - Cardiovascular risk factor assessment and modification
      - Patient education about symptoms and return precautions
      - Lifestyle counseling for cardiovascular health
    - **Diagnostic Value**: Strong negative predictive value for CAD
    
    **Higher Risk (≥3 points):**
    - **CAD Probability**: Approximately 23%
    - **Clinical Significance**: Warrants urgent cardiac evaluation
    - **Management Approach**: Consider urgent evaluation or inpatient admission
    - **Recommended Evaluation**:
      - 12-lead electrocardiogram (ECG)
      - Cardiac biomarkers (troponin I/T)
      - Chest X-ray
      - Consider stress testing or coronary imaging
      - Cardiology consultation as appropriate
    - **Important Note**: Modest positive predictive value emphasizes need for 
      comprehensive evaluation rather than assumption of CAD presence
    
    **Clinical Applications:**
    - **Primary Care Decision Support**: Structured approach to chest pain evaluation
    - **Referral Guidance**: Evidence-based criteria for urgent vs. routine referral
    - **Resource Optimization**: Reduces unnecessary urgent evaluations
    - **Patient Safety**: Maintains diagnostic sensitivity while improving specificity
    - **Quality Improvement**: Standardizes chest pain risk assessment
    
    **Validation and Performance:**
    - **Development**: 1,249 patients across 74 German primary care practices
    - **Sensitivity**: 87.1% for detecting CAD
    - **Specificity**: 80.8% for ruling out CAD
    - **Area Under the Curve**: 0.87 (derivation), 0.90 (validation)
    - **External Validation**: Confirmed in multiple international studies
    - **Clinical Impact**: Demonstrated reduction in unnecessary referrals
    
    **Important Limitations and Considerations:**
    - **Target Population**: Primary care patients ≥35 years with chest pain
    - **Setting Limitations**: NOT validated for emergency department use
    - **Diagnostic Purpose**: Risk stratification tool, NOT diagnostic test
    - **Clinical Judgment**: Should supplement, not replace, clinical assessment
    - **Alternative Diagnoses**: Not for patients with obvious non-cardiac causes
    - **Known CAD**: Not recommended for patients with established CAD
    - **Context Dependency**: Consider patient presentation and clinical stability
    
    **Implementation Best Practices:**
    - Integrate with comprehensive clinical history and examination
    - Consider patient preferences and values in management decisions
    - Account for comorbidities and functional status
    - Maintain awareness of score limitations and appropriate context
    - Use for shared decision-making with patients about evaluation approach
    - Regular reassessment based on symptom evolution or new information
    
    **Quality Assurance:**
    - Validated performance across diverse primary care populations
    - Consistent results across different healthcare systems
    - Integration with electronic health records and clinical decision support
    - Ongoing research for score refinement and validation
    
    **References:**
    1. Bösner S, Haasenritter J, Becker A, et al. Ruling out coronary artery disease 
       in primary care: development and validation of a simple prediction rule. 
       CMAJ. 2010;182(12):1295-300.
    2. Haasenritter J, Bösner S, Vaucher P, et al. Ruling out coronary heart disease 
       in primary care: external validation of a clinical prediction rule. 
       Br J Gen Pract. 2012;62(599):e415-21.
    3. Harskamp RE, Laeven SC, Himmelreich JC, et al. Chest pain in general practice: 
       a systematic review of prediction rules. BMJ Open. 2019;9(2):e027081.
    
    Args:
        request: Marburg Heart Score parameters including five clinical criteria
        
    Returns:
        MarburgHeartScoreResponse: Calculated score with risk stratification, 
        CAD probability, and comprehensive management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("marburg_heart_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Marburg Heart Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MarburgHeartScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Marburg Heart Score",
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