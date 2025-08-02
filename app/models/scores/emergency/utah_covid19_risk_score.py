"""
Utah COVID-19 Risk Score Models

Request and response models for Utah COVID-19 Risk Score calculation.

References (Vancouver style):
1. Utah Department of Health. COVID-19 Treatment Risk Score Calculator. Updated February 2022. 
   Available at: https://coronavirus.utah.gov/
2. Intermountain Healthcare. Utah COVID-19 Risk Assessment for Treatment Prioritization. 2022.
3. Centers for Disease Control and Prevention. Emergency Use Authorization for COVID-19 Treatments. 
   Updated 2022.

The Utah COVID-19 Risk Score identifies high-risk individuals appropriate for COVID-19 treatment 
and helps prioritize oral antiviral treatment during medication shortages. Updated in February 2022 
to remove race/ethnicity and gender criteria while maintaining evidence-based risk stratification 
for treatment allocation.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class UtahCovid19RiskScoreRequest(BaseModel):
    """
    Request model for Utah COVID-19 Risk Score
    
    The Utah COVID-19 Risk Score was developed to optimize allocation of scarce COVID-19 
    treatments during the pandemic by identifying patients at highest risk for hospitalization 
    and severe outcomes. The calculator uses evidence-based risk factors to determine 
    treatment eligibility with different thresholds based on vaccination status.
    
    **SCORING COMPONENTS:**
    
    **1. Age Points (Progressive Risk):**
    
    The risk of severe COVID-19 outcomes increases progressively with age:
    
    - 16-20 years: 1.0 point
    - 21-30 years: 1.5 points  
    - 31-40 years: 2.0 points
    - 41-50 years: 2.5 points
    - 51-60 years: 3.0 points
    - 61-70 years: 3.5 points
    - 71-80 years: 4.0 points
    - 81-90 years: 4.5 points
    - 91-100 years: 5.0 points
    - ≥101 years: 5.5 points
    
    **2. Highest Risk Comorbidities (2 points each):**
    
    These conditions confer the highest risk for severe COVID-19 outcomes:
    
    **Diabetes Mellitus:**
    - Type 1 or Type 2 diabetes mellitus
    - Associated with increased inflammation and immune dysfunction
    - Significantly increases hospitalization and mortality risk
    
    **Obesity (BMI >30 kg/m²):**
    - Body Mass Index greater than 30 kg/m²
    - Associated with impaired immune response and respiratory function
    - Increases risk of severe disease and prolonged illness
    
    **3. Other High-Risk Comorbidities (1 point each):**
    
    **Active Cancer:**
    - Currently receiving treatment for cancer
    - Hematologic malignancies or solid tumors
    - Immunocompromised state due to disease or treatment
    
    **Immunosuppressive Therapies:**
    - Medications that suppress immune system function
    - Including corticosteroids, biologics, chemotherapy
    - Transplant immunosuppression medications
    
    **Cardiovascular Conditions:**
    - Hypertension (high blood pressure)
    - Coronary artery disease
    - Cardiac arrhythmias
    - Congestive heart failure
    
    **Chronic Organ Diseases:**
    - Chronic kidney disease
    - Chronic pulmonary disease (COPD, asthma, pulmonary fibrosis)
    - Chronic liver disease
    - Cerebrovascular disease (stroke history, TIA)
    - Chronic neurologic disease (multiple sclerosis, Parkinson's, etc.)
    
    **4. Symptom Risk Factor (1 point):**
    
    **New Shortness of Breath:**
    - Recent onset dyspnea or worsening baseline dyspnea
    - Strong predictor of disease progression and hospitalization
    - Associated with 2.3 times higher likelihood of hospitalization
    
    **TREATMENT THRESHOLDS:**
    
    Different thresholds apply based on vaccination status, reflecting varying 
    baseline risk levels:
    
    **Vaccinated Patients: ≥8 points**
    - Higher threshold due to reduced baseline risk from vaccination
    - Includes fully vaccinated and boosted individuals
    - Reflects protection conferred by vaccination
    
    **Unvaccinated/Incompletely Vaccinated: ≥6 points**
    - Lower threshold due to higher baseline risk
    - Includes unvaccinated and partially vaccinated individuals
    - Accounts for lack of vaccine protection
    
    **Unvaccinated/Incompletely Vaccinated and Pregnant: ≥4 points**
    - Lowest threshold recognizing pregnancy as additional risk factor
    - Pregnancy increases risk of severe COVID-19 outcomes
    - Prioritizes protection of pregnant patients and fetal health
    
    **CLINICAL CONTEXT:**
    
    **Treatment Timing:**
    - Must be used within 10 days of symptom onset
    - Effectiveness decreases significantly after this window
    - Earlier treatment provides better outcomes
    
    **Available Treatments:**
    - Oral antivirals: nirmatrelvir-ritonavir (Paxlovid), molnupiravir
    - Monoclonal antibodies: bebtelovimab (if oral agents contraindicated)
    - Selection based on patient factors and drug interactions
    
    **Resource Allocation:**
    - Developed during periods of treatment scarcity
    - Helps prioritize limited resources to highest-risk patients
    - May need adjustment based on local availability
    
    **FEBRUARY 2022 UPDATES:**
    
    **Removed Criteria:**
    - Race and ethnicity removed from scoring
    - Gender removed from risk calculation
    - Addressed concerns about health equity and bias
    
    **Retained Evidence-Based Factors:**
    - Age-based progressive risk
    - Validated medical comorbidities
    - Clinical symptoms predictive of progression
    - Vaccination status as risk modifier
    
    **IMPORTANT LIMITATIONS:**
    
    **Development Context:**
    - Created during COVID-19 crisis for urgent need
    - Based on available data from Intermountain Healthcare system
    - Not externally validated in diverse populations
    
    **Clinical Judgment:**
    - Should complement, not replace, clinical assessment
    - Individual patient factors may override score recommendations
    - Consider social determinants and access to care
    
    **Evolving Evidence:**
    - COVID-19 variant characteristics may affect risk profiles
    - Treatment efficacy may vary by viral strain
    - Ongoing research may modify risk factor weights
    
    References (Vancouver style):
    1. Utah Department of Health. COVID-19 Treatment Risk Score Calculator. Updated February 2022.
    2. Intermountain Healthcare. Utah COVID-19 Risk Assessment for Treatment Prioritization. 2022.
    3. Centers for Disease Control and Prevention. Emergency Use Authorization for COVID-19 Treatments.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years (16-120 years)",
        ge=16,
        le=120,
        example=45
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="Diabetes mellitus (Type 1 or Type 2) - highest risk comorbidity (2 points)",
        example="no"
    )
    
    obesity: Literal["yes", "no"] = Field(
        ...,
        description="Obesity with BMI >30 kg/m² - highest risk comorbidity (2 points)",
        example="yes"
    )
    
    active_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Active cancer currently receiving treatment (1 point)",
        example="no"
    )
    
    immunosuppressive_therapies: Literal["yes", "no"] = Field(
        ...,
        description="Immunosuppressive therapies (corticosteroids, biologics, chemotherapy, transplant medications) (1 point)",
        example="no"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Hypertension (high blood pressure) (1 point)",
        example="yes"
    )
    
    coronary_artery_disease: Literal["yes", "no"] = Field(
        ...,
        description="Coronary artery disease (1 point)",
        example="no"
    )
    
    cardiac_arrhythmia: Literal["yes", "no"] = Field(
        ...,
        description="Cardiac arrhythmia (1 point)",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="Congestive heart failure (1 point)",
        example="no"
    )
    
    chronic_kidney_disease: Literal["yes", "no"] = Field(
        ...,
        description="Chronic kidney disease (1 point)",
        example="no"
    )
    
    chronic_pulmonary_disease: Literal["yes", "no"] = Field(
        ...,
        description="Chronic pulmonary disease (COPD, asthma, pulmonary fibrosis) (1 point)",
        example="no"
    )
    
    chronic_liver_disease: Literal["yes", "no"] = Field(
        ...,
        description="Chronic liver disease (1 point)",
        example="no"
    )
    
    cerebrovascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Cerebrovascular disease (stroke history, TIA) (1 point)",
        example="no"
    )
    
    chronic_neurologic_disease: Literal["yes", "no"] = Field(
        ...,
        description="Chronic neurologic disease (multiple sclerosis, Parkinson's, etc.) (1 point)",
        example="no"
    )
    
    shortness_of_breath: Literal["yes", "no"] = Field(
        ...,
        description="New shortness of breath (recent onset dyspnea) - symptom risk factor (1 point)",
        example="no"
    )
    
    vaccination_status: Literal["vaccinated", "unvaccinated_not_pregnant", "unvaccinated_pregnant"] = Field(
        ...,
        description="COVID-19 vaccination status. vaccinated: fully vaccinated/boosted (≥8 pts threshold); unvaccinated_not_pregnant: unvaccinated/incomplete vaccination (≥6 pts threshold); unvaccinated_pregnant: unvaccinated/incomplete vaccination and pregnant (≥4 pts threshold)",
        example="vaccinated"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "diabetes_mellitus": "no",
                "obesity": "yes",
                "active_cancer": "no",
                "immunosuppressive_therapies": "no",
                "hypertension": "yes",
                "coronary_artery_disease": "no",
                "cardiac_arrhythmia": "no",
                "congestive_heart_failure": "no",
                "chronic_kidney_disease": "no",
                "chronic_pulmonary_disease": "no",
                "chronic_liver_disease": "no",
                "cerebrovascular_disease": "no",
                "chronic_neurologic_disease": "no",
                "shortness_of_breath": "no",
                "vaccination_status": "vaccinated"
            }
        }


