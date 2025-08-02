"""
ISTH-SCC Bleeding Assessment Tool Models

Request and response models for ISTH-SCC bleeding assessment tool calculation.

References (Vancouver style):
1. Rodeghiero F, Tosetto A, Abshire T, Arnold DM, Coller B, James P, Neunert C, 
   Lillicrap D. ISTH/SSC bleeding assessment tool: a standardized questionnaire 
   and a proposal for a new bleeding score for inherited bleeding disorders. 
   J Thromb Haemost. 2010 Sep;8(9):2063-5.
2. Elbatarny M, Mollah S, Grabell J, Bae S, Deforest M, Tuttle A, Hopman W, 
   Clark DS, Mauer AC, Bowman M, Riddel J, Christopherson PA, Montgomery RR, 
   James PD. Normal range of bleeding scores for the ISTH-BAT: adult and pediatric 
   data from the merging project. Haemophilia. 2014 Nov;20(6):831-5.
3. Deforest M, Grabell J, Albert S, Young E, Tuttle A, Hopman WM, Heddle N, 
   James PD. Generation and optimization of the self-administered bleeding 
   assessment tool and its validation as a screening test for von Willebrand 
   disease. Haemophilia. 2015 May;21(3):e132-9.
4. Quiroga T, Goycoolea M, Panes O, Aranda E, Martínez C, Belmont S, Muñoz B, 
   Zúñiga P, Pereira J, Mezzano D. High prevalence of bleeders of unknown cause 
   among patients with inherited mucocutaneous bleeding. A prospective study of 
   280 patients and 299 controls. Haematologica. 2007 Mar;92(3):357-65.

The ISTH-SCC Bleeding Assessment Tool is a standardized questionnaire developed by 
the International Society on Thrombosis and Haemostasis Scientific and Standardization 
Committee to evaluate bleeding symptoms in patients with suspected inherited bleeding 
disorders. It assesses 14 different bleeding domains with scores ranging 0-4 points 
each (except CNS bleeding with 0/3/4 scoring), providing demographic-specific 
interpretation thresholds for screening purposes.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class IsthSccBleedingAssessmentToolRequest(BaseModel):
    """
    Request model for ISTH-SCC Bleeding Assessment Tool
    
    The ISTH-SCC Bleeding Assessment Tool evaluates 14 bleeding domains to screen for 
    inherited bleeding disorders. Each domain is scored 0-4 points based on severity:
    
    Scoring Guidelines:
    - 0 points: No bleeding or trivial bleeding (normal physiologic response)
    - 1 point: Bleeding present but doesn't meet criteria for higher scores
    - 2 points: Bleeding requiring medical consultation but not intervention
    - 3 points: Bleeding requiring medical intervention (treatment, procedures)
    - 4 points: Most severe bleeding requiring emergency care or hospitalization
    
    Special Scoring Rules:
    - CNS bleeding: Only 0 (never), 3 (subdural), or 4 (intracerebral) points
    - Score only bleeding symptoms present BEFORE and AT diagnosis
    - Distinction between 0 and 1 is critical for accurate assessment
    - Consider only significant bleeding that causes emotional distress or requires medical attention
    
    14 Bleeding Domains:
    1. Epistaxis: Nosebleeds (frequency, duration, medical intervention needed)
    2. Cutaneous bleeding: Bruising, petechiae, purpura beyond normal patterns
    3. Minor wounds: Bleeding from small cuts, scrapes beyond expected duration
    4. Oral cavity: Gum bleeding, tongue/cheek bleeding, oral mucosal bleeding
    5. GI bleeding: Hematemesis, melena, hematochezia, occult blood
    6. Hematuria: Gross or microscopic blood in urine (exclude infections/stones)
    7. Tooth extraction: Post-extraction bleeding requiring intervention
    8. Surgery: Excessive bleeding during or after surgical procedures
    9. Menorrhagia: Heavy menstrual bleeding (females only, relevant history)
    10. Postpartum hemorrhage: Excessive bleeding after delivery (females with deliveries)
    11. Muscle hematomas: Spontaneous or post-trauma muscle bleeding
    12. Hemarthrosis: Joint bleeding episodes (spontaneous or post-trauma)
    13. CNS bleeding: Central nervous system bleeding (subdural or intracerebral)
    14. Other bleeding: Any significant bleeding not covered in above categories
    
    Interpretation Thresholds:
    - Children (<18 years): 0-2 typical, ≥3 atypical (requires evaluation)
    - Adult males: 0-3 typical, ≥4 atypical (requires evaluation)
    - Adult females: 0-5 typical, ≥6 atypical (requires evaluation)
    
    Clinical Context:
    - Designed as screening tool, not diagnostic
    - Requires trained assessor for reliable results
    - Consider family history and clinical presentation
    - Laboratory testing needed for definitive diagnosis
    
    References (Vancouver style):
    1. Rodeghiero F, Tosetto A, Abshire T, Arnold DM, Coller B, James P, Neunert C, 
    Lillicrap D. ISTH/SSC bleeding assessment tool: a standardized questionnaire 
    and a proposal for a new bleeding score for inherited bleeding disorders. 
    J Thromb Haemat. 2010 Sep;8(9):2063-5.
    2. Elbatarny M, Mollah S, Grabell J, et al. Normal range of bleeding scores 
    for the ISTH-BAT: adult and pediatric data from the merging project. 
    Haemophilia. 2014 Nov;20(6):831-5.
    """
    
    epistaxis: int = Field(
        ...,
        ge=0,
        le=4,
        description="Nosebleed severity score. 0=no/trivial nosebleeds, 1=present but mild, 2=consultation needed, 3=medical intervention required, 4=severe bleeding requiring emergency care. Consider frequency, duration, and interventions needed",
        example=2
    )
    
    cutaneous_bleeding: int = Field(
        ...,
        ge=0,
        le=4,
        description="Skin bleeding severity score including bruising and petechiae. 0=normal bruising pattern, 1=mild increase, 2=consultation for bruising, 3=extensive bruising requiring evaluation, 4=severe spontaneous bleeding into skin",
        example=1
    )
    
    minor_wounds: int = Field(
        ...,
        ge=0,
        le=4,
        description="Bleeding from minor wounds severity score. 0=normal healing, 1=slightly prolonged bleeding, 2=consultation needed, 3=medical intervention required, 4=severe bleeding from minor trauma requiring sutures/cautery",
        example=0
    )
    
    oral_cavity: int = Field(
        ...,
        ge=0,
        le=4,
        description="Oral bleeding severity score including gums and oral mucosa. 0=no abnormal bleeding, 1=mild gum bleeding, 2=consultation for oral bleeding, 3=treatment needed, 4=severe oral bleeding requiring emergency care",
        example=1
    )
    
    gi_bleeding: int = Field(
        ...,
        ge=0,
        le=4,
        description="Gastrointestinal bleeding severity score. 0=no GI bleeding, 1=occult blood, 2=consultation for GI symptoms, 3=overt bleeding requiring treatment, 4=severe GI bleeding requiring hospitalization/transfusion",
        example=0
    )
    
    hematuria: int = Field(
        ...,
        ge=0,
        le=4,
        description="Blood in urine severity score (exclude UTI/stones). 0=no hematuria, 1=microscopic hematuria, 2=consultation needed, 3=gross hematuria requiring evaluation, 4=severe hematuria requiring emergency care",
        example=0
    )
    
    tooth_extraction: int = Field(
        ...,
        ge=0,
        le=4,
        description="Post-tooth extraction bleeding severity score. 0=normal healing, 1=slightly prolonged bleeding, 2=consultation needed, 3=resuturing/packing required, 4=severe bleeding requiring emergency intervention",
        example=0
    )
    
    surgery: int = Field(
        ...,
        ge=0,
        le=4,
        description="Surgical bleeding severity score. 0=normal surgical bleeding, 1=slightly increased bleeding, 2=consultation needed, 3=intervention required, 4=severe bleeding requiring re-operation/transfusion",
        example=0
    )
    
    menorrhagia: int = Field(
        ...,
        ge=0,
        le=4,
        description="Heavy menstrual bleeding severity score (females). 0=normal periods, 1=slightly heavy, 2=consultation sought, 3=treatment required (hormones/iron), 4=severe bleeding requiring emergency care/transfusion",
        example=2
    )
    
    postpartum_hemorrhage: int = Field(
        ...,
        ge=0,
        le=4,
        description="Postpartum bleeding severity score (females with deliveries). 0=normal postpartum bleeding, 1=slightly increased, 2=consultation needed, 3=treatment required, 4=severe hemorrhage requiring transfusion/surgery",
        example=0
    )
    
    muscle_hematomas: int = Field(
        ...,
        ge=0,
        le=4,
        description="Muscle bleeding severity score. 0=no muscle hematomas, 1=small hematomas, 2=consultation needed, 3=large hematomas requiring treatment, 4=severe muscle bleeding causing compartment syndrome/disability",
        example=0
    )
    
    hemarthrosis: int = Field(
        ...,
        ge=0,
        le=4,
        description="Joint bleeding severity score. 0=no joint bleeding, 1=mild joint swelling post-trauma, 2=consultation needed, 3=joint bleeding requiring treatment, 4=recurrent spontaneous hemarthrosis causing disability",
        example=0
    )
    
    cns_bleeding: Literal["never", "subdural", "intracerebral"] = Field(
        ...,
        description="Central nervous system bleeding category. Special scoring: never=0 points, subdural=3 points, intracerebral=4 points. This represents the most serious bleeding complication",
        example="never"
    )
    
    other_bleeding: int = Field(
        ...,
        ge=0,
        le=4,
        description="Other significant bleeding not covered above. 0=no other bleeding, 1=mild bleeding, 2=consultation needed, 3=treatment required, 4=severe bleeding requiring emergency care",
        example=0
    )
    
    age_group: Literal["child", "adult_male", "adult_female"] = Field(
        ...,
        description="Patient age and gender category for interpretation thresholds. Children <18 years, adult males ≥18 years, adult females ≥18 years",
        example="adult_female"
    )
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender for clinical context and score interpretation",
        example="female"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "epistaxis": 2,
                "cutaneous_bleeding": 1,
                "minor_wounds": 0,
                "oral_cavity": 1,
                "gi_bleeding": 0,
                "hematuria": 0,
                "tooth_extraction": 0,
                "surgery": 0,
                "menorrhagia": 2,
                "postpartum_hemorrhage": 0,
                "muscle_hematomas": 0,
                "hemarthrosis": 0,
                "cns_bleeding": "never",
                "other_bleeding": 0,
                "age_group": "adult_female",
                "gender": "female"
            }
        }


class IsthSccBleedingAssessmentToolResponse(BaseModel):
    """
    Response model for ISTH-SCC Bleeding Assessment Tool
    
    The ISTH-SCC bleeding score ranges from 0 to 55 points (maximum theoretical) and 
    provides demographic-specific interpretation:
    
    Score Interpretation by Demographics:
    
    Children (<18 years):
    - 0-2 points: Typical bleeding pattern (low likelihood of inherited bleeding disorder)
    - ≥3 points: Atypical bleeding pattern (increased likelihood, requires evaluation)
    
    Adult Males:
    - 0-3 points: Typical bleeding pattern (low likelihood of inherited bleeding disorder)
    - ≥4 points: Atypical bleeding pattern (increased likelihood, requires evaluation)
    
    Adult Females:
    - 0-5 points: Typical bleeding pattern (low likelihood of inherited bleeding disorder)
    - ≥6 points: Atypical bleeding pattern (increased likelihood, requires evaluation)
    
    Clinical Management by Score Category:
    
    Typical Scores:
    - Low probability of inherited bleeding disorder
    - Consider clinical context and family history
    - No routine hematologic evaluation needed
    - Monitor for changes in bleeding pattern
    
    Atypical Scores:
    - Increased likelihood of inherited bleeding disorder
    - Recommend hematologic evaluation including:
      * Complete blood count with platelet count
      * PT/PTT coagulation studies
      * von Willebrand disease panel (VWF:Ag, VWF:RCo, FVIII)
      * Platelet function studies if indicated
    - Consider specific factor deficiencies based on bleeding pattern
    - Obtain detailed family bleeding history
    
    Tool Limitations:
    - Screening tool only, not diagnostic
    - Requires trained assessor for reliability
    - Relatively insensitive in pediatric populations
    - Clinical judgment essential in interpretation
    - Laboratory confirmation required for diagnosis
    
    Follow-up Recommendations:
    - Document specific bleeding episodes and triggers
    - Assess family history of bleeding disorders
    - Consider genetic counseling for positive results
    - Coordinate with hematology if atypical scores
    - Patient education about bleeding precautions
    
    Reference: Rodeghiero F, et al. J Thromb Haemost. 2010;8(9):2063-5.
    """
    
    result: int = Field(
        ...,
        description="Total ISTH-SCC bleeding assessment score calculated from all 14 bleeding domains (range: 0-55 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the bleeding score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the bleeding score and patient demographics",
        example="Score 6 points for adult females: Atypical bleeding pattern. Increased likelihood of inherited bleeding disorder. This score exceeds the typical range for adult females (≥6 points). Recommend hematologic evaluation including von Willebrand disease studies and platelet function testing, particularly given the higher prevalence of bleeding disorders in women with menorrhagia. Consider comprehensive coagulation panel and detailed gynecologic history."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding pattern category based on demographic-specific thresholds (Typical or Atypical)",
        example="Adult Female - Atypical"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bleeding pattern category",
        example="Atypical bleeding pattern for adult females"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Score 6 points for adult females: Atypical bleeding pattern. Increased likelihood of inherited bleeding disorder. This score exceeds the typical range for adult females (≥6 points). Recommend hematologic evaluation including von Willebrand disease studies and platelet function testing, particularly given the higher prevalence of bleeding disorders in women with menorrhagia. Consider comprehensive coagulation panel and detailed gynecologic history.",
                "stage": "Adult Female - Atypical",
                "stage_description": "Atypical bleeding pattern for adult females"
            }
        }