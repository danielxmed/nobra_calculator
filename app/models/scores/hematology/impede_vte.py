"""
IMPEDE-VTE Models

Request and response models for IMPEDE-VTE calculation.

References (Vancouver style):
1. Sanfilippo KM, Luo S, Wang TF, et al. Predicting venous thromboembolism in 
   multiple myeloma: development and validation of the IMPEDE VTE score. 
   Am J Hematol. 2019 Nov;94(11):1176-1184. doi: 10.1002/ajh.25603.
2. Sanfilippo KM, Luo S, Wang TF, et al. Validation of the IMPEDE VTE score 
   for prediction of venous thromboembolism in multiple myeloma: a retrospective 
   cohort study. Br J Haematol. 2021 Jun;193(5):1005-1015. doi: 10.1111/bjh.17396.
3. Li A, Wu Q, Luo S, et al. Derivation and validation of a risk assessment 
   model for immunomodulatory drug-associated thrombosis among patients with 
   multiple myeloma. J Natl Compr Canc Netw. 2019 Jul 1;17(7):840-847. 
   doi: 10.6004/jnccn.2018.7273.
4. National Comprehensive Cancer Network. Multiple Myeloma (Version 3.2023). 
   https://www.nccn.org/professionals/physician_gls/pdf/myeloma.pdf

The IMPEDE-VTE score predicts venous thromboembolism risk in multiple myeloma 
patients receiving treatment. Developed and validated in large cohorts, this 
score helps identify patients at highest risk for VTE during multiple myeloma 
treatment. Multiple myeloma patients have a 9-fold increased VTE risk compared 
to the general population. The score is incorporated into NCCN guidelines and 
stratifies patients into low (3.8-5.0% 6-month VTE incidence), intermediate 
(8.6-12.6%), and high risk (24.1-40.5%) categories.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImpedeVteRequest(BaseModel):
    """
    Request model for IMPEDE-VTE score calculation
    
    Predicts risk of venous thromboembolism (VTE) in patients with multiple myeloma
    receiving treatment. The IMPEDE-VTE score was developed and validated to identify
    multiple myeloma patients at highest risk for VTE during treatment.
    
    Risk Factors Assessed:
    - Immunomodulatory drugs (IMiDs): Lenalidomide, thalidomide, pomalidomide
    - Patient factors: BMI, ethnicity, previous VTE history
    - Disease factors: Pathologic fractures, bone lesions
    - Treatment factors: Dexamethasone dose, doxorubicin, ESAs
    - Protective factors: Anticoagulation therapy
    - Access factors: Central venous catheters
    
    The score ranges from -7 to +19 points and stratifies patients into:
    - Low risk (≤3 points): 3.8-5.0% 6-month VTE incidence
    - Intermediate risk (4-7 points): 8.6-12.6% 6-month VTE incidence  
    - High risk (≥8 points): 24.1-40.5% 6-month VTE incidence
    
    Multiple myeloma patients have a 9-fold increased VTE risk compared to the 
    general population, making risk stratification essential for appropriate 
    thromboprophylaxis decisions.

    References (Vancouver style):
    1. Sanfilippo KM, Luo S, Wang TF, et al. Predicting venous thromboembolism in 
       multiple myeloma: development and validation of the IMPEDE VTE score. 
       Am J Hematol. 2019 Nov;94(11):1176-1184. doi: 10.1002/ajh.25603.
    2. Sanfilippo KM, Luo S, Wang TF, et al. Validation of the IMPEDE VTE score 
       for prediction of venous thromboembolism in multiple myeloma: a retrospective 
       cohort study. Br J Haematol. 2021 Jun;193(5):1005-1015. doi: 10.1111/bjh.17396.
    3. Li A, Wu Q, Luo S, et al. Derivation and validation of a risk assessment 
       model for immunomodulatory drug-associated thrombosis among patients with 
       multiple myeloma. J Natl Compr Canc Netw. 2019 Jul 1;17(7):840-847. 
       doi: 10.6004/jnccn.2018.7273.
    """
    
    immunomodulatory_drug: Literal["yes", "no"] = Field(
        ...,
        description="Use of immunomodulatory drugs (lenalidomide, thalidomide, pomalidomide). IMiDs significantly increase VTE risk in multiple myeloma patients through multiple mechanisms including increased platelet aggregation and endothelial dysfunction. Scores 4 points if yes",
        example="yes"
    )
    
    bmi_25_or_greater: Literal["yes", "no"] = Field(
        ...,
        description="Body mass index ≥25 kg/m². Overweight and obesity are established risk factors for VTE through multiple mechanisms including increased inflammatory markers, decreased mobility, and compression of venous return. Scores 1 point if yes",
        example="yes"
    )
    
    pelvic_hip_femur_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Pathologic fracture of pelvis, hip, or femur. Bone lesions and fractures are common in multiple myeloma and significantly increase VTE risk through immobilization and local inflammatory processes. Scores 4 points if yes",
        example="no"
    )
    
    erythropoiesis_stimulating_agent: Literal["yes", "no"] = Field(
        ...,
        description="Use of erythropoiesis-stimulating agents (ESAs) such as erythropoietin or darbepoetin. ESAs increase VTE risk by raising hematocrit and blood viscosity, and may increase platelet reactivity. Scores 1 point if yes",
        example="no"
    )
    
    doxorubicin_use: Literal["yes", "no"] = Field(
        ...,
        description="Use of doxorubicin as part of multiple myeloma treatment regimen. Doxorubicin increases VTE risk through endothelial damage and increased coagulation factor activity. Scores 3 points if yes",
        example="no"
    )
    
    dexamethasone_use: Literal["none", "low_dose", "high_dose"] = Field(
        ...,
        description="Dexamethasone dosing level. High-dose dexamethasone (≥160mg/month or ≥40mg/week) significantly increases VTE risk more than low-dose regimens through effects on coagulation factors and platelet function. Scores 2 points for low dose, 4 points for high dose",
        example="low_dose"
    )
    
    asian_pacific_islander: Literal["yes", "no"] = Field(
        ...,
        description="Asian or Pacific Islander ethnicity. This population has lower baseline VTE risk compared to other ethnicities, possibly due to genetic factors affecting coagulation cascade and fibrinolysis. Scores -3 points if yes",
        example="no"
    )
    
    history_of_vte: Literal["yes", "no"] = Field(
        ...,
        description="History of venous thromboembolism (deep vein thrombosis or pulmonary embolism) prior to multiple myeloma diagnosis. Previous VTE is the strongest predictor of recurrent thrombotic events. Scores 5 points if yes",
        example="no"
    )
    
    tunneled_line_cvc: Literal["yes", "no"] = Field(
        ...,
        description="Presence of tunneled central venous catheter or central line. Central venous catheters increase VTE risk through direct endothelial injury, flow disruption, and serving as nidus for thrombus formation. Scores 2 points if yes",
        example="no"
    )
    
    therapeutic_anticoagulation: Literal["yes", "no"] = Field(
        ...,
        description="Current therapeutic anticoagulation with warfarin or low molecular weight heparin (LMWH). Therapeutic anticoagulation significantly reduces VTE risk when used appropriately. Scores -4 points if yes",
        example="no"
    )
    
    prophylactic_anticoagulation: Literal["yes", "no"] = Field(
        ...,
        description="Current prophylactic anticoagulation with low molecular weight heparin (LMWH) or aspirin. Prophylactic measures provide moderate VTE risk reduction in high-risk patients. Scores -3 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "immunomodulatory_drug": "yes",
                "bmi_25_or_greater": "yes",
                "pelvic_hip_femur_fracture": "no",
                "erythropoiesis_stimulating_agent": "no",
                "doxorubicin_use": "no",
                "dexamethasone_use": "low_dose",
                "asian_pacific_islander": "no",
                "history_of_vte": "no",
                "tunneled_line_cvc": "no",
                "therapeutic_anticoagulation": "no",
                "prophylactic_anticoagulation": "no"
            }
        }


class ImpedeVteResponse(BaseModel):
    """
    Response model for IMPEDE-VTE score calculation
    
    Returns the IMPEDE-VTE score with risk stratification and clinical recommendations
    for venous thromboembolism prevention in multiple myeloma patients.
    
    Risk Categories:
    - Low Risk (≤3 points): 3.8-5.0% 6-month VTE incidence - Standard monitoring
    - Intermediate Risk (4-7 points): 8.6-12.6% 6-month VTE incidence - Consider prophylaxis
    - High Risk (≥8 points): 24.1-40.5% 6-month VTE incidence - Prophylaxis recommended
    
    The score is incorporated into NCCN Multiple Myeloma Guidelines and outperforms
    previous risk assessment tools for VTE prediction in this population.
    
    Reference: Sanfilippo KM, et al. Am J Hematol. 2019;94(11):1176-1184.
    """
    
    result: int = Field(
        ...,
        description="IMPEDE-VTE score calculated from risk factors (range -7 to +19 points)",
        example=7,
        ge=-7,
        le=19
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and thromboprophylaxis recommendations based on the score",
        example="Intermediate VTE risk. 6-month cumulative VTE incidence 8.6-12.6%. Consider thromboprophylaxis with aspirin or low molecular weight heparin based on individual patient factors, bleeding risk, and treatment regimen. Regular monitoring recommended."
    )
    
    stage: str = Field(
        ...,
        description="VTE risk category (Low Risk, Intermediate Risk, or High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score range",
        example="Score 7 points (4-7 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "Intermediate VTE risk. 6-month cumulative VTE incidence 8.6-12.6%. Consider thromboprophylaxis with aspirin or low molecular weight heparin based on individual patient factors, bleeding risk, and treatment regimen. Regular monitoring recommended.",
                "stage": "Intermediate Risk",
                "stage_description": "Score 7 points (4-7 points)"
            }
        }