"""
VACO Index COVID-19 Mortality Risk Models

Request and response models for VACO Index COVID-19 mortality risk calculation.

References (Vancouver style):
1. Justice AC, Freiburg MS, Lopez-Class M, et al. Patient-facing COVID-19 risk tool. 
   Developed in collaboration with US Department of Health and Human Services. 
   Yale University and VA Connecticut Healthcare System; 2020.
2. King JT Jr, Yoon JS, Rentsch CT, et al. Development and validation of a 30-day mortality 
   index based on pre-existing medical administrative data from 13,323 COVID-19 patients: 
   The Veterans Health Administration COVID-19 (VACO) Index. PLoS One. 2020;15(11):e0241825. 
   doi: 10.1371/journal.pone.0241825.
3. Rentsch CT, Kidwai-Khan F, Tate JP, et al. Patterns of COVID-19 testing and mortality 
   by race and ethnicity among United States veterans: A nationwide cohort study. 
   PLoS Med. 2020;17(9):e1003379. doi: 10.1371/journal.pmed.1003379.

The VACO Index COVID-19 Mortality Risk calculator estimates 30-day mortality risk after 
COVID-19 infection using pre-existing health conditions and demographics. It was developed 
by researchers from Yale University and VA Connecticut Healthcare System in collaboration 
with the US Department of Health and Human Services to help patients understand their risk 
profile and make informed decisions about protective measures.

The calculator uses age-specific coefficients, sex coefficients, and Charlson Comorbidity 
Index scores to generate a personalized mortality risk estimate. Risk categories range from 
lower risk (0-8.7%) to extreme risk (>21.3%), with specific recommendations for preventive 
measures and medical consultation at each level.

Clinical Application:
- Patient risk stratification for COVID-19 prevention strategies
- Informed decision-making about protective measures
- Healthcare provider-patient discussions about individualized risk
- Public health guidance for high-risk populations
- Vaccination prioritization considerations

Important Notes:
- This calculator estimates mortality risk based on pre-existing conditions
- Does not predict risk of contracting COVID-19
- Based on veterans data and may not fully generalize to all populations
- Should be interpreted in consultation with healthcare professionals
"""

from pydantic import BaseModel, Field
from typing import Literal


