"""
Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival Router

Endpoint for calculating Duval/CIBMTR AML transplant survival score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.duval_cibmtr_score_aml_survival import (
    DuvalCibmtrScoreAmlSurvivalRequest,
    DuvalCibmtrScoreAmlSurvivalResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/duval_cibmtr_score_aml_survival",
    response_model=DuvalCibmtrScoreAmlSurvivalResponse,
    summary="Calculate Duval/CIBMTR Score for Acute Myelogenous Leukemia",
    description="Predicts transplantation survival of AML patients undergoing allogeneic hematopoietic stem cell transplantation (HSCT) based on five pre-transplant risk factors.",
    response_description="The calculated duval cibmtr score aml survival with interpretation",
    operation_id="duval_cibmtr_score_aml_survival"
)
async def calculate_duval_cibmtr_score_aml_survival(request: DuvalCibmtrScoreAmlSurvivalRequest):
    """
    Calculates Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival
    
    The Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival is a validated 
    prognostic tool that predicts transplantation survival for AML patients undergoing 
    allogeneic hematopoietic stem cell transplantation (HSCT). This scoring system is 
    particularly valuable for patients with active disease at the time of conditioning, 
    providing evidence-based risk stratification for clinical decision-making.
    
    Clinical Background and Development:
    
    The Duval/CIBMTR Score was developed from comprehensive analysis of 1,673 AML patients 
    with active disease undergoing allogeneic HSCT across multiple international centers. 
    The study was conducted by the Center for International Blood and Marrow Transplant 
    Research (CIBMTR) and represents one of the largest cohorts used for AML transplant 
    prognostication.
    
    The scoring system was specifically designed to address the challenging clinical 
    scenario of AML patients who proceed to transplant without achieving complete remission 
    or who have early relapse. These patients represent a high-risk population where 
    traditional prognostic factors may not adequately predict outcomes.
    
    Key Clinical Applications:
    
    Transplant Decision-Making:
    - Primary tool for assessing transplant candidacy in high-risk AML patients
    - Guides timing of transplant procedures relative to disease status
    - Supports risk-benefit analysis for patients with active disease
    - Facilitates informed consent discussions with patients and families
    - Enables standardized approach to transplant eligibility assessment
    
    Risk Stratification and Treatment Planning:
    - Identifies patients requiring intensive supportive care protocols
    - Guides selection of conditioning regimen intensity
    - Supports clinical trial enrollment decisions
    - Facilitates multidisciplinary team care planning
    - Enables appropriate resource allocation and staffing decisions
    
    Patient and Family Counseling:
    - Provides objective, evidence-based survival estimates
    - Facilitates realistic expectation setting
    - Supports shared decision-making processes
    - Guides palliative care consultation timing
    - Enables appropriate advance care planning discussions
    
    Scoring System Components and Clinical Rationale:
    
    The Duval/CIBMTR Score evaluates five critical pre-transplant variables:
    
    1. Disease Group (Remission Status and Duration):
    
    Primary Induction Failure or First CR >6 months (0 points):
    - Primary induction failure: Failure to achieve complete remission after initial induction
    - Long first complete remission: Indicates chemotherapy-sensitive disease
    - Clinical rationale: Both scenarios suggest potential for transplant benefit
    - Management implications: Proceed with standard transplant protocols
    
    First CR <6 months (1 point):
    - Short-duration first remission indicates aggressive, chemotherapy-resistant disease
    - Associated with higher relapse risk post-transplant
    - Clinical rationale: Early relapse suggests inherent drug resistance
    - Management implications: Consider intensified conditioning or investigational approaches
    
    2. Cytogenetics Prior to HSCT:
    
    Good or Intermediate Risk (0 points):
    - Good: t(8;21), inv(16)/t(16;16), t(15;17) - favorable molecular signatures
    - Intermediate: Normal karyotype, other abnormalities not classified as poor risk
    - Clinical rationale: Favorable genetics maintain prognostic significance even in active disease
    - Management implications: Standard conditioning regimens appropriate
    
    Poor Risk (1 point):
    - Complex karyotype (≥3 chromosomal abnormalities)
    - Monosomy 5, deletion 5q, monosomy 7, deletion 7q
    - Inversion 3q, t(6;9), t(9;22), 11q23 abnormalities
    - Clinical rationale: High-risk genetics predict treatment resistance and poor outcomes
    - Management implications: Consider experimental conditioning regimens or clinical trials
    
    3. HLA Match Group (Donor-Recipient Compatibility):
    
    HLA Identical Sibling or Well/Partially Matched Unrelated (0 points):
    - HLA identical sibling: Perfect 6/6 HLA match within family
    - Well-matched unrelated: 8/8 or 10/10 HLA compatibility
    - Partially matched unrelated: Single HLA mismatch with excellent donor
    - Clinical rationale: Optimal HLA matching reduces GVHD and improves survival
    - Management implications: Standard GVHD prophylaxis protocols
    
    Mismatched Unrelated (1 point):
    - Multiple HLA mismatches with unrelated donor
    - Increased risk of severe acute and chronic GVHD
    - Clinical rationale: HLA mismatches increase immunological complications
    - Management implications: Enhanced GVHD prophylaxis and monitoring required
    
    Related Other than HLA Identical Sibling (2 points):
    - Haploidentical family members (parents, children, mismatched siblings)
    - Significant HLA disparity requiring specialized protocols
    - Clinical rationale: Major histocompatibility differences increase all transplant risks
    - Management implications: Specialized conditioning and GVHD prevention strategies
    
    4. Circulating Blasts at Transplant:
    
    Absent (0 points):
    - No detectable leukemic blasts in peripheral blood
    - Indicates some degree of disease control despite active status
    - Clinical rationale: Absence of circulating disease suggests better transplant window
    - Management implications: Proceed with standard protocols and monitoring
    
    Present (1 point):
    - Any level of detectable blasts in peripheral circulation
    - Indicates active, proliferative disease at time of transplant
    - Clinical rationale: Circulating blasts predict early post-transplant relapse
    - Management implications: Enhanced monitoring and early intervention protocols
    
    5. Karnofsky/Lansky Performance Status Scale:
    
    90-100 (0 points):
    - Excellent functional status with minimal or no symptoms
    - Karnofsky 90-100: Normal activity with minor symptoms (adults)
    - Lansky 90-100: Normal activity level for age (pediatric patients)
    - Clinical rationale: Good performance status predicts transplant tolerance
    - Management implications: Standard conditioning regimens appropriate
    
    <90 (1 point):
    - Impaired functional status with significant activity limitations
    - Indicates compromised physiological reserve
    - Clinical rationale: Poor performance status increases transplant-related mortality
    - Management implications: Consider reduced-intensity conditioning or delay until improvement
    
    Score Interpretation and Clinical Management:
    
    Score 0 - Excellent Prognosis (42% 3-year overall survival):
    
    Clinical Characteristics:
    - Optimal pre-transplant risk profile across all domains
    - Best possible outcomes for active disease transplant scenario
    - Low transplant-related mortality expected
    
    Management Approach:
    - Proceed with myeloablative conditioning as planned
    - Standard supportive care protocols sufficient
    - Routine post-transplant monitoring and interventions
    - High confidence in transplant decision
    - Family counseling emphasizes favorable prognosis
    
    Score 1 - Good Prognosis (28% 3-year overall survival):
    
    Clinical Characteristics:
    - Single adverse risk factor present
    - Reasonable transplant outcomes expected
    - Moderate risk of complications
    
    Management Approach:
    - Enhanced supportive care measures throughout transplant course
    - Close monitoring for early signs of complications
    - Consider prophylactic interventions for GVHD prevention
    - Regular reassessment of clinical status and response
    - Optimistic but realistic family discussions
    
    Score 2 - Intermediate Prognosis (15% 3-year overall survival):
    
    Clinical Characteristics:
    - Multiple adverse risk factors present
    - Significant transplant risks but potential for benefit
    - Careful risk-benefit analysis required
    
    Management Approach:
    - Intensive multidisciplinary care planning required
    - Enhanced supportive care protocols and monitoring
    - Early intervention strategies for complications
    - Consider patient-specific factors and comorbidities
    - Detailed informed consent discussions essential
    - Consider reduced-intensity conditioning in selected cases
    
    Score ≥3 - Poor Prognosis (6% 3-year overall survival):
    
    Clinical Characteristics:
    - Multiple high-risk factors present
    - Very limited transplant benefit expected
    - High likelihood of transplant-related complications
    
    Management Approach:
    - Mandatory multidisciplinary team consultation
    - Consider alternative treatment approaches
    - Clinical trial enrollment strongly preferred if available
    - Palliative care consultation recommended
    - Comprehensive family counseling and support
    - Advanced care planning discussions essential
    - Transplant decision requires institutional consensus
    
    Validation and Performance Characteristics:
    
    Original Development and Validation:
    - Derivation cohort: 1,673 AML patients with active disease
    - Multi-institutional international study design
    - Median follow-up: 3 years for survival analysis
    - Consistent prognostic performance across participating centers
    
    External Validation Studies:
    - Multiple independent cohorts have confirmed prognostic accuracy
    - Consistent performance across different conditioning regimens
    - Validated in both adult and pediatric populations
    - Maintains prognostic value in contemporary transplant practice
    
    Limitations and Considerations:
    
    Study Population Limitations:
    - Original validation limited to myeloablative conditioning regimens
    - Busulfan and total body irradiation-based conditioning only
    - Reduced-intensity conditioning outcomes may differ significantly
    - Syngeneic and cord blood transplants excluded from analysis
    
    Contemporary Application Considerations:
    - Modern supportive care may improve outcomes across all risk groups
    - Novel conditioning regimens may alter prognostic relationships
    - Targeted therapies and immunotherapies not considered in original model
    - Minimal residual disease testing not incorporated
    
    Clinical Integration Recommendations:
    
    Pre-Transplant Assessment:
    - Use score as part of comprehensive transplant evaluation
    - Integrate with other prognostic tools and clinical factors
    - Consider dynamic reassessment if clinical status changes
    - Document score and rationale in transplant planning records
    
    Treatment Planning:
    - Higher scores warrant enhanced supportive care planning
    - Consider alternative donor sources for high-risk patients
    - Integrate score into conditioning regimen selection
    - Plan for intensive post-transplant monitoring and intervention
    
    Patient Communication:
    - Provide clear explanation of score components and meaning
    - Use score to facilitate realistic expectation setting
    - Support shared decision-making with objective data
    - Coordinate with social work and chaplaincy services as appropriate
    
    Quality Improvement Applications:
    
    Institutional Quality Metrics:
    - Track outcomes by risk score for quality assessment
    - Benchmark institutional performance against published results
    - Identify opportunities for risk-specific protocol optimization
    - Support transplant program accreditation and reporting requirements
    
    Clinical Research Integration:
    - Use for patient stratification in clinical trials
    - Enable retrospective outcome analysis and improvement initiatives
    - Support development of risk-adapted treatment protocols
    - Facilitate multi-center collaborative research efforts
    
    Future Directions and Emerging Considerations:
    
    Score Enhancement Opportunities:
    - Integration of molecular markers and minimal residual disease
    - Incorporation of novel conditioning regimens and techniques
    - Addition of pharmacogenomic factors affecting drug metabolism
    - Integration with post-transplant biomarkers and monitoring
    
    Personalized Medicine Applications:
    - Development of patient-specific risk calculators
    - Integration with electronic health record clinical decision support
    - Real-time risk assessment and treatment modification
    - Precision medicine approaches based on individual risk profiles
    
    Educational and Training Applications:
    
    Medical Education:
    - Essential component of hematology and transplant medicine curricula
    - Provides framework for understanding transplant risk assessment
    - Supports evidence-based medicine teaching and practice
    - Facilitates standardized approach to patient evaluation
    
    Professional Development:
    - Continuing medical education programs for transplant professionals
    - Quality improvement and safety training initiatives
    - Multidisciplinary team communication enhancement
    - Evidence-based practice implementation support
    
    Conclusion:
    
    The Duval/CIBMTR Score represents a critical tool for evidence-based decision-making 
    in AML transplantation. By providing objective, validated prognostic information, 
    it enables clinicians to optimize treatment planning, enhance patient counseling, 
    and improve overall transplant outcomes. The score should be integrated into 
    comprehensive transplant evaluation processes while recognizing its limitations 
    and the need for individualized clinical judgment.
    
    Args:
        request: Duval/CIBMTR assessment parameters for five pre-transplant risk factors
        
    Returns:
        DuvalCibmtrScoreAmlSurvivalResponse: Risk score with survival prediction and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("duval_cibmtr_score_aml_survival", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Duval/CIBMTR Score for AML Survival",
                    "details": {"parameters": parameters}
                }
            )
        
        return DuvalCibmtrScoreAmlSurvivalResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Duval/CIBMTR Score for AML Survival",
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