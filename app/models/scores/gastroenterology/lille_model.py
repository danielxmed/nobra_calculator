"""
Lille Model for Alcoholic Hepatitis Models

Request and response models for Lille Model calculation.

References (Vancouver style):
1. Louvet A, Naveau S, Abdelnour M, Ramond MJ, Diaz E, Fartoux L, et al. 
   The Lille model: a new tool for therapeutic strategy in patients with severe 
   alcoholic hepatitis treated with steroids. Hepatology. 2007 Jun;45(6):1348-54. 
   doi: 10.1002/hep.21607.
2. Mathurin P, O'Grady J, Carithers RL, Phillips M, Louvet A, Mendenhall CL, et al. 
   Corticosteroids improve short-term survival in patients with severe alcoholic 
   hepatitis: a meta-analysis of individual patient data. Gut. 2011 Feb;60(2):255-60. 
   doi: 10.1136/gut.2010.224097.
3. Dhanda AD, Collins PL, McCune CA. Is liver transplantation required after 
   severe alcoholic hepatitis? Curr Opin Crit Care. 2018 Apr;24(2):141-149. 
   doi: 10.1097/MCC.0000000000000492.

The Lille Model for Alcoholic Hepatitis is a validated prognostic tool that predicts 
mortality in patients with severe alcoholic hepatitis who are not responding adequately 
to corticosteroid therapy. This sophisticated model represents a significant advancement 
in the management of severe alcoholic hepatitis by enabling clinicians to identify 
patients early in their treatment course who are unlikely to benefit from continued 
steroid therapy and should be considered for alternative treatments or urgent liver 
transplantation evaluation.

Clinical Background:
Alcoholic hepatitis is a severe form of alcohol-related liver disease characterized by 
hepatocyte necrosis, inflammation, and fibrosis. It represents the most serious 
manifestation of alcohol-related liver disease and carries significant morbidity and 
mortality. Severe alcoholic hepatitis affects approximately 10,000-35,000 individuals 
annually in the United States, with 28-day mortality rates ranging from 15-50% depending 
on severity and response to treatment.

Corticosteroids, specifically prednisolone, have been the standard first-line therapy 
for severe alcoholic hepatitis since the 1970s. However, approximately 40% of patients 
do not respond to steroid therapy, and continuing treatment in non-responders exposes 
them to significant risks including opportunistic infections, gastrointestinal bleeding, 
and metabolic complications without providing survival benefit.

Development and Validation of the Lille Model:

The Lille Model was developed by Louvet et al. in 2007 from a multicenter cohort of 
295 patients with severe alcoholic hepatitis treated with prednisolone 40 mg daily. 
The model was designed to identify steroid non-responders early in the treatment course 
(at day 7) to guide therapeutic decision-making and avoid prolonged exposure to ineffective 
and potentially harmful therapy.

The model demonstrated exceptional discriminative ability with an area under the receiver 
operating characteristic curve (AUROC) of 0.89 ± 0.02, significantly superior to 
existing prognostic tools including Child-Pugh score (AUROC 0.62) and Maddrey 
Discriminant Function (AUROC 0.66). The model's performance has been validated in 
multiple independent cohorts across different geographic regions and healthcare systems.

Lille Model Parameters and Clinical Significance:

Age (Years):
Advanced age is associated with reduced hepatic regenerative capacity, increased 
comorbidity burden, and decreased physiological reserve. Older patients with alcoholic 
hepatitis demonstrate poorer responses to medical therapy and higher mortality rates. 
The model incorporates age as a continuous variable, reflecting the gradual decline 
in treatment responsiveness with advancing age.

Serum Albumin (Day 0, g/L):
Albumin synthesis is exclusively performed by hepatocytes and serves as a sensitive 
marker of hepatic synthetic function. In alcoholic hepatitis, hypoalbuminemia reflects 
both acute hepatocellular dysfunction and chronic liver disease progression. Lower 
albumin levels indicate more severe hepatocellular damage and reduced capacity for 
recovery. Normal serum albumin ranges from 35-50 g/L; levels below 25 g/L suggest 
severe hepatic dysfunction with poor prognosis.

Initial Bilirubin (Day 0, µmol/L):
Total bilirubin elevation in alcoholic hepatitis results from hepatocellular dysfunction, 
cholestasis, and intrahepatic bile duct obstruction from inflammatory infiltrates. 
Higher baseline bilirubin levels indicate more severe hepatocellular injury and 
dysfunction. The degree of hyperbilirubinemia correlates with disease severity and 
mortality risk. Normal total bilirubin is <21 µmol/L; levels >100 µmol/L indicate 
significant hepatocellular dysfunction.

Bilirubin at Day 7 (µmol/L):
The evolution of bilirubin levels during the initial week of steroid therapy provides 
crucial information about treatment response. Patients responding to corticosteroids 
typically demonstrate declining bilirubin levels by day 7, while non-responders show 
persistent elevation or continued rise. The bilirubin evolution (day 7 minus day 0) 
is the most dynamic component of the Lille model and provides real-time assessment 
of treatment efficacy.

Serum Creatinine (mg/dL):
Renal dysfunction in alcoholic hepatitis may result from hepatorenal syndrome, acute 
tubular necrosis, or prerenal azotemia from volume depletion. The presence of renal 
insufficiency (creatinine >1.3 mg/dL or >115 µmol/L) indicates multiorgan dysfunction 
and significantly worsens prognosis. Hepatorenal syndrome, characterized by functional 
renal failure in the absence of intrinsic kidney disease, occurs in up to 20% of 
patients with severe alcoholic hepatitis and carries extremely poor prognosis.

Prothrombin Time (Seconds):
Prothrombin time reflects hepatic synthesis of coagulation factors (II, VII, IX, X) 
and serves as a sensitive marker of hepatocellular synthetic function. Prolonged 
prothrombin time indicates impaired hepatic protein synthesis and increased bleeding 
risk. In alcoholic hepatitis, PT prolongation correlates with disease severity and 
mortality risk. Normal PT is typically 11-13 seconds; prolongation >4 seconds above 
normal indicates significant hepatic dysfunction.

Lille Model Formula and Interpretation:

The Lille Model uses the logistic regression formula:
Lille Score = exp(-R) / (1 + exp(-R))

Where R = 3.19 - 0.101×age + 0.147×albumin + 0.0165×(bilirubin_day7 - bilirubin_day0) 
          - 0.206×renal_insufficiency - 0.0065×bilirubin_day0 - 0.0096×prothrombin_time

The critical threshold of 0.45 divides patients into responders and non-responders:

Lille Score <0.45 (Responders):
- 6-month survival: 85% ± 2.5%
- Treatment recommendation: Continue corticosteroid therapy
- Clinical approach: Complete 4-week prednisolone course with gradual tapering
- Monitoring: Regular assessment of liver function, nutritional status, infection surveillance

Lille Score ≥0.45 (Non-responders):
- 6-month survival: 25% ± 3.8%
- Treatment recommendation: Discontinue corticosteroids, evaluate alternatives
- Clinical approach: Early liver transplant evaluation, supportive care
- Urgent considerations: Infection risk reduction, palliative care consultation

Clinical Decision-Making Framework:

Early Assessment Strategy:
Recent studies demonstrate that the Lille Model can be calculated at day 4 with similar 
accuracy to day 7 assessment. Early Lille Model (LM4) enables even more rapid 
identification of non-responders, reducing unnecessary steroid exposure and facilitating 
earlier intervention with alternative therapies.

Steroid Responders (Lille <0.45):
- Continue prednisolone 40 mg daily for 4 weeks followed by gradual tapering
- Provide comprehensive supportive care including nutritional optimization
- Monitor for steroid-related complications (hyperglycemia, hypertension, infection)
- Implement alcohol cessation programs and psychosocial support
- Address vitamin deficiencies (thiamine, folate, B12) and malnutrition
- Regular monitoring of liver function tests and clinical improvement

Steroid Non-responders (Lille ≥0.45):
- Discontinue corticosteroids immediately to reduce infection risk
- Initiate urgent liver transplant evaluation in appropriate candidates
- Consider alternative therapies where available (N-acetylcysteine, granulocyte colony-stimulating factor)
- Implement palliative care principles with symptom management
- Provide family counseling and advance care planning discussions
- Focus on comfort measures and quality of life optimization

Liver Transplantation Considerations:

The Lille Model plays a crucial role in liver transplant decision-making for alcoholic 
hepatitis. Traditional transplant criteria required 6 months of sobriety, but emerging 
evidence supports early transplantation for highly selected patients with steroid-refractory 
severe alcoholic hepatitis. Lille non-responders represent the highest-risk group who 
may benefit from urgent transplant evaluation.

Key transplant considerations include:
- Absence of active alcohol use with commitment to abstinence
- Adequate psychosocial support systems
- Absence of significant comorbidities precluding transplantation
- Understanding of transplant requirements and long-term commitment
- Multidisciplinary team assessment including addiction specialists

Limitations and Clinical Considerations:

Model Limitations:
- Derived from prednisolone-treated patients; applicability to other steroids uncertain
- Performance may vary in different ethnic populations or healthcare settings
- Does not account for complications such as infection or gastrointestinal bleeding
- Requires 7-day treatment period for traditional calculation

Clinical Implementation:
- Ensure accurate timing of laboratory measurements at days 0 and 7
- Consider drug interactions and adherence to steroid therapy
- Monitor for development of complications that may influence prognosis
- Integrate model results with clinical judgment and patient preferences
- Regular reassessment as clinical status evolves

Quality Improvement and Research Applications:

The Lille Model has enabled standardization of alcoholic hepatitis management and 
facilitated clinical research by providing reliable prognostic stratification. It 
serves as an endpoint in clinical trials evaluating novel therapies and has improved 
patient selection for liver transplantation studies.

Future research directions include:
- Development of earlier prediction models (day 3-4)
- Integration with novel biomarkers and imaging findings
- Validation in specific patient populations (women, elderly, comorbid conditions)
- Cost-effectiveness analyses of Lille-guided treatment strategies
- Long-term outcomes assessment beyond 6 months

The Lille Model represents a paradigm shift in alcoholic hepatitis management by 
providing objective, evidence-based guidance for treatment decisions. Its integration 
into clinical practice has improved patient outcomes by facilitating early identification 
of treatment failures and enabling more rational therapeutic approaches in this 
challenging clinical condition.
"""

