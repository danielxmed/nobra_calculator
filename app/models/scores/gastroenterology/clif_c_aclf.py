"""
CLIF-C ACLF (Acute-on-Chronic Liver Failure) Models

Request and response models for CLIF-C ACLF mortality prediction calculation.

References (Vancouver style):
1. Jalan R, Saliba F, Pavesi M, Amoros A, Moreau R, Ginès P, Levesque E, Durand F, 
   Angeli P, Caraceni P, Hopf C, Alessandria C, Rodriguez E, Solis-Muñoz P, Laleman W, 
   Trebicka J, Zeuzem S, Gustot T, Mookerjee R, Elkrief L, Soriano G, Cordoba J, 
   Morando F, Gerbes A, Agarwal B, Samuel D, Bernardi M, Arroyo V; CANONIC study 
   investigators of the EASL-Clif Consortium. Development and validation of a 
   prognostic score to predict mortality in patients with acute-on-chronic liver 
   failure. J Hepatol. 2014;61(5):1038-47.
2. Moreau R, Jalan R, Gines P, Pavesi M, Angeli P, Cordoba J, Durand F, Gustot T, 
   Saliba F, Domenicali M, Gerbes A, Wendon J, Alessandria C, Laleman W, Zeuzem S, 
   Trebicka J, Bernardi M, Arroyo V; CANONIC Study Investigators of the EASL-Clif 
   Consortium. Acute-on-chronic liver failure is a distinct syndrome that develops 
   in patients with acute decompensation of cirrhosis. Gastroenterology. 2013;144(7):1426-37.

The CLIF-C ACLF (Acute-on-Chronic Liver Failure) score is a validated prognostic 
tool specifically designed to predict mortality in patients with acute-on-chronic 
liver failure (ACLF). This calculator represents a significant advancement in the 
management of critically ill patients with liver disease, providing superior 
mortality prediction compared to traditional scores such as MELD, MELD-Na, and 
Child-Pugh in the ACLF population.

Clinical Background and Development:

Acute-on-chronic liver failure (ACLF) is a distinct clinical syndrome characterized 
by acute deterioration of liver function in patients with pre-existing chronic 
liver disease, leading to organ failure and high short-term mortality. The 
condition affects approximately 30-50% of patients hospitalized with acute 
decompensation of cirrhosis and carries a global mortality rate ranging from 
30% to 50%.

The CLIF-C ACLF score was developed and validated through the CANONIC study 
(EASL-CLIF Acute-on-Chronic Liver Failure in Cirrhosis), a prospective 
observational study conducted by the European Association for the Study of 
Liver-Chronic Liver Failure (EASL-CLIF) consortium. This multicenter study 
included 1,343 patients with acute decompensation of cirrhosis from 29 liver 
units across Europe.

Scoring System Architecture:

The CLIF-C ACLF score integrates multiple physiological and biochemical parameters 
through a sophisticated mathematical model:

CLIF-C ACLF Score = 10 × [0.33 × CLIF-C OF Score + 0.04 × age + 0.63 × ln(WBC count) - 2]

The formula incorporates three key components:

1. CLIF-C Organ Failure (OF) Score:
   This component evaluates dysfunction across six organ systems, each scored 
   from 1-3 points based on severity:
   
   - Liver: Assessed by total bilirubin levels (1-3 points)
   - Kidney: Evaluated by serum creatinine or renal replacement therapy (1-3 points)
   - Brain: Determined by hepatic encephalopathy grade (1-3 points)
   - Coagulation: Measured by international normalized ratio (INR) (1-3 points)
   - Circulatory: Assessed by mean arterial pressure and vasopressor use (1-3 points)
   - Respiratory: Evaluated by PaO2/FiO2 or SpO2/FiO2 ratios (1-3 points)

2. Age Component:
   Patient age contributes directly to mortality risk, reflecting the decreased 
   physiological reserve and reduced regenerative capacity in older patients.

3. Inflammatory Marker:
   White blood cell count (as natural logarithm) serves as a marker of systemic 
   inflammatory response, which is closely associated with ACLF severity and 
   prognosis.

Clinical Performance and Validation:

The CLIF-C ACLF score demonstrates superior predictive accuracy compared to 
existing prognostic models:

- Area Under the Receiver Operating Characteristic (AUROC) for 28-day mortality: 0.8
- CLIF-C OF alone: AUROC 0.75
- MELD score: AUROC 0.68
- Child-Pugh score: AUROC 0.66

Critical Prognostic Thresholds:

The score provides several clinically meaningful cut-points for risk stratification:

- Score ≥70: Associated with 100% mortality at 28 days
- Score ≥65 at 3-7 days after ACLF diagnosis: Indicates 100% mortality rate
- These thresholds have been validated across multiple cohorts and geographic regions

Risk Stratification and Clinical Applications:

Low Risk (Score <45):
- Lower mortality risk with standard supportive care
- Focus on optimizing liver function and addressing precipitating factors
- Regular monitoring for progression to higher ACLF grades
- Consider hepatology consultation for specialized management

Moderate Risk (Score 45-64):
- Significant mortality risk requiring intensive monitoring
- Liver transplantation evaluation should be considered
- Intensive care or high-dependency unit monitoring recommended
- Optimize management of individual organ failures

High Risk (Score 65-69):
- Very high mortality risk requiring urgent intervention
- Urgent liver transplantation evaluation if eligible
- Intensive care unit management required
- Consider experimental therapies or clinical trials

Critical Risk (Score ≥70):
- Associated with 100% mortality at 28 days
- Consider futility of intensive care interventions
- Focus on comfort care and family discussions
- Transition to palliative care approach

Clinical Decision-Making Applications:

Intensive Care Admission:
The score helps guide decisions regarding ICU admission by identifying patients 
most likely to benefit from intensive interventions versus those with futile prognosis.

Liver Transplantation Evaluation:
Risk stratification assists in prioritizing patients for transplantation evaluation 
and determining urgency of listing, while identifying those with prohibitively 
high mortality risk.

Resource Allocation:
The score supports equitable allocation of limited healthcare resources by 
identifying patients with the greatest potential for benefit from intensive care.

Treatment Intensity:
Risk categories guide the appropriateness of aggressive interventions, including 
liver support devices, experimental therapies, and invasive procedures.

Family Communication:
Objective risk assessment facilitates difficult conversations with families 
regarding prognosis and goals of care.

Implementation Considerations:

Timing of Assessment:
- Calculate score at ACLF diagnosis
- Re-assess at 3-7 days to identify patients with persistently high scores
- Monitor trends in score over time as clinical status evolves
- Use score changes to guide treatment modifications

Integration with Clinical Judgment:
While the CLIF-C ACLF score provides valuable prognostic information, it should 
supplement rather than replace clinical judgment. Factors not captured by the 
score may influence individual patient outcomes.

Patient Population:
The score was specifically developed and validated in patients with ACLF, defined 
by specific organ failure criteria. Its applicability to other populations with 
liver disease may be limited.

Dynamic Assessment:
ACLF is a dynamic syndrome with potential for both improvement and deterioration. 
Regular reassessment is essential to guide ongoing management decisions.

Quality Assurance and Standardization:

Accurate Data Collection:
Ensure precise measurement and documentation of all score components, particularly 
laboratory values and clinical assessments like hepatic encephalopathy grading.

Staff Training:
Healthcare providers should be trained in proper score calculation and 
interpretation to ensure consistent application across care teams.

Documentation Standards:
Maintain clear documentation of score calculations, timing of assessments, and 
clinical decisions based on risk stratification.

Limitations and Considerations:

The CLIF-C ACLF score has several important limitations:

- Developed primarily in European populations; generalizability to other 
  ethnic groups requires validation
- Does not account for treatment response or potential for recovery
- Static assessment may not capture dynamic changes in clinical status
- Does not incorporate psychosocial factors that may influence treatment decisions

Future Directions:

Ongoing research continues to refine the application of CLIF-C ACLF scoring:

- Development of dynamic scoring models that incorporate treatment response
- Integration with biomarkers and novel prognostic indicators
- Validation in diverse global populations
- Assessment of score performance with emerging therapies

The CLIF-C ACLF score represents a crucial advancement in the management of 
patients with acute-on-chronic liver failure, providing evidence-based risk 
stratification that guides clinical decision-making and improves patient care. 
When properly implemented with appropriate clinical context and regular 
reassessment, this tool significantly enhances prognostic accuracy and 
treatment optimization in this challenging patient population.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class ClifCAclfRequest(BaseModel):
    """
    Request model for CLIF-C ACLF (Acute-on-Chronic Liver Failure) Score
    
    The CLIF-C ACLF score is specifically designed for patients with acute-on-chronic 
    liver failure (ACLF) to predict mortality risk and guide clinical decision-making. 
    This calculator integrates organ failure assessment, patient demographics, and 
    inflammatory markers to provide superior prognostic accuracy compared to 
    traditional liver disease scoring systems.
    
    Assessment Parameter Guidelines:
    
    Patient Demographics:
    Age in years - Older age contributes to increased mortality risk, reflecting 
    decreased physiological reserve and reduced regenerative capacity in liver failure.
    
    Inflammatory Marker:
    White Blood Cell Count (×10⁹ cells/L) - Serves as a marker of systemic inflammatory 
    response, which correlates strongly with ACLF severity and prognosis. Elevated 
    WBC counts indicate more severe inflammatory states and worse outcomes.
    
    CLIF-C Organ Failure Assessment Components:
    
    1. Liver Function (Total Bilirubin):
    - <6 mg/dL: Normal to mild dysfunction (1 point)
    - 6 to <12 mg/dL: Moderate dysfunction (2 points)
    - ≥12 mg/dL: Severe dysfunction (3 points)
    
    Clinical Significance: Bilirubin elevation reflects both hepatocellular dysfunction 
    and cholestasis. Levels ≥12 mg/dL indicate severe liver dysfunction associated 
    with poor prognosis.
    
    2. Kidney Function (Serum Creatinine/Renal Replacement Therapy):
    - <2 mg/dL: Normal to mild dysfunction (1 point)
    - 2 to <3.5 mg/dL: Moderate dysfunction (2 points)
    - ≥3.5 mg/dL or any renal replacement therapy: Severe dysfunction (3 points)
    
    Clinical Significance: Renal dysfunction in ACLF may result from hepatorenal 
    syndrome, drug toxicity, or multi-organ failure. Need for RRT indicates 
    severe dysfunction regardless of creatinine level.
    
    3. Brain Function (Hepatic Encephalopathy):
    - Grade 0: No encephalopathy (1 point)
    - Grades 1-2: Mild to moderate encephalopathy (2 points)
    - Grades 3-4: Severe encephalopathy (3 points)
    
    Clinical Significance: Hepatic encephalopathy reflects the brain's response to 
    liver dysfunction and toxin accumulation. Grades 3-4 indicate severe 
    neurological compromise with coma or stupor.
    
    4. Coagulation Function (International Normalized Ratio):
    - <2.0: Normal to mild dysfunction (1 point)
    - 2.0 to <2.5: Moderate dysfunction (2 points)
    - ≥2.5: Severe dysfunction (3 points)
    
    Clinical Significance: INR elevation reflects decreased synthetic function and 
    increased bleeding risk. Values ≥2.5 indicate severe coagulopathy requiring 
    careful management of invasive procedures.
    
    5. Circulatory Function (Mean Arterial Pressure/Vasopressors):
    - MAP ≥70 mmHg without vasopressors: Normal (1 point)
    - MAP <70 mmHg without vasopressors: Moderate dysfunction (2 points)
    - Any MAP with vasopressor requirement: Severe dysfunction (3 points)
    
    Clinical Significance: Circulatory dysfunction indicates hemodynamic instability 
    and shock. Vasopressor requirement represents severe dysfunction regardless 
    of achieved blood pressure.
    
    6. Respiratory Function (Oxygenation Ratios):
    PaO2/FiO2 Ratio:
    - >300: Normal oxygenation (1 point)
    - 200-300: Moderate dysfunction (2 points)
    - ≤200: Severe dysfunction (3 points)
    
    SpO2/FiO2 Ratio (when arterial blood gas unavailable):
    - >357: Normal oxygenation (1 point)
    - 214-357: Moderate dysfunction (2 points)
    - ≤214: Severe dysfunction (3 points)
    
    Clinical Significance: Respiratory dysfunction may result from hepatopulmonary 
    syndrome, fluid overload, or ARDS. Severe dysfunction indicates need for 
    mechanical ventilation.
    
    Clinical Assessment Context:
    
    Timing of Assessment:
    - Perform assessment at time of ACLF diagnosis
    - Reassess at 3-7 days to identify persistent high-risk patients
    - Monitor score trends over time to guide treatment modifications
    - Use for objective prognostic discussions with patients and families
    
    Prerequisites for Use:
    - Confirmed diagnosis of acute-on-chronic liver failure
    - Available laboratory and clinical data for all six organ systems
    - Understanding that score is specific to ACLF population
    - Recognition that clinical judgment should supplement score interpretation
    
    Integration with Care Planning:
    - Use for ICU admission decisions and resource allocation
    - Guide liver transplantation evaluation timing and urgency
    - Support decisions regarding treatment intensity and goals of care
    - Facilitate family discussions regarding prognosis and expectations
    
    References (Vancouver style):
    1. Jalan R, Saliba F, Pavesi M, Amoros A, Moreau R, Ginès P, Levesque E, Durand F, 
    Angeli P, Caraceni P, Hopf C, Alessandria C, Rodriguez E, Solis-Muñoz P, Laleman W, 
    Trebicka J, Zeuzem S, Gustot T, Mookerjee R, Elkrief L, Soriano G, Cordoba J, 
    Morando F, Gerbes A, Agarwal B, Samuel D, Bernardi M, Arroyo V; CANONIC study 
    investigators of the EASL-Clif Consortium. Development and validation of a 
    prognostic score to predict mortality in patients with acute-on-chronic liver 
    failure. J Hepatol. 2014;61(5):1038-47.
    2. Moreau R, Jalan R, Gines P, Pavesi M, Angeli P, Cordoba J, Durand F, Gustot T, 
    Saliba F, Domenicali M, Gerbes A, Wendon J, Alessandria C, Laleman W, Zeuzem S, 
    Trebicka J, Bernardi M, Arroyo V; CANONIC Study Investigators of the EASL-Clif 
    Consortium. Acute-on-chronic liver failure is a distinct syndrome that develops 
    in patients with acute decompensation of cirrhosis. Gastroenterology. 2013;144(7):1426-37.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=100,
        description="Patient age in years. Older age increases mortality risk due to decreased physiological reserve",
        example=65
    )
    
    white_blood_cell_count: float = Field(
        ...,
        ge=0.1,
        le=100.0,
        description="White blood cell count (×10⁹ cells/L). Marker of systemic inflammatory response associated with ACLF severity",
        example=12.5
    )
    
    bilirubin: float = Field(
        ...,
        ge=0.1,
        le=50.0,
        description="Total bilirubin (mg/dL). <6=1pt, 6-12=2pts, ≥12=3pts. Reflects hepatocellular dysfunction and cholestasis",
        example=8.2
    )
    
    creatinine: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="Serum creatinine (mg/dL). <2=1pt, 2-3.5=2pts, ≥3.5=3pts. Indicates renal dysfunction severity",
        example=1.8
    )
    
    renal_replacement_therapy: Literal["yes", "no"] = Field(
        ...,
        description="Patient on renal replacement therapy (hemodialysis, CRRT, etc.). RRT use = 3 points regardless of creatinine level",
        example="no"
    )
    
    hepatic_encephalopathy_grade: Literal["grade_0", "grade_1_2", "grade_3_4"] = Field(
        ...,
        description="Hepatic encephalopathy grade. Grade 0=1pt, Grades 1-2=2pts, Grades 3-4=3pts. Reflects neurological dysfunction severity",
        example="grade_1_2"
    )
    
    inr: float = Field(
        ...,
        ge=0.5,
        le=10.0,
        description="International normalized ratio. <2.0=1pt, 2.0-2.5=2pts, ≥2.5=3pts. Indicates coagulopathy and bleeding risk",
        example=2.2
    )
    
    mean_arterial_pressure: float = Field(
        ...,
        ge=30.0,
        le=150.0,
        description="Mean arterial pressure (mmHg). Used with vasopressor status to assess circulatory function",
        example=68
    )
    
    vasopressors: Literal["yes", "no"] = Field(
        ...,
        description="Patient on vasopressors (norepinephrine, epinephrine, etc.). Vasopressor use = 3 points regardless of MAP",
        example="no"
    )
    
    respiratory_ratio_type: Literal["pao2_fio2", "spo2_fio2"] = Field(
        ...,
        description="Type of respiratory ratio available. PaO2/FiO2 preferred when arterial blood gas available",
        example="pao2_fio2"
    )
    
    respiratory_ratio_value: float = Field(
        ...,
        ge=50.0,
        le=600.0,
        description="PaO2/FiO2 (>300=1pt, 200-300=2pts, ≤200=3pts) or SpO2/FiO2 ratio (>357=1pt, 214-357=2pts, ≤214=3pts)",
        example=280
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "white_blood_cell_count": 12.5,
                "bilirubin": 8.2,
                "creatinine": 1.8,
                "renal_replacement_therapy": "no",
                "hepatic_encephalopathy_grade": "grade_1_2",
                "inr": 2.2,
                "mean_arterial_pressure": 68,
                "vasopressors": "no",
                "respiratory_ratio_type": "pao2_fio2",
                "respiratory_ratio_value": 280
            }
        }


