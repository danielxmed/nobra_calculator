"""
Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score Models

Request and response models for DELTA-P Score calculation.

References (Vancouver style):
1. Titulaer MJ, Maddison P, Sont JK, Wirtz PW, Hilton-Jones D, Klooster R, et al. 
   Clinical Dutch-English Lambert-Eaton Myasthenic syndrome (LEMS) tumor association 
   prediction score accurately predicts small-cell lung cancer in the LEMS. 
   J Clin Oncol. 2011;29(7):902-8. doi: 10.1200/JCO.2010.32.0440.
2. van Sonderen A, Wirtz PW, Verschuuren JJ, Titulaer MJ. Paraneoplastic syndromes 
   of the neuromuscular junction: therapeutic implications. Brain. 2016;139(Pt 10):2759-71. 
   doi: 10.1093/brain/aww199.
3. Titulaer MJ, Wirtz PW, Willems LN, van Kralingen KW, Smitt PA, Verschuuren JJ. 
   Screening for small-cell lung cancer: a follow-up study of patients with Lambert-Eaton 
   myasthenic syndrome. J Clin Oncol. 2008;26(26):4276-81. doi: 10.1200/JCO.2008.17.1302.

The Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score is a validated 
clinical prediction tool developed to identify Lambert-Eaton myasthenic syndrome (LEMS) 
patients at high risk for underlying small-cell lung cancer (SCLC). The score uses 
6 clinical parameters assessed at or within 3 months of LEMS symptom onset to provide 
risk stratification for intensive cancer screening protocols.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DeltaPScoreRequest(BaseModel):
    """
    Request model for Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score
    
    The DELTA-P Score uses 6 clinical parameters to predict small-cell lung cancer (SCLC) 
    risk in patients with Lambert-Eaton myasthenic syndrome (LEMS). Each parameter is 
    assessed at or within 3 months of LEMS symptom onset and scores 1 point if positive:
    
    Age at Onset:
    - under_50: Age <50 years at LEMS onset (0 points)
    - 50_or_over: Age ≥50 years at LEMS onset (1 point)
    
    Smoking Status:
    - current_smoker: Active smoking at time of LEMS diagnosis (1 point)
    - former_or_never: Former smoker or never smoked (0 points)
    
    Weight Loss:
    - yes: Weight loss >5% at or within 3 months of onset (1 point)
    - no: No significant weight loss (0 points)
    
    Bulbar Involvement:
    - yes: Presence of bulbar symptoms (dysphagia, dysarthria, ptosis, diplopia) (1 point)
    - no: No bulbar symptoms (0 points)
    
    Erectile Dysfunction:
    - yes: Present in male patients at or within 3 months of onset (1 point)
    - no: Absent or patient is female (0 points)
    
    Karnofsky Performance Status:
    - less_than_70: Karnofsky score <70 indicating significant functional impairment (1 point)
    - 70_or_greater: Karnofsky score ≥70 indicating preserved function (0 points)
    
    Clinical Background:
    Lambert-Eaton myasthenic syndrome is a rare autoimmune disorder affecting the 
    neuromuscular junction. Approximately 50-60% of LEMS patients have underlying 
    small-cell lung cancer (SCLC-LEMS), while 40-50% have non-tumor LEMS (NT-LEMS). 
    Early identification of SCLC is crucial as it significantly impacts treatment 
    approach and prognosis.
    
    Score Interpretation:
    - 0-1 points: Very low SCLC risk (0-2.6%), standard screening
    - 2 points: Low-moderate SCLC risk (~45%), enhanced screening every 6 months
    - 3-6 points: High SCLC risk (83.9-100%), intensive screening every 3 months
    
    References (Vancouver style):
    1. Titulaer MJ, Maddison P, Sont JK, Wirtz PW, Hilton-Jones D, Klooster R, et al. 
       Clinical Dutch-English Lambert-Eaton Myasthenic syndrome (LEMS) tumor association 
       prediction score accurately predicts small-cell lung cancer in the LEMS. 
       J Clin Oncol. 2011;29(7):902-8.
    2. van Sonderen A, Wirtz PW, Verschuuren JJ, Titulaer MJ. Paraneoplastic syndromes 
       of the neuromuscular junction: therapeutic implications. Brain. 2016;139(Pt 10):2759-71.
    """
    
    age_at_onset: Literal["under_50", "50_or_over"] = Field(
        ...,
        description="Age at onset of LEMS symptoms. Patients ≥50 years have higher SCLC risk and score 1 point",
        example="50_or_over"
    )
    
    smoking_status: Literal["current_smoker", "former_or_never"] = Field(
        ...,
        description="Smoking status at time of LEMS diagnosis. Current smoking is strongly associated with SCLC and scores 1 point",
        example="current_smoker"
    )
    
    weight_loss: Literal["yes", "no"] = Field(
        ...,
        description="Unintentional weight loss >5% at or within 3 months of LEMS onset. Significant weight loss suggests malignancy and scores 1 point",
        example="yes"
    )
    
    bulbar_involvement: Literal["yes", "no"] = Field(
        ...,
        description="Presence of bulbar symptoms (dysphagia, dysarthria, ptosis, diplopia) at or within 3 months of onset. Bulbar involvement scores 1 point",
        example="no"
    )
    
    erectile_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Presence of erectile dysfunction in male patients at or within 3 months of onset. Score as 'no' for female patients. Scores 1 point if present in males",
        example="no"
    )
    
    karnofsky_status: Literal["less_than_70", "70_or_greater"] = Field(
        ...,
        description="Karnofsky Performance Status at or within 3 months of onset. Score <70 indicates significant functional impairment and scores 1 point. (100=normal, 90=minor symptoms, 80=normal activity with effort, 70=unable to carry on normal activity but self-care, etc.)",
        example="less_than_70"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_at_onset": "50_or_over",
                "smoking_status": "current_smoker",
                "weight_loss": "yes",
                "bulbar_involvement": "no",
                "erectile_dysfunction": "no",
                "karnofsky_status": "less_than_70"
            }
        }


class DeltaPScoreResponse(BaseModel):
    """
    Response model for Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score
    
    The DELTA-P Score provides risk stratification for small-cell lung cancer (SCLC) in 
    Lambert-Eaton myasthenic syndrome (LEMS) patients, enabling appropriate screening protocols:
    
    Very Low Risk (0-1 points, 0-2.6% SCLC risk):
    - Management: Standard cancer screening protocols
    - Screening: Annual chest imaging sufficient unless other clinical factors present
    - Approach: Focus on neurological management of LEMS
    - Prognosis: Excellent with non-tumor LEMS, normal life expectancy
    
    Low-Moderate Risk (2 points, ~45% SCLC risk):
    - Management: Enhanced screening with chest CT every 6 months
    - Monitoring: Close follow-up for development of additional risk factors
    - Considerations: Balance screening intensity with patient anxiety and radiation exposure
    - Approach: Multidisciplinary care with neurology and oncology involvement
    
    High Risk (3-6 points, 83.9-100% SCLC risk):
    - Management: Immediate intensive cancer screening required
    - Screening: Chest CT every 3 months per guidelines, bronchoscopy if indicated
    - Team: Multidisciplinary oncology evaluation with thoracic surgery consultation
    - Urgency: Early detection and treatment critical as SCLC has poor prognosis
    - Treatment: Consider empirical treatment if imaging highly suggestive of SCLC
    
    Clinical Considerations:
    - SCLC median survival <2 years, making early detection crucial
    - Treatment of underlying SCLC can improve LEMS symptoms in some patients
    - SOX antibodies complement this scoring system and indicate SCLC-LEMS
    - High-risk patients require more aggressive immunosuppression for LEMS symptoms
    - Family counseling important given poor prognosis of SCLC
    
    Screening Protocols:
    - Low risk: Annual chest CT or chest X-ray
    - Moderate risk: Chest CT every 6 months
    - High risk: Chest CT every 3 months, consider PET-CT, bronchoscopy, mediastinoscopy
    - Additional: Consider abdominal/pelvic CT to exclude other tumor types
    
    Treatment Implications:
    - SCLC-LEMS: Combination immunosuppression often needed, monitor for tumor progression
    - NT-LEMS: Lower immunosuppression doses effective, better long-term prognosis
    - Both: 3,4-diaminopyridine (3,4-DAP) first-line symptomatic treatment
    - Severe cases: Plasmapheresis, IVIg, rituximab may be required
    
    Reference: Titulaer MJ, et al. J Clin Oncol. 2011;29(7):902-8.
    """
    
    result: int = Field(
        ...,
        description="DELTA-P score (0-6 points) for SCLC risk prediction in LEMS patients",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and screening recommendations based on SCLC risk level",
        example="High risk of small-cell lung cancer (DELTA-P score = 3, ~83.9% risk). Immediate and intensive cancer screening required with chest CT, bronchoscopy if indicated, and multidisciplinary oncology evaluation. Screen every 3 months as recommended for high-risk patients. Early detection and treatment of SCLC is critical for improved outcomes."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low-Moderate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High SCLC risk - intensive screening required"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "High risk of small-cell lung cancer (DELTA-P score = 3, ~83.9% risk). Immediate and intensive cancer screening required with chest CT, bronchoscopy if indicated, and multidisciplinary oncology evaluation. Screen every 3 months as recommended for high-risk patients. Early detection and treatment of SCLC is critical for improved outcomes.",
                "stage": "High Risk",
                "stage_description": "High SCLC risk - intensive screening required"
            }
        }