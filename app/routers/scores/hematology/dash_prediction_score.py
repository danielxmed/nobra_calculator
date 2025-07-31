"""
DASH Prediction Score for Recurrent VTE Router

Endpoint for calculating DASH prediction score for VTE recurrence risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.dash_prediction_score import (
    DashPredictionScoreRequest,
    DashPredictionScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dash_prediction_score",
    response_model=DashPredictionScoreResponse,
    summary="Calculate DASH Prediction Score for Recurrent VTE",
    description="Predicts likelihood of recurrence of first unprovoked venous thromboembolism (VTE) to guide anticoagulation duration decisions. Utilizes D-dimer, Age, Sex, and Hormonal therapy factors.",
    response_description="The calculated dash prediction score with interpretation",
    operation_id="dash_prediction_score"
)
async def calculate_dash_prediction_score(request: DashPredictionScoreRequest):
    """
    Calculates DASH Prediction Score for Recurrent VTE
    
    The DASH (D-dimer, Age, Sex, Hormonal therapy) prediction score is a validated 
    clinical decision tool that predicts the likelihood of recurrence of first 
    unprovoked venous thromboembolism (VTE) to guide anticoagulation duration decisions.
    
    **Clinical Background and Development:**
    
    The DASH score was developed through rigorous research involving 1,818 patients 
    with first unprovoked VTE from multiple prospective cohort studies. The tool 
    addresses one of the most challenging clinical decisions in hematology and 
    thrombosis medicine: determining the optimal duration of anticoagulation therapy 
    after first unprovoked VTE.
    
    **Evidence Base and Validation:**
    
    **Original Development:**
    The score was derived from analysis of 1,818 cases of first unprovoked VTE, 
    with validation in independent cohorts. The model demonstrated good discrimination 
    (c-statistic 0.66) and calibration across diverse populations and clinical settings.
    
    **External Validation Studies:**
    Multiple subsequent studies have validated the DASH score across different 
    populations, healthcare systems, and anticoagulant types, confirming its 
    utility in clinical practice and research settings.
    
    **Clinical Utility Research:**
    Studies have demonstrated that DASH score implementation:
    - Improves standardization of anticoagulation duration decisions
    - Reduces practice variation in VTE management
    - Facilitates shared decision-making between patients and providers
    - Supports evidence-based anticoagulation stewardship
    
    **Scoring System and Components:**
    
    **D-dimer (Post-anticoagulation):**
    - Positive: +2 points
    - Negative: 0 points
    
    The D-dimer measurement should be obtained approximately 1 month after 
    discontinuing anticoagulation therapy. Persistently elevated D-dimer indicates 
    ongoing activation of the coagulation system and increased thrombotic risk.
    
    **Age:**
    - ≤50 years: +1 point
    - >50 years: 0 points
    
    Younger age paradoxically increases recurrence risk, likely due to longer 
    life expectancy for exposure to recurrent events and fewer age-related 
    comorbidities that might otherwise limit anticoagulation use.
    
    **Sex:**
    - Male: +1 point
    - Female: 0 points
    
    Male sex is associated with higher VTE recurrence risk across multiple studies, 
    with approximately 1.5-2 fold higher annual recurrence rates compared to women.
    
    **Hormonal Therapy (Women Only):**
    - Yes (at time of initial VTE): -2 points
    - No: 0 points
    - Not applicable (men): 0 points
    
    If the initial VTE occurred during hormonal therapy use (oral contraceptives, 
    hormone replacement therapy), the thrombotic risk was likely influenced by 
    the exogenous hormone exposure, reducing intrinsic thrombotic tendency.
    
    **Risk Stratification and Annual Recurrence Rates:**
    
    **Low Risk (-2 to 1 points): 3.1% Annual Recurrence (95% CI 2.3-3.9%)**
    
    **Clinical Significance:**
    Patients in this category have relatively low risk of VTE recurrence, making 
    anticoagulation discontinuation after 3-6 months of initial therapy a reasonable 
    approach for most patients, assuming bleeding risk is not significantly elevated.
    
    **Management Approach:**
    - Standard 3-6 month anticoagulation course is typically sufficient
    - Bleeding risk assessment is important for final decision-making
    - Patient education about VTE symptoms and risk factor modification
    - Regular follow-up for risk reassessment and symptom monitoring
    
    **Intermediate Risk (2 points): 6.4% Annual Recurrence (95% CI 4.8-7.9%)**
    
    **Clinical Significance:**
    This category represents patients where the decision about anticoagulation 
    duration requires careful individualization, weighing thrombotic risk against 
    bleeding risk and incorporating patient values and preferences.
    
    **Management Approach:**
    - Detailed bleeding risk assessment using validated tools (HAS-BLED, HEMORR2HAGES)
    - Comprehensive discussion of risks and benefits with patient
    - Consider patient quality of life factors and treatment preferences
    - May consider extended anticoagulation (6-12 months) with periodic reassessment
    - Shared decision-making is crucial in this risk category
    
    **High Risk (3-6 points): 12.3% Annual Recurrence (95% CI 9.9-14.7%)**
    
    **Clinical Significance:**
    Patients in this category have substantial risk of VTE recurrence, warranting 
    strong consideration for prolonged or indefinite anticoagulation therapy if 
    bleeding risk is acceptable.
    
    **Management Approach:**
    - Prolonged anticoagulation is generally recommended
    - Consider indefinite anticoagulation if bleeding risk is low to moderate
    - Regular monitoring for bleeding complications and drug interactions
    - Periodic reassessment of risk-benefit ratio (annually)
    - Consider newer anticoagulants with improved safety profiles
    
    **Clinical Decision Support Framework:**
    
    **Risk-Benefit Assessment:**
    The DASH score provides quantitative risk assessment that should be integrated 
    with bleeding risk evaluation, patient preferences, and clinical circumstances. 
    Major bleeding risk (typically 1-3% annually) should be weighed against 
    thrombotic recurrence risk for optimal decision-making.
    
    **Shared Decision-Making:**
    - Present quantitative risks in understandable formats
    - Explore patient values regarding risk tolerance and quality of life
    - Discuss lifestyle factors that might influence risk-benefit balance
    - Plan for regular reassessment as circumstances change
    
    **Special Considerations:**
    
    **Age >65 Years:**
    External validation studies have noted that patients >65 years may have higher 
    recurrence risk than predicted by DASH score alone, warranting consideration 
    of more conservative anticoagulation approaches even with low DASH scores.
    
    **VTE Type:**
    While not part of the DASH scoring system, pulmonary embolism may be associated 
    with different risk profiles compared to isolated deep vein thrombosis, and 
    this should be considered in clinical decision-making.
    
    **Bleeding Risk Assessment:**
    The DASH score should always be used in conjunction with bleeding risk 
    assessment tools such as HAS-BLED or HEMORR2HAGES to provide comprehensive 
    risk evaluation for anticoagulation decisions.
    
    **Patient Education and Counseling:**
    
    **Risk Communication:**
    Effective communication of quantitative risk is crucial for shared decision-making. 
    Visual aids, natural frequencies, and patient-friendly materials can improve 
    understanding and engagement in decision-making.
    
    **Lifestyle Counseling:**
    - VTE risk factor modification (weight management, mobility, hydration)
    - Recognition of VTE symptoms and when to seek medical attention
    - Travel precautions and mechanical prophylaxis strategies
    - Importance of medication adherence if continuing anticoagulation
    
    **Implementation Considerations:**
    
    **Clinical Integration:**
    The DASH score can be integrated into electronic health records, clinical 
    decision support systems, and anticoagulation clinic protocols to standardize 
    and improve VTE management decision-making.
    
    **Quality Improvement:**
    DASH score implementation can support quality improvement initiatives in VTE 
    management, reducing practice variation and improving evidence-based care.
    
    **Limitations and Considerations:**
    
    **Score Limitations:**
    - Moderate discriminative ability (c-statistic 0.66)
    - Does not capture all relevant risk factors for VTE recurrence
    - Developed primarily in populations treated with vitamin K antagonists
    - May not fully account for individual patient factors or comorbidities
    
    **Clinical Judgment:**
    The DASH score should supplement rather than replace clinical judgment, and 
    individual patient factors not captured by the score should be considered 
    in final decision-making.
    
    **Regular Reassessment:**
    Patient risk factors and circumstances may change over time, necessitating 
    regular reassessment of both thrombotic and bleeding risk for optimal 
    long-term management.
    
    Args:
        request: DASH prediction parameters including D-dimer result, age, sex, 
                and hormonal therapy status, with optional VTE type and 
                anticoagulation duration for clinical context
        
    Returns:
        DashPredictionScoreResponse: Comprehensive risk assessment including DASH 
        score, annual recurrence risk, risk category classification, anticoagulation 
        recommendations, and clinical decision support guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dash_prediction_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DASH Prediction Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DashPredictionScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DASH Prediction Score",
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