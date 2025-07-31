"""
Corrected QT Interval (QTc) Router

Endpoint for calculating QTc using multiple validated correction formulas.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.corrected_qt_interval import (
    CorrectedQtIntervalRequest,
    CorrectedQtIntervalResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/corrected_qt_interval",
    response_model=CorrectedQtIntervalResponse,
    summary="Calculate Corrected QT Interval (QTc)",
    description="Corrects QT interval for heart rate extremes using multiple validated formulas (Bazett, Fridericia, Framingham, Hodges, or Rautaharju)",
    response_description="The calculated corrected qt interval with interpretation",
    operation_id="corrected_qt_interval"
)
async def calculate_corrected_qt_interval(request: CorrectedQtIntervalRequest):
    """
    Calculates Corrected QT Interval (QTc) using Multiple Validated Formulas
    
    The Corrected QT Interval (QTc) adjusts the measured QT interval for heart rate variations, 
    providing a standardized measure of cardiac repolarization duration that is essential for 
    accurate assessment of arrhythmic risk, drug safety monitoring, and diagnosis of inherited 
    cardiac conditions affecting ventricular repolarization.
    
    **Clinical Background and Significance**:
    
    **Cardiac Repolarization Assessment Framework**:
    - Primary tool for evaluating ventricular repolarization duration independent of heart rate
    - Essential for identifying Long QT Syndrome and Short QT Syndrome
    - Critical component of drug safety monitoring and pharmaceutical development
    - Standard assessment for patients receiving QT-prolonging medications
    - Fundamental measurement in cardiac electrophysiology and arrhythmia risk stratification
    
    **Physiological Foundation and Heart Rate Dependency**:
    The QT interval represents the duration of ventricular depolarization and repolarization, 
    naturally varying inversely with heart rate due to physiological adaptations in cardiac 
    action potential duration. At faster heart rates, the QT interval shortens to accommodate 
    shorter diastolic filling periods, while at slower rates it lengthens to maintain optimal 
    cardiac function.
    
    **Multiple Formula Validation and Clinical Applications**:
    
    **Five Validated Correction Formulas with Specific Clinical Applications**:
    
    **Bazett Formula (bazett) - Clinical Standard**:
    - **Formula**: QTc = QT / √RR (where RR = 60/heart rate in seconds)
    - **Clinical Applications**: Most widely used formula with extensive historical validation
    - **Regulatory Standard**: Required for pharmaceutical QT studies and drug safety assessment
    - **Optimal Range**: Heart rates 60-100 bpm provide most accurate correction
    - **Clinical Significance**: Basis for most published normal values and risk thresholds
    
    **Advantages and Clinical Context**:
    - Universal acceptance in clinical guidelines and regulatory frameworks
    - Extensive historical database for risk stratification and outcome prediction
    - Simple calculation facilitating widespread clinical adoption
    - Standard for comparison across studies and populations
    - Established diagnostic thresholds for Long QT Syndrome
    
    **Limitations and Clinical Considerations**:
    - Overcorrection at heart rates >100 bpm may lead to false prolongation diagnosis
    - Undercorrection at heart rates <60 bpm may miss true QT prolongation
    - Less accurate in patients with significant bradycardia or tachycardia
    - May overestimate arrhythmic risk in patients with sinus tachycardia
    
    **Fridericia Formula (fridericia) - Research Preferred**:
    - **Formula**: QTc = QT / (RR)^(1/3) (cube root correction)
    - **Clinical Applications**: Superior performance across wide heart rate ranges
    - **Research Evidence**: Better mortality prediction and rate correction in validation studies
    - **Optimal Applications**: Patients with extreme heart rates or research requiring high accuracy
    - **Clinical Significance**: Increasingly adopted in specialized clinical practice
    
    **Research Validation and Clinical Benefits**:
    - Studies demonstrate superior rate correction compared to Bazett formula
    - Better correlation with cardiovascular mortality outcomes
    - Reduced false positive rates for QT prolongation diagnosis
    - More consistent results across diverse patient populations
    - Improved accuracy in patients with heart rate extremes
    
    **Clinical Implementation Considerations**:
    - Requires adjustment of established Bazett-based thresholds
    - Growing evidence base supporting clinical adoption
    - Preferred choice for research studies requiring precise rate correction
    - Useful for validation when Bazett results are borderline
    
    **Framingham Formula (framingham) - Population-Based**:
    - **Formula**: QTc = QT + 154 × (1 - RR) (linear correction)
    - **Clinical Applications**: Derived from large-scale epidemiological studies
    - **Population Validation**: Extensive community-based validation with long-term follow-up
    - **Predictive Value**: Excellent predictor of cardiovascular outcomes and mortality
    - **Clinical Significance**: Strong evidence base for population-level risk assessment
    
    **Epidemiological Foundation and Clinical Utility**:
    - Developed from Framingham Heart Study with decades of follow-up data
    - Validated across diverse demographic groups and cardiovascular risk profiles
    - Strong association with cardiovascular mortality in community populations
    - Useful for population screening and epidemiological research applications
    - Good balance between accuracy and practical clinical implementation
    
    **Hodges Formula (hodges) - Linear Alternative**:
    - **Formula**: QTc = QT + 1.75 × [(60/RR) - 60] (linear rate relationship)
    - **Clinical Applications**: Alternative approach when primary formulas show discordance
    - **Performance Characteristics**: Good accuracy across heart rate ranges with linear relationship
    - **Research Utility**: Useful for validation studies requiring multiple correction methods
    - **Clinical Context**: Less commonly used but effective alternative approach
    
    **Rautaharju Formula (rautaharju) - Modern Standard**:
    - **Formula**: QTc = QT × (120 + HR) / 180 (direct heart rate incorporation)
    - **Clinical Applications**: Modern approach based on AHA/ACCF/HRS standardization recommendations
    - **Development Context**: Part of comprehensive electrocardiogram standardization initiative
    - **Clinical Significance**: Contemporary validation with modern ECG interpretation standards
    - **Implementation**: Uses heart rate directly rather than calculated RR interval
    
    **Clinical Interpretation Framework and Risk Stratification**:
    
    **Normal QTc Assessment and Management (≤440 ms)**:
    
    **Clinical Significance and Implications**:
    - Normal cardiac repolarization duration with low arrhythmic risk
    - No specific cardiac monitoring required beyond standard clinical care
    - Standard medication prescribing guidelines apply without QT considerations
    - Normal life expectancy and cardiovascular prognosis expected
    
    **Clinical Management Recommendations**:
    - Routine clinical follow-up according to underlying medical conditions
    - Document baseline QTc for future reference and comparison
    - Standard exercise and activity recommendations without cardiac restrictions
    - No specific lifestyle modifications required for QT-related concerns
    
    **Borderline QTc Assessment and Monitoring (440-480 ms)**:
    
    **Gender-Specific and Clinical Context Interpretation**:
    - Men: 440-450 ms borderline, >450 ms prolonged requiring closer monitoring
    - Women: 440-460 ms borderline, >460 ms prolonged with increased risk
    - Recent guidelines trend toward unified thresholds regardless of gender
    - Clinical context and risk factors crucial for management decisions
    
    **Comprehensive Clinical Assessment Protocol**:
    - Systematic medication review focusing on QT-prolonging agents
    - Complete electrolyte panel with emphasis on potassium, magnesium, calcium
    - Family history assessment for sudden cardiac death and inherited conditions
    - Structural heart disease evaluation including echocardiography when indicated
    
    **Monitoring and Follow-up Strategy**:
    - Serial ECG monitoring during initiation of QT-prolonging medications
    - Periodic QTc reassessment every 6-12 months or with clinical changes
    - Patient education regarding medication interactions and symptom recognition
    - Coordination with pharmacy for QT drug interaction screening
    
    **Prolonged QTc Assessment and Specialist Management (≥480 ms)**:
    
    **Diagnostic Criteria for Long QT Syndrome**:
    - QTc ≥480 ms diagnostic for Long QT Syndrome regardless of symptoms
    - QTc ≥460 ms with recurrent arrhythmic syncope also diagnostic
    - Strong predictor of torsades de pointes risk requiring immediate attention
    - Indicates need for urgent specialized cardiac electrophysiology evaluation
    
    **Immediate Clinical Action Protocol**:
    - Comprehensive medication review with immediate discontinuation of QT-prolonging drugs
    - Urgent electrolyte assessment and aggressive correction of abnormalities
    - Cardiology or electrophysiology consultation within 24-48 hours
    - Continuous cardiac monitoring consideration for high-risk patients
    
    **Long-term Management and Genetic Evaluation**:
    - Genetic testing for Long QT Syndrome mutations in patient and family
    - Comprehensive family screening protocol for asymptomatic relatives
    - Beta-blocker therapy initiation and optimization for symptom prevention
    - Activity restriction counseling based on specific LQTS subtype and risk
    - Implantable cardioverter-defibrillator evaluation for high-risk patients
    
    **Severely Prolonged QTc Emergency Management (>500 ms)**:
    
    **Critical Risk Stratification and Emergency Protocol**:
    - Very high risk of torsades de pointes with potential for sudden cardiac death
    - Immediate cardiology consultation with consideration for urgent hospitalization
    - Aggressive electrolyte optimization with continuous cardiac monitoring
    - Preparation for emergency cardioversion/defibrillation equipment availability
    
    **Specialized Care Coordination and Advanced Interventions**:
    - Urgent electrophysiology consultation for advanced risk stratification
    - Implantable cardioverter-defibrillator evaluation for primary prevention
    - Genetic testing expedited with immediate family screening protocols
    - Multidisciplinary care team coordination including pharmacy, nursing, genetics
    
    **Short QT Syndrome Recognition and Management (≤360 ms)**:
    
    **Diagnostic Framework for Short QT Syndrome**:
    - QTc ≤320 ms diagnostic for Short QT Syndrome with high sudden death risk
    - QTc 320-360 ms suggestive when combined with clinical criteria
    - Associated with increased risk of sudden cardiac death through ventricular arrhythmias
    - Requires specialized electrophysiology evaluation and genetic assessment
    
    **Clinical Evaluation and Risk Assessment**:
    - Comprehensive family history focusing on sudden cardiac death events
    - Personal history assessment for cardiac arrest, syncope, or palpitations
    - Genetic testing for known short QT syndrome mutations
    - Electrophysiology study consideration for inducible arrhythmias
    
    **Specialized Management Strategies**:
    - Implantable cardioverter-defibrillator evaluation for primary prevention
    - Avoidance of medications that further shorten QT interval
    - Activity restriction counseling based on individual risk assessment
    - Family screening protocols with genetic counseling services
    
    **Drug Safety and Pharmaceutical Monitoring**:
    
    **QT-Prolonging Medication Assessment**:
    - Systematic review of all medications for QT prolongation potential
    - Risk-benefit analysis for essential QT-prolonging medications
    - Alternative medication selection when possible to minimize QT risk
    - Dose optimization and monitoring protocols for continued QT-prolonging drugs
    
    **Drug Interaction Management**:
    - Assessment for cytochrome P450 interactions affecting QT-prolonging drugs
    - Evaluation of additive QT effects from multiple medications
    - Coordination with clinical pharmacy for comprehensive drug interaction screening
    - Patient education regarding over-the-counter medications and QT risk
    
    **Quality Assurance and Clinical Documentation**:
    
    **Measurement Standardization and Accuracy**:
    - Consistent ECG lead selection and measurement technique
    - Multiple beat averaging for accurate QT interval determination
    - Heart rate verification and rhythm assessment
    - Formula selection documentation with clinical rationale
    
    **Clinical Decision Documentation**:
    - QTc value recording with formula used and clinical interpretation
    - Risk assessment documentation with management plan
    - Patient education documentation and understanding verification
    - Follow-up monitoring plan with clear intervals and triggers
    
    This comprehensive QTc assessment provides clinicians with validated tools for accurate 
    cardiac repolarization evaluation, supporting evidence-based risk stratification and 
    management decisions across diverse clinical scenarios and patient populations.
    
    Args:
        request: QTc calculation parameters including QT interval, heart rate, and correction formula
        
    Returns:
        CorrectedQtIntervalResponse: Comprehensive QTc assessment with clinical interpretation and risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("corrected_qt_interval", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Corrected QT Interval (QTc)",
                    "details": {"parameters": parameters}
                }
            )
        
        return CorrectedQtIntervalResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for QTc calculation",
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