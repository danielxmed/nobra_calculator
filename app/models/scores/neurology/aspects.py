"""
Alberta Stroke Program Early CT Score (ASPECTS) Models

Request and response models for ASPECTS Score calculation.

References (Vancouver style):
1. Barber PA, Demchuk AM, Zhang J, Buchan AM. Validity and reliability of a 
   quantitative computed tomography score in predicting outcome of hyperacute 
   stroke before thrombolytic therapy. ASPECTS Study Group. Alberta Stroke 
   Programme Early CT Score. Lancet. 2000;355(9216):1670-4. 
   doi: 10.1016/S0140-6736(00)02237-6.
2. Pexman JH, Barber PA, Hill MD, Sevick RJ, Demchuk AM, Hudon ME, Hu WY, 
   Buchan AM. Use of the Alberta Stroke Program Early CT Score (ASPECTS) 
   for assessing CT scans in patients with acute stroke. AJNR Am J Neuroradiol. 
   2001;22(8):1534-42.
3. Goyal M, Demchuk AM, Menon BK, Eesa M, Rempel JL, Thornton J, et al. 
   Randomized assessment of rapid endovascular treatment of ischemic stroke. 
   N Engl J Med. 2015;372(11):1019-30. doi: 10.1056/NEJMoa1414905.

The ASPECTS score is a 10-point quantitative topographic CT scan score used to 
assess early ischemic changes in the middle cerebral artery (MCA) territory. 

Key Features:
- Evaluates 10 specific brain regions on non-contrast CT
- Start with 10 points, subtract 1 for each abnormal region
- Correlates inversely with NIHSS score and stroke severity
- Predicts 3-month functional outcome and symptomatic ICH risk
- Used for treatment selection in acute stroke

ASPECTS Regions:
Basal Ganglia Level: Caudate, Lentiform, Internal Capsule, Insular ribbon, M1, M2, M3
Supraganglionic Level: M4, M5, M6

Score Interpretation:
- 8-10: Favorable (good candidate for reperfusion therapy)
- 5-7: Large infarction (poor outcome, high hemorrhage risk)
- 0-4: Extensive infarction (very poor prognosis)
"""

from pydantic import BaseModel, Field
from typing import Literal, List


