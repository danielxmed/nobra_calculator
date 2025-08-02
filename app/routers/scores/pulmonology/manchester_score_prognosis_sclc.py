"""
Manchester Score for Prognosis in Small Cell Lung Cancer Router

Endpoint for calculating Manchester Score for SCLC prognostic assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.manchester_score_prognosis_sclc import (
    ManchesterScorePrognosisSclcRequest,
    ManchesterScorePrognosisSclcResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/manchester_score_prognosis_sclc",
    response_model=ManchesterScorePrognosisSclcResponse,
    summary="Calculate Manchester Score for Prognosis in Small Cell Lung Cancer",
    description="Calculates the Manchester Score for Prognosis in Small Cell Lung Cancer, a validated "
                "prognostic tool that predicts 2-year survival in SCLC patients using six clinical and "
                "laboratory parameters: serum LDH, sodium, alkaline phosphatase, bicarbonate, disease "
                "stage, and Karnofsky Performance Status. Developed from analysis of 407 patients treated "
                "between 1979-1985, the score stratifies patients into three distinct prognostic groups "
                "(good, medium, poor) with significantly different survival outcomes. The good prognostic "
                "group (0-1 points) contains all long-term survivors with 16.2% two-year survival, while "
                "the poor prognostic group (4-6 points) had 0% two-year survival with no patients surviving "
                "longer than one year. This simple scoring system shows minimal loss of prognostic "
                "information compared to complex multivariate analysis and facilitates treatment decision-"
                "making, patient counseling, clinical trial stratification, and comparison between studies. "
                "Essential for determining appropriateness of aggressive curative-intent treatment versus "
                "palliative care approaches in SCLC management.",
    response_description="The calculated Manchester Score with comprehensive prognostic assessment, survival data, and treatment recommendations",
    operation_id="manchester_score_prognosis_sclc"
)
async def calculate_manchester_score_prognosis_sclc(request: ManchesterScorePrognosisSclcRequest):
    """
    Calculates Manchester Score for comprehensive prognostic assessment in small cell lung cancer
    
    The Manchester Score for Prognosis in Small Cell Lung Cancer is a validated, evidence-based
    prognostic tool specifically designed for patients with small cell lung cancer (SCLC).
    
    Clinical Background and Historical Context:
    Small cell lung cancer represents approximately 10-15% of all lung cancers but is characterized
    by aggressive behavior, rapid growth, and early metastatic spread. Despite initial sensitivity
    to chemotherapy and radiation, the prognosis remains poor with 5-year survival rates of only
    5-10%. The Manchester Score was developed in 1987 during an era when physicians and patients
    requested more detailed prognostic information due to the limited curative potential of SCLC.
    
    Study Development and Validation:
    The Manchester Score was developed by Cerny et al. through comprehensive analysis of 407 patients
    with small cell lung cancer treated between 1979 and 1985. The investigators initially evaluated
    61 pre-treatment variables through univariate and multivariate regression analysis to identify
    the most significant prognostic factors. The final scoring system incorporates six variables
    that demonstrated independent prognostic significance while maintaining clinical simplicity.
    
    Six-Parameter Prognostic Model:
    
    1. Serum Lactate Dehydrogenase (LDH) >Upper Limit of Normal (1 point):
       LDH is a cytoplasmic enzyme released during cellular damage or increased cellular turnover.
       Elevated levels in SCLC reflect high tumor burden, rapid cellular proliferation, and
       extensive tissue necrosis. LDH elevation correlates with advanced disease stage, increased
       metastatic burden, and resistance to therapy. This parameter serves as a surrogate marker
       for overall tumor activity and biological aggressiveness.
    
    2. Serum Sodium <132 mmol/L (1 point):
       Hyponatremia in SCLC patients most commonly results from the syndrome of inappropriate
       antidiuretic hormone secretion (SIADH), which occurs in 10-15% of patients. SCLC cells
       can produce ectopic ADH, leading to water retention and dilutional hyponatremia. This
       paraneoplastic syndrome indicates neuroendocrine activity of tumor cells and is associated
       with more aggressive disease behavior and worse prognosis.
    
    3. Serum Alkaline Phosphatase >1.5x Upper Limit of Normal (1 point):
       Elevated alkaline phosphatase typically indicates liver or bone involvement by metastatic
       disease. In SCLC, liver metastases are common and represent systemic disease spread.
       Bone involvement suggests advanced metastatic disease with potential for skeletal
       complications. Alkaline phosphatase elevation serves as a biochemical marker of
       metastatic burden and extensive disease.
    
    4. Serum Bicarbonate <24 mmol/L (1 point):
       Low serum bicarbonate may indicate metabolic acidosis associated with advanced malignancy,
       organ dysfunction, or systemic metabolic derangements. In SCLC patients, this may reflect
       poor physiologic reserve, compromised organ function, or systemic effects of advanced
       cancer. Metabolic acidosis can indicate impaired cellular metabolism and poor overall
       physiologic status.
    
    5. Extensive Stage Disease (1 point):
       SCLC staging distinguishes between limited stage (confined to one hemithorax, including
       ipsilateral hilar and supraclavicular lymph nodes) and extensive stage (disease beyond
       these boundaries). Extensive stage represents systemic disease with metastatic spread
       and is the most significant adverse prognostic factor in SCLC. Approximately 70% of
       patients present with extensive stage disease at diagnosis.
    
    6. Karnofsky Performance Status ≤50 (1 point):
       The Karnofsky Performance Status scale measures functional capacity and ability to
       perform activities of daily living. Scores ≤50 indicate significant functional impairment
       requiring considerable assistance or medical care. Poor performance status reflects
       disease burden, treatment tolerance capacity, and overall physiologic reserve. It serves
       as an independent prognostic factor across all cancer types.
    
    Prognostic Stratification and Clinical Outcomes:
    
    Good Prognosis Group (0-1 points):
    - Two-year survival: 16.2%
    - Contains all long-term survivors from the original cohort
    - Median survival: approximately 12-15 months
    - Treatment response rates: typically >70% initial response
    
    Clinical Management Approach:
    - Standard chemotherapy regimens with curative intent
    - Concurrent chemoradiotherapy for limited stage disease
    - Aggressive supportive care during treatment
    - Regular monitoring for treatment response and toxicity
    - Consider participation in clinical trials for novel therapies
    - Prophylactic cranial irradiation for complete responders
    
    Medium Prognosis Group (2-3 points):
    - Two-year survival: 2.5%
    - Median survival: approximately 8-10 months
    - Treatment response rates: typically 50-60% initial response
    
    Clinical Management Approach:
    - Standard chemotherapy protocols with monitoring
    - Balance treatment intensity with quality of life considerations
    - Early integration of palliative care services
    - Careful assessment of treatment tolerance and benefit
    - Consider abbreviated treatment courses if no significant response
    - Emphasis on symptom management and supportive care
    
    Poor Prognosis Group (4-6 points):
    - Two-year survival: 0%
    - No patients survived longer than one year
    - Median survival: typically <6 months
    - Treatment response rates: variable, often limited duration
    
    Clinical Management Approach:
    - Palliative care as primary treatment focus
    - Limited, symptom-directed chemotherapy if performance status permits
    - Early hospice referral consideration
    - Emphasis on comfort care and quality of life
    - Aggressive symptom management (pain, dyspnea, nausea)
    - Family support and end-of-life planning
    
    Treatment Considerations by Stage and Prognosis:
    
    Limited Stage SCLC:
    - Good prognosis: Concurrent chemoradiotherapy (preferred) or sequential approach
    - Medium prognosis: Standard chemotherapy with selective radiation
    - Poor prognosis: Palliative chemotherapy only if performance status adequate
    
    Extensive Stage SCLC:
    - Good prognosis: Combination chemotherapy (platinum plus etoposide or irinotecan)
    - Medium prognosis: Standard chemotherapy with careful monitoring
    - Poor prognosis: Single-agent palliative chemotherapy or best supportive care
    
    Modern Treatment Context:
    While the Manchester Score was developed in the pre-immunotherapy era, its prognostic
    principles remain relevant. Contemporary SCLC treatment includes:
    - First-line: Platinum-based chemotherapy with immunotherapy (atezolizumab or durvalumab)
    - Second-line: Topotecan, lurbinectedin, or clinical trial participation
    - Targeted therapies: Limited options, ongoing research into DLL3-targeted therapy
    
    Clinical Decision-Making Applications:
    
    Treatment Intensity Decisions:
    - Guide selection of aggressive vs. palliative treatment approaches
    - Inform discussions about treatment goals and expectations
    - Support decisions about clinical trial eligibility
    - Assist in resource allocation and care planning
    
    Patient and Family Counseling:
    - Provide evidence-based prognostic information
    - Support informed consent for treatment decisions
    - Guide goals-of-care discussions
    - Facilitate advance care planning
    
    Clinical Trial Stratification:
    - Balance treatment arms by prognostic risk
    - Enable subset analyses by risk group
    - Support correlative studies and biomarker development
    - Facilitate comparison between different studies
    
    Quality Assurance and Implementation:
    
    Data Collection Requirements:
    - Accurate staging with appropriate imaging (CT chest/abdomen, brain MRI)
    - Standardized laboratory measurements with institutional normal ranges
    - Validated performance status assessment
    - Complete clinical history and physical examination
    
    Implementation Considerations:
    - Integration with electronic health records and clinical pathways
    - Staff education on prognostic interpretation and communication
    - Quality assurance for laboratory and staging accuracy
    - Regular audit of prognostic accuracy and treatment outcomes
    
    Limitations and Contemporary Considerations:
    
    Temporal Limitations:
    - Developed with 1980s treatment regimens and supportive care
    - May not fully reflect outcomes with modern therapies
    - Consider contemporary survival data when counseling patients
    - Supplement with current clinical trial data when available
    
    Population Considerations:
    - Derived from clinical trial population which may not represent all patients
    - Consider comorbidities, age, and social factors in treatment decisions
    - Validate prognostic accuracy in local patient populations
    - Account for healthcare system differences and resource availability
    
    Future Directions and Research:
    
    Biomarker Integration:
    - Incorporation of molecular markers (TP53, RB1, MYC family genes)
    - Circulating tumor DNA and liquid biopsy applications
    - Immune biomarkers for immunotherapy response prediction
    - Integration with genomic profiling for personalized treatment
    
    Treatment Optimization:
    - Risk-adapted treatment protocols based on prognostic scoring
    - Development of novel targeted therapies for high-risk patients
    - Optimization of immunotherapy combinations
    - Personalized treatment duration and intensity approaches
    
    Prognostic Model Enhancement:
    - Validation in contemporary patient cohorts
    - Integration with modern imaging and laboratory parameters
    - Machine learning approaches for enhanced prediction accuracy
    - Development of dynamic prognostic models incorporating treatment response
    
    The Manchester Score continues to provide valuable prognostic information for SCLC patients
    and their families, enabling evidence-based treatment decisions and appropriate care planning.
    While treatment options have evolved, the fundamental prognostic principles captured by this
    scoring system remain clinically relevant and useful for contemporary practice.
    
    Args:
        request: Manchester Score parameters including LDH, sodium, ALP, bicarbonate, stage, and KPS
        
    Returns:
        ManchesterScorePrognosisSclcResponse: Comprehensive prognostic assessment with treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("manchester_score_prognosis_sclc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Manchester Score for SCLC prognosis",
                    "details": {"parameters": parameters}
                }
            )
        
        return ManchesterScorePrognosisSclcResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Manchester Score calculation",
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
                "message": "Internal error in Manchester Score calculation",
                "details": {"error": str(e)}
            }
        )