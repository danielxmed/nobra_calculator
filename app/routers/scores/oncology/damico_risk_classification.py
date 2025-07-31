"""
D'Amico Risk Classification for Prostate Cancer Router

Endpoint for calculating D'Amico risk stratification for prostate cancer.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.damico_risk_classification import (
    DamicoRiskClassificationRequest,
    DamicoRiskClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/damico_risk_classification",
    response_model=DamicoRiskClassificationResponse,
    summary="Calculate D'Amico Risk Classification for Prostate Cancer",
    description="Assesses 5-year risk of treatment failure in patients with localized prostate cancer based on clinical factors. Stratifies patients into low, intermediate, or high-risk groups to guide treatment decisions and prognosis estimation.",
    response_description="The calculated damico risk classification with interpretation",
    operation_id="calculate_damico_risk_classification"
)
async def calculate_damico_risk_classification(request: DamicoRiskClassificationRequest):
    """
    Calculates D'Amico Risk Classification for Prostate Cancer
    
    The D'Amico Risk Classification is a widely used risk stratification system that 
    categorizes patients with clinically localized prostate cancer into low, intermediate, 
    or high-risk groups based on three readily available clinical parameters: pretreatment 
    prostate-specific antigen (PSA) level, biopsy Gleason score, and clinical tumor (T) stage.
    
    **Historical Background:**
    
    Developed in 1998 by Anthony V. D'Amico and colleagues at Harvard Medical School and 
    Dana-Farber Cancer Institute, this classification system emerged from the need to 
    predict biochemical recurrence following definitive local therapy for prostate cancer. 
    The original study analyzed 888 men treated with radical prostatectomy, external beam 
    radiation therapy, or interstitial radiation therapy, establishing risk groups that 
    have become the foundation for modern prostate cancer management.
    
    **Clinical Significance:**
    
    The D'Amico classification has become the cornerstone of prostate cancer risk 
    stratification because it:
    
    - Provides a simple, reproducible framework using readily available clinical data
    - Predicts biochemical recurrence risk with good discriminatory ability
    - Guides treatment decision-making and patient counseling
    - Serves as the basis for major clinical practice guidelines
    - Enables patient stratification for clinical trials and research
    - Facilitates communication between healthcare providers
    
    **Risk Group Definitions and Clinical Implications:**
    
    **Low Risk Group:**
    
    **Criteria:** ALL of the following must be present:
    - PSA ≤10 ng/mL AND
    - Gleason score ≤6 AND
    - Clinical stage T1-T2a
    
    **Biochemical Recurrence Risk:** 5-15% at 5 years
    
    **Clinical Characteristics:**
    - Well-differentiated tumors with limited extent
    - Excellent prognosis with >95% 10-year disease-specific survival
    - Low metastatic potential
    - Excellent candidates for cure with any definitive therapy
    
    **Treatment Options:**
    - **Active Surveillance:** Appropriate for many patients, especially those >65 years
    - **Radical Prostatectomy:** Excellent cure rates with nerve-sparing techniques
    - **External Beam Radiation:** Equivalent cancer control to surgery
    - **Brachytherapy:** Effective single-modality treatment for suitable candidates
    
    **Management Considerations:**
    - Life expectancy >10 years may favor definitive treatment
    - Quality of life and treatment side effects should be carefully considered
    - Regular monitoring is essential regardless of treatment choice
    - Patient preference and anxiety levels influence treatment selection
    
    **Intermediate Risk Group:**
    
    **Criteria:** ANY of the following:
    - PSA 10-20 ng/mL OR
    - Gleason score 7 OR
    - Clinical stage T2b
    
    **Biochemical Recurrence Risk:** 15-45% at 5 years
    
    **Clinical Characteristics:**
    - Heterogeneous group with varying disease aggressiveness
    - Good to very good prognosis with appropriate treatment
    - Moderate risk of progression without definitive therapy
    - May benefit from risk substratification
    
    **Treatment Options:**
    - **Definitive Local Therapy:** Typically recommended
    - **Radical Prostatectomy:** With lymph node assessment
    - **External Beam Radiation:** With or without short-term androgen deprivation
    - **Brachytherapy:** May require combination with external beam radiation
    
    **Management Considerations:**
    - Multidisciplinary consultation valuable for treatment planning
    - Consider adjuvant or neoadjuvant therapy based on specific risk factors
    - Enhanced monitoring compared to low-risk patients
    - Individual risk factors within group influence treatment intensity
    
    **High Risk Group:**
    
    **Criteria:** ANY of the following:
    - PSA >20 ng/mL OR
    - Gleason score ≥8 OR
    - Clinical stage ≥T2c
    
    **Biochemical Recurrence Risk:** 45-65% at 5 years
    
    **Clinical Characteristics:**
    - Aggressive disease with significant recurrence risk
    - Higher likelihood of micrometastatic disease at presentation
    - Requires intensive treatment and monitoring
    - Potential for systemic disease progression
    
    **Treatment Options:**
    - **Multimodal Therapy:** Often recommended
    - **Radiation + Androgen Deprivation:** Long-term (18-36 months) hormonal therapy
    - **Radical Prostatectomy:** With extended lymph node dissection
    - **Neoadjuvant/Adjuvant Therapy:** Consider based on pathologic findings
    
    **Management Considerations:**
    - Multidisciplinary tumor board review recommended
    - Staging workup may include advanced imaging
    - Close surveillance for local and systemic recurrence
    - Consider clinical trial participation
    
    **Clinical Parameter Analysis:**
    
    **PSA Level Assessment:**
    
    **Normal Physiology:** PSA is produced by prostatic epithelial cells and serves 
    to liquefy semen. Normal levels are typically <4 ng/mL, though age-adjusted 
    ranges are increasingly recognized.
    
    **Risk Stratification:**
    - **≤10 ng/mL:** Associated with localized disease and favorable outcomes
    - **10-20 ng/mL:** Intermediate risk with increased likelihood of extracapsular extension
    - **>20 ng/mL:** High risk with significant probability of advanced local disease
    
    **Clinical Considerations:**
    - Age-adjusted normal values (younger men have lower normal PSA)
    - Prostate volume affects PSA density calculations
    - Medications (5-alpha reductase inhibitors) reduce PSA by ~50%
    - Recent procedures, infections, or inflammation can elevate PSA
    - PSA velocity and doubling time provide additional prognostic information
    
    **Gleason Score Evaluation:**
    
    **Histologic Grading:** The Gleason grading system evaluates the architectural 
    pattern of prostate cancer glands, with scores from 1-5 for primary and secondary 
    patterns. The sum creates the Gleason score (2-10).
    
    **Risk Stratification:**
    - **≤6:** Well-differentiated tumors with excellent prognosis
    - **7:** Moderately differentiated; substratified as 3+4 vs 4+3
    - **≥8:** Poorly differentiated with aggressive behavior
    
    **Modern Considerations:**
    - WHO/ISUP Grade Groups provide clearer risk communication
    - Gleason 6 tumors rarely metastasize or cause cancer death
    - Gleason 7 tumors show heterogeneous behavior
    - Tertiary patterns may provide additional prognostic information
    - Percent involvement and tumor volume add prognostic value
    
    **Clinical Stage Assessment:**
    
    **TNM Staging:** Based on digital rectal examination, imaging studies, and 
    biopsy findings to determine local tumor extent.
    
    **Risk Stratification:**
    - **T1-T2a:** Confined disease with favorable outcomes
    - **T2b:** Intermediate risk with increased recurrence potential
    - **≥T2c:** Advanced local disease requiring aggressive treatment
    
    **Clinical Considerations:**
    - Digital rectal examination has limitations in detecting extracapsular extension
    - MRI increasingly used for local staging assessment
    - Clinical understaging occurs in 20-30% of cases
    - Biochemical and pathologic staging provide additional information
    
    **Treatment Decision-Making Framework:**
    
    **Patient Factors:**
    - Age and life expectancy (treatment benefit requires >10 years)
    - Comorbidities and functional status
    - Patient preferences and quality of life priorities
    - Anxiety level and tolerance for uncertainty
    - Social support and follow-up compliance
    
    **Disease Factors:**
    - D'Amico risk group classification
    - Individual risk factors within group
    - Percent positive biopsies and tumor volume
    - PSA density and kinetics
    - Family history and genetic factors
    
    **Treatment Factors:**
    - Institutional expertise and technology availability
    - Side effect profiles and recovery considerations
    - Long-term surveillance requirements
    - Cost considerations and insurance coverage
    
    **Follow-up and Surveillance:**
    
    **Post-Treatment Monitoring:**
    - PSA surveillance is the cornerstone of follow-up
    - Digital rectal examination assesses local control
    - Biochemical recurrence typically precedes clinical recurrence
    - Salvage therapy options depend on initial treatment
    
    **Risk-Stratified Surveillance:**
    - **Low Risk:** PSA every 6 months × 2 years, then annually
    - **Intermediate Risk:** PSA every 3-6 months × 2 years, then every 6 months × 3 years
    - **High Risk:** PSA every 3 months × 2 years, then every 6 months with imaging
    
    **Active Surveillance Protocols:**
    - Reserved primarily for low-risk patients
    - Regular PSA monitoring, clinical assessment, and repeat biopsies
    - Triggers for treatment intervention include PSA kinetics, grade progression
    - Patient compliance and anxiety tolerance are crucial
    
    **Contemporary Considerations and Limitations:**
    
    **Strengths of D'Amico Classification:**
    - Simple, reproducible, and widely validated
    - Uses readily available clinical parameters
    - Excellent prognostic discrimination
    - Incorporated into major clinical guidelines
    - Facilitates research and clinical trial design
    
    **Limitations and Modern Refinements:**
    - Intermediate risk group is heterogeneous
    - Does not incorporate modern imaging (mpMRI) findings
    - Lacks genomic biomarker integration
    - Based on older patient cohorts and treatment techniques
    - May not reflect contemporary surgical and radiation advances
    
    **Emerging Risk Stratification Tools:**
    - CAPRA (University of California San Francisco Cancer of the Prostate Risk Assessment)
    - Genomic classifiers (Decipher, Prolaris, OncotypeDX)
    - mpMRI-based risk assessment
    - Artificial intelligence and machine learning models
    - Combined clinical-genomic nomograms
    
    **Quality of Life Considerations:**
    
    **Treatment-Related Side Effects:**
    - **Surgery:** Urinary incontinence, erectile dysfunction, surgical risks
    - **Radiation:** Urinary and bowel toxicity, fatigue, skin changes
    - **Hormonal Therapy:** Hot flashes, osteoporosis, metabolic changes, fatigue
    - **Active Surveillance:** Anxiety, repeat procedures, uncertainty
    
    **Shared Decision-Making:**
    - Comprehensive discussion of risks, benefits, and alternatives
    - Patient values and preferences integration
    - Quality of life vs. quantity of life considerations
    - Support for decision-making process and ongoing care
    
    **Implementation in Clinical Practice:**
    
    **Multidisciplinary Care:**
    - Urologist for surgical management and overall care coordination
    - Radiation oncologist for radiation therapy planning
    - Medical oncologist for systemic therapy considerations
    - Pathologist for accurate diagnosis and staging
    - Support services for patient education and navigation
    
    **Quality Metrics:**
    - Appropriate risk stratification documentation
    - Treatment selection aligned with risk group
    - Patient-reported outcome measures
    - Long-term biochemical control rates
    - Treatment-related complications and management
    
    **Future Directions:**
    
    **Precision Medicine Integration:**
    - Genomic biomarkers for treatment selection
    - Imaging biomarkers for active surveillance
    - Liquid biopsies for minimal residual disease detection
    - Personalized treatment algorithms
    
    **Treatment Advances:**
    - Focal therapy for selected low-risk patients
    - Hypofractionated radiation regimens
    - Novel systemic therapies for high-risk disease
    - Combination therapy optimization
    
    Args:
        request: D'Amico risk classification parameters including PSA level, 
                Gleason score, clinical stage, and optional patient factors
        
    Returns:
        DamicoRiskClassificationResponse: Comprehensive risk assessment including 
        risk group classification, biochemical recurrence risk, treatment 
        recommendations, and prognostic information
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("damico_risk_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating D'Amico Risk Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return DamicoRiskClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for D'Amico Risk Classification",
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