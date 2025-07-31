"""
Neonatal Early-Onset Sepsis Calculator Models

Request and response models for Neonatal Early-Onset Sepsis risk calculation.

References (Vancouver style):
1. Puopolo KM, Draper D, Wi S, Newman TB, Zupancic J, Lieberman E, et al. Estimating 
   the probability of neonatal early-onset infection on the basis of maternal risk 
   factors. Pediatrics. 2011 Nov;128(5):e1155-63. doi: 10.1542/peds.2010-3464.
2. Kuzniewicz MW, Walsh EM, Li S, Fischer A, Escobar GJ. Development and 
   implementation of an early-onset sepsis calculator to guide antibiotic management 
   in late preterm and term neonates. Jt Comm J Qual Patient Saf. 2016 May;42(5):232-9. 
   doi: 10.1016/S1553-7250(16)42030-1.
3. Puopolo KM, Benitz WE, Zaoutis TE; Committee on Fetus and Newborn; Committee on 
   Infectious Diseases. Management of Neonates Born at ≥35 0/7 Weeks' Gestation With 
   Suspected or Proven Early-Onset Bacterial Sepsis. Pediatrics. 2018 Dec;142(6):e20182894. 
   doi: 10.1542/peds.2018-2894.

The Neonatal Early-Onset Sepsis (EOS) Calculator uses a multivariate predictive model 
to estimate the probability of culture-positive sepsis within 72 hours of birth in 
newborns ≥34 weeks gestation. It combines maternal risk factors with the infant's 
clinical presentation to guide antibiotic management decisions and reduce unnecessary 
antibiotic exposure while maintaining safety.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class NeonatalEarlyOnsetSepsisRequest(BaseModel):
    """
    Request model for Neonatal Early-Onset Sepsis Calculator
    
    The calculator uses 5 maternal intrapartum risk factors to estimate EOS risk:
    
    1. Gestational Age: Prematurity is a significant risk factor
    2. Maternal Temperature: Maternal fever increases risk of vertical transmission
    3. ROM Duration: Prolonged rupture increases ascending infection risk
    4. GBS Status: Major pathogen in early-onset sepsis
    5. Antibiotics: Intrapartum prophylaxis reduces transmission risk
    
    The model uses logistic regression with these predictors to calculate 
    probability of culture-positive sepsis in the first 72 hours of life.

    References (Vancouver style):
    1. Puopolo KM, Draper D, Wi S, Newman TB, Zupancic J, Lieberman E, et al. Estimating 
    the probability of neonatal early-onset infection on the basis of maternal risk 
    factors. Pediatrics. 2011 Nov;128(5):e1155-63. doi: 10.1542/peds.2010-3464.
    """
    
    gestational_age_weeks: float = Field(
        ...,
        ge=34,
        le=43,
        description="Gestational age in weeks (e.g., 38.5 for 38 weeks 3 days). Must be ≥34 weeks. Calculator is validated for late preterm and term infants only",
        example=39.0
    )
    
    maternal_temp_celsius: float = Field(
        ...,
        ge=35,
        le=42,
        description="Highest maternal antepartum temperature in Celsius. Use the highest documented temperature during labor and before delivery",
        example=37.2
    )
    
    rom_hours: float = Field(
        ...,
        ge=0,
        le=240,
        description="Duration of rupture of membranes (ROM) in hours. Time from membrane rupture to delivery. Prolonged ROM >18 hours is a risk factor",
        example=12.5
    )
    
    gbs_status: Literal["negative", "positive", "unknown"] = Field(
        ...,
        description="Maternal Group B Streptococcus (GBS) status. Negative: negative screen at 35-37 weeks. Positive: positive screen or GBS bacteriuria. Unknown: no screening or unknown result",
        example="negative"
    )
    
    antibiotics_type: Literal[
        "broad_spectrum_gt_4hrs",
        "broad_spectrum_2_to_4hrs",
        "gbs_specific_gt_2hrs",
        "no_antibiotics_or_lt_2hrs"
    ] = Field(
        ...,
        description=(
            "Type and timing of intrapartum antibiotics. "
            "broad_spectrum_gt_4hrs: Broad-spectrum antibiotics given >4 hours before birth. "
            "broad_spectrum_2_to_4hrs: Broad-spectrum antibiotics given 2-3.9 hours before birth. "
            "gbs_specific_gt_2hrs: GBS-specific antibiotics (penicillin, ampicillin) given >2 hours before birth. "
            "no_antibiotics_or_lt_2hrs: No antibiotics or any antibiotics given <2 hours before birth"
        ),
        example="no_antibiotics_or_lt_2hrs"
    )
    
    @field_validator('gestational_age_weeks')
    def validate_gestational_age_precision(cls, v):
        """Ensure gestational age has reasonable precision"""
        # Round to 1 decimal place (days precision)
        return round(v, 1)
    
    @field_validator('maternal_temp_celsius')
    def validate_temperature_precision(cls, v):
        """Ensure temperature has reasonable precision"""
        # Round to 1 decimal place
        return round(v, 1)
    
    @field_validator('rom_hours')
    def validate_rom_precision(cls, v):
        """Ensure ROM hours has reasonable precision"""
        # Round to 1 decimal place
        return round(v, 1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "gestational_age_weeks": 39.0,
                "maternal_temp_celsius": 37.2,
                "rom_hours": 12.5,
                "gbs_status": "negative",
                "antibiotics_type": "no_antibiotics_or_lt_2hrs"
            }
        }


class NeonatalEarlyOnsetSepsisResponse(BaseModel):
    """
    Response model for Neonatal Early-Onset Sepsis Calculator
    
    The calculator provides EOS risk per 1000 live births with interpretation:
    - Very Low Risk (<0.5/1000): Routine care with observation
    - Low Risk (0.5-1.0/1000): Enhanced observation may be considered
    - Intermediate Risk (1.0-3.0/1000): Enhanced observation, consider blood culture
    - High Risk (3.0-10.0/1000): Blood culture and antibiotics strongly recommended
    - Very High Risk (≥10.0/1000): Blood culture, antibiotics, and NICU monitoring
    
    The calculator estimates risk at birth. Clinical examination findings 
    (well-appearing, equivocal, or clinical illness) can modify this baseline risk.
    
    Reference: Puopolo KM, et al. Pediatrics. 2011;128(5):e1155-63.
    """
    
    result: float = Field(
        ...,
        ge=0,
        description="Early-onset sepsis risk per 1000 live births calculated from maternal risk factors",
        example=1.85
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="per 1000 births"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on risk level",
        example="Intermediate risk of early-onset sepsis. Enhanced observation recommended. Consider blood culture and empiric antibiotics based on clinical examination."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with numerical range",
        example="Risk 1.0-3.0 per 1000"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1.85,
                "unit": "per 1000 births",
                "interpretation": "Intermediate risk of early-onset sepsis. Enhanced observation recommended. Consider blood culture and empiric antibiotics based on clinical examination.",
                "stage": "Intermediate Risk",
                "stage_description": "Risk 1.0-3.0 per 1000"
            }
        }