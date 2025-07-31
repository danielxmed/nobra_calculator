"""
EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope Router

Endpoint for calculating EGSYS cardiac syncope risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.egsys_score_syncope import (
    EgsysScoreSyncopeRequest,
    EgsysScoreSyncopeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/egsys_score_syncope",
    response_model=EgsysScoreSyncopeResponse,
    summary="Calculate EGSYS (Evaluation of Guidelines in SY...",
    description="Predicts likelihood that syncope is of cardiac cause to help emergency clinicians with screening and risk stratification in patients presenting with syncope.",
    response_description="The calculated egsys score syncope with interpretation",
    operation_id="egsys_score_syncope"
)
async def calculate_egsys_score_syncope(request: EgsysScoreSyncopeRequest):
    """
    Calculates EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope
    
    The EGSYS score is a validated clinical decision tool that predicts the likelihood of 
    cardiac syncope in emergency department patients. It helps clinicians distinguish between 
    cardiac and non-cardiac causes of syncope, guiding appropriate risk stratification and 
    management decisions.
    
    Clinical Background and Importance:
    
    Syncope is a common presenting complaint in emergency departments, accounting for 1-3% of 
    all visits. The clinical challenge lies in differentiating between benign causes (such as 
    vasovagal syncope) and potentially life-threatening cardiac causes that require immediate 
    evaluation and treatment.
    
    The EGSYS score addresses this challenge by providing a standardized, evidence-based 
    approach to syncope risk stratification. It was developed through analysis of 516 patients 
    across multiple European centers and has been validated in numerous subsequent studies.
    
    Key Clinical Applications:
    
    Emergency Department Risk Stratification:
    - Primary tool for initial syncope evaluation
    - Helps identify patients requiring immediate cardiac workup
    - Guides admission versus discharge decisions
    - Supports resource allocation and care pathway decisions
    
    Clinical Decision Support:
    - High negative predictive value (99%) for excluding cardiac causes
    - Sensitivity of 95% for detecting cardiac syncope
    - Validated cut-off of ≥3 points for high-risk classification
    - Long-term prognostic value for mortality prediction
    
    Healthcare System Benefits:
    - Standardizes syncope evaluation protocols
    - Reduces unnecessary admissions for low-risk patients
    - Ensures appropriate workup for high-risk patients
    - Improves resource utilization and cost-effectiveness
    
    Scoring System and Clinical Variables:
    
    The EGSYS score evaluates six clinical variables with point values ranging from -1 to +4:
    
    Positive Predictors (Favor Cardiac Etiology):
    1. Abnormal EKG and/or Heart Disease (+3 points)
       - Any EKG abnormality or known cardiac condition
       - Strong predictor of underlying cardiac substrate
       - Includes structural and electrical abnormalities
    
    2. Palpitations Before Syncope (+4 points)
       - Strongest individual predictor in the model
       - Suggests arrhythmic etiology preceding loss of consciousness
       - Reported as rapid, irregular, or forceful heartbeats
    
    3. Syncope During Effort (+3 points)
       - Classic presentation of exercise-induced cardiac syncope
       - Associated with structural heart disease or arrhythmias
       - Excludes effort-related vasovagal responses
    
    4. Syncope in Supine Position (+2 points)
       - Unusual for typical vasovagal syncope
       - More consistent with arrhythmic causes
       - Eliminates gravitational component
    
    Negative Predictors (Favor Non-Cardiac Etiology):
    5. Autonomic Prodromes (-1 point)
       - Classic vasovagal warning symptoms
       - Includes nausea, vomiting, diaphoresis
       - Suggests intact autonomic nervous system response
    
    6. Precipitating/Predisposing Factors (-1 point)
       - Identifiable triggers for neurally-mediated syncope
       - Includes emotional stress, pain, prolonged standing
       - Situational syncope triggers
    
    Score Interpretation and Management:
    
    High Risk (Score ≥3 points) - Cardiac Syncope Likely:
    - 95% sensitivity for cardiac syncope detection
    - 17% mortality risk at 21-24 months
    - Management approach:
      * Consider hospital admission for diagnostic confirmation
      * Urgent cardiology consultation
      * Continuous cardiac monitoring (telemetry)
      * Comprehensive cardiac evaluation including echocardiogram
      * Extended cardiac monitoring (Holter, event monitor)
      * Electrophysiology study consideration if indicated
    
    Low Risk (Score <3 points) - Cardiac Syncope Less Likely:
    - 99% negative predictive value for cardiac syncope
    - 3% mortality risk at 21-24 months
    - Management approach:
      * Outpatient evaluation appropriate for stable patients
      * Focus on non-cardiac causes (vasovagal, orthostatic, medication-related)
      * Basic cardiac assessment (EKG, basic metabolic panel)
      * Primary care follow-up with clear return precautions
      * Safety netting with patient education
    
    Validation and Performance:
    
    The EGSYS score has demonstrated consistent performance across multiple studies:
    - Original validation in 516 patients across European centers
    - Subsequent validation in diverse international populations
    - Sensitivity: 86-95% for cardiac syncope detection
    - Specificity: 57-68% for excluding non-cardiac causes
    - Area under ROC curve: 0.80-0.82 in validation studies
    - Long-term mortality data supporting prognostic value
    
    Implementation Considerations:
    
    Best Practices:
    - Use as part of comprehensive syncope evaluation
    - Combine with clinical judgment and other risk factors
    - Ensure proper staff training on score calculation and interpretation
    - Integrate with local cardiology resources and availability
    - Document decision-making rationale clearly
    
    Limitations:
    - Designed for emergency department screening, not definitive diagnosis
    - Should complement, not replace, clinical assessment
    - Performance may vary in different patient populations
    - Less useful in outpatient settings with pre-selected patients
    - Some high-risk features may warrant admission regardless of score
    
    Quality Improvement Applications:
    
    Healthcare systems can leverage EGSYS for:
    - Standardizing syncope evaluation protocols
    - Developing clinical pathways and decision trees
    - Training emergency department staff
    - Quality metrics and performance monitoring
    - Reducing practice variation and improving consistency
    - Supporting evidence-based medicine initiatives
    
    Comparison with Other Syncope Risk Scores:
    
    Alternative validated tools include:
    - San Francisco Syncope Rule (potentially more reliable per some experts)
    - Canadian Syncope Risk Score
    - ROSE (Risk stratification Of Syncope in the Emergency department) rule
    - Boston Syncope Criteria
    
    Each tool has specific strengths and may be preferred in different clinical contexts 
    or healthcare systems based on local validation and implementation experience.
    
    Patient Safety and Communication:
    
    Key safety considerations:
    - Clear communication of risk level to patients and families
    - Appropriate return precautions for all patients
    - Documentation of shared decision-making
    - Follow-up arrangements based on risk level
    - Patient education about warning signs and symptoms
    
    Long-term Outcomes and Prognosis:
    
    The EGSYS score provides valuable prognostic information:
    - Patients with scores ≥3 have significantly higher mortality
    - Score correlates with need for cardiac interventions
    - Long-term follow-up studies support sustained prognostic value
    - Helps identify patients requiring more intensive monitoring
    
    Integration with Clinical Guidelines:
    
    The EGSYS score aligns with major syncope management guidelines:
    - European Society of Cardiology (ESC) syncope guidelines
    - American Heart Association/American College of Cardiology statements
    - Emergency medicine society recommendations
    - Supports evidence-based approach to syncope evaluation
    
    Args:
        request: EGSYS assessment parameters for six clinical variables
        
    Returns:
        EgsysScoreSyncopeResponse: Risk score with cardiac syncope likelihood and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("egsys_score_syncope", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EGSYS Score for Syncope",
                    "details": {"parameters": parameters}
                }
            )
        
        return EgsysScoreSyncopeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EGSYS Score for Syncope",
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