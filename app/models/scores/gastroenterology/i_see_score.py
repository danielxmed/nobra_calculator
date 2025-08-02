"""
Index of Severity for Eosinophilic Esophagitis (I-SEE) Models

Request and response models for I-SEE Score calculation.

References (Vancouver style):
1. Hirano I, Aceves SS, Blanchard C, et al. A Clinical Severity Index for Eosinophilic 
   Esophagitis: Development, Consensus, and Future Directions. Gastroenterology. 2022 
   Jul;163(1):59-76.e16. doi: 10.1053/j.gastro.2022.02.048.
2. Rank MA, Shaffer K, Campion J, et al. A newly proposed severity index for eosinophilic 
   esophagitis is associated with baseline clinical features and successful treatment response. 
   Clin Gastroenterol Hepatol. 2023 Oct;21(11):2890-2897.e2. doi: 10.1016/j.cgh.2023.04.013.
3. Stern E, Schoepfer A, Spechler SJ, et al. The Index of Severity for Eosinophilic 
   Esophagitis (I-SEE) Reflects Longitudinal Clinicopathologic Changes in Children. 
   J Pediatr Gastroenterol Nutr. 2023 Dec;77(6):743-749. doi: 10.1097/MPG.0000000000003928.

The Index of Severity for Eosinophilic Esophagitis (I-SEE) classifies severity of eosinophilic 
esophagitis (EoE) using a comprehensive scoring system that evaluates symptoms, complications, 
inflammatory features, and fibrostenotic changes. Developed by a multidisciplinary international 
group of EoE experts to standardize disease severity assessment beyond eosinophil counts alone. 
This validated clinical tool helps guide practitioners in EoE management by providing standardized 
disease severity classification that correlates with clinical features, treatment response, and 
need for interventions such as dilation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ISeeScoreRequest(BaseModel):
    """
    Request model for Index of Severity for Eosinophilic Esophagitis (I-SEE) calculation
    
    Classifies severity of eosinophilic esophagitis (EoE) using a comprehensive scoring 
    system that evaluates multiple disease domains:
    
    Domains Assessed:
    - Symptoms and Complications: Symptom frequency, food impaction, hospitalization, 
      perforation, malnutrition, persistent inflammation
    - Inflammatory Features: Endoscopic findings (edema, furrows, exudates) and 
      histologic eosinophil counts
    - Fibrostenotic Features: Presence and severity of esophageal rings or strictures
    
    Severity Classification:
    - Inactive (0 points): No evidence of active disease
    - Mild (1-6 points): Minimal functional impact, standard therapy typically effective
    - Moderate (7-14 points): Significant disease activity, may require combination therapy
    - Severe (≥15 points): High disease burden, may require advanced therapies or dilation
    
    The I-SEE standardizes disease severity assessment and helps guide clinical management 
    decisions, monitor treatment response, and predict need for interventions. It correlates 
    with clinical features including BMI, symptom duration, esophageal diameter, and predicts 
    need for dilation at follow-up.

    References (Vancouver style):
    1. Hirano I, Aceves SS, Blanchard C, et al. A Clinical Severity Index for Eosinophilic 
       Esophagitis: Development, Consensus, and Future Directions. Gastroenterology. 2022 
       Jul;163(1):59-76.e16. doi: 10.1053/j.gastro.2022.02.048.
    2. Rank MA, Shaffer K, Campion J, et al. A newly proposed severity index for eosinophilic 
       esophagitis is associated with baseline clinical features and successful treatment response. 
       Clin Gastroenterol Hepatol. 2023 Oct;21(11):2890-2897.e2. doi: 10.1016/j.cgh.2023.04.013.
    """
    
    symptoms_frequency: Literal["none", "weekly", "daily", "multiple_daily"] = Field(
        ...,
        description="Frequency of EoE-related symptoms (dysphagia, food getting stuck, chest pain, heartburn). Symptom frequency correlates with disease activity and quality of life impact. Scores: None (0), Weekly (1), Daily (2), Multiple times per day/disrupting social functioning (4)",
        example="weekly"
    )
    
    food_impaction: Literal["none", "adult_with_er", "pediatric_with_er"] = Field(
        ...,
        description="History of food impaction requiring emergency room visit or endoscopic removal. Food impaction is a serious complication that may require urgent intervention and indicates significant esophageal dysfunction. Scores: None (0), Adult with ER visit/endoscopy (2), Pediatric with ER visit/endoscopy (4)",
        example="none"
    )
    
    hospitalization_due_eoe: Literal["no", "yes"] = Field(
        ...,
        description="Hospitalization specifically due to EoE-related complications. Hospitalization indicates severe disease requiring inpatient management and represents significant healthcare burden. Scores: No (0), Yes (4)",
        example="no"
    )
    
    esophageal_perforation: Literal["no", "yes"] = Field(
        ...,
        description="History of esophageal perforation. Perforation is the most serious complication of EoE, often requiring surgical intervention and carrying significant morbidity risk. Scores: No (0), Yes (15)",
        example="no"
    )
    
    malnutrition: Literal["none", "present"] = Field(
        ...,
        description="Malnutrition defined as body mass <5th percentile or decreased growth velocity. Malnutrition indicates severe functional impact affecting nutritional status and growth, particularly important in pediatric patients. Scores: None (0), Present (15)",
        example="none"
    )
    
    persistent_inflammation: Literal["none", "present"] = Field(
        ...,
        description="Persistent inflammation requiring special treatments (immunosuppressives, biologics, elimination diets). Indicates refractory disease requiring advanced therapeutic interventions beyond standard topical steroids. Scores: None (0), Present (15)",
        example="none"
    )
    
    inflammatory_features: Literal["none", "localized", "diffuse"] = Field(
        ...,
        description="Endoscopic inflammatory features: edema, furrows, and exudates (EFE). These findings represent active inflammatory changes in the esophageal mucosa and correlate with disease activity. Scores: None (0), Localized (1), Diffuse (2)",
        example="localized"
    )
    
    eosinophil_count: Literal["under_15", "15_to_60", "over_60"] = Field(
        ...,
        description="Peak eosinophil count per high-power field (eos/hpf) on esophageal biopsy. Eosinophil count is the hallmark histologic feature of EoE, with ≥15 eos/hpf required for diagnosis. Scores: <15 eos/hpf (0), 15-60 eos/hpf (1), >60 eos/hpf (2)",
        example="15_to_60"
    )
    
    rings_strictures: Literal["none", "endoscope_passes_easily", "requires_dilation", "cannot_pass_endoscope"] = Field(
        ...,
        description="Presence and severity of esophageal rings or strictures. Fibrostenotic changes represent chronic remodeling and may require mechanical intervention (dilation) for symptom relief. Scores: None (0), Endoscope passes easily (1), Requires dilation/snug fit (2), Cannot pass endoscope/repeated dilations (15)",
        example="none"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "symptoms_frequency": "weekly",
                "food_impaction": "none",
                "hospitalization_due_eoe": "no",
                "esophageal_perforation": "no",
                "malnutrition": "none",
                "persistent_inflammation": "none",
                "inflammatory_features": "localized",
                "eosinophil_count": "15_to_60",
                "rings_strictures": "none"
            }
        }


class ISeeScoreResponse(BaseModel):
    """
    Response model for Index of Severity for Eosinophilic Esophagitis (I-SEE) calculation
    
    Returns the I-SEE Severity Score with disease classification and clinical 
    management recommendations for eosinophilic esophagitis patients.
    
    Severity Categories:
    - Inactive (0 points): No evidence of active disease
    - Mild (1-6 points): Disease present but minimal functional impact
    - Moderate (7-14 points): Significant disease activity with moderate functional impact
    - Severe (≥15 points): High disease burden with significant complications
    
    The I-SEE score provides standardized disease severity assessment that correlates 
    with clinical features and helps guide treatment decisions. Higher scores are 
    associated with lower BMI, longer symptom duration, smaller esophageal diameter, 
    and increased need for dilation. The score can be used to monitor treatment 
    response and adjust therapeutic approaches accordingly.
    
    Reference: Hirano I, et al. Gastroenterology. 2022;163(1):59-76.e16.
    """
    
    result: int = Field(
        ...,
        description="I-SEE Severity Score calculated from clinical domains (range 0-45 points)",
        example=3,
        ge=0,
        le=45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the severity score",
        example="Mild EoE severity. Disease is present but with minimal impact on function and low complication risk. Standard topical corticosteroid therapy typically effective."
    )
    
    stage: str = Field(
        ...,
        description="EoE severity category (Inactive, Mild, Moderate, Severe)",
        example="Mild"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category with score range",
        example="Score 3 points (1-6 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Mild EoE severity. Disease is present but with minimal impact on function and low complication risk. Standard topical corticosteroid therapy typically effective.",
                "stage": "Mild",
                "stage_description": "Score 3 points (1-6 points)"
            }
        }