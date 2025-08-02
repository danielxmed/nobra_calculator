"""
Immunization Schedule Calculator Models

Request and response models for immunization schedule calculation.

References (Vancouver style):
1. Centers for Disease Control and Prevention. Child and Adolescent Immunization Schedule by Age. 
   Atlanta, GA: CDC; 2024. Available from: https://www.cdc.gov/vaccines/hcp/imz-schedules/child-adolescent-age.html
2. Centers for Disease Control and Prevention. Adult Immunization Schedule by Age. 
   Atlanta, GA: CDC; 2024. Available from: https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html
3. Advisory Committee on Immunization Practices (ACIP). General recommendations on immunization. 
   MMWR Recomm Rep. 2011;60(RR-2):1-64. doi: 10.15585/mmwr.rr6002a1
4. Kroger AT, Duchin J, Vázquez M. General Best Practice Guidelines for Immunization. 
   Best Practices Guidance of the Advisory Committee on Immunization Practices (ACIP). 
   Atlanta, GA: CDC; 2017.

The Immunization Schedule Calculator is a clinical decision support tool that determines what 
immunizations/vaccinations are due based on patient's age according to CDC vaccination guidelines. 
This tool helps healthcare providers identify appropriate vaccinations for pediatric and adult 
patients based on standardized immunization schedules. The calculator provides general vaccination 
recommendations but requires clinical judgment and knowledge of patient's vaccination history for 
optimal use.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class ImmunizationScheduleCalculatorRequest(BaseModel):
    """
    Request model for Immunization Schedule Calculator
    
    The calculator determines vaccination recommendations based on patient age according to CDC guidelines:
    
    Age Groups:
    - under_2_years: Infants and toddlers (0-23 months) - requires age_months parameter
    - 2_years_and_over: Children and adults (2-120 years) - requires age_years parameter
    
    Vaccination Schedules:
    - Infant Schedule (0-23 months): Primary vaccination series including DTaP, Hib, IPV, PCV13, 
      RV, MMR, Varicella, Hepatitis A/B, and others according to CDC pediatric schedule
    - Child/Adolescent Schedule (2-17 years): Catch-up vaccinations, boosters, HPV series, 
      meningococcal vaccines, and annual influenza
    - Adult Schedule (18+ years): Annual influenza, Tdap/Td boosters, pneumococcal vaccines, 
      zoster vaccine, and risk-based recommendations
    
    Clinical Considerations:
    - Patient's complete vaccination history must be considered
    - Contraindications include immunocompromised state for live vaccines
    - Pregnancy is a contraindication for live vaccines
    - High-risk conditions may require additional vaccines
    - Catch-up schedules apply for delayed vaccinations
    
    References (Vancouver style):
    1. Centers for Disease Control and Prevention. Child and Adolescent Immunization Schedule by Age. 
    Atlanta, GA: CDC; 2024. Available from: https://www.cdc.gov/vaccines/hcp/imz-schedules/child-adolescent-age.html
    2. Centers for Disease Control and Prevention. Adult Immunization Schedule by Age. 
    Atlanta, GA: CDC; 2024. Available from: https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html
    3. Advisory Committee on Immunization Practices (ACIP). General recommendations on immunization. 
    MMWR Recomm Rep. 2011;60(RR-2):1-64. doi: 10.15585/mmwr.rr6002a1
    """
    
    age_group: Literal["under_2_years", "2_years_and_over"] = Field(
        ...,
        description="Patient age group category to determine appropriate vaccination schedule. 'under_2_years' for infants/toddlers (0-23 months), '2_years_and_over' for children and adults (2-120 years)",
        example="under_2_years"
    )
    
    age_months: Optional[int] = Field(
        None,
        ge=0,
        le=23,
        description="Patient age in months (required and valid only when age_group is 'under_2_years'). Used to determine infant vaccination schedule according to CDC pediatric immunization guidelines",
        example=6
    )
    
    age_years: Optional[int] = Field(
        None,
        ge=2,
        le=120,
        description="Patient age in years (required and valid only when age_group is '2_years_and_over'). Used to determine child, adolescent, or adult vaccination schedule according to CDC guidelines",
        example=25
    )
    
    @validator('age_months')
    def validate_age_months(cls, v, values):
        if 'age_group' in values:
            if values['age_group'] == 'under_2_years' and v is None:
                raise ValueError('age_months is required when age_group is under_2_years')
            if values['age_group'] == '2_years_and_over' and v is not None:
                raise ValueError('age_months should not be provided when age_group is 2_years_and_over')
        return v
    
    @validator('age_years')
    def validate_age_years(cls, v, values):
        if 'age_group' in values:
            if values['age_group'] == '2_years_and_over' and v is None:
                raise ValueError('age_years is required when age_group is 2_years_and_over')
            if values['age_group'] == 'under_2_years' and v is not None:
                raise ValueError('age_years should not be provided when age_group is under_2_years')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age_group": "under_2_years",
                "age_months": 6,
                "age_years": None
            }
        }


class ImmunizationScheduleCalculatorResponse(BaseModel):
    """
    Response model for Immunization Schedule Calculator
    
    The response provides vaccination recommendations based on CDC immunization schedules:
    
    Schedule Categories:
    - Pediatric Schedule (0-23 months): Focuses on primary vaccination series with specific timing
    - Child/Adolescent Schedule (2-17 years): Emphasizes catch-up vaccinations and boosters
    - Adult Schedule (18+ years): Concentrates on routine adult vaccines and age-specific recommendations
    
    Key Vaccination Components:
    - Primary Series: Initial vaccinations for disease protection (DTaP, MMR, etc.)
    - Booster Doses: Reinforcement of immunity (Tdap every 10 years)
    - Annual Vaccines: Yearly recommendations (influenza)
    - Age-Specific: Vaccines recommended at certain ages (HPV at 11-12 years, zoster at 50+)
    - Risk-Based: Additional vaccines for high-risk individuals
    
    Clinical Applications:
    - Routine vaccination scheduling for healthy individuals
    - Catch-up immunizations for delayed schedules
    - Travel medicine preparation
    - Occupational health assessments
    - Patient counseling and education
    
    Reference: Centers for Disease Control and Prevention. Immunization Schedules. Atlanta, GA: CDC; 2024.
    """
    
    result: str = Field(
        ...,
        description="Comprehensive vaccination recommendations based on patient age and CDC immunization guidelines, including specific vaccines due and general clinical guidance",
        example="DTaP (3rd dose); Hib (3rd dose); PCV13 (3rd dose); RV (3rd dose); Hepatitis B (2nd dose); Influenza (annual); Consider patient's vaccination history and any contraindications.; Consult current CDC immunization schedules for most up-to-date recommendations."
    )
    
    unit: Optional[str] = Field(
        None,
        description="Unit of measurement for the result (null for vaccination recommendations)",
        example=None
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and guidance for vaccination management based on patient age group and CDC recommendations",
        example="Follow CDC pediatric immunization schedule with appropriate spacing between doses. Ensure primary vaccination series is completed on time. Consider patient's vaccination history and any contraindications. Live vaccines are contraindicated in immunocompromised patients."
    )
    
    stage: str = Field(
        ...,
        description="Vaccination schedule category based on patient age (Pediatric Schedule, Child/Adolescent Schedule, Adult Schedule)",
        example="Pediatric Schedule"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the vaccination schedule category",
        example="Infant and toddler vaccination schedule"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "DTaP (3rd dose); Hib (3rd dose); PCV13 (3rd dose); RV (3rd dose); Hepatitis B (2nd dose); Influenza (annual); Consider patient's vaccination history and any contraindications.; Consult current CDC immunization schedules for most up-to-date recommendations.",
                "unit": None,
                "interpretation": "Follow CDC pediatric immunization schedule with appropriate spacing between doses. Ensure primary vaccination series is completed on time. Consider patient's vaccination history and any contraindications. Live vaccines are contraindicated in immunocompromised patients.",
                "stage": "Pediatric Schedule",
                "stage_description": "Infant and toddler vaccination schedule"
            }
        }