class ClifCAclfResponse(BaseModel):
    """
    Response model for CLIF-C ACLF (Acute-on-Chronic Liver Failure) Score
    
    Provides comprehensive mortality risk assessment for patients with acute-on-chronic 
    liver failure based on the validated CLIF-C ACLF scoring system. The response 
    includes detailed prognostic information, risk stratification, and evidence-based 
    clinical guidance to support optimal patient management and family communication.
    
    Score Interpretation and Risk Stratification:
    
    Low Risk (Score <45 points):
    
    Clinical Characteristics:
    - Lower short-term mortality risk in ACLF population
    - Potential for stabilization with appropriate supportive care
    - Organ failures may be limited in number or severity
    - Better preserved physiological reserve
    
    Management Approach:
    - Standard hepatology care with close monitoring
    - Focus on identifying and treating precipitating factors
    - Optimize management of underlying liver disease
    - Regular assessment for progression to higher risk categories
    - Consider hepatology consultation for specialized management
    
    Prognosis:
    - 28-day mortality: <30%
    - Potential for clinical improvement with appropriate intervention
    - Monitor for ACLF progression or resolution
    
    Moderate Risk (Score 45-64 points):
    
    Clinical Characteristics:
    - Significant mortality risk requiring intensive monitoring
    - Multiple organ systems involved or moderate severity dysfunction
    - Substantial physiological stress and organ failure burden
    - Need for advanced supportive care measures
    
    Management Approach:
    - Intensive care or high-dependency unit monitoring
    - Liver transplantation evaluation should be initiated
    - Optimize management of individual organ failures
    - Consider liver support devices if available
    - Frequent reassessment of clinical status and score trends
    
    Prognosis:
    - 28-day mortality: 30-60%
    - 90-day mortality: 50-80%
    - Potential for improvement with aggressive management
    - Transplantation may offer survival benefit if eligible
    
    High Risk (Score 65-69 points):
    
    Clinical Characteristics:
    - Very high mortality risk with severe multi-organ failure
    - Limited physiological reserve and poor short-term prognosis
    - Multiple organ systems severely affected
    - High likelihood of clinical deterioration
    
    Management Approach:
    - Urgent liver transplantation evaluation if potentially eligible
    - Intensive care unit management required
    - Consider experimental therapies or clinical trial enrollment
    - Aggressive treatment of individual organ failures
    - Prepare for difficult prognostic discussions with family
    
    Prognosis:
    - 28-day mortality: >80%
    - 90-day mortality: >90%
    - Very limited potential for recovery without transplantation
    - Score ≥65 at 3-7 days indicates extremely poor prognosis
    
    Critical Risk (Score ≥70 points):
    
    Clinical Characteristics:
    - Associated with 100% mortality at 28 days based on validation studies
    - Universally fatal outcome in this risk category
    - Severe multi-organ failure with no potential for recovery
    - End-stage physiological dysfunction
    
    Management Approach:
    - Consider futility of intensive care interventions
    - Focus on comfort care and symptom management
    - Facilitate family discussions regarding goals of care
    - Transition to palliative care approach when appropriate
    - Avoid futile invasive procedures and interventions
    
    Prognosis:
    - 28-day mortality: 100% (validated in multiple studies)
    - No documented survivors in this score range
    - Universal fatal outcome regardless of interventions
    
    Clinical Decision Support Features:
    
    Intensive Care Management:
    The score provides objective criteria for ICU admission decisions, helping 
    identify patients most likely to benefit from intensive interventions while 
    recognizing those with futile prognosis.
    
    Liver Transplantation Evaluation:
    Risk stratification guides transplantation evaluation timing and urgency:
    - Moderate risk: Consider evaluation
    - High risk: Urgent evaluation required
    - Critical risk: Contraindication due to futility
    
    Resource Allocation:
    Objective risk assessment supports equitable allocation of limited healthcare 
    resources, ensuring those with greatest potential benefit receive appropriate care.
    
    Family Communication:
    The score provides evidence-based prognostic information to facilitate difficult 
    conversations regarding treatment goals, expectations, and end-of-life care planning.
    
    Treatment Intensity Guidance:
    Risk categories inform decisions regarding:
    - Appropriateness of aggressive interventions
    - Use of mechanical organ support
    - Enrollment in experimental therapies
    - Timing of comfort care transition
    
    Monitoring and Reassessment Guidelines:
    
    Timing Recommendations:
    - Initial assessment at ACLF diagnosis
    - Reassessment at 3-7 days (critical prognostic timepoint)
    - Regular monitoring for score trends and clinical evolution
    - Use score changes to guide treatment modifications
    
    Dynamic Assessment:
    ACLF is a dynamic syndrome with potential for both improvement and deterioration. 
    Regular reassessment is essential as clinical status evolves.
    
    Integration with Clinical Judgment:
    While providing valuable prognostic information, the score should supplement 
    rather than replace clinical judgment. Individual patient factors not captured 
    by the score may influence outcomes.
    
    Quality Assurance Considerations:
    
    Data Accuracy:
    Ensure precise measurement and documentation of all score components, particularly 
    laboratory values and clinical assessments requiring subjective interpretation.
    
    Staff Training:
    Healthcare teams should be trained in proper score calculation, interpretation, 
    and clinical application to ensure consistent use across providers.
    
    Documentation Standards:
    Maintain clear documentation of score calculations, assessment timing, and 
    clinical decisions based on risk stratification.
    
    The CLIF-C ACLF score represents a significant advancement in acute-on-chronic 
    liver failure management, providing superior mortality prediction compared to 
    traditional liver disease scores. When properly implemented with appropriate 
    clinical context and regular reassessment, this tool significantly enhances 
    prognostic accuracy and guides optimal treatment decisions for this challenging 
    patient population.
    
    Reference: Jalan R, et al. J Hepatol. 2014;61(5):1038-47.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="CLIF-C ACLF score (0-100 points). Higher scores indicate increased mortality risk",
        example=52.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with mortality risk assessment and treatment recommendations",
        example="CLIF-C ACLF Score 52.3: Moderate mortality risk in ACLF. Consider intensive care monitoring and advanced therapies. Evaluate for liver transplantation eligibility."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, Critical Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate mortality risk"
    )
    
    scoring_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of organ failure scores, score components, clinical guidance, and prognostic information",
        example={
            "clif_of_components": {
                "liver": {
                    "parameter": "Bilirubin",
                    "value": "8.2 mg/dL",
                    "score": 2,
                    "clinical_significance": "Reflects hepatocellular dysfunction and cholestasis"
                },
                "kidney": {
                    "parameter": "Creatinine/RRT",
                    "value": "1.8 mg/dL",
                    "score": 1,
                    "clinical_significance": "Indicates renal dysfunction and need for renal replacement"
                }
            },
            "score_summary": {
                "clif_of_score": 11,
                "final_aclf_score": 52.3,
                "risk_category": "Moderate risk"
            },
            "clinical_guidance": {
                "mortality_prediction": {
                    "28_day": "Moderate to high (30-60%)",
                    "clinical_implication": "Significant mortality risk"
                }
            }
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 52.3,
                "unit": "points",
                "interpretation": "CLIF-C ACLF Score 52.3: Moderate mortality risk in ACLF. Consider intensive care monitoring and advanced therapies. Evaluate for liver transplantation eligibility.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate mortality risk",
                "scoring_breakdown": {
                    "clif_of_components": {
                        "liver": {
                            "parameter": "Bilirubin",
                            "value": "8.2 mg/dL",
                            "score": 2,
                            "clinical_significance": "Reflects hepatocellular dysfunction and cholestasis"
                        }
                    },
                    "score_summary": {
                        "clif_of_score": 11,
                        "final_aclf_score": 52.3,
                        "risk_category": "Moderate risk"
                    }
                }
            }
        }