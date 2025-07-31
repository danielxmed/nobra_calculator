"""
Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria Router

Endpoint for calculating GELF criteria for follicular lymphoma treatment decisions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.gelf_criteria import (
    GelfCriteriaRequest,
    GelfCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gelf_criteria",
    response_model=GelfCriteriaResponse,
    summary="Calculate Groupe d'Etude des Lymphomes Folliculaires",
    description="Determines if immediate therapy for follicular lymphoma is needed by identifying high tumor burden patients requiring treatment rather than active surveillance",
    response_description="The calculated gelf criteria with interpretation",
    operation_id="gelf_criteria"
)
async def calculate_gelf_criteria(request: GelfCriteriaRequest):
    """
    Calculates Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria
    
    The GELF Criteria is a clinical decision tool developed to determine whether patients 
    with follicular lymphoma require immediate treatment or can be managed with active 
    surveillance (watch and wait approach). This assessment is crucial for optimizing 
    treatment decisions and avoiding unnecessary therapy in patients with low tumor burden.
    
    **Clinical Background**:
    Follicular lymphoma is an indolent B-cell non-Hodgkin lymphoma that often presents 
    in advanced stages but follows a variable clinical course. Many patients with low 
    tumor burden can be safely managed with active surveillance, while those with high 
    tumor burden require immediate treatment to prevent complications and optimize outcomes.
    
    **Historical Development**:
    The GELF criteria were originally developed by the Groupe d'Etude des Lymphomes 
    Folliculaires in 1997 to standardize treatment decisions in follicular lymphoma 
    and harmonize clinical trial populations. Despite being developed in the pre-rituximab 
    era, these criteria remain clinically relevant and widely used in current practice.
    
    **Nine GELF Criteria Parameters**:
    
    **Anatomical/Mass Effect Criteria**:
    1. **Tumor Mass >7cm**: Any single nodal or extranodal tumor mass >7 cm diameter
    2. **Multiple Large Nodes**: ≥3 nodal sites, each >3 cm diameter
    3. **Splenic Enlargement**: Splenomegaly with inferior margin below umbilical line
    4. **Compression Syndrome**: Ureteral, orbital, or gastrointestinal compression
    
    **Systemic Disease Criteria**:
    5. **B Symptoms**: Fever >38°C, night sweats, or weight loss >10% in 6 months
    6. **Serous Effusions**: Pleural or peritoneal effusion attributable to lymphoma
    
    **Hematologic/Leukemic Criteria**:
    7. **Leukemic Phase**: >5.0 × 10⁹/L circulating malignant cells
    8. **Granulocytopenia**: Absolute granulocyte count <1.0 × 10⁹/L
    9. **Thrombocytopenia**: Platelet count <100 × 10⁹/L
    
    **Clinical Decision Framework**:
    
    **Low Tumor Burden (No GELF Criteria)**:
    - **Management**: Active surveillance (watch and wait) is appropriate
    - **Monitoring**: Clinical assessment every 3-6 months, imaging every 6-12 months
    - **Outcomes**: Excellent overall survival with preserved quality of life
    - **Treatment Trigger**: Disease progression, transformation, or symptom development
    
    **High Tumor Burden (≥1 GELF Criteria)**:
    - **Management**: Immediate treatment recommended
    - **Treatment Options**: Rituximab-based regimens (R-CHOP, R-CVP, R-bendamustine)
    - **Approach**: Multidisciplinary team discussion for optimal treatment selection
    - **Considerations**: Patient age, comorbidities, performance status, preferences
    
    **Treatment Selection Guidelines**:
    
    **For Immediate Treatment**:
    - **R-CHOP**: Younger patients with good performance status requiring rapid response
    - **R-CVP**: Older patients or those with comorbidities limiting anthracycline use
    - **R-Bendamustine**: Excellent efficacy with favorable toxicity profile
    - **Radiation Therapy**: Selected cases with limited-stage disease
    
    **For Active Surveillance**:
    - **Initial Monitoring**: Every 3-4 months for first 2 years
    - **Extended Monitoring**: Every 6-12 months if stable disease
    - **Imaging Schedule**: CT every 6-12 months or when clinically indicated
    - **Laboratory Monitoring**: CBC to detect cytopenias or transformation
    
    **Prognostic Integration**:
    The GELF criteria should be used in conjunction with prognostic scoring systems:
    - **FLIPI (Follicular Lymphoma International Prognostic Index)**: Age, stage, hemoglobin, LDH, nodal areas
    - **FLIPI-2**: Beta-2 microglobulin, longest diameter, bone marrow involvement, hemoglobin, age
    - **Combined Assessment**: GELF for treatment timing, FLIPI/FLIPI-2 for long-term prognosis
    
    **Modern Clinical Context**:
    While GELF criteria provide standardized guidelines, recent studies demonstrate some 
    discordance between GELF criteria and actual treatment patterns in routine practice. 
    Clinicians often consider additional factors including:
    - Patient anxiety about surveillance vs. treatment toxicity concerns
    - Rate of disease progression and transformation risk
    - Comorbidities affecting treatment tolerance
    - Access to care and ability to comply with monitoring requirements
    - Quality of life considerations and patient preferences
    
    **Quality Measures and Outcomes**:
    - **Surveillance Success**: Majority of low-burden patients avoid treatment toxicity
    - **Treatment Efficacy**: High response rates with rituximab-based regimens
    - **Overall Survival**: Excellent long-term survival regardless of initial approach
    - **Quality of Life**: Preserved during surveillance, managed during treatment
    
    **Clinical Trial Implications**:
    GELF criteria continue to be used for clinical trial stratification and enrollment, 
    helping to standardize patient populations and enable meaningful comparison of 
    treatment outcomes across studies.
    
    **Important Clinical Considerations**:
    - GELF criteria should complement, not replace, clinical judgment
    - Regular reassessment is essential as clinical status may change
    - Patient preferences and values must be incorporated into final decisions
    - Consider second opinions for complex cases or borderline situations
    - Document rationale when deviating from GELF-based recommendations
    - Multidisciplinary team input enhances decision-making quality
    
    Args:
        request: GELF criteria parameters including all nine clinical assessments
        
    Returns:
        GelfCriteriaResponse: GELF assessment with treatment recommendations and clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gelf_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GELF Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return GelfCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GELF Criteria",
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