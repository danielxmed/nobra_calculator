"""
Licurse Score for Renal Ultrasound Models

Request and response models for Licurse Score calculation.

References (Vancouver style):
1. Licurse A, Dziura J, Spinella PC, Dziura J, Kahan BC, Nelson LS, et al. 
   Renal ultrasonography in the evaluation of acute kidney injury: developing 
   a risk stratification framework. Archives of Internal Medicine. 2010 Nov 
   22;170(21):1900-7. doi: 10.1001/archinternmed.2010.362.
2. Ip IK, Silveira PC, Alper EC, Zalis MG, Oliva MR, Hanson RH, et al. 
   External validation of risk stratification strategy in the use of renal 
   ultrasonography in the evaluation of acute kidney injury. Journal of 
   Hospital Medicine. 2016 May;11(5):316-21. doi: 10.1002/jhm.2598.
3. Ip IK, Jang HJ, Babiarz LS, Patel RP, McMahon B, Ali S, et al. What is 
   the appropriate use of renal ultrasound in an inner city population with 
   new onset acute kidney injury? Emergency Medicine Journal. 2015 Nov;32(11):
   916-20. doi: 10.1136/emermed-2014-204141.

The Licurse Score for Renal Ultrasound is a validated clinical decision tool developed 
to predict the likelihood of hydronephrosis on renal ultrasonography in adult patients 
with acute kidney injury (AKI). This risk stratification framework helps clinicians 
determine the appropriate use of renal ultrasound, reducing unnecessary imaging while 
maintaining diagnostic accuracy for those who truly need intervention.

Clinical Background:
Acute kidney injury affects approximately 13.3 million people worldwide annually and is 
associated with significant morbidity and mortality. Urinary tract obstruction accounts 
for 5-10% of AKI cases but is one of the most readily reversible causes when identified 
early. However, renal ultrasound is often ordered routinely in AKI evaluation, leading 
to unnecessary healthcare costs and potential delays in definitive care.

The Licurse Score was developed and internally validated using data from 223 consecutive 
adult patients with AKI at Yale-New Haven Hospital from January 2005 to May 2009. The 
tool demonstrated excellent discriminative ability and has been externally validated in 
multiple independent cohorts across different healthcare settings.

Risk Stratification Framework:

Historical Context and Automatic Risk Assignment:
Patients with a history of hydronephrosis are automatically classified as high-risk 
regardless of other clinical factors. This reflects the known predisposition to recurrent 
urinary tract obstruction and the clinical imperative to exclude this reversible cause 
of AKI in vulnerable patients.

Scoring Components for Patients Without Prior Hydronephrosis:

1. Race (Non-Black: 1 point):
   Epidemiological studies demonstrate racial differences in the prevalence of conditions 
   predisposing to urinary tract obstruction. Non-black patients have higher rates of 
   nephrolithiasis, benign prostatic hyperplasia, and certain malignancies that can cause 
   obstruction. While race is a complex social construct, it serves as a proxy for genetic, 
   environmental, and healthcare access factors that influence obstruction risk.

2. History of Recurrent Urinary Tract Infections (1 point if present):
   Recurrent UTIs suggest anatomical abnormalities, functional voiding disorders, or 
   conditions that predispose to urinary stasis and obstruction. These patients have 
   higher baseline risk for structural abnormalities that may contribute to AKI through 
   obstructive mechanisms.

3. Diagnosis Consistent with Possible Obstruction (1 point if present):
   This includes established diagnoses known to cause urinary tract obstruction:
   - Benign prostatic hyperplasia (BPH): Common in older men, causing bladder outlet obstruction
   - Abdominal or pelvic malignancy: Primary or metastatic tumors causing extrinsic compression
   - Neurogenic bladder: Impaired bladder function leading to retention and reflux
   - Single functioning kidney: Higher clinical significance of any degree of obstruction
   - History of pelvic surgery: Increased risk of ureteral injury or stricture formation

4. No History of Congestive Heart Failure (1 point if absent):
   The absence of CHF suggests that prerenal causes are less likely to be the primary 
   etiology of AKI. Conversely, patients with known CHF are more likely to have 
   cardiorenal syndrome or volume-related AKI rather than obstructive causes.

5. No History of Sepsis/Prerenal AKI/Pressors/Hypotension (1 point if absent):
   The absence of these systemic factors suggests that intrarenal or postrenal causes 
   are more likely. Patients without evidence of sepsis or hemodynamic instability are 
   more likely to have structural causes of AKI requiring imaging evaluation.

6. No Exposure to Nephrotoxic Medications (1 point if absent):
   The absence of nephrotoxic drug exposure reduces the likelihood of drug-induced 
   intrarenal AKI. Common nephrotoxins include NSAIDs, ACE inhibitors, ARBs, 
   aminoglycosides, contrast agents, and certain chemotherapy agents.

Clinical Performance and Validation:

Original Validation Study Results:
- Low-risk group (≤2 points): 4.0% hydronephrosis rate, 1.1% intervention rate
- Medium-risk group (3 points): 6.8% hydronephrosis rate, 0.5% intervention rate  
- High-risk group (>3 points): 20.9% hydronephrosis rate, 4.9% intervention rate

External Validation Performance:
A subsequent multicenter validation study demonstrated:
- Sensitivity: 91.3% for urological intervention, 93.4% for hydronephrosis
- Specificity: 23.0% for urological intervention, 25.1% for hydronephrosis
- Negative predictive value: 98.9% for urological intervention

Cost-Effectiveness Analysis:
- Number needed to screen (NNS) in low-risk group: 25 for hydronephrosis, 91 for intervention
- Cost per positive study in low-risk group: $5,000 for hydronephrosis (at $200/study)
- Annual potential savings: Estimated $1.2 million at a single academic center

Clinical Applications and Treatment Decision Framework:

Low-Risk Group (≤2 points):
- Clinical Strategy: Defer renal ultrasound initially
- Alternative Approach: Address volume status, discontinue nephrotoxins, treat underlying conditions
- Imaging Trigger: Consider ultrasound if no improvement after 24-48 hours of conservative management
- Cost-Benefit: Low yield imaging with high NNS, resource optimization opportunity

Medium-Risk Group (3 points):
- Clinical Strategy: Individualized decision-making based on clinical context
- Considerations: Severity of AKI, rate of creatinine rise, clinical presentation
- Timing: Early ultrasound may be appropriate with high clinical suspicion
- Monitoring: Close follow-up with reassessment if conservative measures fail

High-Risk Group (>3 points or history of hydronephrosis):
- Clinical Strategy: Prompt renal ultrasound indicated
- Urgency: Consider urgent imaging if rapid decline in renal function
- Intervention Readiness: Prepare for potential urological consultation
- Follow-up: Serial monitoring if hydronephrosis identified

Integration with Clinical Workflow:

Emergency Department Applications:
- Rapid risk stratification for AKI patients
- Resource allocation and throughput optimization  
- Systematic approach to ultrasound ordering

Inpatient Management:
- Guide timing of nephrology consultation
- Coordinate with urology for high-risk patients
- Optimize length of stay through efficient evaluation

Quality Improvement Applications:
- Reduce unnecessary imaging and associated costs
- Standardize AKI evaluation protocols
- Monitor appropriate use of renal ultrasound

Limitations and Considerations:

Clinical Limitations:
- Derived from single-center academic medical center population
- May not generalize to all healthcare settings or patient populations
- Does not replace clinical judgment or comprehensive patient assessment
- Performance may vary with different ultrasound techniques and interpretation

Methodological Considerations:
- Retrospective derivation with inherent selection bias
- Limited sample size for certain risk categories
- External validation shows lower specificity than derivation study
- Need for periodic recalibration as practice patterns evolve

Future Directions:
- Integration with electronic health records for automated risk calculation
- Validation in specific populations (pediatric, elderly, chronic kidney disease)
- Cost-effectiveness studies in different healthcare systems
- Development of machine learning models incorporating additional variables

Quality Measures and Performance Indicators:
- Appropriate use of risk stratification in eligible AKI patients
- Correlation between risk category and imaging utilization
- Clinical outcomes in patients managed according to risk stratification
- Cost savings through reduced unnecessary imaging
- Time to definitive diagnosis and treatment in high-risk patients

Patient Safety Considerations:
- Clear documentation of risk assessment and decision rationale
- Safety nets for patients who deteriorate despite low-risk classification
- Regular reassessment as clinical status evolves
- Communication with patients and families about evaluation approach
- Integration with existing AKI protocols and pathways
"""

