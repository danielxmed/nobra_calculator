"""
Bristol Stool Form Scale Models

Request and response models for Bristol Stool Form Scale classification.

References (Vancouver style):
1. Lewis SJ, Heaton KW. Stool form scale as a useful guide to intestinal transit time. 
   Scand J Gastroenterol. 1997;32(9):920-4. doi: 10.3109/00365529709011203.
2. Heaton KW, Radvan J, Cripps H, Mountford RA, Braddon FE, Hughes AO. Defecation 
   frequency and timing, and stool form in the general population: a prospective study. 
   Gut. 1992;33(6):818-24. doi: 10.1136/gut.33.6.818.
3. O'Donnell LJ, Virjee J, Heaton KW. Detection of pseudodiarrhoea by simple clinical 
   assessment of intestinal transit rate. BMJ. 1990;300(6722):439-40. doi: 10.1136/bmj.300.6722.439.

The Bristol Stool Form Scale is a diagnostic medical tool designed to classify the form 
of human faeces into seven categories. It was developed at the Bristol Royal Infirmary 
as a clinical assessment tool in 1997 by Stephen Lewis and Ken Heaton. It is widely used 
as a research tool to evaluate the effectiveness of treatments for various diseases of 
the bowel, as well as a clinical communication aid, including being part of the diagnostic 
triad for irritable bowel syndrome.

The scale correlates stool form with intestinal transit time and provides valuable 
clinical information for assessing bowel health, diagnosing digestive issues, and 
monitoring treatment effectiveness.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class BristolStoolFormScaleRequest(BaseModel):
    """
    Request model for Bristol Stool Form Scale classification
    
    The Bristol Stool Form Scale classifies stool into seven distinct types:
    
    Type 1: Separate hard lumps, like nuts (severe constipation)
    - Hard, separate pellets that are difficult to pass
    - Indicates prolonged colonic transit time with excessive water absorption
    - Requires dietary modifications and possible laxative therapy
    
    Type 2: Sausage-like but lumpy (mild constipation)
    - Hard, lumpy stools that are somewhat larger but still difficult to pass
    - Indicates slow colonic transit with increased water absorption
    - Requires increased fiber intake, hydration, and physical activity
    
    Type 3: Like a sausage but with cracks on the surface (normal, lower range)
    - Sausage-shaped with surface cracks
    - Represents adequate hydration and fiber intake with normal colonic transit time
    - Generally considered healthy stool consistency
    
    Type 4: Like a sausage or snake, smooth and soft (ideal normal)
    - Smooth, soft, sausage-shaped stool that is easy to pass
    - Represents optimal hydration, diet, and normal colonic transit time
    - This is the target consistency for healthy bowel movements
    
    Type 5: Soft blobs with clear-cut edges (normal, upper range)
    - Soft blobs with clear-cut edges that pass easily
    - May indicate slightly faster colonic transit or higher water content
    - Generally acceptable but monitor for progression to diarrhea
    
    Type 6: Fluffy pieces with ragged edges, mushy (mild diarrhea)
    - Mushy stool with fluffy pieces and ragged edges
    - Indicates rapid colonic transit with reduced water absorption
    - May be caused by dietary factors, medications, or mild gastrointestinal conditions
    
    Type 7: Watery, no solid pieces, entirely liquid (severe diarrhea)
    - Watery stool with no solid pieces
    - Indicates very rapid intestinal transit with minimal water absorption
    - May lead to dehydration and electrolyte imbalance, requires medical evaluation if persistent

    References (Vancouver style):
    1. Lewis SJ, Heaton KW. Stool form scale as a useful guide to intestinal transit time. 
    Scand J Gastroenterol. 1997;32(9):920-4. doi: 10.3109/00365529709011203.
    2. Heaton KW, Radvan J, Cripps H, Mountford RA, Braddon FE, Hughes AO. Defecation 
    frequency and timing, and stool form in the general population: a prospective study. 
    Gut. 1992;33(6):818-24. doi: 10.1136/gut.33.6.818.
    3. O'Donnell LJ, Virjee J, Heaton KW. Detection of pseudodiarrhoea by simple clinical 
    assessment of intestinal transit rate. BMJ. 1990;300(6722):439-40. doi: 10.1136/bmj.300.6722.439.
    """
    
    stool_type: Literal[1, 2, 3, 4, 5, 6, 7] = Field(
        ...,
        description="Bristol Stool Form Scale type (1-7). Type 1: Separate hard lumps (severe constipation), Type 2: Sausage-like but lumpy (mild constipation), Type 3: Sausage with cracks (normal lower), Type 4: Smooth sausage (ideal), Type 5: Soft blobs (normal upper), Type 6: Fluffy pieces (mild diarrhea), Type 7: Watery liquid (severe diarrhea)",
        example=4
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "stool_type": 4
            }
        }


class BristolStoolFormScaleResponse(BaseModel):
    """
    Response model for Bristol Stool Form Scale classification
    
    The Bristol Stool Form Scale provides:
    - Classification of stool consistency into 7 types
    - Assessment of intestinal transit time
    - Clinical significance and recommendations
    - Bowel health categorization (Constipation, Normal, Diarrhea)
    
    Types 3 and 4 are considered normal and ideal stool consistency.
    Types 1-2 indicate constipation with slow transit time.
    Types 6-7 indicate diarrhea with fast transit time.
    
    Reference: Lewis SJ, Heaton KW. Scand J Gastroenterol. 1997;32(9):920-4.
    """
    
    result: int = Field(
        ...,
        description="Bristol Stool Form Scale type (1-7)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the scale",
        example="type"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and detailed assessment of stool type",
        example="Ideal bowel function. Smooth, soft, sausage-shaped stool that is easy to pass. Represents optimal hydration, diet, and normal colonic transit time. This is the target consistency for healthy bowel movements."
    )
    
    stage: str = Field(
        ...,
        description="Clinical stage classification (e.g., Severe Constipation, Normal, Mild Diarrhea)",
        example="Normal (Ideal)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stool form appearance",
        example="Smooth, soft sausage or snake"
    )
    
    transit_time: str = Field(
        ...,
        description="Assessment of intestinal transit time based on stool form",
        example="Normal"
    )
    
    clinical_significance: str = Field(
        ...,
        description="Clinical significance and recommended actions",
        example="Ideal - optimal bowel health"
    )
    
    bowel_health_category: str = Field(
        ...,
        description="Overall bowel health category (Constipation, Normal, Diarrhea)",
        example="Normal"
    )
    
    recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Clinical recommendations categorized by dietary, lifestyle, and medical interventions",
        example={
            "dietary": ["Maintain current diet", "Continue balanced nutrition"],
            "lifestyle": ["Maintain current routine", "Continue healthy habits"],
            "medical": ["Ideal - no changes needed", "Continue current management"]
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "type",
                "interpretation": "Ideal bowel function. Smooth, soft, sausage-shaped stool that is easy to pass. Represents optimal hydration, diet, and normal colonic transit time. This is the target consistency for healthy bowel movements.",
                "stage": "Normal (Ideal)",
                "stage_description": "Smooth, soft sausage or snake",
                "transit_time": "Normal",
                "clinical_significance": "Ideal - optimal bowel health",
                "bowel_health_category": "Normal",
                "recommendations": {
                    "dietary": ["Maintain current diet", "Continue balanced nutrition"],
                    "lifestyle": ["Maintain current routine", "Continue healthy habits"],
                    "medical": ["Ideal - no changes needed", "Continue current management"]
                }
            }
        }