from pydantic import BaseModel, Field


class LilleModelRequest(BaseModel):
    """
    Request model for Lille Model for Alcoholic Hepatitis
    
    The Lille Model for Alcoholic Hepatitis is a validated prognostic tool that predicts 
    mortality in patients with severe alcoholic hepatitis undergoing corticosteroid therapy. 
    This evidence-based model enables clinicians to identify steroid non-responders early 
    in the treatment course (at day 7), facilitating critical decisions about continuing 
    therapy versus pursuing alternative treatments including liver transplantation.
    
    Clinical Assessment Parameters:
    
    Patient Age:
    Age represents a crucial prognostic factor in alcoholic hepatitis, reflecting diminished 
    hepatic regenerative capacity, increased comorbidity burden, and reduced physiological 
    reserve in older patients. Advanced age is associated with poorer response to medical 
    therapy and higher mortality rates. The model incorporates age as a continuous variable, 
    acknowledging the gradual decline in treatment responsiveness with advancing years.
    
    Serum Albumin (Day 0):
    Albumin synthesis occurs exclusively in hepatocytes and serves as a highly sensitive 
    marker of hepatic synthetic function. In severe alcoholic hepatitis, hypoalbuminemia 
    reflects both acute hepatocellular dysfunction and underlying chronic liver disease 
    progression. Baseline albumin levels provide critical prognostic information, with 
    lower values indicating more extensive hepatocellular damage and reduced capacity 
    for recovery. Normal serum albumin ranges from 35-50 g/L; levels below 25 g/L 
    suggest severe hepatic dysfunction with poor prognosis.
    
    Total Bilirubin (Day 0):
    Baseline total bilirubin elevation in alcoholic hepatitis results from multiple 
    mechanisms including hepatocellular dysfunction, intrahepatic cholestasis, and 
    bile duct obstruction from inflammatory infiltrates. Higher initial bilirubin 
    levels indicate more severe hepatocellular injury and dysfunction. The degree 
    of hyperbilirubinemia at presentation correlates strongly with disease severity 
    and mortality risk. Normal total bilirubin is <21 µmol/L; levels >100 µmol/L 
    indicate significant hepatocellular dysfunction requiring aggressive intervention.
    
    Total Bilirubin (Day 7):
    The evolution of bilirubin levels during the initial week of corticosteroid therapy 
    provides the most dynamic and clinically relevant information about treatment response. 
    Patients responding favorably to steroids typically demonstrate declining bilirubin 
    levels by day 7, while non-responders show persistent elevation or continued rise. 
    The bilirubin change from day 0 to day 7 represents the most important predictor 
    of treatment success and forms the core dynamic component of the Lille model.
    
    Serum Creatinine:
    Renal dysfunction in severe alcoholic hepatitis may arise from multiple etiologies 
    including hepatorenal syndrome, acute tubular necrosis, or prerenal azotemia from 
    volume depletion and reduced effective circulating volume. The presence of renal 
    insufficiency (defined as creatinine >1.3 mg/dL or >115 µmol/L) indicates multiorgan 
    dysfunction and significantly worsens prognosis. Hepatorenal syndrome, characterized 
    by functional renal failure without intrinsic kidney disease, occurs in up to 20% 
    of patients with severe alcoholic hepatitis and carries extremely poor prognosis.
    
    Prothrombin Time:
    Prothrombin time reflects hepatic synthesis of vitamin K-dependent coagulation 
    factors (factors II, VII, IX, and X) and serves as a highly sensitive marker of 
    hepatocellular synthetic function. Prolonged prothrombin time indicates impaired 
    hepatic protein synthesis capacity and significantly increased bleeding risk. In 
    severe alcoholic hepatitis, PT prolongation correlates directly with disease 
    severity, treatment response, and mortality risk. Normal PT ranges from 11-13 seconds; 
    prolongation >4 seconds above institutional normal indicates significant hepatic 
    synthetic dysfunction.
    
    Clinical Application Guidelines:
    - Ensure accurate timing of laboratory measurements at days 0 and 7 of steroid therapy
    - Verify patient compliance with prednisolone 40 mg daily dosing regimen
    - Account for potential drug interactions affecting steroid metabolism or efficacy
    - Monitor for development of complications (infection, bleeding) that may influence prognosis
    - Consider early calculation at day 4 for more rapid clinical decision-making
    - Integrate model results with comprehensive clinical assessment and patient preferences
    
    Treatment Decision Framework:
    - Lille Score <0.45: Continue corticosteroids, expect 85% 6-month survival
    - Lille Score ≥0.45: Discontinue steroids, consider transplant evaluation, expect 25% 6-month survival
    - Non-responders should be evaluated for alternative therapies and urgent liver transplantation
    - Early identification reduces unnecessary steroid exposure and associated complications
    
    Quality Assurance Considerations:
    - Verify laboratory timing and accuracy of measurements
    - Ensure consistent units of measurement (g/L for albumin, µmol/L for bilirubin, mg/dL for creatinine)
    - Document clinical context including complications and concurrent medications
    - Consider institutional laboratory reference ranges and analytical methods
    - Maintain clear documentation of treatment response assessment and decision rationale
    
    References (Vancouver style):
    1. Louvet A, Naveau S, Abdelnour M, Ramond MJ, Diaz E, Fartoux L, et al. 
    The Lille model: a new tool for therapeutic strategy in patients with severe 
    alcoholic hepatitis treated with steroids. Hepatology. 2007 Jun;45(6):1348-54.
    2. Mathurin P, O'Grady J, Carithers RL, Phillips M, Louvet A, Mendenhall CL, et al. 
    Corticosteroids improve short-term survival in patients with severe alcoholic 
    hepatitis: a meta-analysis of individual patient data. Gut. 2011 Feb;60(2):255-60.
    """
    
    age_years: int = Field(
        ...,
        description="Patient age in years. Advanced age is associated with reduced hepatic regenerative "
                   "capacity, increased comorbidity burden, and decreased physiological reserve. Older "
                   "patients with alcoholic hepatitis demonstrate poorer responses to medical therapy "
                   "and higher mortality rates. The model incorporates age as a continuous variable, "
                   "reflecting the gradual decline in treatment responsiveness with advancing age. "
                   "Age >65 years is associated with particularly poor prognosis.",
        ge=18,
        le=100,
        example=52
    )
    
    albumin_day0: float = Field(
        ...,
        description="Serum albumin level at day 0 (start of steroid therapy) in g/L. Albumin synthesis "
                   "occurs exclusively in hepatocytes and serves as a sensitive marker of hepatic synthetic "
                   "function. In severe alcoholic hepatitis, hypoalbuminemia reflects both acute "
                   "hepatocellular dysfunction and chronic liver disease progression. Lower albumin levels "
                   "indicate more severe hepatocellular damage and reduced capacity for recovery. Normal "
                   "range: 35-50 g/L. Levels <25 g/L suggest severe hepatic dysfunction with poor prognosis.",
        ge=10.0,
        le=60.0,
        example=24.5
    )
    
    bilirubin_day0: float = Field(
        ...,
        description="Total bilirubin at day 0 (start of steroid therapy) in µmol/L. Bilirubin elevation "
                   "results from hepatocellular dysfunction, intrahepatic cholestasis, and bile duct "
                   "obstruction from inflammatory infiltrates. Higher baseline bilirubin levels indicate "
                   "more severe hepatocellular injury and dysfunction. The degree of hyperbilirubinemia "
                   "correlates with disease severity and mortality risk. Normal: <21 µmol/L. Levels "
                   ">100 µmol/L indicate significant hepatocellular dysfunction requiring intervention.",
        ge=50.0,
        le=1000.0,
        example=280.0
    )
    
    bilirubin_day7: float = Field(
        ...,
        description="Total bilirubin at day 7 of steroid therapy in µmol/L. The evolution of bilirubin "
                   "levels during the initial week provides crucial information about treatment response. "
                   "Patients responding to corticosteroids typically demonstrate declining bilirubin by "
                   "day 7, while non-responders show persistent elevation or continued rise. The bilirubin "
                   "evolution (day 7 minus day 0) is the most dynamic component of the Lille model, "
                   "providing real-time assessment of treatment efficacy and response prediction.",
        ge=20.0,
        le=1000.0,
        example=320.0
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine level in mg/dL. Renal dysfunction may result from hepatorenal "
                   "syndrome, acute tubular necrosis, or prerenal azotemia. The presence of renal "
                   "insufficiency (creatinine >1.3 mg/dL or >115 µmol/L) indicates multiorgan dysfunction "
                   "and significantly worsens prognosis. Hepatorenal syndrome occurs in up to 20% of "
                   "patients with severe alcoholic hepatitis and carries extremely poor prognosis. "
                   "Normal range: 0.6-1.2 mg/dL. Values >1.3 mg/dL indicate renal insufficiency.",
        ge=0.3,
        le=15.0,
        example=1.8
    )
    
    prothrombin_time: float = Field(
        ...,
        description="Prothrombin time in seconds. PT reflects hepatic synthesis of coagulation factors "
                   "(II, VII, IX, X) and serves as a sensitive marker of hepatocellular synthetic function. "
                   "Prolonged PT indicates impaired hepatic protein synthesis and increased bleeding risk. "
                   "In alcoholic hepatitis, PT prolongation correlates with disease severity and mortality "
                   "risk. Normal range: 11-13 seconds. Prolongation >4 seconds above normal indicates "
                   "significant hepatic dysfunction and poor prognosis.",
        ge=10.0,
        le=120.0,
        example=22.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_years": 52,
                "albumin_day0": 24.5,
                "bilirubin_day0": 280.0,
                "bilirubin_day7": 320.0,
                "creatinine": 1.8,
                "prothrombin_time": 22.0
            }
        }


