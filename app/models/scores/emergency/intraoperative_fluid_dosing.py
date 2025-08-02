"""
Intraoperative Fluid Dosing in Adult Patients Models

Request and response models for intraoperative fluid dosing calculation.

References (Vancouver style):
1. Miller RD, Cohen NH, Eriksson LI, Fleisher LA, Wiener-Kronish JP, Young WL, editors. 
   Miller's Anesthesia. 8th ed. Philadelphia: Elsevier Saunders; 2015.
2. Holte K, Sharrock NE, Kehlet H. Pathophysiology and clinical implications of perioperative 
   fluid excess. Br J Anaesth. 2002;89(4):622-32. doi: 10.1093/bja/aef220.
3. Brandstrup B, Tønnesen H, Beier-Holgersen R, Hjørtsø E, Ørding H, Lindorff-Larsen K, 
   et al. Effects of intravenous fluid restriction on postoperative complications: comparison 
   of two perioperative fluid regimens: a randomized assessor-blinded multicenter trial. 
   Ann Surg. 2003;238(5):641-8. doi: 10.1097/01.sla.0000094387.50865.23.
4. Gan TJ, Soppitt A, Maroof M, el-Moalem H, Robertson KM, Moretti E, et al. Goal-directed 
   intraoperative fluid administration reduces length of hospital stay after major surgery. 
   Anesthesiology. 2002;97(4):820-6. doi: 10.1097/00000542-200210000-00012.

The Intraoperative Fluid Dosing calculator provides evidence-based fluid management for adult 
patients during surgery. It calculates hourly fluid requirements, NPO deficit replacement, 
and surgical trauma-related fluid losses to optimize perioperative outcomes. The calculator 
uses a structured approach with initial deficit replacement followed by maintenance and 
ongoing loss replacement based on surgical trauma severity.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IntraoperativeFluidDosingRequest(BaseModel):
    """
    Request model for Intraoperative Fluid Dosing in Adult Patients
    
    The calculator determines intraoperative IV fluid requirements based on three key parameters:
    
    Patient Factors:
    - Body weight (≥20 kg): Used to calculate baseline maintenance fluid requirements and 
      surgical trauma-related losses
    
    Preoperative Status:
    - NPO time: Duration of fasting before surgery affects fluid deficit that needs replacement
    
    Surgical Factors:
    - Trauma severity: Categorizes procedures by expected fluid loss and tissue trauma
    
    Calculation Methodology:
    - Hourly maintenance fluid = body weight (kg) + 40 mL
    - NPO fluid deficit = hourly maintenance fluid × hours NPO
    - Fluid replacement schedule:
      * Hour 1: ½ NPO deficit + hourly maintenance
      * Hours 2-3: ¼ NPO deficit + hourly maintenance + surgical trauma loss
      * Hour 4+: hourly maintenance + surgical trauma loss
    
    Surgical Trauma Classifications:
    - Minimal (3 mL/kg/hr): Laparoscopic procedures, minor surface procedures
    - Moderate (5 mL/kg/hr): Open cholecystectomy, appendectomy, hernia repair
    - Severe (7 mL/kg/hr): Bowel resection, major abdominal surgery, extensive orthopedic procedures
    
    Clinical Considerations:
    - Not recommended for patients with fluid overload risks (heart failure, COPD, kidney failure)
    - Requires continuous monitoring of hemodynamics, urine output, and fluid balance
    - Should be used in conjunction with clinical judgment and patient-specific factors
    
    References (Vancouver style):
    1. Miller RD, Cohen NH, Eriksson LI, Fleisher LA, Wiener-Kronish JP, Young WL, editors. 
    Miller's Anesthesia. 8th ed. Philadelphia: Elsevier Saunders; 2015.
    2. Holte K, Sharrock NE, Kehlet H. Pathophysiology and clinical implications of perioperative 
    fluid excess. Br J Anaesth. 2002;89(4):622-32. doi: 10.1093/bja/aef220.
    3. Brandstrup B, Tønnesen H, Beier-Holgersen R, Hjørtsø E, Ørding H, Lindorff-Larsen K, 
    et al. Effects of intravenous fluid restriction on postoperative complications: comparison 
    of two perioperative fluid regimens: a randomized assessor-blinded multicenter trial. 
    Ann Surg. 2003;238(5):641-8. doi: 10.1097/01.sla.0000094387.50865.23.
    """
    
    weight_kg: float = Field(
        ...,
        ge=20,
        le=300,
        description="Patient body weight in kilograms. Must be ≥20 kg for adult calculator. Used to calculate baseline maintenance fluid requirements (weight + 40 mL/hr) and surgical trauma-related fluid losses based on body surface area",
        example=70.0
    )
    
    hours_npo: float = Field(
        ...,
        ge=0,
        le=48,
        description="Time spent NPO (nothing by mouth) before surgery in hours. Determines fluid deficit that needs replacement during the first few hours of surgery. Longer NPO times result in larger deficits requiring more aggressive initial fluid replacement",
        example=8.0
    )
    
    surgical_trauma: Literal["minimal", "moderate", "severe"] = Field(
        ...,
        description="Estimated surgical trauma severity based on procedure type, invasiveness, and expected tissue trauma. Minimal (3 mL/kg/hr): laparoscopic procedures, minor surface operations. Moderate (5 mL/kg/hr): open cholecystectomy, appendectomy, hernia repair. Severe (7 mL/kg/hr): bowel resection, major abdominal surgery, extensive orthopedic procedures",
        example="moderate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight_kg": 70.0,
                "hours_npo": 8.0,
                "surgical_trauma": "moderate"
            }
        }


class IntraoperativeFluidDosingResponse(BaseModel):
    """
    Response model for Intraoperative Fluid Dosing in Adult Patients
    
    The response provides a structured fluid management plan including:
    
    Fluid Plan Components:
    - Hourly maintenance fluid requirements based on body weight
    - Total NPO deficit calculation and replacement schedule
    - Surgical trauma-related fluid losses based on procedure severity
    - Hour-by-hour fluid administration recommendations
    - Total fluid requirements for the first 4 hours of surgery
    
    Clinical Applications:
    - Perioperative fluid management in adult surgical patients
    - Prevention of both hypovolemia and fluid overload
    - Goal-directed fluid therapy planning
    - Optimization of patient outcomes through evidence-based fluid management
    
    Monitoring Requirements:
    - Continuous hemodynamic monitoring (blood pressure, heart rate)
    - Urine output monitoring (target >0.5 mL/kg/hr)
    - Central venous pressure monitoring for complex cases
    - Blood loss and third-space loss assessment
    - Electrolyte and acid-base balance monitoring
    
    Key Benefits of Structured Fluid Management:
    - Reduced postoperative complications
    - Shorter hospital length of stay
    - Improved wound healing
    - Reduced risk of pulmonary edema and tissue edema
    - Better hemodynamic stability
    
    Reference: Gan TJ, et al. Goal-directed intraoperative fluid administration reduces 
    length of hospital stay after major surgery. Anesthesiology. 2002;97(4):820-6.
    """
    
    result: str = Field(
        ...,
        description="Structured intraoperative fluid dosing plan with hourly maintenance requirements, NPO deficit replacement schedule, surgical trauma losses, and hour-by-hour fluid administration recommendations",
        example="Hourly maintenance fluid: 110 mL/hr; NPO deficit (total): 880 mL (8.0 hrs NPO); Surgical trauma loss: 350 mL/hr (moderate trauma); ; Hour-by-hour fluid requirements:; Hour 1: 550 mL (½ NPO deficit + maintenance); Hours 2-3: 680 mL/hr (¼ NPO deficit + maintenance + surgical loss); Hour 4+: 460 mL/hr (maintenance + surgical loss); ; Total first 4 hours: 2370 mL"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for fluid volumes",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and monitoring recommendations based on surgical trauma severity and patient-specific fluid requirements",
        example="Moderate tissue trauma and fluid loss procedures such as open cholecystectomy or appendectomy. Requires 5 mL/kg/hr (350 mL/hr for this patient) additional fluid replacement for surgical losses. Close monitoring of hemodynamics, urine output, and fluid balance is essential. Consider goal-directed fluid therapy."
    )
    
    stage: str = Field(
        ...,
        description="Surgical trauma severity category (Minimal Trauma, Moderate Trauma, Severe Trauma)",
        example="Moderate Trauma"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the trauma severity category",
        example="Moderate fluid loss procedures"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Hourly maintenance fluid: 110 mL/hr; NPO deficit (total): 880 mL (8.0 hrs NPO); Surgical trauma loss: 350 mL/hr (moderate trauma); ; Hour-by-hour fluid requirements:; Hour 1: 550 mL (½ NPO deficit + maintenance); Hours 2-3: 680 mL/hr (¼ NPO deficit + maintenance + surgical loss); Hour 4+: 460 mL/hr (maintenance + surgical loss); ; Total first 4 hours: 2370 mL",
                "unit": "mL",
                "interpretation": "Moderate tissue trauma and fluid loss procedures such as open cholecystectomy or appendectomy. Requires 5 mL/kg/hr (350 mL/hr for this patient) additional fluid replacement for surgical losses. Close monitoring of hemodynamics, urine output, and fluid balance is essential. Consider goal-directed fluid therapy.",
                "stage": "Moderate Trauma",
                "stage_description": "Moderate fluid loss procedures"
            }
        }