class AspectsRequest(BaseModel):
    """
    Request model for Alberta Stroke Program Early CT Score (ASPECTS)
    
    The ASPECTS score quantifies early ischemic changes in the MCA territory 
    on non-contrast CT to predict stroke outcome and guide treatment decisions.
    
    Evaluation Method:
    - Assess two standardized axial CT cuts
    - Basal ganglia level (thalamus and basal ganglia visible)
    - Supraganglionic level (just rostral to basal ganglia level)
    - Subtract 1 point for each region with ≥1/3 area involvement
    
    Regions Assessed:
    
    Basal Ganglia Level (7 regions):
    - Caudate nucleus
    - Lentiform nucleus (putamen + globus pallidus)
    - Internal capsule
    - Insular ribbon/cortex
    - M1: Anterior MCA cortex (frontal operculum)
    - M2: MCA cortex lateral to insular ribbon (anterior temporal)
    - M3: Posterior MCA cortex (posterior temporal)
    
    Supraganglionic Level (3 regions):
    - M4: Anterior MCA cortex (superior to M1)
    - M5: Lateral MCA cortex (superior to M2)
    - M6: Posterior MCA cortex (superior to M3)
    
    Clinical Applications:
    - Acute stroke prognostication
    - Treatment selection (IV thrombolysis, mechanical thrombectomy)
    - Risk stratification for symptomatic hemorrhage
    - Outcome prediction at 3 months
    - Research standardization
    
    Score Interpretation:
    - 10: Normal CT (all regions normal)
    - 8-10: Favorable (good candidate for reperfusion therapy)
    - 5-7: Large infarction (poor outcome, consider thrombectomy if ≥6)
    - 0-4: Extensive infarction (very poor prognosis, high hemorrhage risk)
    
    Important Notes:
    - Evaluate all axial cuts, not just two standardized levels
    - Requires focal edema or parenchymal hypoattenuation
    - Good interrater reliability with proper training
    - Correlates inversely with NIHSS score
    - Used in major stroke trials (ESCAPE, SWIFT-PRIME)

    References (Vancouver style):
    1. Barber PA, Demchuk AM, Zhang J, Buchan AM. Validity and reliability of a 
    quantitative computed tomography score in predicting outcome of hyperacute 
    stroke before thrombolytic therapy. ASPECTS Study Group. Alberta Stroke 
    Programme Early CT Score. Lancet. 2000;355(9216):1670-4. 
    doi: 10.1016/S0140-6736(00)02237-6.
    2. Pexman JH, Barber PA, Hill MD, Sevick RJ, Demchuk AM, Hudon ME, Hu WY, 
    Buchan AM. Use of the Alberta Stroke Program Early CT Score (ASPECTS) 
    for assessing CT scans in patients with acute stroke. AJNR Am J Neuroradiol. 
    2001;22(8):1534-42.
    3. Goyal M, Demchuk AM, Menon BK, Eesa M, Rempel JL, Thornton J, et al. 
    Randomized assessment of rapid endovascular treatment of ischemic stroke. 
    N Engl J Med. 2015;372(11):1019-30. doi: 10.1056/NEJMoa1414905.
    """
    
    caudate: Literal["normal", "abnormal"] = Field(
        ...,
        description="Caudate nucleus - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    lentiform: Literal["normal", "abnormal"] = Field(
        ...,
        description="Lentiform nucleus (putamen + globus pallidus) - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    internal_capsule: Literal["normal", "abnormal"] = Field(
        ...,
        description="Internal capsule - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="abnormal"
    )
    
    insular_ribbon: Literal["normal", "abnormal"] = Field(
        ...,
        description="Insular ribbon/cortex - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="abnormal"
    )
    
    m1: Literal["normal", "abnormal"] = Field(
        ...,
        description="M1 - Anterior MCA cortex (frontal operculum) - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    m2: Literal["normal", "abnormal"] = Field(
        ...,
        description="M2 - MCA cortex lateral to insular ribbon (anterior temporal) - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="abnormal"
    )
    
    m3: Literal["normal", "abnormal"] = Field(
        ...,
        description="M3 - Posterior MCA cortex (posterior temporal) - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    m4: Literal["normal", "abnormal"] = Field(
        ...,
        description="M4 - Anterior MCA cortex superior to M1 - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    m5: Literal["normal", "abnormal"] = Field(
        ...,
        description="M5 - Lateral MCA cortex superior to M2 - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    m6: Literal["normal", "abnormal"] = Field(
        ...,
        description="M6 - Posterior MCA cortex superior to M3 - focal edema or parenchymal hypoattenuation (≥1/3 area involvement)",
        example="normal"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "caudate": "normal",
                "lentiform": "normal", 
                "internal_capsule": "abnormal",
                "insular_ribbon": "abnormal",
                "m1": "normal",
                "m2": "abnormal",
                "m3": "normal",
                "m4": "normal",
                "m5": "normal",
                "m6": "normal"
            }
        }


