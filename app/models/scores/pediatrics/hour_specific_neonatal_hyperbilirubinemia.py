"""
Hour-Specific Risk for Neonatal Hyperbilirubinemia Models

Request and response models for Hour-Specific Risk assessment using the Bhutani nomogram.

References (Vancouver style):
1. Bhutani VK, Johnson L, Sivieri EM. Predictive ability of a predischarge hour-specific 
   serum bilirubin for subsequent significant hyperbilirubinemia in healthy term and 
   near-term newborns. Pediatrics. 1999 Jan;103(1):6-14. doi: 10.1542/peds.103.1.6.
2. American Academy of Pediatrics Subcommittee on Hyperbilirubinemia. Management of 
   hyperbilirubinemia in the newborn infant 35 or more weeks of gestation. Pediatrics. 
   2004 Jul;114(1):297-316. doi: 10.1542/peds.114.1.297.
3. Bhutani VK, Johnson LH, Schwoebel A, Gennaro S. A systems approach for neonatal 
   hyperbilirubinemia in term and near-term newborns. J Obstet Gynecol Neonatal Nurs. 
   2006 Jul-Aug;35(4):444-55. doi: 10.1111/j.1552-6909.2006.00044.x.

The Bhutani nomogram is a clinical tool that plots hour-specific total serum bilirubin 
values to stratify neonates into risk zones for developing subsequent significant 
hyperbilirubinemia (>95th percentile). This prediction tool helps identify infants who 
require closer follow-up after hospital discharge.
"""

from pydantic import BaseModel, Field


class HourSpecificNeonatalHyperbilirubinemiaRequest(BaseModel):
    """
    Request model for Hour-Specific Risk for Neonatal Hyperbilirubinemia
    
    The Bhutani nomogram requires two parameters:
    
    1. Age in hours: Postnatal age from birth (12-168 hours)
       - Measurements before 12 hours are not reliable
       - After 168 hours (7 days), different criteria apply
    
    2. Total serum bilirubin: Laboratory measurement in mg/dL
       - Transcutaneous measurements can be used for screening
       - Serum bilirubin is required for accurate risk assessment
    
    Important Notes:
    - Only validated for neonates ≥35 weeks gestational age
    - Not for infants with positive direct Coombs test
    - Not for infants who received phototherapy before 60 hours
    - Not for determining need for exchange transfusion
    
    References (Vancouver style):
    1. Bhutani VK, Johnson L, Sivieri EM. Predictive ability of a predischarge hour-specific 
       serum bilirubin for subsequent significant hyperbilirubinemia in healthy term and 
       near-term newborns. Pediatrics. 1999 Jan;103(1):6-14. doi: 10.1542/peds.103.1.6.
    2. American Academy of Pediatrics Subcommittee on Hyperbilirubinemia. Management of 
       hyperbilirubinemia in the newborn infant 35 or more weeks of gestation. Pediatrics. 
       2004 Jul;114(1):297-316. doi: 10.1542/peds.114.1.297.
    """
    
    age_hours: int = Field(
        ...,
        ge=12,
        le=168,
        description="Age of neonate in hours from birth (12-168). Measurements before 12 hours "
                   "are not reliable for prediction. After 168 hours (7 days), different "
                   "criteria for jaundice evaluation apply.",
        example=48
    )
    
    total_bilirubin: float = Field(
        ...,
        gt=0.1,
        le=30.0,
        description="Total serum bilirubin level in mg/dL. Transcutaneous bilirubin can be "
                   "used for screening but serum bilirubin is required for accurate risk "
                   "assessment. Normal range varies significantly with age in hours.",
        example=9.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_hours": 48,
                "total_bilirubin": 9.5
            }
        }


class HourSpecificNeonatalHyperbilirubinemiaResponse(BaseModel):
    """
    Response model for Hour-Specific Risk for Neonatal Hyperbilirubinemia
    
    The Bhutani nomogram stratifies neonates into four risk zones:
    
    1. Low Risk (<40th percentile): 0% probability of subsequent hyperbilirubinemia
    2. Low-Intermediate (40-75th): 2.2% probability
    3. High-Intermediate (76-94th): 12.9% probability
    4. High Risk (≥95th percentile): 39.5% probability
    
    Follow-up recommendations are based on both risk zone and discharge timing:
    - Discharged <24 hrs: See by 72 hrs
    - Discharged 24-48 hrs: See by 96 hrs
    - Discharged 48-72 hrs: See by 120 hrs
    
    Reference: Bhutani VK, et al. Pediatrics. 1999;103(1):6-14.
    """
    
    result: str = Field(
        ...,
        description="Risk zone classification based on Bhutani nomogram (Low Risk, "
                   "Low-Intermediate Risk, High-Intermediate Risk, or High Risk)",
        example="Low-Intermediate Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="zone"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with probability of subsequent hyperbilirubinemia "
                   "and recommended follow-up timing based on risk zone",
        example="Low-intermediate risk zone. Small risk of subsequent hyperbilirubinemia "
                "(2.2% probability). Follow-up within 48-72 hours recommended based on "
                "clinical factors."
    )
    
    stage: str = Field(
        ...,
        description="Risk zone category (Low Risk, Low-Intermediate Risk, High-Intermediate Risk, "
                   "or High Risk)",
        example="Low-Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Percentile range description for the risk zone",
        example="40th-75th percentile"
    )
    
    percentile: float = Field(
        ...,
        ge=0,
        le=100,
        description="Estimated percentile of the bilirubin measurement on the Bhutani nomogram "
                   "for the specific postnatal age",
        example=55.3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Low-Intermediate Risk",
                "unit": "zone",
                "interpretation": "Low-intermediate risk zone. Small risk of subsequent "
                                "hyperbilirubinemia (2.2% probability). Follow-up within "
                                "48-72 hours recommended based on clinical factors.",
                "stage": "Low-Intermediate Risk",
                "stage_description": "40th-75th percentile",
                "percentile": 55.3
            }
        }