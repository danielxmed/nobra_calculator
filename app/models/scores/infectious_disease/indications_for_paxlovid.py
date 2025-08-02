"""
Indications for Paxlovid Models

Request and response models for Paxlovid eligibility assessment.

References (Vancouver style):
1. U.S. Food and Drug Administration. Fact Sheet for Healthcare Providers: Emergency 
   Use Authorization for Paxlovid. Updated May 2023.
2. Hammond J, Leister-Tebbe H, Gardner A, et al. Oral nirmatrelvir for high-risk, 
   nonhospitalized adults with Covid-19. N Engl J Med. 2022;386(15):1397-1408. 
   doi: 10.1056/NEJMoa2118542.
3. Centers for Disease Control and Prevention. Clinical Care Guidance: Oral Antiviral 
   Treatment for COVID-19. Updated 2023.
4. NIH COVID-19 Treatment Guidelines Panel. Ritonavir-Boosted Nirmatrelvir (Paxlovid). 
   Updated 2023.

Paxlovid (nirmatrelvir-ritonavir) is an oral antiviral treatment authorized for 
mild-to-moderate COVID-19 in patients at high risk for progression to severe COVID-19, 
including hospitalization or death. The medication must be started within 5 days of 
symptom onset and requires careful screening for eligibility criteria and drug 
interactions. This tool systematically evaluates FDA-approved indications, contraindications, 
and dosing considerations to help clinicians make appropriate prescribing decisions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IndicationsForPaxlovidRequest(BaseModel):
    """
    Request model for Paxlovid eligibility assessment
    
    Evaluates patient eligibility for Paxlovid (nirmatrelvir-ritonavir) therapy based 
    on FDA guidelines and clinical criteria:
    
    Basic Eligibility Requirements (ALL must be met):
    - Age >12 years and weight >40 kg (88 lbs)
    - Mild to moderate COVID-19 (not hospitalized/severe)
    - Symptom onset ≤5 days (critical timing requirement)
    - Adequate renal function (eGFR >30 mL/min/1.73m²)
    - No severe hepatic impairment (Child-Pugh Class C)
    
    High-Risk Factors (at least ONE required):
    - Age >50 years (especially ≥65)
    - Diabetes mellitus (Type 1 or 2)
    - Cardiovascular disease
    - Chronic lung disease (asthma, COPD, etc.)
    - Obesity (BMI ≥30 or ≥25 for Asian descent)
    - Immunocompromised state
    - Pregnancy
    - Unvaccinated or not up to date with vaccines
    - Other CDC-recognized high-risk conditions
    
    Contraindications:
    - Significant drug interactions with ritonavir (CYP3A4 inhibitor)
    - Severe renal impairment (eGFR <30)
    - Severe hepatic impairment
    
    Dosing:
    - Standard: nirmatrelvir 300mg + ritonavir 100mg twice daily × 5 days
    - Reduced (eGFR 30-60): nirmatrelvir 150mg + ritonavir 100mg twice daily × 5 days
    
    References (Vancouver style):
    1. U.S. Food and Drug Administration. Fact Sheet for Healthcare Providers: Emergency 
       Use Authorization for Paxlovid. Updated May 2023.
    2. Hammond J, Leister-Tebbe H, Gardner A, et al. Oral nirmatrelvir for high-risk, 
       nonhospitalized adults with Covid-19. N Engl J Med. 2022;386(15):1397-1408.
    """
    
    age_over_12: Literal["no", "yes"] = Field(
        ...,
        description="Patient age >12 years. Paxlovid is FDA-approved for patients 12 years and older with appropriate weight and risk factors",
        example="yes"
    )
    
    weight_over_40kg: Literal["no", "yes"] = Field(
        ...,
        description="Patient weight >40 kg (approximately 88 lbs). Minimum weight requirement for safe dosing in pediatric/adolescent patients",
        example="yes"
    )
    
    mild_moderate_covid: Literal["no", "yes"] = Field(
        ...,
        description="Mild to moderate COVID-19 disease severity. Excludes patients with severe COVID-19 requiring hospitalization or oxygen therapy",
        example="yes"
    )
    
    symptom_onset_5_days: Literal["no", "yes"] = Field(
        ...,
        description="Symptom onset ≤5 days. Critical timing requirement - Paxlovid must be initiated within 5 days of COVID-19 symptom onset for efficacy",
        example="yes"
    )
    
    egfr_over_30: Literal["no", "yes"] = Field(
        ...,
        description="Estimated glomerular filtration rate (eGFR) >30 mL/min/1.73m². Severe renal impairment (eGFR <30) is a contraindication",
        example="yes"
    )
    
    no_severe_hepatic_impairment: Literal["no", "yes"] = Field(
        ...,
        description="No severe hepatic impairment (Child-Pugh Class C). Severe liver dysfunction affects drug metabolism and safety",
        example="yes"
    )
    
    age_over_50: Literal["no", "yes"] = Field(
        ...,
        description="Age >50 years. Major risk factor for progression to severe COVID-19, especially patients ≥65 years old",
        example="yes"
    )
    
    diabetes: Literal["no", "yes"] = Field(
        ...,
        description="Diabetes mellitus (Type 1 or Type 2). High-risk condition for severe COVID-19 complications and hospitalization",
        example="no"
    )
    
    heart_disease: Literal["no", "yes"] = Field(
        ...,
        description="Cardiovascular disease including coronary artery disease, heart failure, cardiomyopathy, or congenital heart disease",
        example="no"
    )
    
    lung_disease: Literal["no", "yes"] = Field(
        ...,
        description="Chronic lung disease including asthma, COPD, pulmonary fibrosis, or other chronic respiratory conditions",
        example="no"
    )
    
    obesity: Literal["no", "yes"] = Field(
        ...,
        description="Obesity defined as BMI ≥30 kg/m² or BMI ≥25 kg/m² in adults of Asian descent. Significant risk factor for severe COVID-19",
        example="no"
    )
    
    immunocompromised: Literal["no", "yes"] = Field(
        ...,
        description="Immunocompromised state due to disease or medications (cancer, organ transplant, immunosuppressive therapy, HIV, primary immunodeficiency)",
        example="no"
    )
    
    pregnancy: Literal["no", "yes"] = Field(
        ...,
        description="Current pregnancy. Pregnancy increases risk for severe COVID-19 and adverse pregnancy outcomes",
        example="no"
    )
    
    unvaccinated_or_not_current: Literal["no", "yes"] = Field(
        ...,
        description="Unvaccinated against COVID-19 or not up to date with COVID-19 vaccines according to CDC recommendations",
        example="no"
    )
    
    other_high_risk_condition: Literal["no", "yes"] = Field(
        ...,
        description="Other high-risk conditions including cancer, chronic kidney disease, chronic liver disease, neurological conditions, substance use disorders, or other conditions per CDC high-risk list",
        example="no"
    )
    
    significant_drug_interactions: Literal["no", "yes"] = Field(
        ...,
        description="Significant drug interactions with ritonavir component. Ritonavir is a strong CYP3A4 inhibitor with potential for serious drug-drug interactions",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_over_12": "yes",
                "weight_over_40kg": "yes",
                "mild_moderate_covid": "yes",
                "symptom_onset_5_days": "yes",
                "egfr_over_30": "yes", 
                "no_severe_hepatic_impairment": "yes",
                "age_over_50": "yes",
                "diabetes": "no",
                "heart_disease": "no",
                "lung_disease": "no",
                "obesity": "no",
                "immunocompromised": "no",
                "pregnancy": "no",
                "unvaccinated_or_not_current": "no",
                "other_high_risk_condition": "no",
                "significant_drug_interactions": "no"
            }
        }


class IndicationsForPaxlovidResponse(BaseModel):
    """
    Response model for Paxlovid eligibility assessment
    
    Returns prescribing recommendation with dosing guidance and clinical considerations 
    for Paxlovid (nirmatrelvir-ritonavir) therapy in COVID-19 patients.
    
    Recommendation Categories:
    - Not Indicated: Patient doesn't meet eligibility criteria
    - Contraindicated: Safety concerns prevent prescribing
    - Standard Dose: Eligible for standard dosing regimen
    - Reduced Dose: Eligible with dose adjustment for moderate renal impairment
    
    The assessment provides evidence-based recommendations following FDA guidelines 
    and helps ensure appropriate patient selection for this time-sensitive antiviral 
    therapy. Proper screening prevents adverse drug interactions and optimizes 
    therapeutic outcomes while minimizing safety risks.
    
    Reference: Hammond J, et al. N Engl J Med. 2022;386(15):1397-1408.
    """
    
    result: str = Field(
        ...,
        description="Paxlovid prescribing recommendation (Not Indicated, Contraindicated, Standard Dose, Reduced Dose)",
        example="Standard Dose"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the recommendation",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and specific prescribing guidance based on the assessment",
        example="Patient eligible for Paxlovid. Prescribe standard dose: nirmatrelvir 300mg + ritonavir 100mg twice daily for 5 days. Start within 5 days of symptom onset."
    )
    
    stage: str = Field(
        ...,
        description="Recommendation category (Not Indicated, Contraindicated, Standard Dose, Reduced Dose)",
        example="Standard Dose"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the recommendation category",
        example="Paxlovid indicated - standard dose"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Standard Dose",
                "unit": "recommendation",
                "interpretation": "Patient eligible for Paxlovid. Prescribe standard dose: nirmatrelvir 300mg + ritonavir 100mg twice daily for 5 days. Start within 5 days of symptom onset.",
                "stage": "Standard Dose",
                "stage_description": "Paxlovid indicated - standard dose"
            }
        }