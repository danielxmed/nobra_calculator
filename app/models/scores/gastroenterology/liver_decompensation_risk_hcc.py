"""
Liver Decompensation Risk after Hepatectomy for HCC Models

Request and response models for Liver Decompensation Risk calculation.

References (Vancouver style):
1. Cescon M, Colecchia A, Cucchetti A, Peri E, Montrone L, Berretta M, et al. 
   Value of transient elastography measured with FibroScan in predicting the outcome 
   of hepatic resection for hepatocellular carcinoma. Ann Surg. 2012 Nov;256(5):706-12; 
   discussion 712-3. doi: 10.1097/SLA.0b013e3182724258.
2. Cucchetti A, Ercolani G, Vivarelli M, Cescon M, Ravaioli M, La Barba G, et al. 
   Impact of model for end-stage liver disease (MELD) score on prognosis after 
   hepatectomy for hepatocellular carcinoma on cirrhosis. Liver Transpl. 2006 Jun;12(6):966-71. 
   doi: 10.1002/lt.20769.
3. Santambrogio R, Kluger MD, Costa M, Belli A, Barabino M, Laurent A, et al. 
   Hepatic resection for hepatocellular carcinoma in patients with Child-Pugh's A cirrhosis: 
   is clinical evidence of portal hypertension a contraindication? HPB (Oxford). 2013 Jan;15(1):78-84. 
   doi: 10.1111/j.1477-2574.2012.00583.x.

The Liver Decompensation Risk after Hepatectomy for Hepatocellular Carcinoma (HCC) is a 
validated clinical prediction tool that stratifies patients into low, intermediate, and high 
risk categories for post-operative liver decompensation. This evidence-based calculator was 
developed from analysis of 543 patients with HCC undergoing hepatectomy and enables clinicians 
to make informed decisions about surgical candidacy, perioperative management strategies, and 
alternative treatment considerations.

Clinical Background:
Hepatocellular carcinoma (HCC) represents the most common primary liver malignancy worldwide 
and the third leading cause of cancer-related mortality. Surgical resection remains the 
treatment of choice for patients with preserved liver function and absence of portal 
hypertension. However, patients with underlying cirrhosis or significant liver dysfunction 
face substantial risks of post-operative liver decompensation, which can result in liver 
failure, prolonged hospitalization, and increased mortality.

The decision to proceed with hepatectomy in patients with HCC requires careful balance between 
oncologic benefit and perioperative risk. Traditional assessments based solely on Child-Pugh 
classification or MELD scores may not adequately capture the complex interplay of factors 
that influence post-operative outcomes. This prediction model addresses this clinical need 
by providing a structured, evidence-based approach to risk stratification.

Model Development and Validation:

The Liver Decompensation Risk model was derived from a comprehensive analysis of 543 consecutive 
patients with HCC who underwent hepatic resection. The study identified three independent 
predictors of post-operative liver decompensation through multivariable logistic regression 
analysis, with hierarchical interaction effects that enhance predictive accuracy.

Key Predictive Factors and Clinical Significance:

Portal Hypertension (Primary Risk Factor):
Portal hypertension emerged as the most significant predictor of post-operative liver 
decompensation (OR, 2.99; 95% CI, 1.93-4.62; P < .001). In the context of this model, 
portal hypertension is defined by the presence of at least F1 esophageal varices on upper 
endoscopy OR the combination of platelet count <100,000/μL with splenomegaly on imaging.

Clinical Assessment of Portal Hypertension:
- Upper endoscopy revealing esophageal varices (F1 or greater)
- Platelet count <100,000/μL combined with splenomegaly
- Additional supportive findings may include ascites, abdominal collaterals, or hepatic 
  venous pressure gradient (HVPG) ≥10 mmHg when available

The presence of portal hypertension indicates advanced liver disease with compromised 
hepatic reserve and increased risk of post-operative complications. Patients with portal 
hypertension demonstrate impaired regenerative capacity and are more susceptible to 
post-hepatectomy liver failure.

Extension of Hepatectomy (Secondary Risk Factor):
The extent of planned hepatic resection significantly influences decompensation risk 
(OR, 2.41; 95% CI, 1.17-4.30; P = .01). The model distinguishes between:

Major Hepatectomy:
- Removal of ≥3 adjacent hepatic segments
- Examples: right hepatectomy, left hepatectomy, right trisectionectomy
- Associated with greater parenchymal loss and functional compromise
- Requires significant hepatic regenerative capacity

Minor Hepatectomy:
- Removal of <3 hepatic segments
- Examples: segmentectomy, bisegmentectomy, wedge resection
- Preserves greater functional hepatic mass
- Generally associated with lower decompensation risk

MELD Score (Tertiary Risk Factor):
The Model for End-Stage Liver Disease (MELD) score provides additional risk stratification, 
particularly in patients without portal hypertension undergoing minor resections (OR, 2.26; 
95% CI, 1.10-4.58; P = .02). The critical threshold of MELD >9 identifies patients at 
increased risk even in the absence of other major risk factors.

MELD Score Calculation:
MELD = 3.8[ln(bilirubin mg/dL)] + 11.2[ln(INR)] + 9.6[ln(creatinine mg/dL)] + 6.4

Laboratory Requirements for MELD:
- Serum total bilirubin (mg/dL): marker of hepatocellular function and cholestasis
- International Normalized Ratio (INR): reflects hepatic synthetic function
- Serum creatinine (mg/dL): indicates renal function and potential hepatorenal syndrome

Risk Stratification Framework:

Low Risk Category (4.9% Decompensation Rate):
- Clinical Profile: No portal hypertension + Minor resection + MELD score ≤9
- Patient Population: 226 patients (41.6% of cohort)
- Expected Outcomes: Median length of stay 7 days, liver-related mortality 4.4%
- Clinical Significance: Optimal surgical candidates with minimal perioperative risk
- Management Approach: Standard surgical care with routine postoperative monitoring

Intermediate Risk Category (28.6% Decompensation Rate):
- Clinical Profile: No portal hypertension + Major resection OR Minor resection + 
  (Portal hypertension OR MELD >9)
- Patient Population: 297 patients (54.7% of cohort)
- Expected Outcomes: Median length of stay 8 days, liver-related mortality 9.0%
- Clinical Significance: Moderate risk requiring enhanced perioperative management
- Management Approach: Intensive monitoring, potential ICU admission, multidisciplinary care

High Risk Category (60.0% Decompensation Rate):
- Clinical Profile: Major resection + Portal hypertension
- Patient Population: 20 patients (3.7% of cohort)
- Expected Outcomes: Median length of stay 11 days, liver-related mortality 25.0%
- Clinical Significance: Prohibitive surgical risk requiring careful consideration
- Management Approach: Consider alternative treatments, mandatory ICU care if surgery proceeds

Clinical Decision-Making Applications:

Preoperative Assessment:
The risk calculator should be integrated into comprehensive preoperative evaluation alongside 
imaging assessment of tumor characteristics, functional liver assessment (Child-Pugh, 
hepatic volumetry), and patient performance status evaluation. High-risk patients may benefit 
from alternative treatments including liver transplantation, ablative therapies, or 
transarterial chemoembolization.

Surgical Planning:
Risk stratification informs decisions about operative approach, extent of resection, and 
perioperative management strategies. Intermediate and high-risk patients require enhanced 
monitoring protocols, potential intensive care admission, and multidisciplinary team 
coordination.

Patient Counseling:
Risk estimates facilitate informed consent discussions, allowing patients and families to 
understand expected outcomes and make educated treatment decisions. The calculator provides 
objective, evidence-based risk estimates that enhance communication quality.

Quality Improvement:
Risk-adjusted outcome monitoring enables institutions to track performance, identify areas 
for improvement, and benchmark results against expected outcomes based on patient case mix.

Limitations and Considerations:

Model Applicability:
- Derived from patients with HCC undergoing curative-intent resection
- May not apply to patients with other liver malignancies or benign conditions
- Performance may vary in different populations or healthcare systems

Clinical Assessment Requirements:
- Accurate assessment of portal hypertension requires appropriate diagnostic studies
- MELD score calculation requires recent, accurate laboratory values
- Surgical planning must account for tumor-specific factors not captured in the model

Alternative Treatment Considerations:
High-risk patients should be evaluated for liver transplantation when appropriate, as this 
may provide both oncologic cure and definitive treatment of underlying liver disease. 
Multidisciplinary tumor board discussion is essential for optimal treatment planning.

Research and Future Directions:

The model has been validated in multiple independent cohorts and continues to serve as a 
foundation for hepatic surgery risk assessment. Future research directions include integration 
with novel biomarkers, imaging-based liver function assessment, and long-term oncologic 
outcomes to further refine risk prediction and optimize patient selection.

This evidence-based tool represents a significant advancement in hepatic surgery risk 
assessment, enabling more precise patient selection, enhanced perioperative care, and 
improved communication between clinicians and patients facing complex treatment decisions 
in the management of hepatocellular carcinoma.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class LiverDecompensationRiskHccRequest(BaseModel):
    """
    Request model for Liver Decompensation Risk after Hepatectomy for HCC
    
    The Liver Decompensation Risk calculator is a validated clinical prediction tool that 
    stratifies patients with hepatocellular carcinoma into risk categories for post-operative 
    liver decompensation. This evidence-based model enables informed surgical decision-making 
    and perioperative management planning by identifying patients at low, intermediate, and 
    high risk for adverse outcomes following hepatic resection.
    
    Clinical Assessment Parameters:
    
    Portal Hypertension Assessment:
    Portal hypertension represents the most significant predictor of post-operative liver 
    decompensation (odds ratio 2.99, 95% CI 1.93-4.62) and serves as the primary risk 
    stratification factor. The presence of portal hypertension indicates advanced liver 
    disease with compromised hepatic reserve and impaired regenerative capacity.
    
    Diagnostic Criteria for Portal Hypertension:
    - Upper endoscopy revealing F1 or greater esophageal varices (small, straight varices)
    - Platelet count <100,000/μL in the presence of splenomegaly on imaging
    - Supporting evidence may include ascites, abdominal collaterals, or hepatic venous 
      pressure gradient (HVPG) ≥10 mmHg when available
    
    Clinical Significance of Portal Hypertension:
    Portal hypertension reflects increased resistance to portal blood flow, typically resulting 
    from hepatic fibrosis, cirrhosis, or sinusoidal compression. In the context of HCC, portal 
    hypertension indicates underlying liver disease that significantly increases surgical risk 
    through multiple mechanisms including impaired hepatic synthetic function, compromised 
    regenerative capacity, increased bleeding risk, and susceptibility to post-operative 
    complications.
    
    Extension of Hepatectomy Assessment:
    The planned extent of hepatic resection significantly influences decompensation risk 
    (odds ratio 2.41, 95% CI 1.17-4.30) by determining the volume of functional liver 
    parenchyma that will be removed and the regenerative demands placed on the remnant liver.
    
    Major Hepatectomy Definition:
    - Removal of three or more adjacent hepatic segments (Couinaud classification)
    - Examples include right hepatectomy (segments V, VI, VII, VIII), left hepatectomy 
      (segments II, III, IV), right trisectionectomy (segments IV-VIII), or left 
      trisectionectomy (segments II-IV + V/VI)
    - Associated with removal of >50% of liver volume in most cases
    - Requires substantial hepatic regenerative capacity for successful recovery
    
    Minor Hepatectomy Definition:
    - Removal of fewer than three hepatic segments
    - Examples include segmentectomy, bisegmentectomy, or wedge resection
    - Preserves majority of functional hepatic mass (typically >70-80%)
    - Generally associated with lower physiologic stress and decompensation risk
    
    MELD Score Assessment:
    The Model for End-Stage Liver Disease (MELD) score provides additional risk stratification 
    (odds ratio 2.26, 95% CI 1.10-4.58) particularly in patients without portal hypertension 
    undergoing minor resections. The MELD score integrates multiple markers of liver and 
    kidney function to provide objective assessment of disease severity.
    
    MELD Score Calculation and Interpretation:
    MELD = 3.8[ln(total bilirubin mg/dL)] + 11.2[ln(INR)] + 9.6[ln(creatinine mg/dL)] + 6.4
    
    Critical Threshold: MELD >9 identifies patients at increased decompensation risk even 
    in the absence of portal hypertension when undergoing minor resections.
    
    Laboratory Components and Clinical Significance:
    - Total Bilirubin: Reflects hepatocellular function and bile excretion capacity
    - INR (International Normalized Ratio): Measures hepatic synthetic function via 
      coagulation factor production
    - Serum Creatinine: Indicates renal function and potential hepatorenal syndrome
    
    Clinical Decision-Making Framework:
    
    Risk Stratification Logic:
    The model uses hierarchical interaction of risk factors to classify patients:
    
    Low Risk (4.9% decompensation rate):
    - No portal hypertension + Minor resection + MELD ≤9
    - Expected outcomes: 7-day median length of stay, 4.4% mortality rate
    - Management: Standard surgical care with routine monitoring
    
    Intermediate Risk (28.6% decompensation rate):
    - No portal hypertension + Major resection, OR
    - Minor resection + (Portal hypertension OR MELD >9)
    - Expected outcomes: 8-day median length of stay, 9.0% mortality rate
    - Management: Enhanced monitoring, potential ICU admission
    
    High Risk (60.0% decompensation rate):
    - Major resection + Portal hypertension
    - Expected outcomes: 11-day median length of stay, 25.0% mortality rate
    - Management: Consider alternative treatments, mandatory intensive care if surgery proceeds
    
    Quality Assurance Considerations:
    - Ensure accurate assessment of esophageal varices through experienced endoscopist
    - Verify platelet count and spleen size measurements on recent imaging
    - Use fresh laboratory values (within 2 weeks) for MELD calculation
    - Consider institutional laboratory reference ranges and analytical methods
    - Document clinical reasoning for surgical decision-making
    
    Alternative Treatment Considerations:
    High-risk patients should be evaluated for liver transplantation when appropriate, 
    ablative therapies (radiofrequency ablation, microwave ablation), transarterial 
    chemoembolization (TACE), or systemic therapies depending on tumor characteristics, 
    patient performance status, and institutional expertise.
    
    References (Vancouver style):
    1. Cescon M, Colecchia A, Cucchetti A, Peri E, Montrone L, Berretta M, et al. 
    Value of transient elastography measured with FibroScan in predicting the outcome 
    of hepatic resection for hepatocellular carcinoma. Ann Surg. 2012 Nov;256(5):706-12.
    2. Cucchetti A, Ercolani G, Vivarelli M, Cescon M, Ravaioli M, La Barba G, et al. 
    Impact of model for end-stage liver disease (MELD) score on prognosis after 
    hepatectomy for hepatocellular carcinoma on cirrhosis. Liver Transpl. 2006 Jun;12(6):966-71.
    """
    
    portal_hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Presence of portal hypertension defined as F1 or greater esophageal varices on upper "
                   "endoscopy OR platelet count <100,000/μL with splenomegaly. Portal hypertension is the "
                   "most significant predictor of post-operative liver decompensation (OR 2.99) and indicates "
                   "advanced liver disease with compromised hepatic reserve. Clinical assessment should include "
                   "upper endoscopy, complete blood count, and abdominal imaging. Supporting findings may "
                   "include ascites, abdominal collaterals, or hepatic venous pressure gradient ≥10 mmHg.",
        example="no"
    )
    
    hepatectomy_extent: Literal["minor", "major"] = Field(
        ...,
        description="Planned extent of hepatic resection significantly influences decompensation risk (OR 2.41). "
                   "Major hepatectomy is defined as removal of ≥3 adjacent hepatic segments (e.g., right "
                   "hepatectomy, left hepatectomy, trisectionectomy) and typically involves >50% liver volume "
                   "removal, requiring substantial regenerative capacity. Minor hepatectomy involves <3 segments "
                   "(segmentectomy, bisegmentectomy, wedge resection) and preserves majority of functional "
                   "hepatic mass, generally associated with lower physiologic stress and decompensation risk.",
        example="minor"
    )
    
    meld_score_category: Optional[Literal["9_or_less", "greater_than_9"]] = Field(
        None,
        description="MELD score category (only required when portal hypertension is absent and minor hepatectomy "
                   "is planned). MELD >9 identifies increased decompensation risk (OR 2.26) even in low-risk "
                   "patients. MELD score integrates total bilirubin, INR, and creatinine to assess liver and "
                   "kidney function severity. Formula: 3.8[ln(bilirubin)] + 11.2[ln(INR)] + 9.6[ln(creatinine)] + 6.4. "
                   "Use recent laboratory values (within 2 weeks) for accurate calculation. This parameter "
                   "provides additional risk stratification in patients who otherwise appear low-risk.",
        example="9_or_less"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "portal_hypertension": "no",
                "hepatectomy_extent": "minor",
                "meld_score_category": "9_or_less"
            }
        }


class LiverDecompensationRiskHccResponse(BaseModel):
    """
    Response model for Liver Decompensation Risk after Hepatectomy for HCC
    
    Provides calculated decompensation risk percentage with comprehensive clinical interpretation 
    and evidence-based management recommendations for patients with hepatocellular carcinoma 
    undergoing hepatic resection. The response stratifies patients into risk categories enabling 
    informed surgical decision-making, perioperative planning, and alternative treatment 
    considerations.
    
    Risk Categories and Clinical Implications:
    
    Low Risk Category (4.9% Decompensation Rate):
    - Patient Profile: No portal hypertension, minor resection, MELD score ≤9
    - Clinical Outcomes: Median 7-day hospitalization, 4.4% liver-related mortality
    - Management Strategy: Standard surgical care with routine postoperative monitoring
    - Prognosis: Excellent with minimal perioperative risk and low complication rates
    - Surveillance: Standard hepatology follow-up for HCC recurrence and liver function
    
    Intermediate Risk Category (28.6% Decompensation Rate):
    - Patient Profile: Mixed risk factors including major resection without portal hypertension 
      or minor resection with portal hypertension/elevated MELD
    - Clinical Outcomes: Median 8-day hospitalization, 9.0% liver-related mortality
    - Management Strategy: Enhanced perioperative monitoring, potential ICU admission
    - Surveillance: Close monitoring of liver function, coagulation parameters, clinical status
    - Coordination: Multidisciplinary team involvement with hepatology consultation
    
    High Risk Category (60.0% Decompensation Rate):
    - Patient Profile: Major resection in presence of portal hypertension
    - Clinical Outcomes: Median 11-day hospitalization, 25.0% liver-related mortality
    - Management Strategy: Careful surgical candidacy review, mandatory ICU admission
    - Alternative Considerations: Liver transplantation, ablation, TACE evaluation
    - Risk Communication: Detailed informed consent regarding significant morbidity/mortality
    
    Clinical Management Framework:
    
    Preoperative Optimization:
    - Nutritional assessment and optimization in malnourished patients
    - Management of portal hypertension complications (varices, ascites)
    - Optimization of liver function and treatment of reversible factors
    - Multidisciplinary evaluation including hepatology, anesthesia, and surgery
    
    Perioperative Monitoring:
    - Serial liver function tests (ALT, AST, bilirubin, albumin, PT/INR)
    - Comprehensive metabolic panel with attention to renal function
    - Clinical assessment for signs of hepatic decompensation
    - Early recognition and management of complications
    
    Post-operative Care Considerations:
    - Risk-stratified monitoring protocols based on calculated decompensation risk
    - Enhanced surveillance for intermediate and high-risk patients
    - Early hepatology consultation for concerning laboratory trends
    - Aggressive management of complications including bleeding, infection, and organ failure
    
    Alternative Treatment Decision-Making:
    
    Liver Transplantation Evaluation:
    High-risk patients within Milan criteria should be considered for liver transplantation 
    evaluation, which may provide both oncologic cure and definitive treatment of underlying 
    liver disease. Early transplant evaluation is essential given organ allocation timelines 
    and disease progression potential.
    
    Ablative Therapies:
    Radiofrequency ablation or microwave ablation may be appropriate for small tumors in 
    high-risk patients, offering local tumor control with minimal impact on liver function. 
    These treatments are particularly suitable for tumors <3 cm in favorable locations.
    
    Transarterial Treatments:
    Transarterial chemoembolization (TACE) or transarterial radioembolization (TARE) may 
    provide tumor control and potential downstaging in patients unsuitable for resection. 
    These treatments preserve liver parenchyma while delivering targeted therapy.
    
    Quality Assurance and Implementation:
    
    Risk Communication:
    - Use calculator results to facilitate informed consent discussions
    - Provide quantitative risk estimates for patient and family counseling
    - Document risk assessment rationale in medical record
    - Ensure patient understanding of treatment alternatives and expected outcomes
    
    Institutional Quality Improvement:
    - Track risk-adjusted outcomes to monitor institutional performance
    - Use risk stratification for quality improvement initiatives
    - Benchmark results against expected outcomes based on patient case mix
    - Identify opportunities for enhanced perioperative care protocols
    
    Research Applications:
    - Risk stratification for clinical trial enrollment and outcome analysis
    - Comparative effectiveness research between treatment modalities
    - Development of enhanced risk prediction models with additional variables
    - Long-term oncologic outcome correlation with perioperative risk factors
    
    The Liver Decompensation Risk calculator represents a significant advancement in evidence-based 
    surgical decision-making for patients with hepatocellular carcinoma. By providing objective, 
    validated risk estimates, this tool enhances communication quality, optimizes patient selection, 
    and enables individualized perioperative management strategies that improve patient safety and 
    outcomes in hepatic surgery.
    
    Reference: Cescon M, et al. Ann Surg. 2012;256(5):706-12.
    """
    
    result: float = Field(
        ...,
        description="Liver decompensation rate percentage calculated from clinical risk factors",
        example=4.9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the decompensation rate",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk classification, expected outcomes, "
                   "and evidence-based management recommendations for hepatic resection planning",
        example="Low Risk Classification: 4.9% liver decompensation rate. Clinical parameters: no portal hypertension, minor hepatectomy, MELD score ≤9. Expected outcomes: median length of stay 7 days, liver-related mortality risk 4.4%. Management: These patients represent the optimal candidates for hepatectomy with minimal perioperative risk. Standard surgical care with routine postoperative monitoring. Excellent prognosis with low complication rates. Continue standard hepatology follow-up for HCC surveillance and liver function monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk of liver decompensation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4.9,
                "unit": "%",
                "interpretation": "Low Risk Classification: 4.9% liver decompensation rate. Clinical parameters: no portal hypertension, minor hepatectomy, MELD score ≤9. Expected outcomes: median length of stay 7 days, liver-related mortality risk 4.4%. Management: These patients represent the optimal candidates for hepatectomy with minimal perioperative risk. Standard surgical care with routine postoperative monitoring. Excellent prognosis with low complication rates. Continue standard hepatology follow-up for HCC surveillance and liver function monitoring.",
                "stage": "Low Risk",
                "stage_description": "Low risk of liver decompensation"
            }
        }