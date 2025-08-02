"""
Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score Models

Request and response models for PE-SARD Score calculation.

References (Vancouver style):
1. Barrios D, Rosa-Salazar V, Morillo R, Nieto R, Fernández-Golfín C, Zamorano JL, et al. 
   An Original Risk Score to Predict Early Major Bleeding in Acute Pulmonary Embolism: 
   The Syncope, Anemia, Renal Dysfunction (PE-SARD) Bleeding Score. Chest. 2021 Sep;160(3):992-1000. 
   doi: 10.1016/j.chest.2021.04.063.
2. Lobo JL, Zorrilla V, Aizpuru F, Grau E, Jiménez D, Prandoni P, et al. 
   External validation of the PE-SARD risk score for predicting early bleeding in acute 
   pulmonary embolism in the RIETE Registry. Thromb Res. 2024 Mar;235:176-181. 
   doi: 10.1016/j.thromres.2024.01.016.
3. Yamashita Y, Morimoto T, Amano H, Takase T, Hiramori S, Kim K, et al. 
   External validation of the Pulmonary Embolism-Syncope, Anemia, and Renal Dysfunction 
   bleeding score for early major bleeding in patients with acute pulmonary embolism: 
   from the COMMAND VTE Registry-2. J Thromb Thrombolysis. 2024 Aug;58(2):357-365. 
   doi: 10.1007/s11239-024-02988-4.

The Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score is a validated 
clinical decision tool that estimates the risk of early major bleeding (within 30 days) 
in patients with acute pulmonary embolism receiving anticoagulation therapy. Developed 
by Barrios et al. in 2021, this simple 3-variable score has been externally validated 
in multiple large registries and demonstrates superior performance compared to existing 
bleeding risk scores in the PE setting.

Clinical Applications:
- Risk stratification for bleeding complications in acute PE patients
- Guiding intensity of anticoagulation monitoring and management
- Identifying patients requiring modified anticoagulation strategies
- Supporting shared decision-making in PE treatment planning
- Quality improvement initiatives for PE care pathways
- Clinical research stratification and endpoint assessment

PE-SARD Score Components:
The PE-SARD score incorporates three readily available clinical variables:

1. Syncope (1.5 points if present):
   - History of syncope at presentation or shortly before PE diagnosis
   - Indicates hemodynamic compromise and increased bleeding risk
   - May reflect more severe PE with higher treatment intensity needs

2. Anemia (2.5 points if present):
   - Defined as hemoglobin level <12 g/dL (120 g/L)
   - Highest weighted factor in the score due to strong bleeding association
   - May indicate underlying bleeding tendency or reduced hemostatic reserve
   - Most predictive single variable for early major bleeding

3. Renal Dysfunction (1.0 point if present):
   - Defined as glomerular filtration rate (GFR) <60 mL/min/1.73m²
   - Associated with impaired drug clearance and bleeding complications
   - May indicate multimorbidity and increased treatment complexity

Risk Stratification and Clinical Outcomes:
The PE-SARD score stratifies patients into three distinct risk categories:

Low Risk (0 points):
- 30-day major bleeding incidence: 0.6%
- Represents patients with excellent bleeding safety profile
- Standard anticoagulation therapy with routine monitoring appropriate
- Consider outpatient management if other clinical factors permit

Intermediate Risk (1-2.5 points):
- 30-day major bleeding incidence: 1.5%
- Represents patients requiring careful bleeding vs. thrombotic risk assessment
- May benefit from enhanced monitoring or modified anticoagulation approach
- Consider more frequent follow-up and patient education

High Risk (>2.5 points):
- 30-day major bleeding incidence: 2.5%
- Represents patients at highest bleeding risk requiring careful management
- Consider reduced-intensity anticoagulation or alternative strategies
- May benefit from specialist consultation and closer surveillance

Validation and Performance:
The PE-SARD score has been extensively validated across multiple populations:
- Original derivation study: 1,238 acute PE patients
- RIETE Registry validation: External validation in large international cohort
- COMMAND VTE Registry-2: Additional validation in Asian population
- Demonstrated superior discrimination compared to existing bleeding scores
- Consistent performance across diverse patient populations and healthcare settings
- Simple calculation enhances clinical usability and implementation

Clinical Implementation Considerations:
- Calculate for all patients with acute PE receiving anticoagulation
- Use in conjunction with thrombotic risk assessment tools
- Consider patient-specific factors not captured in the score
- Results should supplement, not replace, clinical judgment
- Document rationale for decisions that deviate from score recommendations
- Reassess if clinical condition or bleeding risk factors change
- Integrate into clinical decision support systems and care pathways

Limitations and Important Notes:
- Score validated for 30-day early bleeding risk, not long-term outcomes
- Does not capture all potential bleeding risk factors
- Social factors and anticoagulation adherence not incorporated
- Requires clinical judgment for final treatment decisions
- May not apply to patients with contraindications to anticoagulation
- Performance may vary in populations not represented in validation studies

The PE-SARD score represents a significant advance in bleeding risk assessment for acute 
PE patients, providing evidence-based risk stratification that can guide clinical 
decision-making and improve patient safety while maintaining therapeutic efficacy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class PeSardScoreRequest(BaseModel):
    """
    Request model for Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score
    
    The PE-SARD score uses three simple clinical variables to assess 30-day major bleeding 
    risk in patients with acute pulmonary embolism receiving anticoagulation therapy. This 
    validated tool helps clinicians make informed decisions about treatment intensity and 
    monitoring strategies.
    
    Clinical Variable Assessment:
    
    1. Syncope Assessment:
       - Document any syncopal episodes at presentation or shortly before PE diagnosis
       - Includes witnessed loss of consciousness with spontaneous recovery
       - May indicate hemodynamic compromise and increased treatment complexity
       - Consider relationship to PE severity and right heart dysfunction
    
    2. Anemia Evaluation:
       - Use most recent hemoglobin level prior to anticoagulation initiation
       - Threshold: <12 g/dL (120 g/L) regardless of sex
       - Consider underlying causes: chronic disease, occult bleeding, malnutrition
       - Most predictive single variable for early major bleeding risk
    
    3. Renal Function Assessment:
       - Use estimated glomerular filtration rate (eGFR) calculation
       - Threshold: <60 mL/min/1.73m² using CKD-EPI or similar equation
       - Consider impact on anticoagulant clearance and dosing requirements
       - May indicate multimorbidity affecting bleeding risk
    
    Clinical Context and Timing:
    - Assess variables at time of acute PE diagnosis
    - Use baseline values before anticoagulation therapy initiation
    - Consider recent changes in clinical status that may affect risk
    - Document any temporary factors that may influence bleeding risk
    
    Interpretation Guidelines:
    - Low risk (0 points): Standard anticoagulation with routine monitoring
    - Intermediate risk (1-2.5 points): Enhanced monitoring and risk assessment
    - High risk (>2.5 points): Consider modified anticoagulation strategies
    - Always integrate with clinical judgment and patient preferences
    
    Quality Assurance:
    - Verify accuracy of laboratory values and clinical history
    - Consider patient-specific factors not captured in the score
    - Document rationale for treatment decisions based on score results
    - Plan appropriate follow-up based on bleeding risk category
    
    References: See module docstring for complete citation list.
    """
    
    syncope: Literal["yes", "no"] = Field(
        ...,
        description="History of syncope at presentation or shortly before PE diagnosis. Syncope indicates potential hemodynamic compromise and contributes 1.5 points to the bleeding risk score. Include any witnessed loss of consciousness with spontaneous recovery.",
        example="no"
    )
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Anemia defined as hemoglobin level less than 12 g/dL (120 g/L). This is the highest weighted factor (2.5 points) and most predictive single variable for early major bleeding. Use the most recent hemoglobin level prior to anticoagulation initiation.",
        example="yes"
    )
    
    renal_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Renal dysfunction defined as estimated glomerular filtration rate (eGFR) less than 60 mL/min/1.73m². Contributes 1.0 point to the score. Use CKD-EPI or similar validated equation for eGFR calculation. Consider impact on anticoagulant clearance.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "syncope": "no",
                "anemia": "yes",
                "renal_dysfunction": "no"
            }
        }


class PeSardScoreResponse(BaseModel):
    """
    Response model for Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score
    
    The PE-SARD score provides evidence-based bleeding risk stratification for patients 
    with acute pulmonary embolism, enabling clinicians to make informed decisions about 
    anticoagulation management and monitoring intensity. Understanding score results is 
    essential for optimizing patient safety while maintaining therapeutic efficacy.
    
    Risk Category Interpretation and Clinical Management:
    
    Low Risk (0 points, 0.6% bleeding incidence):
    - Excellent bleeding safety profile with minimal early bleeding risk
    - Standard anticoagulation therapy with routine monitoring appropriate
    - Consider outpatient management if other clinical factors permit
    - Routine follow-up schedule with standard bleeding precaution education
    - No modification of anticoagulation intensity typically required
    - Monitor for changes in clinical status that may affect bleeding risk
    
    Intermediate Risk (1-2.5 points, 1.5% bleeding incidence):
    - Moderate bleeding risk requiring enhanced attention to risk-benefit balance
    - Consider more frequent monitoring and enhanced patient education
    - Evaluate for factors that may modify bleeding risk (drug interactions, falls risk)
    - May benefit from closer follow-up and structured bleeding assessment
    - Consider consultation if complex management decisions required
    - Document rationale for anticoagulation approach and monitoring plan
    
    High Risk (>2.5 points, 2.5% bleeding incidence):
    - Highest bleeding risk category requiring careful management strategy
    - Consider reduced-intensity anticoagulation or alternative treatment approaches
    - Evaluate for specialist consultation (hematology, cardiology, internal medicine)
    - Enhanced monitoring with frequent clinical and laboratory assessment
    - Structured bleeding risk assessment and mitigation strategies
    - Consider patient preferences and quality of life in treatment decisions
    
    Clinical Decision Support and Management Strategies:
    
    Anticoagulation Considerations:
    - Low risk: Standard-dose anticoagulation (warfarin INR 2-3, DOAC standard dose)
    - Intermediate risk: Consider standard dose with enhanced monitoring or consultation
    - High risk: Evaluate reduced-intensity anticoagulation, IVC filter, or specialist input
    - Always consider individual patient factors and contraindications
    
    Monitoring and Follow-up:
    - Low risk: Routine follow-up per standard PE protocols (typically 1-3 months)
    - Intermediate risk: Consider more frequent monitoring (2-4 weeks initially)
    - High risk: Close monitoring (1-2 weeks initially) with structured assessment
    - All patients: Education about bleeding signs and emergency care instructions
    
    Risk Mitigation Strategies:
    - Address modifiable bleeding risk factors (medication interactions, fall prevention)
    - Optimize management of comorbidities contributing to bleeding risk
    - Consider proton pump inhibitor therapy for patients with GI bleeding risk
    - Evaluate for reversibility of risk factors over time
    
    Shared Decision-Making Elements:
    - Discuss bleeding vs. thrombotic risk trade-offs with patients and families
    - Consider patient preferences, goals of care, and quality of life priorities
    - Provide clear information about risk levels and monitoring requirements
    - Document discussion and rationale for chosen management approach
    
    Quality Assurance and Documentation:
    - Document PE-SARD score calculation and clinical interpretation
    - Record rationale for anticoagulation decisions based on bleeding risk assessment
    - Plan systematic reassessment if clinical condition changes
    - Consider integration with other risk assessment tools (Wells score, PESI, etc.)
    
    Limitations and Clinical Judgment:
    - Score provides population-level estimates; individual risk may vary
    - Consider patient-specific factors not captured in the scoring system
    - Social factors, medication adherence, and support systems not incorporated
    - Use clinical judgment to supplement score-based recommendations
    - Reassess periodically as clinical condition and risk factors may change
    
    The PE-SARD score enables evidence-based bleeding risk assessment that can significantly 
    improve the safety and effectiveness of anticoagulation therapy in acute PE management, 
    supporting optimal patient outcomes through personalized treatment approaches.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: float = Field(
        ...,
        description="PE-SARD bleeding risk score calculated from clinical variables. Score ranges from 0 to 5 points, with higher scores indicating greater risk of early (30-day) major bleeding complications.",
        example=2.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the PE-SARD score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including bleeding risk category, 30-day bleeding incidence rates, anticoagulation management recommendations, monitoring guidance, and clinical decision support based on the calculated PE-SARD score.",
        example="Intermediate risk for early major bleeding (1.5% incidence within 30 days). Consider more frequent monitoring and careful assessment of bleeding vs. thrombotic risk. May require modified anticoagulation approach, closer surveillance, or enhanced patient education about bleeding precautions."
    )
    
    stage: str = Field(
        ...,
        description="PE-SARD bleeding risk category (Low Risk, Intermediate Risk, or High Risk) with associated clinical significance",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bleeding risk level associated with the calculated PE-SARD score",
        example="Intermediate bleeding risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "points",
                "interpretation": "Intermediate risk for early major bleeding (1.5% incidence within 30 days). Consider more frequent monitoring and careful assessment of bleeding vs. thrombotic risk. May require modified anticoagulation approach, closer surveillance, or enhanced patient education about bleeding precautions.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate bleeding risk"
            }
        }