"""
Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid Router

Endpoint for calculating T-MACS probability of acute coronary syndrome.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.troponin_only_macs import (
    TroponinOnlyMacsRequest,
    TroponinOnlyMacsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/troponin_only_macs",
    response_model=TroponinOnlyMacsResponse,
    summary="Calculate T-MACS Probability for Acute Coronary Syndrome",
    description="Calculates the Troponin-only Manchester Acute Coronary Syndromes (T-MACS) decision aid "
                "for emergency department patients presenting with chest pain. This validated clinical "
                "prediction tool uses a single high-sensitivity cardiac troponin T measurement and "
                "clinical factors to calculate the probability of acute coronary syndrome (ACS). "
                "T-MACS can safely rule out ACS in approximately 40% of patients with <1% probability "
                "of missed diagnosis, while identifying high-risk patients requiring immediate intervention. "
                "The tool significantly reduces unnecessary hospital admissions and healthcare costs while "
                "maintaining excellent safety profile with 99.3% negative predictive value and 98.7% "
                "sensitivity for ACS detection.",
    response_description="The calculated ACS probability with risk stratification and evidence-based management recommendations",
    operation_id="troponin_only_macs"
)
async def calculate_troponin_only_macs(request: TroponinOnlyMacsRequest):
    """
    Calculates Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid
    
    The T-MACS decision aid is a revolutionary clinical prediction tool that transforms 
    emergency department chest pain evaluation by providing rapid, accurate risk 
    stratification using readily available clinical data and a single troponin measurement.
    
    ## Clinical Background and Development
    
    T-MACS was developed at Manchester Royal Infirmary as a refinement of the original 
    Manchester Acute Coronary Syndromes (MACS) tool. The original MACS required two 
    biomarkers (troponin and H-FABP), but T-MACS simplified this to use only 
    high-sensitivity cardiac troponin T (hs-cTnT), making it more practical for 
    widespread clinical implementation.
    
    ## How T-MACS Works
    
    **Single Biomarker Approach:**
    T-MACS requires only one blood test on arrival - high-sensitivity cardiac troponin T. 
    This eliminates the need for:
    - Serial troponin measurements over 6-12 hours
    - Multiple biomarker panels
    - Extended observation periods for many patients
    
    **Clinical Factor Integration:**
    The algorithm incorporates six key clinical factors that are readily available 
    during initial assessment:
    
    1. **ECG Ischemia:** New ischemic changes including ST depression ≥0.5mm, 
       ST elevation, T-wave inversion, or new LBBB
    2. **Crescendo Angina:** Worsening pattern of chest pain with increasing 
       frequency, severity, or duration
    3. **Right Arm/Shoulder Radiation:** Classic anginal symptom pattern
    4. **Associated Vomiting:** May indicate vagal response to cardiac ischemia
    5. **Diaphoresis:** Sweating associated with chest pain episode
    6. **Hypotension:** Systolic BP <100 mmHg suggesting hemodynamic compromise
    
    ## Risk Stratification and Clinical Decision-Making
    
    **Very Low Risk (<2% ACS probability):**
    - **Clinical Action:** Safe for immediate discharge
    - **Evidence Base:** 99.3% negative predictive value
    - **Patient Benefit:** Avoids unnecessary hospital admission
    - **Healthcare Impact:** Reduces costs and ED overcrowding
    - **Safety Net:** Clear return precautions and follow-up instructions
    
    **Low Risk (2-5% ACS probability):**
    - **Clinical Action:** Short-term observation with serial troponin
    - **Duration:** 3-6 hours in ED or observation unit
    - **Discharge Criteria:** Negative serial troponin and clinical stability
    - **Follow-up:** Outpatient stress testing within 72 hours
    
    **Moderate Risk (5-95% ACS probability):**
    - **Clinical Action:** Extended evaluation and risk stratification
    - **Testing Strategy:** Serial troponin over 6-12 hours
    - **Advanced Testing:** Stress testing or CT coronary angiography
    - **Treatment:** Consider antiplatelet therapy if high suspicion
    - **Admission:** May require overnight observation
    
    **High Risk (≥95% ACS probability):**
    - **Clinical Action:** Immediate ACS protocol activation
    - **Cardiology:** Urgent consultation within 30 minutes
    - **Treatment:** Dual antiplatelet therapy and anticoagulation
    - **Intervention:** Expedite cardiac catheterization
    - **Monitoring:** Continuous cardiac monitoring and frequent assessments
    
    ## Clinical Implementation and Real-World Impact
    
    **Manchester Royal Infirmary Experience:**
    Since implementation, over 3,500 patients have been managed using T-MACS with:
    - Superior performance compared to NICE guidelines
    - Reduction in average length of stay from 2 days to same-day discharge
    - Significant decrease in unnecessary hospital admissions
    - Maintained excellent safety profile with no increase in missed diagnoses
    
    **Quality Metrics and Performance:**
    - **Sensitivity:** 98.7% for detecting ACS
    - **Negative Predictive Value:** 99.3% for ruling out ACS
    - **Rule-Out Rate:** 40% of patients classified as very low risk
    - **Rule-In Rate:** 5% of patients classified as high risk
    - **Cost Effectiveness:** Substantial reduction in healthcare costs
    
    ## Validation and Evidence Base
    
    T-MACS has been extensively validated in multiple cohorts:
    - **Derivation Study:** 703 patients at Manchester Royal Infirmary
    - **External Validation:** 1,459 patients across three independent cohorts
    - **Point-of-Care Validation:** Demonstrated accuracy with bedside troponin assays
    - **International Validation:** Studies in Australia and other healthcare systems
    
    ## Clinical Advantages Over Traditional Approaches
    
    **Compared to Serial Troponin Strategy:**
    - Faster decision-making (single measurement vs. 6-12 hours)
    - Reduced resource utilization
    - Earlier discharge for low-risk patients
    - Fewer repeat blood draws and patient discomfort
    
    **Compared to Clinical Judgment Alone:**
    - Objective, standardized risk assessment
    - Reduced inter-physician variability
    - Evidence-based thresholds for decision-making
    - Improved documentation and quality metrics
    
    ## Safety Considerations and Limitations
    
    **Appropriate Use:**
    - Emergency department patients with chest pain suspicious for ACS
    - Patients without obvious STEMI on presentation
    - High-sensitivity cardiac troponin T assay availability
    - Trained clinical staff familiar with the tool
    
    **Limitations:**
    - Not validated in patients <25 years old
    - Requires accurate troponin measurement
    - Should complement, not replace, clinical judgment
    - May need local validation for different populations
    
    **Contraindications:**
    - Obvious STEMI or ACS on presentation
    - Hemodynamically unstable patients
    - Patients requiring immediate intervention
    
    ## Integration with Clinical Pathways
    
    T-MACS seamlessly integrates with existing chest pain pathways and can be:
    - Embedded in electronic health records
    - Implemented as decision support tools
    - Used for quality improvement initiatives
    - Applied in clinical audit and research
    
    ## Future Directions and Research
    
    Ongoing research includes:
    - Validation with different troponin assays
    - Implementation in different healthcare systems
    - Cost-effectiveness analyses
    - Integration with artificial intelligence platforms
    - Extension to other acute cardiac conditions
    
    Args:
        request: Clinical parameters including hs-cTnT and clinical factors
        
    Returns:
        TroponinOnlyMacsResponse: ACS probability with risk stratification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("troponin_only_macs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating T-MACS probability",
                    "details": {"parameters": parameters}
                }
            )
        
        return TroponinOnlyMacsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for T-MACS calculation",
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
                "message": "Internal error in T-MACS calculation",
                "details": {"error": str(e)}
            }
        )