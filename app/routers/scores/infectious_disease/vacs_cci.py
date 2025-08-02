"""
Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) Router

Endpoint for calculating VACS-CCI to provide enhanced mortality risk prediction 
for patients with HIV by combining VACS Index with Charlson Comorbidity Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.vacs_cci import (
    VacsCciRequest,
    VacsCciResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/vacs_cci",
    response_model=VacsCciResponse,
    summary="Calculate Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI)",
    description="Calculates the Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) to provide enhanced 5-year all-cause mortality risk prediction for patients with HIV. This integrated prognostic tool combines the VACS Index (which incorporates HIV-specific biomarkers like CD4 count and viral load with general health indicators and composite measures of organ system injury) with the Charlson Comorbidity Index (which provides comprehensive assessment of non-HIV comorbidities). The VACS-CCI addresses limitations of using either HIV-specific or general health markers alone by providing a more comprehensive risk assessment that incorporates both HIV disease severity and burden of comorbid conditions. The score is expressed as a percentage from 0-100% representing 5-year mortality risk, with clinical interpretation ranging from low risk (routine care) to very high risk (maximum interventions and palliative care consideration). This tool is particularly valuable for risk stratification, treatment planning, prognosis communication, and quality improvement in HIV care programs.",
    response_description="The calculated VACS-CCI mortality risk percentage with detailed component breakdown (VACS and Charlson scores), composite biomarkers (FIB-4 and eGFR), risk stratification, and comprehensive clinical management recommendations",
    operation_id="vacs_cci"
)
async def calculate_vacs_cci(request: VacsCciRequest):
    """
    Calculates Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) for enhanced HIV mortality prediction
    
    The Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) is an 
    integrated prognostic tool that combines the strengths of HIV-specific risk 
    assessment (VACS Index) with comprehensive comorbidity evaluation (Charlson 
    Comorbidity Index) to provide enhanced mortality risk prediction for patients 
    with HIV infection.
    
    **CLINICAL SIGNIFICANCE:**
    
    **Background and Rationale:**
    The VACS-CCI was developed to address the limitation that HIV-specific markers 
    alone (such as CD4 count and viral load) do not fully capture mortality risk 
    in the modern era of effective antiretroviral therapy. Similarly, general 
    comorbidity indices may not adequately account for HIV-specific disease burden. 
    By combining both approaches, the VACS-CCI provides more accurate and 
    comprehensive risk stratification.
    
    **Component Integration:**
    
    **VACS Index Components:**
    - **Age**: Most influential demographic factor
    - **HIV Disease Markers**: CD4 count (immunodeficiency), HIV viral load (treatment effectiveness)
    - **Organ System Injury**: Hemoglobin (anemia), FIB-4 (liver fibrosis), eGFR (kidney function)
    - **Co-infections**: Hepatitis C status (accelerates liver disease)
    
    **Charlson Comorbidity Index Components:**
    - **Cardiovascular**: MI, CHF, PVD, stroke (1 point each)
    - **Neurological**: Dementia, hemiplegia (1-2 points)
    - **Pulmonary**: Chronic lung disease (1 point)
    - **Rheumatologic**: Connective tissue disease (1 point)
    - **Gastrointestinal**: PUD, liver disease (1-3 points based on severity)
    - **Endocrine**: Diabetes with/without complications (1-2 points)
    - **Renal**: Moderate to severe kidney disease (2 points)
    - **Oncologic**: Malignancy (2 points), metastatic disease (6 points)
    - **Immunologic**: AIDS diagnosis (6 points)
    
    **Composite Biomarkers:**
    
    **FIB-4 Score (Liver Assessment):**
    - Formula: (Age × AST) / (Platelets × √ALT)
    - Interpretation: <1.45 low risk, 1.45-3.25 intermediate, >3.25 high risk for significant fibrosis
    - Clinical significance: Validated non-invasive marker of liver fibrosis in HIV/HCV co-infected patients
    
    **eGFR (Kidney Assessment):**
    - Formula: CKD-EPI equation incorporating creatinine, age, sex, race
    - Interpretation: ≥90 normal, 60-89 mild decrease, 30-59 moderate decrease, <30 severe decrease
    - Clinical significance: Primary measure of kidney function and cardiovascular risk
    
    **Score Interpretation and Risk Stratification:**
    
    **Risk Categories:**
    - **Low Risk (0-25%)**: Excellent prognosis, routine HIV care appropriate
    - **Moderate Risk (26-50%)**: Enhanced monitoring and preventive care recommended
    - **High Risk (51-75%)**: Intensive management and multidisciplinary care needed
    - **Very High Risk (76-100%)**: Maximum interventions and palliative care consideration
    
    **Clinical Applications:**
    
    **Risk Stratification:**
    - Identify patients at highest mortality risk for intensive interventions
    - Guide frequency and intensity of clinical monitoring
    - Prioritize resource allocation and specialist referrals
    - Support population health management initiatives
    
    **Treatment Planning:**
    - Inform discussions about treatment intensity and therapeutic goals
    - Guide timing of interventions for comorbid conditions
    - Support shared decision-making between patients and providers
    - Facilitate coordination between HIV specialists and other providers
    
    **Prognosis Communication:**
    - Provide evidence-based framework for life expectancy discussions
    - Support advance care planning conversations
    - Guide end-of-life care discussions when appropriate
    - Help patients and families understand disease trajectory
    
    **Quality Improvement:**
    - Standardized mortality risk assessment across providers and settings
    - Quality metrics and outcome measures for HIV care programs
    - Research tool for clinical trials and epidemiological studies
    - Population health surveillance and care optimization
    
    **Important Clinical Considerations:**
    
    **Dynamic Assessment:**
    - Score should be recalculated regularly with updated clinical data
    - Treatment responses can significantly improve risk profiles over time
    - Monitor for changes in HIV status, comorbidities, and laboratory values
    - Consider reassessment every 6-12 months or with significant clinical changes
    
    **Modifiable Risk Factors:**
    - **HIV Management**: Optimize antiretroviral therapy for viral suppression
    - **Co-infection Treatment**: Treat hepatitis C if present
    - **Comorbidity Management**: Address individual Charlson conditions aggressively
    - **Preventive Care**: Implement age-appropriate screening and interventions
    - **Lifestyle Interventions**: Address smoking, substance use, nutrition, exercise
    - **Medication Optimization**: Review and optimize management of chronic conditions
    
    **Clinical Interpretation Guidelines:**
    - Use in conjunction with comprehensive clinical assessment and judgment
    - Consider individual patient goals, preferences, and values
    - Account for social determinants of health and patient context
    - Recognize that the tool provides risk estimates, not definitive prognoses
    - Update assessments as clinical status and treatment responses evolve
    
    **Validation and Performance:**
    - Developed and validated in large HIV cohorts including veteran populations
    - Demonstrates superior discrimination compared to individual indices alone
    - Consistent performance across diverse demographic and clinical subgroups
    - Established utility in clinical practice and research settings
    
    **Limitations:**
    - Developed primarily in male veteran populations (generalizability considerations)
    - Requires accurate clinical history and current laboratory values
    - May not fully capture all mortality determinants in diverse populations
    - Represents static assessment that may not reflect dynamic clinical changes
    - Should not replace comprehensive clinical evaluation and judgment
    
    Args:
        request: VACS-CCI parameters including demographics, HIV markers, laboratory 
                values, and comprehensive Charlson comorbidity assessment
        
    Returns:
        VacsCciResponse: Mortality risk percentage with component breakdown, 
        composite biomarkers, risk stratification, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("vacs_cci", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating VACS-CCI",
                    "details": {"parameters": parameters}
                }
            )
        
        return VacsCciResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for VACS-CCI",
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
                "message": "Internal error in VACS-CCI calculation",
                "details": {"error": str(e)}
            }
        )