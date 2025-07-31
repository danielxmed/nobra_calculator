"""
Geneva Risk Score for Venous Thromboembolism (VTE) Prophylaxis Models

Request and response models for Geneva VTE Risk Score calculation.

References (Vancouver style):
1. Chopard P, Spirk D, Bounameaux H. Identifying acutely ill medical patients requiring 
   thromboprophylaxis. J Thromb Haemost. 2006;4(4):915-916. doi: 10.1111/j.1538-7836.2006.01818.x.
2. Nendaz M, Spirk D, Kucher N, et al. Multicentre validation of the Geneva Risk Score for 
   hospitalised medical patients at risk of venous thromboembolism. Explicit ASsessment of 
   Thromboembolic RIsk and Prophylaxis for Medical PATients in SwitzErland (ESTIMATE). 
   Thromb Haemost. 2014;111(3):531-538. doi: 10.1160/TH13-05-0427.
3. Decousus H, Tapson VF, Bergmann JF, et al. Factors at admission associated with bleeding 
   risk in medical patients: findings from the IMPROVE investigators. Chest. 2011;139(1):69-79. 
   doi: 10.1378/chest.09-3081.

The Geneva Risk Score for VTE Prophylaxis is a validated clinical decision tool for 
predicting the need for venous thromboembolism prophylaxis in hospitalized medical patients. 
Developed and validated through multiple studies including the ESTIMATE trial, this score 
helps clinicians identify patients at high risk for VTE who would benefit from 
thromboprophylaxis and those at low risk who may not require anticoagulation.

Key Clinical Applications:
- VTE risk stratification in hospitalized medical patients
- Thromboprophylaxis decision-making and optimization
- Reduction of unnecessary anticoagulation in low-risk patients
- Standardization of VTE prevention protocols in hospitals
- Quality improvement initiatives for VTE prevention

The score incorporates 19 risk factors with differential weighting: major risk factors 
(2 points each) include conditions like cardiac failure, respiratory failure, active 
malignancy, and prior VTE history, while minor risk factors (1 point each) include 
age >60 years, obesity, immobilization, and hormonal therapy. A threshold of ≥3 points 
identifies patients at high risk (3.2% VTE rate) who should receive prophylaxis, while 
patients with <3 points are at low risk (0.6% VTE rate) and may not require pharmacological 
prophylaxis.

The Geneva Risk Score demonstrated superior negative predictive value compared to the 
Padua Prediction Score in the ESTIMATE validation study, particularly for identifying 
low-risk patients who safely avoid unnecessary anticoagulation. This tool supports 
evidence-based decision-making in VTE prevention while balancing efficacy and safety 
considerations in diverse hospitalized medical populations.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GenevaVteProphylaxisRequest(BaseModel):
    """
    Request model for Geneva Risk Score for Venous Thromboembolism (VTE) Prophylaxis
    
    The Geneva Risk Score for VTE Prophylaxis assesses hospitalized medical patients' risk 
    for venous thromboembolism to guide thromboprophylaxis decisions. This validated tool 
    incorporates 19 clinical risk factors with differential point values to identify patients 
    who would benefit from anticoagulation versus those who can safely avoid it.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Clinical Application**:
    - **Target Population**: Hospitalized medical patients requiring VTE risk assessment
    - **Decision Point**: Admission or during hospitalization when considering thromboprophylaxis
    - **Clinical Utility**: Standardized, evidence-based approach to VTE prevention decisions
    
    **Risk Assessment Framework**:
    - **Validated Threshold**: Score ≥3 points indicates high VTE risk requiring prophylaxis
    - **Evidence Base**: Derived from multicenter validation studies including ESTIMATE trial
    - **Performance Metrics**: Superior negative predictive value for identifying low-risk patients
    
    **RISK FACTOR CATEGORIES AND CLINICAL SIGNIFICANCE**:
    
    **MAJOR RISK FACTORS (2 points each)**:
    
    These conditions represent significant prothrombotic states with substantial impact on VTE risk:
    
    **Cardiac Failure**:
    - **Clinical Definition**: Acute or chronic heart failure with reduced cardiac output
    - **Pathophysiology**: Venous stasis, reduced mobility, increased coagulation factors
    - **Risk Impact**: Approximately doubles baseline VTE risk
    - **Assessment**: Based on clinical symptoms, imaging, or laboratory markers (BNP/NT-proBNP)
    
    **Respiratory Failure**:
    - **Clinical Definition**: Acute respiratory failure requiring mechanical ventilation or high-flow oxygen
    - **Pathophysiology**: Hypoxemia-induced hypercoagulability, immobilization, inflammation
    - **Risk Impact**: Significant increase in VTE risk through multiple mechanisms
    - **Assessment**: Based on oxygen requirements, blood gas analysis, clinical status
    
    **Recent Stroke (<3 months)**:
    - **Clinical Definition**: Ischemic or hemorrhagic stroke within the past 3 months
    - **Pathophysiology**: Immobilization, hemostatic activation, endothelial dysfunction
    - **Risk Impact**: Particularly high for patients with hemiplegia or significant mobility impairment
    - **Assessment**: Based on medical history, neurological examination, imaging findings
    
    **Recent Myocardial Infarction (<4 weeks)**:
    - **Clinical Definition**: ST-elevation or non-ST-elevation myocardial infarction within 4 weeks
    - **Pathophysiology**: Hypercoagulable state, reduced mobility, inflammatory response
    - **Risk Impact**: Acute phase associated with highest thrombotic risk
    - **Assessment**: Based on clinical presentation, ECG changes, cardiac biomarkers
    
    **Acute Infectious Disease (including Sepsis)**:
    - **Clinical Definition**: Acute bacterial, viral, or fungal infection with systemic involvement
    - **Pathophysiology**: Inflammatory cytokines, endothelial activation, disseminated intravascular coagulation
    - **Risk Impact**: Sepsis particularly high-risk due to systemic inflammatory response
    - **Assessment**: Based on clinical criteria, laboratory markers (WBC, CRP, procalcitonin), cultures
    
    **Acute Rheumatic Disease**:
    - **Clinical Definition**: Active inflammatory rheumatic conditions (lupus flare, rheumatoid arthritis exacerbation)
    - **Pathophysiology**: Autoimmune inflammation, antiphospholipid antibodies, steroid effects
    - **Risk Impact**: Variable based on disease activity and treatment
    - **Assessment**: Based on clinical symptoms, laboratory markers (ESR, CRP), disease-specific criteria
    
    **Active Malignancy**:
    - **Clinical Definition**: Current cancer diagnosis with active treatment or metastatic disease
    - **Pathophysiology**: Tumor-induced hypercoagulability, chemotherapy effects, immobilization
    - **Risk Impact**: Among highest risk factors, varies by cancer type and stage
    - **Assessment**: Based on histology, staging, current treatment status
    
    **Myeloproliferative Syndrome**:
    - **Clinical Definition**: Disorders like polycythemia vera, essential thrombocythemia, myelofibrosis
    - **Pathophysiology**: Abnormal platelet function, hyperviscosity, JAK2 mutations
    - **Risk Impact**: Particularly high thrombotic risk due to hematologic abnormalities
    - **Assessment**: Based on blood counts, bone marrow biopsy, molecular testing
    
    **Nephrotic Syndrome**:
    - **Clinical Definition**: Proteinuria >3.5g/day with hypoalbuminemia and edema
    - **Pathophysiology**: Loss of anticoagulant proteins, increased synthesis of prothrombotic factors
    - **Risk Impact**: Proportional to degree of proteinuria and hypoalbuminemia
    - **Assessment**: Based on urinalysis, 24-hour urine protein, serum albumin
    
    **Prior VTE History**:
    - **Clinical Definition**: Previous deep vein thrombosis or pulmonary embolism
    - **Pathophysiology**: Residual vascular damage, genetic predisposition, recurrence risk
    - **Risk Impact**: Strong predictor of recurrent VTE events
    - **Assessment**: Based on documented imaging, anticoagulation history, clinical records
    
    **Known Hypercoagulable State**:
    - **Clinical Definition**: Identified thrombophilia (Factor V Leiden, prothrombin mutation, protein deficiencies)
    - **Pathophysiology**: Genetic or acquired defects in coagulation or fibrinolysis
    - **Risk Impact**: Variable based on specific thrombophilia and clinical context
    - **Assessment**: Based on specialized coagulation testing, family history
    
    **MINOR RISK FACTORS (1 point each)**:
    
    These factors represent moderate increases in VTE risk:
    
    **Immobilization (≥3 days, <30 min walking/day)**:
    - **Clinical Definition**: Bed rest or severely limited mobility for 3 or more consecutive days
    - **Pathophysiology**: Venous stasis, muscle pump dysfunction, endothelial changes
    - **Risk Impact**: Risk increases with duration and degree of immobilization
    - **Assessment**: Based on nursing documentation, physical therapy notes, clinical observation
    
    **Recent Travel (>6 hours)**:
    - **Clinical Definition**: Air, train, or automobile travel >6 hours within past 4 weeks
    - **Pathophysiology**: Prolonged sitting, dehydration, cabin pressure effects
    - **Risk Impact**: Modest increase, higher with additional risk factors
    - **Assessment**: Based on patient history, travel itinerary
    
    **Age >60 Years**:
    - **Clinical Definition**: Chronological age greater than 60 years
    - **Pathophysiology**: Age-related changes in coagulation, reduced mobility, comorbidities
    - **Risk Impact**: Linear increase in VTE risk with advancing age
    - **Assessment**: Based on date of birth, medical record documentation
    
    **Obesity (BMI >30 kg/m²)**:
    - **Clinical Definition**: Body mass index greater than 30 kg/m²
    - **Pathophysiology**: Increased coagulation factors, reduced fibrinolysis, mechanical effects
    - **Risk Impact**: Proportional to degree of obesity, higher with central distribution
    - **Assessment**: Based on measured height and weight, BMI calculation
    
    **Chronic Venous Insufficiency**:
    - **Clinical Definition**: Chronic venous disease with valve dysfunction or obstruction
    - **Pathophysiology**: Venous stasis, endothelial dysfunction, previous thrombotic damage
    - **Risk Impact**: Particularly high for patients with history of post-thrombotic syndrome
    - **Assessment**: Based on clinical examination, duplex ultrasound, venous function studies
    
    **Pregnancy**:
    - **Clinical Definition**: Current pregnancy at any gestational age
    - **Pathophysiology**: Hormonal changes, mechanical compression, hypercoagulable state
    - **Risk Impact**: Increases throughout pregnancy, highest in postpartum period
    - **Assessment**: Based on pregnancy test, clinical examination, obstetric history
    
    **Hormonal Therapy**:
    - **Clinical Definition**: Estrogen-containing contraceptives or hormone replacement therapy
    - **Pathophysiology**: Estrogen-induced changes in coagulation factors and fibrinolysis
    - **Risk Impact**: Dose-dependent, higher with combined preparations
    - **Assessment**: Based on medication history, prescription records
    
    **Dehydration**:
    - **Clinical Definition**: Clinical evidence of volume depletion or inadequate fluid intake
    - **Pathophysiology**: Increased blood viscosity, reduced cardiac output, venous stasis
    - **Risk Impact**: Variable based on severity and duration
    - **Assessment**: Based on clinical examination, laboratory values, fluid balance
    
    **CLINICAL DECISION FRAMEWORK**:
    
    **Risk Stratification**:
    - **Low Risk (<3 points)**: 0.6% VTE rate, prophylaxis generally not recommended
    - **High Risk (≥3 points)**: 3.2% VTE rate, prophylaxis recommended unless contraindicated
    
    **Prophylaxis Recommendations**:
    
    **Low Risk Management**:
    - **Primary Approach**: Mechanical prophylaxis (sequential compression devices, early mobilization)
    - **Monitoring**: Daily reassessment for changes in risk profile
    - **Patient Education**: VTE awareness, early ambulation, hydration
    
    **High Risk Management**:
    - **Pharmacological Options**: Low molecular weight heparin, unfractionated heparin, fondaparinux
    - **Dosing Considerations**: Adjust for renal function, weight, bleeding risk
    - **Contraindications**: Active bleeding, severe thrombocytopenia, recent surgery with bleeding risk
    - **Alternative Measures**: Mechanical prophylaxis if anticoagulation contraindicated
    
    **Special Considerations**:
    - **Bleeding Risk Assessment**: Consider tools like IMPROVE bleeding score
    - **Duration**: Continue throughout hospitalization, consider extended prophylaxis for high-risk patients
    - **Monitoring**: Regular assessment of clinical status, laboratory parameters
    - **Patient Factors**: Age, comorbidities, functional status, patient preferences
    
    References (Vancouver style):
    1. Chopard P, Spirk D, Bounameaux H. Identifying acutely ill medical patients requiring 
       thromboprophylaxis. J Thromb Haemost. 2006;4(4):915-916.
    2. Nendaz M, Spirk D, Kucher N, et al. Multicentre validation of the Geneva Risk Score for 
       hospitalised medical patients at risk of venous thromboembolism. Thromb Haemost. 2014;111(3):531-538.
    3. Decousus H, Tapson VF, Bergmann JF, et al. Factors at admission associated with bleeding 
       risk in medical patients: findings from the IMPROVE investigators. Chest. 2011;139(1):69-79.
    """
    
    # Major risk factors (2 points each)
    cardiac_failure: Literal["yes", "no"] = Field(
        ...,
        description="Cardiac failure (acute or chronic heart failure). Major risk factor worth 2 points",
        example="no"
    )
    
    respiratory_failure: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory failure requiring mechanical ventilation or high-flow oxygen. Major risk factor worth 2 points",
        example="no"
    )
    
    recent_stroke: Literal["yes", "no"] = Field(
        ...,
        description="Recent stroke (ischemic or hemorrhagic) within the past 3 months. Major risk factor worth 2 points",
        example="no"
    )
    
    recent_myocardial_infarction: Literal["yes", "no"] = Field(
        ...,
        description="Recent myocardial infarction (STEMI or NSTEMI) within the past 4 weeks. Major risk factor worth 2 points",
        example="no"
    )
    
    acute_infectious_disease: Literal["yes", "no"] = Field(
        ...,
        description="Acute infectious disease including sepsis with systemic involvement. Major risk factor worth 2 points",
        example="no"
    )
    
    acute_rheumatic_disease: Literal["yes", "no"] = Field(
        ...,
        description="Acute rheumatic disease (active inflammatory conditions like lupus flare, RA exacerbation). Major risk factor worth 2 points",
        example="no"
    )
    
    active_malignancy: Literal["yes", "no"] = Field(
        ...,
        description="Active malignancy (current cancer diagnosis with active treatment or metastatic disease). Major risk factor worth 2 points",
        example="no"
    )
    
    myeloproliferative_syndrome: Literal["yes", "no"] = Field(
        ...,
        description="Myeloproliferative syndrome (polycythemia vera, essential thrombocythemia, myelofibrosis). Major risk factor worth 2 points",
        example="no"
    )
    
    nephrotic_syndrome: Literal["yes", "no"] = Field(
        ...,
        description="Nephrotic syndrome (proteinuria >3.5g/day with hypoalbuminemia and edema). Major risk factor worth 2 points",
        example="no"
    )
    
    prior_vte_history: Literal["yes", "no"] = Field(
        ...,
        description="Prior history of venous thromboembolism (previous DVT or PE documented by imaging). Major risk factor worth 2 points",
        example="no"
    )
    
    known_hypercoagulable_state: Literal["yes", "no"] = Field(
        ...,
        description="Known hypercoagulable state (identified thrombophilia like Factor V Leiden, protein deficiencies). Major risk factor worth 2 points",
        example="no"
    )
    
    # Minor risk factors (1 point each)
    immobilization: Literal["yes", "no"] = Field(
        ...,
        description="Immobilization for 3 or more consecutive days with less than 30 minutes of walking per day. Minor risk factor worth 1 point",
        example="no"
    )
    
    recent_travel: Literal["yes", "no"] = Field(
        ...,
        description="Recent travel longer than 6 hours (air, train, or automobile) within past 4 weeks. Minor risk factor worth 1 point",
        example="no"
    )
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Age greater than 60 years. Minor risk factor worth 1 point",
        example="yes"
    )
    
    obesity: Literal["yes", "no"] = Field(
        ...,
        description="Obesity with body mass index (BMI) greater than 30 kg/m². Minor risk factor worth 1 point",
        example="no"
    )
    
    chronic_venous_insufficiency: Literal["yes", "no"] = Field(
        ...,
        description="Chronic venous insufficiency (chronic venous disease with valve dysfunction). Minor risk factor worth 1 point",
        example="no"
    )
    
    pregnancy: Literal["yes", "no"] = Field(
        ...,
        description="Current pregnancy at any gestational age. Minor risk factor worth 1 point",
        example="no"
    )
    
    hormonal_therapy: Literal["yes", "no"] = Field(
        ...,
        description="Hormonal therapy (estrogen-containing contraceptives or hormone replacement therapy). Minor risk factor worth 1 point",
        example="no"
    )
    
    dehydration: Literal["yes", "no"] = Field(
        ...,
        description="Clinical evidence of dehydration or volume depletion. Minor risk factor worth 1 point",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cardiac_failure": "no",
                "respiratory_failure": "no",
                "recent_stroke": "no",
                "recent_myocardial_infarction": "no",
                "acute_infectious_disease": "yes",
                "acute_rheumatic_disease": "no",
                "active_malignancy": "no",
                "myeloproliferative_syndrome": "no",
                "nephrotic_syndrome": "no",
                "prior_vte_history": "no",
                "known_hypercoagulable_state": "no",
                "immobilization": "yes",
                "recent_travel": "no",
                "age_over_60": "yes",
                "obesity": "no",
                "chronic_venous_insufficiency": "no",
                "pregnancy": "no",
                "hormonal_therapy": "no",
                "dehydration": "yes"
            }
        }


class GenevaVteProphylaxisResponse(BaseModel):
    """
    Response model for Geneva Risk Score for Venous Thromboembolism (VTE) Prophylaxis
    
    The response provides the calculated Geneva VTE Risk Score with detailed risk factor 
    analysis and evidence-based thromboprophylaxis recommendations based on validated 
    clinical data from the ESTIMATE trial and other validation studies.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **Geneva VTE Risk Score Components**:
    - **Total Score Range**: 0-33 points with binary risk stratification
    - **Validated Threshold**: ≥3 points indicates high VTE risk requiring prophylaxis
    - **Evidence Base**: Derived from multicenter validation studies with 1,478 patients
    - **Performance Metrics**: Superior negative predictive value for low-risk identification
    
    **Risk Category Definitions and Clinical Outcomes**:
    
    **Low Risk (<3 points)**:
    - **Patient Population**: Approximately 35% of hospitalized medical patients
    - **VTE Incidence**: 0.6% (95% CI: 0.2-1.9%) three-month VTE rate
    - **Clinical Significance**: Very low likelihood of VTE events without prophylaxis
    - **Negative Predictive Value**: 99.4% accuracy for ruling out VTE risk
    - **Management Implications**: Pharmacological prophylaxis generally not recommended
    
    **High Risk (≥3 points)**:
    - **Patient Population**: Approximately 65% of hospitalized medical patients
    - **VTE Incidence**: 3.2% (95% CI: 2.2-4.6%) three-month VTE rate
    - **Clinical Significance**: Significant VTE risk warranting intervention
    - **Positive Predictive Value**: Sufficient to justify prophylaxis benefits over risks
    - **Management Implications**: Thromboprophylaxis recommended unless contraindicated
    
    **CLINICAL MANAGEMENT BY RISK CATEGORY**:
    
    **Low Risk Management Approach**:
    
    **Prophylaxis Strategy**:
    - **Primary Recommendation**: Mechanical prophylaxis preferred over pharmacological
    - **Mechanical Options**: Sequential compression devices, graduated compression stockings
    - **Mobilization**: Early and frequent ambulation when clinically feasible
    - **Monitoring**: Daily reassessment for changes in risk factors or clinical status
    
    **Considerations**:
    - **Cost-Effectiveness**: Avoid unnecessary anticoagulation costs and monitoring
    - **Safety Profile**: Minimize bleeding risks associated with pharmacological prophylaxis
    - **Patient Comfort**: Reduce injection burden and potential adverse effects
    - **Quality Metrics**: Appropriate use of prophylaxis resources
    
    **Patient Education**:
    - **VTE Awareness**: Signs and symptoms of DVT and PE
    - **Preventive Measures**: Importance of early mobilization and hydration
    - **Risk Factor Modification**: Address modifiable factors when possible
    - **Communication**: Clear explanation of low-risk status and management rationale
    
    **High Risk Management Approach**:
    
    **Pharmacological Prophylaxis**:
    
    **First-Line Options**:
    - **Low Molecular Weight Heparin (LMWH)**: Enoxaparin 40mg daily subcutaneous
    - **Unfractionated Heparin (UFH)**: 5,000 units q8-12h subcutaneous
    - **Fondaparinux**: 2.5mg daily subcutaneous (if heparin contraindicated)
    
    **Dosing Adjustments**:
    - **Renal Impairment**: Reduce LMWH dose or use UFH for CrCl <30 mL/min
    - **Weight-Based Considerations**: May require dose adjustment for extreme weights
    - **Elderly Patients**: Consider reduced dosing and enhanced monitoring
    
    **Contraindications Assessment**:
    - **Absolute**: Active bleeding, severe thrombocytopenia (<50,000/μL)
    - **Relative**: Recent surgery with high bleeding risk, severe liver disease
    - **Drug Interactions**: Concurrent anticoagulation, antiplatelet therapy
    - **Patient Factors**: History of heparin-induced thrombocytopenia
    
    **Alternative Strategies**:
    - **Mechanical Prophylaxis**: If pharmacological prophylaxis contraindicated
    - **Combined Approach**: Mechanical plus pharmacological for highest-risk patients
    - **Inferior Vena Cava Filter**: Rare cases with contraindications and very high risk
    
    **Monitoring and Duration**:
    
    **Clinical Monitoring**:
    - **Daily Assessment**: Signs of bleeding, thrombocytopenia, skin reactions
    - **Laboratory Monitoring**: Platelet count every 2-3 days for UFH
    - **Efficacy Surveillance**: Monitor for VTE symptoms throughout hospitalization
    - **Risk Reassessment**: Daily evaluation for changes in clinical status
    
    **Duration Considerations**:
    - **Standard Duration**: Throughout hospitalization until discharge
    - **Extended Prophylaxis**: Consider for high-risk patients with prolonged recovery
    - **Transition Planning**: Bridge to outpatient anticoagulation if indicated
    - **Discontinuation**: When patient fully mobile or bleeding risk increases
    
    **Quality Improvement and Documentation**:
    
    **Performance Metrics**:
    - **Appropriate Prophylaxis Rate**: Percentage of high-risk patients receiving prophylaxis
    - **Avoidance of Overuse**: Percentage of low-risk patients not receiving unnecessary prophylaxis
    - **VTE Prevention**: Hospital-acquired VTE rates and preventable events
    - **Bleeding Complications**: Prophylaxis-associated bleeding events and outcomes
    
    **Documentation Requirements**:
    - **Risk Assessment**: Clear documentation of Geneva score calculation and rationale
    - **Prophylaxis Decision**: Explicit documentation of prophylaxis choice and reasoning
    - **Contraindications**: Documentation of any factors precluding standard prophylaxis
    - **Patient Communication**: Record of patient education and consent
    
    **Special Clinical Situations**:
    
    **High-Risk Subgroups**:
    - **Active Malignancy**: Consider extended prophylaxis and higher intensity
    - **Prior VTE**: May warrant therapeutic rather than prophylactic anticoagulation
    - **Multiple Risk Factors**: Enhanced monitoring and combination prophylaxis
    - **Critical Illness**: Consider therapeutic anticoagulation in ICU settings
    
    **Bleeding Risk Considerations**:
    - **IMPROVE Bleeding Score**: Consider complementary bleeding risk assessment
    - **Risk-Benefit Analysis**: Weigh VTE prevention against bleeding complications
    - **Individualized Approach**: Tailor prophylaxis to patient-specific factors
    - **Multidisciplinary Discussion**: Involve specialists for complex cases
    
    Reference: Nendaz M, et al. Thromb Haemost. 2014;111(3):531-538.
    """
    
    result: int = Field(
        ...,
        description="Geneva VTE Risk Score calculated from risk factors (0-33 points)",
        ge=0,
        le=33,
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for Geneva VTE Risk Score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk factor analysis and evidence-based prophylaxis recommendations",
        example="Geneva VTE Risk Score: 5 points. Major risk factors (2 pts each): acute infectious disease/sepsis. Minor risk factors (1 pt each): immobilization (≥3 days), age >60 years, dehydration. High risk for venous thromboembolism (approximately 3.2% risk). Thromboprophylaxis recommended unless contraindicated. Consider low molecular weight heparin, unfractionated heparin, or fondaparinux based on renal function and bleeding risk. If pharmacological prophylaxis is contraindicated, use mechanical prophylaxis (sequential compression devices). Continue prophylaxis throughout hospitalization and consider extended prophylaxis based on risk factors."
    )
    
    stage: str = Field(
        ...,
        description="VTE risk category classification (Low Risk or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of VTE risk level",
        example="High risk for VTE"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Geneva VTE Risk Score: 5 points. Major risk factors (2 pts each): acute infectious disease/sepsis. Minor risk factors (1 pt each): immobilization (≥3 days), age >60 years, dehydration. High risk for venous thromboembolism (approximately 3.2% risk). Thromboprophylaxis recommended unless contraindicated. Consider low molecular weight heparin, unfractionated heparin, or fondaparinux based on renal function and bleeding risk. If pharmacological prophylaxis is contraindicated, use mechanical prophylaxis (sequential compression devices). Continue prophylaxis throughout hospitalization and consider extended prophylaxis based on risk factors.",
                "stage": "High Risk",
                "stage_description": "High risk for VTE"
            }
        }