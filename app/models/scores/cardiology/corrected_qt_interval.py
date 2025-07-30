"""
Corrected QT Interval (QTc) Models

Request and response models for QTc calculation using multiple validated formulas.

References (Vancouver style):
1. Bazett HC. An analysis of the time-relations of electrocardiograms. Heart. 1920;7:353-370.
2. Fridericia LS. Die Systolendauer im Elektrokardiogramm bei normalen Menschen und bei Herzkranken. 
   Acta Med Scand. 1920;53:469-486.
3. Sagie A, Larson MG, Goldberg RJ, Bengtson JR, Levy D. An improved method for adjusting the QT 
   interval for heart rate (the Framingham Heart Study). Am J Cardiol. 1992;70(7):797-801.
4. Hodges M, Salerno D, Erlien D. Bazett's QT correction reviewed. Evidence that a linear QT 
   correction for heart rate is better. J Am Coll Cardiol. 1983;1(2):694.
5. Rautaharju PM, Surawicz B, Gettes LS, et al. AHA/ACCF/HRS recommendations for the 
   standardization and interpretation of the electrocardiogram. J Am Coll Cardiol. 2009;53(11):982-991.

The Corrected QT Interval (QTc) adjusts the measured QT interval for heart rate variations, 
providing a standardized measure of cardiac repolarization duration. This correction is 
essential for accurate assessment of QT prolongation and associated arrhythmic risk, 
particularly in the context of drug safety, genetic conditions, and electrolyte abnormalities.

Clinical Background and Development:

QT Interval Physiology:
The QT interval represents the duration of ventricular depolarization and repolarization, 
measured from the beginning of the QRS complex to the end of the T wave on the ECG. 
This interval varies inversely with heart rate, becoming shorter at faster rates and 
longer at slower rates due to physiological adaptations in cardiac action potential duration.

Need for Heart Rate Correction:
Raw QT interval measurements are difficult to interpret clinically due to their dependence 
on heart rate. At fast heart rates, the QT interval naturally shortens, while at slow 
rates it lengthens. Without correction for heart rate, clinically significant QT prolongation 
might be missed at fast rates, or normal QT intervals might be misinterpreted as prolonged 
at slow rates.

Historical Development of Correction Formulas:
Multiple correction formulas have been developed over the past century, each with specific 
advantages and limitations depending on the clinical context and heart rate range:

Bazett Formula (1920):
- First and most widely used correction formula
- QTc = QT / √RR (where RR is in seconds)
- Simple square root relationship with RR interval
- Tends to overcorrect at fast heart rates (>100 bpm) and undercorrect at slow rates (<60 bpm)
- Most commonly used in clinical practice and drug safety studies
- Recommended by many regulatory agencies for drug development

Fridericia Formula (1920):
- QTc = QT / (RR)^(1/3)
- Cube root relationship provides better correction across wider heart rate ranges
- Less affected by extreme heart rates compared to Bazett
- Increasingly preferred in research and clinical studies
- Better rate correction according to recent comparative studies

Framingham Formula (1992):
- QTc = QT + 154 × (1 - RR)
- Linear correction method developed from large population study
- Performs well across broad range of heart rates
- Good predictor of cardiovascular outcomes
- Derived from extensive epidemiological data

Hodges Formula (1983):
- QTc = QT + 1.75 × [(60/RR) - 60]
- Linear relationship with heart rate
- Good performance at extreme heart rates
- Less commonly used but effective alternative

Rautaharju Formula (2009):
- QTc = QT × (120 + HR) / 180
- Developed as part of AHA/ACCF/HRS standardization recommendations
- Incorporates heart rate directly rather than RR interval
- Modern approach based on extensive validation studies

Five-Formula Assessment Framework:

Bazett Formula Applications:
- Most established formula with extensive historical data
- Standard for drug safety and regulatory submissions
- Widely used in clinical practice and research
- Simple calculation facilitating widespread adoption
- Best for heart rates between 60-100 bpm

Clinical Significance:
- Regulatory standard for QT studies in drug development
- Baseline for most published normal values and risk thresholds
- Universal acceptance in clinical guidelines
- Established thresholds for arrhythmic risk assessment

Limitations:
- Overcorrection at heart rates >100 bpm leading to false prolongation
- Undercorrection at heart rates <60 bpm potentially missing true prolongation
- Less accurate in patients with significant bradycardia or tachycardia
- May overestimate arrhythmic risk in sinus tachycardia

Fridericia Formula Applications:
- Superior performance across wide heart rate ranges
- Preferred for research studies requiring accurate correction
- Better mortality prediction in comparative studies
- Reduced heart rate dependency compared to Bazett
- Increasingly adopted in clinical practice

Clinical Significance:
- More accurate correction at extreme heart rates
- Better correlation with clinical outcomes
- Reduced false positive rates for QT prolongation
- Improved specificity for identifying true QT abnormalities

Research Evidence:
- Studies show superior rate correction compared to Bazett
- Better prediction of cardiovascular mortality
- More consistent results across different populations
- Reduced variability in serial measurements

Framingham Formula Applications:
- Derived from large-scale epidemiological study
- Excellent predictor of cardiovascular outcomes
- Linear correction method with intuitive interpretation
- Good performance across diverse populations
- Strong evidence base for risk stratification

Clinical Significance:
- Population-based validation with extensive follow-up data
- Strong association with cardiovascular mortality
- Practical application in risk assessment
- Good balance between accuracy and simplicity

Population Health Applications:
- Developed from community-based cohort study
- Validated in diverse demographic groups
- Useful for population screening and epidemiological research
- Strong evidence for cardiovascular risk prediction

Hodges and Rautaharju Formula Applications:
- Alternative approaches for specific clinical scenarios
- Useful when primary formulas show discordant results
- Research applications requiring multiple correction methods
- Validation of findings across different correction approaches

Clinical Interpretation Framework:

Normal Values and Thresholds:
Based on extensive population studies and clinical outcome data:

Gender-Specific Normal Values:
- Men: QTc <450 ms (normal), 450-460 ms (borderline), >460 ms (prolonged)
- Women: QTc <460 ms (normal), 460-470 ms (borderline), >470 ms (prolonged)
- Recent guidelines suggest unified thresholds for both genders

Clinical Risk Stratification:

Normal QTc (≤440 ms):
- Low arrhythmic risk
- Normal cardiac repolarization
- No specific monitoring required
- Standard clinical care appropriate

Borderline QTc (440-480 ms):
- Gender-specific interpretation required
- Consider clinical context and risk factors
- Monitor for progression
- Review medications and electrolytes

Prolonged QTc (≥480 ms):
- Diagnostic for Long QT Syndrome regardless of symptoms
- High risk of torsades de pointes
- Requires specialized evaluation
- Consider genetic testing and family screening

Severely Prolonged QTc (>500 ms):
- Very high risk of sudden cardiac death
- Immediate cardiology consultation required
- Continuous cardiac monitoring recommended
- Urgent intervention may be necessary

Short QT Syndrome:
- QTc ≤320 ms: Diagnostic for Short QT Syndrome
- QTc 320-360 ms: Suggestive with additional clinical criteria
- Associated with increased sudden cardiac death risk
- Requires specialized electrophysiology evaluation

Clinical Applications and Use Cases:

Drug Safety and Monitoring:
- Pre-prescription baseline QTc assessment
- Serial monitoring during treatment with QT-prolonging medications
- Drug interaction assessment
- Regulatory requirement for new drug development

Genetic Conditions:
- Long QT Syndrome diagnosis and management
- Short QT Syndrome identification
- Family screening and genetic counseling
- Risk stratification for sudden cardiac death

Electrolyte and Metabolic Monitoring:
- Hypokalemia and hypomagnesemia assessment
- Hypocalcemia evaluation
- Thyroid disorder monitoring
- Renal disease management

Perioperative Assessment:
- Preoperative risk stratification
- Anesthesia planning and monitoring
- Postoperative complication prevention
- ICU patient monitoring

Implementation Guidelines and Quality Assurance:

ECG Measurement Standards:
- Use consistent lead (typically lead II or V5)
- Measure multiple beats and average results
- Ensure proper calibration and paper speed
- Document measurement methodology

Heart Rate Assessment:
- Use simultaneous heart rate from same ECG strip
- Calculate from RR interval when possible
- Account for rhythm irregularities
- Consider automated vs. manual measurements

Quality Control Measures:
- Verify calculation accuracy with multiple formulas
- Compare results across different correction methods
- Consider clinical context when interpreting results
- Document discrepancies and clinical decisions

Limitations and Clinical Considerations:

Formula-Specific Limitations:
- Each formula has optimal heart rate ranges
- Results may vary significantly between formulas
- Clinical correlation always required
- Population-specific validation may differ

Technical Limitations:
- Dependent on accurate QT interval measurement
- Affected by T wave morphology and measurement endpoints
- Limited in presence of significant arrhythmias
- May be confounded by bundle branch blocks

Clinical Context Requirements:
- Must consider patient age, gender, and medical history
- Account for medications and electrolyte status
- Evaluate for structural heart disease
- Consider family history and genetic factors

This comprehensive QTc assessment provides clinicians with multiple validated approaches 
to heart rate correction, supporting accurate diagnosis and risk stratification for 
patients with potential cardiac repolarization abnormalities.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CorrectedQtIntervalRequest(BaseModel):
    """
    Request model for Corrected QT Interval (QTc) Calculation
    
    The QTc corrects the measured QT interval for heart rate variations using validated 
    formulas, providing accurate assessment of cardiac repolarization duration and 
    associated arrhythmic risk across different clinical scenarios.
    
    Assessment Framework and Parameter Specifications:
    
    The QTc calculation requires three essential parameters for accurate heart rate 
    correction and clinical interpretation:
    
    QT Interval Measurement:
    The QT interval represents the duration of ventricular depolarization and repolarization, 
    measured from the beginning of the QRS complex to the end of the T wave on the ECG. 
    Accurate measurement is critical for reliable QTc calculation and clinical interpretation.
    
    Measurement Guidelines:
    - Use consistent ECG lead (typically lead II, V5, or V6)
    - Measure from QRS onset to T wave termination
    - Average measurements from multiple beats when possible
    - Ensure proper ECG calibration and paper speed (25 mm/s standard)
    - Account for T wave morphology variations
    
    Clinical Significance:
    - Reflects total ventricular repolarization time
    - Baseline measurement for heart rate correction
    - Critical for identifying repolarization abnormalities
    - Essential for drug safety monitoring
    
    Measurement Challenges:
    - U waves may complicate T wave endpoint identification
    - Bundle branch blocks can affect measurement accuracy
    - Atrial fibrillation requires averaging multiple beats
    - Baseline artifacts may interfere with precise measurement
    
    Heart Rate Assessment:
    Heart rate provides the physiological context for QT interval correction, as the 
    QT interval naturally varies inversely with heart rate due to autonomic and 
    cellular mechanisms affecting action potential duration.
    
    Measurement Standards:
    - Use heart rate from same ECG strip as QT measurement
    - Calculate from RR interval when rhythm is regular
    - Average heart rate over 10-beat period for accuracy
    - Document rhythm regularity and any arrhythmias
    - Consider automated vs. manual heart rate determination
    
    Clinical Significance:
    - Determines degree of correction required
    - Affects formula selection and interpretation
    - Critical for accurate QTc calculation
    - Important for identifying rate-related QT changes
    
    Physiological Considerations:
    - Normal QT shortening with increased heart rate
    - QT prolongation with decreased heart rate
    - Autonomic influences on rate-QT relationship
    - Age and gender effects on heart rate variability
    
    Formula Selection:
    The choice of correction formula significantly affects QTc results and clinical 
    interpretation. Each formula has specific advantages, limitations, and optimal 
    applications based on heart rate range and clinical context.
    
    Bazett Formula (bazett):
    QTc = QT / √RR (where RR = 60/HR seconds)
    
    Clinical Applications:
    - Most widely used and established formula
    - Standard for regulatory drug safety studies
    - Basis for most published normal values
    - Universal acceptance in clinical guidelines
    - Optimal for heart rates 60-100 bpm
    
    Advantages:
    - Extensive historical data and validation
    - Simple calculation facilitating widespread use
    - Established clinical thresholds and risk categories
    - Regulatory standard for pharmaceutical development
    
    Limitations:
    - Overcorrection at heart rates >100 bpm
    - Undercorrection at heart rates <60 bpm
    - May overestimate risk in sinus tachycardia
    - Less accurate at extreme heart rates
    
    Fridericia Formula (fridericia):
    QTc = QT / (RR)^(1/3)
    
    Clinical Applications:
    - Superior performance across wide heart rate ranges
    - Preferred for research requiring accurate correction
    - Better mortality prediction in comparative studies
    - Increasingly adopted in specialized clinical practice
    
    Advantages:
    - More accurate at extreme heart rates
    - Better correlation with clinical outcomes
    - Reduced false positive rates
    - Superior rate correction in validation studies
    
    Research Evidence:
    - Studies demonstrate better rate correction than Bazett
    - Improved prediction of cardiovascular mortality
    - More consistent results across populations
    - Reduced measurement variability
    
    Framingham Formula (framingham):
    QTc = QT + 154 × (1 - RR)
    
    Clinical Applications:
    - Population-based validation with extensive follow-up
    - Excellent predictor of cardiovascular outcomes
    - Linear correction method with intuitive interpretation
    - Strong evidence base for risk stratification
    
    Advantages:
    - Derived from large epidemiological study
    - Strong association with mortality outcomes
    - Good performance across diverse populations
    - Practical application in risk assessment
    
    Population Health Applications:
    - Community-based validation
    - Useful for screening and epidemiological research
    - Strong cardiovascular risk prediction
    - Broad demographic validation
    
    Hodges Formula (hodges):
    QTc = QT + 1.75 × [(60/RR) - 60]
    
    Clinical Applications:
    - Linear relationship with heart rate
    - Good performance at extreme heart rates
    - Alternative when primary formulas show discordance
    - Research applications requiring multiple methods
    
    Advantages:
    - Linear correction approach
    - Less complex than exponential formulas
    - Good accuracy across heart rate ranges
    - Alternative validation method
    
    Rautaharju Formula (rautaharju):
    QTc = QT × (120 + HR) / 180
    
    Clinical Applications:
    - Modern approach based on standardization recommendations
    - Uses heart rate directly rather than RR interval
    - Developed for contemporary clinical practice
    - Part of AHA/ACCF/HRS standardization efforts
    
    Advantages:
    - Direct heart rate incorporation
    - Modern validation methodology
    - Standardization committee endorsement
    - Contemporary clinical validation
    
    Clinical Decision-Making and Formula Selection:
    
    Standard Clinical Practice:
    - Bazett formula for routine clinical use
    - Fridericia for patients with extreme heart rates
    - Multiple formulas when results are borderline
    - Consider clinical context and patient factors
    
    Research Applications:
    - Use multiple formulas for validation
    - Report results from primary and secondary formulas
    - Consider population-specific validation data
    - Account for study design and objectives
    
    Drug Safety Monitoring:
    - Bazett formula for regulatory compliance
    - Secondary formula for validation
    - Consider heart rate effects of study drug
    - Document formula selection rationale
    
    Quality Assurance and Validation:
    
    Measurement Verification:
    - Verify QT interval measurement accuracy
    - Confirm heart rate calculation
    - Check formula application
    - Review clinical context and interpretation
    
    Clinical Correlation:
    - Compare results across multiple formulas
    - Consider patient-specific factors
    - Evaluate clinical symptoms and history
    - Account for medications and comorbidities
    
    Documentation Standards:
    - Record formula used for calculation
    - Document measurement methodology
    - Note any measurement challenges
    - Provide clinical interpretation context
    
    References (Vancouver style):
    1. Bazett HC. An analysis of the time-relations of electrocardiograms. Heart. 1920;7:353-370.
    2. Fridericia LS. Die Systolendauer im Elektrokardiogramm bei normalen Menschen und bei Herzkranken. 
       Acta Med Scand. 1920;53:469-486.
    3. Sagie A, Larson MG, Goldberg RJ, Bengtson JR, Levy D. An improved method for adjusting the QT 
       interval for heart rate (the Framingham Heart Study). Am J Cardiol. 1992;70(7):797-801.
    """
    
    qt_interval: int = Field(
        ...,
        ge=200,
        le=800,
        description="QT interval measured on ECG in milliseconds. Measure from QRS onset to T wave termination using consistent lead (typically II, V5, or V6). Average multiple beats when possible",
        example=420
    )
    
    heart_rate: int = Field(
        ...,
        ge=30,
        le=300,
        description="Heart rate measured on ECG in beats per minute. Use simultaneous heart rate from same ECG strip as QT measurement. Calculate from RR interval when rhythm is regular",
        example=75
    )
    
    formula: Literal["bazett", "fridericia", "framingham", "hodges", "rautaharju"] = Field(
        ...,
        description="QTc correction formula: bazett (most common, regulatory standard), fridericia (better at extreme HR), framingham (population-based), hodges (linear), rautaharju (modern AHA standard)",
        example="bazett"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "qt_interval": 420,
                "heart_rate": 75,
                "formula": "bazett"
            }
        }


class CalculationDetails(BaseModel):
    """Detailed calculation information for QTc assessment"""
    
    formula_used: str = Field(
        ...,
        description="Name of the correction formula used",
        example="Bazett"
    )
    
    rr_interval: float = Field(
        ...,
        description="RR interval calculated from heart rate (seconds)",
        example=0.800
    )
    
    formula_equation: str = Field(
        ...,
        description="Specific equation used with actual values",
        example="QTc = 420 / √0.800 = 420 / 0.894"
    )
    
    clinical_significance: str = Field(
        ...,
        description="Clinical significance of the calculated QTc value",
        example="Normal cardiac repolarization"
    )
    
    risk_level: str = Field(
        ...,
        description="Arrhythmic risk level based on QTc value",
        example="Low"
    )


class CorrectedQtIntervalResponse(BaseModel):
    """
    Response model for Corrected QT Interval (QTc) Calculation
    
    Provides comprehensive QTc assessment with clinical interpretation, risk stratification, 
    and evidence-based recommendations for cardiac monitoring and management based on 
    validated correction formulas and established clinical thresholds.
    
    QTc Assessment Framework and Clinical Interpretation:
    
    Scale Overview and Clinical Significance:
    The QTc represents the QT interval corrected for heart rate, providing a standardized 
    measure of cardiac repolarization duration that is independent of heart rate variations. 
    This correction is essential for accurate assessment of arrhythmic risk, drug safety 
    monitoring, and diagnosis of inherited cardiac conditions.
    
    Clinical Applications and Diagnostic Framework:
    
    Normal QTc Assessment (≤440 ms):
    
    Clinical Significance:
    - Normal cardiac repolarization duration
    - Low risk of ventricular arrhythmias
    - No specific cardiac monitoring required
    - Standard clinical care appropriate
    
    Management Recommendations:
    - Routine clinical follow-up as indicated
    - Standard medication prescribing guidelines
    - No additional cardiac monitoring required
    - Document baseline for future reference
    
    Quality of Life Implications:
    - Normal activities without cardiac restrictions
    - Standard exercise and activity recommendations
    - No specific lifestyle modifications required
    - Normal life expectancy and prognosis
    
    Borderline QTc Assessment (440-480 ms):
    
    Gender-Specific Interpretation:
    - Men: 440-450 ms borderline, >450 ms prolonged
    - Women: 440-460 ms borderline, >460 ms prolonged
    - Recent guidelines trend toward unified thresholds
    - Clinical context crucial for interpretation
    
    Clinical Decision Framework:
    - Review medications with QT prolongation potential
    - Assess electrolyte status (K+, Mg2+, Ca2+)
    - Consider family history of sudden cardiac death
    - Evaluate for structural heart disease
    
    Monitoring Recommendations:
    - Serial ECG monitoring during medication changes
    - Periodic reassessment every 6-12 months
    - Patient education about medication interactions
    - Awareness of symptoms requiring urgent evaluation
    
    Risk Modification Strategies:
    - Optimize electrolyte levels
    - Review and minimize QT-prolonging medications
    - Lifestyle modifications for cardiovascular health
    - Consider genetic counseling if family history present
    
    Prolonged QTc Assessment (≥480 ms):
    
    Diagnostic Criteria for Long QT Syndrome:
    - QTc ≥480 ms diagnostic regardless of symptoms
    - QTc ≥460 ms with recurrent arrhythmic syncope
    - Strong predictor of torsades de pointes risk
    - Indicates need for specialized cardiac evaluation
    
    Immediate Clinical Actions:
    - Comprehensive medication review and optimization
    - Complete electrolyte panel and correction
    - Cardiology or electrophysiology consultation
    - Continuous cardiac monitoring in high-risk patients
    
    Long-Term Management Strategies:
    - Genetic testing for Long QT Syndrome
    - Family screening and counseling
    - Beta-blocker therapy consideration
    - Activity restriction counseling
    - ICD evaluation in high-risk patients
    
    Lifestyle and Activity Modifications:
    - Avoid QT-prolonging medications when possible
    - Maintain optimal electrolyte levels
    - Consider activity restrictions based on risk
    - Emergency action plan for syncope episodes
    
    Severely Prolonged QTc Assessment (>500 ms):
    
    Critical Risk Stratification:
    - Very high risk of torsades de pointes
    - Immediate risk of sudden cardiac death
    - Requires urgent cardiology intervention
    - May need continuous cardiac monitoring
    
    Emergency Management Protocol:
    - Immediate cardiology consultation
    - Discontinue all QT-prolonging medications
    - Aggressive electrolyte optimization
    - Consider temporary pacing if bradycardic
    - Prepare for emergency defibrillation
    
    Specialized Care Requirements:
    - Electrophysiology consultation urgent
    - Consider ICD implantation evaluation
    - Genetic testing and family screening urgent
    - Intensive cardiac monitoring
    - Multidisciplinary care coordination
    
    Short QT Syndrome Assessment (≤360 ms):
    
    Diagnostic Criteria:
    - QTc ≤320 ms diagnostic for Short QT Syndrome
    - QTc 320-360 ms suggestive with clinical criteria
    - Associated with increased sudden death risk
    - Requires specialized electrophysiology evaluation
    
    Clinical Evaluation Requirements:
    - Family history of sudden cardiac death
    - Personal history of cardiac arrest or syncope
    - Genetic testing for short QT mutations
    - Electrophysiology study consideration
    
    Management Considerations:
    - ICD evaluation for primary prevention
    - Avoid drugs that further shorten QT
    - Activity restriction counseling
    - Family screening protocols
    
    Formula-Specific Interpretation Considerations:
    
    Bazett Formula Results:
    - Most established clinical thresholds
    - Standard for regulatory and clinical guidelines
    - May overestimate risk at fast heart rates
    - Underestimate risk at slow heart rates
    
    Alternative Formula Validation:
    - Use Fridericia or Framingham for validation
    - Consider multiple formulas for borderline results
    - Document formula-specific interpretations
    - Account for heart rate-dependent accuracy
    
    Clinical Decision Integration:
    - Combine QTc results with clinical presentation
    - Consider family history and genetic factors
    - Account for medications and comorbidities
    - Integrate with other cardiac risk markers
    
    Quality Assurance and Follow-up:
    
    Documentation Standards:
    - Record QTc value and formula used
    - Document clinical interpretation and risk level
    - Note any confounding factors
    - Plan for follow-up monitoring
    
    Patient Education Components:
    - Explain QTc significance and implications
    - Provide medication interaction guidelines
    - Discuss symptom recognition and response
    - Coordinate care with other providers
    
    Long-term Monitoring Strategy:
    - Schedule appropriate follow-up intervals
    - Plan for medication and electrolyte monitoring
    - Coordinate with specialist care as needed
    - Adjust monitoring based on risk changes
    
    This comprehensive QTc assessment provides clinicians with the information needed 
    to accurately interpret cardiac repolarization status and implement appropriate 
    monitoring and management strategies based on evidence-based thresholds and 
    clinical guidelines.
    
    Reference: Bazett HC. Heart. 1920;7:353-370.
    """
    
    result: float = Field(
        ...,
        description="Corrected QT interval (QTc) value in milliseconds",
        example=469.4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the QTc value",
        example="ms"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the QTc value with specific recommendations and risk assessment",
        example="QTc of 469.4 ms is prolonged for both sexes (460-480 ms). Increased risk of arrhythmias. Evaluate for reversible causes and consider medication review."
    )
    
    stage: str = Field(
        ...,
        description="QTc interval classification (Normal, Borderline, Prolonged, Severely Prolonged, Short QT, etc.)",
        example="Prolonged"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the QTc interval category",
        example="Prolonged QTc interval"
    )
    
    calculation_details: CalculationDetails = Field(
        ...,
        description="Detailed calculation information including formula specifics and clinical significance"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 469.4,
                "unit": "ms",
                "interpretation": "QTc of 469.4 ms is prolonged for both sexes (460-480 ms). Increased risk of arrhythmias. Evaluate for reversible causes and consider medication review.",
                "stage": "Prolonged",
                "stage_description": "Prolonged QTc interval",
                "calculation_details": {
                    "formula_used": "Bazett",
                    "rr_interval": 0.800,
                    "formula_equation": "QTc = 420 / √0.800 = 420 / 0.894",
                    "clinical_significance": "Increased arrhythmic risk",
                    "risk_level": "Moderate-High"
                }
            }
        }