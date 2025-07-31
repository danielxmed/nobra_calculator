"""
El-Ganzouri Risk Index (EGRI) for Difficult Airway Models

Request and response models for EGRI calculation.

References (Vancouver style):
1. El-Ganzouri AR, McCarthy RJ, Tuman KJ, Tanck EN, Ivankovich AD. Preoperative airway 
   assessment: predictive value of a multivariate risk index. Anesth Analg. 1996;82(6):1197-204. 
   doi: 10.1097/00000539-199606000-00017.
2. Cortellazzi P, Caldiroli D, Byrne A, Sommariva A, Orena EF, Tramacere I. Defining and 
   developing expertise in tracheal intubation using a GlideScope for anaesthetists with 
   expertise in Macintosh direct laryngoscopy: an in-vivo longitudinal study. Anaesthesia. 
   2015;70(3):290-5. doi: 10.1111/anae.12878.
3. Caldiroli D, Cortellazzi P. A new difficult airway management algorithm based upon the 
   El Ganzouri Risk Index and GlideScope® videolaryngoscope. A new look for intubation? 
   Minerva Anestesiol. 2011;77(6):637-45.
4. Lundstrøm LH, Vester-Andersen M, Møller AM, Charuluxananan S, L'hermite J, Wetterslev J. 
   Poor prognostic value of the modified Mallampati score: a meta-analysis involving 177,088 
   patients. Br J Anaesth. 2011;107(5):659-67. doi: 10.1093/bja/aer292.

The El-Ganzouri Risk Index (EGRI), also known as the Simplified Airway Risk Index (SARI), 
is a validated preoperative assessment tool that predicts the likelihood of difficult airway 
using seven clinical parameters. It provides objective, evidence-based guidance for anesthesia 
planning and airway management strategy selection.

The EGRI evaluates anatomical and historical factors associated with difficult intubation:
- Mouth opening distance (inter-incisor gap)
- Thyromental distance (thyroid notch to mandible tip)
- Modified Mallampati classification
- Neck extension/flexion range of motion
- Ability to prognath (advance lower jaw)
- Patient body weight category
- Previous history of difficult intubation

A score ≥4 points indicates high risk of difficult airway (93.8% specificity) and warrants 
special precautions including experienced anesthesiologist, video laryngoscopy consideration, 
difficult airway equipment availability, and backup plans. Scores ≥7 may warrant awake 
fiberoptic intubation in some practice guidelines.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ElGanzouriRiskIndexDifficultAirwayRequest(BaseModel):
    """
    Request model for El-Ganzouri Risk Index (EGRI) for Difficult Airway
    
    The EGRI uses seven clinical parameters to assess difficult airway risk:
    
    Anatomical Assessment Parameters:
    
    1. Mouth Opening (Inter-incisor Distance):
    - ≥4 cm: Normal mouth opening (0 points)
    - <4 cm: Limited mouth opening, increases difficulty (+1 point)
    
    2. Thyromental Distance:
    - >6.5 cm: Adequate distance for laryngoscopy (0 points)  
    - 6.0-6.5 cm: Borderline distance (+1 point)
    - <6.0 cm: Short distance, anterior larynx position (+2 points)
    
    3. Modified Mallampati Classification:
    - Class I: Soft palate, fauces, uvula, pillars visible (0 points)
    - Class II: Soft palate, fauces, uvula visible (+1 point)
    - Class III: Soft palate, base of uvula visible (+2 points)
    - Class IV: Only hard palate visible (+2 points)
    
    4. Neck Movement (Extension/Flexion Range):
    - >90°: Normal neck mobility (0 points)
    - 80-90°: Slightly limited mobility (+1 point)
    - <80°: Significantly limited mobility (+2 points)
    
    5. Ability to Prognath (Advance Lower Jaw):
    - Yes: Can advance lower jaw beyond upper teeth (0 points)
    - No: Cannot advance lower jaw, limited mandibular mobility (+1 point)
    
    Patient Factors:
    
    6. Body Weight Category:
    - <90 kg: Normal weight range (0 points)
    - 90-110 kg: Moderate increase in soft tissue (+1 point)
    - >110 kg: Significant increase in soft tissue mass (+2 points)
    
    7. History of Difficult Intubation:
    - None: No previous difficult intubation (0 points)
    - Questionable: Uncertain or conflicting history (+1 point)
    - Definite: Documented previous difficult intubation (+2 points)
    
    Score Interpretation:
    - 0-3 points: Low risk of difficult airway (conventional techniques likely successful)
    - ≥4 points: High risk of difficult airway (93.8% specificity, consider special precautions)
    - ≥7 points: Very high risk (may warrant awake fiberoptic intubation)

    References (Vancouver style):
    1. El-Ganzouri AR, McCarthy RJ, Tuman KJ, Tanck EN, Ivankovich AD. Preoperative airway 
    assessment: predictive value of a multivariate risk index. Anesth Analg. 1996;82(6):1197-204. 
    doi: 10.1097/00000539-199606000-00017.
    2. Cortellazzi P, Caldiroli D, Byrne A, Sommariva A, Orena EF, Tramacere I. Defining and 
    developing expertise in tracheal intubation using a GlideScope for anaesthetists with 
    expertise in Macintosh direct laryngoscopy: an in-vivo longitudinal study. Anaesthesia. 
    2015;70(3):290-5. doi: 10.1111/anae.12878.
    3. Caldiroli D, Cortellazzi P. A new difficult airway management algorithm based upon the 
    El Ganzouri Risk Index and GlideScope® videolaryngoscope. A new look for intubation? 
    Minerva Anestesiol. 2011;77(6):637-45.
    4. Lundstrøm LH, Vester-Andersen M, Møller AM, Charuluxananan S, L'hermite J, Wetterslev J. 
    Poor prognostic value of the modified Mallampati score: a meta-analysis involving 177,088 
    patients. Br J Anaesth. 2011;107(5):659-67. doi: 10.1093/bja/aer292.
    """
    
    mouth_opening: Literal["≥4 cm", "<4 cm"] = Field(
        ...,
        description="Inter-incisor mouth opening distance. ≥4 cm scores 0 points, <4 cm scores 1 point",
        example="≥4 cm"
    )
    
    thyromental_distance: Literal[">6.5 cm", "6.0-6.5 cm", "<6.0 cm"] = Field(
        ...,
        description="Thyromental distance (thyroid notch to mandible tip with neck extended). >6.5 cm scores 0 points, 6.0-6.5 cm scores 1 point, <6.0 cm scores 2 points",
        example=">6.5 cm"
    )
    
    mallampati_class: Literal["Class I", "Class II", "Class III", "Class IV"] = Field(
        ...,
        description="Modified Mallampati Classification (pharyngeal visualization). Class I scores 0 points, Class II scores 1 point, Class III and IV score 2 points each",
        example="Class II"
    )
    
    neck_movement: Literal[">90°", "80-90°", "<80°"] = Field(
        ...,
        description="Neck extension/flexion movement range. >90° scores 0 points, 80-90° scores 1 point, <80° scores 2 points",
        example=">90°"
    )
    
    ability_to_prognath: Literal["Yes", "No"] = Field(
        ...,
        description="Ability to advance lower jaw (prognathism) beyond upper teeth. Yes scores 0 points, No scores 1 point",
        example="Yes"
    )
    
    weight: Literal["<90 kg", "90-110 kg", ">110 kg"] = Field(
        ...,
        description="Patient body weight category. <90 kg scores 0 points, 90-110 kg scores 1 point, >110 kg scores 2 points",
        example="<90 kg"
    )
    
    history_difficult_intubation: Literal["None", "Questionable", "Definite"] = Field(
        ...,
        description="Previous history of difficult intubation. None scores 0 points, Questionable scores 1 point, Definite scores 2 points",
        example="None"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "mouth_opening": "≥4 cm",
                "thyromental_distance": ">6.5 cm",
                "mallampati_class": "Class II",
                "neck_movement": ">90°",
                "ability_to_prognath": "Yes",
                "weight": "<90 kg",
                "history_difficult_intubation": "None"
            }
        }


class ElGanzouriRiskIndexDifficultAirwayResponse(BaseModel):
    """
    Response model for El-Ganzouri Risk Index (EGRI) for Difficult Airway
    
    The EGRI score ranges from 0-12 points and classifies patients into:
    - Low Risk (0-3 points): Conventional laryngoscopy likely successful
    - High Risk (≥4 points): 93.8% specificity for difficult airway, special precautions needed
    - Very High Risk (≥7 points): May warrant awake fiberoptic intubation
    
    Clinical Management Based on Score:
    
    Low Risk (0-3 points):
    - Standard airway management protocol
    - Conventional laryngoscopy with Macintosh blade
    - Routine preparation and equipment
    - Standard monitoring and backup plans
    
    High Risk (4-6 points):
    - Video laryngoscopy as first-line approach
    - Experienced anesthesiologist recommended
    - Difficult airway equipment readily available
    - Enhanced monitoring and backup plans
    - Consider awake techniques if other risk factors present
    
    Very High Risk (≥7 points):
    - Strong consideration for awake fiberoptic intubation
    - Senior anesthesiologist involvement
    - Comprehensive difficult airway equipment setup
    - Multiple backup techniques prepared
    - Consider regional anesthesia alternatives if appropriate
    
    Reference: El-Ganzouri AR, et al. Anesth Analg. 1996;82(6):1197-204.
    """
    
    result: int = Field(
        ...,
        description="EGRI score calculated from seven clinical parameters (range: 0-12 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the score",
        example="Low risk of difficult airway. Conventional laryngoscopy and standard intubation techniques are likely to be successful. Routine airway management protocol can be followed with standard preparation and equipment readily available."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk of difficult airway"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Low risk of difficult airway. Conventional laryngoscopy and standard intubation techniques are likely to be successful. Routine airway management protocol can be followed with standard preparation and equipment readily available. Always have backup airway plan and appropriate equipment available. Consider consultation with senior anesthesiologist for high-risk cases.",
                "stage": "Low Risk",
                "stage_description": "Low risk of difficult airway"
            }
        }