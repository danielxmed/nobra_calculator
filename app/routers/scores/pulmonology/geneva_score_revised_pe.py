"""
Geneva Score (Revised) for Pulmonary Embolism Router

Endpoint for calculating Geneva Score (Revised) for PE risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.geneva_score_revised_pe import (
    GenevaScoreRevisedPeRequest,
    GenevaScoreRevisedPeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/geneva_score_revised_pe",
    response_model=GenevaScoreRevisedPeResponse,
    summary="Calculate Geneva Score (Revised) for Pulmonary Embolism",
    description="Objectifies risk of pulmonary embolism, similar to Wells' score, but without requiring clinical gestalt. Helps determine clinical probability of PE to guide diagnostic workup including D-dimer testing and imaging decisions",
    response_description="The calculated geneva score revised pe with interpretation",
    operation_id="geneva_score_revised_pe"
)
async def calculate_geneva_score_revised_pe(request: GenevaScoreRevisedPeRequest):
    """
    Calculates Geneva Score (Revised) for Pulmonary Embolism
    
    The Geneva Score (Revised) for Pulmonary Embolism is a validated clinical decision rule 
    that provides objective assessment of pulmonary embolism probability without requiring 
    subjective clinical gestalt. This evidence-based tool helps clinicians determine 
    appropriate diagnostic pathways and resource utilization in patients with suspected 
    pulmonary embolism, offering a standardized approach to PE risk stratification.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    Objective risk stratification for pulmonary embolism in patients presenting with 
    suspected PE to guide evidence-based diagnostic workup and optimize healthcare 
    resource utilization while maintaining diagnostic accuracy and patient safety.
    
    **Key Clinical Advantages**:
    
    **Objective Assessment Framework**:
    - Eliminates subjective clinical gestalt requirement present in Wells' criteria
    - Provides reproducible results across different clinicians and healthcare settings
    - Standardized approach reduces inter-observer variability in PE assessment
    - Evidence-based parameters derived from large-scale prospective studies
    
    **Clinical Validation and Performance**:
    - Extensively validated in multicenter prospective studies with thousands of patients
    - Comparable diagnostic performance to Wells' criteria for PE probability assessment
    - Superior reproducibility due to objective clinical parameters
    - Validated specifically in emergency department and outpatient clinical settings
    
    **Risk Stratification Framework**:
    - Low risk (0-3 points): <10% PE incidence, D-dimer testing recommended
    - Intermediate risk (4-10 points): 20-30% PE incidence, D-dimer followed by imaging if positive
    - High risk (≥11 points): >60% PE incidence, direct urgent CT pulmonary angiography
    - Clear decision thresholds optimize diagnostic efficiency and patient safety
    
    **Clinical Decision Support**:
    
    **Low Risk Management (0-3 points)**:
    - **Diagnostic Strategy**: D-dimer testing as first-line assessment
    - **Negative D-dimer**: PE effectively ruled out, no further testing required
    - **Positive D-dimer**: Proceed to CT pulmonary angiography for definitive diagnosis
    - **Clinical Impact**: Safely avoids unnecessary imaging in low-probability patients
    - **Cost-Effectiveness**: Significant reduction in healthcare costs and radiation exposure
    
    **Intermediate Risk Management (4-10 points)**:
    - **Diagnostic Strategy**: D-dimer testing followed by risk-benefit assessment
    - **Negative D-dimer**: PE unlikely, consider alternative diagnoses
    - **Positive D-dimer**: CT pulmonary angiography recommended
    - **Clinical Considerations**: Patient factors, symptom severity, and clinical context
    - **Resource Optimization**: Balanced approach to diagnostic accuracy and efficiency
    
    **High Risk Management (≥11 points)**:
    - **Diagnostic Strategy**: Urgent CT pulmonary angiography without D-dimer testing
    - **Clinical Rationale**: High pretest probability (>60%) justifies direct imaging
    - **Timing**: Expedited imaging within hours of presentation
    - **Management Considerations**: May warrant empirical anticoagulation pending results
    - **Alternative Imaging**: Ventilation-perfusion scan if CT contraindicated
    
    **Special Clinical Considerations**:
    
    **D-dimer Optimization**:
    - Standard cutoff: 500 ng/mL for most patients
    - Age-adjusted cutoff: Age × 10 ng/mL for patients >50 years
    - Improved specificity in elderly patients without compromising sensitivity
    - Particularly valuable in reducing false positives in older adults
    
    **Clinical Limitations and Considerations**:
    - Validated primarily in outpatient and emergency department settings
    - Not validated for use in hospitalized patients (consider Wells' criteria)
    - Should complement rather than replace clinical judgment
    - High clinical suspicion may warrant imaging regardless of score
    
    **Quality Improvement Applications**:
    - Standardization of PE assessment protocols across healthcare institutions
    - Reduction in unnecessary imaging and associated healthcare expenditures
    - Educational tool for training healthcare providers in evidence-based PE assessment
    - Integration into clinical decision support systems and electronic health records
    
    **Research and Validation Context**:
    
    **Original Development Study**:
    - Derived from analysis of 965 patients with suspected PE
    - Prospective multicenter validation in emergency departments
    - Objective parameters selected through systematic clinical evaluation
    - Validated threshold values optimized for clinical decision-making
    
    **Subsequent Validation Studies**:
    - Multiple independent validation studies confirming diagnostic performance
    - Meta-analyses demonstrating comparable performance to Wells' criteria
    - Real-world implementation studies showing practical clinical utility
    - International adoption across diverse healthcare systems
    
    **Clinical Implementation Evidence**:
    - Successful integration into emergency department protocols
    - Demonstrated reduction in unnecessary CT scans without missing PE cases
    - Improved standardization of PE assessment across different providers
    - Enhanced medical education and training in evidence-based PE diagnosis
    
    **Comparative Analysis with Other Scoring Systems**:
    - Wells' criteria: Comparable accuracy but requires subjective clinical gestalt
    - PERC rule: Useful for very low-risk patients but less discriminatory
    - Years criteria: Less extensively validated and more complex to calculate
    - Geneva score provides optimal balance of objectivity and diagnostic performance
    
    Args:
        request: Patient clinical parameters including demographics (age), medical history 
                (previous VTE, surgery, malignancy), symptoms (limb pain, hemoptysis), 
                physical findings (heart rate, limb examination) required for Geneva PE 
                score calculation
        
    Returns:
        GenevaScoreRevisedPeResponse: Geneva PE score with detailed risk stratification, 
                                     evidence-based diagnostic recommendations, and 
                                     comprehensive clinical management guidance based 
                                     on validated probability thresholds
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("geneva_score_revised_pe", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Geneva Score (Revised) for PE",
                    "details": {"parameters": parameters}
                }
            )
        
        return GenevaScoreRevisedPeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Geneva PE Score calculation",
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
                "message": "Internal error in Geneva PE Score calculation",
                "details": {"error": str(e)}
            }
        )