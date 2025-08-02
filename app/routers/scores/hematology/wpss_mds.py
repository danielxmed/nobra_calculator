"""
WPSS (WHO classification-based Prognostic Scoring System) for MDS Router

Endpoint for WPSS calculation for myelodysplastic syndrome prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.wpss_mds import (
    WpssMdsRequest,
    WpssMdsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/wpss_mds",
    response_model=WpssMdsResponse,
    summary="Calculate WPSS for Myelodysplastic Syndrome",
    description="Calculates the WPSS (WHO classification-based Prognostic Scoring System) for "
                "myelodysplastic syndrome prognosis assessment. This time-dependent prognostic "
                "scoring system combines WHO morphological classification, cytogenetic risk category, "
                "and transfusion requirement to stratify patients into five distinct risk groups "
                "(Very Low, Low, Intermediate, High, Very High) with significantly different overall "
                "survival and probability of leukemic evolution. The WPSS provides dynamic prognostic "
                "assessment throughout the disease course, unlike static scoring systems, making it "
                "valuable for treatment planning, monitoring disease progression, and guiding clinical "
                "decision-making in hematology and oncology practice.",
    response_description="The calculated WPSS score with risk stratification, survival estimates, and comprehensive clinical management recommendations",
    operation_id="wpss_mds"
)
async def calculate_wpss_mds(request: WpssMdsRequest):
    """
    Calculates WPSS (WHO classification-based Prognostic Scoring System) for Myelodysplastic Syndrome
    
    The WPSS is a time-dependent prognostic scoring system developed by Malcovati et al. 
    that provides dynamic prognostic assessment for patients with myelodysplastic syndrome (MDS). 
    This system revolutionized MDS prognostication by incorporating WHO morphological 
    classification and allowing recalculation throughout the disease course.
    
    Background and Clinical Context:
    
    Myelodysplastic syndromes are a heterogeneous group of clonal hematopoietic stem cell 
    disorders characterized by dysplastic changes in bone marrow cells, peripheral blood 
    cytopenias, and risk of transformation to acute myeloid leukemia. MDS primarily affects 
    older adults with a median age of 70 years and represents one of the most common 
    hematologic malignancies in this population.
    
    Key Pathophysiology:
    - Clonal hematopoietic stem cell disorder with ineffective hematopoiesis
    - Progressive accumulation of genetic abnormalities
    - Dysplastic changes in all myeloid lineages
    - Variable risk of leukemic transformation (10-30% of patients)
    - Bone marrow failure leading to cytopenias and clinical complications
    
    **WPSS SCORING SYSTEM:**
    
    **Component 1: WHO Morphological Classification (0-3 points)**
    
    The WHO classification system categorizes MDS based on blast percentage, 
    dysplastic changes, and specific morphological features:
    
    **0 Points - Lower Risk Subtypes:**
    
    1. **Refractory Anemia (RA):**
       - <5% blasts in bone marrow, <1% in peripheral blood
       - Unilineage dysplasia limited to erythroid lineage
       - No ring sideroblasts (<15% of erythroid precursors)
       - Generally indolent course with low transformation risk
    
    2. **Refractory Anemia with Ring Sideroblasts (RARS):**
       - <5% blasts in bone marrow, <1% in peripheral blood
       - ≥15% ring sideroblasts of erythroid precursors
       - Unilineage dysplasia (erythroid only)
       - Often associated with SF3B1 mutations
    
    3. **MDS with Isolated del(5q):**
       - <5% blasts in bone marrow, <1% in peripheral blood
       - Isolated deletion 5q cytogenetic abnormality
       - Macrocytic anemia, normal to elevated platelet count
       - Excellent response to lenalidomide therapy
    
    **1 Point - Intermediate Risk Subtype:**
    
    4. **Refractory Cytopenia with Multilineage Dysplasia (RCMD):**
       - <5% blasts in bone marrow, <1% in peripheral blood
       - Dysplasia in ≥10% of cells in 2 or more myeloid lineages
       - Bicytopenia or pancytopenia common
       - Higher transformation risk than unilineage variants
    
    **2 Points - Higher Risk Subtype:**
    
    5. **Refractory Anemia with Excess Blasts-1 (RAEB-1):**
       - 2-4% blasts in peripheral blood OR 5-9% blasts in bone marrow
       - No Auer rods present
       - Unilineage or multilineage dysplasia
       - Intermediate transformation risk
    
    **3 Points - Highest Risk Subtype:**
    
    6. **Refractory Anemia with Excess Blasts-2 (RAEB-2):**
       - 5-19% blasts in peripheral blood OR 10-19% blasts in bone marrow
       - Auer rods may be present
       - Highest transformation risk among MDS subtypes
       - Often requires aggressive treatment approach
    
    **Component 2: Cytogenetic Risk Category (0-2 points)**
    
    Cytogenetics represent the most important prognostic factor in MDS:
    
    **0 Points - Good Risk Cytogenetics:**
    - Normal karyotype (46,XY or 46,XX)
    - Isolated -Y (loss of Y chromosome)
    - Isolated del(5q) (deletion 5q31-33)
    - Isolated del(20q) (deletion 20q11-13)
    
    These abnormalities are associated with:
    - Better overall survival
    - Lower risk of leukemic transformation
    - Better response to therapy
    - More indolent disease course
    
    **1 Point - Intermediate Risk Cytogenetics:**
    - All other single or double abnormalities not classified as good or poor
    - +8 (trisomy 8) - most common abnormality
    - +19 (trisomy 19)
    - i(17q) (isochromosome 17q)
    - +21 (trisomy 21)
    - Other balanced translocations
    
    **2 Points - Poor Risk Cytogenetics:**
    - Complex karyotype (≥3 unrelated abnormalities)
    - Chromosome 7 abnormalities (-7, del(7q))
    - inv(3)(q21q26) or t(3;3)(q21;q26)
    - -7/del(7q) with additional abnormalities
    - Complex abnormalities involving 5q
    
    Poor risk cytogenetics indicate:
    - Aggressive disease behavior
    - Higher likelihood of treatment resistance
    - Rapid progression to AML
    - Significantly shortened survival
    
    **Component 3: Transfusion Requirement (0-1 points)**
    
    **0 Points - No Regular Transfusion Requirement:**
    - Hemoglobin levels maintained without regular transfusions
    - Occasional or no transfusion support needed
    - Generally indicates better bone marrow reserve
    
    **1 Point - Regular Transfusion Requirement:**
    - ≥1 RBC transfusion every 8 weeks over a 4-month period
    - Indicates significant anemia and bone marrow failure
    - Associated with iron overload complications
    - Predictor of decreased quality of life and survival
    
    Transfusion dependency implications:
    - Iron overload leading to organ dysfunction
    - Increased infection risk
    - Alloimmunization complications
    - Reduced quality of life
    - Independent adverse prognostic factor
    
    **WPSS RISK STRATIFICATION:**
    
    **Very Low Risk (0 points):**
    - Median overall survival: 141 months (11.8 years)
    - 25% risk of AML transformation at 10 years
    - Management: Watch and wait, supportive care
    - Prognosis: Excellent, near-normal life expectancy
    
    **Low Risk (1 point):**
    - Median overall survival: 66 months (5.5 years)
    - 35% risk of AML transformation at 10 years
    - Management: Regular monitoring, ESAs, supportive care
    - Prognosis: Good, prolonged survival expected
    
    **Intermediate Risk (2 points):**
    - Median overall survival: 48 months (4 years)
    - 50% risk of AML transformation at 10 years
    - Management: Consider early intervention, hypomethylating agents
    - Prognosis: Moderate, treatment may improve outcomes
    
    **High Risk (3-4 points):**
    - Median overall survival: 26 months (2.2 years)
    - 70% risk of AML transformation at 5 years
    - Management: Intensive treatment, transplant evaluation
    - Prognosis: Poor, aggressive intervention needed
    
    **Very High Risk (5-6 points):**
    - Median overall survival: 9 months
    - 85% risk of AML transformation at 3 years
    - Management: Urgent intensive treatment, palliation consideration
    - Prognosis: Very poor, limited treatment options
    
    **Clinical Applications and Treatment Implications:**
    
    **Low Risk Disease Management:**
    - Watch and wait approach with regular monitoring
    - Supportive care for symptomatic anemia
    - ESAs (erythropoiesis-stimulating agents) for anemia
    - Iron chelation if transfusion dependent
    - Quality of life optimization
    - Clinical trial participation for novel agents
    
    **Intermediate Risk Disease Management:**
    - Close monitoring with consideration for early intervention
    - Hypomethylating agents (azacitidine, decitabine)
    - Lenalidomide for del(5q) patients
    - Clinical trials for combination therapies
    - Support care optimization
    - Regular assessment for disease progression
    
    **High Risk Disease Management:**
    - Urgent hematology-oncology consultation
    - Intensive treatment strategies
    - Hypomethylating agents as first-line therapy
    - Allogeneic stem cell transplantation evaluation
    - Clinical trials for investigational agents
    - Aggressive supportive care
    - Psychosocial support and advance care planning
    
    **Advantages of WPSS over Other Scoring Systems:**
    
    **Dynamic Assessment:**
    - Can be calculated at any time during disease course
    - Reflects disease evolution and treatment effects
    - Not limited to time of diagnosis like IPSS
    - Accounts for transfusion dependency development
    
    **WHO Classification Integration:**
    - Uses contemporary WHO morphological criteria
    - Better reflects biological behavior
    - More accurate prognostic discrimination
    - Standardized worldwide classification system
    
    **Clinical Validation:**
    - Extensively validated in multiple international cohorts
    - Superior prognostic accuracy compared to IPSS
    - Validated across different treatment modalities
    - Correlates with quality of life measures
    
    **Treatment Decision Support:**
    - Guides selection of appropriate therapeutic strategies
    - Helps determine timing of interventions
    - Assists in transplant candidacy assessment
    - Supports clinical trial enrollment decisions
    
    **Limitations and Considerations:**
    
    **Molecular Markers:**
    - Does not incorporate somatic mutations
    - Newer systems (IPSS-R, IPSS-M) include molecular data
    - Consider molecular testing for comprehensive assessment
    
    **Patient-Specific Factors:**
    - Age and performance status affect treatment decisions
    - Comorbidities influence therapeutic options
    - Patient preferences impact management choices
    
    **Treatment Effects:**
    - Score may change with therapy
    - Response to treatment affects prognosis
    - Regular reassessment recommended
    
    **Quality Indicators:**
    
    - High prognostic accuracy (C-index >0.70)
    - Reproducible results across institutions
    - Clinically meaningful risk stratification
    - Evidence-based treatment recommendations
    
    Args:
        request: WHO category, cytogenetic risk, and transfusion requirement for WPSS calculation
        
    Returns:
        WpssMdsResponse: WPSS score with comprehensive prognostic assessment and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("wpss_mds", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating WPSS for MDS",
                    "details": {"parameters": parameters}
                }
            )
        
        return WpssMdsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for WPSS calculation",
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
                "message": "Internal error in WPSS calculation",
                "details": {"error": str(e)}
            }
        )