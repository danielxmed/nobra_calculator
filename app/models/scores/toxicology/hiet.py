"""
High-dose Insulin Euglycemia Therapy (HIET) Models

Request and response models for HIET calculation.

References (Vancouver style):
1. Holger JS, Stellpflug SJ, Cole JB, Harris CR, Engebretsen KM. High-dose insulin: 
   a consecutive case series in toxin-induced cardiogenic shock. Clin Toxicol (Phila). 
   2011 Aug;49(7):653-8. doi: 10.3109/15563650.2011.593522.
2. Greene SL, Gawarammana I, Wood DM, Jones AL, Dargan PI. Relative safety of 
   hyperinsulinaemia/euglycaemia therapy in the management of calcium channel 
   blocker overdose: a prospective observational study. Intensive Care Med. 
   2007 Nov;33(11):2019-24. doi: 10.1007/s00134-007-0768-y.
3. Engebretsen KM, Kaczmarek KM, Morgan J, Holger JS. High-dose insulin therapy 
   in beta-blocker and calcium channel-blocker poisoning. Clin Toxicol (Phila). 
   2011 Apr;49(4):277-83. doi: 10.3109/15563650.2011.582471.

High-dose Insulin Euglycemia Therapy (HIET) is an advanced treatment modality for 
severe calcium channel blocker and beta blocker overdoses. These overdoses can cause 
profound cardiovascular toxicity including cardiogenic shock, and HIET helps overcome 
the metabolic dysfunction by improving myocardial contractility and cellular metabolism.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class HietRequest(BaseModel):
    """
    Request model for High-dose Insulin Euglycemia Therapy (HIET)
    
    HIET is used for treating severe calcium channel blocker (CCB) and beta blocker (BB) 
    overdoses that result in cardiogenic shock. The therapy involves:
    
    1. Insulin Bolus: 1 unit/kg IV push
    2. Insulin Infusion: 0.5-1 unit/kg/hr (can titrate up to 10 units/kg/hr)
    3. Dextrose Infusion: To maintain euglycemia (glucose 110-250 mg/dL)
    
    Mechanism of Action:
    - Overcomes insulin resistance induced by CCB/BB toxicity
    - Improves myocardial contractility through metabolic effects
    - Enhances cellular glucose uptake and utilization
    - Provides inotropic support without increasing myocardial oxygen demand
    
    Clinical Monitoring:
    - Glucose: Every 30 minutes for first 1-2 hours, then hourly
    - Potassium: Every hour (insulin drives K+ intracellularly)
    - Hemodynamics: Every 10-15 minutes initially
    
    References (Vancouver style):
    1. Holger JS, Stellpflug SJ, Cole JB, Harris CR, Engebretsen KM. High-dose insulin: 
       a consecutive case series in toxin-induced cardiogenic shock. Clin Toxicol (Phila). 
       2011 Aug;49(7):653-8.
    2. Greene SL, Gawarammana I, Wood DM, Jones AL, Dargan PI. Relative safety of 
       hyperinsulinaemia/euglycaemia therapy in the management of calcium channel 
       blocker overdose: a prospective observational study. Intensive Care Med. 
       2007 Nov;33(11):2019-24.
    """
    
    weight: float = Field(
        ...,
        ge=1,
        le=500,
        description="Patient weight in kilograms. Used to calculate weight-based dosing for "
                    "both insulin bolus and infusion rates. Range: 1-500 kg.",
        example=70.0
    )
    
    infusion_rate: Literal["0.5", "1.0"] = Field(
        ...,
        description="Initial insulin infusion rate in units/kg/hr. Start with 0.5 units/kg/hr "
                    "for moderate toxicity or 1.0 units/kg/hr for severe toxicity. Can be "
                    "titrated up to 10 units/kg/hr based on hemodynamic response.",
        example="0.5"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight": 70.0,
                "infusion_rate": "0.5"
            }
        }


class HietProtocol(BaseModel):
    """
    HIET dosing protocol details
    """
    
    insulin_bolus: float = Field(
        ...,
        description="Initial insulin bolus dose in units (1 unit/kg IV push)",
        example=70.0
    )
    
    insulin_infusion: float = Field(
        ...,
        description="Initial insulin infusion rate in units/hr",
        example=35.0
    )
    
    dextrose_g_per_hr: float = Field(
        ...,
        description="Dextrose requirement in grams per hour (0.5 g/kg/hr)",
        example=35.0
    )
    
    d10_rate_ml_hr: float = Field(
        ...,
        description="D10W (10% dextrose) infusion rate in mL/hr",
        example=350
    )
    
    d25_rate_ml_hr: float = Field(
        ...,
        description="D25W (25% dextrose) infusion rate in mL/hr",
        example=140
    )
    
    d50_rate_ml_hr: float = Field(
        ...,
        description="D50W (50% dextrose) infusion rate in mL/hr",
        example=70
    )


class HietResponse(BaseModel):
    """
    Response model for High-dose Insulin Euglycemia Therapy (HIET)
    
    Returns a complete dosing protocol including:
    - Insulin bolus and infusion doses
    - Dextrose requirements with rates for different concentrations
    - Monitoring and titration guidance
    
    Important Clinical Considerations:
    - Concentrate insulin to prevent fluid overload (e.g., 100 units in 100 mL)
    - Hypoglycemia can occur hours after stopping insulin infusion
    - Continue therapy until hemodynamic improvement (typically 1-2 days, up to 4 days)
    - May need additional vasopressors, calcium, or other supportive measures
    
    Reference: Holger JS, et al. Clin Toxicol. 2011;49(7):653-8.
    """
    
    result: HietProtocol = Field(
        ...,
        description="Complete HIET dosing protocol with insulin and dextrose calculations",
        example={
            "insulin_bolus": 70.0,
            "insulin_infusion": 35.0,
            "dextrose_g_per_hr": 35.0,
            "d10_rate_ml_hr": 350,
            "d25_rate_ml_hr": 140,
            "d50_rate_ml_hr": 70
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="protocol"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with monitoring and titration guidance",
        example="Follow the calculated protocol with close monitoring. Check glucose every 30 minutes for 1-2 hours until stable. Monitor potassium hourly. Continue until hemodynamic improvement achieved. May increase insulin infusion up to 10 units/kg/hr if needed. Maintain glucose 110-250 mg/dL. Give dextrose 25-50g bolus if glucose <250 mg/dL."
    )
    
    stage: str = Field(
        ...,
        description="Protocol stage",
        example="HIET Protocol"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the protocol status",
        example="Dosing calculated"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "insulin_bolus": 70.0,
                    "insulin_infusion": 35.0,
                    "dextrose_g_per_hr": 35.0,
                    "d10_rate_ml_hr": 350,
                    "d25_rate_ml_hr": 140,
                    "d50_rate_ml_hr": 70
                },
                "unit": "protocol",
                "interpretation": "Follow the calculated protocol with close monitoring. Check glucose every 30 minutes for 1-2 hours until stable. Monitor potassium hourly. Continue until hemodynamic improvement achieved. May increase insulin infusion up to 10 units/kg/hr if needed. Maintain glucose 110-250 mg/dL. Give dextrose 25-50g bolus if glucose <250 mg/dL.",
                "stage": "HIET Protocol",
                "stage_description": "Dosing calculated"
            }
        }