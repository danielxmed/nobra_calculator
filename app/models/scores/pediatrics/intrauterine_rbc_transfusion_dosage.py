"""
Intrauterine RBC Transfusion Dosage Models

Request and response models for intrauterine RBC transfusion dosage calculation.

References (Vancouver style):
1. Mandelbrot L, Daffos F, Forestier F, MacAleese J, Descamps P. Assessment of fetal blood 
   volume for computer-assisted management of in utero transfusion. Fetal Ther. 1988;3(1-2):60-6.
2. Liley AW. Intrauterine transfusion of foetus in haemolytic disease. Br Med J. 1963;2(5365):1107-9.
3. Society for Maternal-Fetal Medicine (SMFM), Norton ME, Chauhan SP, Dashe JS. Society for 
   Maternal-Fetal Medicine (SMFM) Clinical Guideline #7: nonimmune hydrops fetalis. Am J Obstet 
   Gynecol. 2015;212(2):127-39.
4. Van Kamp IL, Klumper FJ, Oepkes D, Meerman RH, Scherjon SA, Vandenbussche FP, et al. 
   Complications of intrauterine intravascular transfusion for fetal anemia due to maternal 
   red-cell alloimmunization. Am J Obstet Gynecol. 2005;192(1):171-7.

The Intrauterine RBC Transfusion Dosage calculator estimates the volume of donor RBCs needed 
for intrauterine transfusion (IUT) in cases of fetal anemia, primarily due to hemolytic 
disease of the fetus and newborn (HDFN). This evidence-based tool uses fetal weight, current 
and target hematocrit levels, and donor RBC characteristics to calculate precise transfusion 
volumes, minimizing risks of over- or under-transfusion while optimizing fetal outcomes.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class IntrauterineRbcTransfusionDosageRequest(BaseModel):
    """
    Request model for Intrauterine RBC Transfusion Dosage
    
    The calculator determines the appropriate volume of donor RBCs for intrauterine transfusion using:
    
    Fetal Parameters:
    - Estimated fetal weight: Obtained from biometric measurements on ultrasound (biparietal diameter, 
      head circumference, abdominal circumference, femur length)
    - Current fetal hematocrit: Measured from fetal blood sampling, typically showing severe anemia 
      (<30% or more than 2 standard deviations below mean for gestational age)
    
    Transfusion Goals:
    - Target hematocrit: Usually 40-45% post-transfusion to optimize oxygen delivery while avoiding 
      hyperviscosity
    - Donor RBC characteristics: Packed RBCs with hematocrit typically 75-85%, should be CMV-negative, 
      irradiated, and compatible with maternal serum
    
    Calculation Methodology:
    - Fetoplacental volume = fetal weight (g) × 0.14 mL/g (based on Mandelbrot study)
    - Transfusion volume = Fetoplacental volume × [Hct(goal) - Hct(initial)] / Hct(transfused)
    
    Clinical Indications:
    - Hemolytic disease of fetus and newborn (HDFN) due to maternal alloantibodies
    - Severe fetal anemia from other causes (parvovirus B19, fetomaternal hemorrhage)
    - Twin-twin transfusion syndrome with severe anemia in donor twin
    
    Procedure Considerations:
    - Requires specialized maternal-fetal medicine expertise
    - Ultrasound-guided intravascular access (umbilical vein or intrahepatic vein)
    - Fetal immobilization with pancuronium may be necessary
    - Continuous fetal heart rate monitoring during procedure
    
    References (Vancouver style):
    1. Mandelbrot L, Daffos F, Forestier F, MacAleese J, Descamps P. Assessment of fetal blood 
    volume for computer-assisted management of in utero transfusion. Fetal Ther. 1988;3(1-2):60-6.
    2. Society for Maternal-Fetal Medicine (SMFM). Management of alloimmunization during pregnancy. 
    Am J Obstet Gynecol. 2018;218(2):B7-B18.
    """
    
    fetal_weight_g: float = Field(
        ...,
        ge=200,
        le=5000,
        description="Estimated fetal weight in grams based on biometric measurements from ultrasound examination. Used to calculate fetoplacental blood volume (14% of fetal weight). Typical range from 20 weeks gestation (~500g) to term (~3500g)",
        example=2000.0
    )
    
    initial_hematocrit: float = Field(
        ...,
        ge=5,
        le=60,
        description="Current fetal hematocrit percentage before transfusion, typically obtained from cordocentesis or fetal blood sampling. Values <30% or >2 SD below gestational age mean indicate severe fetal anemia requiring intervention",
        example=20.0
    )
    
    goal_hematocrit: float = Field(
        ...,
        ge=25,
        le=60,
        description="Target fetal hematocrit percentage after transfusion. Standard target is 40-45% to optimize oxygen delivery while avoiding hyperviscosity syndrome. Should not exceed 50% to prevent circulatory complications",
        example=42.0
    )
    
    transfused_hematocrit: float = Field(
        ...,
        ge=60,
        le=90,
        description="Hematocrit percentage of the donor packed RBC unit to be transfused. Typically 75-85% for standard packed RBCs. Donor blood should be CMV-negative, irradiated (<2500 cGy), ABO/Rh compatible, and crossmatched with maternal serum",
        example=80.0
    )
    
    @validator('goal_hematocrit')
    def validate_goal_hematocrit(cls, v, values):
        if 'initial_hematocrit' in values and v <= values['initial_hematocrit']:
            raise ValueError('goal_hematocrit must be greater than initial_hematocrit')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "fetal_weight_g": 2000.0,
                "initial_hematocrit": 20.0,
                "goal_hematocrit": 42.0,
                "transfused_hematocrit": 80.0
            }
        }


class IntrauterineRbcTransfusionDosageResponse(BaseModel):
    """
    Response model for Intrauterine RBC Transfusion Dosage
    
    The response provides the calculated transfusion volume with clinical interpretation:
    
    Volume Calculations:
    - Based on fetoplacental blood volume (14% of estimated fetal weight)
    - Accounts for desired hematocrit increase and donor RBC characteristics
    - Provides precise volume to minimize risks of over- or under-transfusion
    
    Clinical Considerations by Volume:
    - Small volumes (<20 mL): Conservative approach for early gestation or mild anemia
    - Moderate volumes (20-60 mL): Standard transfusion for established fetal anemia
    - Large volumes (>60 mL): Requires enhanced monitoring, may need staged approach
    
    Procedure Safety:
    - All volumes require continuous fetal heart rate monitoring
    - Ultrasound guidance essential for vascular access
    - Post-procedure hematocrit measurement to confirm adequacy
    - Monitor for complications: bradycardia, bleeding, cord hematoma
    
    Post-Transfusion Management:
    - Serial ultrasound examinations to assess fetal well-being
    - Middle cerebral artery Doppler studies to monitor for recurrent anemia
    - Consider repeat transfusions if anemia recurs (typically every 2-3 weeks)
    - Delivery planning based on fetal maturity and severity of condition
    
    Outcomes:
    - Successful IUT can normalize fetal hematocrit and reduce hydrops
    - May suppress fetal erythropoiesis, reducing ongoing hemolysis
    - Survival rates >95% when performed by experienced centers
    - Long-term neurodevelopmental outcomes generally favorable
    
    Reference: Van Kamp IL, et al. Complications of intrauterine intravascular transfusion 
    for fetal anemia due to maternal red-cell alloimmunization. Am J Obstet Gynecol. 2005;192(1):171-7.
    """
    
    result: float = Field(
        ...,
        description="Volume of donor RBCs needed for intrauterine transfusion in milliliters, calculated using fetoplacental volume and hematocrit parameters",
        example=15.4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for transfusion volume",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and procedural guidance based on calculated transfusion volume, fetal weight, and clinical considerations",
        example="Small volume transfusion (15.4 mL) appropriate for early gestational age or mild anemia. This volume represents a conservative approach that minimizes risk of circulatory overload. Monitor fetal heart rate closely during and after transfusion. Ensure adequate venous access and consider pre-medication to prevent fetal bradycardia. Post-transfusion hematocrit should be checked to confirm adequate response."
    )
    
    stage: str = Field(
        ...,
        description="Transfusion volume category (Small Volume, Moderate Volume, Large Volume)",
        example="Small Volume"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the volume category",
        example="Small transfusion volume"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 15.4,
                "unit": "mL",
                "interpretation": "Small volume transfusion (15.4 mL) appropriate for early gestational age or mild anemia. This volume represents a conservative approach that minimizes risk of circulatory overload. Monitor fetal heart rate closely during and after transfusion. Ensure adequate venous access and consider pre-medication to prevent fetal bradycardia. Post-transfusion hematocrit should be checked to confirm adequate response.",
                "stage": "Small Volume",
                "stage_description": "Small transfusion volume"
            }
        }