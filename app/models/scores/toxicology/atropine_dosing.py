"""
Atropine Dosing for Cholinesterase Inhibitor Toxicity Models

Request and response models for atropine dosing calculation.

References (Vancouver style):
1. Howland MA. Antidotes in Depth: Atropine. In: Hoffman RS, Howland MA, Lewin NA, 
   Nelson LS, Goldfrank LR, eds. Goldfrank's Toxicologic Emergencies. 10th ed. 
   New York, NY: McGraw-Hill; 2015.
2. Abedin MJ, Sayeed AA, Basher A, Maude RJ, Hoque G, Faiz MA. Open-label randomized 
   clinical trial of atropine bolus injection versus incremental boluses plus infusion 
   for organophosphate poisoning in Bangladesh. Clin Toxicol (Phila). 2012 Jun;50(5):433-40. 
   doi: 10.3109/15563650.2012.681163.
3. Eddleston M, Dawson A, Karalliedde L, Dissanayake W, Hittarage A, Azher S, et al. 
   Early management after self-poisoning with an organophosphorus or carbamate pesticide - 
   a treatment protocol for junior doctors. Crit Care. 2004 Dec;8(6):R391-7. 
   doi: 10.1186/cc2953.

Atropine is the primary antidote for cholinesterase inhibitor toxicity, which can result 
from exposure to organophosphate insecticides, nerve agents, or certain medications. 
The calculator provides initial dosing recommendations and a protocol for dose escalation 
until atropinization is achieved.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, List, Dict


class AtropineDosingRequest(BaseModel):
    """
    Request model for Atropine Dosing for Cholinesterase Inhibitor Toxicity
    
    Atropine is administered to counteract muscarinic effects of cholinesterase 
    inhibitor toxicity. Dosing varies by patient type and severity:
    
    Initial Dosing:
    - Pediatric: 0.02 mg/kg (up to adult maximum dose)
    - Adult, mild toxicity: 1-2 mg
    - Adult, severe toxicity: 3-5 mg
    
    Protocol:
    - Assess for atropinization every 5 minutes
    - If not achieved, double the previous dose
    - Once atropinized, start continuous infusion at 10% of total initial doses per hour
    
    Atropinization endpoints:
    - Clear lung exam (no rales/rhonchi)
    - Heart rate >80 bpm
    - Systolic blood pressure >80 mmHg
    
    References (Vancouver style):
    1. Howland MA. Antidotes in Depth: Atropine. In: Hoffman RS, Howland MA, Lewin NA, 
       Nelson LS, Goldfrank LR, eds. Goldfrank's Toxicologic Emergencies. 10th ed. 
       New York, NY: McGraw-Hill; 2015.
    2. Abedin MJ, Sayeed AA, Basher A, Maude RJ, Hoque G, Faiz MA. Open-label randomized 
       clinical trial of atropine bolus injection versus incremental boluses plus infusion 
       for organophosphate poisoning in Bangladesh. Clin Toxicol (Phila). 2012 Jun;50(5):433-40.
    3. Eddleston M, Dawson A, Karalliedde L, Dissanayake W, Hittarage A, Azher S, et al. 
       Early management after self-poisoning with an organophosphorus or carbamate pesticide - 
       a treatment protocol for junior doctors. Crit Care. 2004 Dec;8(6):R391-7.
    """
    
    patient_type: Literal["adult", "pediatric"] = Field(
        ...,
        description="Patient age category. Adult patients receive fixed dose ranges based on severity. Pediatric patients receive weight-based dosing",
        example="adult"
    )
    
    weight: Optional[float] = Field(
        None,
        description="Patient weight in kilograms. Required for pediatric patients to calculate weight-based dosing (0.02 mg/kg). Optional for adults",
        example=70.0,
        ge=0.1,
        le=300
    )
    
    severity: Literal["mild", "severe"] = Field(
        ...,
        description="Severity of cholinesterase inhibitor toxicity. Mild toxicity (minor symptoms): 1-2 mg for adults. Severe toxicity (respiratory distress, altered mental status): 3-5 mg for adults",
        example="severe"
    )
    
    @field_validator('weight')
    def validate_weight_for_pediatric(cls, v, values):
        """Ensure weight is provided for pediatric patients"""
        if 'patient_type' in values and values['patient_type'] == 'pediatric' and v is None:
            raise ValueError('Weight is required for pediatric patients')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_type": "adult",
                "severity": "severe",
                "weight": None
            }
        }


class DosingResult(BaseModel):
    """Detailed dosing recommendations"""
    initial_dose: str = Field(
        ...,
        description="Recommended initial atropine dose",
        example="3-5 mg"
    )
    initial_dose_mg: float = Field(
        ...,
        description="Numeric value of recommended dose in mg",
        example=4.0
    )
    dose_range: Dict[str, float] = Field(
        ...,
        description="Minimum and maximum dose range",
        example={"min": 3.0, "max": 5.0}
    )
    escalation_protocol: str = Field(
        ...,
        description="Protocol for dose escalation if atropinization not achieved",
        example="Double dose every 5 minutes until atropinization achieved"
    )
    infusion_rate: str = Field(
        ...,
        description="Continuous infusion rate calculation",
        example="10% of total initial doses per hour"
    )
    infusion_examples: List[str] = Field(
        ...,
        description="Example infusion rates based on total initial doses",
        example=["10 mg total → 1.0 mg/hr", "20 mg total → 2.0 mg/hr"]
    )


class AtropineDosingResponse(BaseModel):
    """
    Response model for Atropine Dosing for Cholinesterase Inhibitor Toxicity
    
    Provides complete atropine dosing recommendations including:
    - Initial dose based on patient type and severity
    - Escalation protocol for achieving atropinization
    - Continuous infusion rate calculations
    - Clinical interpretation and monitoring parameters
    
    Reference: Howland MA. In: Goldfrank's Toxicologic Emergencies. 10th ed. 2015.
    """
    
    result: DosingResult = Field(
        ...,
        description="Complete dosing recommendations including initial dose and protocols",
        example={
            "initial_dose": "3-5 mg",
            "initial_dose_mg": 4.0,
            "dose_range": {"min": 3.0, "max": 5.0},
            "escalation_protocol": "Double dose every 5 minutes until atropinization achieved",
            "infusion_rate": "10% of total initial doses per hour",
            "infusion_examples": [
                "10 mg total → 1.0 mg/hr",
                "20 mg total → 2.0 mg/hr",
                "50 mg total → 5.0 mg/hr",
                "100 mg total → 10.0 mg/hr"
            ]
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for doses",
        example="mg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with detailed protocol for atropine administration and monitoring",
        example="Initial atropine dose: 3-5 mg\n\nReassess for atropinization every 5 minutes..."
    )
    
    stage: str = Field(
        ...,
        description="Severity classification",
        example="Severe"
    )
    
    stage_description: str = Field(
        ...,
        description="Patient and toxicity description",
        example="Adult patient with severe toxicity"
    )
    
    warnings: List[str] = Field(
        ...,
        description="Important warnings and considerations",
        example=[
            "Not indicated for isolated bradycardia",
            "Large cumulative doses may be necessary",
            "Immediate decontamination is critical",
            "Consider concurrent pralidoxime administration"
        ]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "initial_dose": "3-5 mg",
                    "initial_dose_mg": 4.0,
                    "dose_range": {"min": 3.0, "max": 5.0},
                    "escalation_protocol": "Double dose every 5 minutes until atropinization achieved",
                    "infusion_rate": "10% of total initial doses per hour",
                    "infusion_examples": [
                        "10 mg total → 1.0 mg/hr",
                        "20 mg total → 2.0 mg/hr",
                        "50 mg total → 5.0 mg/hr",
                        "100 mg total → 10.0 mg/hr"
                    ]
                },
                "unit": "mg",
                "interpretation": "Initial atropine dose: 3-5 mg\n\nReassess for atropinization every 5 minutes:\n• Clear lung exam (no rales/rhonchi)\n• Heart rate >80 bpm\n• Systolic blood pressure >80 mmHg\n\nIf not atropinized, double the previous dose.\n\nOnce atropinized, start continuous infusion at 10% of total initial doses per hour.\n\nExample infusion rates:\n• 10 mg total → 1.0 mg/hr\n• 20 mg total → 2.0 mg/hr\n• 50 mg total → 5.0 mg/hr\n• 100 mg total → 10.0 mg/hr",
                "stage": "Severe",
                "stage_description": "Adult patient with severe toxicity",
                "warnings": [
                    "Not indicated for isolated bradycardia",
                    "Large cumulative doses may be necessary",
                    "Immediate decontamination is critical",
                    "Consider concurrent pralidoxime administration"
                ]
            }
        }