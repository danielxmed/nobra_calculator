"""
GARFIELD-AF Risk Score Models

Request and response models for GARFIELD-AF risk prediction in atrial fibrillation.

References (Vancouver style):
1. Fox KAA, Lucas JE, Pieper KS, et al. Improved risk stratification of patients with atrial 
   fibrillation: an integrated GARFIELD-AF tool for the prediction of mortality, stroke and bleed 
   in patients with and without anticoagulation. BMJ Open. 2017;7(12):e017157. 
   doi: 10.1136/bmjopen-2017-017157.
2. Apenteng PN, Murray ET, Holder R, et al. An international longitudinal registry of patients 
   with atrial fibrillation at risk of stroke: Global Anticoagulant Registry in the FIELD (GARFIELD). 
   Am Heart J. 2012;163(1):13-19.e1. doi: 10.1016/j.ahj.2011.09.011.
3. Camm AJ, Accetta G, Ambrosio G, et al. Evolving antithrombotic treatment patterns for patients 
   with newly diagnosed atrial fibrillation. Heart. 2017;103(4):307-314. doi: 10.1136/heartjnl-2016-309832.

The GARFIELD-AF risk score is a contemporary, validated tool that simultaneously predicts 1- and 
2-year risks of mortality, ischemic stroke/systemic embolism, and major bleeding in patients with 
atrial fibrillation. Unlike traditional single-outcome risk scores (CHA2DS2-VASc for stroke, 
HAS-BLED for bleeding), GARFIELD-AF provides integrated multi-outcome risk assessment to support 
individualized anticoagulation decisions.

This score was derived and validated from the Global Anticoagulant Registry in the FIELD (GARFIELD-AF), 
a prospective registry of over 52,000 patients with newly diagnosed atrial fibrillation from 35 countries. 
The tool incorporates 16 readily available clinical variables and has been validated in both 
anticoagulated and non-anticoagulated patients across diverse international populations.

Clinical Applications:
- Comprehensive risk stratification for patients with atrial fibrillation
- Integrated assessment of mortality, stroke/systemic embolism, and bleeding risks
- Support for individualized anticoagulation decision-making
- Risk-benefit analysis for anticoagulation therapy
- Patient counseling and shared decision-making
- Clinical trial stratification and endpoint prediction
- Quality improvement initiatives and population health management

Key Advantages over Single-Outcome Scores:
- Simultaneous prediction of multiple clinically relevant outcomes
- Contemporary derivation reflecting modern AF management
- Validation in diverse international populations
- Inclusion of both anticoagulated and non-anticoagulated patients
- Integration of multiple time horizons (1 and 2 years)
- Evidence-based risk-benefit framework for clinical decisions

The score uses 16 clinical variables:
- Demographics: Age, weight, race, sex
- Vital signs: Pulse rate, diastolic blood pressure
- Medical history: Bleeding history, heart failure, stroke/TIA, chronic kidney disease
- Comorbidities: Vascular disease, diabetes mellitus, dementia, carotid disease
- Medications/behaviors: Current smoking, antiplatelet use

Risk Stratification Categories:
- Low Risk: <2% maximum annual risk - Standard management approach
- Moderate Risk: 2-5% maximum annual risk - Individualized approach with careful monitoring  
- High Risk: >5% maximum annual risk - Intensive monitoring and specialist consultation

Clinical Decision Framework:
The GARFIELD-AF score enables clinicians to move beyond simple rule-based approaches 
(e.g., CHA2DS2-VASc ≥2 = anticoagulate) to individualized risk-benefit assessment. 
Patients with high stroke risk but also high bleeding risk require nuanced decision-making 
that considers patient preferences, functional status, and ability to maintain safe anticoagulation.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class GarfieldAfRequest(BaseModel):
    """
    Request model for GARFIELD-AF Risk Score calculation
    
    The GARFIELD-AF score simultaneously predicts 1- and 2-year risks of mortality, 
    ischemic stroke/systemic embolism, and major bleeding in patients with atrial fibrillation. 
    This contemporary, evidence-based tool supports individualized anticoagulation decisions 
    by providing integrated multi-outcome risk assessment.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Indication**: 
    - Patients with atrial fibrillation requiring anticoagulation risk stratification
    
    **Clinical Applications**:
    - **Anticoagulation Decision-Making**: Balance stroke prevention against bleeding risk
    - **Risk Communication**: Provide patients with personalized risk estimates
    - **Monitoring Strategy**: Determine frequency and intensity of follow-up
    - **Specialist Referral**: Identify patients requiring cardiology or hematology consultation
    - **Clinical Trial Enrollment**: Stratify patients for research participation
    - **Quality Improvement**: Population-level risk assessment and management optimization
    
    **PARAMETER INTERPRETATION GUIDE**:
    
    **1. Demographics and Anthropometrics**:
    
    **Age (years)**:
    - **Clinical Context**: Age is the strongest predictor of all three outcomes
    - **Risk Relationship**: Linear increase in risk with advancing age
    - **Considerations**: Older patients may have higher bleeding risk but also higher stroke risk
    - **Range**: 18-120 years (realistic clinical range)
    
    **Weight (kg)**:
    - **Clinical Context**: Lower weight associated with higher risk across all outcomes
    - **Mechanism**: May reflect frailty, malnutrition, or underlying comorbidities
    - **Considerations**: Consider BMI context and nutritional status
    - **Range**: 30-300 kg (covers underweight and obese patients)
    
    **Race/Ethnicity**:
    - **Asian**: Generally lower mortality and bleeding risk, variable stroke risk
    - **Black**: Higher stroke risk, variable bleeding and mortality risk  
    - **Other**: Reference category (includes White, Hispanic, and other ethnicities)
    - **Clinical Context**: Reflects genetic, environmental, and healthcare access factors
    - **Considerations**: Individual variation exists within racial categories
    
    **Sex**:
    - **Male**: Higher mortality risk, lower bleeding risk, variable stroke risk
    - **Female**: Lower mortality risk, higher bleeding risk, CHA2DS2-VASc adds points for female
    - **Clinical Context**: Hormonal and anatomical differences influence outcomes
    
    **2. Vital Signs and Physiological Parameters**:
    
    **Pulse Rate (bpm)**:
    - **Clinical Context**: Heart rate variability and rhythm control assessment
    - **Risk Relationship**: Higher heart rates associated with increased risk
    - **Considerations**: May reflect AF burden, rate control adequacy, or cardiovascular fitness
    - **Range**: 30-250 bpm (covers bradycardia to severe tachycardia)
    
    **Diastolic Blood Pressure (mmHg)**:
    - **Clinical Context**: Reflects cardiovascular health and medication effects
    - **Risk Relationship**: Lower diastolic BP associated with higher risk (J-curve)
    - **Considerations**: May indicate heart failure, medication effects, or arterial stiffness
    - **Range**: 40-150 mmHg (covers hypotension to severe hypertension)
    
    **3. Medical History and Comorbidities**:
    
    **History of Major Bleeding**:
    - **Definition**: Previous major bleeding requiring hospitalization, transfusion, or surgery
    - **Clinical Context**: Strongest predictor of future bleeding events
    - **Examples**: GI bleeding, ICH, major surgical bleeding, spontaneous bleeding
    - **Considerations**: Timing, cause, and reversibility of previous bleeding important
    
    **Heart Failure**:
    - **Definition**: Clinical diagnosis of heart failure or reduced ejection fraction
    - **Clinical Context**: Increases all three outcome risks significantly
    - **Staging**: Include both HFrEF and HFpEF
    - **Considerations**: Optimize heart failure management may reduce risks
    
    **History of Stroke/TIA**:
    - **Definition**: Previous ischemic stroke, hemorrhagic stroke, or transient ischemic attack
    - **Clinical Context**: Strongest predictor of future stroke/systemic embolism
    - **Considerations**: Time since stroke, cause, and residual deficits relevant
    - **Management**: May influence anticoagulation decisions and monitoring
    
    **Chronic Kidney Disease**:
    - **Definition**: eGFR <60 mL/min/1.73m² or clinical diagnosis of CKD
    - **Clinical Context**: Increases all outcome risks, affects drug clearance
    - **Considerations**: Monitor renal function, adjust anticoagulant dosing
    - **Staging**: Include all CKD stages ≥3
    
    **Vascular Disease**:
    - **Definition**: Coronary artery disease, peripheral arterial disease, or aortic plaque
    - **Examples**: Previous MI, PCI, CABG, PAD, carotid disease, aortic atherosclerosis
    - **Clinical Context**: Reflects systemic atherosclerosis and thrombotic risk
    - **Considerations**: May require dual antiplatelet therapy consideration
    
    **Diabetes Mellitus**:
    - **Definition**: Diabetes requiring medication (oral or insulin)
    - **Clinical Context**: Increases stroke and bleeding risk through multiple mechanisms
    - **Considerations**: Optimize glycemic control, monitor for complications
    - **Exclusions**: Diet-controlled diabetes not typically included
    
    **Current Smoking**:
    - **Definition**: Active tobacco use within past 30 days
    - **Clinical Context**: Increases all outcome risks, especially cardiovascular
    - **Considerations**: Smoking cessation counseling essential
    - **Mechanism**: Prothrombotic effects, endothelial dysfunction, drug interactions
    
    **Dementia**:
    - **Definition**: Clinical diagnosis of dementia or significant cognitive impairment
    - **Clinical Context**: Increases all risks, affects medication compliance
    - **Considerations**: Involve caregivers, consider bleeding risk vs. benefit carefully
    - **Management**: May require alternative anticoagulation strategies
    
    **Antiplatelet Use**:
    - **Definition**: Current use of aspirin, clopidogrel, or other antiplatelet agents
    - **Clinical Context**: Increases bleeding risk, may interact with anticoagulants
    - **Considerations**: Evaluate necessity, consider dual vs. triple therapy risks
    - **Examples**: Low-dose aspirin, P2Y12 inhibitors, combination antiplatelet therapy
    
    **Carotid Disease**:
    - **Definition**: Carotid artery stenosis or previous carotid intervention
    - **Clinical Context**: Marker of cerebrovascular disease and stroke risk
    - **Considerations**: May influence stroke subtype risk and management
    - **Staging**: Include both symptomatic and asymptomatic carotid disease
    
    **CLINICAL DECISION SUPPORT FRAMEWORK**:
    
    **Risk-Benefit Integration**:
    - **Low Overall Risk**: Standard anticoagulation approach if stroke risk warrants
    - **Moderate Risk**: Individualize based on patient preferences and clinical context
    - **High Risk**: Intensive monitoring, consider specialist consultation
    
    **Anticoagulation Considerations by Risk Profile**:
    
    **Low Risk (<2% max annual risk)**:
    - **Approach**: Standard management following guidelines
    - **Monitoring**: Routine follow-up per standard protocols
    - **Patient Education**: Standard counseling on adherence and bleeding precautions
    
    **Moderate Risk (2-5% max annual risk)**:
    - **Approach**: Individualized risk-benefit discussion
    - **Monitoring**: Consider more frequent follow-up (every 3-6 months)
    - **Patient Education**: Enhanced counseling on signs/symptoms to monitor
    - **Considerations**: Patient preferences weigh heavily in decisions
    
    **High Risk (>5% max annual risk)**:
    - **Approach**: Intensive management with specialist input
    - **Monitoring**: Frequent follow-up (every 1-3 months)
    - **Patient Education**: Extensive counseling, involve family/caregivers
    - **Considerations**: May require alternative strategies (e.g., left atrial appendage occlusion)
    
    **Time Horizon Considerations**:
    - **1-Year Risks**: More relevant for acute decision-making and patient counseling
    - **2-Year Risks**: Better for longer-term planning and treatment strategy
    - **Dynamic Assessment**: Risks change over time with aging and comorbidity evolution
    
    **Quality of Life Integration**:
    - Consider functional status, life expectancy, and patient goals
    - Balance aggressive treatment with quality of life preservation
    - Incorporate advance directives and care preferences
    - Reassess periodically as clinical status changes
    
    References (Vancouver style):
    1. Fox KAA, Lucas JE, Pieper KS, et al. Improved risk stratification of patients with atrial 
       fibrillation: an integrated GARFIELD-AF tool for the prediction of mortality, stroke and bleed 
       in patients with and without anticoagulation. BMJ Open. 2017;7(12):e017157.
    2. Apenteng PN, Murray ET, Holder R, et al. An international longitudinal registry of patients 
       with atrial fibrillation at risk of stroke: Global Anticoagulant Registry in the FIELD (GARFIELD). 
       Am Heart J. 2012;163(1):13-19.e1.
    3. Camm AJ, Accetta G, Ambrosio G, et al. Evolving antithrombotic treatment patterns for patients 
       with newly diagnosed atrial fibrillation. Heart. 2017;103(4):307-314.
    """
    
    age: int = Field(
        ...,
        description="Patient's age in years. Strongest predictor of all outcomes with linear risk increase",
        ge=18,
        le=120,
        example=72
    )
    
    weight: float = Field(
        ...,
        description="Patient's body weight in kg. Lower weight associated with higher risk across all outcomes",
        ge=30,
        le=300,
        example=80.5
    )
    
    race: Literal["asian", "black", "other"] = Field(
        ...,
        description="Patient's race/ethnicity. Asian: lower mortality/bleeding risk; Black: higher stroke risk; Other: reference category",
        example="other"
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Male: higher mortality, lower bleeding risk; Female: lower mortality, higher bleeding risk",
        example="male"
    )
    
    pulse: int = Field(
        ...,
        description="Heart rate in beats per minute. Higher rates associated with increased risk across outcomes",
        ge=30,
        le=250,
        example=78
    )
    
    diastolic_bp: int = Field(
        ...,
        description="Diastolic blood pressure in mmHg. Lower values associated with higher risk (J-curve relationship)",
        ge=40,
        le=150,
        example=85
    )
    
    history_of_bleeding: Literal["yes", "no"] = Field(
        ...,
        description="History of major bleeding requiring hospitalization, transfusion, or surgery. Strongest predictor of future bleeding",
        example="no"
    )
    
    heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="Clinical diagnosis of heart failure or reduced ejection fraction. Significantly increases all outcome risks",
        example="yes"
    )
    
    history_of_stroke: Literal["yes", "no"] = Field(
        ...,
        description="Previous ischemic stroke, hemorrhagic stroke, or TIA. Strongest predictor of future stroke/systemic embolism",
        example="no"
    )
    
    chronic_kidney_disease: Literal["yes", "no"] = Field(
        ...,
        description="eGFR <60 mL/min/1.73m² or clinical CKD diagnosis. Increases all risks and affects drug clearance",
        example="yes"
    )
    
    vascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Coronary artery disease, peripheral arterial disease, or aortic plaque. Reflects systemic atherosclerosis",
        example="yes"  
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="Diabetes requiring medication (oral or insulin). Increases stroke and bleeding risk",
        example="yes"
    )
    
    current_smoking: Literal["yes", "no"] = Field(
        ...,
        description="Active tobacco use within past 30 days. Increases all outcome risks through multiple mechanisms",
        example="no"
    )
    
    dementia: Literal["yes", "no"] = Field(
        ...,
        description="Clinical diagnosis of dementia or significant cognitive impairment. Increases all risks, affects compliance",
        example="no"
    )
    
    antiplatelet_use: Literal["yes", "no"] = Field(
        ...,
        description="Current use of aspirin, clopidogrel, or other antiplatelet agents. Increases bleeding risk",
        example="yes"
    )
    
    carotid_disease: Literal["yes", "no"] = Field(
        ...,
        description="Carotid artery stenosis or previous carotid intervention. Marker of cerebrovascular disease",
        example="no"  
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "weight": 80.5,
                "race": "other",
                "sex": "male", 
                "pulse": 78,
                "diastolic_bp": 85,
                "history_of_bleeding": "no",
                "heart_failure": "yes",
                "history_of_stroke": "no",
                "chronic_kidney_disease": "yes",
                "vascular_disease": "yes",
                "diabetes_mellitus": "yes",
                "current_smoking": "no",
                "dementia": "no",
                "antiplatelet_use": "yes",
                "carotid_disease": "no"
            }
        }


class GarfieldAfResponse(BaseModel):
    """
    Response model for GARFIELD-AF Risk Score calculation
    
    The response provides simultaneous risk predictions for three clinically relevant outcomes 
    (mortality, stroke/systemic embolism, major bleeding) at two time horizons (1 and 2 years), 
    along with integrated clinical interpretation and management recommendations.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **Multi-Outcome Risk Assessment**:
    The GARFIELD-AF score uniquely provides integrated assessment of competing risks:
    - **Mortality Risk**: Overall survival prediction accounting for AF and comorbidities
    - **Stroke/Systemic Embolism Risk**: Thromboembolic events that anticoagulation prevents
    - **Major Bleeding Risk**: Serious bleeding events that anticoagulation may cause
    
    **Time Horizon Integration**:
    - **1-Year Risks**: More precise for immediate clinical decisions and patient counseling
    - **2-Year Risks**: Better for strategic planning and treatment monitoring
    - **Risk Trajectory**: Consider how risks evolve over time with aging and disease progression
    
    **RISK STRATIFICATION AND MANAGEMENT**:
    
    **Low Risk Category (<2% maximum annual risk)**:
    
    **Clinical Characteristics**:
    - Younger patients with fewer comorbidities
    - Lower burden of cardiovascular risk factors
    - Generally good functional status and life expectancy
    
    **Management Approach**:
    - **Anticoagulation**: Standard approach following guideline recommendations
    - **Monitoring**: Routine follow-up per standard protocols (every 6-12 months)
    - **Patient Education**: Standard counseling on adherence and bleeding precautions
    - **Risk Factor Management**: Address modifiable cardiovascular risk factors
    - **Lifestyle**: Emphasize healthy lifestyle, exercise, smoking cessation if applicable
    
    **Clinical Considerations**:
    - May safely use standard anticoagulation approaches
    - Lower threshold for anticoagulation when stroke risk is present
    - Focus on optimizing adherence and lifestyle factors
    
    **Moderate Risk Category (2-5% maximum annual risk)**:
    
    **Clinical Characteristics**:
    - Mixed risk profile with moderate comorbidity burden
    - Balance between stroke prevention benefit and bleeding risk
    - Requires individualized assessment of patient preferences
    
    **Management Approach**:
    - **Anticoagulation**: Individualized risk-benefit discussion essential
    - **Monitoring**: More frequent follow-up (every 3-6 months)
    - **Patient Education**: Enhanced counseling on signs/symptoms to monitor
    - **Shared Decision-Making**: Extensive discussion of risks, benefits, and alternatives
    - **Risk Optimization**: Aggressive management of modifiable risk factors
    
    **Clinical Considerations**:
    - Consider patient preferences heavily in anticoagulation decisions
    - May benefit from alternative anticoagulation strategies
    - Consider non-pharmacological approaches (e.g., lifestyle, rhythm control)
    - Regular reassessment as clinical status changes
    
    **High Risk Category (>5% maximum annual risk)**:
    
    **Clinical Characteristics**:
    - Multiple significant comorbidities
    - Complex competing risks requiring specialist input
    - May have limited life expectancy or functional status
    
    **Management Approach**:
    - **Anticoagulation**: Intensive management with specialist consultation
    - **Monitoring**: Frequent follow-up (every 1-3 months)  
    - **Patient Education**: Extensive counseling involving family/caregivers
    - **Multidisciplinary Care**: Cardiology, hematology, geriatrics as appropriate
    - **Alternative Strategies**: Consider LAAO, rhythm control, or palliative approaches
    
    **Clinical Considerations**:
    - May require alternative anticoagulation strategies
    - Consider left atrial appendage occlusion if bleeding risk prohibitive
    - Palliative care consultation may be appropriate
    - Advanced care planning and goals-of-care discussions essential
    
    **SPECIFIC OUTCOME INTERPRETATION**:
    
    **Mortality Risk Interpretation**:
    - **Low (<2%)**: Good prognosis, focus on stroke prevention and quality of life
    - **Moderate (2-8%)**: Intermediate prognosis, balance aggressive treatment with risks
    - **High (>8%)**: Limited prognosis, focus on comfort and symptom management
    
    **Stroke/Systemic Embolism Risk Interpretation**:
    - **Low (<1%)**: Minimal stroke risk, anticoagulation benefit may be limited
    - **Moderate (1-4%)**: Clear benefit from anticoagulation if bleeding risk acceptable
    - **High (>4%)**: Strong indication for anticoagulation unless major contraindications
    
    **Major Bleeding Risk Interpretation**:
    - **Low (<1%)**: Minimal bleeding concern, standard anticoagulation approach
    - **Moderate (1-3%)**: Careful monitoring, consider bleeding risk reduction strategies
    - **High (>3%)**: Major bleeding concern, consider alternatives or intensive monitoring
    
    **INTEGRATED CLINICAL DECISION-MAKING**:
    
    **Risk-Benefit Integration Strategies**:
    
    **Scenario 1: High Stroke, Low Bleeding Risk**:
    - **Decision**: Strong anticoagulation indication
    - **Approach**: Standard anticoagulation with routine monitoring
    - **Focus**: Optimize adherence and stroke prevention
    
    **Scenario 2: High Stroke, High Bleeding Risk**:
    - **Decision**: Complex risk-benefit analysis required
    - **Approach**: Consider specialist consultation, alternative strategies
    - **Options**: Reduced-dose anticoagulation, LAAO, intensive monitoring
    
    **Scenario 3: Low Stroke, High Bleeding Risk**:
    - **Decision**: Anticoagulation may not be beneficial
    - **Approach**: Focus on rhythm control, lifestyle modification
    - **Monitoring**: Regular reassessment as stroke risk may increase
    
    **MONITORING AND REASSESSMENT**:
    
    **Dynamic Risk Assessment**:
    - **Annual Reassessment**: Minimum frequency for stable patients
    - **Event-Triggered**: Reassess after major clinical events
    - **Age-Related**: Consider more frequent assessment in elderly patients
    - **Comorbidity Changes**: Reassess when new conditions develop
    
    **Monitoring Parameters**:
    - **Clinical Status**: Functional capacity, cognitive status, frailty
    - **Laboratory Values**: Renal function, hemoglobin, liver function
    - **Medication Effects**: Efficacy, side effects, interactions
    - **Patient Preferences**: Goals of care, quality of life priorities
    
    **Quality Improvement Applications**:
    - **Population Health**: Risk stratification for AF management programs
    - **Clinical Pathways**: Standardized approaches based on risk categories
    - **Performance Metrics**: Outcomes tracking and quality improvement
    - **Patient Safety**: Bleeding event prevention and monitoring protocols
    
    Reference: Fox KAA, et al. BMJ Open. 2017;7(12):e017157.
    """
    
    result: Dict[str, float] = Field(
        ...,
        description="Comprehensive risk predictions for all three outcomes at 1 and 2 years",
        example={
            "mortality_1_year": 4.2,
            "mortality_2_year": 8.1,
            "stroke_se_1_year": 2.8,
            "stroke_se_2_year": 5.4,
            "major_bleeding_1_year": 1.9,
            "major_bleeding_2_year": 3.7
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for all risk predictions",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with integrated risk-benefit analysis and management recommendations",
        example="Moderate risk profile with 1-year risks of 4.2% mortality, 2.8% stroke/systemic embolism, and 1.9% major bleeding. 2-year risks: 8.1% mortality, 5.4% stroke/SE, 3.7% bleeding. Consider individualized approach to anticoagulation with careful benefit-risk assessment. Regular follow-up every 3-6 months recommended to monitor clinical status and treatment response."
    )
    
    stage: str = Field(
        ...,
        description="Overall risk category based on maximum risk across all outcomes",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level and clinical approach",
        example="Moderate risk requiring careful monitoring"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "mortality_1_year": 4.2,
                    "mortality_2_year": 8.1,
                    "stroke_se_1_year": 2.8,
                    "stroke_se_2_year": 5.4,
                    "major_bleeding_1_year": 1.9,
                    "major_bleeding_2_year": 3.7
                },
                "unit": "percentage",
                "interpretation": "Moderate risk profile with 1-year risks of 4.2% mortality, 2.8% stroke/systemic embolism, and 1.9% major bleeding. 2-year risks: 8.1% mortality, 5.4% stroke/SE, 3.7% bleeding. Consider individualized approach to anticoagulation with careful benefit-risk assessment. Regular follow-up every 3-6 months recommended to monitor clinical status and treatment response.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk requiring careful monitoring"
            }
        }