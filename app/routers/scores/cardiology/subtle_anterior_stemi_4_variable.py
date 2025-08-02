"""
Subtle Anterior STEMI Calculator (4-Variable) Router

Endpoint for calculating Subtle Anterior STEMI 4-Variable Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.subtle_anterior_stemi_4_variable import (
    SubtleAnteriorStemi4VariableRequest,
    SubtleAnteriorStemi4VariableResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/subtle_anterior_stemi_4_variable",
    response_model=SubtleAnteriorStemi4VariableResponse,
    summary="Calculate Subtle Anterior STEMI 4-Variable Score",
    description="Calculates the Subtle Anterior STEMI 4-Variable Score to differentiate normal variant ST elevation "
                "(benign early repolarization) from subtle anterior STEMI that may require urgent intervention. "
                "This evidence-based clinical decision tool was developed by Dr. Stephen Smith and colleagues to "
                "address the critical challenge of identifying patients with chest pain and non-diagnostic ECG "
                "changes who may have 100% coronary artery occlusion requiring immediate percutaneous coronary "
                "intervention. The 4-variable formula improves upon the original 3-variable version by adding "
                "QRS amplitude in lead V2, achieving 83.3% sensitivity and 87.7% specificity with 85.9% diagnostic "
                "accuracy. The calculator uses four ECG parameters: Bazett-corrected QT interval, QRS amplitude "
                "in V2, R wave amplitude in V4, and ST elevation 60ms after J point in V3. A score ≥18.2 indicates "
                "likely anterior STEMI requiring urgent cardiology consultation and consideration for cardiac "
                "catheterization, while scores <18.2 suggest benign early repolarization. Prerequisites include "
                "≥1mm ST elevation in V2-V4 without obvious STEMI features (non-concave STE, reciprocal changes, "
                "Q waves, or T wave inversions). This tool significantly improves clinical decision-making in "
                "emergency settings where distinguishing subtle STEMI from benign variants is crucial for optimal "
                "patient outcomes and appropriate resource utilization.",
    response_description="Calculated Subtle Anterior STEMI 4-Variable Score with diagnostic probability and comprehensive clinical management recommendations",
    operation_id="subtle_anterior_stemi_4_variable"
)
async def calculate_subtle_anterior_stemi_4_variable(request: SubtleAnteriorStemi4VariableRequest):
    """
    Subtle Anterior STEMI Calculator (4-Variable) - Advanced ECG Analysis Tool
    
    Calculates the Subtle Anterior STEMI 4-Variable Score, a sophisticated clinical 
    decision tool that differentiates normal variant ST elevation (benign early 
    repolarization) from subtle anterior ST-elevation myocardial infarction requiring 
    urgent intervention. This evidence-based calculator addresses one of the most 
    challenging diagnostic dilemmas in emergency cardiology.
    
    Clinical Context and Diagnostic Challenge:
    
    Emergency physicians and cardiologists frequently encounter patients presenting 
    with chest pain and ECG changes that are suspicious but non-diagnostic for STEMI. 
    These subtle presentations can represent either benign early repolarization (BER), 
    a common normal variant especially in young patients, or acute coronary occlusion 
    requiring immediate intervention. Missing a subtle STEMI can result in significant 
    morbidity and mortality, while false positives lead to unnecessary invasive 
    procedures and resource consumption.
    
    The Subtle Anterior STEMI Calculator (4-Variable) provides objective, quantitative 
    criteria to guide clinical decision-making in these challenging cases, enabling 
    healthcare providers to identify patients who would benefit from urgent 
    percutaneous coronary intervention while avoiding unnecessary procedures in 
    those with benign conditions.
    
    Development and Validation:
    
    Original Research Foundation:
    The calculator is based on landmark research by Dr. Stephen Smith and colleagues, 
    beginning with Smith et al. (2012) who established the electrocardiographic 
    foundation for differentiating early repolarization from subtle anterior STEMI. 
    Driver et al. (2017) enhanced the original 3-variable formula by adding QRS 
    amplitude in lead V2 as the fourth variable, significantly improving diagnostic 
    accuracy and clinical utility.
    
    The research involved retrospective analysis of patients presenting with chest 
    pain and ST elevation in precordial leads V2-V4 who underwent cardiac 
    catheterization. The study population included patients with both acute LAD 
    occlusion (subtle STEMI group) and those with angiographically normal coronaries 
    (benign early repolarization group).
    
    Enhanced 4-Variable Performance:
    The addition of QRS amplitude in lead V2 to the original formula resulted in 
    improved diagnostic performance:
    - Sensitivity: 83.3% (compared to 80% for 3-variable version)
    - Specificity: 87.7% (compared to 82% for 3-variable version)
    - Overall diagnostic accuracy: 85.9%
    - Area under the ROC curve: 0.926
    
    These performance metrics demonstrate superior accuracy compared to clinical 
    judgment alone and represent a significant advancement in emergency cardiac care.
    
    ECG Parameter Analysis and Clinical Significance:
    
    Bazett-corrected QT Interval (QTc):
    The QTc interval reflects the duration of ventricular repolarization and can be 
    prolonged in acute myocardial ischemia. In the context of subtle anterior STEMI, 
    ischemic myocardium exhibits delayed repolarization, contributing to QTc 
    prolongation. The positive coefficient (0.052) in the formula indicates that 
    longer QTc intervals increase the probability of STEMI.
    
    Clinical significance:
    - Ischemia-induced cellular electrophysiologic changes affect repolarization
    - Prolonged QTc may be an early sign of myocardial injury
    - Measurement technique is critical for accuracy
    - Normal variation exists between individuals and with age/gender
    
    QRS Amplitude in Lead V2:
    Lead V2 overlies the interventricular septum, which is typically supplied by 
    the first septal perforator branch of the LAD. Reduced QRS amplitude in V2 
    may indicate septal ischemia or injury, as ischemic myocardium generates 
    reduced electrical activity. The negative coefficient (-0.151) indicates 
    that lower QRS amplitudes increase STEMI probability.
    
    Clinical significance:
    - Septal involvement is common in anterior LAD occlusions
    - QRS amplitude reflects viable myocardial mass and electrical activity
    - Ischemic tissue contributes less to overall QRS voltage
    - This parameter adds specificity to the diagnostic algorithm
    
    R Wave Amplitude in Lead V4:
    Lead V4 overlies the anterior-lateral wall of the left ventricle, supplied 
    by the mid-to-distal LAD and possibly diagonal branches. Reduced R wave 
    amplitude may indicate anterior wall ischemia or injury. The negative 
    coefficient (-0.268) suggests that lower R wave amplitudes increase the 
    likelihood of STEMI.
    
    Clinical significance:
    - V4 represents the classic anterior wall territory
    - Loss of R wave amplitude may precede Q wave development
    - Reflects electrical activity of the anterior myocardial wall
    - Important for localizing the affected coronary territory
    
    ST Elevation in Lead V3 (60ms after J point):
    The degree of ST elevation, measured precisely 60 milliseconds after the 
    J point, is a critical parameter. This timing is important because measuring 
    at the J point itself can be less reliable due to notching or slurring. 
    The positive coefficient (1.062) indicates that greater ST elevation 
    increases STEMI probability.
    
    Clinical significance:
    - ST elevation magnitude correlates with degree of ischemia
    - 60ms measurement point improves specificity over J point measurement
    - Lead V3 represents the mid-anterior wall territory
    - Helps distinguish pathologic from physiologic ST elevation
    
    Mathematical Formula and Clinical Application:
    
    Score = 0.052 × QTc(ms) - 0.151 × QRS_V2(mm) - 0.268 × R_V4(mm) + 1.062 × ST_V3(mm)
    
    The formula integrates multiple ECG parameters to generate a composite score 
    that reflects the probability of acute coronary occlusion. Each coefficient 
    was derived through logistic regression analysis and represents the 
    independent contribution of each variable to the diagnostic outcome.
    
    Diagnostic Threshold: 18.2 Points
    This threshold was established through ROC curve analysis to optimize the 
    balance between sensitivity and specificity. The cutpoint was selected to 
    minimize both false negatives (missed STEMIs) and false positives (unnecessary 
    procedures) while maximizing overall diagnostic accuracy.
    
    Clinical Decision-Making Framework:
    
    Score <18.2 (Likely Benign Early Repolarization):
    
    Interpretation:
    - Low probability of acute coronary occlusion
    - Likely represents normal variant ST elevation
    - Suggests benign early repolarization pattern
    
    Recommended Actions:
    - Continue standard chest pain evaluation protocol
    - Serial ECGs every 15-30 minutes to monitor for evolution
    - Cardiac biomarkers per institutional protocol
    - Consider outpatient stress testing if symptoms persist
    - Patient education and appropriate discharge planning
    - Clear return precautions for symptom progression
    
    Important Caveats:
    - Clinical correlation remains essential
    - Do not ignore high clinical suspicion despite low score
    - Consider alternative diagnoses if appropriate
    - Serial assessment recommended regardless of initial score
    
    Score ≥18.2 (Likely Subtle Anterior STEMI):
    
    Interpretation:
    - High probability of acute LAD occlusion
    - May represent 100% coronary artery occlusion
    - Time-sensitive condition requiring urgent intervention
    
    Recommended Actions:
    - Immediate cardiology consultation
    - Consider emergent cardiac catheterization
    - Activate catheterization laboratory if appropriate
    - Dual antiplatelet therapy unless contraindicated
    - Anticoagulation per institutional protocol
    - Continuous cardiac monitoring
    - Preparation for primary percutaneous coronary intervention
    
    Quality Assurance and Performance Monitoring:
    
    ECG Measurement Standardization:
    - Ensure high-quality ECG recordings with minimal artifact
    - Use consistent measurement techniques across providers
    - Consider digital calipers for precise measurements
    - Regular calibration and quality checks
    
    Provider Training and Education:
    - Comprehensive training on ECG measurement techniques
    - Understanding of calculator limitations and appropriate use
    - Integration with clinical decision-making protocols
    - Regular case-based educational sessions
    
    Outcome Tracking:
    - Monitor diagnostic accuracy in local patient population
    - Track door-to-balloon times for confirmed STEMI cases
    - Assess false positive catheterization laboratory activations
    - Patient outcome analysis and quality improvement initiatives
    
    Special Considerations and Limitations:
    
    Patient Population Considerations:
    - Validation primarily in adult populations
    - May be less accurate in elderly patients with baseline ECG abnormalities
    - Consider impact of medications affecting QTc interval
    - Account for electrolyte abnormalities and other confounding factors
    
    Clinical Limitations:
    - Does not replace comprehensive clinical assessment
    - Requires accurate ECG measurement technique for reliability
    - May be less accurate in patients with prior MI or cardiomyopathy
    - Should be used in conjunction with clinical judgment and other diagnostic tools
    
    Technical Limitations:
    - Assumes standard ECG calibration and paper speed
    - Sensitive to measurement errors and technique variations
    - May be affected by ECG artifact or poor lead placement
    - Limited validation in certain patient subgroups
    
    Integration with Emergency Care Protocols:
    
    Workflow Integration:
    - Incorporate into chest pain evaluation pathways
    - Establish clear criteria for calculator use
    - Define roles and responsibilities for team members
    - Document decision-making rationale appropriately
    
    Communication Protocols:
    - Standardize communication with cardiology consultants
    - Provide complete clinical context with calculator results
    - Establish urgency levels based on score and clinical assessment
    - Ensure appropriate documentation and follow-up
    
    The Subtle Anterior STEMI Calculator (4-Variable) represents a significant 
    advancement in emergency cardiac care, providing evidence-based, objective 
    criteria to guide clinical decision-making in one of the most challenging 
    diagnostic scenarios in cardiology. When used appropriately within the 
    clinical context, it can improve patient outcomes by facilitating timely 
    recognition and treatment of subtle anterior STEMIs while reducing unnecessary 
    invasive procedures for benign conditions.
    
    Args:
        request: Subtle Anterior STEMI 4-Variable parameters including QTc interval, QRS amplitude V2, R wave amplitude V4, and ST elevation V3
        
    Returns:
        SubtleAnteriorStemi4VariableResponse: Calculated score with diagnostic probability and comprehensive clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("subtle_anterior_stemi_4_variable", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Subtle Anterior STEMI 4-Variable Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return SubtleAnteriorStemi4VariableResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Subtle Anterior STEMI 4-Variable calculation",
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
                "message": "Internal error in Subtle Anterior STEMI 4-Variable calculation",
                "details": {"error": str(e)}
            }
        )