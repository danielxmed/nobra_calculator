"""
Diabetic Ketoacidosis Mortality Prediction Model (DKA MPM) Score Router

Endpoint for calculating DKA MPM Score for mortality prediction in diabetic ketoacidosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.dka_mpm_score import (
    DkaMpmScoreRequest,
    DkaMpmScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dka_mpm_score",
    response_model=DkaMpmScoreResponse,
    summary="Calculate Diabetic Ketoacidosis Mortality Prediction Model",
    description="Predicts in-hospital mortality in patients with diabetic ketoacidosis using clinical and laboratory parameters at presentation, 12 hours, and 24 hours",
    response_description="The calculated dka mpm score with interpretation",
    operation_id="calculate_dka_mpm_score"
)
async def calculate_dka_mpm_score(request: DkaMpmScoreRequest):
    """
    Calculates Diabetic Ketoacidosis Mortality Prediction Model (DKA MPM) Score
    
    The DKA MPM Score is a mortality prediction model specifically developed for patients 
    with diabetic ketoacidosis (DKA) that uses clinical and laboratory parameters assessed 
    at presentation, 12 hours, and 24 hours to stratify patients into distinct risk 
    categories for in-hospital mortality. This evidence-based tool provides valuable 
    prognostic information to guide clinical decision-making, intensive care resource 
    allocation, and family counseling in the management of DKA.
    
    **Historical Context and Development:**
    
    **Recognition of DKA Mortality Risk Heterogeneity:**
    Diabetic ketoacidosis has historically been associated with significant mortality, 
    particularly in older patients and those with comorbidities. Prior to the development 
    of the DKA MPM Score, clinicians relied primarily on general severity of illness 
    scores or clinical judgment to assess prognosis in DKA patients. There was a clear 
    need for a DKA-specific mortality prediction tool that could identify patients at 
    highest risk for poor outcomes.
    
    **Development Process:**
    The DKA MPM Score was developed by Efstathiou et al. in 2002 through a retrospective 
    analysis of 154 consecutive patients admitted with DKA. The researchers systematically 
    analyzed clinical and laboratory variables at different time points to identify 
    independent predictors of in-hospital mortality. The final model incorporated six 
    parameters assessed at presentation, 12 hours, and 24 hours after admission.
    
    **Validation and Performance:**
    In the original study, the DKA MPM Score demonstrated excellent discriminatory ability 
    with clear risk stratification. The score effectively separated patients into three 
    distinct risk categories with markedly different mortality rates: low risk (0.86%), 
    high risk (20.8%), and very high risk (93.3%).
    
    **Clinical Assessment Parameters:**
    
    **1. At Presentation (0 Hours):**
    
    **Severe Comorbidities (6 points if present):**
    
    **Clinical Significance:**
    The presence of severe comorbidities represents the single highest-weighted parameter 
    in the DKA MPM Score, reflecting the profound impact of underlying medical conditions 
    on DKA outcomes. These comorbidities not only complicate DKA management but also 
    limit the patient's physiological reserve to recover from the metabolic crisis.
    
    **Included Comorbidities:**
    - **Immunosuppression:** Increases infection risk and impairs healing
    - **Previous Myocardial Infarction:** Indicates cardiovascular compromise
    - **Chronic Obstructive Pulmonary Disease (COPD):** Affects acid-base compensation
    - **Cirrhosis:** Impairs metabolic function and increases bleeding risk
    - **Congestive Heart Failure:** Limits ability to handle fluid resuscitation
    - **Previous Stroke:** Indicates cerebrovascular disease and potential complications
    
    **Clinical Implications:**
    Patients with severe comorbidities require multidisciplinary care coordination, 
    careful fluid management, and enhanced monitoring for complications. The presence 
    of any of these conditions should prompt consideration for intensive care unit 
    admission and specialist consultation.
    
    **pH < 7.0 (4 points if present):**
    
    **Clinical Significance:**
    Severe acidosis with pH < 7.0 represents a life-threatening metabolic derangement 
    that significantly increases mortality risk in DKA. This level of acidosis indicates 
    massive ketone production, severe insulin deficiency, and potentially irreversible 
    metabolic dysfunction.
    
    **Pathophysiology:**
    pH < 7.0 reflects overwhelming ketoacid production that exceeds the body's buffering 
    capacity and compensatory mechanisms. This severe acidosis can lead to cardiovascular 
    depression, altered mental status, and cellular dysfunction throughout the body.
    
    **Clinical Implications:**
    Patients with pH < 7.0 require immediate aggressive intervention including high-dose 
    insulin therapy, careful bicarbonate consideration, and intensive monitoring. This 
    finding mandates ICU-level care and frequent reassessment of acid-base status.
    
    **2. At 12 Hours After Presentation:**
    
    **> 50 Units Regular Insulin Required (4 points if present):**
    
    **Clinical Significance:**
    The requirement for more than 50 units of regular insulin in the first 12 hours 
    indicates severe insulin resistance, massive ketone production, or inadequate 
    response to initial therapy. This finding suggests either very severe DKA or 
    complicating factors that impair insulin effectiveness.
    
    **Underlying Mechanisms:**
    High insulin requirements may reflect severe dehydration, electrolyte imbalances, 
    concurrent illness, medication interference, or underlying insulin resistance. 
    Patients with concurrent infections, steroids, or other stress factors may require 
    significantly higher insulin doses.
    
    **Clinical Implications:**
    Patients requiring high-dose insulin need intensive monitoring of glucose, 
    electrolytes, and fluid balance. Clinicians should investigate underlying causes 
    of insulin resistance and consider alternative insulin delivery methods or 
    concurrent treatment of precipitating factors.
    
    **Serum Glucose > 300 mg/dL at 12 Hours (4 points if present):**
    
    **Clinical Significance:**
    Persistent severe hyperglycemia after 12 hours of treatment indicates inadequate 
    response to therapy and suggests either insufficient insulin delivery, ongoing 
    ketogenesis, or complicating factors. This finding is particularly concerning 
    as glucose typically responds more rapidly than ketosis to insulin therapy.
    
    **Prognostic Implications:**
    Failure to achieve significant glucose reduction within 12 hours suggests a more 
    severe or complicated course and identifies patients at higher risk for prolonged 
    hospitalization and complications.
    
    **Clinical Implications:**
    Persistent hyperglycemia requires reassessment of insulin dosing, investigation 
    for precipitating factors, and consideration of alternative treatment approaches. 
    Enhanced monitoring and potential intensification of therapy are indicated.
    
    **3. At 24 Hours After Presentation:**
    
    **Depressed Mental State (4 points if present):**
    
    **Clinical Significance:**
    Altered mental status persisting at 24 hours after presentation is an ominous 
    sign that may indicate cerebral edema, persistent severe metabolic derangement, 
    or other serious complications. Normal mental status should return relatively 
    early in DKA treatment as acidosis and dehydration resolve.
    
    **Potential Causes:**
    - **Cerebral Edema:** Most feared complication, especially in younger patients
    - **Persistent Severe Acidosis:** Ongoing metabolic dysfunction
    - **Hypoglycemia:** From overly aggressive insulin therapy
    - **Electrolyte Imbalances:** Particularly hyponatremia or hypophosphatemia
    - **Concurrent Illness:** Sepsis, stroke, or other neurological conditions
    
    **Clinical Implications:**
    Depressed mental status at 24 hours requires immediate neurological assessment, 
    brain imaging consideration, and intensive monitoring. This finding may indicate 
    need for neurosurgical consultation and aggressive management of intracranial 
    pressure.
    
    **Fever at 24 Hours (3 points if present):**
    
    **Clinical Significance:**
    Fever developing or persisting at 24 hours after presentation suggests infectious 
    complications, which significantly worsen DKA prognosis. While DKA itself rarely 
    causes fever, the development of fever during treatment is concerning for 
    secondary complications.
    
    **Common Infectious Complications:**
    - **Pneumonia:** Aspiration or nosocomial acquisition
    - **Urinary Tract Infection:** Common precipitant that may worsen
    - **Central Line Infections:** From invasive monitoring
    - **Surgical Site Infections:** If procedures performed
    - **Catheter-Associated Infections:** From urinary catheters
    
    **Clinical Implications:**
    Fever at 24 hours requires immediate infectious workup including blood cultures, 
    chest imaging, urinalysis, and consideration of empiric antibiotic therapy. 
    Source control and appropriate antimicrobial treatment are essential.
    
    **Risk Stratification and Clinical Decision-Making:**
    
    **Low Risk (0-14 points, 0.86% mortality):**
    
    **Clinical Characteristics:**
    Patients in this category typically have uncomplicated DKA without significant 
    comorbidities, adequate response to initial therapy, and no major complications 
    during the first 24 hours. They represent the majority of DKA patients and have 
    an excellent prognosis with standard care.
    
    **Management Approach:**
    - Standard DKA protocols are appropriate
    - General medical ward admission typically sufficient
    - Routine monitoring intervals (q4-6h initially)
    - Standard nursing ratios acceptable
    - Focus on diabetes education and discharge planning
    
    **High Risk (15-18 points, 20.8% mortality):**
    
    **Clinical Characteristics:**
    These patients have either significant comorbidities, suboptimal response to 
    initial therapy, or early complications. They require enhanced monitoring and 
    more intensive management but may still have good outcomes with appropriate care.
    
    **Management Approach:**
    - Consider intensive care unit or step-down unit admission
    - Enhanced monitoring (q2-4h assessments)
    - Increased nursing attention and specialist consultation
    - More frequent laboratory monitoring
    - Proactive management of complications
    
    **Very High Risk (19-25 points, 93.3% mortality):**
    
    **Clinical Characteristics:**
    Patients in this category have multiple high-risk features, severe complications, 
    or poor response to therapy. They have an extremely poor prognosis and require 
    the most intensive interventions available.
    
    **Management Approach:**
    - Immediate intensive care unit admission mandatory
    - Continuous monitoring and one-to-one nursing
    - Aggressive interventions and specialist consultation
    - Early family discussions about prognosis and goals of care
    - Consideration of comfort measures if appropriate
    
    **Clinical Implementation and Workflow Integration:**
    
    **Assessment Timing Requirements:**
    The DKA MPM Score requires systematic assessment at three time points, which 
    necessitates organized workflow integration:
    
    **At Presentation (0 hours):**
    - Complete history and physical examination
    - Review of comorbidities and previous medical records
    - Arterial blood gas analysis for pH determination
    - Initial risk stratification for triage decisions
    
    **At 12 Hours:**
    - Review total insulin requirements from arrival
    - Assess glucose response to therapy
    - Evaluate need for treatment intensification
    - Consider risk category adjustment
    
    **At 24 Hours:**
    - Comprehensive neurological assessment
    - Temperature monitoring and infection evaluation
    - Complete score calculation and final risk stratification
    - Prognostic counseling and care planning
    
    **Quality Improvement Applications:**
    
    **Standardized Risk Assessment:**
    Implementation of the DKA MPM Score can standardize risk assessment across 
    providers and institutions, ensuring consistent identification of high-risk 
    patients and appropriate resource allocation.
    
    **Outcome Monitoring:**
    Regular use of the score allows tracking of institutional outcomes and 
    identification of opportunities for improvement in DKA care protocols.
    
    **Resource Allocation:**
    Risk stratification can guide appropriate use of intensive care resources, 
    ensuring that patients most likely to benefit receive enhanced monitoring 
    while avoiding unnecessary intensive interventions for low-risk patients.
    
    **Education and Training:**
    The score provides a framework for teaching residents and fellows about 
    DKA prognostic factors and the importance of systematic assessment at 
    multiple time points.
    
    **Limitations and Considerations:**
    
    **External Validation:**
    The DKA MPM Score has not been externally validated in independent patient 
    populations, which limits confidence in its universal applicability. Clinicians 
    should use the score in conjunction with clinical judgment rather than as a 
    standalone decision-making tool.
    
    **Alternative Scores:**
    The APACHE II score may provide superior mortality prediction in some populations 
    and should be considered as a complementary assessment tool, particularly in 
    intensive care settings.
    
    **Population Limitations:**
    The score was developed in an adult population and may not be applicable to 
    pediatric patients with DKA, who have different risk factors and outcomes.
    
    **Temporal Considerations:**
    The requirement for assessment at multiple time points may limit the score's 
    utility for immediate triage decisions, though early parameters (presentation 
    findings) can provide initial risk assessment.
    
    **Integration with Modern DKA Management:**
    
    **Contemporary Protocols:**
    Modern DKA management protocols emphasize early aggressive intervention, 
    continuous insulin infusions, and systematic monitoring. The DKA MPM Score 
    can complement these protocols by providing objective risk stratification 
    to guide intensity of monitoring and intervention.
    
    **Technology Integration:**
    Electronic health record integration can facilitate automated score calculation 
    and alert generation, ensuring systematic assessment and reducing the risk of 
    missed high-risk patients.
    
    **Multidisciplinary Care:**
    Risk stratification can guide appropriate involvement of subspecialists, 
    including endocrinology, critical care, and infectious disease consultants 
    based on patient risk category and specific complications.
    
    **Patient and Family Communication:**
    
    **Prognostic Counseling:**
    The DKA MPM Score provides objective data to guide prognostic discussions 
    with patients and families, particularly for those in high and very high-risk 
    categories where honest communication about outcomes is essential.
    
    **Shared Decision-Making:**
    Risk stratification can inform discussions about intensity of care, goals 
    of treatment, and consideration of comfort measures for patients with very 
    poor prognosis.
    
    **Research and Quality Initiatives:**
    
    **Clinical Trials:**
    The DKA MPM Score can be used for risk stratification in clinical trials 
    investigating new DKA treatments or interventions, ensuring balanced 
    randomization across risk categories.
    
    **Outcome Studies:**
    Regular monitoring using the score can facilitate outcomes research and 
    identification of factors associated with improved or worsened prognosis 
    in contemporary DKA care.
    
    **Future Directions:**
    
    **External Validation:**
    Prospective validation studies in diverse populations are needed to confirm 
    the score's accuracy and generalizability across different healthcare settings 
    and patient populations.
    
    **Score Refinement:**
    Integration of additional biomarkers, imaging findings, or clinical parameters 
    might improve the score's predictive accuracy and clinical utility.
    
    **Pediatric Adaptation:**
    Development of pediatric-specific versions or modifications could extend the 
    score's utility to younger populations where DKA outcomes and risk factors 
    may differ significantly.
    
    Args:
        request: DKA MPM Score parameters including comorbidities, pH, insulin 
                requirements, glucose response, mental status, and fever at 
                specified time points
        
    Returns:
        DkaMpmScoreResponse: Comprehensive mortality risk assessment including 
        score, risk category, detailed clinical recommendations, monitoring 
        guidance, and prognostic counseling information
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dka_mpm_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DKA MPM Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DkaMpmScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DKA MPM Score",
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