from pydantic import BaseModel, Field
from typing import Literal


class LicurseScoreRequest(BaseModel):
    """
    Request model for Licurse Score for Renal Ultrasound
    
    The Licurse Score for Renal Ultrasound is a validated clinical decision tool that 
    predicts the likelihood of hydronephrosis on renal ultrasonography in adult patients 
    with acute kidney injury. This risk stratification framework helps clinicians make 
    evidence-based decisions about the appropriate use of renal ultrasound, optimizing 
    resource utilization while maintaining diagnostic accuracy.
    
    Clinical Assessment Parameters:
    
    History of Hydronephrosis:
    Any prior documentation of hydronephrosis automatically classifies the patient as 
    high-risk, regardless of other clinical factors. This reflects the established 
    predisposition to recurrent urinary tract obstruction and the clinical imperative 
    to exclude this readily reversible cause of AKI in vulnerable patients.
    
    Race Classification:
    While race is a complex social construct, epidemiological data demonstrate significant 
    differences in conditions predisposing to urinary tract obstruction. Non-black patients 
    have statistically higher rates of nephrolithiasis, benign prostatic hyperplasia, and 
    certain malignancies that can cause obstruction. This parameter serves as a proxy for 
    genetic, environmental, and healthcare access factors influencing obstruction risk.
    
    Recurrent Urinary Tract Infections:
    A history of recurrent UTIs suggests underlying anatomical abnormalities, functional 
    voiding disorders, or conditions predisposing to urinary stasis. These structural or 
    functional abnormalities increase the baseline risk for obstruction that may contribute 
    to AKI through postrenal mechanisms.
    
    Obstruction-Associated Diagnoses:
    Established diagnoses with known association to urinary tract obstruction include:
    - Benign prostatic hyperplasia: Bladder outlet obstruction in older men
    - Abdominal/pelvic malignancy: Primary or metastatic tumor causing extrinsic compression
    - Neurogenic bladder: Impaired bladder function with retention and potential reflux
    - Single functioning kidney: Higher clinical significance of any degree of obstruction
    - Pelvic surgery history: Increased risk of ureteral injury or stricture formation
    
    Congestive Heart Failure History:
    The presence of CHF increases the likelihood that AKI is due to cardiorenal syndrome 
    or hemodynamic factors rather than obstructive causes. Conversely, the absence of CHF 
    suggests that prerenal etiologies are less likely, making postrenal causes more probable.
    
    Prerenal AKI Risk Factors:
    History of sepsis, known prerenal AKI, vasopressor use, or hypotension suggests systemic 
    causes of AKI rather than structural obstruction. The absence of these factors increases 
    the relative likelihood of intrarenal or postrenal etiologies requiring imaging evaluation.
    
    Nephrotoxic Medication Exposure:
    Exposure to known nephrotoxic medications (NSAIDs, ACE inhibitors, ARBs, aminoglycosides, 
    contrast agents, chemotherapy) increases the likelihood of drug-induced intrarenal AKI. 
    The absence of such exposure makes obstructive causes relatively more likely.
    
    Clinical Application Guidelines:
    - Apply to adult patients with acute kidney injury
    - Ensure accurate medication history and comorbidity assessment
    - Consider temporal relationship between risk factors and AKI onset
    - Integrate results with overall clinical assessment and institutional protocols
    - Document decision rationale in medical record
    - Reassess if clinical status changes or initial management fails
    
    Risk Stratification Outcomes:
    - Low Risk (≤2 points): 4.0% hydronephrosis risk, may defer ultrasound initially
    - Medium Risk (3 points): 6.8% hydronephrosis risk, individualized decision-making
    - High Risk (>3 points): 20.9% hydronephrosis risk, ultrasound strongly indicated
    - History of hydronephrosis: Automatic high-risk classification, urgent evaluation needed
    
    Quality Assurance Considerations:
    - Verify accuracy of historical information through chart review
    - Ensure consistent application of risk stratification criteria
    - Monitor clinical outcomes and validate local performance
    - Adjust protocols based on institutional experience and validation studies
    - Maintain clear documentation of risk assessment and management decisions
    
    References (Vancouver style):
    1. Licurse A, Dziura J, Spinella PC, Dziura J, Kahan BC, Nelson LS, et al. 
    Renal ultrasonography in the evaluation of acute kidney injury: developing 
    a risk stratification framework. Archives of Internal Medicine. 2010 Nov 
    22;170(21):1900-7. doi: 10.1001/archinternmed.2010.362.
    2. Ip IK, Silveira PC, Alper EC, Zalis MG, Oliva MR, Hanson RH, et al. 
    External validation of risk stratification strategy in the use of renal 
    ultrasonography in the evaluation of acute kidney injury. Journal of 
    Hospital Medicine. 2016 May;11(5):316-21. doi: 10.1002/jhm.2598.
    """
    
    history_hydronephrosis: Literal["yes", "no"] = Field(
        ...,
        description="History of hydronephrosis. Any prior documentation of hydronephrosis automatically "
                   "classifies the patient as high-risk regardless of other clinical factors. This reflects "
                   "the established predisposition to recurrent urinary tract obstruction and the clinical "
                   "imperative to exclude this readily reversible cause of AKI in vulnerable patients.",
        example="no"
    )
    
    race: Literal["black", "non_black"] = Field(
        ...,
        description="Patient race classification. Non-black patients have statistically higher rates of "
                   "nephrolithiasis, benign prostatic hyperplasia, and certain malignancies that can cause "
                   "urinary tract obstruction. While race is a complex social construct, epidemiological "
                   "data demonstrate significant differences in conditions predisposing to obstruction. "
                   "This parameter serves as a proxy for genetic, environmental, and healthcare access "
                   "factors that influence obstruction risk. Non-black race scores 1 point.",
        example="non_black"
    )
    
    recurrent_utis: Literal["yes", "no"] = Field(
        ...,
        description="History of recurrent urinary tract infections. Recurrent UTIs suggest underlying "
                   "anatomical abnormalities, functional voiding disorders, or conditions predisposing "
                   "to urinary stasis and obstruction. These structural or functional abnormalities "
                   "increase the baseline risk for obstruction that may contribute to AKI through "
                   "postrenal mechanisms. Recurrent UTIs are typically defined as ≥3 UTIs in the past "
                   "12 months or ≥2 UTIs in the past 6 months. Scores 1 point if present.",
        example="no"
    )
    
    obstruction_diagnosis: Literal["yes", "no"] = Field(
        ...,
        description="Diagnosis consistent with possible urinary tract obstruction. This includes established "
                   "diagnoses with known association to obstruction: benign prostatic hyperplasia (BPH) "
                   "causing bladder outlet obstruction; abdominal or pelvic malignancy (primary or metastatic) "
                   "causing extrinsic compression; neurogenic bladder with impaired function and potential "
                   "retention; single functioning kidney where any degree of obstruction has higher clinical "
                   "significance; history of pelvic surgery with increased risk of ureteral injury or "
                   "stricture formation. Scores 1 point if any of these conditions are present.",
        example="no"
    )
    
    history_chf: Literal["yes", "no"] = Field(
        ...,
        description="History of congestive heart failure. The presence of CHF increases the likelihood "
                   "that AKI is due to cardiorenal syndrome or hemodynamic factors rather than obstructive "
                   "causes. Patients with known CHF are more likely to have volume-related or perfusion-related "
                   "AKI. Conversely, the absence of CHF suggests that prerenal etiologies are less likely, "
                   "making postrenal (obstructive) causes relatively more probable. Scores 1 point if CHF "
                   "history is absent (indicating higher risk for obstruction).",
        example="no"
    )
    
    prerenal_aki_sepsis: Literal["yes", "no"] = Field(
        ...,
        description="History of sepsis, prerenal AKI, vasopressor use, or hypotension. The presence of "
                   "these systemic factors suggests that AKI is more likely due to hemodynamic or systemic "
                   "causes rather than structural urinary tract obstruction. This includes documented sepsis, "
                   "known prerenal AKI episodes, requirement for vasopressor support, or significant "
                   "hypotension. The absence of these factors increases the relative likelihood of intrarenal "
                   "or postrenal etiologies that would benefit from imaging evaluation. Scores 1 point if "
                   "these prerenal factors are absent (indicating higher risk for obstruction).",
        example="no"
    )
    
    nephrotoxic_exposure: Literal["yes", "no"] = Field(
        ...,
        description="Recent exposure to nephrotoxic medications. Common nephrotoxins include nonsteroidal "
                   "anti-inflammatory drugs (NSAIDs), ACE inhibitors, angiotensin receptor blockers (ARBs), "
                   "aminoglycoside antibiotics, radiocontrast agents, and certain chemotherapy agents. "
                   "Exposure to these medications increases the likelihood of drug-induced intrarenal AKI. "
                   "The absence of nephrotoxic exposure makes obstructive (postrenal) causes relatively "
                   "more likely and increases the potential benefit of renal imaging. Scores 1 point if "
                   "nephrotoxic exposure is absent (indicating higher risk for obstruction).",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "history_hydronephrosis": "no",
                "race": "non_black",
                "recurrent_utis": "no",
                "obstruction_diagnosis": "no",
                "history_chf": "no",
                "prerenal_aki_sepsis": "no",
                "nephrotoxic_exposure": "yes"
            }
        }


