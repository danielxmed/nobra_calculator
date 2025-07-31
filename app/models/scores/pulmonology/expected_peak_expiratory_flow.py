"""
Estimated/Expected Peak Expiratory Flow (Peak Flow) Models

Request and response models for estimating expected peak expiratory flow and assessing asthma severity.

References (Vancouver style):
1. Hankinson JL, Odencrantz JR, Fedan KB. Spirometric reference values from a sample of the 
   general U.S. population. Am J Respir Crit Care Med. 1999 Jan;159(1):179-87. 
   doi: 10.1164/ajrccm.159.1.9712108.
2. Nunn AJ, Gregg I. New regression equations for predicting peak expiratory flow in adults. 
   BMJ. 1989 Apr 22;298(6680):1068-70. doi: 10.1136/bmj.298.6680.1068.
3. Godfrey S, Kamburoff PL, Nairn JR. Spirometry, lung volumes and airway resistance in normal 
   children aged 5 to 18 years. Br J Dis Chest. 1970 Jan;64(1):15-24. 
   doi: 10.1016/s0007-0971(70)80045-0.
4. Global Initiative for Asthma. Global Strategy for Asthma Management and Prevention, 2023. 
   Available from: www.ginasthma.org

The Peak Expiratory Flow (PEF) calculator estimates expected peak flow based on age, height, 
sex, and race/ethnicity using validated regression equations. It provides zone-based assessment 
for asthma management when a measured PEF is provided for comparison.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class ExpectedPeakExpiratoryFlowRequest(BaseModel):
    """
    Request model for Estimated/Expected Peak Expiratory Flow (Peak Flow) Calculator
    
    This calculator estimates expected peak expiratory flow rate using age-appropriate and 
    ethnicity-specific regression equations:
    
    Age-Based Formulas:
    
    1. Ages 5-7 years (all ethnicities):
       PEFR = [(Height, cm - 100) × 5] + 100
       
    2. Ages 8-17 years (non-Caucasian/African American/Mexican American):
       PEFR = [(Height, cm - 100) × 5] + 100
       
    3. Ages 18-80 years (non-Caucasian/African American/Mexican American):
       - Male: PEFR = {[(Height, m × 5.48) + 1.58] - [Age × 0.041]} × 60
       - Female: PEFR = {[(Height, m × 3.72) + 2.24] - [Age × 0.03]} × 60
       
    4. Ages 8-80 years (Caucasian/African American/Mexican American):
       Uses Hankinson 1999 NHANES III regression equations with ethnicity-specific coefficients
    
    Zone Assessment (when measured PEF provided):
    - Green Zone: ≥80% of expected (good asthma control)
    - Yellow Zone: 50-79% of expected (caution, may need treatment adjustment)
    - Red Zone: <50% of expected (emergency, seek immediate medical attention)
    
    Clinical Applications:
    - Asthma management and monitoring
    - Assessment of treatment effectiveness
    - Early detection of exacerbations
    - Patient self-management with action plans
    - Baseline establishment for new patients
    
    Key Considerations:
    - Height and sex are most strongly correlated with peak flow
    - Not a standalone diagnostic tool - must be combined with clinical assessment
    - Environmental factors and measurement technique can affect results
    - Regular monitoring provides better insights than isolated measurements
    - Most accurate when compared to patient's personal best value
    
    References (Vancouver style):
    1. Hankinson JL, Odencrantz JR, Fedan KB. Spirometric reference values from a sample of the 
       general U.S. population. Am J Respir Crit Care Med. 1999 Jan;159(1):179-87. 
       doi: 10.1164/ajrccm.159.1.9712108.
    2. Global Initiative for Asthma. Global Strategy for Asthma Management and Prevention, 2023. 
       Available from: www.ginasthma.org
    """
    
    age_years: int = Field(
        ...,
        description="Patient age in years. Used to select appropriate regression equation and age-specific coefficients",
        ge=5,
        le=80,
        example=35
    )
    
    height_cm: float = Field(
        ...,
        description="Patient height in centimeters. Height is the strongest predictor of expected peak flow",
        ge=100,
        le=220,
        example=170.0
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Male and female have different regression coefficients in most equations",
        example="male"
    )
    
    race_ethnicity: Literal["caucasian", "african_american", "mexican_american", "other"] = Field(
        ...,
        description="Patient race/ethnicity for appropriate formula selection. Caucasian, African American, and Mexican American use Hankinson NHANES III equations with ethnicity-specific coefficients. 'Other' uses simplified equations",
        example="caucasian"
    )
    
    measured_pef: Optional[float] = Field(
        None,
        description="Measured peak expiratory flow in L/min (optional). When provided, enables zone-based assessment and percentage calculation for asthma management",
        ge=50,
        le=800,
        example=450.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_years": 35,
                "height_cm": 170.0,
                "sex": "male",
                "race_ethnicity": "caucasian",
                "measured_pef": 450.0
            }
        }


class ExpectedPeakExpiratoryFlowResponse(BaseModel):
    """
    Response model for Estimated/Expected Peak Expiratory Flow (Peak Flow) Calculator
    
    Provides expected peak expiratory flow estimation and zone-based assessment for asthma management:
    
    Expected PEF Calculation:
    - Based on validated regression equations specific to age, sex, height, and ethnicity
    - Represents the normal/predicted peak flow for the patient's demographic characteristics
    - Used as reference for comparison with measured values
    
    Zone-Based Assessment (Traffic Light System):
    
    Green Zone (≥80% of expected):
    - Indicates good asthma control
    - Peak flow within normal range
    - Continue current treatment plan
    - Maintain regular monitoring
    
    Yellow Zone (50-79% of expected):
    - Caution indicated - reduced lung function
    - May indicate developing asthma exacerbation
    - Consider increasing treatment per asthma action plan
    - Monitor closely, contact healthcare provider if symptoms worsen
    
    Red Zone (<50% of expected):
    - EMERGENCY - dangerously low peak flow
    - Severe asthma exacerbation requiring immediate medical attention
    - Use rescue medications immediately
    - Seek emergency care without delay
    
    Clinical Interpretation Guidelines:
    - Peak flow variability >20% may suggest asthma diagnosis
    - Regular monitoring helps assess treatment effectiveness
    - Most accurate when compared to patient's personal best value
    - Consider diurnal variation in measurements
    - Combine with clinical symptoms for complete assessment
    
    Important Limitations:
    - Equations are population-based estimates; individual variation exists
    - Environmental factors and measurement technique affect results
    - Not suitable as sole diagnostic criterion
    - Always combine with clinical assessment and patient history
    - Personal best values are preferred over predicted values when available
    
    Reference: Hankinson JL, et al. Am J Respir Crit Care Med. 1999;159(1):179-87.
    """
    
    result: str = Field(
        ...,
        description="Calculation result status (expected_pef_calculated)",
        example="expected_pef_calculated"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for peak expiratory flow (L/min)",
        example="L/min"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including expected PEF, zone assessment (if measured PEF provided), and management recommendations",
        example="Expected peak expiratory flow: 520.5 L/min based on age, height, sex, and ethnicity. Measured peak flow: 450.0 L/min (86.5% of expected). GREEN ZONE - Good asthma control. Peak flow is within normal range (≥80% of expected). Continue current treatment plan and regular monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Clinical assessment stage based on zone or expected value status",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical stage",
        example="Good control"
    )
    
    expected_pef: float = Field(
        ...,
        description="Expected/predicted peak expiratory flow in L/min based on patient demographics",
        example=520.5
    )
    
    measured_pef: Optional[float] = Field(
        None,
        description="Measured peak expiratory flow in L/min (provided by user, if any)",
        example=450.0
    )
    
    percentage_of_expected: Optional[float] = Field(
        None,
        description="Percentage of expected peak flow (calculated when measured PEF provided)",
        example=86.5
    )
    
    zone: str = Field(
        ...,
        description="Zone classification based on percentage of expected (Green Zone, Yellow Zone, Red Zone, or Not assessed)",
        example="Green Zone"
    )
    
    zone_color: str = Field(
        ...,
        description="Color code for zone classification (green, yellow, red, or gray)",
        example="green"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "expected_pef_calculated",
                "unit": "L/min",
                "interpretation": "Expected peak expiratory flow: 520.5 L/min based on age, height, sex, and ethnicity. Measured peak flow: 450.0 L/min (86.5% of expected). GREEN ZONE - Good asthma control. Peak flow is within normal range (≥80% of expected). Continue current treatment plan and regular monitoring.",
                "stage": "Normal",
                "stage_description": "Good control",
                "expected_pef": 520.5,
                "measured_pef": 450.0,
                "percentage_of_expected": 86.5,
                "zone": "Green Zone",
                "zone_color": "green"
            }
        }