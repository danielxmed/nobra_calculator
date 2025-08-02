"""
Michigan Risk Score for PICC-Related Thrombosis Models

Request and response models for Michigan PICC thrombosis risk calculation.

References (Vancouver style):
1. Chopra V, Kaatz S, Conlon A, Paje D, Grant PJ, Rogers MAM, et al. The Michigan 
   Risk Score to predict peripherally inserted central catheter-associated thrombosis. 
   J Thromb Haemost. 2017 Oct;15(10):1951-1962. doi: 10.1111/jth.13794.
2. Chopra V, Anand S, Hickner A, Buist M, Rogers MA, Saint S, et al. Risk of venous 
   thromboembolism associated with peripherally inserted central catheters: a systematic 
   review and meta-analysis. Lancet. 2013 Jul 27;382(9889):311-25. 
   doi: 10.1016/S0140-6736(13)60592-9.
3. Evans RS, Sharp JH, Linford LH, Lloyd JF, Tripp JS, Jones JP, et al. Risk of 
   symptomatic DVT associated with peripherally inserted central catheters. Chest. 
   2010 Oct;138(4):803-10. doi: 10.1378/chest.10-0154.

The Michigan Risk Score was developed from data on 23,010 patients in the Michigan 
Hospital Medicine Safety Consortium, where 475 (2.1%) developed symptomatic PICC-DVT. 
This validated risk stratification tool helps clinicians assess thrombosis risk 
before PICC insertion and consider alternative vascular access for high-risk patients.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class MichiganPiccRiskRequest(BaseModel):
    """
    Request model for Michigan Risk Score for PICC-Related Thrombosis
    
    The Michigan Risk Score uses five clinical factors to predict PICC-associated DVT:
    
    1. Another CVC present: Indicates higher baseline thrombosis risk (+1 point)
    2. WBC > 12 × 10⁹/µL: Marker of inflammation/infection increasing risk (+1 point)
    3. Multi-lumen PICC: More lumens = larger catheter diameter = higher risk (+1-2 points)
    4. History of VTE: Prior thrombosis strongly predicts recurrence (+2-3 points)
    5. Active cancer: Hypercoagulable state significantly increases risk (+3 points)
    
    Clinical Context:
    PICCs are associated with a 2-4% risk of upper extremity DVT. The Michigan Risk 
    Score stratifies patients into four risk classes with thrombosis rates ranging 
    from 0.9% (Class I) to 4.7% (Class IV), representing a 5.2-fold risk increase.
    
    Important Limitations:
    - Validated only in medical patients ≥18 years old
    - Not validated for surgical, pediatric, or pregnant patients
    - Some external validation studies have shown mixed results
    
    References (Vancouver style):
    1. Chopra V, Kaatz S, Conlon A, Paje D, Grant PJ, Rogers MAM, et al. The Michigan 
       Risk Score to predict peripherally inserted central catheter-associated thrombosis. 
       J Thromb Haemost. 2017 Oct;15(10):1951-1962. doi: 10.1111/jth.13794.
    """
    
    another_cvc_present: Literal["no", "yes"] = Field(
        ...,
        description="Is another central venous catheter (CVC) present when PICC is placed? "
                    "Includes all types of CVCs (tunneled, non-tunneled, ports). Scores +1 point if yes",
        example="no"
    )
    
    wbc_over_12: Literal["no", "yes"] = Field(
        ...,
        description="Is white blood cell count > 12.0 × 10⁹/µL (or × 10³/µL)? "
                    "Use most recent value before PICC insertion. Scores +1 point if yes",
        example="no"
    )
    
    picc_lumens: Literal["1", "2", "3_or_4"] = Field(
        ...,
        description="Number of PICC lumens. Single lumen = 0 points, double lumen = +1 point, "
                    "triple or quadruple lumen = +2 points. More lumens mean larger catheter diameter",
        example="2"
    )
    
    history_of_vte: Literal["never", "yes_over_30_days", "yes_within_30_days"] = Field(
        ...,
        description="History of venous thromboembolism (VTE: DVT or PE)? Never = 0 points, "
                    ">30 days prior = +2 points, within 30 days = +3 points. Recent VTE highest risk",
        example="never"
    )
    
    active_cancer: Literal["no", "yes"] = Field(
        ...,
        description="Active cancer defined as: currently on chemotherapy OR admission for "
                    "cancer-related reason. Does not include cancer in remission. Scores +3 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "another_cvc_present": "no",
                "wbc_over_12": "yes",
                "picc_lumens": "2",
                "history_of_vte": "never",
                "active_cancer": "yes"
            }
        }


class MichiganPiccRiskResponse(BaseModel):
    """
    Response model for Michigan Risk Score for PICC-Related Thrombosis
    
    Risk Classes and Clinical Implications:
    - Class I (0 points): 0.9% risk - Low risk, standard care
    - Class II (1-2 points): 1.6% risk - Enhanced monitoring recommended
    - Class III (3-4 points): 2.7% risk - Consider alternative access
    - Class IV (≥5 points): 4.7% risk - Strongly consider alternatives
    
    Clinical Decision Support:
    For high-risk patients (Class III-IV), consider:
    - Midline catheters for shorter duration therapy
    - Tunneled catheters for long-term access
    - Peripheral IVs if feasible
    - Enhanced VTE prophylaxis if PICC necessary
    - More frequent monitoring for DVT symptoms
    
    Reference: Chopra V, et al. J Thromb Haemost. 2017;15(10):1951-1962.
    """
    
    result: int = Field(
        ...,
        description="Michigan Risk Score (range 0-10 points). Higher scores indicate greater VTE risk",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and management recommendations",
        example="High risk of PICC-related thrombosis. Strongly consider alternative vascular access options. If PICC necessary, implement aggressive VTE prophylaxis and frequent monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (Class I-IV)",
        example="Class IV"
    )
    
    stage_description: str = Field(
        ...,
        description="VTE probability for the risk class",
        example="4.7% VTE probability"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "High risk of PICC-related thrombosis. Strongly consider alternative vascular access options. If PICC necessary, implement aggressive VTE prophylaxis and frequent monitoring.",
                "stage": "Class IV",
                "stage_description": "4.7% VTE probability"
            }
        }