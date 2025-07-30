"""
Current Opioid Misuse Measure (COMM) Router

Endpoint for calculating COMM opioid misuse risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.comm import (
    CommRequest,
    CommResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/comm", response_model=CommResponse)
async def calculate_comm(request: CommRequest):
    """
    Calculates Current Opioid Misuse Measure (COMM)
    
    The COMM is a validated self-report instrument designed to identify and monitor 
    opioid misuse in chronic pain patients taking prescription opioids for pain 
    management. This tool helps clinicians assess the risk of aberrant drug-related 
    behaviors and implement appropriate monitoring strategies.
    
    **Clinical Background:**
    
    Developed by Butler et al. in 2007, the COMM addresses the critical need for 
    reliable tools to identify opioid misuse in clinical practice. With the ongoing 
    opioid crisis, early identification of misuse behaviors is essential for patient 
    safety and appropriate pain management. The COMM provides a standardized, 
    evidence-based approach to this challenging clinical problem.
    
    **Assessment Methodology:**
    
    The COMM consists of 17 self-report questions evaluating behaviors over the 
    past 30 days. Each question is scored on a 5-point scale (0-4) based on frequency:
    
    **Scoring Scale:**
    - **0 = Never**: No occurrence of the behavior in the past 30 days
    - **1 = Seldom**: Rare occurrence, minimal frequency
    - **2 = Sometimes**: Occasional occurrence, moderate frequency
    - **3 = Often**: Frequent occurrence, regular pattern
    - **4 = Very often**: Very frequent occurrence, consistent pattern
    
    **Question Categories and Clinical Significance:**
    
    **Behavioral Indicators (5 questions):**
    These questions assess direct medication-related behaviors that suggest misuse:
    
    - **Taking medications differently than prescribed**: Deviation from prescribed regimen
    - **Taking more medication than prescribed**: Dose escalation beyond prescription
    - **Getting pain relief from other sources**: Seeking medications from multiple providers
    - **Needing medications from others**: Obtaining medications from friends/family
    - **Borrowing pain medication from others**: Acquiring medications from unauthorized sources
    
    **Psychological Indicators (6 questions):**
    These assess psychological and emotional factors associated with misuse:
    
    - **Trouble thinking clearly or memory problems**: Cognitive impairment from medication use
    - **Thoughts of self-harm**: Mental health concerns and risk assessment
    - **Time spent thinking about opioid medications**: Preoccupation and obsessive thoughts
    - **Being in arguments**: Interpersonal conflicts potentially related to medication use
    - **Trouble controlling anger**: Emotional dysregulation and irritability
    - **Getting angry with people**: Interpersonal aggression and mood changes
    
    **Functional Indicators (1 question):**
    - **Not completing necessary tasks**: Functional impairment affecting daily responsibilities
    
    **Healthcare Seeking Patterns (2 questions):**
    - **Emergency clinic calls/visits**: Urgent care seeking for pain or medication needs
    - **Emergency room visits**: Hospital utilization patterns that may indicate misuse
    
    **Substance-Related Concerns (3 questions):**
    - **Worried about handling medications**: Self-awareness of problematic medication use
    - **Others worried about medication handling**: External concern from family/friends
    - **Using pain medicine for non-pain symptoms**: Non-medical use of prescription opioids
    
    **Scoring and Interpretation:**
    
    **Total Score Calculation**: Sum of all 17 responses (range: 0-68 points)
    
    **Risk Thresholds:**
    - **Score < 9**: Low risk for opioid misuse, continue standard monitoring
    - **Score ≥ 9**: Elevated risk for opioid misuse, enhanced monitoring recommended
    
    **Performance Characteristics:**
    - **Sensitivity**: 47% (ability to identify true misuse cases)
    - **Specificity**: 89% (ability to correctly identify non-misuse cases)
    - **Area Under Curve**: 0.84 (good discriminative ability)
    - **Positive Predictive Value**: ~30% at cut-off score of 13
    - **Internal Consistency**: α = 0.86 (excellent reliability)
    - **Test-retest Reliability**: ICC = 0.86 (excellent stability)
    
    **Clinical Applications:**
    
    **Primary Care Settings:**
    - Routine screening of patients on long-term opioid therapy
    - Monitoring for development of aberrant behaviors
    - Clinical decision support for prescription management
    - Documentation for medical record and regulatory compliance
    
    **Pain Management Clinics:**
    - Comprehensive pain assessment and risk stratification
    - Treatment planning and goal setting
    - Monitoring treatment response and medication effects
    - Identifying patients needing additional support services
    
    **Specialty Care:**
    - Psychiatry: Assessment of comorbid substance use disorders
    - Emergency Medicine: Evaluation of patients seeking pain medications
    - Surgery: Preoperative risk assessment for opioid prescribing
    - Addiction Medicine: Screening and monitoring in treatment programs
    
    **Risk Stratification and Management:**
    
    **Low Risk (Score < 9):**
    - Continue standard pain management protocols
    - Routine monitoring with periodic COMM reassessment (every 3-6 months)
    - Standard opioid safety education and counseling
    - Regular assessment of pain control and functional improvement
    
    **Elevated Risk (Score ≥ 9):**
    - Enhanced monitoring with more frequent clinic visits
    - Consider urine drug testing and prescription monitoring programs
    - Pill counts and medication reconciliation
    - Evaluation for substance use disorder
    - Consider substance abuse or addiction medicine consultation
    - Review and potentially modify opioid treatment plan
    - Implement additional risk mitigation strategies
    
    **High-Risk Indicators and Red Flags:**
    
    **Immediate Concern Behaviors:**
    - Frequent dose escalation (taking more than prescribed ≥ often)
    - Obtaining medications from unauthorized sources (borrowing ≥ sometimes)
    - Using opioids for non-pain symptoms (≥ sometimes)
    - Thoughts of self-harm (any frequency > never)
    - Preoccupation with medications (thinking about opioids ≥ often)
    
    **Healthcare System Red Flags:**
    - Frequent emergency department visits for pain
    - Multiple provider shopping or "doctor shopping"
    - Lost or stolen prescription reports
    - Requests for early refills or specific medications
    - Aggressive or threatening behavior when questioned about medication use
    
    **Monitoring Strategies by Risk Level:**
    
    **Standard Monitoring (Score < 9):**
    - Clinical assessment every 3-6 months
    - COMM reassessment annually or as indicated
    - Pain and functional status evaluation
    - Medication effectiveness and side effect assessment
    
    **Enhanced Monitoring (Score 9-15):**
    - Clinical assessment every 1-2 months
    - COMM reassessment every 3-6 months
    - Consider urine drug testing (random or scheduled)
    - Prescription monitoring program review
    - Medication agreement and patient education reinforcement
    
    **Intensive Monitoring (Score > 15):**
    - Clinical assessment monthly or more frequently
    - COMM reassessment every 1-3 months
    - Regular urine drug testing and pill counts
    - Prescription monitoring program surveillance
    - Consider opioid dose reduction or alternative treatments
    - Subspecialty consultation (addiction medicine, psychiatry)
    
    **Clinical Decision Support:**
    
    **Prescribing Considerations:**
    - High COMM scores may indicate need for opioid dose reduction
    - Consider non-opioid alternatives or adjuvant therapies
    - Evaluate risk-benefit ratio of continued opioid therapy
    - Implement or modify opioid treatment agreements
    
    **Referral Indications:**
    - Score ≥ 9 with concerning clinical presentation
    - Multiple red flag behaviors or escalating scores
    - Patient or family concerns about medication dependence
    - Comorbid mental health or substance use disorders
    
    **Documentation and Legal Considerations:**
    
    **Medical Record Documentation:**
    - COMM scores and administration dates
    - Clinical interpretation and risk assessment
    - Monitoring plan and follow-up schedule
    - Patient education provided and response
    - Any interventions implemented based on results
    
    **Regulatory Compliance:**
    - Demonstrates due diligence in opioid prescribing
    - Supports clinical decision-making documentation
    - May be required by institutional policies
    - Useful for quality improvement and safety programs
    
    **Limitations and Considerations:**
    
    **Tool Limitations:**
    - Self-report instrument subject to response bias
    - May have false positives in certain populations
    - Not a diagnostic tool for opioid use disorder
    - Should be combined with clinical judgment and other assessments
    
    **Cultural and Social Factors:**
    - Consider patient's cultural background and health literacy
    - Language barriers may affect response accuracy
    - Social determinants of health impact healthcare utilization
    - Stigma surrounding addiction may influence responses
    
    **Alternative Assessment Tools:**
    
    **Complementary Instruments:**
    - **SOAPP-R** (Screener and Opioid Assessment for Patients with Pain-Revised): Pre-prescription risk assessment
    - **ORT** (Opioid Risk Tool): Brief pre-prescription screening
    - **DIRE** (Diagnosis, Intractability, Risk, Efficacy): Comprehensive opioid therapy candidacy
    - **PMQ** (Pain Medication Questionnaire): Alternative misuse assessment
    
    **COMM-9 Brief Version:**
    A validated 9-item short form is available for settings requiring briefer assessment:
    - Maintains good psychometric properties
    - Reduced administration time
    - Comparable performance to full 17-item version
    - May be preferred in busy clinical settings
    
    **Implementation Best Practices:**
    
    **Staff Training:**
    - Educate providers on COMM administration and interpretation
    - Develop institutional protocols for scoring and follow-up
    - Regular competency assessment and updates
    - Integration with electronic health record systems
    
    **Patient Communication:**
    - Explain purpose and importance of assessment
    - Emphasize confidentiality and non-judgmental approach
    - Discuss results collaboratively with patients
    - Use as opportunity for education and engagement
    
    **Quality Improvement:**
    - Monitor COMM utilization and completion rates
    - Track clinical outcomes and intervention effectiveness
    - Regular review of positive screens and follow-up actions
    - Continuous improvement of assessment and monitoring processes
    
    Args:
        request: COMM parameters including all 17 behavioral assessment questions 
                scored 0-4 for frequency over past 30 days
        
    Returns:
        CommResponse: Comprehensive assessment including total score, risk 
        categorization, pattern analysis, clinical recommendations, and 
        monitoring guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("comm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Current Opioid Misuse Measure",
                    "details": {"parameters": parameters}
                }
            )
        
        return CommResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Current Opioid Misuse Measure",
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