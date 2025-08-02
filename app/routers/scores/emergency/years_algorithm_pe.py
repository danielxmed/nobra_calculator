"""
YEARS Algorithm for Pulmonary Embolism (PE) Router

Endpoint for YEARS Algorithm calculation for PE diagnosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.years_algorithm_pe import (
    YearsAlgorithmPeRequest,
    YearsAlgorithmPeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/years_algorithm_pe",
    response_model=YearsAlgorithmPeResponse,
    summary="Calculate YEARS Algorithm for Pulmonary Embolism",
    description="Calculates the YEARS Algorithm for ruling out pulmonary embolism in hemodynamically "
                "stable patients ≥18 years old using variable D-dimer thresholds based on clinical criteria. "
                "This simplified diagnostic tool uses three clinical criteria (DVT signs, hemoptysis, "
                "PE most likely diagnosis) to determine appropriate D-dimer cutoff values. The algorithm "
                "reduces unnecessary CT pulmonary angiography by 14% compared to standard algorithms "
                "while maintaining safety with a 3-month VTE incidence of 0.43% for patients not "
                "undergoing CTPA. Validated in prospective multicenter studies with excellent safety "
                "profile and clinical utility in emergency department settings.",
    response_description="The YEARS Algorithm diagnostic recommendation with D-dimer threshold analysis, clinical decision support, and comprehensive safety information",
    operation_id="years_algorithm_pe"
)
async def calculate_years_algorithm_pe(request: YearsAlgorithmPeRequest):
    """
    Calculates YEARS Algorithm for Pulmonary Embolism (PE)
    
    The YEARS Algorithm is a simplified diagnostic tool developed by van der Hulle et al. 
    that revolutionizes pulmonary embolism diagnosis by using variable D-dimer thresholds 
    based on clinical probability assessment. This evidence-based approach significantly 
    reduces unnecessary imaging while maintaining excellent safety standards.
    
    **CLINICAL BACKGROUND:**
    
    Pulmonary embolism (PE) is a life-threatening condition with an annual incidence of 
    1-2 per 1000 in the general population. Traditional diagnostic approaches often 
    result in overuse of CT pulmonary angiography (CTPA), leading to:
    
    - Unnecessary radiation exposure
    - Increased healthcare costs
    - False positive findings
    - Incidental findings requiring follow-up
    - Resource utilization strain
    
    **YEARS ALGORITHM DEVELOPMENT:**
    
    The YEARS study was a prospective, multicenter cohort study conducted in 12 Dutch 
    hospitals that enrolled 3,465 consecutive patients with suspected PE. The algorithm 
    was derived from the three most predictive items from the Wells score:
    
    1. Clinical signs of deep vein thrombosis
    2. Hemoptysis  
    3. PE as the most likely diagnosis
    
    **ALGORITHM LOGIC:**
    
    **Variable D-dimer Thresholds:**
    
    The key innovation is using different D-dimer cutoff values based on clinical 
    probability:
    
    **0 YEARS Items Present (Lower Clinical Probability):**
    - D-dimer threshold: 1000 ng/mL FEU
    - Rationale: Higher threshold appropriate for lower pre-test probability
    - If D-dimer <1000 ng/mL → PE excluded safely
    
    **≥1 YEARS Items Present (Higher Clinical Probability):**
    - D-dimer threshold: 500 ng/mL FEU
    - Rationale: Standard threshold for higher pre-test probability
    - If D-dimer <500 ng/mL → PE excluded with standard sensitivity
    
    **D-dimer Above Threshold:**
    - CTPA required to exclude PE
    - Standard diagnostic imaging pathway
    
    **CLINICAL VALIDATION:**
    
    **Performance Metrics:**
    - 3-month VTE incidence: 0.43% (95% CI 0.20-0.91%) for patients not undergoing CTPA
    - Sensitivity: 90% for clinically significant PE
    - Specificity: 65% reducing false positives
    - Miss rate: 0.5% (95% CI 0.2-1.1%) in external validation
    
    **Efficiency Gains:**
    - 14% reduction in CTPA utilization compared to standard algorithms
    - 42.9% of patients can have PE ruled out without imaging
    - Significant cost savings and resource optimization
    - Reduced radiation exposure and contrast agent use
    
    **Safety Profile:**
    - Non-inferior to standard diagnostic pathways
    - No increase in missed clinically significant PEs
    - Appropriate negative predictive value for clinical decision-making
    - Extensive external validation in multiple populations
    
    **CLINICAL IMPLEMENTATION:**
    
    **Patient Selection Criteria:**
    
    **Appropriate Candidates:**
    - Hemodynamically stable patients ≥18 years old
    - Suspected pulmonary embolism based on clinical presentation
    - Able to undergo CTPA if indicated
    - Reliable follow-up available
    
    **Exclusion Criteria:**
    - Patients currently on therapeutic anticoagulation
    - Life expectancy <3 months
    - Geographic limitations preventing adequate follow-up
    - Contrast agent allergies or contraindications to CTPA
    - Hemodynamic instability requiring immediate intervention
    
    **Special Populations:**
    
    **Pregnancy:**
    - Standard YEARS algorithm not validated in pregnancy
    - Use Pregnancy-Adapted YEARS Algorithm (van der Pol et al., NEJM 2019)
    - Includes compression ultrasonography for patients with DVT signs
    - Maintains safety while reducing imaging in pregnant patients
    
    **Elderly Patients:**
    - Algorithm performance maintained in older adults
    - Consider age-adjusted D-dimer interpretations with caution
    - Clinical judgment important for frail elderly patients
    
    **Cancer Patients:**
    - Algorithm not specifically validated in active cancer patients
    - Higher baseline D-dimer levels may affect performance
    - Consider alternative diagnostic approaches in high-risk cancer patients
    
    **CLINICAL DECISION SUPPORT:**
    
    **PE Excluded (D-dimer Below Threshold):**
    
    **Immediate Actions:**
    - No further imaging for PE workup required
    - Document YEARS assessment and D-dimer result
    - Pursue alternative diagnostic considerations
    
    **Alternative Diagnoses to Consider:**
    - Pneumonia or lower respiratory tract infection
    - Pleuritis or pleural effusion
    - Musculoskeletal chest pain
    - Cardiac causes (MI, pericarditis)
    - Anxiety or panic disorder
    
    **Follow-up Recommendations:**
    - Patient education about symptoms warranting re-evaluation
    - Return precautions for worsening dyspnea or chest pain
    - Primary care follow-up for ongoing symptom management
    
    **CTPA Required (D-dimer Above Threshold):**
    
    **Immediate Actions:**
    - Proceed with CT pulmonary angiography
    - Assess clinical urgency and hemodynamic stability
    - Consider interim anticoagulation if high clinical suspicion
    
    **Imaging Considerations:**
    - CTPA preferred first-line imaging modality
    - V/Q scan alternative if CTPA contraindicated
    - Timing based on clinical urgency and resource availability
    
    **Interim Management:**
    - Consider therapeutic anticoagulation pending imaging if:
      - High clinical suspicion for PE
      - Significant delay expected for imaging
      - No contraindications to anticoagulation
    
    **QUALITY ASSURANCE:**
    
    **Documentation Requirements:**
    - Document all three YEARS criteria assessments
    - Record D-dimer value and threshold used
    - Note clinical decision-making rationale
    - Document patient counseling and follow-up plans
    
    **Audit Considerations:**
    - Monitor adherence to algorithm recommendations
    - Track imaging utilization rates
    - Assess patient outcomes and safety metrics
    - Review cases with unexpected outcomes
    
    **LIMITATIONS AND CONSIDERATIONS:**
    
    **Algorithm Limitations:**
    - Not validated in patients on therapeutic anticoagulation
    - Limited data in certain populations (cancer, pregnancy, elderly frail)
    - Requires reliable D-dimer assay with FEU reporting
    - Clinical judgment remains essential for implementation
    
    **D-dimer Considerations:**
    - Must be reported in ng/mL FEU (fibrinogen equivalent units)
    - Different assays may have varying performance characteristics
    - False positives common with inflammatory conditions, surgery, trauma
    - Age, pregnancy, and cancer can elevate baseline levels
    
    **Clinical Judgment:**
    - Algorithm provides guidance but doesn't replace clinical reasoning
    - Consider patient-specific factors affecting risk assessment
    - Shared decision-making appropriate for borderline cases
    - Alternative approaches may be needed for complex patients
    
    Args:
        request: YEARS criteria assessment and D-dimer level for algorithm calculation
        
    Returns:
        YearsAlgorithmPeResponse: Diagnostic recommendation with comprehensive clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("years_algorithm_pe", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating YEARS Algorithm for PE",
                    "details": {"parameters": parameters}
                }
            )
        
        return YearsAlgorithmPeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for YEARS Algorithm calculation",
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
                "message": "Internal error in YEARS Algorithm calculation",
                "details": {"error": str(e)}
            }
        )