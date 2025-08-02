"""
HIV Needle Stick Risk Assessment Stratification Protocol (RASP) Models

Request and response models for HIV Needle Stick RASP calculation.

References (Vancouver style):
1. Vertesi L. Risk Assessment Stratification Protocol (RASP) to help patients decide 
   on the use of postexposure prophylaxis for HIV exposure. CJEM. 2003 Jan;5(1):46-8.
2. Panlilio AL, Cardo DM, Grohskopf LA, Heneine W, Ross CS; U.S. Public Health Service. 
   Updated U.S. Public Health Service guidelines for the management of occupational 
   exposures to HIV and recommendations for postexposure prophylaxis. MMWR Recomm Rep. 
   2005 Sep 30;54(RR-9):1-17.
3. Cardo DM, Culver DH, Ciesielski CA, Srivastava PU, Marcus R, Abiteboul D, et al. 
   A case-control study of HIV seroconversion in health care workers after percutaneous 
   exposure. Centers for Disease Control and Prevention Needlestick Surveillance Group. 
   N Engl J Med. 1997 Nov 20;337(21):1485-90.

The RASP tool quantifies HIV transmission risk following needle stick injuries or other 
potential exposures by multiplying risk factors across four domains: source patient HIV 
status, type of body fluid, transmission route, and volume of exposure. It helps guide 
decisions about post-exposure prophylaxis (PEP) initiation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HivNeedleStickRaspRequest(BaseModel):
    """
    Request model for HIV Needle Stick Risk Assessment Stratification Protocol (RASP)
    
    RASP calculates HIV transmission risk by multiplying factors across four domains:
    
    1. Source Population (HIV status):
    - hiv_acute_aids: Known HIV+ with acute AIDS illness (risk factor: 1)
    - hiv_asymptomatic: Known HIV+ but asymptomatic (risk factor: 10)
    - unknown_high_risk: Unknown HIV status, high-risk situation (risk factor: 100)
    - unknown_low_risk: Unknown HIV status, low-risk situation (risk factor: 1000)
    
    2. Inoculum Type (body fluid):
    - fresh_blood: Fresh blood (risk factor: 1)
    - high_risk_fluids: Semen, vaginal fluid, CSF, etc. (risk factor: 10)
    - dried_old_blood: Dried or old blood (risk factor: 100)
    - low_risk_secretions: Tears, urine, saliva (risk factor: 1000)
    
    3. Transmission Method:
    - intravenous: Direct IV injection (risk factor: 1)
    - deep_intramuscular: Deep IM injection (risk factor: 10)
    - deep_transcutaneous_bleeding: Deep puncture with bleeding (risk factor: 100)
    - superficial_transcutaneous: Superficial puncture, no bleeding (risk factor: 200)
    - mucosal_contact: Contact with mucous membranes (risk factor: 500)
    - intact_skin: Contact with intact skin only (risk factor: 1000)
    
    4. Volume of Inoculum:
    - massive_transfusion: Massive exposure like transfusion (multiplier: 100)
    - measurable_over_1ml: Measurable volume >1 mL (multiplier: 10)
    - moderate_large_bore: Large-bore hollow needle >22g (multiplier: 5)
    - small_small_bore: Small-bore hollow needle <22g (multiplier: 3)
    - trace_surface_only: Trace/surface only, solid needle (multiplier: 1)

    References (Vancouver style):
    1. Vertesi L. Risk Assessment Stratification Protocol (RASP) to help patients decide 
    on the use of postexposure prophylaxis for HIV exposure. CJEM. 2003 Jan;5(1):46-8.
    2. Panlilio AL, Cardo DM, Grohskopf LA, Heneine W, Ross CS; U.S. Public Health Service. 
    Updated U.S. Public Health Service guidelines for the management of occupational 
    exposures to HIV and recommendations for postexposure prophylaxis. MMWR Recomm Rep. 
    2005 Sep 30;54(RR-9):1-17.
    """
    
    source_population: Literal["hiv_acute_aids", "hiv_asymptomatic", "unknown_high_risk", "unknown_low_risk"] = Field(
        ...,
        description="HIV status and clinical condition of source patient. Known HIV+ with acute AIDS (factor 1), known HIV+ asymptomatic (factor 10), unknown status high-risk (factor 100), unknown status low-risk (factor 1000)",
        example="unknown_high_risk"
    )
    
    inoculum_type: Literal["fresh_blood", "high_risk_fluids", "dried_old_blood", "low_risk_secretions"] = Field(
        ...,
        description="Type of body fluid involved in exposure. Fresh blood (factor 1), high-risk fluids like semen/CSF (factor 10), dried/old blood (factor 100), low-risk secretions like saliva/urine (factor 1000)",
        example="fresh_blood"
    )
    
    transmission_method: Literal["intravenous", "deep_intramuscular", "deep_transcutaneous_bleeding", "superficial_transcutaneous", "mucosal_contact", "intact_skin"] = Field(
        ...,
        description="Method of exposure/transmission route. IV injection (factor 1), deep IM (factor 10), deep puncture with bleeding (factor 100), superficial puncture (factor 200), mucosal contact (factor 500), intact skin (factor 1000)",
        example="deep_transcutaneous_bleeding"
    )
    
    inoculum_volume: Literal["massive_transfusion", "measurable_over_1ml", "moderate_large_bore", "small_small_bore", "trace_surface_only"] = Field(
        ...,
        description="Volume of inoculum/exposure. Massive like transfusion (multiplier 100), measurable >1mL (multiplier 10), large-bore needle >22g (multiplier 5), small-bore needle <22g (multiplier 3), trace/solid needle (multiplier 1)",
        example="moderate_large_bore"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "source_population": "unknown_high_risk",
                "inoculum_type": "fresh_blood",
                "transmission_method": "deep_transcutaneous_bleeding",
                "inoculum_volume": "moderate_large_bore"
            }
        }


class HivNeedleStickRaspResponse(BaseModel):
    """
    Response model for HIV Needle Stick Risk Assessment Stratification Protocol (RASP)
    
    The RASP score expresses HIV transmission risk as "1 in X" where lower X values 
    indicate higher risk. The risk is calculated by multiplying factors across four 
    domains and guides PEP recommendations:
    
    - Risk ≥1/1000 (X ≤1000): PEP definitely indicated
    - Risk 1/1001-1/10000: PEP recommended but optional
    - Risk 1/10001-1/100000: PEP optional, not generally recommended
    - Risk ≤1/100000 (X >100000): PEP not indicated
    
    Reference: Vertesi L. CJEM. 2003;5(1):46-8.
    """
    
    result: int = Field(
        ...,
        description="HIV transmission risk expressed as 1 in X, where X is the calculated risk ratio",
        example=20000
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="risk_ratio"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with PEP recommendations based on calculated risk",
        example="PEP is optional but not generally recommended. May consider in special circumstances or if exposed person has high anxiety. Ensure appropriate counseling and follow-up."
    )
    
    stage: str = Field(
        ...,
        description="PEP recommendation category (Definitely Indicated, Recommended, Optional, Not Indicated)",
        example="Optional"
    )
    
    stage_description: str = Field(
        ...,
        description="Risk range description for the recommendation category",
        example="Risk 1/10001-1/100000"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 20000,
                "unit": "risk_ratio",
                "interpretation": "PEP is optional but not generally recommended. May consider in special circumstances or if exposed person has high anxiety. Ensure appropriate counseling and follow-up.",
                "stage": "Optional",
                "stage_description": "Risk 1/10001-1/100000"
            }
        }