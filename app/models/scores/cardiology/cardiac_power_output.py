"""
Cardiac Power Output (CPO) Models

Request and response models for Cardiac Power Output calculation.

References (Vancouver style):
1. Tan LB. Cardiac pumping capability and prognosis in heart failure. Lancet. 1986 Dec 13;2(8520):1360-3. doi: 10.1016/s0140-6736(86)92002-6.
2. Fincke R, Hochman JS, Lowe AM, Menon V, Slater JN, Zeitlin J, et al. Cardiac power is the strongest hemodynamic correlate of mortality in cardiogenic shock: a report from the SHOCK trial registry. J Am Coll Cardiol. 2004 Jul 21;44(2):340-8. doi: 10.1016/j.jacc.2004.03.060.
3. Mendoza DD, Cooper HA, Panza JA. Cardiac power output predicts mortality across a broad spectrum of patients with acute cardiac disease. Am Heart J. 2007 Mar;153(3):366-70. doi: 10.1016/j.ahj.2006.11.014.
4. Williams SG, Cooke GA, Wright DJ, Parsons RJ, Riley RL, Marshall P, et al. Peak exercise cardiac power output; a direct indicator of cardiac function strongly predictive of prognosis in chronic heart failure. Eur Heart J. 2001 Aug;22(16):1496-503. doi: 10.1053/euhj.2000.2547.

Cardiac Power Output (CPO) calculates the rate of energy output of the heart, integrating both pressure (mean arterial pressure) and flow (cardiac output) components of cardiac work. It is recognized as the strongest hemodynamic predictor of mortality in cardiogenic shock.

The CPO can be calculated using two formulas:
1. Standard formula (commonly used): CPO = (MAP × CO) / 451
2. Original Tan formula (includes RAP): CPO = [(MAP - RAP) × CO] / 451

Where MAP = mean arterial pressure (mmHg), CO = cardiac output (L/min), RAP = right atrial pressure (mmHg), and 451 is the conversion constant.

Clinical significance:
- Normal resting CPO: ~1.0 Watt
- CPO <0.6W: Severe ventricular dysfunction with poor prognosis
- CPO 0.6-1.0W: Moderately reduced cardiac function
- CPO ≥1.0W: Adequate cardiac function
- Exercise CPO: Can reach up to 6 Watts

The inclusion of right atrial pressure (RAP) in the original formula provides better prognostic performance, especially in patients with elevated filling pressures or cardiogenic shock, as it accounts for the true pressure gradient across which the heart pumps.
"""

from pydantic import BaseModel, Field
from typing import Optional


class CardiacPowerOutputRequest(BaseModel):
    """
    Request model for Cardiac Power Output (CPO) calculation
    
    CPO calculates the rate of energy output of the heart by integrating pressure and flow components.
    It serves as the strongest hemodynamic predictor of mortality in cardiogenic shock.
    
    Parameters:
    - mean_arterial_pressure: Mean arterial pressure in mmHg (required)
    - cardiac_output: Cardiac output in L/min (required)  
    - right_atrial_pressure: Right atrial pressure in mmHg (optional, for original Tan formula)
    
    Formulas:
    - Standard: CPO = (MAP × CO) / 451
    - Original Tan: CPO = [(MAP - RAP) × CO] / 451
    
    Clinical thresholds:
    - Normal resting CPO: ~1.0 Watt
    - CPO <0.6W: Severe dysfunction, poor prognosis
    - CPO 0.6-1.0W: Moderately reduced function
    - CPO ≥1.0W: Adequate function
    
    References (Vancouver style):
    1. Tan LB. Cardiac pumping capability and prognosis in heart failure. Lancet. 1986 Dec 13;2(8520):1360-3. doi: 10.1016/s0140-6736(86)92002-6.
    2. Fincke R, Hochman JS, Lowe AM, Menon V, Slater JN, Zeitlin J, et al. Cardiac power is the strongest hemodynamic correlate of mortality in cardiogenic shock: a report from the SHOCK trial registry. J Am Coll Cardiol. 2004 Jul 21;44(2):340-8. doi: 10.1016/j.jacc.2004.03.060.
    3. Mendoza DD, Cooper HA, Panza JA. Cardiac power output predicts mortality across a broad spectrum of patients with acute cardiac disease. Am Heart J. 2007 Mar;153(3):366-70. doi: 10.1016/j.ahj.2006.11.014.
    """
    
    mean_arterial_pressure: float = Field(
        ...,
        description="Mean arterial pressure in mmHg. Can be calculated as (SBP + 2×DBP)/3 or directly measured via arterial catheter",
        ge=30.0,
        le=200.0,
        example=85.0
    )
    
    cardiac_output: float = Field(
        ...,
        description="Cardiac output in L/min. Can be measured via thermodilution, Fick method, or other techniques",
        ge=1.0,
        le=15.0,
        example=5.0
    )
    
    right_atrial_pressure: Optional[float] = Field(
        None,
        description="Right atrial pressure in mmHg (optional). When provided, uses original Tan formula which may provide better prognostic performance. Measured via central venous catheter",
        ge=0.0,
        le=30.0,
        example=8.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "mean_arterial_pressure": 85.0,
                "cardiac_output": 5.0,
                "right_atrial_pressure": 8.0
            }
        }


class CardiacPowerOutputResponse(BaseModel):
    """
    Response model for Cardiac Power Output (CPO) calculation
    
    Returns CPO measurements using both standard and original formulas (when RAP is provided).
    The primary CPO value is used for clinical interpretation.
    
    Results include:
    - cpo_standard: CPO calculated without RAP (standard formula)
    - cpo_original: CPO calculated with RAP (original Tan formula, if RAP provided)
    - primary_cpo: The CPO value used for interpretation
    - formula_used: Which formula was used for primary interpretation
    
    Clinical interpretation based on primary CPO:
    - <0.6W: Severe ventricular dysfunction, poor prognosis
    - 0.6-1.0W: Moderately reduced cardiac function
    - ≥1.0W: Adequate cardiac function
    
    Reference: Tan LB. Lancet. 1986;2(8520):1360-3.
    """
    
    result: dict = Field(
        ...,
        description="CPO calculation results including standard and original formulas",
        example={
            "cpo_standard": 0.942,
            "cpo_original": 0.856,
            "primary_cpo": 0.856,
            "formula_used": "Original Tan (with RAP)"
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for cardiac power output",
        example="Watts"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on CPO value",
        example="CPO 0.856W indicates moderately reduced cardiac function. Monitor closely and optimize medical therapy. Consider inotropic support and evaluate for underlying causes of reduced cardiac performance."
    )
    
    stage: str = Field(
        ...,
        description="Clinical stage based on CPO value (Severe dysfunction, Moderately reduced, Normal to high, Very high)",
        example="Moderately reduced"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical stage",
        example="Moderately reduced cardiac power"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "cpo_standard": 0.942,
                    "cpo_original": 0.856,
                    "primary_cpo": 0.856,
                    "formula_used": "Original Tan (with RAP)"
                },
                "unit": "Watts",
                "interpretation": "CPO 0.856W indicates moderately reduced cardiac function. Monitor closely and optimize medical therapy. Consider inotropic support and evaluate for underlying causes of reduced cardiac performance.",
                "stage": "Moderately reduced",
                "stage_description": "Moderately reduced cardiac power"
            }
        }