class AspectsResponse(BaseModel):
    """
    Response model for Alberta Stroke Program Early CT Score (ASPECTS)
    
    The response provides the calculated ASPECTS score with detailed clinical 
    interpretation and treatment recommendations for acute stroke management.
    
    Score Interpretations:
    
    ASPECTS 8-10 (Favorable):
    * Limited early ischemic changes
    * Good prognosis for functional outcome
    * Low risk of symptomatic hemorrhage
    * Good candidate for reperfusion therapy
    * Greater benefit from IV thrombolysis expected
    
    ASPECTS 5-7 (Large Infarction):
    * Large MCA territory involvement
    * Poor functional outcome likely
    * High risk (14%) of symptomatic ICH with IV thrombolysis
    * Mechanical thrombectomy may be considered if ASPECTS ≥6
    * Careful risk-benefit assessment required
    
    ASPECTS 0-4 (Extensive Infarction):
    * Extensive MCA territory involvement
    * Very poor prognosis
    * Very high risk of symptomatic hemorrhage
    * Consider palliative care discussions
    * Reperfusion therapy generally not recommended
    
    Clinical Decision Support:
    - Treatment selection (IV tPA, mechanical thrombectomy)
    - Risk stratification for symptomatic hemorrhage
    - Prognostication for functional outcome
    - Resource allocation and care planning
    - Family discussions and expectations
    
    Important Considerations:
    - Correlates inversely with NIHSS score
    - Predicts 3-month functional outcome
    - Used in major stroke trials for patient selection
    - Should be combined with clinical assessment
    - Time from onset affects treatment decisions
    
    Reference: Barber PA, et al. Lancet. 2000;355(9216):1670-4.
    """
    
    result: int = Field(
        ...,
        description="ASPECTS score (0-10 points, 10=normal, 0=extensive infarction)",
        ge=0,
        le=10,
        example=7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with treatment recommendations",
        example="ASPECTS score: 7/10 points (Large Infarction). Abnormal regions: Internal capsule, Insular ribbon/cortex, M2 - MCA cortex lateral to insular ribbon. Prognosis: Poor. Hemorrhage risk: High (14% with IV tPA). TREATMENT: Large infarction present. Poor functional outcome likely. High risk (14%) of symptomatic ICH with IV thrombolysis. Mechanical thrombectomy may still be considered if ASPECTS ≥6 and within time window. CLINICAL CONTEXT: ASPECTS correlates inversely with NIHSS score and stroke severity. Score predicts 3-month functional outcome and symptomatic ICH risk. Use with clinical assessment, time from onset, and other imaging findings. IMPORTANT: ASPECTS should be evaluated on all axial CT cuts, not just two standardized levels. Requires assessment for ≥1/3 area involvement in each region. Consider stroke team consultation for treatment decisions."
    )
    
    stage: str = Field(
        ...,
        description="Prognostic category (Favorable, Large Infarction, Extensive Infarction)",
        example="Large Infarction"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the infarction extent",
        example="Large MCA territory involvement"
    )
    
    abnormal_regions: List[str] = Field(
        ...,
        description="List of brain regions with abnormal findings",
        example=[
            "Internal capsule",
            "Insular ribbon/cortex", 
            "M2 - MCA cortex lateral to insular ribbon"
        ]
    )
    
    prognosis: str = Field(
        ...,
        description="Overall prognosis assessment",
        example="Poor"
    )
    
    hemorrhage_risk: str = Field(
        ...,
        description="Risk of symptomatic hemorrhage with thrombolysis",
        example="High (14% with IV tPA)"
    )
    
    treatment_recommendation: str = Field(
        ...,
        description="General treatment recommendation category",
        example="Mechanical thrombectomy may be considered if ≥6"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "ASPECTS score: 7/10 points (Large Infarction). Abnormal regions: Internal capsule, Insular ribbon/cortex, M2 - MCA cortex lateral to insular ribbon. Prognosis: Poor. Hemorrhage risk: High (14% with IV tPA). TREATMENT: Large infarction present. Poor functional outcome likely. High risk (14%) of symptomatic ICH with IV thrombolysis. Mechanical thrombectomy may still be considered if ASPECTS ≥6 and within time window. CLINICAL CONTEXT: ASPECTS correlates inversely with NIHSS score and stroke severity. Score predicts 3-month functional outcome and symptomatic ICH risk. Use with clinical assessment, time from onset, and other imaging findings. IMPORTANT: ASPECTS should be evaluated on all axial CT cuts, not just two standardized levels. Requires assessment for ≥1/3 area involvement in each region. Consider stroke team consultation for treatment decisions.",
                "stage": "Large Infarction",
                "stage_description": "Large MCA territory involvement",
                "abnormal_regions": [
                    "Internal capsule",
                    "Insular ribbon/cortex",
                    "M2 - MCA cortex lateral to insular ribbon"
                ],
                "prognosis": "Poor",
                "hemorrhage_risk": "High (14% with IV tPA)",
                "treatment_recommendation": "Mechanical thrombectomy may be considered if ≥6"
            }
        }