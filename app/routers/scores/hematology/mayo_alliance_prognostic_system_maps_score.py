"""
Mayo Alliance Prognostic System (MAPS) Score Router

Endpoint for calculating MAPS score for systemic mastocytosis prognosis assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.mayo_alliance_prognostic_system_maps_score import (
    MayoAlliancePrognosticSystemMapsScoreRequest,
    MayoAlliancePrognosticSystemMapsScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mayo_alliance_prognostic_system_maps_score",
    response_model=MayoAlliancePrognosticSystemMapsScoreResponse,
    summary="Calculate Mayo Alliance Prognostic System (MAPS) Score",
    description="Calculates the Mayo Alliance Prognostic System (MAPS) Score for prognostic "
                "assessment of systemic mastocytosis using clinical and molecular parameters. "
                "This contemporary risk stratification tool was developed from analysis of 580 "
                "patients at Mayo Clinic to provide accurate survival prediction and guide "
                "treatment decisions in systemic mastocytosis management. The calculator uses "
                "five key parameters including WHO disease subtype, patient age, platelet count, "
                "serum alkaline phosphatase level, and presence of adverse mutations (ASXL1, "
                "RUNX1, NRAS) to generate a score from 0-6 points. Risk stratification includes "
                "low risk (≤2 points) with excellent prognosis and median survival of 198 months, "
                "intermediate risk (3-4 points) with variable outcomes, and high risk (≥5 points) "
                "with poor prognosis requiring aggressive intervention. The tool provides "
                "comprehensive prognostic information including survival estimates, management "
                "recommendations, monitoring guidelines, and treatment considerations tailored "
                "to each risk category for optimal patient care and counseling.",
    response_description="The calculated MAPS score with comprehensive risk stratification, survival estimates, and detailed management recommendations",
    operation_id="mayo_alliance_prognostic_system_maps_score"
)
async def calculate_mayo_alliance_prognostic_system_maps_score(request: MayoAlliancePrognosticSystemMapsScoreRequest):
    """
    Calculates Mayo Alliance Prognostic System (MAPS) Score
    
    The Mayo Alliance Prognostic System (MAPS) Score is a validated prognostic tool 
    for systemic mastocytosis that provides contemporary risk stratification using 
    both clinical and molecular parameters to accurately predict survival outcomes 
    and guide therapeutic decision-making.
    
    **Clinical Context and Disease Background:**
    
    **Systemic Mastocytosis Overview:**
    Systemic mastocytosis (SM) represents a heterogeneous group of clonal hematopoietic 
    disorders characterized by abnormal proliferation and accumulation of mast cells 
    in various organs, including bone marrow, liver, spleen, lymph nodes, and 
    gastrointestinal tract. The disease exhibits remarkable clinical diversity, 
    ranging from indolent forms with near-normal life expectancy to aggressive 
    variants associated with rapid progression and poor survival.
    
    **Historical Context and Need for MAPS:**
    Prior to MAPS development, prognosis in systemic mastocytosis was primarily 
    based on WHO morphologic classification, which, while important, provided 
    limited granular prognostic information within disease categories. The 
    increasing availability of molecular genetic information and recognition 
    of clinical factors affecting outcomes prompted development of more 
    sophisticated prognostic models.
    
    **MAPS Development and Validation:**
    
    **Study Population:**
    The MAPS Score was developed through retrospective analysis of 580 patients 
    with systemic mastocytosis seen at Mayo Clinic between 1968 and 2015. This 
    large, single-institution cohort provided comprehensive clinical, laboratory, 
    and molecular data with extended follow-up for survival analysis.
    
    **Statistical Methodology:**
    The development employed multivariable Cox proportional hazards modeling to 
    identify independent prognostic factors. Both clinical-only and hybrid 
    clinical-molecular models were developed, with the hybrid model showing 
    superior discrimination for survival prediction.
    
    **External Validation:**
    Multiple independent studies have validated MAPS performance across different 
    populations and healthcare systems, confirming its reproducibility and 
    clinical utility in diverse settings.
    
    **Detailed Parameter Analysis:**
    
    **1. SM Type (WHO Classification) - 0 or 2 points:**
    
    **Indolent/Smoldering SM (0 points):**
    - **Indolent SM (ISM)**: Most common subtype with excellent prognosis
    - **Smoldering SM (SSM)**: Intermediate behavior with stable clinical course
    - **Characteristics**: Preserved organ function, minimal cytopenias, slow progression
    - **Management**: Primarily symptomatic treatment and monitoring
    
    **Advanced SM (2 points):**
    - **Aggressive SM (ASM)**: Organ dysfunction without associated hematologic neoplasm
    - **SM with Associated Hematologic Neoplasm (SM-AHN)**: Concurrent myeloid malignancy
    - **Mast Cell Leukemia (MCL)**: Rare, highly aggressive variant with circulating mast cells
    - **Characteristics**: Organ dysfunction, cytopenias, rapid progression
    - **Management**: Requires systemic therapy and aggressive intervention
    
    **2. Age (>60 years) - 0 or 1 point:**
    
    **Physiological Considerations:**
    - **Immune Senescence**: Age-related decline in immune function affecting disease control
    - **Organ Reserve**: Decreased physiological reserve limiting treatment tolerance
    - **Comorbidity Burden**: Increased prevalence of cardiovascular, renal, and pulmonary disease
    - **Treatment Complications**: Higher risk of therapy-related toxicity and mortality
    
    **Clinical Implications:**
    - Influences treatment selection and intensity
    - Affects eligibility for aggressive interventions
    - Guides supportive care requirements
    - Impacts quality of life considerations
    
    **3. Platelet Count (<150 ×10⁹/L) - 0 or 1 point:**
    
    **Pathophysiology:**
    - **Bone Marrow Involvement**: Direct mast cell infiltration compromising hematopoiesis
    - **Hypersplenism**: Sequestration and destruction in enlarged spleen
    - **Cytokine Effects**: Inflammatory mediators suppressing platelet production
    - **Drug Effects**: Cytoreductive therapy causing thrombocytopenia
    
    **Clinical Significance:**
    - **Bleeding Risk**: Hemorrhagic complications with procedures and trauma
    - **Treatment Limitations**: Contraindications to certain therapies
    - **Disease Progression**: Marker of advanced disease and organ involvement
    - **Monitoring Requirements**: Need for frequent laboratory surveillance
    
    **4. Serum Alkaline Phosphatase (Elevated) - 0 or 1 point:**
    
    **Sources of Elevation:**
    - **Liver Involvement**: Hepatic mastocytosis with potential fibrosis
    - **Bone Disease**: Osteosclerosis, osteolysis, or mixed bone lesions
    - **Organ Dysfunction**: Secondary effects of mediator release
    - **Drug Effects**: Medication-induced hepatotoxicity
    
    **Clinical Correlations:**
    - **Organ Damage**: Indicates significant disease burden
    - **Functional Impairment**: May affect drug metabolism and clearance
    - **Monitoring Needs**: Regular assessment of organ function
    - **Treatment Planning**: Influences therapy selection and dosing
    
    **5. Adverse Mutations (ASXL1, RUNX1, NRAS) - 0 or 1 point:**
    
    **Molecular Pathogenesis:**
    - **ASXL1**: Chromatin remodeling gene associated with poor prognosis
    - **RUNX1**: Transcription factor critical for hematopoiesis
    - **NRAS**: RAS pathway oncogene promoting cellular proliferation
    
    **Clinical Implications:**
    - **Clonal Evolution**: Indicates genomic instability and disease progression
    - **Treatment Resistance**: May predict poor response to standard therapies
    - **Transformation Risk**: Associated with evolution to more aggressive disease
    - **Prognostic Information**: Provides additional survival prediction beyond clinical factors
    
    **Risk Stratification and Management:**
    
    **Low Risk (≤2 points) - Excellent Prognosis:**
    
    **Survival Outcomes:**
    - Median survival: 198 months (16.5 years)
    - 5-year survival rate: 99%
    - 10-year survival rate: >90%
    
    **Management Approach:**
    - **Monitoring Strategy**: Regular clinical assessments every 6-12 months
    - **Laboratory Surveillance**: Annual complete blood counts and chemistry panels
    - **Symptom Management**: Antihistamines, mast cell stabilizers as needed
    - **Lifestyle Counseling**: Trigger avoidance, emergency action plans
    - **Long-term Planning**: Focus on quality of life and symptom control
    
    **Treatment Indications:**
    - Symptomatic mediator-related symptoms
    - Progressive organomegaly
    - Increasing mast cell burden
    - Development of cytopenias
    
    **Intermediate Risk (3-4 points) - Variable Prognosis:**
    
    **Survival Outcomes:**
    - Median survival: 36-85 months (3-7 years)
    - 5-year survival rate: 50-91%
    - Wide variability based on specific risk factors
    
    **Management Approach:**
    - **Enhanced Monitoring**: Clinical assessments every 3-6 months
    - **Laboratory Studies**: Comprehensive panels every 3-6 months
    - **Imaging Studies**: Annual assessment of organ involvement
    - **Molecular Monitoring**: Periodic assessment of clonal markers
    - **Early Intervention**: Consider treatment before symptom development
    
    **Treatment Considerations:**
    - **Targeted Therapy**: KIT inhibitors for appropriate mutations
    - **Cytoreductive Agents**: Hydroxyurea, interferon-alpha, or cladribine
    - **Clinical Trials**: Enrollment in investigational studies
    - **Supportive Care**: Prophylactic measures for complications
    
    **High Risk (≥5 points) - Poor Prognosis:**
    
    **Survival Outcomes:**
    - Median survival: 12 months (1 year)
    - 5-year survival rate: 4-24%
    - Requires immediate aggressive intervention
    
    **Management Approach:**
    - **Urgent Consultation**: Immediate hematology/oncology referral
    - **Multidisciplinary Care**: Team approach with multiple specialists
    - **Aggressive Treatment**: Immediate initiation of systemic therapy
    - **Clinical Trials**: Priority enrollment in experimental protocols
    - **Palliative Planning**: Early palliative care consultation
    
    **Treatment Options:**
    - **KIT Inhibitors**: Midostaurin for KIT D816V mutations
    - **Intensive Chemotherapy**: AML-type regimens for eligible patients
    - **Stem Cell Transplant**: Allogeneic transplant evaluation
    - **Investigational Agents**: Novel targeted therapies in development
    - **Supportive Care**: Comprehensive symptom management
    
    **Clinical Decision Support and Implementation:**
    
    **Treatment Algorithm Integration:**
    The MAPS Score should be integrated into institutional treatment algorithms 
    and clinical pathways to ensure consistent application and optimal patient 
    outcomes. Regular reassessment is important as patient risk profiles may 
    change over time.
    
    **Multidisciplinary Care Coordination:**
    High-risk patients benefit from coordinated care involving hematology, 
    oncology, pathology, genetics, palliative care, and other specialists 
    as indicated by specific clinical circumstances.
    
    **Patient and Family Communication:**
    The MAPS Score provides an evidence-based framework for discussing prognosis 
    with patients and families, supporting informed decision-making about 
    treatment options, goals of care, and advance planning.
    
    **Quality Metrics and Outcomes:**
    
    **Performance Monitoring:**
    - Accuracy of risk stratification
    - Treatment response rates by risk category
    - Survival outcomes compared to predicted
    - Quality of life measures
    - Healthcare utilization patterns
    
    **Continuous Improvement:**
    - Regular review of scoring accuracy
    - Integration of new prognostic factors
    - Adaptation to evolving treatment options
    - Incorporation of patient-reported outcomes
    
    **Future Directions and Research:**
    
    **Emerging Prognostic Factors:**
    - Additional molecular markers (TET2, DNMT3A, IDH mutations)
    - Cytogenetic abnormalities
    - Serum biomarkers (tryptase, IL-6, TNF-α)
    - Imaging-based disease burden assessment
    
    **Treatment Integration:**
    - Response-adapted therapy based on MAPS risk
    - Combination treatment strategies
    - Minimal residual disease monitoring
    - Personalized medicine approaches
    
    **Technology Enhancement:**
    - Machine learning for prognostic refinement
    - Real-time risk assessment tools
    - Integration with electronic health records
    - Patient-facing mobile applications
    
    **References:**
    1. Pardanani A, Reichard KK, Zblewski D, Abdelrahman RA, Wassie EA, Koschmann J, 
       et al. Mayo alliance prognostic system for mastocytosis: clinical and hybrid 
       clinical-molecular models. Blood Adv. 2018 Nov 27;2(21):2964-2975.
    2. Valent P, Sotlar K, Blatt K, Hartmann K, Reiter A, Sadovnik I, et al. Proposed 
       diagnostic algorithm for patients with suspected mastocytosis: a proposal of 
       the European Competence Network on Mastocytosis. Allergy. 2014 Oct;69(10):1267-74.
    3. Sperr WR, Kundi M, Alvarez-Twose I, van Anrooij B, Oude Elberink JN, Gorska A, 
       et al. International prognostic scoring system for mastocytosis (IPSM): a 
       retrospective cohort study. Lancet Haematol. 2019 Nov;6(11):e638-e649.
    4. Arber DA, Orazi A, Hasserjian R, Thiele J, Borowitz MJ, Le Beau MM, et al. 
       The 2016 revision to the World Health Organization classification of myeloid 
       neoplasms and acute leukemia. Blood. 2016 May 19;127(20):2391-405.
    
    Args:
        request: MAPS Score parameters including SM type, age, platelet count, ALP level, and mutation status
        
    Returns:
        MayoAlliancePrognosticSystemMapsScoreResponse: Calculated MAPS score with comprehensive 
        risk assessment, survival estimates, and detailed management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mayo_alliance_prognostic_system_maps_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mayo Alliance Prognostic System (MAPS) Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MayoAlliancePrognosticSystemMapsScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mayo Alliance Prognostic System (MAPS) Score",
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