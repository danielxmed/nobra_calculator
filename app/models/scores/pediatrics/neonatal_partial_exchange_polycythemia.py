"""
Neonatal Partial Exchange for Polycythemia Models

Request and response models for Neonatal Partial Exchange for Polycythemia calculation.

References (Vancouver style):
1. Black VD, Lubchenco LO, Koops BL, Poland RL, Powell DP. Neonatal hyperviscosity: 
   randomized study of effect of partial plasma exchange transfusion on long-term 
   outcome. Pediatrics. 1985 Aug;76(2):225-31.
2. Roback JD, editor. Technical Manual. 18th ed. Bethesda, MD: American Association 
   of Blood Banks (AABB); 2014.

The Neonatal Partial Exchange for Polycythemia calculator estimates the total blood 
volume to remove and the crystalloid volume to infuse in neonatal polycythemia. 
Polycythemia is defined as a central venous hematocrit level greater than 65%, 
which can lead to hyperviscosity syndrome and associated complications.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class NeonatalPartialExchangePolycythemiaRequest(BaseModel):
    """
    Request model for Neonatal Partial Exchange for Polycythemia
    
    This calculator uses the following formula:
    Volume of replacement fluid = [blood volume (mL) × (initial Hct - goal Hct)] / initial Hct
    
    Blood volume estimates:
    - Preterm infants: 100 mL/kg
    - Term infants: 85 mL/kg
    
    Clinical context:
    - Consider partial exchange transfusion in infants with Hct >65% who are symptomatic
    - Consider partial exchange transfusion in asymptomatic infants with Hct >75%
    - Crystalloid replacement (normal saline) is used to avoid necrotizing enterocolitis (NEC)
    - The procedure involves simultaneous withdrawal and infusion of equal volumes
    
    References (Vancouver style):
    1. Black VD, Lubchenco LO, Koops BL, Poland RL, Powell DP. Neonatal hyperviscosity: 
       randomized study of effect of partial plasma exchange transfusion on long-term 
       outcome. Pediatrics. 1985 Aug;76(2):225-31.
    2. Roback JD, editor. Technical Manual. 18th ed. Bethesda, MD: American Association 
       of Blood Banks (AABB); 2014.
    """
    
    weight: float = Field(
        ...,
        ge=0.5,
        le=10,
        description="Patient weight in kilograms. Typical range for neonates is 0.5-10 kg",
        example=3.5
    )
    
    gestational_age: Literal["preterm", "term"] = Field(
        ...,
        description="Gestational age at birth. Preterm: <37 weeks, Term: ≥37 weeks. This affects blood volume estimation (100 mL/kg for preterm, 85 mL/kg for term)",
        example="term"
    )
    
    initial_hematocrit: float = Field(
        ...,
        ge=0,
        le=100,
        description="Initial hematocrit percentage. Polycythemia is defined as Hct >65%. Normal range for neonates is 42-65%",
        example=72
    )
    
    goal_hematocrit: float = Field(
        ...,
        ge=40,
        le=80,
        description="Goal hematocrit percentage. Recommended goal is 55-60% to reduce hyperviscosity while maintaining adequate oxygen-carrying capacity",
        example=55
    )
    
    @field_validator('goal_hematocrit')
    def validate_goal_less_than_initial(cls, v, values):
        """Ensure goal hematocrit is less than initial hematocrit"""
        if 'initial_hematocrit' in values and v >= values['initial_hematocrit']:
            raise ValueError('Goal hematocrit must be less than initial hematocrit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "weight": 3.5,
                "gestational_age": "term",
                "initial_hematocrit": 72,
                "goal_hematocrit": 55
            }
        }


class NeonatalPartialExchangePolycythemiaResponse(BaseModel):
    """
    Response model for Neonatal Partial Exchange for Polycythemia
    
    The calculated exchange volume represents both:
    - The volume of whole blood to withdraw from the infant
    - The volume of crystalloid (normal saline) to infuse simultaneously
    
    The simultaneous technique helps maintain hemodynamic stability during the procedure.
    
    Reference: Black VD, et al. Pediatrics. 1985;76(2):225-31.
    """
    
    result: float = Field(
        ...,
        description="Volume of blood to remove and crystalloid to infuse in milliliters",
        example=51.1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the exchange volume",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and procedural guidance for the partial exchange",
        example="Withdraw 51.1 mL of whole blood while simultaneously infusing 51.1 mL of normal saline. With initial Hct >65%, partial exchange is indicated if the infant is symptomatic. The procedure should be performed by experienced clinical team members following institutional policies. Monitor vital signs and hematocrit levels during and after the procedure."
    )
    
    stage: str = Field(
        ...,
        description="Type of result (always 'Exchange Volume' for this calculator)",
        example="Exchange Volume"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the exchange procedure",
        example="Remove 51.1 mL of blood and infuse 51.1 mL of crystalloid"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 51.1,
                "unit": "mL",
                "interpretation": "Withdraw 51.1 mL of whole blood while simultaneously infusing 51.1 mL of normal saline. With initial Hct >65%, partial exchange is indicated if the infant is symptomatic. The procedure should be performed by experienced clinical team members following institutional policies. Monitor vital signs and hematocrit levels during and after the procedure.",
                "stage": "Exchange Volume",
                "stage_description": "Remove 51.1 mL of blood and infuse 51.1 mL of crystalloid"
            }
        }