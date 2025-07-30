"""
CKiD U25 eGFR Calculator Models

Request and response models for CKiD U25 eGFR calculation.

References (Vancouver style):
1. Pierce CB, Muñoz A, Ng DK, Warady BA, Furth SL, Schwartz GJ. Age- and sex-dependent 
   clinical equations to estimate glomerular filtration rates in children and young adults 
   with chronic kidney disease. Kidney Int. 2021 Oct;100(4):948-959.
2. Schwartz GJ, Muñoz A, Schneider MF, Mak RH, Kaskel F, Warady BA, et al. New equations 
   to estimate GFR in children with CKD. J Am Soc Nephrol. 2009 Mar;20(3):629-37.
3. Levey AS, Stevens LA, Schmid CH, Zhang YL, Castro AF 3rd, Feldman HI, et al. A new 
   equation to estimate glomerular filtration rate. Ann Intern Med. 2009 May 5;150(9):604-12.

The Chronic Kidney Disease in Children (CKiD) U25 eGFR Calculator estimates glomerular 
filtration rate based on creatinine and/or cystatin C in patients aged 1 to 25 years. 
This calculator addresses the critical gap in kidney function assessment for children 
and young adults, providing superior estimation of GFR across the pediatric and young 
adult age spectrum.

Clinical Background and Development:

The CKiD U25 equations were developed from the Chronic Kidney Disease in Children (CKiD) 
study, a large prospective cohort study of children with chronic kidney disease. These 
equations offer several key advantages over previous pediatric GFR estimation methods:

Key Advantages of CKiD U25 Equations:

Seamless Transition Care:
One of the most significant challenges in pediatric nephrology is the transition from 
pediatric to adult care at age 18. Traditional approaches create "jumps" in estimated 
GFR when switching from pediatric-specific equations (like the original CKiD equation) 
to adult equations (like CKD-EPI) at age 18. The CKiD U25 equations eliminate these 
discontinuities by providing consistent GFR estimation across the entire 1-25 year 
age range, enabling seamless longitudinal monitoring of kidney function.

Superior Accuracy:
In internal validation analysis, the CKiD U25 equations outperformed 11 other published 
equations for estimating GFR in children and young adults with chronic kidney disease. 
The equations demonstrate:
- P30 accuracy of 86.2% in children younger than 18 years for creatinine-based equation
- P30 accuracy of 90.7% in young adults ages 18-25 years for creatinine-based equation
- P30 accuracy of 86.6% in children younger than 18 years for cystatin C-based equation
- P30 accuracy of 85.7% in young adults ages 18-25 years for cystatin C-based equation
(P30 indicates the percentage of estimated GFRs within 30% of measured GFR)

No Race-Based Adjustments:
Unlike many adult GFR estimation equations, the CKiD U25 equations do not require 
race-based modifiers, addressing concerns about the clinical appropriateness and 
social implications of race-based medical calculations.

Three Equation Options:

1. Creatinine-Based CKiD U25 Equation:
   - Requires: Age, sex, height, serum creatinine
   - Formula: eGFR = k × (height_m / serum_creatinine_mg/dL)
   - k values are age- and sex-specific constants
   - Advantages: Uses routinely available laboratory test
   - Limitations: Affected by muscle mass, diet, and creatinine generation

2. Cystatin C-Based CKiD U25 Equation:
   - Requires: Age, sex, cystatin C
   - Formula: eGFR = k × (1 / cystatin_c_mg/L)
   - k values are age- and sex-specific constants
   - Advantages: Less affected by muscle mass than creatinine
   - Limitations: More expensive test, less widely available

3. Combined Creatinine-Cystatin C CKiD U25 Equation:
   - Requires: Age, sex, height, serum creatinine, cystatin C
   - Formula: eGFR = (creatinine_eGFR + cystatin_c_eGFR) / 2
   - Advantages: Most accurate approach, combining benefits of both biomarkers
   - Limitations: Requires both laboratory tests

Age-Dependent Constants:

The equations use sophisticated age- and sex-dependent k values that account for 
physiological changes in kidney function and biomarker metabolism:

For Males - Creatinine:
- Ages 1-<12 years: k = 39.0 × 1.008^(age-12)
- Ages 12-<18 years: k = 39.0 × 1.045^(age-12)
- Ages 18-25 years: k = 50.8

For Females - Creatinine:
- Ages 1-<12 years: k = 36.1 × 1.008^(age-12)
- Ages 12-<18 years: k = 36.1 × 1.023^(age-12)
- Ages 18-25 years: k = 41.4

Similar age-dependent patterns exist for cystatin C-based calculations with different 
k values optimized for cystatin C metabolism.

Clinical Applications:

Pediatric Nephrology:
- Monitoring CKD progression in children and adolescents
- Timing of interventions and therapies
- Drug dosing adjustments based on kidney function
- Research applications with standardized GFR estimation

Transition Medicine:
- Seamless monitoring from pediatric to adult care
- Avoiding artificial changes in GFR estimates at age 18
- Supporting coordinated care between pediatric and adult nephrology teams
- Maintaining consistency in clinical decision-making

Young Adult Care:
- More appropriate GFR estimation for young adults with CKD
- Better accuracy than adult equations in the 18-25 year age group
- Supporting early detection and management of CKD in young adults

Clinical Decision Support:

CKD Staging:
The calculator provides standard CKD staging based on eGFR:
- G1 (≥90): Normal or high kidney function
- G2 (60-89): Mildly decreased kidney function
- G3a (45-59): Mild to moderately decreased kidney function
- G3b (30-44): Moderately to severely decreased kidney function
- G4 (15-29): Severely decreased kidney function
- G5 (<15): Kidney failure

Treatment Planning:
- Monitoring kidney function decline over time
- Timing preparation for renal replacement therapy
- Coordinating multidisciplinary care interventions
- Supporting family counseling and education

Quality Improvement:
- Standardizing GFR estimation across pediatric and young adult populations
- Enabling accurate outcome research and quality metrics
- Supporting clinical protocol development and refinement

Implementation Considerations:

Laboratory Requirements:
- Serum creatinine: Standardized IDMS-traceable methods required
- Cystatin C: Certified reference material standardization needed
- Height measurement: Accurate standing height preferred

Clinical Context:
- Results should be interpreted in conjunction with clinical assessment
- Consider proteinuria, hematuria, and structural abnormalities
- Account for acute illness effects on biomarker levels
- Regular monitoring recommended for CKD management

Limitations:
- Validated specifically in CKD populations
- May not apply to acute kidney injury settings
- Limited validation in certain ethnic populations
- Cystatin C availability and cost considerations

The CKiD U25 eGFR Calculator represents a significant advancement in pediatric and 
young adult kidney function assessment, addressing critical gaps in clinical care 
and providing evidence-based tools for optimal patient management across the 
challenging transition from pediatric to adult healthcare.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Dict, Any, Optional


class CkidU25EgfrRequest(BaseModel):
    """
    Request model for CKiD U25 eGFR Calculator
    
    The CKiD U25 eGFR Calculator estimates glomerular filtration rate using age- and 
    sex-dependent clinical equations specifically developed for children and young adults 
    aged 1 to 25 years with chronic kidney disease. This calculator offers three 
    equation options to accommodate different clinical scenarios and laboratory availability.
    
    Equation Selection Guide:
    
    Creatinine-Based Equation:
    - Most commonly used option utilizing routinely available serum creatinine
    - Requires patient height for accurate calculation
    - Formula: eGFR = k × (height_m / serum_creatinine_mg/dL)
    - Best for: Routine monitoring when creatinine is readily available
    - Considerations: May be affected by muscle mass and dietary protein intake
    
    Cystatin C-Based Equation:
    - Alternative biomarker less affected by muscle mass than creatinine
    - Does not require height measurement
    - Formula: eGFR = k × (1 / cystatin_c_mg/L)
    - Best for: Patients with altered muscle mass or when creatinine may be unreliable
    - Considerations: More expensive test, less widely available than creatinine
    
    Combined Creatinine-Cystatin C Equation:
    - Most accurate approach using both biomarkers
    - Averages results from both creatinine and cystatin C equations
    - Formula: eGFR = (creatinine_eGFR + cystatin_c_eGFR) / 2
    - Best for: Maximum accuracy when both biomarkers are available
    - Considerations: Requires both laboratory tests and height measurement
    
    Patient Demographics:
    
    Age Considerations (1-25 years):
    The calculator uses sophisticated age-dependent constants that account for 
    physiological changes in kidney function and biomarker metabolism across 
    different developmental stages:
    
    Pediatric Range (1-17 years):
    - Accounts for rapid growth and changing body composition
    - Uses age-adjusted k values that reflect developmental physiology
    - Provides continuity with adult equations at transition to age 18
    
    Young Adult Range (18-25 years):
    - Bridges the gap between pediatric and adult care
    - More accurate than adult CKD-EPI equations in this age group
    - Eliminates "jumps" in eGFR that occur with equation transitions
    
    Sex Considerations:
    - Male and female patients have different k values reflecting physiological differences
    - Accounts for sex-based differences in creatinine and cystatin C metabolism
    - No race-based adjustments required, addressing equity concerns
    
    Laboratory Parameters:
    
    Height (Required for Creatinine Equations):
    - Should be measured as standing height when possible
    - Used to normalize creatinine values to body size
    - Critical for accurate eGFR calculation in growing children
    - Range: 50-250 cm to accommodate wide age range
    
    Serum Creatinine (Required for Creatinine Equations):
    - Must be measured using IDMS-traceable standardized methods
    - Should be obtained in steady-state conditions when possible
    - Range: 0.1-20.0 mg/dL to accommodate normal and severely impaired function
    - Consider effects of recent illness, medications, or dietary changes
    
    Cystatin C (Required for Cystatin C Equations):
    - Should be measured using certified reference material standardized methods
    - Less affected by muscle mass, age, and sex than creatinine
    - Range: 0.1-10.0 mg/L to accommodate normal and severely impaired function
    - More expensive than creatinine but provides additional clinical value
    
    Clinical Applications:
    
    Chronic Kidney Disease Monitoring:
    - Track kidney function progression over time
    - Guide timing of interventions and treatments
    - Support medication dosing adjustments
    - Enable family counseling and education
    
    Transition Care:
    - Seamless monitoring from pediatric to adult nephrology care
    - Maintain consistency in clinical decision-making
    - Avoid artificial changes in eGFR estimates at age 18
    - Support coordinated care between healthcare teams
    
    Research and Quality Improvement:
    - Standardize GFR estimation for clinical research
    - Enable accurate outcome measurements and quality metrics
    - Support development of evidence-based care protocols
    - Facilitate multi-center studies and comparisons
    
    References (Vancouver style):
    1. Pierce CB, Muñoz A, Ng DK, Warady BA, Furth SL, Schwartz GJ. Age- and sex-dependent 
    clinical equations to estimate glomerular filtration rates in children and young adults 
    with chronic kidney disease. Kidney Int. 2021 Oct;100(4):948-959.
    2. Schwartz GJ, Muñoz A, Schneider MF, Mak RH, Kaskel F, Warady BA, et al. New equations 
    to estimate GFR in children with CKD. J Am Soc Nephrol. 2009 Mar;20(3):629-37.
    """
    
    equation_type: Literal["creatinine", "cystatin_c", "creatinine_cystatin_c"] = Field(
        ...,
        description="Type of equation to use. 'creatinine' uses serum creatinine and height, 'cystatin_c' uses cystatin C only, 'creatinine_cystatin_c' uses both for maximum accuracy",
        example="creatinine"
    )
    
    age: int = Field(
        ...,
        ge=1,
        le=25,
        description="Patient age in years. CKiD U25 equations are specifically validated for ages 1-25 years",
        example=12
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Used to determine appropriate age- and sex-dependent k values for calculation",
        example="female"
    )
    
    height: Optional[float] = Field(
        None,
        ge=50.0,
        le=250.0,
        description="Patient height in centimeters. Required for creatinine-based equations. Should be standing height when possible",
        example=150.0
    )
    
    serum_creatinine: Optional[float] = Field(
        None,
        ge=0.1,
        le=20.0,
        description="Serum creatinine level in mg/dL. Required for creatinine-based equations. Should be measured using IDMS-traceable methods",
        example=1.2
    )
    
    cystatin_c: Optional[float] = Field(
        None,
        ge=0.1,
        le=10.0,
        description="Cystatin C level in mg/L. Required for cystatin C-based equations. Should be measured using certified reference material standards",
        example=1.5
    )
    
    @validator('height')
    def validate_height_for_creatinine(cls, v, values):
        """Validate height is provided for creatinine-based equations"""
        equation_type = values.get('equation_type')
        if equation_type in ['creatinine', 'creatinine_cystatin_c'] and v is None:
            raise ValueError('Height is required for creatinine-based equations')
        return v
    
    @validator('serum_creatinine')
    def validate_creatinine_for_creatinine_equations(cls, v, values):
        """Validate serum creatinine is provided for creatinine-based equations"""
        equation_type = values.get('equation_type')
        if equation_type in ['creatinine', 'creatinine_cystatin_c'] and v is None:
            raise ValueError('Serum creatinine is required for creatinine-based equations')
        return v
    
    @validator('cystatin_c')
    def validate_cystatin_for_cystatin_equations(cls, v, values):
        """Validate cystatin C is provided for cystatin C-based equations"""
        equation_type = values.get('equation_type')
        if equation_type in ['cystatin_c', 'creatinine_cystatin_c'] and v is None:
            raise ValueError('Cystatin C is required for cystatin C-based equations')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "equation_type": "creatinine",
                "age": 12,
                "sex": "female",
                "height": 150.0,
                "serum_creatinine": 1.2,
                "cystatin_c": None
            }
        }


class CkidU25EgfrResponse(BaseModel):
    """
    Response model for CKiD U25 eGFR Calculator
    
    The CKiD U25 eGFR Calculator response provides comprehensive kidney function assessment 
    with clinical interpretation and management guidance. The calculator returns estimated 
    glomerular filtration rate (eGFR) with appropriate CKD staging and detailed clinical 
    context to support evidence-based patient care.
    
    eGFR Interpretation and CKD Staging:
    
    The calculator provides standard Kidney Disease: Improving Global Outcomes (KDIGO) 
    CKD staging based on eGFR values:
    
    Stage G1 (eGFR ≥90 mL/min/1.73m²): Normal or High Kidney Function
    - Clinical significance: Normal kidney function level
    - Interpretation: If kidney damage is present (such as proteinuria, hematuria, or 
      structural abnormalities), this indicates CKD stage G1
    - Management: Regular monitoring for kidney damage markers, address cardiovascular 
      risk factors, maintain healthy lifestyle
    - Follow-up: Annual eGFR and urinalysis unless high-risk conditions present
    
    Stage G2 (eGFR 60-89 mL/min/1.73m²): Mildly Decreased Kidney Function
    - Clinical significance: Mild reduction in kidney function
    - Interpretation: Indicates CKD stage G2, particularly if kidney damage is present
    - Management: Monitor kidney function progression, address cardiovascular risk factors, 
      treat complications of CKD
    - Follow-up: Every 6-12 months with comprehensive metabolic panel and urinalysis
    
    Stage G3a (eGFR 45-59 mL/min/1.73m²): Mild to Moderately Decreased Kidney Function
    - Clinical significance: Moderate reduction in kidney function
    - Interpretation: CKD stage G3a with increased risk of complications
    - Management: Evaluate and treat CKD complications (anemia, bone disease, acidosis), 
      slow progression, cardiovascular risk reduction
    - Follow-up: Every 3-6 months with nephrology consultation recommended
    
    Stage G3b (eGFR 30-44 mL/min/1.73m²): Moderately to Severely Decreased Kidney Function
    - Clinical significance: Significant reduction in kidney function
    - Interpretation: CKD stage G3b with high risk of progression and complications
    - Management: Active management of CKD complications, prepare for renal replacement 
      therapy, nephrology co-management essential
    - Follow-up: Every 3 months with multidisciplinary CKD team involvement
    
    Stage G4 (eGFR 15-29 mL/min/1.73m²): Severely Decreased Kidney Function
    - Clinical significance: Severe reduction in kidney function approaching kidney failure
    - Interpretation: CKD stage G4 requiring preparation for renal replacement therapy
    - Management: Comprehensive CKD management, renal replacement therapy education and 
      preparation, vascular access planning for dialysis
    - Follow-up: Monthly monitoring with nephrology and transplant team involvement
    
    Stage G5 (eGFR <15 mL/min/1.73m²): Kidney Failure
    - Clinical significance: Kidney failure requiring renal replacement therapy
    - Interpretation: CKD stage G5, dialysis or transplantation indicated
    - Management: Initiate renal replacement therapy, comprehensive supportive care, 
      transplant evaluation if appropriate
    - Follow-up: Intensive monitoring with dialysis or transplant team management
    
    Clinical Decision Support Features:
    
    Calculation Method Transparency:
    - Specifies which equation was used (creatinine, cystatin C, or combined)
    - Provides age- and sex-specific k values used in calculation
    - Shows laboratory values and patient demographics used
    - Explains equation advantages and limitations
    
    Transition Care Support:
    - For patients 18-25 years, provides guidance on comparison with adult equations
    - Highlights advantages of CKiD U25 equations for young adults with CKD
    - Supports smooth transition from pediatric to adult nephrology care
    - Eliminates artificial "jumps" in eGFR at age 18
    
    Quality Assurance Features:
    - P30 accuracy metrics provided for clinical context
    - Validation population characteristics described
    - Equation limitations and appropriate use cases outlined
    - Recommendations for clinical interpretation and follow-up
    
    Pediatric-Specific Considerations:
    
    Growth and Development:
    - Accounts for physiological changes in kidney function during growth
    - Considers age-appropriate normal values and interpretation
    - Supports family education and counseling appropriate for age
    - Addresses unique pediatric CKD management considerations
    
    Longitudinal Monitoring:
    - Enables consistent eGFR tracking from childhood through young adulthood
    - Supports detection of kidney function decline over time
    - Facilitates research and quality improvement initiatives
    - Provides standardized outcomes measurement
    
    Research and Quality Applications:
    
    Clinical Research Support:
    - Standardized GFR estimation for pediatric and young adult studies
    - Enables accurate outcome measurements and comparisons
    - Supports multi-center research collaboration
    - Facilitates longitudinal cohort studies
    
    Quality Improvement:
    - Consistent eGFR estimation across care settings
    - Supports development of evidence-based care protocols
    - Enables benchmarking and performance measurement
    - Facilitates population health management initiatives
    
    The CKiD U25 eGFR Calculator response provides comprehensive clinical decision support 
    for optimal kidney function assessment and management in children and young adults, 
    addressing critical gaps in pediatric nephrology care and supporting evidence-based 
    clinical practice.
    
    Reference: Pierce CB, et al. Kidney Int. 2021;100(4):948-959.
    """
    
    result: float = Field(
        ...,
        description="Estimated glomerular filtration rate calculated using CKiD U25 equations",
        example=65.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for eGFR",
        example="mL/min/1.73m²"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with CKD staging and management recommendations",
        example="eGFR 65.2 mL/min/1.73m²: Mildly decreased kidney function (CKD stage G2). Monitor kidney function progression and address cardiovascular risk factors."
    )
    
    stage: str = Field(
        ...,
        description="CKD stage classification based on eGFR (G1, G2, G3a, G3b, G4, G5)",
        example="G2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the CKD stage",
        example="Mildly decreased"
    )
    
    calculation_details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of calculation method, parameters, and clinical context",
        example={
            "method": "Creatinine-based CKiD U25",
            "patient_demographics": {
                "age": "12 years",
                "sex": "Female",
                "age_group": "Pediatric (1-17 years)"
            },
            "laboratory_values": {
                "height": "150.0 cm",
                "serum_creatinine": "1.2 mg/dL"
            },
            "equation_parameters": {
                "creatinine_k_value": 36.1
            },
            "equation_explanation": "eGFR = k × (height_m / serum_creatinine_mg/dL)",
            "clinical_context": {
                "equation_advantages": [
                    "Superior to other pediatric equations for ages 1-25 years",
                    "Eliminates 'jumps' in eGFR when transitioning from pediatric to adult care",
                    "Does not require race-based adjustments",
                    "Validated in diverse populations with chronic kidney disease"
                ],
                "clinical_applications": [
                    "Monitoring kidney function progression in children and young adults",
                    "Supporting clinical decision-making for CKD management",
                    "Facilitating smooth transition from pediatric to adult nephrology care",
                    "Guiding timing of renal replacement therapy preparation"
                ]
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 65.2,
                "unit": "mL/min/1.73m²",
                "interpretation": "eGFR 65.2 mL/min/1.73m²: Mildly decreased kidney function (CKD stage G2). Monitor kidney function progression and address cardiovascular risk factors.",
                "stage": "G2",
                "stage_description": "Mildly decreased",
                "calculation_details": {
                    "method": "Creatinine-based CKiD U25",
                    "patient_demographics": {
                        "age": "12 years",
                        "sex": "Female",
                        "age_group": "Pediatric (1-17 years)"
                    },
                    "laboratory_values": {
                        "height": "150.0 cm",
                        "serum_creatinine": "1.2 mg/dL"
                    },
                    "equation_parameters": {
                        "creatinine_k_value": 36.1
                    }
                }
            }
        }