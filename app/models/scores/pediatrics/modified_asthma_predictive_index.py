"""
Modified Asthma Predictive Index (mAPI) Models

Request and response models for mAPI assessment in pediatric patients.

References (Vancouver style):
1. Guilbert TW, Morgan WJ, Zeiger RS, Mauger DT, Boehmer SJ, Szefler SJ, et al. 
   Long-term inhaled corticosteroids in preschool children at high risk for asthma. 
   N Engl J Med. 2006 May 11;354(19):1985-97. doi: 10.1056/NEJMoa051378.
2. Chang TS, Lemanske RF, Guilbert TW, Gern JE, Coen MH, Evans MD, et al. 
   Evaluation of the modified asthma predictive index in high-risk preschoolers. 
   J Allergy Clin Immunol Pract. 2013 Mar-Apr;1(2):152-6. doi: 10.1016/j.jaip.2012.10.008.
3. Castro-Rodríguez JA, Holberg CJ, Wright AL, Martinez FD. A clinical index to 
   define risk of asthma in young children with recurrent wheezing. Am J Respir Crit 
   Care Med. 2000 Oct;162(4 Pt 1):1403-6. doi: 10.1164/ajrccm.162.4.9912111.

The Modified Asthma Predictive Index (mAPI) is a validated tool for predicting 
future asthma development in children ≤3 years old with recurrent wheezing. 
It requires ≥4 wheezing episodes per year and evaluates 3 major criteria and 
3 minor criteria. The index is positive when ≥1 major OR ≥2 minor criteria 
are present, indicating increased asthma risk.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class ModifiedAsthmaPredictiveIndexRequest(BaseModel):
    """
    Request model for Modified Asthma Predictive Index (mAPI)
    
    The mAPI predicts future asthma onset in children ≤3 years old with recurrent 
    wheezing episodes. It requires ≥4 wheezing episodes per year for applicability.
    
    Scoring Criteria:
    
    Major Criteria (≥1 required for positive mAPI):
    - Parent with asthma
    - Patient has physician-diagnosed atopic dermatitis  
    - Patient has aeroallergen sensitivity (positive skin tests or blood tests)
    
    Minor Criteria (≥2 required for positive mAPI if no major criteria):
    - Wheezing unrelated to colds
    - Eosinophils ≥4% on complete blood count
    - Documented allergy to milk, egg, or peanuts
    
    mAPI is POSITIVE when:
    - ≥4 wheezing episodes per year AND
    - ≥1 major criteria OR ≥2 minor criteria
    
    Clinical Interpretation:
    - Positive mAPI: Increased risk of future asthma development
    - Negative mAPI: Lower risk of future asthma development
    - Not Applicable: <4 wheezing episodes per year
    
    Performance Characteristics:
    - High specificity: 98-100%
    - Variable sensitivity: 8.2-19% (depends on age)
    - Does not guarantee future asthma diagnosis
    
    References (Vancouver style):
    1. Guilbert TW, Morgan WJ, Zeiger RS, Mauger DT, Boehmer SJ, Szefler SJ, et al. 
       Long-term inhaled corticosteroids in preschool children at high risk for asthma. 
       N Engl J Med. 2006 May 11;354(19):1985-97. doi: 10.1056/NEJMoa051378.
    2. Chang TS, Lemanske RF, Guilbert TW, Gern JE, Coen MH, Evans MD, et al. 
       Evaluation of the modified asthma predictive index in high-risk preschoolers. 
       J Allergy Clin Immunol Pract. 2013 Mar-Apr;1(2):152-6. doi: 10.1016/j.jaip.2012.10.008.
    3. Castro-Rodríguez JA, Holberg CJ, Wright AL, Martinez FD. A clinical index to 
       define risk of asthma in young children with recurrent wheezing. Am J Respir Crit 
       Care Med. 2000 Oct;162(4 Pt 1):1403-6. doi: 10.1164/ajrccm.162.4.9912111.
    """
    
    wheezing_episodes_per_year: int = Field(
        ...,
        ge=0,
        le=50,
        description="Number of wheezing episodes per year. mAPI requires ≥4 episodes for applicability. Document all episodes including those associated with viral infections",
        example=6
    )
    
    parent_asthma: Literal["yes", "no"] = Field(
        ...,
        description="Parent (mother or father) has physician-diagnosed asthma. Major criteria worth 1 point",
        example="no"
    )
    
    atopic_dermatitis: Literal["yes", "no"] = Field(
        ...,
        description="Patient has physician-diagnosed atopic dermatitis (eczema). Major criteria worth 1 point",
        example="yes"
    )
    
    aeroallergen_sensitivity: Literal["yes", "no"] = Field(
        ...,
        description="Patient has demonstrated aeroallergen sensitivity through positive skin prick tests or specific IgE blood tests to environmental allergens (dust mites, pollens, molds, pet dander). Major criteria worth 1 point",
        example="no"
    )
    
    wheezing_unrelated_colds: Literal["yes", "no"] = Field(
        ...,
        description="Patient experiences wheezing episodes that occur independently of cold symptoms or viral upper respiratory infections. Minor criteria worth 1 point",
        example="yes"
    )
    
    eosinophils_4_percent: Literal["yes", "no"] = Field(
        ...,
        description="Eosinophils ≥4% on complete blood count differential. Minor criteria worth 1 point",
        example="no"
    )
    
    food_allergies: Literal["yes", "no"] = Field(
        ...,
        description="Documented allergy to milk, egg, or peanuts (confirmed by physician or positive allergy testing). This is the key modification in mAPI compared to original API. Minor criteria worth 1 point",
        example="no"
    )
    
    @validator('wheezing_episodes_per_year')
    def validate_wheezing_episodes(cls, v):
        if v < 0:
            raise ValueError('wheezing_episodes_per_year must be non-negative')
        if v > 50:
            raise ValueError('wheezing_episodes_per_year seems unusually high, please verify')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "wheezing_episodes_per_year": 6,
                "parent_asthma": "no",
                "atopic_dermatitis": "yes",
                "aeroallergen_sensitivity": "no",
                "wheezing_unrelated_colds": "yes",
                "eosinophils_4_percent": "no",
                "food_allergies": "no"
            }
        }


class ModifiedAsthmaPredictiveIndexResponse(BaseModel):
    """
    Response model for Modified Asthma Predictive Index (mAPI)
    
    The mAPI result indicates the likelihood of future asthma development:
    
    Positive mAPI:
    - Increased risk of future asthma development
    - Present when ≥4 wheezing episodes/year AND (≥1 major OR ≥2 minor criteria)
    - High specificity (98-100%) but variable sensitivity (8.2-19%)
    - Consider close monitoring and specialist consultation
    
    Negative mAPI:
    - Lower risk of future asthma development
    - Present when ≥4 wheezing episodes/year AND (<1 major AND <2 minor criteria)
    - Continue routine monitoring and supportive care
    
    Not Applicable:
    - mAPI cannot be evaluated due to <4 wheezing episodes per year
    - Consider monitoring and reassessment as clinical picture evolves
    
    Clinical Considerations:
    - mAPI does not guarantee future asthma diagnosis
    - Predictive ability depends on local asthma prevalence
    - Early intervention benefits remain unproven
    - Tool helps identify high-risk children for closer monitoring
    
    Reference: Guilbert TW, et al. N Engl J Med. 2006;354(19):1985-97.
    """
    
    result: Literal["Positive", "Negative", "Not Applicable"] = Field(
        ...,
        description="mAPI result indicating asthma risk prediction",
        example="Positive"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="result"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with risk assessment and management recommendations",
        example="mAPI is POSITIVE. Patient has 6 wheezing episodes per year with 1 major criteria and 1 minor criteria present. This indicates an increased risk of future asthma development. Consider close monitoring, environmental control measures, and discussion with pediatric pulmonologist or allergist."
    )
    
    stage: str = Field(
        ...,
        description="Clinical risk category (Positive mAPI, Negative mAPI, Not Applicable)",
        example="Positive mAPI"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Increased asthma risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Positive",
                "unit": "result",
                "interpretation": "mAPI is POSITIVE. Patient has 6 wheezing episodes per year with 1 major criteria and 1 minor criteria present. This indicates an increased risk of future asthma development. Consider close monitoring, environmental control measures, and discussion with pediatric pulmonologist or allergist.",
                "stage": "Positive mAPI",
                "stage_description": "Increased asthma risk"
            }
        }