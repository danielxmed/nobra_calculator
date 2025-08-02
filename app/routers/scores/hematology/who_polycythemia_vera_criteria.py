"""
WHO Diagnostic Criteria for Polycythemia Vera (2016) Router

Endpoint for WHO 2016 diagnostic criteria for polycythemia vera evaluation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.who_polycythemia_vera_criteria import (
    WhoPolycythemiaVeraCriteriaRequest,
    WhoPolycythemiaVeraCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/who_polycythemia_vera_criteria",
    response_model=WhoPolycythemiaVeraCriteriaResponse,
    summary="Calculate WHO 2016 Diagnostic Criteria for Polycythemia Vera",
    description="Evaluates polycythemia vera diagnosis using the World Health Organization 2016 "
                "diagnostic criteria. This systematic assessment tool requires either 3 major criteria "
                "OR 2 major criteria + 1 minor criterion for diagnosis confirmation. The 2016 WHO criteria "
                "represent a significant revision from the 2008 criteria, with lowered hemoglobin thresholds "
                "and introduction of hematocrit cutoffs to detect 'masked polycythemia vera' cases that were "
                "previously missed. Major criteria include: (1) Hemoglobin >16.5 g/dL (men) or >16.0 g/dL "
                "(women) OR Hematocrit >49% (men) or >48% (women) OR elevated red cell mass >25% above normal; "
                "(2) Bone marrow hypercellularity with trilineage growth and pleomorphic megakaryocytes; "
                "(3) JAK2V617F or JAK2 exon 12 mutation. The minor criterion is subnormal serum erythropoietin "
                "level. These criteria provide systematic diagnostic assessment with high sensitivity and "
                "specificity for polycythemia vera, enabling early diagnosis and appropriate management "
                "initiation including phlebotomy, cytoreductive therapy consideration, and thrombotic risk "
                "reduction strategies.",
    response_description="The diagnostic assessment with criteria fulfillment status, clinical interpretation, and comprehensive management recommendations",
    operation_id="who_polycythemia_vera_criteria"
)
async def calculate_who_polycythemia_vera_criteria(request: WhoPolycythemiaVeraCriteriaRequest):
    """
    Calculates WHO 2016 Diagnostic Criteria for Polycythemia Vera
    
    The World Health Organization 2016 diagnostic criteria for polycythemia vera provide 
    a systematic, evidence-based approach to diagnosing this Philadelphia chromosome-negative 
    myeloproliferative neoplasm. These criteria were significantly revised from the 2008 
    version to improve diagnostic sensitivity and detect previously missed cases.
    
    Background and Clinical Context:
    
    Polycythemia vera (PV) is a clonal hematopoietic stem cell disorder characterized by 
    increased red blood cell production. It belongs to the Philadelphia chromosome-negative 
    myeloproliferative neoplasms (MPNs) along with essential thrombocythemia and primary 
    myelofibrosis. PV affects approximately 2-3 per 100,000 people annually, with peak 
    incidence in the sixth decade of life.
    
    Key Pathophysiology:
    - JAK2V617F mutation present in ~95% of PV patients
    - JAK2 exon 12 mutations in ~3% of PV patients
    - Constitutive activation of JAK-STAT signaling pathway
    - Autonomous erythropoiesis independent of erythropoietin stimulation
    - Trilineage myeloproliferation with erythroid predominance
    
    WHO 2016 Diagnostic Criteria:
    
    **DIAGNOSIS REQUIRES:** 3 major criteria OR 2 major + 1 minor criterion
    
    **Major Criteria:**
    
    1. **Hemoglobin/Hematocrit/Red Cell Mass Threshold:**
       - Hemoglobin >16.5 g/dL (men) or >16.0 g/dL (women), OR
       - Hematocrit >49% (men) or >48% (women), OR
       - Red cell mass >25% above mean normal predicted value
       
       *Rationale:* 2016 criteria lowered hemoglobin thresholds from 2008 
       (previously >18.5 g/dL men, >16.5 g/dL women) to detect masked PV
    
    2. **Bone Marrow Hypercellularity:**
       - Age-adjusted hypercellularity with trilineage growth
       - Prominent erythroid, granulocytic, and megakaryocytic proliferation
       - Pleomorphic, mature megakaryocytes (distinguishes from ET and PMF)
       
       *Rationale:* Elevated from minor to major criterion in 2016 due to 
       increasing recognition of morphologic importance in PV diagnosis
    
    3. **JAK2 Mutation:**
       - JAK2V617F mutation (found in ~95% of PV patients), OR
       - JAK2 exon 12 mutation (found in ~3% of PV patients)
       
       *Clinical significance:* JAK2 mutations are driver mutations that 
       cause constitutive JAK-STAT activation and autonomous cell growth
    
    **Minor Criterion:**
    
    1. **Subnormal Serum Erythropoietin (EPO) Level:**
       - Helps distinguish primary (PV) from secondary polycythemia
       - In PV, EPO is typically suppressed due to autonomous red cell production
       - Elevated EPO suggests secondary polycythemia (hypoxic conditions, tumors)
    
    **Significant Changes from WHO 2008 Criteria:**
    
    1. **Lowered Hemoglobin Thresholds:** Reduced false negative rate by ~46%
    2. **Hematocrit Criteria Addition:** Alternative to hemoglobin measurement
    3. **Bone Marrow Elevation:** From minor to major criterion status
    4. **EPO Reclassification:** From major to minor criterion
    5. **Enhanced Sensitivity:** Better detection of masked PV cases
    
    **Clinical Applications:**
    
    Diagnostic Assessment:
    - Systematic evaluation of suspected polycythemia vera
    - Differentiation from secondary polycythemia causes
    - Risk stratification for thrombotic complications
    - Guide treatment initiation and monitoring strategies
    
    Risk Stratification:
    - Age >60 years and/or history of thrombosis = high risk
    - Younger patients without thrombosis history = low risk
    - JAK2 allele burden may correlate with thrombotic risk
    
    **Management Implications by Diagnosis:**
    
    Confirmed PV Diagnosis:
    - Therapeutic phlebotomy to maintain hematocrit <45% (men and women)
    - Low-dose aspirin (81-100 mg daily) unless contraindicated
    - Cytoreductive therapy for high-risk patients (hydroxyurea first-line)
    - Regular monitoring for disease progression and complications
    - Specialist hematology-oncology care coordination
    
    Probable PV (Partial Criteria):
    - Complete missing diagnostic workup (EPO, bone marrow, JAK2)
    - Hematology consultation for expert evaluation
    - Symptomatic management with phlebotomy if indicated
    - Close monitoring of hematologic parameters
    
    Criteria Not Met:
    - Investigate secondary causes of erythrocytosis
    - Consider sleep apnea, pulmonary disease, renal pathology
    - Evaluate medication effects and smoking history
    - Rule out relative polycythemia (dehydration, stress)
    
    **Prognostic Considerations:**
    
    Natural History:
    - Median survival >20 years with appropriate treatment
    - Thrombotic complications are leading cause of morbidity/mortality
    - Transformation risk: myelofibrosis (~15% at 15 years), acute leukemia (~2-5% at 20 years)
    - Quality of life significantly improved with modern management
    
    **Important Clinical Limitations:**
    
    - Criteria designed specifically for polycythemia vera diagnosis
    - Bone marrow biopsy expertise required for accurate morphologic assessment
    - JAK2 mutation testing must be performed in qualified molecular laboratory
    - EPO levels can be influenced by various factors (kidney disease, medications)
    - Clinical correlation always required - criteria supplement, not replace, judgment
    
    **Quality Indicators:**
    
    - High sensitivity: Detects >95% of PV cases when properly applied
    - High specificity: Low false positive rate when criteria strictly followed
    - Reproducibility: Standardized criteria improve diagnostic consistency
    - Evidence-based: Developed through large multicenter validation studies
    
    Args:
        request: Patient laboratory values and diagnostic test results for WHO criteria evaluation
        
    Returns:
        WhoPolycythemiaVeraCriteriaResponse: Comprehensive diagnostic assessment with criteria breakdown and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("who_polycythemia_vera_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating WHO Polycythemia Vera Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return WhoPolycythemiaVeraCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for WHO PV criteria calculation",
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
                "message": "Internal error in WHO PV criteria calculation",
                "details": {"error": str(e)}
            }
        )