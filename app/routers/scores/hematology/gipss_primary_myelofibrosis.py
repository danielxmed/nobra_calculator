"""
GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis Router

Endpoint for calculating GIPSS score for primary myelofibrosis patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.gipss_primary_myelofibrosis import (
    GipssPrimaryMyelofibrosisRequest,
    GipssPrimaryMyelofibrosisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gipss_primary_myelofibrosis",
    response_model=GipssPrimaryMyelofibrosisResponse,
    summary="Calculate GIPSS - Genetically Inspired Prognostic Scoring...",
    description="The GIPSS is a genetically-based prognostic scoring system for primary myelofibrosis that relies exclusively on cytogenetic and molecular genetic markers. This system eliminates subjective clinical variables and provides more accurate risk stratification for treatment planning, particularly for allogeneic stem cell transplant decisions.",
    response_description="The calculated gipss primary myelofibrosis with interpretation",
    operation_id="gipss_primary_myelofibrosis"
)
async def calculate_gipss_primary_myelofibrosis(request: GipssPrimaryMyelofibrosisRequest):
    """
    Calculates GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis
    
    The GIPSS provides prognostic assessment for primary myelofibrosis patients based exclusively 
    on genetic markers, eliminating subjective clinical variables and providing objective risk 
    stratification for treatment planning decisions, particularly for allogeneic stem cell 
    transplant candidacy evaluation.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    Genetic-based prognostic assessment for primary myelofibrosis using cytogenetic and molecular 
    genetic markers to guide treatment decisions and transplant evaluation.
    
    **Key Clinical Advantages**:
    
    **Objective Assessment**:
    - Eliminates subjective clinical variables (constitutional symptoms, physical findings)
    - Provides reproducible, standardized risk assessment independent of clinical expertise
    - Can be performed on peripheral blood samples, avoiding bone marrow aspiration challenges
    - Particularly valuable in patients with dry bone marrow aspirations ("dry tap")
    
    **Evidence-Based Stratification**:
    - Derived from analysis of 641 primary myelofibrosis patients with robust validation
    - Four-tiered risk stratification with significantly different survival outcomes
    - Superior prognostic accuracy compared to DIPSS in cases of disagreement
    - Validated across multiple international cohorts with consistent performance
    
    **Treatment Decision Support**:
    - Identifies candidates for allogeneic stem cell transplant (high-risk disease)
    - Guides conservative management approach (low-risk disease with excellent prognosis)
    - Supports clinical trial enrollment and research stratification
    - Enables personalized treatment approach based on genetic risk profile
    
    **Genetic Components and Clinical Significance**:
    
    **Cytogenetic Risk Classification**:
    
    **Favorable Karyotype (0 points)**:
    - Normal karyotype (46,XX/XY) or isolated loss of chromosome Y
    - Associated with better overall survival and lower transformation risk
    - Present in approximately 70-80% of primary myelofibrosis patients
    - Generally indicates more indolent disease course
    
    **Unfavorable Karyotype (1 point)**:
    - All other cytogenetic abnormalities except very high-risk
    - Examples: +8, del(20q), del(13q), +9, isolated complex karyotypes
    - Intermediate prognostic impact with moderate survival reduction
    - Present in approximately 15-20% of patients
    
    **Very High-Risk Karyotype (2 points)**:
    - Monosomal karyotype, inv(3), i(17q), chromosome 12 abnormalities, 11q23 rearrangements
    - Associated with very poor survival and high acute leukemia transformation risk
    - Present in approximately 5-10% of patients
    - Strong indication for aggressive treatment including transplant evaluation
    
    **Molecular Genetic Markers**:
    
    **Type 1/like CALR Mutation**:
    - **Present (0 points)**: Protective factor associated with better survival
    - **Absent (1 point)**: Includes JAK2V617F-positive, MPL-positive, or triple-negative
    - CALR mutations associated with younger age, higher platelet count, better prognosis
    - Type 1 (52bp deletion) and type 1-like mutations in CALR exon 9
    
    **High Molecular Risk (HMR) Mutations**:
    - **ASXL1 Mutation (1 point)**: Chromatin remodeling gene, poor survival, transformation risk
    - **SRSF2 Mutation (1 point)**: RNA splicing factor, associated with poor outcomes
    - **U2AF1Q157 Mutation (1 point)**: Splicing factor, specific Q157 mutations adverse
    
    **Risk Stratification and Clinical Management**:
    
    **Low Risk (0 points) - Excellent Prognosis**:
    - **Population**: ~15% of patients with optimal genetic profile
    - **Survival**: Median 26.4 years, 5-year survival 94%
    - **Management**: Conservative approach with observation and symptom-directed therapy
    - **Monitoring**: Every 6-12 months with complete blood count and clinical assessment
    - **Transplant**: Not indicated unless disease progression occurs
    
    **Intermediate-1 Risk (1 point) - Good Prognosis**:
    - **Population**: ~40% of patients with single adverse genetic factor
    - **Survival**: Median 8.0 years, 5-year survival 73%
    - **Management**: Symptom-directed therapy with regular monitoring
    - **Treatment**: JAK inhibitors for symptomatic disease or splenomegaly
    - **Transplant**: Generally not indicated unless progression to higher risk
    
    **Intermediate-2 Risk (2 points) - Intermediate Prognosis**:
    - **Population**: ~30% of patients with moderate genetic risk burden
    - **Survival**: Median 4.2 years, 5-year survival 40%
    - **Management**: Active treatment with transplant evaluation consideration
    - **Treatment**: JAK inhibitors and evaluation of transplant candidacy
    - **Transplant**: Consider in appropriate candidates with good performance status
    
    **High Risk (3-6 points) - Poor Prognosis**:
    - **Population**: ~15% of patients with multiple adverse genetic factors
    - **Survival**: Median 2.0 years, 5-year survival 14%
    - **Management**: Aggressive treatment with urgent transplant evaluation
    - **Treatment**: JAK inhibitors for symptom control while pursuing transplant
    - **Transplant**: Strong indication if age and performance status appropriate
    
    **Clinical Decision Framework**:
    
    **Transplant Decision-Making**:
    - **High-Risk Disease**: Strong indication for allogeneic transplant evaluation
    - **Intermediate-2 Risk**: Consider transplant in younger, fit patients
    - **Lower Risk Categories**: Transplant not typically indicated
    - **Age Considerations**: Optimal candidates are typically <70 years with good performance status
    
    **Treatment Intensity Decisions**:
    - **Conservative Management**: Low-risk patients with excellent prognosis
    - **Moderate Intervention**: Intermediate-risk patients with symptom-directed therapy
    - **Aggressive Treatment**: High-risk patients requiring comprehensive supportive care
    - **Clinical Trials**: Appropriate for all risk categories with investigational approaches
    
    **Monitoring and Follow-up Strategy**:
    - **Risk-Based Frequency**: Higher risk categories require more frequent assessment
    - **Disease Progression**: Monitor for clinical and laboratory deterioration
    - **Transformation Surveillance**: Watch for acute leukemia transformation (blast increase)
    - **Molecular Evolution**: Consider repeat genetic testing if clinical changes occur
    
    **Quality of Life and Supportive Care**:
    - **Symptom Assessment**: Use validated tools like MPN-SAF symptom assessment form
    - **Functional Status**: ECOG performance status and activities of daily living
    - **Palliative Care**: Early integration in high-risk patients for symptom management
    - **Patient Education**: Genetic counseling and family screening considerations
    
    **Research and Clinical Trial Applications**:
    - **Risk Stratification**: Enrollment criteria and endpoint prediction for clinical trials
    - **Biomarker Development**: Framework for evaluating new prognostic markers
    - **Treatment Evaluation**: Assessment of therapeutic interventions across risk groups
    - **Population Studies**: Epidemiological research and disease surveillance applications
    
    Args:
        request: Patient genetic data including cytogenetic risk classification and molecular 
                mutation status (CALR, ASXL1, SRSF2, U2AF1Q157) required for GIPSS calculation
        
    Returns:
        GipssPrimaryMyelofibrosisResponse: GIPSS score with genetic component breakdown, 
                                          evidence-based survival predictions, and comprehensive 
                                          clinical management recommendations by risk category
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gipss_primary_myelofibrosis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GIPSS for Primary Myelofibrosis",
                    "details": {"parameters": parameters}
                }
            )
        
        return GipssPrimaryMyelofibrosisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GIPSS calculation",
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
                "message": "Internal error in GIPSS calculation",
                "details": {"error": str(e)}
            }
        )