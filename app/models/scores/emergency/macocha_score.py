"""
MACOCHA Score Models

Request and response models for MACOCHA Score calculation to predict difficult intubation in ICU patients.

References (Vancouver style):
1. De Jong A, Molinari N, Terzi N, Mongardon N, Arnal JM, Guitton C, et al. Early 
   identification of patients at risk for difficult intubation in the intensive care 
   unit: development and validation of the MACOCHA score in a multicenter cohort study. 
   Am J Respir Crit Care Med. 2013 Apr 15;187(8):832-9. doi: 10.1164/rccm.201210-1851OC.
2. De Jong A, Clavieras N, Conseil M, Coisel Y, Moury PH, Pouzeratte Y, et al. 
   Implementation of a combo videolaryngoscope for intubation in critically ill 
   patients: a before-after comparative study. Intensive Care Med. 2013 Dec;39(12):2144-52. 
   doi: 10.1007/s00134-013-3099-1.
3. Mosier JM, Whitmore SP, Bloom JW, Bohnert S, Cairns BA, Sakles JC. Video laryngoscopy 
   improves intubation success and reduces esophageal intubations compared to direct 
   laryngoscopy in the medical intensive care unit. Crit Care. 2013 Oct 11;17(5):R237. 
   doi: 10.1186/cc13061.

The MACOCHA Score predicts difficult intubation in ICU patients using seven clinical 
factors across patient-related, pathology-related, and operator-related domains. It was 
developed and validated in multicenter studies involving over 1,000 ICU intubations. 
The score has excellent negative predictive value (98%) for ruling out difficult intubation, 
making it particularly useful for identifying patients who can safely undergo standard 
intubation procedures.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MacochaScoreRequest(BaseModel):
    """
    Request model for MACOCHA Score
    
    The MACOCHA Score uses seven clinical factors to predict difficult intubation in ICU patients:
    
    Patient-Related Factors:
    - Mallampati III or IV: Visual assessment of tongue size relative to mouth opening (5 points)
      - Class I: Soft palate, uvula, fauces, pillars visible
      - Class II: Soft palate, uvula, fauces visible
      - Class III: Soft palate, base of uvula visible (5 points if present)
      - Class IV: Only soft palate visible (5 points if present)
    
    - Obstructive Sleep Apnea Syndrome: History of OSA or clinical suspicion (2 points)
      - Snoring, witnessed apneas, daytime sleepiness
      - Previous sleep study diagnosis
      - Use of CPAP or BiPAP therapy
    
    - Reduced Cervical Spine Mobility: Limited neck extension/flexion (1 point)
      - Cervical collar or immobilization
      - Arthritis, previous spine surgery
      - Ankylosing spondylitis, rheumatoid arthritis
    
    - Limited Mouth Opening: Interincisor distance <3 cm (1 point)
      - Temporomandibular joint dysfunction
      - Trismus from infection or trauma
      - Previous radiation therapy
    
    Pathology-Related Factors:
    - Coma: Glasgow Coma Scale ≤8 or unresponsive (1 point)
      - Altered mental status requiring intubation
      - Neurological conditions affecting airway reflexes
    
    - Severe Hypoxemia: SpO₂ <80% despite supplemental oxygen (1 point)
      - Acute respiratory failure
      - Severe pneumonia or ARDS
      - Pulmonary edema
    
    Operator-Related Factors:
    - Non-Anesthesiologist: Operator other than anesthesiology specialist (1 point)
      - Emergency medicine physician
      - Internal medicine/ICU physician
      - Resident or less experienced provider
    
    Score Interpretation:
    - 0-2 points: Low risk (<10% probability of difficult intubation)
    - 3-5 points: Intermediate risk (10-30% probability)
    - 6-12 points: High risk (>30% probability)
    
    Clinical Significance:
    - Area under curve: 0.89 (development), 0.86 (validation)
    - Sensitivity: 73%, Specificity: 89%
    - Negative predictive value: 98% (excellent for ruling out difficult intubation)
    - Positive predictive value: 36%
    
    References (Vancouver style):
    1. De Jong A, Molinari N, Terzi N, Mongardon N, Arnal JM, Guitton C, et al. Early 
    identification of patients at risk for difficult intubation in the intensive care 
    unit: development and validation of the MACOCHA score in a multicenter cohort study. 
    Am J Respir Crit Care Med. 2013 Apr 15;187(8):832-9. doi: 10.1164/rccm.201210-1851OC.
    2. De Jong A, Clavieras N, Conseil M, Coisel Y, Moury PH, Pouzeratte Y, et al. 
    Implementation of a combo videolaryngoscope for intubation in critically ill 
    patients: a before-after comparative study. Intensive Care Med. 2013 Dec;39(12):2144-52. 
    doi: 10.1007/s00134-013-3099-1.
    """
    
    mallampati_3_or_4: Literal["yes", "no"] = Field(
        ...,
        description="Mallampati score III or IV. Class III: soft palate and base of uvula visible. "
                   "Class IV: only soft palate visible. Scores 5 points if present",
        example="no"
    )
    
    obstructive_sleep_apnea: Literal["yes", "no"] = Field(
        ...,
        description="Obstructive sleep apnea syndrome. History of OSA, snoring, witnessed apneas, "
                   "or CPAP/BiPAP use. Scores 2 points if present",
        example="no"
    )
    
    reduced_cervical_mobility: Literal["yes", "no"] = Field(
        ...,
        description="Reduced mobility of cervical spine. Limited neck extension/flexion from "
                   "collar, arthritis, previous surgery, or inflammatory conditions. Scores 1 point if present",
        example="no"
    )
    
    limited_mouth_opening: Literal["yes", "no"] = Field(
        ...,
        description="Limited mouth opening less than 3 cm (interincisor distance). "
                   "TMJ dysfunction, trismus, or previous radiation. Scores 1 point if present",
        example="no"
    )
    
    coma: Literal["yes", "no"] = Field(
        ...,
        description="Coma (Glasgow Coma Scale ≤8 or unresponsive state). "
                   "Altered mental status requiring intubation. Scores 1 point if present",
        example="yes"
    )
    
    severe_hypoxemia: Literal["yes", "no"] = Field(
        ...,
        description="Severe hypoxemia with SpO₂ <80% despite supplemental oxygen. "
                   "Acute respiratory failure, severe pneumonia, or ARDS. Scores 1 point if present",
        example="yes"
    )
    
    non_anesthesiologist: Literal["yes", "no"] = Field(
        ...,
        description="Non-anesthesiologist operator. Emergency medicine, internal medicine, "
                   "ICU physician, or resident performing intubation. Scores 1 point if present",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "mallampati_3_or_4": "no",
                "obstructive_sleep_apnea": "no",
                "reduced_cervical_mobility": "no",
                "limited_mouth_opening": "no",
                "coma": "yes",
                "severe_hypoxemia": "yes",
                "non_anesthesiologist": "yes"
            }
        }


class MacochaScoreResponse(BaseModel):
    """
    Response model for MACOCHA Score
    
    The MACOCHA Score provides risk stratification for difficult intubation in ICU patients:
    
    Risk Categories:
    - Low Risk (0-2 points): <10% probability of difficult intubation
      Standard intubation preparation and techniques appropriate
      Negative predictive value of 98% makes this category highly reliable
    
    - Intermediate Risk (3-5 points): 10-30% probability of difficult intubation
      Enhanced preparation with video laryngoscopy and additional equipment
      Experienced intubator and backup airway plan recommended
    
    - High Risk (6-12 points): >30% probability of difficult intubation
      Comprehensive difficult airway preparation with fiberoptic bronchoscope
      Consider awake fiberoptic intubation and surgical airway backup
    
    Clinical Applications:
    - Pre-intubation risk assessment in ICU patients
    - Equipment and personnel preparation planning
    - Decision support for intubation approach and backup plans
    - Quality improvement and safety protocols
    
    Complications Prevention:
    Difficult intubation is associated with 51% vs 36% severe life-threatening 
    complications including severe hypoxia, cardiovascular collapse, cardiac arrest, 
    and death. Early identification allows for appropriate preparation.
    
    Reference: De Jong A, et al. Am J Respir Crit Care Med. 2013;187(8):832-9.
    """
    
    result: int = Field(
        ...,
        description="MACOCHA score calculated from clinical factors (range: 0-12 points)",
        ge=0,
        le=12,
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the MACOCHA score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment and preparation recommendations",
        example="MACOCHA Score Assessment:\\n\\nComponent Scores:\\n• Patient-related factors: 0 points\\n• Pathology-related factors: 2 points\\n• Operator-related factors: 1 points\\n• Total MACOCHA score: 3/12 points"
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on MACOCHA score",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of intubation difficulty risk",
        example="Intermediate risk for difficult intubation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "MACOCHA Score Assessment:\\n\\nComponent Scores:\\n• Patient-related factors: 0 points\\n• Pathology-related factors: 2 points\\n• Operator-related factors: 1 points\\n• Total MACOCHA score: 3/12 points\\n\\nRisk Assessment:\\n• Risk category: Intermediate Risk\\n• Probability of difficult intubation: 10-30%\\n• Negative predictive value: 98% (if score ≤2)\\n\\nPreparation Recommendations:\\n• Preparation level: Enhanced preparation with additional equipment\\n• Required equipment: Video laryngoscope, supraglottic airway devices, fiberoptic bronchoscope availability\\n• Personnel requirements: Experienced intubator, additional skilled assistant\\n• Backup plan: Supraglottic airway device, consider awake fiberoptic intubation",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk for difficult intubation"
            }
        }