"""
WHO Diagnostic Criteria for Systemic Mastocytosis (2016) Router

Endpoint for WHO 2016 diagnostic criteria for systemic mastocytosis evaluation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.who_systemic_mastocytosis_criteria import (
    WhoSystemicMastocytosisCriteriaRequest,
    WhoSystemicMastocytosisCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/who_systemic_mastocytosis_criteria",
    response_model=WhoSystemicMastocytosisCriteriaResponse,
    summary="Calculate WHO 2016 Diagnostic Criteria for Systemic Mastocytosis",
    description="Evaluates systemic mastocytosis diagnosis using the World Health Organization 2016 "
                "diagnostic criteria. This systematic assessment tool requires either 1 major criterion "
                "+ 1 minor criterion OR 3 minor criteria for diagnosis confirmation. The major criterion "
                "focuses on multifocal mast cell infiltrates (≥15 cells in aggregates) in bone marrow "
                "and/or extracutaneous organs. The four minor criteria include: (1) Atypical mast cell "
                "morphology (≥25% spindle-shaped or type I/II forms); (2) KIT mutations at codon 816 "
                "(usually D816V) or other critical regions; (3) Aberrant CD expression (CD2/CD25/CD30); "
                "and (4) Elevated serum tryptase >20 ng/mL in absence of associated myeloid neoplasm. "
                "These criteria distinguish systemic mastocytosis from cutaneous mastocytosis and other "
                "mast cell disorders, enabling appropriate risk stratification, subtype classification, "
                "and specialized management including hematology-oncology referral for staging and "
                "treatment planning.",
    response_description="The diagnostic assessment with criteria fulfillment status, clinical interpretation, and comprehensive management recommendations",
    operation_id="who_systemic_mastocytosis_criteria"
)
async def calculate_who_systemic_mastocytosis_criteria(request: WhoSystemicMastocytosisCriteriaRequest):
    """
    Calculates WHO 2016 Diagnostic Criteria for Systemic Mastocytosis
    
    The World Health Organization 2016 diagnostic criteria for systemic mastocytosis provide 
    a systematic, evidence-based approach to diagnosing this clonal mast cell disorder 
    characterized by abnormal accumulation and activation of mast cells in various organs.
    
    Background and Clinical Context:
    
    Systemic mastocytosis (SM) is a rare clonal hematopoietic disorder characterized by 
    abnormal accumulation of mast cells in one or more extracutaneous organs, most commonly 
    bone marrow, liver, spleen, and lymph nodes. It affects approximately 1 in 100,000-300,000 
    people, with median age of diagnosis around 60 years. SM is distinct from cutaneous 
    mastocytosis, which is limited to skin involvement.
    
    Key Pathophysiology:
    - KIT D816V mutation present in >95% of adult SM patients
    - Constitutive KIT activation leads to mast cell proliferation and survival
    - Aberrant mast cell phenotype with CD2/CD25/CD30 expression
    - Elevated tryptase release from increased mast cell burden
    - Potential for mediator release causing systemic symptoms
    
    WHO 2016 Diagnostic Criteria:
    
    **DIAGNOSIS REQUIRES:** 1 major criterion + 1 minor criterion OR 3 minor criteria
    
    **Major Criterion:**
    
    1. **Multifocal Mast Cell Infiltrates:**
       - Dense infiltrates of mast cells (≥15 mast cells in aggregates)
       - Found in bone marrow biopsies and/or other extracutaneous organ sections
       - Evaluated by histopathology with CD117/tryptase immunohistochemistry
       
       *Clinical significance:* This pattern distinguishes systemic from cutaneous 
       mastocytosis and indicates clonal expansion beyond skin involvement
    
    **Minor Criteria:**
    
    1. **Atypical Mast Cell Morphology:**
       - ≥25% of mast cells are atypical (type I or II) on bone marrow smears
       - OR spindle-shaped mast cells in tissue infiltrates
       
       *Morphological features:* Type I cells have bilobed or irregularly shaped 
       nuclei; Type II cells have prominent nucleoli and hypogranular cytoplasm
    
    2. **KIT Mutations:**
       - KIT-activating point mutations at codon 816 (usually D816V)
       - OR other critical KIT regions with published transformative behavior
       
       *Molecular significance:* KIT D816V found in >95% of adult SM cases; 
       confers resistance to imatinib but sensitivity to newer KIT inhibitors
    
    3. **Aberrant CD Expression:**
       - Mast cells express CD2 and/or CD25 and/or CD30
       - In addition to normal mast cell markers (CD117, tryptase)
       - Detected by flow cytometry or immunohistochemistry
       
       *Immunophenotype significance:* CD25 most commonly positive (>90%), 
       followed by CD2; aberrant expression indicates clonality
    
    4. **Elevated Serum Tryptase:**
       - Baseline serum tryptase concentration >20 ng/mL
       - Only valid in absence of associated myeloid neoplasm
       - Normal range: <11.4 ng/mL
       
       *Biomarker significance:* Correlates with mast cell burden and disease 
       activity; useful for monitoring treatment response
    
    **Clinical Applications:**
    
    Diagnostic Assessment:
    - Systematic evaluation of suspected systemic mastocytosis
    - Differentiation from cutaneous mastocytosis and MCAS
    - Risk stratification and subtype classification
    - Guide treatment decisions and monitoring strategies
    
    Disease Subtypes:
    - Indolent SM: Most common, near-normal life expectancy
    - Smoldering SM: High mast cell burden, organomegaly
    - SM with associated hematologic neoplasm (SM-AHN)
    - Aggressive SM: Organ dysfunction, poor prognosis
    - Mast cell leukemia: Rare, very aggressive form
    
    **Management Implications by Diagnosis:**
    
    Confirmed SM Diagnosis:
    - Hematology-oncology referral for staging and subtype classification
    - Assess for organ involvement and functional impairment
    - Mediator symptom management (antihistamines, leukotriene antagonists)
    - Allergy/immunology consultation for anaphylaxis prevention
    - Monitor for disease progression and transformation
    - Consider targeted therapy for aggressive variants
    
    Probable SM (Partial Criteria):
    - Complete comprehensive diagnostic workup
    - Bone marrow biopsy with immunohistochemistry if not done
    - Molecular testing for KIT mutations
    - Flow cytometry for aberrant CD expression
    - Close monitoring of symptoms and biomarkers
    
    Criteria Not Met:
    - Consider cutaneous mastocytosis if skin involvement present
    - Evaluate for mast cell activation syndrome (MCAS)
    - Test for hereditary alpha-tryptasemia if tryptase elevated
    - Rule out other causes of elevated tryptase
    - Specialist consultation if clinical suspicion persists
    
    **Prognostic Considerations:**
    
    Overall Prognosis:
    - Indolent SM: Near-normal life expectancy with symptom management
    - Smoldering SM: Generally good prognosis with monitoring
    - Aggressive SM: Median survival 3.5 years without effective therapy
    - Mast cell leukemia: Median survival <6 months
    
    Prognostic Factors:
    - Disease subtype most important prognostic factor
    - Organ dysfunction and associated cytopenia indicate poor prognosis
    - High KIT D816V allele burden may correlate with aggressive disease
    - Response to therapy guides long-term outcomes
    
    **Important Clinical Limitations:**
    
    - Criteria designed specifically for systemic mastocytosis diagnosis
    - Bone marrow biopsy typically required for definitive diagnosis
    - KIT mutation testing must be performed in qualified molecular laboratory
    - Tryptase criterion invalid in presence of associated myeloid neoplasm
    - Clinical correlation always required - criteria supplement clinical judgment
    - Hereditary alpha-tryptasemia can mimic elevated tryptase
    
    **Quality Indicators:**
    
    - High sensitivity: Detects >95% of SM cases when properly applied
    - High specificity: Low false positive rate with strict criteria adherence
    - Reproducibility: Standardized criteria improve diagnostic consistency
    - Evidence-based: Developed through multicenter validation studies
    
    Args:
        request: Patient laboratory values, tissue findings, and molecular test results for WHO criteria evaluation
        
    Returns:
        WhoSystemicMastocytosisCriteriaResponse: Comprehensive diagnostic assessment with criteria breakdown and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("who_systemic_mastocytosis_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating WHO Systemic Mastocytosis Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return WhoSystemicMastocytosisCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for WHO systemic mastocytosis criteria calculation",
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
                "message": "Internal error in WHO systemic mastocytosis criteria calculation",
                "details": {"error": str(e)}
            }
        )