class UtahCovid19RiskScoreResponse(BaseModel):
    """
    Response model for Utah COVID-19 Risk Score
    
    The Utah COVID-19 Risk Score provides evidence-based treatment recommendations 
    for COVID-19 patients by assessing risk factors for severe outcomes and applying 
    vaccination status-specific thresholds for treatment eligibility.
    
    **INTERPRETATION CATEGORIES:**
    
    **Treatment Eligible:**
    - Score meets or exceeds threshold for vaccination status
    - Qualifies for COVID-19 antiviral treatment
    - Should initiate treatment within 10 days of symptom onset
    - Consider nirmatrelvir-ritonavir or molnupiravir based on patient factors
    
    **Treatment Not Eligible:**
    - Score below threshold for vaccination status
    - Does not meet current criteria for antiviral treatment
    - Continue supportive care and monitor for progression
    - Re-evaluate if new symptoms or risk factors develop
    
    **CLINICAL DECISION SUPPORT:**
    
    **For Treatment-Eligible Patients:**
    - Initiate oral antiviral therapy promptly
    - Choose appropriate agent based on contraindications and interactions
    - Monitor for treatment response and adverse effects
    - Provide patient education on treatment expectations
    
    **For Non-Eligible Patients:**
    - Continue symptomatic care and supportive measures
    - Monitor daily for symptom progression
    - Educate on warning signs requiring medical attention
    - Consider individual factors that may override score
    
    **TREATMENT OPTIONS:**
    
    **Nirmatrelvir-ritonavir (Paxlovid):**
    - Preferred first-line oral antiviral
    - High efficacy in preventing severe outcomes
    - Significant drug interactions require careful review
    - Contraindicated with severe renal or hepatic impairment
    
    **Molnupiravir:**
    - Alternative oral antiviral option
    - Fewer drug interactions than nirmatrelvir-ritonavir
    - Contraindicated in pregnancy due to mutagenic potential
    - Consider when Paxlovid contraindicated
    
    **Bebtelovimab:**
    - Monoclonal antibody for intravenous use
    - Reserved for patients who cannot take oral agents
    - May be limited by viral variant resistance
    - Requires healthcare facility administration
    
    **MONITORING AND FOLLOW-UP:**
    
    **Daily Assessment:**
    - Symptom progression or improvement
    - Development of warning signs (dyspnea, chest pain, confusion)
    - Treatment adherence and side effects
    - Isolation compliance and duration
    
    **Return Criteria:**
    - Worsening shortness of breath or chest pain
    - High fever not responding to antipyretics
    - Altered mental status or severe fatigue
    - Signs of secondary bacterial infection
    
    **IMPORTANT CONSIDERATIONS:**
    
    **Timing Critical:**
    - Treatment most effective within 5 days of symptom onset
    - Benefit decreases significantly after 10 days
    - Do not delay treatment for test results if clinically indicated
    
    **Individual Assessment:**
    - Score should guide but not replace clinical judgment
    - Consider social determinants affecting outcome risk
    - Account for patient preferences and treatment goals
    - Evaluate access to care and follow-up capabilities
    
    Reference: Utah Department of Health. COVID-19 Treatment Risk Score Calculator. 2022.
    """
    
    result: float = Field(
        ...,
        description="Total Utah COVID-19 Risk Score in points",
        example=5.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendation based on risk score and vaccination status",
        example="Utah COVID-19 Risk Score: 5.5 points. Patient does not meet current criteria for COVID-19 antiviral treatment (vaccinated threshold: ≥8 points). Continue supportive care and monitor for symptom progression."
    )
    
    stage: str = Field(
        ...,
        description="Treatment eligibility category (Treatment Eligible or Treatment Not Eligible)",
        example="Treatment Not Eligible"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of treatment eligibility status",
        example="Does not meet treatment criteria"
    )
    
    treatment_eligible: bool = Field(
        ...,
        description="Boolean indicating whether patient qualifies for COVID-19 treatment",
        example=False
    )
    
    threshold_score: float = Field(
        ...,
        description="Treatment threshold score for patient's vaccination status",
        example=8.0
    )
    
    vaccination_status: str = Field(
        ...,
        description="Patient's vaccination status used for threshold determination",
        example="vaccinated"
    )
    
    component_scores: Dict[str, float] = Field(
        ...,
        description="Breakdown of score components contributing to total",
        example={
            "age_points": 2.5,
            "comorbidity_points": 3.0,
            "symptom_points": 0.0
        }
    )
    
    clinical_recommendations: Dict[str, Any] = Field(
        ...,
        description="Detailed clinical management recommendations based on treatment eligibility",
        example={
            "immediate_actions": [
                "Continue supportive care (rest, hydration, symptom management)",
                "Monitor for symptom progression or deterioration",
                "Educate on warning signs requiring medical attention",
                "Ensure appropriate isolation measures"
            ],
            "monitoring": [
                "Daily symptom monitoring",
                "Return if symptoms worsen (shortness of breath, chest pain, confusion)",
                "Re-evaluate if new high-risk symptoms develop",
                "Complete isolation per current CDC guidelines"
            ],
            "considerations": [
                "Score may change if new symptoms or comorbidities develop",
                "Individual clinical judgment may override score recommendations",
                "Consider treatment if patient deteriorates despite supportive care"
            ]
        }
    )
    
    important_considerations: Dict[str, Any] = Field(
        ...,
        description="Critical safety information and implementation guidance",
        example={
            "timing": "Treatment must be initiated within 10 days of symptom onset for maximum effectiveness",
            "limitations": [
                "Calculator developed during COVID-19 crisis and not externally validated",
                "Should complement clinical judgment, not replace comprehensive evaluation",
                "Local resource availability may affect treatment thresholds"
            ],
            "contraindications": [
                "Check for drug interactions, especially with nirmatrelvir-ritonavir",
                "Consider renal and hepatic function for dosing adjustments",
                "Review patient allergies and previous adverse reactions"
            ],
            "special_populations": [
                "Pregnancy: unvaccinated pregnant patients have lower threshold (≥4 points)",
                "Immunocompromised: may need individualized assessment",
                "Elderly: often qualify based on age alone"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5.5,
                "unit": "points",
                "interpretation": "Utah COVID-19 Risk Score: 5.5 points. Patient does not meet current criteria for COVID-19 antiviral treatment (vaccinated threshold: ≥8 points). Continue supportive care and monitor for symptom progression.",
                "stage": "Treatment Not Eligible",
                "stage_description": "Does not meet treatment criteria",
                "treatment_eligible": False,
                "threshold_score": 8.0,
                "vaccination_status": "vaccinated",
                "component_scores": {
                    "age_points": 2.5,
                    "comorbidity_points": 3.0,
                    "symptom_points": 0.0
                },
                "clinical_recommendations": {
                    "immediate_actions": [
                        "Continue supportive care (rest, hydration, symptom management)",
                        "Monitor for symptom progression or deterioration",
                        "Educate on warning signs requiring medical attention",
                        "Ensure appropriate isolation measures"
                    ],
                    "monitoring": [
                        "Daily symptom monitoring",
                        "Return if symptoms worsen (shortness of breath, chest pain, confusion)",
                        "Re-evaluate if new high-risk symptoms develop",
                        "Complete isolation per current CDC guidelines"
                    ],
                    "considerations": [
                        "Score may change if new symptoms or comorbidities develop",
                        "Individual clinical judgment may override score recommendations",
                        "Consider treatment if patient deteriorates despite supportive care"
                    ]
                },
                "important_considerations": {
                    "timing": "Treatment must be initiated within 10 days of symptom onset for maximum effectiveness",
                    "limitations": [
                        "Calculator developed during COVID-19 crisis and not externally validated",
                        "Should complement clinical judgment, not replace comprehensive evaluation",
                        "Local resource availability may affect treatment thresholds"
                    ],
                    "contraindications": [
                        "Check for drug interactions, especially with nirmatrelvir-ritonavir",
                        "Consider renal and hepatic function for dosing adjustments",
                        "Review patient allergies and previous adverse reactions"
                    ],
                    "special_populations": [
                        "Pregnancy: unvaccinated pregnant patients have lower threshold (≥4 points)",
                        "Immunocompromised: may need individualized assessment",
                        "Elderly: often qualify based on age alone"
                    ]
                }
            }
        }