class LilleModelResponse(BaseModel):
    """
    Response model for Lille Model for Alcoholic Hepatitis
    
    Provides calculated Lille Model score with comprehensive prognostic assessment and 
    evidence-based treatment recommendations for patients with severe alcoholic hepatitis 
    undergoing corticosteroid therapy. The response stratifies patients into responders 
    and non-responders, enabling critical decisions about treatment continuation versus 
    alternative therapeutic approaches including liver transplantation evaluation.
    
    Prognostic Categories and Clinical Implications:
    
    Steroid Responders (Lille Score <0.45):
    - 6-month survival: 85% ± 2.5%
    - Clinical significance: Good response to corticosteroid therapy
    - Treatment approach: Continue prednisolone 40 mg daily for full 4-week course
    - Management priorities: Complete steroid regimen with gradual tapering over 2-4 weeks
    - Supportive care: Nutritional optimization, vitamin supplementation (thiamine, folate, B12)
    - Monitoring requirements: Regular liver function tests, infection surveillance, steroid complications
    - Long-term care: Alcohol cessation programs, psychosocial support, liver disease management
    - Prognosis: Favorable response expected with appropriate medical management
    
    Steroid Non-responders (Lille Score ≥0.45):
    - 6-month survival: 25% ± 3.8%
    - Clinical significance: Poor response to corticosteroid therapy
    - Treatment approach: Discontinue corticosteroids immediately to reduce infection risk
    - Urgent priorities: Liver transplant evaluation in appropriate candidates
    - Alternative therapies: Consider investigational treatments where available
    - Palliative approach: Implement comfort-focused care with symptom management
    - Family involvement: Early discussions about prognosis and care preferences
    - Transplant considerations: Urgent evaluation for early liver transplantation
    
    Clinical Decision-Making Framework:
    
    Treatment Optimization for Responders:
    - Complete prednisolone course: 40 mg daily × 4 weeks followed by tapering
    - Infection prevention: Monitor for bacterial, fungal, and opportunistic infections
    - Nutritional support: High-protein diet, multivitamins, thiamine supplementation
    - Alcohol cessation: Comprehensive addiction treatment and psychosocial support
    - Complication management: Address ascites, hepatic encephalopathy, portal hypertension
    - Long-term monitoring: Regular hepatology follow-up, liver function assessment
    
    Urgent Interventions for Non-responders:
    - Immediate steroid discontinuation: Prevent further immunosuppression
    - Transplant evaluation: Urgent assessment for liver transplantation candidacy
    - Infection management: Aggressive surveillance and treatment of infections
    - Alternative therapies: Consider N-acetylcysteine, G-CSF, or experimental treatments
    - Palliative care consultation: Early involvement for symptom management
    - Family communication: Clear discussions about prognosis and treatment options
    
    Liver Transplantation Considerations:
    
    Transplant Candidacy Assessment:
    - Medical criteria: Absence of active alcohol use, commitment to abstinence
    - Psychosocial evaluation: Adequate support systems, understanding of requirements
    - Comorbidity assessment: Absence of conditions precluding transplantation
    - Multidisciplinary team: Hepatology, transplant surgery, addiction medicine, psychiatry
    - Timing considerations: Urgent evaluation given poor prognosis without intervention
    - Alternative options: Living donor transplantation for selected candidates
    
    Early Transplantation Protocol:
    - Traditional 6-month sobriety requirement may be waived for selected patients
    - Lille non-responders represent highest-priority group for urgent evaluation
    - Careful selection criteria essential to optimize outcomes and organ utilization
    - Comprehensive addiction assessment and commitment to long-term sobriety
    - Integration with addiction treatment programs and ongoing support systems
    
    Quality Assurance and Implementation:
    
    Clinical Accuracy:
    - Verify accurate timing of laboratory measurements (days 0 and 7)
    - Ensure consistent prednisolone dosing (40 mg daily) throughout assessment period
    - Account for potential drug interactions or adherence issues
    - Document clinical complications that may influence interpretation
    - Consider early calculation at day 4 for more rapid decision-making
    
    Treatment Standardization:
    - Implement standardized protocols for steroid therapy and monitoring
    - Establish clear pathways for transplant evaluation and referral
    - Coordinate multidisciplinary care teams for comprehensive management
    - Develop institutional guidelines for Lille-guided treatment decisions
    - Monitor outcomes and validate model performance in local patient population
    
    Communication and Documentation:
    - Clear documentation of Lille score calculation and interpretation
    - Transparent communication with patients and families about prognosis
    - Detailed rationale for treatment decisions based on model results
    - Coordination between hepatology, transplant, and addiction medicine teams
    - Regular reassessment as clinical status and treatment response evolve
    
    Research and Quality Improvement:
    - Track patient outcomes stratified by Lille score categories
    - Validate model performance in institutional patient cohorts
    - Contribute to research on alternative therapies for non-responders
    - Participate in multicenter studies on early liver transplantation
    - Develop quality metrics for Lille-guided care pathways
    
    The Lille Model represents a transformative tool in alcoholic hepatitis management 
    by providing objective, evidence-based guidance for critical treatment decisions. 
    Its integration into clinical practice has significantly improved patient outcomes 
    by enabling early identification of treatment failures and facilitating rational, 
    individualized therapeutic approaches in this challenging and life-threatening condition.
    
    Reference: Louvet A, et al. Hepatology. 2007;45(6):1348-54.
    """
    
    result: float = Field(
        ...,
        description="Lille Model score calculated from clinical parameters (range: 0.0-1.0)",
        example=0.6234
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the prognostic score",
        example="score"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including response classification, survival estimates, "
                   "treatment recommendations, and evidence-based management guidance for alcoholic hepatitis",
        example="Lille Model Score: 0.6234. Classification: Steroid Non-responder. The score is at or above the threshold of 0.45, indicating poor response to corticosteroid therapy with an expected 6-month survival of only 25%. Clinical parameters: bilirubin change from 280 to 320 µmol/L (+14.3%), albumin 24.5 g/L, age 52 years, renal insufficiency present, PT 22.0 seconds. Recommendations: Strongly consider discontinuing corticosteroids to avoid further immunosuppression and infection risk. Evaluate for alternative therapies and urgent liver transplant assessment. Non-responders have significantly increased mortality and should be managed with palliative care principles while pursuing definitive treatment options. Early transplant evaluation is critical as this represents the only proven life-saving intervention for steroid non-responders."
    )
    
    stage: str = Field(
        ...,
        description="Response classification (Responder or Non-responder)",
        example="Non-responder"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the response category",
        example="Poor response to steroid therapy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0.6234,
                "unit": "score",
                "interpretation": "Lille Model Score: 0.6234. Classification: Steroid Non-responder. The score is at or above the threshold of 0.45, indicating poor response to corticosteroid therapy with an expected 6-month survival of only 25%. Clinical parameters: bilirubin change from 280 to 320 µmol/L (+14.3%), albumin 24.5 g/L, age 52 years, renal insufficiency present, PT 22.0 seconds. Recommendations: Strongly consider discontinuing corticosteroids to avoid further immunosuppression and infection risk. Evaluate for alternative therapies and urgent liver transplant assessment. Non-responders have significantly increased mortality and should be managed with palliative care principles while pursuing definitive treatment options. Early transplant evaluation is critical as this represents the only proven life-saving intervention for steroid non-responders.",
                "stage": "Non-responder",
                "stage_description": "Poor response to steroid therapy"
            }
        }