"""
Gillmore Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM) Router

Endpoint for calculating Gillmore staging for ATTR-CM prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.gillmore_staging_attr_cm import (
    GillmoreStagingAttrCmRequest,
    GillmoreStagingAttrCmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gillmore_staging_attr_cm",
    response_model=GillmoreStagingAttrCmResponse,
    summary="Calculate Gillmore Staging System for Transthyr...",
    description="Staging system for transthyretin amyloid cardiomyopathy using NT-proBNP and estimated glomerular filtration rate (eGFR) to stratify patients into prognostic categories for both wild-type and variant ATTR-CM",
    response_description="The calculated gillmore staging attr cm with interpretation",
    operation_id="gillmore_staging_attr_cm"
)
async def calculate_gillmore_staging_attr_cm(request: GillmoreStagingAttrCmRequest):
    """
    Calculates Gillmore Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM)
    
    The Gillmore staging system is a prognostic classification system for patients with 
    transthyretin amyloid cardiomyopathy (ATTR-CM) that uses two readily available biomarkers 
    to stratify patients into three distinct prognostic categories. This system provides 
    clinicians with valuable prognostic information to guide treatment decisions, monitoring 
    frequency, and care coordination for both wild-type and variant forms of ATTR-CM.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    Prognostic stratification for patients with confirmed ATTR-CM to facilitate risk-based 
    treatment planning, monitoring strategies, and clinical trial eligibility assessment 
    across diverse healthcare settings and patient populations.
    
    **Key Clinical Advantages**:
    
    **Universal Applicability**:
    - Effective for both wild-type (ATTRwt) and variant (ATTRv) forms of cardiac amyloidosis
    - Uses readily available biomarkers that are standard in most healthcare settings
    - Validated across different patient populations and healthcare systems internationally
    - Simple calculation enabling widespread clinical implementation and adoption
    
    **Prognostic Accuracy**:
    - Developed from 869 patients with comprehensive survival follow-up data
    - Externally validated in independent cohort of 318 patients with consistent performance
    - Strong statistical discrimination between stages with significant survival differences (p < 0.0001)
    - Hazard ratios demonstrate clinically meaningful risk gradation across stages
    
    **Clinical Decision Support Framework**:
    - Treatment intensity guidance based on prognostic risk stratification
    - Monitoring frequency recommendations tailored to disease stage and survival expectations
    - Clinical trial eligibility assessment and patient stratification for research participation
    - Multidisciplinary care coordination planning based on expected disease trajectory
    
    **Evidence-Based Risk Stratification**:
    
    **Stage I (Best Prognosis)**:
    - Median survival of 69.2 months with favorable biomarker profile
    - Both NT-proBNP ≤3000 ng/L and eGFR ≥45 ml/min indicating preserved organ function
    - Standard ATTR-CM management with regular monitoring and optimization of heart failure therapy
    - Excellent candidates for clinical trials and disease-specific therapies
    
    **Stage II (Intermediate Prognosis)**:
    - Median survival of 46.7 months with mixed biomarker profile
    - Hazard ratio 2.05 compared to Stage I, indicating moderate increase in mortality risk
    - Enhanced monitoring with consideration for disease-specific therapies and treatment intensification
    - Appropriate for most clinical trials with intermediate risk stratification
    
    **Stage III (Worst Prognosis)**:
    - Median survival of 24.1 months with both biomarkers indicating advanced disease
    - Hazard ratio 3.80 compared to Stage I, representing highest mortality risk category
    - Urgent consideration for intensive therapies and multidisciplinary care coordination
    - May require specialized clinical trials for advanced disease populations
    
    **Clinical Implementation Applications**:
    
    **Treatment Planning**:
    - Disease-specific therapy selection based on prognosis and expected survival benefit
    - Heart failure management intensity calibrated to disease stage and functional status
    - Advanced therapy consideration (transplantation, mechanical support) for appropriate candidates
    - Palliative care integration timing based on prognostic trajectory and patient preferences
    
    **Monitoring Strategy**:
    - Visit frequency and biomarker monitoring intervals tailored to disease stage
    - Serial staging assessment to monitor disease progression and treatment response
    - Functional capacity and quality of life evaluation schedule based on prognotic category
    - Imaging surveillance frequency recommendations aligned with expected disease progression
    
    **Research Applications**:
    - Clinical trial eligibility screening and patient stratification for balanced enrollment
    - Subgroup analysis framework for treatment effect assessment across prognostic categories
    - Natural history studies and disease progression modeling based on staging outcomes
    - Comparative effectiveness research using staging as prognostic adjustment variable
    
    **Quality Improvement Integration**:
    - Population health surveillance for ATTR-CM patient outcomes and care quality metrics
    - Resource allocation planning based on staging distribution and care intensity requirements
    - Provider education and competency assessment using staging accuracy as quality indicator
    - Healthcare system planning for specialized services and multidisciplinary care capacity
    
    Args:
        request: Biomarker parameters including NT-proBNP (cardiac dysfunction marker) 
                and eGFR (renal function marker) for comprehensive prognostic assessment
        
    Returns:
        GillmoreStagingAttrCmResponse: Staging result with detailed prognostic interpretation, 
                                     evidence-based management recommendations, and comprehensive 
                                     clinical guidance based on validated survival outcomes 
                                     from extensive clinical validation studies
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gillmore_staging_attr_cm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Gillmore Staging for ATTR-CM",
                    "details": {"parameters": parameters}
                }
            )
        
        return GillmoreStagingAttrCmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Gillmore staging calculation",
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
                "message": "Internal error in Gillmore staging calculation",
                "details": {"error": str(e)}
            }
        )