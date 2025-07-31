"""
Charlson Comorbidity Index (CCI) Router

Endpoint for calculating Charlson Comorbidity Index for 10-year survival prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.charlson_comorbidity_index import (
    CharlsonComorbidityIndexRequest,
    CharlsonComorbidityIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/charlson_comorbidity_index",
    response_model=CharlsonComorbidityIndexResponse,
    summary="Calculate Charlson Comorbidity Index (CCI)",
    description="Predicts 10-year survival in patients with multiple comorbidities. Uses 19 weighted comorbidity categories plus age adjustment to estimate mortality risk and guide clinical decision-making.",
    response_description="The calculated charlson comorbidity index with interpretation",
    operation_id="charlson_comorbidity_index"
)
async def calculate_charlson_comorbidity_index(request: CharlsonComorbidityIndexRequest):
    """
    Calculates Charlson Comorbidity Index (CCI) for 10-Year Survival Prediction
    
    The Charlson Comorbidity Index is a widely validated prognostic tool that predicts 
    10-year mortality in patients with multiple comorbid conditions. Developed in 1987 
    by Charlson et al., it has become the gold standard for comorbidity assessment in 
    clinical practice and research.
    
    **CCI Overview and Purpose**:
    
    **Primary Function**: 
    - Predict 10-year survival probability based on age and comorbidity burden
    - Quantify overall health status using weighted disease categories
    - Guide clinical decision-making regarding treatment intensity and prognosis
    
    **Development and Validation**:
    - Originally developed in 1987 from 559 medical patients
    - Validated across multiple populations and healthcare systems
    - Maximum possible score of 37 points
    - Widely adapted for use with ICD-9 and ICD-10 coding systems
    
    **Scoring System Components**:
    
    **Age Adjustment** (Systematic Impact):
    - **<50 years**: 0 points (minimal age-related mortality risk)
    - **50-59 years**: 1 point (slight increase in baseline risk)
    - **60-69 years**: 2 points (moderate age-related risk)
    - **70-79 years**: 3 points (significant age-related risk)
    - **≥80 years**: 4 points (maximum age adjustment)
    
    **1-Point Comorbidities** (Moderate Mortality Impact):
    
    1. **Myocardial Infarction**
       - History of heart attack with ECG, enzyme, or imaging documentation
       - Includes both STEMI and NSTEMI
       - Prior silent MI counts if clinically documented
    
    2. **Congestive Heart Failure**
       - Clinical syndrome regardless of ejection fraction
       - Both systolic and diastolic heart failure
       - Requires clinical documentation or objective evidence
    
    3. **Peripheral Vascular Disease**
       - Aortic aneurysm, peripheral arterial disease, claudication
       - Documented by imaging, physical exam, or ABI
       - History of revascularization procedures
    
    4. **Cerebrovascular Disease**
       - Stroke (ischemic/hemorrhagic) or TIA with sequelae
       - Documented neurological deficits or imaging changes
       - Both completed stroke and TIA with residual effects
    
    5. **Dementia**
       - Chronic cognitive impairment affecting daily function
       - Alzheimer's disease, vascular dementia, other dementias
       - Clinical diagnosis beyond mild cognitive impairment
    
    6. **Chronic Pulmonary Disease**
       - COPD, chronic bronchitis, emphysema, severe asthma
       - Chronic symptoms and/or objective testing abnormalities
       - Chronic oxygen dependence or systemic steroid use
    
    7. **Connective Tissue Disease**
       - SLE, rheumatoid arthritis, systemic sclerosis
       - Polymyositis, dermatomyositis, mixed CTD
       - Systemic manifestations required
    
    8. **Peptic Ulcer Disease**
       - History of peptic/duodenal ulcer requiring treatment
       - Includes bleeding, perforation, or other complications
       - H. pylori treatment history qualifies
    
    9. **Mild Liver Disease** (1 point)
       - Chronic hepatitis without portal hypertension
       - Compensated cirrhosis
       - Hepatitis B/C without complications
    
    10. **Uncomplicated Diabetes** (1 point)
        - Type 1 or Type 2 without end-organ damage
        - Well-controlled diabetes without complications
        - Excludes gestational diabetes history
    
    **2-Point Comorbidities** (Significant Mortality Impact):
    
    1. **Hemiplegia/Paraplegia**
       - Paralysis from stroke, spinal cord injury, or other cause
       - Must have persistent neurological deficit
       - Includes both complete and incomplete paralysis
    
    2. **Moderate to Severe Chronic Kidney Disease**
       - eGFR <60 mL/min/1.73m² (CKD stages 3-5)
       - Dialysis dependence or end-stage renal disease
       - Kidney transplant recipients
    
    3. **Diabetes with End-Organ Damage** (2 points)
       - Diabetic retinopathy, nephropathy, or neuropathy
       - History of diabetic ketoacidosis or hyperosmolar coma
       - Insulin-dependent diabetes with complications
    
    4. **Localized Solid Tumor**
       - Cancer without evidence of metastasis
       - Tumors treated with curative intent
       - Active disease or remission <5 years
    
    5. **Leukemia**
       - Acute or chronic leukemia (lymphocytic or myeloid)
       - Active treatment or remission phase
       - All leukemia subtypes included
    
    6. **Lymphoma**
       - Hodgkin's or non-Hodgkin's lymphoma
       - Multiple myeloma typically included
       - Active disease or treatment phase
    
    **3-Point Comorbidity** (Major Mortality Impact):
    
    **Moderate to Severe Liver Disease** (3 points)
    - Cirrhosis with portal hypertension, varices, or ascites
    - Hepatic encephalopathy or hepatorenal syndrome
    - Liver transplant recipients
    - Significantly decompensated liver function
    
    **6-Point Comorbidities** (Severe Mortality Impact):
    
    1. **Metastatic Solid Tumor**
       - Cancer with distant metastases (Stage IV)
       - Significantly impacts life expectancy
       - Any solid tumor with distant spread
    
    2. **AIDS**
       - HIV with opportunistic infections or CD4 <200
       - AIDS-defining illnesses present
       - HIV alone without AIDS does not qualify
    
    **10-Year Survival Calculation**:
    
    **Mathematical Formula**: 
    10-year survival probability = 0.983^(CCI score × 0.9)
    
    **Interpretation Framework**:
    - Formula assumes theoretical low-risk population with 98.3% baseline survival
    - Exponential relationship between score and mortality risk
    - Higher scores indicate progressively worse prognosis
    
    **Risk Stratification and Clinical Interpretation**:
    
    **Low Risk (Score 0-1)**:
    - **Survival**: >90% 10-year survival
    - **Clinical Approach**: Aggressive screening, prevention, intensive treatments
    - **Prognosis**: Excellent, minimal comorbidity impact
    - **Decision-Making**: Standard of care, consider all interventions
    
    **Moderate Risk (Score 2-3)**:
    - **Survival**: 70-90% 10-year survival
    - **Clinical Approach**: Standard screening, individualized treatment decisions
    - **Prognosis**: Good, moderate comorbidity impact
    - **Decision-Making**: Balance benefits/risks, consider patient preferences
    
    **High Risk (Score 4-5)**:
    - **Survival**: 30-70% 10-year survival
    - **Clinical Approach**: Selective screening, focus on proven short-term benefits
    - **Prognosis**: Reduced, significant comorbidity impact
    - **Decision-Making**: Prioritize quality of life, limited aggressive interventions
    
    **Very High Risk (Score ≥6)**:
    - **Survival**: <30% 10-year survival
    - **Clinical Approach**: Symptom management, comfort care focus
    - **Prognosis**: Poor, severe comorbidity impact
    - **Decision-Making**: Palliative approach, quality over quantity of life
    
    **Clinical Applications**:
    
    **Treatment Planning**:
    - Guide intensity of medical interventions
    - Balance potential benefits against remaining life expectancy
    - Inform discussions about goals of care
    - Support shared decision-making processes
    
    **Screening Decisions**:
    - Cancer screening appropriateness based on life expectancy
    - Cardiovascular prevention strategies in context
    - Osteoporosis screening and intervention decisions
    - Preventive care prioritization
    
    **Resource Allocation**:
    - ICU triage and resource prioritization
    - Rehabilitation potential assessment
    - Long-term care planning
    - Palliative care referral timing
    
    **Research Applications**:
    - Patient stratification in clinical trials
    - Outcome research risk adjustment
    - Population health management
    - Healthcare quality measurement
    
    **Implementation Considerations**:
    
    **Data Collection**:
    - Use current and historical diagnoses
    - Administrative coding adaptations available
    - Chart review or patient interview methods
    - Electronic health record integration possible
    
    **Clinical Context**:
    - Consider functional status alongside numerical score
    - Account for patient values and preferences
    - Integrate with other prognostic indicators
    - Regular reassessment as conditions change
    
    **Limitations and Cautions**:
    - Originally validated in hospitalized medical patients
    - May not capture frailty or functional decline
    - Some modern conditions may be under-weighted
    - Cultural and social determinants not included
    - Individual variation around population predictions
    
    **Quality Improvement Applications**:
    - Risk-adjusted outcome comparisons
    - Population health stratification
    - Care pathway optimization
    - Provider performance assessment with case-mix adjustment
    
    This calculator provides evidence-based prognostic assessment to support clinical 
    decision-making, treatment planning, and shared decision-making conversations with 
    patients and families about goals of care and life expectancy.
    
    Args:
        request: CCI parameters including age and 19 comorbidity categories
        
    Returns:
        CharlsonComorbidityIndexResponse: Score with survival probability and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("charlson_comorbidity_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Charlson Comorbidity Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return CharlsonComorbidityIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Charlson Comorbidity Index",
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