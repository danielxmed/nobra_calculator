"""
Asthma Predictive Index (API) Models

Request and response models for Asthma Predictive Index calculation.

References (Vancouver style):
1. Castro-Rodríguez JA, Holberg CJ, Wright AL, Martinez FD. A clinical index to define 
   risk of asthma in young children with recurrent wheezing. Am J Respir Crit Care Med. 
   2000;162(4 Pt 1):1403-6.
2. Leonardi NA, Spycher BD, Strippoli MP, Frey U, Silverman M, Kuehni CE. Validation of 
   the Asthma Predictive Index and comparison with simpler clinical prediction rules. 
   J Allergy Clin Immunol. 2011;127(6):1466-72.e6.
3. Castro-Rodriguez JA. The Asthma Predictive Index: early diagnosis of asthma. 
   Curr Opin Allergy Clin Immunol. 2011;11:157–161.

The Asthma Predictive Index (API) is a clinical decision tool that uses 6 clinical 
variables to assess the likelihood of pediatric patients ≤3 years old developing 
childhood asthma during school years. It distinguishes between stringent criteria 
(≥3 wheezing episodes) and loose criteria (<3 wheezing episodes), combined with 
major criteria (family history of asthma, eczema) and minor criteria (air allergen 
sensitivity, wheezing apart from colds, >4% eosinophils).
"""

from pydantic import BaseModel, Field
from typing import Literal


class AsthmaPreductiveIndexRequest(BaseModel):
    """
    Request model for Asthma Predictive Index (API)
    
    The API uses 6 clinical variables to assess asthma development risk in children ≤3 years:
    
    Wheezing Episodes:
    - less_than_3: Less than 3 wheezing episodes per year (loose criteria)
    - 3_or_more: 3 or more wheezing episodes per year (stringent criteria)
    
    Major Criteria (need 1 for positive result):
    - Family history (parent) with asthma
    - Patient diagnosed with eczema (atopic dermatitis)
    
    Minor Criteria (need 2 for positive result):
    - Patient diagnosed with sensitivity to allergens in the air (positive skin tests/blood tests)
    - Wheezing present apart from colds
    - Greater than 4% blood eosinophils
    
    API Classification:
    - Positive Stringent: ≥3 wheezing episodes + (1 major OR 2 minor) = 77% asthma risk
    - Positive Loose: <3 wheezing episodes + (1 major OR 2 minor) = 59% asthma risk  
    - Negative: Does not meet positive criteria = <3% asthma risk

    References (Vancouver style):
    1. Castro-Rodríguez JA, Holberg CJ, Wright AL, Martinez FD. A clinical index to define 
    risk of asthma in young children with recurrent wheezing. Am J Respir Crit Care Med. 
    2000;162(4 Pt 1):1403-6.
    2. Leonardi NA, Spycher BD, Strippoli MP, Frey U, Silverman M, Kuehni CE. Validation of 
    the Asthma Predictive Index and comparison with simpler clinical prediction rules. 
    J Allergy Clin Immunol. 2011;127(6):1466-72.e6.
    3. Castro-Rodriguez JA. The Asthma Predictive Index: early diagnosis of asthma. 
    Curr Opin Allergy Clin Immunol. 2011;11:157–161.
    """
    
    wheezing_episodes: Literal["less_than_3", "3_or_more"] = Field(
        ...,
        description="Number of wheezing episodes per year. Less than 3 episodes qualifies for loose criteria, 3 or more for stringent criteria",
        example="less_than_3"
    )
    
    family_history_asthma: Literal["yes", "no"] = Field(
        ...,
        description="Family history (parent) with asthma. Major criterion - positive increases asthma development risk",
        example="no"
    )
    
    eczema_diagnosis: Literal["yes", "no"] = Field(
        ...,
        description="Patient diagnosed with eczema (atopic dermatitis). Major criterion - positive increases asthma development risk",
        example="yes"
    )
    
    air_allergen_sensitivity: Literal["yes", "no"] = Field(
        ...,
        description="Patient diagnosed with sensitivity to allergens in the air. Minor criterion - demonstrated through positive skin prick tests or blood tests to allergens like dust mites, mold, weeds, etc.",
        example="no"
    )
    
    wheezing_apart_from_colds: Literal["yes", "no"] = Field(
        ...,
        description="Wheezing present apart from colds (not just during viral respiratory illnesses). Minor criterion - indicates underlying airway reactivity",
        example="no"
    )
    
    eosinophils_over_4_percent: Literal["yes", "no"] = Field(
        ...,
        description="Greater than 4% blood eosinophils on complete blood count. Minor criterion - indicates allergic/atopic predisposition",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "wheezing_episodes": "less_than_3",
                "family_history_asthma": "no",
                "eczema_diagnosis": "yes",
                "air_allergen_sensitivity": "no",
                "wheezing_apart_from_colds": "no",
                "eosinophils_over_4_percent": "no"
            }
        }


class AsthmaPreductiveIndexResponse(BaseModel):
    """
    Response model for Asthma Predictive Index (API)
    
    The API classifies patients into three risk categories:
    - Positive Stringent (77% asthma risk): ≥3 wheezing episodes + criteria met
    - Positive Loose (59% asthma risk): <3 wheezing episodes + criteria met
    - Negative (<3% asthma risk): Criteria not met
    
    Criteria are met with either 1 major criterion OR 2 minor criteria.
    
    Reference: Castro-Rodríguez JA, et al. Am J Respir Crit Care Med. 2000;162(4 Pt 1):1403-6.
    """
    
    result: str = Field(
        ...,
        description="API classification result (Positive Stringent, Positive Loose, or Negative)",
        example="Positive Loose"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the API classification",
        example="59% chance of diagnosed asthma. Requires <3 wheezing episodes per year AND either 1 major criterion OR 2 minor criteria. Consider monitoring and evaluation for asthma development."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Positive Stringent, Positive Loose, or Negative)",
        example="Positive Loose"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate risk for asthma development"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Positive Loose",
                "unit": "classification",
                "interpretation": "59% chance of diagnosed asthma. Requires <3 wheezing episodes per year AND either 1 major criterion OR 2 minor criteria. Consider monitoring and evaluation for asthma development.",
                "stage": "Positive Loose",
                "stage_description": "Moderate risk for asthma development"
            }
        }