class VacoIndexCovid19Request(BaseModel):
    """
    Request model for VACO Index COVID-19 Mortality Risk calculator
    
    The VACO Index uses patient age, biological sex, and 14 comorbidity conditions based 
    on the Charlson Comorbidity Index to estimate 30-day mortality risk after COVID-19 infection.
    
    **Age Categories:**
    - 20-49 years: Lower baseline risk coefficient
    - 50-54 years: Reference category (coefficient = 0)
    - 55+ years: Progressively higher risk coefficients with advanced age
    
    **Sex Impact:**
    - Female: Reference category (coefficient = 0)
    - Male: Higher risk coefficient (+0.32)
    
    **Comorbidity Conditions (Charlson Comorbidity Index based):**
    
    1. **Diabetes Mellitus**: Uncomplicated (1 point) or with complications (2 points)
    2. **Chronic Pulmonary Disease**: COPD, asthma, pulmonary fibrosis (1 point)
    3. **Renal Disease**: Mild-moderate CKD (1 point) or severe CKD/dialysis (2 points)
    4. **Peripheral Vascular Disease**: PAD, claudication, bypass surgery (1 point)
    5. **Congestive Heart Failure**: Any history of CHF (1 point)
    6. **Dementia**: Any form of dementia or cognitive impairment (1 point)
    7. **Cancer**: Localized solid tumor or leukemia/lymphoma (2 points), metastatic cancer (6 points)
    8. **Cerebrovascular Accident**: History of stroke or TIA (1 point)
    9. **Liver Disease**: Mild liver disease (1 point) or moderate-severe cirrhosis (3 points)
    10. **Myocardial Infarction**: History of heart attack (1 point)
    11. **Peptic Ulcer Disease**: History of peptic ulcers (1 point)
    12. **Paralysis**: Hemiplegia, paraplegia, quadriplegia (2 points)
    13. **AIDS**: HIV with AIDS-defining illness (6 points)
    14. **Rheumatologic Disease**: RA, SLE, polymyositis (1 point)
    
    **Risk Interpretation:**
    - Lower Risk (0-8.7%): Standard preventive measures
    - Moderate Risk (8.8-16.0%): Enhanced preventive measures recommended
    - High Risk (16.1-21.2%): Strict preventive measures, additional protection strategies
    - Extreme Risk (>21.3%): Maximum preventive measures, immediate medical consultation

    References (Vancouver style):
    1. Justice AC, Freiburg MS, Lopez-Class M, et al. Patient-facing COVID-19 risk tool. 
       Developed in collaboration with US Department of Health and Human Services. 
       Yale University and VA Connecticut Healthcare System; 2020.
    2. King JT Jr, Yoon JS, Rentsch CT, et al. Development and validation of a 30-day mortality 
       index based on pre-existing medical administrative data from 13,323 COVID-19 patients: 
       The Veterans Health Administration COVID-19 (VACO) Index. PLoS One. 2020;15(11):e0241825.
    3. Rentsch CT, Kidwai-Khan F, Tate JP, et al. Patterns of COVID-19 testing and mortality 
       by race and ethnicity among United States veterans: A nationwide cohort study. 
       PLoS Med. 2020;17(9):e1003379.
    """
    
    age: int = Field(
        ...,
        description=(
            "Patient age in years. Age-specific coefficients applied: "
            "20-49 years (lower risk), 50-54 years (reference), "
            "55+ years (progressively higher risk with advanced age)."
        ),
        ge=20,
        le=115,
        example=65
    )
    
    sex: Literal["female", "male"] = Field(
        ...,
        description=(
            "Patient biological sex. Males have higher COVID-19 mortality risk "
            "(coefficient +0.32) compared to females (reference category)."
        ),
        example="male"
    )
    
    diabetes: Literal["none", "uncomplicated", "complicated"] = Field(
        ...,
        description=(
            "Diabetes mellitus status and complications. "
            "None (0 points), uncomplicated diabetes (1 point), "
            "diabetes with complications like neuropathy, nephropathy, retinopathy (2 points)."
        ),
        example="none"
    )
    
    chronic_pulmonary_disease: Literal["no", "yes"] = Field(
        ...,
        description=(
            "Chronic pulmonary disease including COPD, asthma, pulmonary fibrosis, "
            "or other chronic lung conditions. Scores 1 point if present."
        ),
        example="no"
    )
    
    renal_disease: Literal["none", "mild_moderate", "severe"] = Field(
        ...,
        description=(
            "Kidney/renal disease status and severity. "
            "None (0 points), mild-moderate CKD (1 point), "
            "severe CKD or dialysis (2 points)."
        ),
        example="none"
    )
    
    peripheral_vascular_disease: Literal["no", "yes"] = Field(
        ...,
        description=(
            "Peripheral vascular disease including claudication, bypass surgery, "
            "acute arterial insufficiency, or gangrene. Scores 1 point if present."
        ),
        example="no"
    )
    
    congestive_heart_failure: Literal["no", "yes"] = Field(
        ...,
        description=(
            "History of congestive heart failure, including systolic or diastolic "
            "heart failure, cardiomyopathy. Scores 1 point if present."
        ),
        example="no"
    )
    
    dementia: Literal["no", "yes"] = Field(
        ...,
        description=(
            "Dementia including Alzheimer's disease, vascular dementia, "
            "or other forms of cognitive impairment. Scores 1 point if present."
        ),
        example="no"
    )
    
    cancer: Literal["none", "localized_solid", "metastatic_solid", "leukemia", "lymphoma"] = Field(
        ...,
        description=(
            "Cancer status and type. None (0 points), "
            "localized solid tumor (2 points), metastatic solid tumor (6 points), "
            "leukemia (2 points), lymphoma (2 points)."
        ),
        example="none"
    )
    
    cerebrovascular_accident: Literal["no", "yes"] = Field(
        ...,
        description=(
            "History of cerebrovascular accident (stroke) or transient ischemic attack (TIA). "
            "Scores 1 point if present."
        ),
        example="no"
    )
    
    liver_disease: Literal["none", "mild", "moderate_severe"] = Field(
        ...,
        description=(
            "Liver disease status and severity. "
            "None (0 points), mild liver disease without portal hypertension (1 point), "
            "moderate-severe liver disease with cirrhosis and portal hypertension (3 points)."
        ),
        example="none"
    )
    
    myocardial_infarction: Literal["no", "yes"] = Field(
        ...,
        description=(
            "History of myocardial infarction (heart attack) confirmed by ECG changes "
            "or enzyme elevation. Scores 1 point if present."
        ),
        example="no"
    )
    
    peptic_ulcer_disease: Literal["no", "yes"] = Field(
        ...,
        description=(
            "History of peptic ulcer disease including gastric or duodenal ulcers "
            "requiring treatment or bleeding. Scores 1 point if present."
        ),
        example="no"
    )
    
    paralysis: Literal["no", "yes"] = Field(
        ...,
        description=(
            "Paralysis including hemiplegia, paraplegia, or quadriplegia "
            "from any cause. Scores 2 points if present."
        ),
        example="no"
    )
    
    aids: Literal["no", "yes"] = Field(
        ...,
        description=(
            "AIDS (acquired immunodeficiency syndrome) or HIV with AIDS-defining illness "
            "such as opportunistic infections. Scores 6 points if present."
        ),
        example="no"
    )
    
    rheumatologic_disease: Literal["no", "yes"] = Field(
        ...,
        description=(
            "Rheumatologic disease including rheumatoid arthritis, systemic lupus erythematosus, "
            "polymyositis, or other connective tissue disorders. Scores 1 point if present."
        ),
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "diabetes": "uncomplicated",
                "chronic_pulmonary_disease": "yes",
                "renal_disease": "none",
                "peripheral_vascular_disease": "no",
                "congestive_heart_failure": "no",
                "dementia": "no",
                "cancer": "none",
                "cerebrovascular_accident": "no",
                "liver_disease": "none",
                "myocardial_infarction": "no",
                "peptic_ulcer_disease": "no",
                "paralysis": "no",
                "aids": "no",
                "rheumatologic_disease": "no"
            }
        }


