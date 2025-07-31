"""
Binet Staging System for Chronic Lymphocytic Leukemia (CLL) Router

Endpoint for calculating Binet staging for chronic lymphocytic leukemia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.binet_staging_cll import (
    BinetStagingCllRequest,
    BinetStagingCllResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/binet_staging_cll",
    response_model=BinetStagingCllResponse,
    summary="Calculate Binet Staging System for Chronic Lymphocytic Le...",
    description="Stages chronic lymphocytic leukemia based on lymphadenopathy areas and hematologic parameters to predict prognosis and guide treatment decisions",
    response_description="The calculated binet staging cll with interpretation",
    operation_id="binet_staging_cll"
)
async def calculate_binet_staging_cll(request: BinetStagingCllRequest):
    """
    Calculates Binet Staging System for Chronic Lymphocytic Leukemia (CLL)
    
    The Binet Staging System is the European standard for chronic lymphocytic leukemia 
    staging, developed by Jacques-Louis Binet and colleagues in 1981. It provides a 
    simple, reproducible classification based on physical examination and basic 
    laboratory tests, making it accessible worldwide without requiring imaging studies.
    
    **Historical Context:**
    - Developed to replace less standardized staging approaches
    - Based on multivariate survival analysis of 1,456 CLL patients
    - Comparable to the American Rai staging system developed around the same time
    - Remains the preferred staging system in European clinical practice
    
    **Clinical Assessment Framework:**
    
    **Five Lymphoid Areas Evaluated:**
    
    **1. Cervical Lymphadenopathy:**
    - Palpable lymph nodes in anterior and posterior cervical chains
    - May present as unilateral or bilateral involvement
    - Often the first site of lymphadenopathy in early CLL
    
    **2. Axillary Lymphadenopathy:**
    - Enlarged nodes in central, anterior, posterior, and lateral axillary groups
    - Assessed during systematic bilateral examination
    - May be associated with upper extremity lymphedema in advanced cases
    
    **3. Inguinal Lymphadenopathy:**
    - Horizontal and vertical groups of inguinal lymph nodes
    - Palpable nodes >1 cm diameter considered significant
    - May be associated with lower extremity symptoms
    
    **4. Splenomegaly:**
    - Spleen extending >2 cm below left costal margin on inspiration
    - May cause left upper quadrant pain, early satiety, or cytopenias
    - Confirms systemic disease involvement
    
    **5. Hepatomegaly:**
    - Liver extending >2 cm below right costal margin
    - May indicate advanced disease or portal involvement
    - Can contribute to cytopenias through sequestration
    
    **Hematologic Criteria:**
    
    **Anemia (Hemoglobin <10 g/dL):**
    - May result from bone marrow infiltration
    - Can indicate disease progression
    - Automatically classifies as Stage C regardless of lymphoid involvement
    
    **Thrombocytopenia (Platelets <100×10³/mm³):**
    - May result from bone marrow replacement or hypersplenism
    - Associated with increased bleeding risk
    - Automatically classifies as Stage C regardless of lymphoid involvement
    
    **Staging Classifications and Prognosis:**
    
    **Stage A (Low Risk):**
    - **Criteria**: <3 lymphoid areas involved + normal blood counts
    - **Prevalence**: ~60% of newly diagnosed patients
    - **Prognosis**: Median overall survival ~12 years
    - **Management**: Watchful waiting approach typically recommended
    - **Monitoring**: Annual assessments usually sufficient
    
    **Stage B (Intermediate Risk):**
    - **Criteria**: ≥3 lymphoid areas involved + normal blood counts
    - **Prevalence**: ~30% of newly diagnosed patients
    - **Prognosis**: Median overall survival ~7 years
    - **Management**: Closer monitoring required, earlier treatment consideration
    - **Monitoring**: Every 3-6 months with symptom assessment
    
    **Stage C (High Risk):**
    - **Criteria**: Anemia and/or thrombocytopenia (any lymphoid involvement)
    - **Prevalence**: ~10% of newly diagnosed patients
    - **Prognosis**: Median overall survival 2-4 years (historical data)
    - **Management**: Often requires immediate treatment consideration
    - **Monitoring**: Monthly assessments and aggressive intervention
    
    **Modern Clinical Considerations:**
    
    **Treatment Indications (iwCLL Guidelines):**
    - Progressive lymphadenopathy (>50% increase in 2 months)
    - Massive or progressive splenomegaly
    - Progressive anemia or thrombocytopenia
    - Autoimmune complications
    - Constitutional symptoms (fever, night sweats, weight loss)
    
    **Contemporary Therapeutic Options:**
    - **BTK Inhibitors**: Ibrutinib, acalabrutinib, zanubrutinib
    - **BCL-2 Inhibitor**: Venetoclax (often combined with anti-CD20 antibodies)
    - **Anti-CD20 Antibodies**: Rituximab, obinutuzumab
    - **Chemotherapy**: FCR, BR regimens (selected patients)
    
    **Prognostic Refinements:**
    
    **Molecular Markers (not in original Binet system):**
    - **17p deletion/TP53 mutations**: Poor prognosis, BTK inhibitor preferred
    - **11q deletion**: Intermediate-high risk, consider intensive therapy
    - **IGHV mutation status**: Unmutated = worse prognosis
    - **ZAP-70 expression**: High expression = more aggressive disease
    
    **Additional Risk Factors:**
    - **Age and fitness**: Influence treatment selection
    - **Comorbidities**: Affect treatment tolerance
    - **β2-microglobulin levels**: Correlate with tumor burden
    - **LDH elevation**: May indicate increased proliferative activity
    
    **Clinical Limitations and Modern Updates:**
    
    **Original Binet Limitations:**
    - Does not incorporate molecular/genetic risk factors
    - Survival estimates based on pre-targeted therapy era
    - Limited discrimination within Stage A patients
    - Does not account for disease kinetics
    
    **Contemporary Adaptations:**
    - International Workshop on CLL (iwCLL) guidelines incorporate Binet staging
    - Combined with molecular markers for refined prognostication
    - Used in clinical trial stratification
    - Integrated with treatment response criteria
    
    **Quality of Life Considerations:**
    - Stage A patients typically maintain good quality of life
    - Stage B patients may experience fatigue and lymphadenopathy symptoms
    - Stage C patients often have significant symptoms requiring intervention
    - Modern treatments generally well-tolerated with improved outcomes
    
    **Research and Future Directions:**
    - Integration of minimal residual disease (MRD) assessment
    - Development of time-dependent risk models
    - Incorporation of genomic complexity measures
    - Patient-reported outcome measures integration
    
    Args:
        request: Binet staging assessment parameters (lymphoid areas and blood counts)
        
    Returns:
        BinetStagingCllResponse: Binet stage with prognosis and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("binet_staging_cll", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Binet Staging for CLL",
                    "details": {"parameters": parameters}
                }
            )
        
        return BinetStagingCllResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Binet Staging CLL calculation",
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