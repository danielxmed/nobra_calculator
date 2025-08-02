"""
Kt/V for Dialysis Adequacy Models

Request and response models for Kt/V dialysis adequacy calculation.

References (Vancouver style):
1. Daugirdas JT. Second generation logarithmic estimates of single-pool variable 
   volume Kt/V: an analysis of error. J Am Soc Nephrol. 1993 Nov;4(5):1205-13.
2. National Kidney Foundation. KDOQI Clinical Practice Guidelines for Hemodialysis 
   Adequacy: 2015 update. Am J Kidney Dis. 2015 Nov;66(5):884-930.
3. Bargman JM, Thorpe KE, Churchill DN; CANUSA Peritoneal Dialysis Study Group. 
   Relative contribution of residual renal function and peritoneal clearance to 
   adequacy of dialysis: a reanalysis of the CANUSA study. J Am Soc Nephrol. 2001 
   Oct;12(10):2158-62.
4. Blake PG, Jain AK, Nolph KD. Peritoneal dialysis adequacy: clinical implications. 
   Semin Dial. 2002 Nov-Dec;15(6):411-4.
5. Locatelli F, Cavalli PL, Tucci B, et al. The effect of different schedules of 
   dialysis on the removal of urea and phosphate. Clin Nephrol. 1999 Feb;51(2):93-102.

The Kt/V for Dialysis Adequacy is a dimensionless parameter that quantifies the 
adequacy of dialysis treatment for patients with end-stage renal disease. It represents 
the fractional clearance of urea from the body during a dialysis session and is 
calculated using the Daugirdas second-generation equation.

Key Components:
- K: Dialyzer clearance of urea (mL/min)
- t: Treatment time (minutes)  
- V: Volume of distribution of urea (approximately total body water in mL)
- Kt/V: Dimensionless ratio representing the fraction of body water cleared of urea

The Daugirdas Second-Generation Formula:
Kt/V = -ln(R - 0.008 × t) + (4 - 3.5 × R) × UF/V

Where:
- R = Post-dialysis BUN / Pre-dialysis BUN (BUN reduction ratio)
- t = Session length in hours
- UF = Ultrafiltration volume in liters
- V = Volume of distribution (approximated by post-dialysis weight in kg)

Clinical Significance:
- Hemodialysis: KDOQI target Kt/V ≥1.3 (minimum 1.2) per session
- Peritoneal Dialysis: ISPD target Kt/V ≥1.7 per week
- Higher Kt/V values generally associated with improved patient survival
- Kt/V should be monitored monthly for hemodialysis patients
- Adequate dialysis reduces uremic toxicity and improves quality of life

The calculator also computes the Urea Reduction Ratio (URR), which is closely 
related to Kt/V and provides an alternative measure of dialysis adequacy. 
Target URR for hemodialysis is ≥65%.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class KtvDialysisAdequacyRequest(BaseModel):
    """
    Request model for Kt/V Dialysis Adequacy calculation
    
    The Kt/V calculation requires pre- and post-dialysis blood urea nitrogen (BUN) 
    measurements, along with treatment parameters to assess the adequacy of dialysis 
    using the validated Daugirdas second-generation equation:
    
    Clinical Parameters:
    - Pre-dialysis BUN: Baseline urea level before treatment
    - Post-dialysis BUN: Urea level after dialysis completion
    - Dialysis Time: Duration of treatment session
    - Ultrafiltration Volume: Fluid removed during treatment
    - Post-dialysis Weight: Patient weight after fluid removal
    - Dialysis Type: Hemodialysis vs. peritoneal dialysis
    
    Calculation Method:
    The Daugirdas equation accounts for:
    1. Urea removal during dialysis (-ln term)
    2. Urea generation during treatment (0.008 correction factor)
    3. Convective clearance from ultrafiltration (UF/V term)
    
    Clinical Context:
    - Essential for monitoring dialysis prescription adequacy
    - Required monthly assessment for hemodialysis patients
    - Helps optimize treatment parameters for better outcomes
    - Correlates with patient survival and morbidity
    
    Quality Assurance:
    - BUN samples must be drawn properly (pre-dialysis: before treatment; post-dialysis: immediately after)
    - Avoid recirculation and access issues that may affect BUN measurements
    - Consider equilibrated Kt/V (eKt/V) for patients with high Kt/V values
    - Account for residual renal function in peritoneal dialysis patients
    
    References (Vancouver style):
    1. Daugirdas JT. Second generation logarithmic estimates of single-pool variable 
       volume Kt/V: an analysis of error. J Am Soc Nephrol. 1993 Nov;4(5):1205-13.
    2. National Kidney Foundation. KDOQI Clinical Practice Guidelines for Hemodialysis 
       Adequacy: 2015 update. Am J Kidney Dis. 2015 Nov;66(5):884-930.
    """
    
    pre_dialysis_bun: float = Field(
        ...,
        description="Pre-dialysis blood urea nitrogen (BUN) level in mg/dL. Should be drawn "
                   "immediately before dialysis initiation, avoiding dilution from saline priming. "
                   "Typical range: 20-100 mg/dL for dialysis patients.",
        ge=5.0,
        le=200.0,
        example=60.0
    )
    
    post_dialysis_bun: float = Field(
        ...,
        description="Post-dialysis blood urea nitrogen (BUN) level in mg/dL. Should be drawn "
                   "immediately after dialysis completion or from the arterial line to avoid "
                   "recirculation. Must be lower than pre-dialysis BUN.",
        ge=2.0,
        le=150.0,
        example=18.0
    )
    
    dialysis_time_hours: float = Field(
        ...,
        description="Duration of dialysis treatment session in hours. Typical hemodialysis "
                   "sessions range from 3-5 hours, while peritoneal dialysis dwells may vary "
                   "from 4-10 hours per exchange.",
        ge=0.5,
        le=24.0,
        example=4.0
    )
    
    ultrafiltration_volume: float = Field(
        ...,
        description="Volume of fluid removed during dialysis (ultrafiltration) in liters. "
                   "Represents excess fluid removal and affects the convective component "
                   "of urea clearance. Typical range: 0-6 L per hemodialysis session.",
        ge=0.0,
        le=10.0,
        example=2.5
    )
    
    post_dialysis_weight: float = Field(
        ...,
        description="Patient's weight after dialysis completion in kilograms. Used as an "
                   "approximation of the volume of distribution (V) in the Kt/V equation. "
                   "Should represent the patient's 'dry weight' or target weight.",
        ge=20.0,
        le=300.0,
        example=70.0
    )
    
    dialysis_type: Literal["hemodialysis", "peritoneal_dialysis"] = Field(
        ...,
        description="Type of dialysis treatment being assessed. Hemodialysis and peritoneal "
                   "dialysis have different adequacy targets: HD target Kt/V ≥1.3 per session, "
                   "PD target Kt/V ≥1.7 per week.",
        example="hemodialysis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pre_dialysis_bun": 60.0,
                "post_dialysis_bun": 18.0,
                "dialysis_time_hours": 4.0,
                "ultrafiltration_volume": 2.5,
                "post_dialysis_weight": 70.0,
                "dialysis_type": "hemodialysis"
            }
        }


class KtvDialysisAdequacyResponse(BaseModel):
    """
    Response model for Kt/V Dialysis Adequacy calculation
    
    Provides comprehensive assessment of dialysis adequacy using the Daugirdas 
    second-generation equation, including Kt/V calculation, adequacy assessment, 
    and clinical recommendations for dialysis optimization.
    
    Key Metrics:
    - Kt/V Value: Primary adequacy parameter (dimensionless)
    - Urea Reduction Ratio (URR): Alternative adequacy measure (percentage)
    - BUN Ratio: Post-dialysis/Pre-dialysis BUN ratio
    - Adequacy Assessment: Meets guidelines (yes/no) with specific targets
    
    Clinical Interpretation:
    
    Hemodialysis Targets:
    - Minimum Kt/V: ≥1.2 per session
    - Target Kt/V: ≥1.3 per session (KDOQI guidelines)
    - Target URR: ≥65%
    
    Peritoneal Dialysis Targets:
    - Target Kt/V: ≥1.7 per week (ISPD/KDOQI guidelines)
    - Include residual renal function in total clearance
    
    Clinical Actions Based on Results:
    - Inadequate Kt/V: Increase dialysis time, frequency, or dialyzer efficiency
    - Borderline Kt/V: Optimize treatment parameters and reassess
    - Adequate Kt/V: Continue current prescription with regular monitoring
    
    Quality Considerations:
    - Monthly monitoring recommended for hemodialysis patients
    - Consider equilibrated Kt/V (eKt/V) for high single-pool Kt/V values
    - Assess patient symptoms and laboratory values in addition to Kt/V
    - Account for access function and treatment adherence
    
    Performance Characteristics:
    - Validated for Kt/V range 0.8-2.0
    - Strong correlation with patient outcomes
    - May overestimate clearance when Kt/V >1.3
    - Single-pool model assumes instant equilibration
    
    Reference: Daugirdas JT. J Am Soc Nephrol. 1993;4(5):1205-13.
    """
    
    result: Dict = Field(
        ...,
        description="Detailed Kt/V calculation including adequacy assessment and calculation components",
        example={
            "ktv_value": 1.42,
            "urea_reduction_ratio": 70.0,
            "bun_ratio": 0.30,
            "dialysis_type": "hemodialysis",
            "adequacy_assessment": {
                "stage": "Target Adequate (HD)",
                "description": "Meets target hemodialysis adequacy",
                "meets_guidelines": True
            },
            "calculation_components": {
                "pre_dialysis_bun": 60.0,
                "post_dialysis_bun": 18.0,
                "dialysis_time_hours": 4.0,
                "ultrafiltration_volume": 2.5,
                "post_dialysis_weight": 70.0,
                "first_term": 1.288,
                "second_term": 0.132
            },
            "thresholds": {
                "minimum": 1.2,
                "target": 1.3
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for Kt/V (dimensionless ratio)",
        example="dimensionless"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including adequacy assessment, "
                   "guidelines comparison, and specific recommendations for dialysis optimization",
        example="Kt/V = 1.420 for hemodialysis treatment. Urea Reduction Ratio (URR) = 70.0%. This Kt/V value meets clinical adequacy guidelines. Kt/V meets KDOQI target guidelines (≥1.3). Adequate dialysis clearance achieved. Monitor dialysis adequacy regularly (monthly for hemodialysis, every 4-6 months for peritoneal dialysis). Consider patient symptoms, laboratory values, and overall clinical status in addition to Kt/V. Note: Daugirdas equation may overestimate Kt/V when values exceed 1.3. Consider equilibrated Kt/V (eKt/V) for more accurate assessment."
    )
    
    stage: str = Field(
        ...,
        description="Overall adequacy assessment category",
        example="Target Adequate (HD)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the adequacy level",
        example="Meets target hemodialysis adequacy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "ktv_value": 1.42,
                    "urea_reduction_ratio": 70.0,
                    "bun_ratio": 0.30,
                    "dialysis_type": "hemodialysis",
                    "adequacy_assessment": {
                        "stage": "Target Adequate (HD)",
                        "description": "Meets target hemodialysis adequacy",
                        "meets_guidelines": True
                    },
                    "calculation_components": {
                        "pre_dialysis_bun": 60.0,
                        "post_dialysis_bun": 18.0,
                        "dialysis_time_hours": 4.0,
                        "ultrafiltration_volume": 2.5,
                        "post_dialysis_weight": 70.0,
                        "first_term": 1.288,
                        "second_term": 0.132
                    },
                    "thresholds": {
                        "minimum": 1.2,
                        "target": 1.3
                    }
                },
                "unit": "dimensionless",
                "interpretation": "Kt/V = 1.420 for hemodialysis treatment. Urea Reduction Ratio (URR) = 70.0%. This Kt/V value meets clinical adequacy guidelines. Kt/V meets KDOQI target guidelines (≥1.3). Adequate dialysis clearance achieved. Monitor dialysis adequacy regularly (monthly for hemodialysis, every 4-6 months for peritoneal dialysis). Consider patient symptoms, laboratory values, and overall clinical status in addition to Kt/V. Note: Daugirdas equation may overestimate Kt/V when values exceed 1.3. Consider equilibrated Kt/V (eKt/V) for more accurate assessment.",
                "stage": "Target Adequate (HD)",
                "stage_description": "Meets target hemodialysis adequacy"
            }
        }