class VacoIndexCovid19Response(BaseModel):
    """
    Response model for VACO Index COVID-19 Mortality Risk calculator
    
    The VACO Index provides a 30-day mortality risk percentage after COVID-19 infection 
    with risk stratification into four categories for clinical and patient decision-making.
    
    **Risk Categories:**
    - **Lower Risk (0-8.7%)**: Continue standard preventive measures
    - **Moderate Risk (8.8-16.0%)**: Enhanced preventive measures recommended
    - **High Risk (16.1-21.2%)**: Strict preventive measures, consider additional protection
    - **Extreme Risk (>21.3%)**: Maximum preventive measures, immediate medical consultation
    
    **Clinical Applications:**
    - Patient risk stratification for preventive measures
    - Healthcare provider-patient risk discussions
    - Vaccination prioritization considerations
    - Public health guidance for high-risk populations
    - Informed decision-making about protective behaviors
    
    **Important Limitations:**
    - Estimates mortality risk, not infection risk
    - Based on veterans data, may not fully generalize
    - Should be interpreted with healthcare provider guidance
    - Does not account for vaccination status or treatment advances
    
    Reference: King JT Jr, et al. PLoS One. 2020;15(11):e0241825.
    """
    
    result: float = Field(
        ...,
        description="30-day mortality risk percentage after COVID-19 infection based on pre-existing conditions",
        ge=0.0,
        le=100.0,
        example=12.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk estimate",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk category and specific recommendations for preventive measures",
        example="Moderate risk (12.5%) of death within 30 days of COVID-19 infection. Enhanced preventive measures recommended. Seek medical attention promptly if COVID-19 symptoms develop."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category (Lower Risk, Moderate Risk, High Risk, Extreme Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate risk of 30-day mortality"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12.5,
                "unit": "percentage",
                "interpretation": "Moderate risk (12.5%) of death within 30 days of COVID-19 infection. Enhanced preventive measures recommended. Seek medical attention promptly if COVID-19 symptoms develop.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk of 30-day mortality"
            }
        }