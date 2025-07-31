"""
Gail Model for Breast Cancer Risk Models

Request and response models for Gail Model breast cancer risk assessment.

References (Vancouver style):
1. Gail MH, Brinton LA, Byar DP, et al. Projecting individualized probabilities of 
   developing breast cancer for white females who are being examined annually. 
   J Natl Cancer Inst. 1989;81(24):1879-86. doi: 10.1093/jnci/81.24.1879.
2. Costantino JP, Gail MH, Pee D, et al. Validation studies for models projecting 
   the risk of invasive and total breast cancer incidence. J Natl Cancer Inst. 
   1999;91(18):1541-8. doi: 10.1093/jnci/91.18.1541.
3. Matsuno RK, Costantino JP, Ziegler RG, et al. Projecting individualized absolute 
   invasive breast cancer risk in Asian and Pacific Islander American women. 
   J Natl Cancer Inst. 2011;103(12):951-61. doi: 10.1093/jnci/djr154.

The Gail Model is a validated statistical tool that estimates a woman's absolute risk 
of developing invasive breast cancer over the next 5 years and up to age 90 (lifetime risk). 
The model uses personal medical and reproductive history along with family history of 
breast cancer among first-degree relatives to calculate individualized risk estimates.

Key Features:
- Validated for women aged 35-85 years without personal history of breast cancer
- Uses 7 key risk factors: age, race/ethnicity, age at menarche, age at first live birth, 
  family history, breast biopsy history, and atypical hyperplasia
- Validated for White, African-American, Hispanic, and Asian/Pacific Islander women in the US
- Primary clinical threshold: 5-year risk ≥1.67% for chemoprevention consideration

Clinical Applications:
- Risk assessment for breast cancer screening and prevention decisions
- Identification of high-risk women for enhanced surveillance or chemoprevention
- Shared decision-making for preventive interventions
- Research participant selection for breast cancer prevention trials
- Population health screening and risk stratification

Risk Factors Evaluated:
1. **Age**: Current age (35-85 years) - primary driver of baseline risk
2. **Race/Ethnicity**: White, African-American, Hispanic, Asian-American, American Indian/Alaska Native
3. **Age at Menarche**: First menstrual period (7-11, 12-13, >13 years)
4. **Age at First Live Birth**: <20, 20-24, 25-29, ≥30 years, or nulliparous
5. **Family History**: Number of first-degree relatives with breast cancer (0, 1, >1)
6. **Breast Biopsy History**: Number of previous breast biopsies (0, 1, >1)
7. **Atypical Hyperplasia**: Presence on previous breast biopsy (if applicable)

Clinical Interpretation:
- **Low Risk (<1.67% 5-year risk)**: Routine screening, lifestyle modifications
- **High Risk (≥1.67% 5-year risk)**: Consider chemoprevention, enhanced screening, genetic counseling

Limitations:
- Cannot be used for women with BRCA1/BRCA2 mutations or previous breast cancer
- Does not include lifestyle factors (alcohol, physical activity, hormone therapy)
- May underestimate risk in certain populations (Black women with biopsies, Hispanic women born outside US)
- Requires clinical judgment in interpretation and application

Implementation Note:
This implementation uses representative relative risk values from the literature. 
The exact NCI Gail Model uses complex race-specific coefficients and competing 
hazards calculations that are proprietary.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class GailModelBreastCancerRiskRequest(BaseModel):
    """
    Request model for Gail Model Breast Cancer Risk Assessment
    
    The Gail Model estimates a woman's absolute risk of developing invasive breast cancer 
    over the next 5 years using personal medical and reproductive history and family 
    history of breast cancer among first-degree relatives.
    
    **ELIGIBILITY CRITERIA**:
    
    **Inclusion Criteria**:
    - Women aged 35-85 years
    - No personal history of invasive or in situ breast cancer
    - No known BRCA1/BRCA2 mutations or high-penetrance genetic mutations
    
    **Exclusion Criteria**:
    - Personal history of breast cancer (invasive or in situ)
    - Known BRCA1/BRCA2 mutation carriers
    - Women under 35 years of age (model not validated)
    - Women over 85 years of age (limited data)
    
    **RISK FACTOR ASSESSMENT**:
    
    1. **Current Age** (35-85 years)
       - Primary driver of baseline breast cancer risk
       - Risk increases with age but may plateau after menopause
    
    2. **Age at Menarche** (First Menstrual Period)
       - **7-11 years**: Earlier menarche increases risk due to longer estrogen exposure
       - **12-13 years**: Average age range
       - **>13 years**: Later menarche associated with lower risk
       - **Unknown**: Use when information is not available or uncertain
    
    3. **Age at First Live Birth** or Nulliparous Status
       - **No births**: Nulliparous women have increased risk
       - **<20 years**: Early first birth associated with lower risk
       - **20-24 years**: Typical age range
       - **25-29 years**: Later first birth increases risk
       - **≥30 years**: Late first birth significantly increases risk
       - **Unknown**: Use when reproductive history is unclear
    
    4. **First-Degree Relatives with Breast Cancer**
       - **Include only**: Mother, sisters, daughters
       - **Do not include**: Aunts, grandmothers, cousins, paternal relatives
       - **0**: No affected first-degree relatives
       - **1**: One affected first-degree relative
       - **>1**: Two or more affected first-degree relatives
       - **Unknown**: When family history is incomplete or uncertain
    
    5. **Previous Breast Biopsies**
       - **0**: No previous breast biopsies
       - **1**: One previous breast biopsy
       - **>1**: Two or more previous breast biopsies
       - **Unknown**: When biopsy history is unclear
       - Include all breast biopsies regardless of result
    
    6. **Atypical Hyperplasia on Breast Biopsy**
       - **Only relevant if previous biopsies ≥1**
       - **Yes**: Atypical ductal hyperplasia (ADH) or atypical lobular hyperplasia (ALH)
       - **No**: No atypical hyperplasia found on any biopsy
       - **Unknown**: When pathology results are not available
       - High-risk lesion that significantly increases breast cancer risk
    
    7. **Race/Ethnicity**
       - **White**: Non-Hispanic White
       - **African-American**: Black or African-American
       - **Hispanic**: Hispanic or Latina (any race)
       - **Asian-American**: Asian or Pacific Islander
       - **American Indian/Alaska Native**: Indigenous populations
       - **Unknown**: When race/ethnicity is not specified
    
    8. **Asian Sub-Race** (if Asian-American selected)
       - **Chinese**: Chinese ancestry
       - **Japanese**: Japanese ancestry
       - **Filipino**: Filipino ancestry
       - **Hawaiian**: Native Hawaiian
       - **Pacific Islander**: Other Pacific Islander
    
    **CLINICAL DECISION THRESHOLDS**:
    
    **5-Year Risk <1.67%**: Low Risk
    - Continue routine screening mammography according to guidelines
    - Discuss general risk reduction strategies
    - Consider lifestyle modifications (healthy weight, physical activity, limit alcohol)
    - Routine clinical breast examinations
    
    **5-Year Risk ≥1.67%**: High Risk (FDA threshold for chemoprevention)
    - **Chemoprevention Options**:
      - Tamoxifen: For pre- and postmenopausal women
      - Raloxifene: For postmenopausal women only
      - Aromatase inhibitors: For postmenopausal women
    - **Enhanced Screening**:
      - Earlier screening initiation
      - Shorter screening intervals
      - Consider breast MRI for very high-risk women
    - **Genetic Counseling**: If strong family history or multiple risk factors
    - **Risk-Benefit Analysis**: Carefully weigh benefits vs. risks of interventions
    
    **CLINICAL CONSIDERATIONS**:
    - Model provides estimates, not definitive predictions
    - Individual counseling essential for high-risk women
    - Consider patient preferences and values in decision-making
    - Regular reassessment as risk factors may change over time
    - Integration with other risk assessment tools when appropriate
    
    References (Vancouver style):
    1. Gail MH, Brinton LA, Byar DP, et al. Projecting individualized probabilities of 
       developing breast cancer for white females who are being examined annually. 
       J Natl Cancer Inst. 1989;81(24):1879-86.
    2. Costantino JP, Gail MH, Pee D, et al. Validation studies for models projecting 
       the risk of invasive and total breast cancer incidence. J Natl Cancer Inst. 
       1999;91(18):1541-8.
    3. Matsuno RK, Costantino JP, Ziegler RG, et al. Projecting individualized absolute 
       invasive breast cancer risk in Asian and Pacific Islander American women. 
       J Natl Cancer Inst. 2011;103(12):951-61.
    """
    
    age: int = Field(
        ...,
        description="Current age of the woman (35-85 years)",
        ge=35,
        le=85,
        example=45
    )
    
    age_at_menarche: Literal["unknown", "7_to_11", "12_to_13", "over_13"] = Field(
        ...,
        description="Age at first menstrual period. Earlier menarche increases risk due to longer estrogen exposure",
        example="12_to_13"
    )
    
    age_at_first_birth: Literal["unknown", "no_births", "under_20", "20_to_24", "25_to_29", "30_or_over"] = Field(
        ...,
        description="Age at first live birth or nulliparous status. Later first birth and nulliparity increase risk",
        example="25_to_29"
    )
    
    relatives_with_breast_cancer: Literal["unknown", "0", "1", "more_than_1"] = Field(
        ...,
        description="Number of first-degree relatives (mother, sisters, daughters) with breast cancer",
        example="0"
    )
    
    previous_biopsies: Literal["unknown", "0", "1", "more_than_1"] = Field(
        ...,
        description="Number of previous breast biopsies (regardless of result). Each biopsy increases risk",
        example="0"
    )
    
    atypical_hyperplasia: Literal["unknown", "no", "yes"] = Field(
        ...,
        description="Presence of atypical hyperplasia (ADH or ALH) on breast biopsy. Only relevant if previous biopsies ≥1",
        example="no"
    )
    
    race_ethnicity: Literal["white", "african_american", "hispanic", "asian_american", "american_indian_alaskan_native", "unknown"] = Field(
        ...,
        description="Race/ethnicity for risk adjustment. Model validated for specific populations",
        example="white"
    )
    
    asian_subrace: Optional[Literal["chinese", "japanese", "filipino", "hawaiian", "pacific_islander"]] = Field(
        None,
        description="Asian sub-race (required only if race_ethnicity is asian_american)",
        example=None
    )
    
    @validator('asian_subrace')
    def validate_asian_subrace(cls, v, values):
        if values.get('race_ethnicity') == 'asian_american' and v is None:
            raise ValueError('asian_subrace is required when race_ethnicity is asian_american')
        if values.get('race_ethnicity') != 'asian_american' and v is not None:
            raise ValueError('asian_subrace should only be provided when race_ethnicity is asian_american')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "age_at_menarche": "12_to_13",
                "age_at_first_birth": "25_to_29",
                "relatives_with_breast_cancer": "0",
                "previous_biopsies": "0",
                "atypical_hyperplasia": "no",
                "race_ethnicity": "white",
                "asian_subrace": None
            }
        }


class GailModelBreastCancerRiskResponse(BaseModel):
    """
    Response model for Gail Model Breast Cancer Risk Assessment
    
    The response provides the calculated 5-year absolute breast cancer risk along with 
    risk classification and evidence-based clinical recommendations for screening, 
    prevention, and management.
    
    **RISK INTERPRETATION AND CLINICAL MANAGEMENT**:
    
    **Low Risk (<1.67% 5-year risk)**:
    - **Clinical Significance**: Below FDA threshold for chemoprevention consideration
    - **Screening Recommendations**:
      - Annual mammography starting age 40-50 (per guidelines)
      - Clinical breast examination every 1-3 years (ages 20-39), annually (40+)
      - Breast self-awareness education
    - **Prevention Strategies**:
      - Maintain healthy body weight (BMI 18.5-24.9)
      - Regular physical activity (≥150 minutes moderate intensity weekly)
      - Limit alcohol consumption (<1 drink/day)
      - Avoid unnecessary postmenopausal hormone therapy
      - Breastfeeding if planning children (protective effect)
    - **Follow-up**: Reassess risk periodically or if risk factors change
    
    **High Risk (≥1.67% 5-year risk)**:
    - **Clinical Significance**: Meets FDA threshold for chemoprevention consideration
    - **Comprehensive Risk Assessment**:
      - Detailed family history and pedigree analysis
      - Consider genetic counseling referral if strong family history
      - Assess for BRCA1/BRCA2 or other high-penetrance mutations
      - Evaluate life expectancy and comorbidities
    - **Chemoprevention Options** (discuss benefits vs. risks):
      - **Tamoxifen**: 
        - Reduces invasive breast cancer risk by ~50%
        - Suitable for pre- and postmenopausal women
        - Consider if 5-year risk >1.67% and life expectancy >10 years
        - Risks: VTE, endometrial cancer, cataracts, vasomotor symptoms
      - **Raloxifene** (postmenopausal women only):
        - Reduces invasive breast cancer risk by ~38%
        - May preserve bone density
        - Lower endometrial cancer risk than tamoxifen
        - Similar VTE risk to tamoxifen
      - **Aromatase Inhibitors** (postmenopausal women):
        - Exemestane or anastrozole
        - Reduce breast cancer risk by ~50-65%
        - Consider for women with contraindications to SERMs
        - Risks: bone loss, arthralgia, cardiovascular effects
    
    **Enhanced Screening Strategies**:
    - **Earlier Initiation**: Consider starting at age 40 or 10 years before youngest affected relative
    - **Increased Frequency**: Annual mammography, consider every 6 months for very high-risk
    - **Additional Modalities**:
      - Breast MRI annually for lifetime risk >20-25%
      - Consider tomosynthesis (3D mammography)
      - Ultrasound as adjunct in dense breast tissue
    - **Clinical Surveillance**:
      - Clinical breast examination every 6 months
      - Provider with expertise in high-risk breast management
      - Coordinate care with breast imaging specialists
    
    **Genetic Counseling Referral Criteria**:
    - Personal history of breast cancer <50 years
    - Bilateral breast cancer
    - Personal history of ovarian cancer
    - Male breast cancer in family
    - ≥2 first-degree relatives with breast cancer
    - First-degree relative with breast cancer <50 years
    - Ashkenazi Jewish ancestry with family history
    - Personal or family history of pancreatic or prostate cancer
    
    **Shared Decision-Making Process**:
    - Present quantitative risk estimates clearly
    - Discuss patient's perception and concerns about breast cancer
    - Review benefits and risks of each intervention
    - Consider patient's preferences, values, and quality of life priorities
    - Provide decision aids and educational materials
    - Allow time for reflection and discussion with family
    - Document shared decision-making process and final decisions
    
    **Monitoring and Follow-up**:
    - **Risk Reassessment**: Every 5 years or when risk factors change
    - **Adherence Monitoring**: For women choosing chemoprevention
    - **Adverse Event Monitoring**: Regular assessment for medication side effects
    - **Screening Compliance**: Ensure adherence to enhanced screening recommendations
    - **Family History Updates**: Reassess as new family history information becomes available
    
    **Special Populations**:
    - **Pregnancy/Lactation**: Defer chemoprevention, adjust screening timing
    - **DCIS History**: Use modified risk assessment approaches
    - **Strong Family History**: Consider multi-gene panel testing
    - **Racial/Ethnic Minorities**: Consider population-specific validation data
    
    **Quality Measures**:
    - Documented risk assessment using validated tool
    - Appropriate referral for genetic counseling when indicated
    - Shared decision-making for high-risk women
    - Patient education and counseling documentation
    - Follow-up plan for risk reassessment
    
    **Limitations to Discuss with Patients**:
    - Model provides population-based estimates, not individual certainty
    - Does not account for all risk factors (lifestyle, environmental)
    - May underestimate risk in certain populations
    - Requires periodic reassessment as risk factors change
    - Should be one component of comprehensive breast health assessment
    
    Reference: Gail MH, et al. J Natl Cancer Inst. 1989;81(24):1879-86.
    """
    
    result: float = Field(
        ...,
        description="5-year absolute risk of developing invasive breast cancer (percentage)",
        ge=0,
        le=50.0,
        example=2.1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk estimate",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk level, clinical significance, and evidence-based management recommendations",
        example="5-year breast cancer risk of 2.1% meets or exceeds the 1.67% threshold. Consider discussing chemoprevention options (tamoxifen, raloxifene, or aromatase inhibitors) with patient after evaluating benefits and risks. Enhanced screening strategies may be appropriate including earlier screening initiation, shorter screening intervals, or consideration of breast MRI."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on 5-year risk threshold (Low Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High risk for breast cancer"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.1,
                "unit": "percentage",
                "interpretation": "5-year breast cancer risk of 2.1% meets or exceeds the 1.67% threshold. Consider discussing chemoprevention options (tamoxifen, raloxifene, or aromatase inhibitors) with patient after evaluating benefits and risks. Enhanced screening strategies may be appropriate including earlier screening initiation, shorter screening intervals, or consideration of breast MRI. Genetic counseling may be considered if family history is significant.",
                "stage": "High Risk",
                "stage_description": "High risk for breast cancer"
            }
        }