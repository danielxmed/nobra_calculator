"""
Fuhrman Nuclear Grade for Clear Cell Renal Carcinoma Models

Request and response models for Fuhrman Nuclear Grade calculation.

References (Vancouver style):
1. Fuhrman SA, Lasky LC, Limas C. Prognostic significance of morphologic parameters 
   in renal cell carcinoma. Am J Surg Pathol. 1982 Oct;6(7):655-63. 
   doi: 10.1097/00000478-198210000-00007.
2. Rioux-Leclercq N, Karakiewicz PI, Trinh QD, Ficarra V, Cindolo L, de la Taille A, 
   et al. Prognostic ability of simplified nuclear grading of renal cell carcinoma. 
   Cancer. 2007 Mar 1;109(5):868-74. doi: 10.1002/cncr.22463.
3. Delahunt B, Cheville JC, Martignoni G, Humphrey PA, Magi-Galluzzi C, McKenney J, 
   et al. The International Society of Urological Pathology (ISUP) grading system for 
   renal cell carcinoma and other prognostic parameters. Am J Surg Pathol. 
   2013 Oct;37(10):1490-504. doi: 10.1097/PAS.0b013e318299f0fb.

The Fuhrman Nuclear Grade is a four-tiered prognostic grading system for clear cell 
renal cell carcinoma based on nuclear morphology. It evaluates nuclear size, shape, 
nucleoli prominence, and presence of bizarre features. Higher grades correlate with 
worse cancer-specific survival. Note: The WHO/ISUP grading system is now recommended 
over Fuhrman grading for improved prognostic accuracy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FuhrmanNuclearGradeRequest(BaseModel):
    """
    Request model for Fuhrman Nuclear Grade for Clear Cell Renal Carcinoma
    
    The Fuhrman grading system evaluates four key nuclear features:
    
    1. Nuclear Diameter:
       - small_10um: Small nuclei (~10 µm), similar to mature lymphocytes (Grade 1)
       - larger_15um: Slightly larger nuclei (~15 µm) (Grade 2)
       - even_larger_20um: Even larger nuclei (~20 µm) (Grade 3)
    
    2. Nuclear Shape:
       - round_uniform: Round and uniform shape (Grade 1)
       - irregularities: Irregularities in nuclear outline (Grade 2)
       - obvious_irregular: Obvious irregular nuclear outline (Grade 3)
    
    3. Nucleoli Visibility:
       - absent_inconspicuous: Absent or inconspicuous nucleoli (Grade 1)
       - visible_400x: Nucleoli visible at 400x magnification (Grade 2)
       - prominent_100x: Prominent nucleoli visible at 100x magnification (Grade 3)
    
    4. Bizarre Features:
       - Presence of bizarre, multilobed nuclei or spindle cells automatically indicates Grade 4
    
    Grading Rules:
    - Grade 1-3: Determined by the highest grade feature among the first three parameters
    - Grade 4: Automatically assigned if bizarre features are present
    - Grade is based on the worst (highest grade) features observed
    
    References (Vancouver style):
    1. Fuhrman SA, Lasky LC, Limas C. Prognostic significance of morphologic parameters 
       in renal cell carcinoma. Am J Surg Pathol. 1982 Oct;6(7):655-63.
    2. Rioux-Leclercq N, Karakiewicz PI, Trinh QD, Ficarra V, Cindolo L, de la Taille A, 
       et al. Prognostic ability of simplified nuclear grading of renal cell carcinoma. 
       Cancer. 2007 Mar 1;109(5):868-74.
    """
    
    nuclear_diameter: Literal["small_10um", "larger_15um", "even_larger_20um"] = Field(
        ...,
        description="Size of tumor cell nuclei compared to lymphocytes. Small (~10µm) indicates Grade 1 features, larger (~15µm) indicates Grade 2, even larger (~20µm) indicates Grade 3",
        example="larger_15um"
    )
    
    nuclear_shape: Literal["round_uniform", "irregularities", "obvious_irregular"] = Field(
        ...,
        description="Shape and regularity of nuclear outline. Round/uniform indicates Grade 1, irregularities indicate Grade 2, obvious irregular outline indicates Grade 3",
        example="irregularities"
    )
    
    nucleoli: Literal["absent_inconspicuous", "visible_400x", "prominent_100x"] = Field(
        ...,
        description="Visibility and prominence of nucleoli. Absent/inconspicuous indicates Grade 1, visible at 400x magnification indicates Grade 2, prominent at 100x indicates Grade 3",
        example="visible_400x"
    )
    
    bizarre_multilobed_spindle: Literal["yes", "no"] = Field(
        ...,
        description="Presence of bizarre, multilobed nuclei or spindle cells. If present (yes), automatically indicates Grade 4 regardless of other features",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "nuclear_diameter": "larger_15um",
                "nuclear_shape": "irregularities",
                "nucleoli": "visible_400x",
                "bizarre_multilobed_spindle": "no"
            }
        }


class FuhrmanNuclearGradeResponse(BaseModel):
    """
    Response model for Fuhrman Nuclear Grade for Clear Cell Renal Carcinoma
    
    The Fuhrman grade ranges from 1 to 4, with higher grades indicating:
    - Grade 1: Best prognosis, small round nuclei without visible nucleoli
    - Grade 2: Intermediate prognosis, slightly irregular nuclei with visible nucleoli
    - Grade 3: Worse prognosis, obviously irregular nuclei with prominent nucleoli
    - Grade 4: Poorest prognosis, extreme nuclear pleomorphism or bizarre features
    
    Clinical Significance:
    - Independent predictor of cancer-specific survival
    - Used for risk stratification and treatment planning
    - Higher grades associated with more aggressive disease
    - Most tumors are grades 2-3; grade 1 is rare (<5%), grade 4 accounts for 5-10%
    
    Note: The WHO/ISUP grading system is now recommended over Fuhrman grading
    as it provides superior prognostic accuracy with less inter-observer variability.
    
    Reference: Fuhrman SA, et al. Am J Surg Pathol. 1982;6(7):655-63.
    """
    
    result: int = Field(
        ...,
        description="Fuhrman nuclear grade (1-4) based on nuclear morphology features",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grade",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including nuclear features and prognostic implications",
        example="Larger nuclei (15 µm), may be oval with finely granular chromatin. Nucleoli visible at 400x magnification. Intermediate prognosis."
    )
    
    stage: str = Field(
        ...,
        description="Fuhrman grade classification (Grade 1, Grade 2, Grade 3, or Grade 4)",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade characteristics",
        example="Slightly irregular nuclei with visible nucleoli"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Larger nuclei (15 µm), may be oval with finely granular chromatin. Nucleoli visible at 400x magnification. Intermediate prognosis.",
                "stage": "Grade 2",
                "stage_description": "Slightly irregular nuclei with visible nucleoli"
            }
        }