"""
American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index Models

Request and response models for AUB-HAS2 cardiovascular risk assessment.

References (Vancouver style):
1. Dakik H, Chehab O, Eldirani M, Soud M, Kassas I, Almedani S, et al. A New Index 
   for Pre-Operative Cardiovascular Evaluation. J Am Coll Cardiol. 2019 Jul 9;73(26):
   3067-3078. doi: 10.1016/j.jacc.2019.04.023. PMID: 31272543.
2. Dakik H, Sbaity E, Msheik A, Kasmar A, Chehab O, Tamim H. AUB-HAS2 Cardiovascular 
   Risk Index: Performance in Surgical Subpopulations and Comparison to the Revised 
   Cardiac Risk Index. J Am Heart Assoc. 2020 May 19;9(10):e016228. 
   doi: 10.1161/JAHA.119.016228. PMID: 32423287; PMCID: PMC7429017.
3. Dakik H, Eldirani M, Kaspar C, Chehab O, Sbaity E, Msheik A, et al. Prospective 
   Validation of the AUB-HAS2 Cardiovascular Risk Index. Eur Heart J Qual Care Clin 
   Outcomes. 2021 Jan 8;7(1):96-97. doi: 10.1093/ehjqcco/qcaa077. PMID: 33043961.

The American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index is a simple, 
powerful preoperative risk stratification tool that uses 6 easily obtainable clinical 
variables to predict major cardiovascular events (death, myocardial infarction, or 
stroke) within 30 days after noncardiac surgery.

Developed and validated by Dakik et al. at the American University of Beirut in 2019, 
this index demonstrated superior discriminatory power compared to the widely used 
Revised Cardiac Risk Index (RCRI) in multiple large-scale validation studies involving 
over 1 million patients.

The HAS2 acronym represents:
- **H**eart disease history
- **A**ge ≥75 years
- **S**ymptoms (angina or dyspnea)
- **2** additional risk factors: anemia (hemoglobin <12 mg/dL) and surgery type 
  (vascular surgery and emergency surgery)

Clinical Application:
The AUB-HAS2 index is designed for preoperative cardiovascular risk assessment in 
patients scheduled for noncardiac surgery. It provides superior discriminatory ability 
with area under the curve (AUC) values ranging from 0.82-0.90 in validation studies, 
significantly outperforming other established risk indices.

Risk Stratification:
- **Low Risk (0-1 points)**: Event rate <1%, routine perioperative care
- **Intermediate Risk (2-3 points)**: Event rate 5-11%, consider enhanced monitoring
- **High Risk (≥4 points)**: Event rate >15%, requires cardiac consultation and 
  intensive perioperative management

The index has been extensively validated across diverse surgical populations and 
geographic regions, demonstrating consistent performance and clinical utility in 
perioperative risk assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AubHas2CardiovascularRiskIndexRequest(BaseModel):
    """
    Request model for American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index
    
    The AUB-HAS2 index uses 6 clinical variables to assess cardiovascular risk in 
    patients undergoing noncardiac surgery:
    
    Risk Factors (each worth 1 point):
    
    1. **History of Heart Disease**: 
       - Includes ischemic heart disease, congestive heart failure, valvular disease, 
         arrhythmias, or other significant cardiac conditions
       - Based on medical history, previous cardiac procedures, or documented cardiac disease
    
    2. **Age ≥75 Years**:
       - Advanced age is an independent risk factor for perioperative cardiac events
       - Reflects increased physiologic vulnerability and comorbidity burden
    
    3. **Symptoms of Angina or Dyspnea**:
       - Angina: chest pain or discomfort suggestive of myocardial ischemia
       - Dyspnea: shortness of breath that may indicate cardiac or pulmonary compromise
       - These symptoms suggest reduced functional capacity and underlying cardiovascular disease
    
    4. **Anemia (Hemoglobin <12 mg/dL)**:
       - Defined as hemoglobin concentration below 12 mg/dL regardless of gender
       - Anemia increases cardiac workload and reduces oxygen delivery capacity
       - Associated with increased perioperative morbidity and mortality
    
    5. **Vascular Surgery**:
       - High-risk surgical procedures involving vascular system
       - Includes procedures on aorta, carotid, peripheral vessels
       - Associated with higher cardiovascular stress and complication rates
    
    6. **Emergency Surgery**:
       - Urgent or emergent procedures that cannot be delayed
       - Prevents optimization of medical therapy and cardiovascular status
       - Associated with increased physiologic stress and complication risk
    
    Clinical Implementation:
    Each risk factor present contributes 1 point to the total score (range: 0-6 points).
    The score stratifies patients into three risk categories with specific event rates 
    and management recommendations, enabling informed perioperative decision-making.
    
    References (Vancouver style):
    1. Dakik H, Chehab O, Eldirani M, Soud M, Kassas I, Almedani S, et al. A New Index 
    for Pre-Operative Cardiovascular Evaluation. J Am Coll Cardiol. 2019;73(26):3067-3078.
    2. Dakik H, Sbaity E, Msheik A, Kasmar A, Chehab O, Tamim H. AUB-HAS2 Cardiovascular 
    Risk Index: Performance in Surgical Subpopulations and Comparison to the Revised 
    Cardiac Risk Index. J Am Heart Assoc. 2020;9(10):e016228.
    """
    
    history_heart_disease: Literal["no", "yes"] = Field(
        ...,
        description="History of heart disease including ischemic heart disease, congestive heart failure, valvular disease, arrhythmias, or other significant cardiac conditions. Contributes 1 point if present",
        example="no"
    )
    
    age_75_or_older: Literal["no", "yes"] = Field(
        ...,
        description="Patient age 75 years or older. Advanced age increases perioperative cardiovascular risk due to reduced physiologic reserve and increased comorbidity burden. Contributes 1 point if present",
        example="no"
    )
    
    symptoms_angina_dyspnea: Literal["no", "yes"] = Field(
        ...,
        description="Presence of angina (chest pain/discomfort suggestive of ischemia) or dyspnea (shortness of breath) indicating potential cardiac or pulmonary compromise and reduced functional capacity. Contributes 1 point if present",
        example="no"
    )
    
    anemia_hgb_less_12: Literal["no", "yes"] = Field(
        ...,
        description="Anemia defined as hemoglobin concentration less than 12 mg/dL (regardless of gender). Anemia increases cardiac workload, reduces oxygen delivery, and is associated with increased perioperative morbidity. Contributes 1 point if present",
        example="no"
    )
    
    vascular_surgery: Literal["no", "yes"] = Field(
        ...,
        description="High-risk vascular surgical procedures including aortic, carotid, or peripheral vascular operations. These procedures are associated with increased cardiovascular stress and higher complication rates. Contributes 1 point if present",
        example="no"
    )
    
    emergency_surgery: Literal["no", "yes"] = Field(
        ...,
        description="Emergency or urgent surgical procedure that cannot be delayed for optimization. Emergency surgery prevents preoperative medical therapy optimization and is associated with increased physiologic stress. Contributes 1 point if present",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "history_heart_disease": "no",
                "age_75_or_older": "no", 
                "symptoms_angina_dyspnea": "no",
                "anemia_hgb_less_12": "no",
                "vascular_surgery": "no",
                "emergency_surgery": "no"
            }
        }


class AubHas2CardiovascularRiskIndexResponse(BaseModel):
    """
    Response model for American University of Beirut (AUB)-HAS2 Cardiovascular Risk Index
    
    The AUB-HAS2 index provides cardiovascular risk stratification for noncardiac surgery 
    patients based on total score (0-6 points):
    
    Risk Categories and Clinical Management:
    
    **Low Risk (0-1 points)**:
    - Event Rate: <1% for major cardiovascular events at 30 days
    - Clinical Interpretation: Very low risk of death, myocardial infarction, or stroke
    - Management: Routine perioperative care without additional cardiac interventions
    - Monitoring: Standard perioperative monitoring protocols
    - Follow-up: Routine postoperative care
    
    **Intermediate Risk (2-3 points**:
    - Event Rate: 5-11% for major cardiovascular events at 30 days  
    - Clinical Interpretation: Moderate risk requiring enhanced perioperative management
    - Management: Consider preoperative cardiac consultation for risk factor optimization
    - Monitoring: Enhanced perioperative cardiac monitoring and telemetry
    - Interventions: Optimize medical therapy (beta-blockers, statins, ACE inhibitors)
    - Follow-up: Closer postoperative monitoring with cardiac biomarkers if indicated
    
    **High Risk (≥4 points)**:
    - Event Rate: >15% for major cardiovascular events at 30 days
    - Clinical Interpretation: High risk requiring comprehensive perioperative cardiac care
    - Management: Mandatory preoperative cardiac consultation and risk stratification
    - Monitoring: Intensive perioperative monitoring, consider arterial line and central access
    - Interventions: Aggressive medical optimization, consider delay if feasible for stabilization
    - Setting: Consider postoperative intensive care unit monitoring
    - Follow-up: Serial cardiac biomarkers, ECGs, and close cardiovascular monitoring
    
    Clinical Validation:
    The AUB-HAS2 index has been validated in over 1 million patients with superior 
    discriminatory performance (AUC 0.82-0.90) compared to other established risk indices 
    including the Revised Cardiac Risk Index. The index demonstrates consistent performance 
    across diverse surgical populations and geographic regions.
    
    Outcome Prediction:
    The score specifically predicts the composite outcome of all-cause mortality, 
    myocardial infarction, or stroke within 30 days after noncardiac surgery. This 
    clinically relevant endpoint guides perioperative management decisions and 
    resource allocation.
    
    Reference: Dakik H, et al. J Am Coll Cardiol. 2019;73(26):3067-3078.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=6,
        description="AUB-HAS2 cardiovascular risk score calculated by summing present risk factors (range: 0-6 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific management recommendations based on the calculated risk category and expected event rates",
        example="Moderate risk of major cardiovascular events within 30 days after surgery. Event rate 5-11%. Consider enhanced perioperative monitoring and cardiac consultation for optimization of medical therapy."
    )
    
    stage: str = Field(
        ...,
        description="Cardiovascular risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate cardiovascular risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Moderate risk of major cardiovascular events within 30 days after surgery. Event rate 5-11%. Consider enhanced perioperative monitoring and cardiac consultation for optimization of medical therapy.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate cardiovascular risk"
            }
        }