class LicurseScoreResponse(BaseModel):
    """
    Response model for Licurse Score for Renal Ultrasound
    
    Provides calculated risk stratification score with evidence-based recommendations 
    for renal ultrasound utilization in adult patients with acute kidney injury. The 
    response categorizes patients into risk groups that guide clinical decision-making 
    and optimize resource utilization while maintaining diagnostic accuracy.
    
    Risk Stratification Categories and Clinical Implications:
    
    Low Risk (≤2 points):
    - Hydronephrosis risk: 4.0%
    - Urological intervention risk: 1.1%
    - Clinical approach: May defer renal ultrasound initially
    - Alternative management: Focus on volume optimization, nephrotoxin avoidance, conservative care
    - Imaging triggers: Consider ultrasound if no improvement after 24-48 hours of conservative management
    - Cost-effectiveness: Number needed to screen = 25 for hydronephrosis, representing low yield imaging
    - Monitoring: Close clinical follow-up with reassessment if AKI persists or worsens
    
    Medium Risk (3 points):
    - Hydronephrosis risk: 6.8%
    - Urological intervention risk: 0.5%
    - Clinical approach: Individualized decision-making based on clinical context
    - Considerations: Severity of AKI, rate of creatinine rise, clinical presentation, institutional protocols
    - Timing: Early ultrasound may be appropriate with high clinical suspicion for obstruction
    - Monitoring: Close follow-up with reassessment of renal function and clinical status
    - Flexibility: Protocol may be adjusted based on patient-specific factors and clinical judgment
    
    High Risk (>3 points):
    - Hydronephrosis risk: 20.9%
    - Urological intervention risk: 4.9%
    - Clinical approach: Renal ultrasound strongly indicated
    - Urgency: Consider urgent imaging if rapid decline in renal function or clinical deterioration
    - Intervention readiness: Prepare for potential urological consultation and intervention
    - Follow-up: Serial monitoring and multidisciplinary care coordination if hydronephrosis identified
    
    Automatic High Risk (History of Hydronephrosis):
    - Risk assignment: Automatic high-risk classification regardless of other factors
    - Clinical rationale: Known predisposition to recurrent urinary tract obstruction
    - Management approach: Urgent renal ultrasound to evaluate for recurrent hydronephrosis
    - Intervention planning: Early urological consultation if significant findings identified
    
    Clinical Decision Framework:
    
    Emergency Department Applications:
    - Rapid risk stratification for systematic AKI evaluation
    - Resource allocation and throughput optimization
    - Evidence-based approach to ultrasound ordering
    - Integration with existing AKI protocols
    
    Inpatient Management:
    - Guide timing and urgency of nephrology consultation
    - Coordinate multidisciplinary care with urology for high-risk patients
    - Optimize length of stay through efficient diagnostic evaluation
    - Support clinical decision-making with validated risk assessment
    
    Quality Improvement Implementation:
    - Reduce unnecessary imaging and associated healthcare costs
    - Standardize AKI evaluation protocols across departments
    - Monitor appropriate use metrics and clinical outcomes
    - Validate local performance and calibrate thresholds as needed
    
    Communication and Documentation:
    - Clear documentation of risk assessment methodology and results
    - Transparent communication with patients and families about evaluation approach
    - Rationale for imaging decisions based on evidence-based risk stratification
    - Integration with existing clinical pathways and institutional protocols
    
    Performance Metrics and Validation:
    - Original validation: 91.3% sensitivity for urological intervention, 93.4% for hydronephrosis
    - External validation: Maintained high sensitivity with 98.9% negative predictive value
    - Cost-effectiveness: Estimated annual savings of $1.2 million at single academic center
    - Quality measures: Appropriate use correlation with risk category and clinical outcomes
    
    Limitations and Clinical Considerations:
    - Population-based risk estimates; individual outcomes may vary
    - Should complement, not replace, comprehensive clinical assessment and judgment
    - Performance may vary across different healthcare settings and patient populations
    - Regular reassessment needed as clinical status and risk factors evolve
    - Integration with institutional protocols and local practice patterns
    
    Safety Considerations and Risk Mitigation:
    - Clear documentation of risk assessment and management rationale
    - Safety nets for patients who deteriorate despite low-risk classification
    - Regular reassessment protocols as clinical status changes
    - Escalation pathways for clinical deterioration or diagnostic uncertainty
    - Quality assurance monitoring of outcomes across risk categories
    
    Reference: Licurse A, et al. Archives of Internal Medicine. 2010;170(21):1900-7.
    """
    
    result: int = Field(
        ...,
        description="Licurse Score calculated from clinical risk factors (range: 0-6 points, or 99 for automatic high-risk due to hydronephrosis history)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk stratification score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk stratification, hydronephrosis probability, "
                   "intervention likelihood, and evidence-based recommendations for renal ultrasound utilization",
        example="Licurse Score: 4 points. Risk category: High Risk. High risk group with 20.9% risk of hydronephrosis and 4.9% risk of urological intervention. Renal ultrasound is strongly indicated for evaluation of possible urinary tract obstruction. Given the significant risk of hydronephrosis requiring intervention, prompt imaging is recommended to guide appropriate management decisions. Early detection of obstruction can prevent further kidney damage and facilitate timely urological consultation if intervention is needed."
    )
    
    stage: str = Field(
        ...,
        description="Risk category for hydronephrosis probability (Low Risk, Medium Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High risk for hydronephrosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Licurse Score: 4 points. Risk category: High Risk. High risk group with 20.9% risk of hydronephrosis and 4.9% risk of urological intervention. Renal ultrasound is strongly indicated for evaluation of possible urinary tract obstruction. Given the significant risk of hydronephrosis requiring intervention, prompt imaging is recommended to guide appropriate management decisions. Early detection of obstruction can prevent further kidney damage and facilitate timely urological consultation if intervention is needed.",
                "stage": "High Risk",
                "stage_description": "High risk for hydronephrosis"
            }
        }