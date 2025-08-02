"""
MALT Lymphoma Prognostic Index (MALT-IPI) Router

Endpoint for calculating MALT-IPI score for prognostic assessment in MALT lymphoma patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.malt_lymphoma_prognostic_index import (
    MaltLymphomaPrognosticIndexRequest,
    MaltLymphomaPrognosticIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/malt_lymphoma_prognostic_index",
    response_model=MaltLymphomaPrognosticIndexResponse,
    summary="Calculate MALT Lymphoma Prognostic Index (MALT-IPI)",
    description="Calculates the MALT Lymphoma Prognostic Index (MALT-IPI), a validated prognostic tool that "
                "identifies MALT lymphoma patients at risk for poor outcomes using three simple clinical "
                "parameters: age ≥70 years, Ann Arbor stage III/IV, and elevated lactate dehydrogenase (LDH). "
                "The index stratifies patients into three risk groups (low, intermediate, high) predictive for "
                "event-free survival and overall survival. Developed using 401 patients from the IELSG-19 "
                "randomized trial and validated in independent cohorts (N=633). The MALT-IPI is applicable to "
                "both gastric and non-gastric MALT lymphoma and retains prognostic utility across different "
                "treatment regimens including chlorambucil, rituximab, and combination therapy. This simple, "
                "accessible tool significantly discriminates between patients with different progression-free, "
                "overall, and cause-specific survival, helping to define appropriate treatment approaches for "
                "individual patients. Essential for treatment planning, patient counseling, clinical trial "
                "stratification, and determining monitoring frequency in MALT lymphoma management.",
    response_description="The calculated MALT-IPI score with comprehensive risk stratification, detailed survival outcomes, and treatment recommendations",
    operation_id="malt_lymphoma_prognostic_index"
)
async def calculate_malt_lymphoma_prognostic_index(request: MaltLymphomaPrognosticIndexRequest):
    """
    Calculates MALT-IPI score for comprehensive prognostic assessment in MALT lymphoma
    
    The MALT Lymphoma Prognostic Index (MALT-IPI) is a validated, evidence-based prognostic tool
    specifically designed for mucosa-associated lymphoid tissue (MALT) lymphoma patients.
    
    Clinical Background and Development:
    MALT lymphoma is the most common subtype of marginal zone lymphoma, typically arising from
    mucosa-associated lymphoid tissue in various organs including stomach, lung, thyroid, salivary
    glands, and ocular adnexa. While generally considered indolent, clinical outcomes can be
    heterogeneous, necessitating reliable prognostic tools for treatment planning.
    
    The MALT-IPI was developed by the International Extranodal Lymphoma Study Group (IELSG) using
    data from 401 patients enrolled in the IELSG-19 randomized trial. The index underwent rigorous
    validation in multiple independent cohorts totaling 633 patients, demonstrating consistent
    prognostic utility across diverse populations and treatment settings.
    
    Three-Parameter Prognostic Model:
    
    1. Age ≥70 Years (Hazard Ratio 1.72, 95% CI 1.26-2.33):
       Advanced age is independently associated with worse outcomes in MALT lymphoma, likely
       reflecting decreased physiologic reserve, increased comorbidities, and potential treatment
       intolerance. Age ≥70 years adds 1 point to the total score.
    
    2. Ann Arbor Stage III/IV (Hazard Ratio 1.79, 95% CI 1.35-2.38):
       Advanced stage disease indicates more extensive lymphoma involvement beyond localized
       sites, representing systemic disease burden. Stage III (lymph node regions on both sides
       of the diaphragm) or Stage IV (disseminated involvement) adds 1 point to the total score.
    
    3. Elevated Lactate Dehydrogenase (Hazard Ratio 1.87, 95% CI 1.27-2.77):
       Elevated LDH above the institutional upper limit of normal reflects increased tumor burden,
       cellular turnover, and metabolic activity. LDH elevation is a well-established adverse
       prognostic factor in lymphomas and adds 1 point to the total score.
    
    Risk Stratification and Clinical Outcomes:
    
    Low Risk (0 points) - Excellent Prognosis:
    - 5-year overall survival: 96.7%
    - 5-year event-free survival: 76.0%
    - 5-year cause-specific survival: 98.2%
    - 5-year progression-free survival: 56.8%
    
    Clinical Management Approach:
    - Conservative management strategies may be appropriate
    - Watchful waiting for asymptomatic, localized disease
    - Minimal intervention with close monitoring
    - Treatment decisions based on symptoms, organ function, and patient preference
    - Regular surveillance with clinical assessment and imaging
    
    Intermediate Risk (1 point) - Moderate Prognosis:
    - 5-year overall survival: 81.7%
    - 5-year event-free survival: 48.4%
    - 5-year cause-specific survival: 94.7%
    - 5-year progression-free survival: 48.0%
    
    Clinical Management Approach:
    - More intensive monitoring and treatment planning required
    - Consider early intervention based on clinical presentation
    - Regular oncology follow-up for treatment optimization
    - Balance between conservative management and active treatment
    - Patient education regarding disease course and treatment options
    
    High Risk (≥2 points) - Poor Prognosis:
    - 5-year overall survival: 64.9%
    - 5-year event-free survival: 15.7%
    - 5-year cause-specific survival: 74.3%
    - 5-year progression-free survival: 22.7%
    
    Clinical Management Approach:
    - Aggressive treatment approaches strongly recommended
    - Prompt oncology referral and multidisciplinary care planning
    - Consider combination chemotherapy regimens
    - Rituximab-based treatments often beneficial
    - Clinical trial enrollment should be considered
    - Intensive monitoring and supportive care
    
    Treatment Considerations Across Risk Groups:
    
    Gastric MALT Lymphoma:
    - H. pylori eradication therapy for early-stage disease
    - Response assessment with endoscopic follow-up
    - Additional treatment for H. pylori-negative or refractory disease
    - Consider radiation therapy for localized disease
    
    Non-Gastric MALT Lymphoma:
    - Organ-specific treatment approaches
    - Radiation therapy for localized disease
    - Systemic therapy for advanced or symptomatic disease
    - Consider organ function and anatomic constraints
    
    Systemic Treatment Options:
    - Rituximab monotherapy or combination regimens
    - Chlorambucil or other alkylating agents
    - Bendamustine-based combinations
    - Lenalidomide for refractory disease
    - Clinical trials for novel targeted therapies
    
    Validation and Clinical Utility:
    
    Multi-Cohort Validation:
    The MALT-IPI has been validated across multiple independent cohorts, confirming its
    prognostic utility in diverse populations and healthcare settings. The index maintains
    discriminatory power across different treatment modalities and geographic regions.
    
    Treatment-Independent Prognostic Value:
    Prognostic utility is retained across different treatment arms including:
    - Chlorambucil monotherapy
    - Rituximab monotherapy
    - Rituximab plus chlorambucil combination therapy
    - Watch-and-wait strategies
    - Radiation therapy approaches
    
    Clinical Applications:
    
    Treatment Planning:
    - Guide treatment intensity decisions
    - Balance benefits and risks of active intervention
    - Inform timing of treatment initiation
    - Support multidisciplinary treatment planning
    
    Patient Counseling:
    - Provide evidence-based prognostic information
    - Support informed decision-making
    - Set appropriate expectations for disease course
    - Guide discussions about treatment goals
    
    Clinical Trial Stratification:
    - Stratify patients by risk group in clinical trials
    - Enable balanced randomization across risk categories
    - Support correlative studies and biomarker development
    - Facilitate comparison across different studies
    
    Monitoring and Follow-up:
    - Determine appropriate surveillance intensity
    - Guide timing of restaging assessments
    - Support long-term care planning
    - Identify patients requiring closer monitoring
    
    Quality Assurance and Implementation:
    
    Clinical Data Requirements:
    - Accurate staging assessment with appropriate imaging
    - Standardized LDH measurement with institutional normal ranges
    - Complete clinical history and physical examination
    - Histologic confirmation of MALT lymphoma diagnosis
    
    Implementation Considerations:
    - Integration with electronic health records
    - Staff training on risk assessment and interpretation
    - Quality assurance for staging and laboratory measurements
    - Regular audit of prognostic accuracy and clinical outcomes
    
    Limitations and Considerations:
    
    Patient Selection:
    - Developed and validated primarily in clinical trial populations
    - May not fully represent all MALT lymphoma patients
    - Consider comorbidities and performance status in treatment decisions
    - Individual patient factors may modify risk assessment
    
    Temporal Considerations:
    - Prognostic assessment reflects disease status at diagnosis
    - Risk stratification may change with disease evolution
    - Regular reassessment may be appropriate for some patients
    - Consider treatment-related factors in ongoing management
    
    Future Directions:
    
    Biomarker Integration:
    - Investigation of molecular markers for enhanced prognostication
    - Integration of genetic and genomic profiling
    - Development of personalized medicine approaches
    - Correlation with treatment response biomarkers
    
    Treatment Optimization:
    - Risk-adapted treatment protocols
    - Development of novel targeted therapies
    - Optimization of combination regimens
    - Personalized treatment intensity approaches
    
    Args:
        request: MALT-IPI parameters including age, LDH level, and Ann Arbor stage
        
    Returns:
        MaltLymphomaPrognosticIndexResponse: Comprehensive prognostic assessment with risk stratification and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("malt_lymphoma_prognostic_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MALT-IPI score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MaltLymphomaPrognosticIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MALT-IPI calculation",
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
                "message": "Internal error in MALT-IPI calculation",
                "details": {"error": str(e)}
            }
        )