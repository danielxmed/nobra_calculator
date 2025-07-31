"""
Emergency Department Assessment of Chest Pain Score (EDACS) Router

Endpoint for calculating EDACS score for chest pain risk stratification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.emergency_department_assessment_chest_pain_edacs import (
    EmergencyDepartmentAssessmentChestPainEdacsRequest,
    EmergencyDepartmentAssessmentChestPainEdacsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/emergency_department_assessment_chest_pain_edacs", response_model=EmergencyDepartmentAssessmentChestPainEdacsResponse)
async def calculate_emergency_department_assessment_chest_pain_edacs(request: EmergencyDepartmentAssessmentChestPainEdacsRequest):
    """
    Calculates Emergency Department Assessment of Chest Pain Score (EDACS)
    
    The Emergency Department Assessment of Chest Pain Score (EDACS) is a clinical 
    decision tool developed for risk stratification of chest pain patients in the 
    emergency department. It identifies low-risk patients who can be safely discharged 
    when combined with no new ischemia on ECG and negative troponins at 0 and 2 hours.
    
    Historical Context and Development:
    
    EDACS was developed in 2014 by Than et al. in Australia and New Zealand as part 
    of the ADAPT-ADP (Accelerated Diagnostic Protocol) to improve emergency department 
    efficiency while maintaining safety in chest pain evaluation. The tool was created 
    to address the need for a reliable, validated approach to identify patients suitable 
    for early discharge, reducing healthcare costs and overcrowding while ensuring 
    patient safety.
    
    Clinical Applications and Validation:
    
    EDACS has been extensively validated in multiple populations and healthcare systems, 
    demonstrating consistent performance across different demographics and clinical 
    settings. The tool is particularly valuable in:
    
    - Emergency department triage and disposition decisions
    - Resource allocation and bed management
    - Quality improvement initiatives for chest pain care
    - Integration with electronic health record systems
    - Training and education for emergency medicine providers
    
    Scoring Methodology:
    
    The EDACS score incorporates seven clinical variables:
    
    1. Age (Primary Risk Factor):
       - Uses decade-based point assignment from 18-85+ years
       - Reflects increasing cardiovascular risk with advancing age
       - Accounts for the majority of score variance in most patients
    
    2. Gender:
       - Male patients receive additional points reflecting higher baseline CAD risk
       - Based on epidemiological data showing gender differences in CAD prevalence
    
    3. Risk Factors (Ages 18-50 Only):
       - Known coronary artery disease OR ≥3 traditional risk factors
       - Risk factors: hypertension, dyslipidemia, diabetes, smoking, family history
       - Age limitation recognizes that risk factors become less discriminatory in older patients
    
    4. Clinical Symptoms and Signs:
       - Diaphoresis: Associated with sympathetic activation in ACS
       - Pain radiation: Classic pattern suggesting cardiac ischemia
       - Pleuritic pain: Suggests non-cardiac etiology (negative points)
       - Chest wall tenderness: Suggests musculoskeletal cause (negative points)
    
    EDACS-Accelerated Diagnostic Protocol (EDACS-ADP):
    
    The complete EDACS-ADP combines the clinical score with objective testing:
    
    Low-Risk Criteria (All Must Be Present):
    1. EDACS score <16 points
    2. No new ischemic changes on electrocardiogram
    3. Troponin negative at presentation (0 hours)
    4. Troponin negative at 2 hours
    
    Performance Characteristics:
    - Sensitivity: >99% for 30-day major adverse cardiac events (MACE)
    - Negative predictive value: Approaches 100% when all criteria met
    - External validation across multiple studies confirms safety profile
    - Reduces length of stay by 12-24 hours in appropriate patients
    
    Clinical Implementation and Safety:
    
    Successful EDACS implementation requires:
    - Provider training on proper application and interpretation
    - Integration with institutional chest pain protocols
    - Quality assurance monitoring of outcomes
    - Patient education regarding return precautions
    - Appropriate follow-up arrangements for discharged patients
    
    Safety Considerations:
    - Most validated in patients presenting within 12 hours of symptom onset
    - Should not replace clinical judgment in complex cases
    - Requires completion of full ADP protocol for low-risk classification
    - Regular outcome monitoring essential for quality assurance
    - Clear documentation of decision-making rationale recommended
    
    Economic and Quality Benefits:
    - Reduces unnecessary admissions and prolonged observations
    - Decreases healthcare costs while maintaining quality of care
    - Improves emergency department throughput and capacity
    - Enhances patient satisfaction through reduced wait times
    - Supports value-based care initiatives and quality metrics
    
    Integration with Modern Emergency Medicine:
    
    EDACS represents a shift toward evidence-based, protocol-driven care in emergency 
    medicine. It exemplifies the use of validated clinical decision tools to optimize 
    resource utilization while maintaining the highest standards of patient safety. 
    The tool's success has influenced the development of similar risk stratification 
    instruments for other conditions in emergency medicine.
    
    Future Directions:
    - Integration with high-sensitivity troponin assays
    - Combination with other biomarkers and imaging modalities
    - Application in different healthcare systems and populations
    - Development of electronic decision support tools
    - Quality improvement and outcome monitoring systems
    
    The EDACS score and ADP protocol represent a paradigm shift in emergency chest 
    pain evaluation, providing a safe, efficient, and evidence-based approach to 
    patient care that benefits providers, patients, and healthcare systems alike.
    
    Args:
        request: EDACS calculation parameters including age, sex, risk factors, and clinical symptoms
        
    Returns:
        EmergencyDepartmentAssessmentChestPainEdacsResponse: Score with risk stratification and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("emergency_department_assessment_chest_pain_edacs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EDACS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return EmergencyDepartmentAssessmentChestPainEdacsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EDACS calculation",
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
                "message": "Internal error in EDACS calculation",
                "details": {"error": str(e)}
            }
        )