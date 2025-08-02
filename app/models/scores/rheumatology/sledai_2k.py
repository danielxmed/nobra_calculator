"""
Systemic Lupus Erythematosus Disease Activity Index 2000 (SLEDAI-2K) Models

Request and response models for SLEDAI-2K calculation.

References (Vancouver style):
1. Gladman DD, Ibañez D, Urowitz MB. Systemic lupus erythematosus disease activity 
   index 2000. J Rheumatol. 2002 Feb;29(2):288-91.
2. Buyon JP, Petri MA, Kim MY, Kalunian KC, Grossman J, Hahn BH, et al. The effect 
   of combined estrogen and progesterone hormone replacement therapy on disease activity 
   in systemic lupus erythematosus: a randomized trial. Ann Intern Med. 2005 Jun 
   21;142(12 Pt 1):953-62.
3. Touma Z, Urowitz MB, Gladman DD. SLEDAI-2K for a 30-day window. Lupus. 2010 
   Jan;19(1):49-51. doi: 10.1177/0961203309346505.

SLEDAI-2K is a 24-item weighted index that stratifies disease activity in SLE patients. 
It was modified from the original SLEDAI to allow documentation of persistent disease 
activity in rash, alopecia, mucosal ulcers, and proteinuria, making it more suitable 
for clinical trials and longitudinal assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class Sledai2kRequest(BaseModel):
    """
    Request model for Systemic Lupus Erythematosus Disease Activity Index 2000 (SLEDAI-2K)
    
    SLEDAI-2K evaluates 24 weighted items across multiple organ systems:
    
    CNS and Vascular (8 points each):
    - Seizure, psychosis, organic brain syndrome, visual disturbance
    - Cranial nerve disorder, lupus headache, CVA, vasculitis
    
    Musculoskeletal and Renal (4 points each):
    - Arthritis, myositis
    - Urinary casts, hematuria, proteinuria, pyuria
    
    Dermatologic and Serositis (2 points each):
    - Rash, alopecia, mucosal ulcers
    - Pleurisy, pericarditis
    
    Immunologic (2 points each):
    - Low complement, increased DNA binding
    
    Constitutional and Hematologic (1 point each):
    - Fever, thrombocytopenia, leukopenia
    
    References (Vancouver style):
    1. Gladman DD, Ibañez D, Urowitz MB. Systemic lupus erythematosus disease activity 
       index 2000. J Rheumatol. 2002 Feb;29(2):288-91.
    """
    
    # CNS and Vascular manifestations (8 points each)
    seizure: Literal["yes", "no"] = Field(
        ...,
        description="Recent onset seizure (exclude metabolic, infectious, or drug causes)",
        example="no"
    )
    
    psychosis: Literal["yes", "no"] = Field(
        ...,
        description="Altered mental function with impaired reality perception (exclude uremia, drugs)",
        example="no"
    )
    
    organic_brain_syndrome: Literal["yes", "no"] = Field(
        ...,
        description="Altered mental function with impaired cognition, memory, or concentration",
        example="no"
    )
    
    visual_disturbance: Literal["yes", "no"] = Field(
        ...,
        description="Retinal changes of SLE (cytoid bodies, retinal hemorrhages, exudates, hemorrhage in choroid or optic neuritis)",
        example="no"
    )
    
    cranial_nerve_disorder: Literal["yes", "no"] = Field(
        ...,
        description="New onset sensory or motor neuropathy involving cranial nerves",
        example="no"
    )
    
    lupus_headache: Literal["yes", "no"] = Field(
        ...,
        description="Severe persistent headache, may be migrainous, nonresponsive to narcotic analgesia",
        example="no"
    )
    
    cva: Literal["yes", "no"] = Field(
        ...,
        description="New onset cerebrovascular accident (stroke)",
        example="no"
    )
    
    vasculitis: Literal["yes", "no"] = Field(
        ...,
        description="Ulceration, gangrene, tender finger nodules, periungual infarction, splinter hemorrhages, or biopsy/angiogram proof",
        example="no"
    )
    
    # Musculoskeletal and Renal manifestations (4 points each)
    arthritis: Literal["yes", "no"] = Field(
        ...,
        description="≥2 joints with pain and signs of inflammation (tenderness, swelling, or effusion)",
        example="yes"
    )
    
    myositis: Literal["yes", "no"] = Field(
        ...,
        description="Proximal muscle aching/weakness with elevated CPK/aldolase or EMG changes or biopsy showing myositis",
        example="no"
    )
    
    urinary_casts: Literal["yes", "no"] = Field(
        ...,
        description="Heme-granular or red blood cell casts",
        example="no"
    )
    
    hematuria: Literal["yes", "no"] = Field(
        ...,
        description=">5 RBCs/high power field (exclude stone, infection, or other causes)",
        example="no"
    )
    
    proteinuria: Literal["yes", "no"] = Field(
        ...,
        description="New onset or recent increase >0.5 g/24 hours",
        example="yes"
    )
    
    pyuria: Literal["yes", "no"] = Field(
        ...,
        description=">5 WBCs/high power field (exclude infection)",
        example="no"
    )
    
    # Dermatologic and Serositis manifestations (2 points each)
    rash: Literal["yes", "no"] = Field(
        ...,
        description="New or ongoing inflammatory type rash",
        example="yes"
    )
    
    alopecia: Literal["yes", "no"] = Field(
        ...,
        description="New or ongoing abnormal patchy or diffuse hair loss",
        example="no"
    )
    
    mucosal_ulcers: Literal["yes", "no"] = Field(
        ...,
        description="New or ongoing oral or nasal ulcerations",
        example="yes"
    )
    
    pleurisy: Literal["yes", "no"] = Field(
        ...,
        description="Pleuritic chest pain with pleural rub, effusion, or pleural thickening",
        example="no"
    )
    
    pericarditis: Literal["yes", "no"] = Field(
        ...,
        description="Pericardial pain with rub, effusion, or ECG/echo confirmation",
        example="no"
    )
    
    # Immunologic manifestations (2 points each)
    low_complement: Literal["yes", "no"] = Field(
        ...,
        description="Decreased C3, C4, or CH50 below normal lab limits",
        example="yes"
    )
    
    increased_dna_binding: Literal["yes", "no"] = Field(
        ...,
        description="Increased anti-dsDNA antibody binding above normal range",
        example="yes"
    )
    
    # Constitutional and Hematologic manifestations (1 point each)
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Temperature >100.4°F (38°C) excluding infection",
        example="no"
    )
    
    thrombocytopenia: Literal["yes", "no"] = Field(
        ...,
        description="Platelets <100 × 10⁹/L excluding drug causes",
        example="no"
    )
    
    leukopenia: Literal["yes", "no"] = Field(
        ...,
        description="WBC <3 × 10⁹/L excluding drug causes",
        example="no"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "seizure": "no",
                "psychosis": "no",
                "organic_brain_syndrome": "no",
                "visual_disturbance": "no",
                "cranial_nerve_disorder": "no",
                "lupus_headache": "no",
                "cva": "no",
                "vasculitis": "no",
                "arthritis": "yes",
                "myositis": "no",
                "urinary_casts": "no",
                "hematuria": "no",
                "proteinuria": "yes",
                "pyuria": "no",
                "rash": "yes",
                "alopecia": "no",
                "mucosal_ulcers": "yes",
                "pleurisy": "no",
                "pericarditis": "no",
                "low_complement": "yes",
                "increased_dna_binding": "yes",
                "fever": "no",
                "thrombocytopenia": "no",
                "leukopenia": "no"
            }
        }
    }


class Sledai2kResponse(BaseModel):
    """
    Response model for Systemic Lupus Erythematosus Disease Activity Index 2000 (SLEDAI-2K)
    
    Scoring:
    - Range: 0-105 points
    - Active disease cutoff: 3-4 points
    - Treatment threshold: ≥6 points
    - Scores >45 are rare in clinical practice
    
    Reference: Gladman DD, et al. J Rheumatol. 2002;29(2):288-91.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=105,
        description="Total SLEDAI-2K score (range 0-105 points)",
        example=14
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on disease activity level",
        example="Moderate disease activity. Treatment modification usually indicated. Consider increasing immunosuppression."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity level (No Activity, Mild Activity, Moderate Activity, High Activity, Very High Activity)",
        example="Moderate Activity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity level",
        example="Moderate disease activity"
    )
    
    present_features: Optional[str] = Field(
        None,
        description="List of present features contributing to the score",
        example="Arthritis (4 points), Proteinuria (4 points), Rash (2 points), Mucosal Ulcers (2 points), Low Complement (2 points), Increased Dna Binding (2 points)"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 14,
                "unit": "points",
                "interpretation": "Moderate disease activity. Treatment modification usually indicated. Consider increasing immunosuppression.",
                "stage": "Moderate Activity",
                "stage_description": "Moderate disease activity",
                "present_features": "Arthritis (4 points), Proteinuria (4 points), Rash (2 points), Mucosal Ulcers (2 points), Low Complement (2 points), Increased Dna Binding (2 points)"
            }
        }
    }