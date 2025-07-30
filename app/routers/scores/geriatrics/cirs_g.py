"""
Cumulative Illness Rating Scale-Geriatric (CIRS-G) Router

Endpoint for calculating CIRS-G illness burden assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.cirs_g import (
    CirsGRequest,
    CirsGResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cirs_g", response_model=CirsGResponse)
async def calculate_cirs_g(request: CirsGRequest):
    """
    Calculates Cumulative Illness Rating Scale-Geriatric (CIRS-G)
    
    The CIRS-G is a validated comprehensive assessment tool that quantifies illness 
    burden in elderly patients by systematically rating the severity of medical 
    conditions across 13 organ systems. Each system is scored from 0 (no problem) 
    to 4 (extremely severe), providing a standardized measure of overall health 
    status and comorbidity burden.
    
    **Clinical Background:**
    
    Developed by Miller et al. based on the original Cumulative Illness Rating Scale 
    (Linn et al., 1968), the CIRS-G was specifically adapted for geriatric populations. 
    It provides a more comprehensive assessment of disease burden compared to other 
    comorbidity indices and has demonstrated good inter-rater reliability with 
    intraclass correlation coefficients ranging from 0.78 to 0.88.
    
    **Assessment Methodology:**
    
    The CIRS-G systematically evaluates 13 organ systems using standardized criteria:
    
    **Organ Systems Evaluated:**
    
    1. **Cardiovascular (Heart)**: Arrhythmias, congestive heart failure, coronary artery disease, 
       myocardial infarction, valvular disease
    
    2. **Vascular**: Hypertension, peripheral vascular disease, cerebrovascular disease, 
       aortic aneurysm, arterial stenosis
    
    3. **Hematopoietic**: Anemia, leukemia, lymphoma, bleeding disorders, blood clotting 
       disorders, thrombocytopenia
    
    4. **Respiratory**: COPD, asthma, pneumonia, lung cancer, pulmonary embolism, 
       restrictive lung disease
    
    5. **Eyes, Ears, Nose, Throat, Larynx (EENT)**: Vision problems, hearing loss, 
       ENT disorders, laryngeal problems
    
    6. **Upper Gastrointestinal**: Esophageal disorders, gastric ulcers, reflux disease, 
       gastritis, upper GI bleeding
    
    7. **Lower Gastrointestinal**: Inflammatory bowel disease, diverticulitis, colorectal 
       cancer, lower GI bleeding, bowel obstruction
    
    8. **Liver, Pancreas, Biliary**: Hepatitis, cirrhosis, pancreatitis, gallbladder disease, 
       pancreatic cancer
    
    9. **Renal**: Chronic kidney disease, acute kidney injury, nephrolithiasis, 
       glomerulonephritis, dialysis dependence
    
    10. **Genitourinary**: Prostate disease, urinary incontinence, sexual dysfunction, 
        reproductive system disorders
    
    11. **Musculoskeletal and Skin**: Arthritis, osteoporosis, fractures, skin disorders, 
        chronic wounds, connective tissue diseases
    
    12. **Neurologic**: Stroke, dementia, Parkinson's disease, seizure disorders, 
        peripheral neuropathy, spinal cord disorders
    
    13. **Endocrine and Breast**: Diabetes mellitus, thyroid disease, adrenal disorders, 
        breast cancer, other endocrine tumors
    
    **Scoring Criteria:**
    
    **0 - No Problem**: No disease or symptoms affecting this organ system
    
    **1 - Mild**: Mild disease with minimal symptoms or well-controlled conditions that 
    do not significantly impact daily functioning
    
    **2 - Moderate**: Moderate disease requiring ongoing medical management with some 
    functional limitation or impact on quality of life
    
    **3 - Severe**: Severe disease that significantly impacts daily activities and 
    requires intensive medical management
    
    **4 - Extremely Severe**: Life-threatening condition, end-stage disease, or 
    condition requiring immediate intervention
    
    **Calculated Indices:**
    
    **Total Score (0-52)**: Sum of all 13 organ system scores. Higher scores indicate 
    greater overall illness burden.
    
    **Severity Index**: Total score divided by the number of affected organ systems 
    (systems with score > 0). Provides average severity of affected systems.
    
    **Comorbidity Index**: Number of organ systems with scores ≥ 3. Indicates the 
    number of severely affected systems.
    
    **Clinical Interpretation:**
    
    **Low Burden (0-6 points):**
    - Minimal illness burden with few or mild medical conditions
    - Good overall health status and favorable prognosis
    - Low risk of adverse outcomes
    - Minimal care coordination needs
    
    **Mild Burden (7-12 points):**
    - Some health conditions but generally well-managed
    - Good prognosis with appropriate medical care
    - Basic to moderate care coordination needed
    - Regular monitoring recommended
    
    **Moderate Burden (13-20 points):**
    - Multiple health conditions or more severe single conditions
    - May impact daily activities and quality of life
    - Comprehensive care coordination important
    - Consider geriatric assessment
    
    **High Burden (21-30 points):**
    - Multiple severe conditions with significant functional impact
    - Requires intensive medical management
    - Multidisciplinary care approach recommended
    - Higher risk of adverse outcomes
    
    **Very High Burden (31-52 points):**
    - Extensive comorbidities with multiple severely affected systems
    - May indicate poor prognosis
    - Intensive multidisciplinary care required
    - Consider palliative care consultation
    
    **Clinical Applications:**
    
    **Comprehensive Geriatric Assessment:**
    - Systematic evaluation of elderly patients
    - Baseline health status documentation
    - Treatment planning and goal setting
    - Risk stratification for interventions
    
    **Hospital Medicine:**
    - Predicting length of stay and outcomes
    - Discharge planning and resource allocation
    - Identifying patients needing intensive services
    - Quality improvement initiatives
    
    **Research Applications:**
    - Standardized comorbidity measurement
    - Clinical trial eligibility and stratification
    - Outcome prediction modeling
    - Health services research
    
    **Comparison with Other Indices:**
    - May be more accurate than Charlson Comorbidity Index for geriatric patients
    - More comprehensive than simple disease counting methods
    - Better captures severity and functional impact
    - Useful complement to other geriatric assessment tools
    
    **Validation and Reliability:**
    
    **Inter-rater Reliability**: Good agreement between trained assessors (ICC 0.78-0.88)
    
    **Predictive Validity**: Validated for predicting:
    - Hospital mortality and morbidity
    - Length of hospital stay
    - Functional decline
    - Healthcare resource utilization
    - Need for discharge services
    
    **Clinical Utility**: 
    - Can be reliably assessed by medical students and residents
    - Useful for early identification of high-risk patients
    - Helps target medical care and resource allocation
    - Improves quality by identifying patient needs early
    
    **Implementation Considerations:**
    
    **Training Requirements:**
    - Healthcare professionals should receive training on scoring criteria
    - Familiarity with organ system classifications important
    - Regular calibration exercises to maintain reliability
    - Use of standardized scoring guidelines recommended
    
    **Documentation:**
    - Record scores with supporting clinical rationale
    - Note any factors influencing assessment
    - Update scores if clinical status changes significantly
    - Use for care planning and team communication
    
    **Quality Assurance:**
    - Consider second opinion for complex cases
    - Regular review of scoring consistency
    - Feedback and continuing education for assessors
    - Integration with electronic health records when possible
    
    Args:
        request: CIRS-G parameters including scores (0-4) for all 13 organ systems
        
    Returns:
        CirsGResponse: Comprehensive assessment including total score, calculated 
        indices, system analysis, burden categorization, clinical recommendations, 
        and care complexity assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cirs_g", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cumulative Illness Rating Scale-Geriatric",
                    "details": {"parameters": parameters}
                }
            )
        
        return CirsGResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cumulative Illness Rating Scale-Geriatric",
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