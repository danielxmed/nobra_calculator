"""
Geneva Score (Revised) for Pulmonary Embolism Models

Request and response models for Geneva Score (Revised) PE calculation.

References (Vancouver style):
1. Le Gal G, Righini M, Roy PM, et al. Prediction of pulmonary embolism in the emergency 
   department: the revised Geneva score. Ann Intern Med. 2006;144(3):165-171. 
   doi: 10.7326/0003-4819-144-3-200602070-00004.
2. Klok FA, Mos IC, Nijkeuter M, et al. Simplification of the revised Geneva score for 
   assessing clinical probability of pulmonary embolism. Arch Intern Med. 2008;168(19):2131-2136. 
   doi: 10.1001/archinte.168.19.2131.
3. Ceriani E, Combescure C, Le Gal G, et al. Clinical prediction rules for pulmonary embolism: 
   a systematic review and meta-analysis. J Thromb Haemost. 2010;8(5):957-970. 
   doi: 10.1111/j.1538-7836.2010.03801.x.

The Geneva Score (Revised) for Pulmonary Embolism is a validated clinical decision rule 
that provides an objective assessment of pulmonary embolism probability without requiring 
clinical gestalt. Developed as an alternative to Wells' criteria, this score incorporates 
8 clinical parameters to stratify patients into low, intermediate, or high risk categories 
for PE, guiding appropriate diagnostic workup and management decisions.

Key Clinical Applications:
- Emergency department and outpatient PE risk stratification
- Objective assessment without subjective clinical judgment
- Guide D-dimer testing and imaging decisions
- Standardized approach to PE diagnosis across clinicians
- Cost-effective diagnostic pathway optimization

The score ranges from 0-25 points and has been extensively validated in multiple studies, 
demonstrating comparable performance to Wells' criteria while offering the advantage of 
being more reproducible across different healthcare providers. It helps identify patients 
who can safely forego further testing (low risk with negative D-dimer) versus those 
requiring urgent imaging (high risk patients).

Clinical validation studies have shown that low-risk patients (0-3 points) have less than 
10% PE incidence, intermediate-risk patients (4-10 points) have 20-30% incidence, and 
high-risk patients (≥11 points) have greater than 60% PE incidence. This risk stratification 
enables appropriate resource utilization while maintaining diagnostic accuracy and patient safety.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GenevaScoreRevisedPeRequest(BaseModel):
    """
    Request model for Geneva Score (Revised) for Pulmonary Embolism
    
    The Geneva Score (Revised) for Pulmonary Embolism provides objective assessment of PE 
    probability using 8 clinical parameters without requiring subjective clinical gestalt. 
    This validated decision rule helps clinicians determine appropriate diagnostic pathways 
    and resource utilization in patients with suspected pulmonary embolism.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Clinical Application**:
    - **Target Population**: Patients presenting with suspected pulmonary embolism
    - **Clinical Setting**: Emergency departments, outpatient clinics, urgent care facilities
    - **Decision Point**: Initial assessment before D-dimer testing or imaging
    - **Validation**: Extensively validated in multicenter prospective studies
    
    **Key Advantages over Wells' Criteria**:
    - **Objective Assessment**: No requirement for subjective "PE most likely diagnosis" judgment
    - **Reproducibility**: Consistent results across different clinicians and settings
    - **Standardization**: Eliminates inter-observer variability in clinical gestalt
    - **Training**: Easier to teach and implement in clinical practice
    
    **CLINICAL PARAMETER INTERPRETATION GUIDE**:
    
    **DEMOGRAPHIC AND HISTORICAL FACTORS**:
    
    **Age Greater than 65 Years (1 point)**:
    - **Clinical Rationale**: Age-related increase in VTE risk due to multiple factors
    - **Pathophysiology**: Reduced mobility, increased comorbidities, hypercoagulable changes
    - **Assessment**: Based on chronological age at time of presentation
    - **Clinical Context**: Part of comprehensive geriatric risk assessment
    
    **Previous DVT or PE (3 points)**:
    - **Clinical Rationale**: Strong predictor of recurrent venous thromboembolism
    - **Pathophysiology**: Residual vascular damage, genetic predisposition, ongoing risk factors
    - **Assessment**: Documented history of venous thromboembolism confirmed by imaging
    - **Clinical Context**: Includes both proximal and distal DVT, any previous PE episode
    - **Documentation**: Should be verified through medical records or imaging reports
    
    **RECENT PRECIPITATING FACTORS**:
    
    **Surgery or Lower Limb Fracture within Past Month (2 points)**:
    - **Clinical Rationale**: Major surgery and trauma are well-established VTE risk factors
    - **Pathophysiology**: Immobilization, tissue factor release, inflammatory response
    - **Assessment**: Any surgical procedure or lower extremity fracture within 30 days
    - **Clinical Context**: Includes both major and minor surgical procedures
    - **Risk Duration**: Elevated risk persists for weeks to months post-procedure
    
    **Active Malignant Condition (2 points)**:
    - **Clinical Rationale**: Cancer is among the strongest risk factors for VTE
    - **Pathophysiology**: Tumor-induced hypercoagulability, chemotherapy effects, immobilization
    - **Assessment**: Currently receiving treatment or treatment within past 6 months
    - **Clinical Context**: Includes solid tumors, hematologic malignancies, metastatic disease
    - **Risk Variation**: Higher risk with certain cancer types (pancreatic, lung, brain)
    
    **CLINICAL SYMPTOMS AND SIGNS**:
    
    **Unilateral Lower Limb Pain (3 points)**:
    - **Clinical Rationale**: May indicate concurrent deep vein thrombosis
    - **Pathophysiology**: Venous obstruction causing pain, swelling, and inflammation
    - **Assessment**: Pain localized to one lower extremity, particularly calf or thigh
    - **Clinical Context**: Often accompanies pulmonary embolism in 30-50% of cases
    - **Differential**: Must differentiate from musculoskeletal, arterial, or other causes
    
    **Hemoptysis (2 points)**:
    - **Clinical Rationale**: Classic symptom of pulmonary embolism
    - **Pathophysiology**: Pulmonary infarction, alveolar hemorrhage, pleural irritation
    - **Assessment**: Coughing up blood or blood-tinged sputum
    - **Clinical Context**: May be minimal (blood-streaked sputum) or frank hemoptysis
    - **Differential**: Must exclude other causes like pneumonia, malignancy, bronchitis
    
    **Pain on Lower Limb Deep Venous Palpation and Unilateral Edema (4 points)**:
    - **Clinical Rationale**: Physical findings suggestive of deep vein thrombosis
    - **Pathophysiology**: Venous obstruction causing tenderness, swelling, and inflammation
    - **Assessment**: Requires both pain with deep palpation AND unilateral edema
    - **Clinical Context**: Most valuable when asymmetric between legs
    - **Technique**: Systematic palpation of calf and thigh venous pathways
    
    **VITAL SIGNS ASSESSMENT**:
    
    **Heart Rate Categories**:
    
    **Heart Rate <75 bpm (0 points)**:
    - **Clinical Context**: Normal heart rate, no additional PE risk
    - **Assessment**: Resting heart rate measured in clinical setting
    - **Considerations**: May be influenced by medications (beta-blockers), fitness level
    
    **Heart Rate 75-94 bpm (3 points)**:
    - **Clinical Context**: Mild tachycardia possibly related to PE
    - **Pathophysiology**: Compensatory response to impaired gas exchange or cardiac output
    - **Assessment**: Consistent measurements preferably after brief rest
    
    **Heart Rate ≥95 bpm (5 points)**:
    - **Clinical Context**: Significant tachycardia strongly suggestive of PE
    - **Pathophysiology**: Hemodynamic compromise, hypoxemia, pain response
    - **Assessment**: Persistent tachycardia not explained by other causes
    - **Clinical Significance**: Highest point value reflecting strong association with PE
    
    **CLINICAL DECISION FRAMEWORK**:
    
    **Risk Assessment and Management**:
    
    **Low Risk (0-3 points)**:
    - **PE Incidence**: <10% probability of pulmonary embolism
    - **Management**: D-dimer testing recommended as next step
    - **Interpretation**: Negative D-dimer rules out PE; positive D-dimer warrants imaging
    - **Cost-Effectiveness**: Avoids unnecessary imaging in majority of low-risk patients
    
    **Intermediate Risk (4-10 points)**:
    - **PE Incidence**: 20-30% probability of pulmonary embolism
    - **Management**: D-dimer testing followed by imaging if positive
    - **Interpretation**: Negative D-dimer makes PE unlikely; positive requires CT-PA
    - **Clinical Judgment**: Consider patient factors and clinical context
    
    **High Risk (≥11 points)**:
    - **PE Incidence**: >60% probability of pulmonary embolism
    - **Management**: Urgent CT pulmonary angiogram recommended
    - **Rationale**: High pretest probability justifies direct imaging
    - **D-dimer**: Not necessary due to high clinical probability
    
    **Special Considerations**:
    
    **Age-Adjusted D-dimer**:
    - Consider age-adjusted cutoffs (age × 10 ng/mL) in patients >50 years
    - May improve specificity without significantly reducing sensitivity
    - Particularly valuable in elderly patients with higher baseline D-dimer levels
    
    **Clinical Limitations**:
    - Not validated in hospitalized patients (outpatient/ED use only)
    - Should not replace clinical judgment in obvious high-risk scenarios
    - Requires accurate clinical assessment and measurement of parameters
    - May be less reliable in patients with multiple comorbidities
    
    **Quality Improvement Applications**:
    - Standardize PE assessment protocols across emergency departments
    - Reduce unnecessary imaging and associated healthcare costs
    - Improve diagnostic accuracy and patient safety
    - Educational tool for training healthcare providers
    
    References (Vancouver style):
    1. Le Gal G, Righini M, Roy PM, et al. Prediction of pulmonary embolism in the emergency 
       department: the revised Geneva score. Ann Intern Med. 2006;144(3):165-171.
    2. Klok FA, Mos IC, Nijkeuter M, et al. Simplification of the revised Geneva score for 
       assessing clinical probability of pulmonary embolism. Arch Intern Med. 2008;168(19):2131-2136.
    3. Ceriani E, Combescure C, Le Gal G, et al. Clinical prediction rules for pulmonary embolism: 
       a systematic review and meta-analysis. J Thromb Haemost. 2010;8(5):957-970.
    """
    
    age_over_65: Literal["yes", "no"] = Field(
        ...,
        description="Age greater than 65 years. Scores 1 point if yes",
        example="no"
    )
    
    previous_dvt_pe: Literal["yes", "no"] = Field(
        ...,
        description="Previous history of deep vein thrombosis or pulmonary embolism documented by imaging. Scores 3 points if yes",
        example="no"
    )
    
    surgery_fracture_past_month: Literal["yes", "no"] = Field(
        ...,
        description="Surgery (any type) or lower limb fracture within the past month (30 days). Scores 2 points if yes",
        example="no"
    )
    
    active_malignancy: Literal["yes", "no"] = Field(
        ...,
        description="Active malignant condition (currently receiving treatment or treatment within past 6 months). Scores 2 points if yes",
        example="no"
    )
    
    unilateral_limb_pain: Literal["yes", "no"] = Field(
        ...,
        description="Unilateral lower limb pain (calf or thigh pain localized to one leg). May suggest concurrent DVT. Scores 3 points if yes",
        example="no"
    )
    
    hemoptysis: Literal["yes", "no"] = Field(
        ...,
        description="Hemoptysis (coughing up blood or blood-tinged sputum). Classic PE symptom. Scores 2 points if yes",
        example="no"
    )
    
    heart_rate_category: Literal["under_75", "75_to_94", "95_or_higher"] = Field(
        ...,
        description="Heart rate category in beats per minute. <75 bpm=0 points, 75-94 bpm=3 points, ≥95 bpm=5 points",
        example="75_to_94"
    )
    
    limb_palpation_edema: Literal["yes", "no"] = Field(
        ...,
        description="Pain on lower limb deep venous palpation AND unilateral edema (both must be present). Suggests DVT. Scores 4 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_over_65": "no",
                "previous_dvt_pe": "no",
                "surgery_fracture_past_month": "no",
                "active_malignancy": "no",
                "unilateral_limb_pain": "yes",
                "hemoptysis": "no",
                "heart_rate_category": "75_to_94",
                "limb_palpation_edema": "no"
            }
        }


class GenevaScoreRevisedPeResponse(BaseModel):
    """
    Response model for Geneva Score (Revised) for Pulmonary Embolism
    
    The response provides the calculated Geneva PE score with detailed clinical interpretation 
    and evidence-based diagnostic recommendations based on validated risk stratification 
    thresholds from multicenter prospective studies.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **Geneva PE Score Components**:
    - **Total Score Range**: 0-25 points with three distinct risk categories
    - **Objective Assessment**: No subjective clinical gestalt required
    - **Validation**: Extensively validated in emergency department and outpatient settings
    - **Reproducibility**: Consistent results across different clinicians and institutions
    
    **Risk Category Definitions and Clinical Outcomes**:
    
    **Low Risk (0-3 points)**:
    - **Patient Population**: Approximately 30-40% of patients with suspected PE
    - **PE Incidence**: Less than 10% probability of pulmonary embolism
    - **Clinical Significance**: Very low likelihood justifying conservative diagnostic approach
    - **Validation**: Consistently low PE rates across multiple validation studies
    - **Cost-Effectiveness**: Avoids unnecessary imaging in low-probability patients
    
    **Intermediate Risk (4-10 points)**:
    - **Patient Population**: Approximately 40-50% of patients with suspected PE
    - **PE Incidence**: 20-30% probability of pulmonary embolism
    - **Clinical Significance**: Moderate probability requiring careful diagnostic evaluation
    - **Validation**: Intermediate PE rates consistent with clinical decision-making needs
    - **Risk-Benefit**: Balances diagnostic accuracy with resource utilization
    
    **High Risk (≥11 points)**:
    - **Patient Population**: Approximately 10-20% of patients with suspected PE
    - **PE Incidence**: Greater than 60% probability of pulmonary embolism
    - **Clinical Significance**: High likelihood warranting urgent diagnostic confirmation
    - **Validation**: Consistently high PE rates justifying direct imaging approach
    - **Clinical Urgency**: May warrant empirical anticoagulation pending imaging
    
    **DIAGNOSTIC MANAGEMENT BY RISK CATEGORY**:
    
    **Low Risk Management Approach**:
    
    **Primary Diagnostic Strategy**:
    - **D-dimer Testing**: First-line diagnostic test for risk stratification
    - **Negative D-dimer**: Pulmonary embolism effectively ruled out, no further testing needed
    - **Positive D-dimer**: Proceed to CT pulmonary angiography for definitive diagnosis
    - **Age Considerations**: Consider age-adjusted D-dimer cutoffs in elderly patients
    
    **Clinical Decision Points**:
    - **D-dimer Cutoff**: Standard cutoff 500 ng/mL or age-adjusted (age × 10 ng/mL for >50 years)
    - **Sensitivity**: High sensitivity of D-dimer maintains safety in low-risk patients
    - **Specificity**: Accept lower specificity to avoid missing PE in this population
    - **Cost-Effectiveness**: Significantly reduces unnecessary CT scans
    
    **Patient Management**:
    - **Reassurance**: Provide clear explanation of low PE probability
    - **Symptom Monitoring**: Advise return if symptoms worsen or new symptoms develop
    - **Follow-up**: Consider outpatient follow-up for persistent symptoms
    - **Alternative Diagnoses**: Evaluate for other causes of chest pain or dyspnea
    
    **Intermediate Risk Management Approach**:
    
    **Diagnostic Algorithm**:
    - **D-dimer Testing**: Recommended as initial diagnostic step
    - **Negative D-dimer**: PE unlikely, consider alternative diagnoses
    - **Positive D-dimer**: CT pulmonary angiography recommended
    - **Clinical Context**: Consider patient factors and presentation severity
    
    **Clinical Decision Making**:
    - **Risk-Benefit Analysis**: Balance diagnostic accuracy with radiation exposure
    - **Patient Factors**: Age, comorbidities, functional status influence decisions
    - **Symptom Severity**: More severe symptoms may favor direct imaging
    - **Resource Availability**: Consider local protocols and imaging availability
    
    **Monitoring Strategy**:
    - **Close Observation**: Monitor for clinical deterioration while awaiting results
    - **Symptom Assessment**: Regular evaluation of chest pain, dyspnea, vital signs
    - **Risk Reassessment**: Consider changes in clinical status that might alter risk
    - **Communication**: Clear communication with patient about diagnostic process
    
    **High Risk Management Approach**:
    
    **Urgent Diagnostic Strategy**:
    - **Direct Imaging**: CT pulmonary angiography without D-dimer testing
    - **Rationale**: High pretest probability (>60%) justifies direct definitive imaging
    - **Timing**: Urgent imaging within hours of presentation
    - **Alternative Imaging**: Consider V/Q scan if CT-PA contraindicated
    
    **Clinical Management**:
    - **Anticoagulation Consideration**: May initiate empirical anticoagulation if low bleeding risk
    - **Hemodynamic Assessment**: Evaluate for signs of right heart strain or hemodynamic compromise
    - **Multidisciplinary Approach**: Consider pulmonology or cardiology consultation
    - **Risk Stratification**: Assess for massive or submassive PE requiring advanced therapies
    
    **Monitoring and Support**:
    - **Continuous Monitoring**: Cardiac monitoring, frequent vital signs assessment
    - **Oxygen Support**: Supplemental oxygen if hypoxemic
    - **IV Access**: Establish reliable IV access for potential interventions
    - **Preparation**: Prepare for potential thrombolytic therapy or embolectomy
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Age-Related Factors**:
    - **Elderly Patients**: Higher baseline D-dimer levels may require age-adjusted cutoffs
    - **Comorbidities**: Multiple medical conditions may complicate assessment
    - **Functional Status**: Consider impact on quality of life and treatment goals
    - **Polypharmacy**: Evaluate for drug interactions with anticoagulation
    
    **Pregnancy Considerations**:
    - **Modified Assessment**: Geneva score not validated in pregnancy
    - **Alternative Approaches**: Use pregnancy-specific diagnostic algorithms
    - **Imaging Considerations**: Balance fetal radiation exposure with maternal risk
    - **D-dimer Limitations**: Physiologically elevated in pregnancy
    
    **Inpatient Limitations**:
    - **Validation Scope**: Score validated primarily in outpatient/ED settings
    - **Comorbidity Impact**: Hospitalized patients often have multiple confounding factors
    - **Alternative Tools**: Consider Wells' criteria or clinical judgment in inpatients
    - **Risk Modification**: Hospital-acquired risk factors may alter probability
    
    **Quality Improvement Applications**:
    
    **Clinical Protocol Development**:
    - **Standardization**: Implement standardized PE assessment protocols
    - **Education**: Train healthcare providers on proper score calculation and interpretation
    - **Decision Support**: Integrate into electronic health record systems
    - **Performance Metrics**: Monitor appropriate use of diagnostic testing
    
    **Resource Optimization**:
    - **Cost Reduction**: Decrease unnecessary CT scans through appropriate risk stratification
    - **Efficiency**: Streamline diagnostic pathways and reduce time to diagnosis
    - **Quality**: Maintain diagnostic accuracy while optimizing resource utilization
    - **Safety**: Ensure patient safety through appropriate risk assessment
    
    Reference: Le Gal G, et al. Ann Intern Med. 2006;144(3):165-171.
    """
    
    result: int = Field(
        ...,
        description="Geneva Score (Revised) calculated from clinical parameters (0-25 points)",
        ge=0,
        le=25,
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for Geneva PE score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment and evidence-based diagnostic recommendations",
        example="Geneva Score (Revised): 6 points. Present risk factors: unilateral limb pain (3 pts), heart rate 75-94 bpm (3 pts). Intermediate clinical probability of pulmonary embolism (20-30% incidence). Recommend D-dimer testing. If D-dimer is negative, pulmonary embolism is unlikely and further testing may not be necessary. If D-dimer is positive, CT pulmonary angiogram is recommended for definitive diagnosis. Consider clinical context and patient factors when interpreting results."
    )
    
    stage: str = Field(
        ...,
        description="PE risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of PE probability level",
        example="Intermediate clinical probability of PE"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Geneva Score (Revised): 6 points. Present risk factors: unilateral limb pain (3 pts), heart rate 75-94 bpm (3 pts). Intermediate clinical probability of pulmonary embolism (20-30% incidence). Recommend D-dimer testing. If D-dimer is negative, pulmonary embolism is unlikely and further testing may not be necessary. If D-dimer is positive, CT pulmonary angiogram is recommended for definitive diagnosis. Consider clinical context and patient factors when interpreting results.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate clinical probability of PE"
            }
        }