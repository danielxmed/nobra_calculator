"""
Hestia Criteria for Outpatient Pulmonary Embolism Treatment Models

Request and response models for Hestia Criteria calculation.

References (Vancouver style):
1. Zondag W, Mos IC, Creemers-Schild D, Mulder JW, Herb-van Toumhout SJ, Hovens MM, 
   et al.; Hestia Study Investigators. Outpatient treatment in patients with acute 
   pulmonary embolism: the Hestia Study. J Thromb Haemost. 2011 Aug;9(8):1500-7. 
   doi: 10.1111/j.1538-7836.2011.04388.x.
2. Zondag W, den Exter PL, Crobach MJ, Dolsma A, Donker ML, Eijsvogel M, et al.; 
   Hestia Study Investigators. Comparison of two methods for selection of out of 
   hospital treatment in patients with acute pulmonary embolism. Thromb Haemost. 
   2013 Jan;109(1):47-52. doi: 10.1160/TH12-07-0466.
3. Barco S, Schmidtmann I, Ageno W, Bauersachs RM, Becattini C, Bernardi E, et al.; 
   HoT-PE Investigators. Early discharge and home treatment of patients with low-risk 
   pulmonary embolism with the oral factor Xa inhibitor rivaroxaban: an international 
   multicentre single-arm clinical trial. Eur Heart J. 2020 Jan 21;41(4):509-518. 
   doi: 10.1093/eurheartj/ehz367.

The Hestia Criteria is a clinical decision tool that identifies hemodynamically stable 
patients with acute pulmonary embolism who can be safely treated as outpatients. 
Unlike scoring systems, it uses exclusion criteria - any single criterion excludes 
the patient from outpatient management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HestiaCriteriaRequest(BaseModel):
    """
    Request model for Hestia Criteria for Outpatient Pulmonary Embolism Treatment
    
    The Hestia Criteria uses 11 exclusion criteria to identify PE patients suitable 
    for outpatient treatment. All criteria must be absent (answered "no") for a 
    patient to be considered low risk and eligible for outpatient management.
    
    The criteria assess:
    - Hemodynamic stability
    - Need for advanced interventions
    - Bleeding risk
    - Oxygen requirements
    - Treatment failure
    - Pain control needs
    - Social support and comorbidities
    - Organ function
    - Special populations
    
    This tool has been validated in multiple studies showing that patients meeting 
    all criteria (0 points) have excellent outcomes with outpatient treatment, 
    including 0% mortality and 2% VTE recurrence rates.
    
    References (Vancouver style):
    1. Zondag W, Mos IC, Creemers-Schild D, Mulder JW, Herb-van Toumhout SJ, Hovens MM, 
       et al. Outpatient treatment in patients with acute pulmonary embolism: the Hestia 
       Study. J Thromb Haemost. 2011 Aug;9(8):1500-7.
    2. Zondag W, den Exter PL, Crobach MJ, Dolsma A, Donker ML, Eijsvogel M, et al. 
       Comparison of two methods for selection of out of hospital treatment in patients 
       with acute pulmonary embolism. Thromb Haemost. 2013 Jan;109(1):47-52.
    """
    
    hemodynamically_unstable: Literal["yes", "no"] = Field(
        ...,
        description="Hemodynamically unstable, defined as systolic BP <100 mmHg with heart rate >100 bpm, "
                    "or condition requiring ICU admission. This identifies patients who need intensive "
                    "monitoring and aggressive treatment. Scores 1 point if yes.",
        example="no"
    )
    
    thrombolysis_embolectomy: Literal["yes", "no"] = Field(
        ...,
        description="Thrombolysis or embolectomy needed. Indicates massive or submassive PE requiring "
                    "advanced intervention beyond standard anticoagulation. Scores 1 point if yes.",
        example="no"
    )
    
    active_bleeding: Literal["yes", "no"] = Field(
        ...,
        description="Active bleeding or high risk for bleeding, including recent major surgery, "
                    "gastrointestinal bleeding, intracranial hemorrhage, or other conditions that "
                    "significantly increase bleeding risk with anticoagulation. Scores 1 point if yes.",
        example="no"
    )
    
    oxygen_24hr: Literal["yes", "no"] = Field(
        ...,
        description="More than 24 hours on supplemental oxygen required to maintain oxygen saturation >90%. "
                    "Indicates significant respiratory compromise requiring inpatient monitoring. "
                    "Scores 1 point if yes.",
        example="no"
    )
    
    pe_on_anticoagulation: Literal["yes", "no"] = Field(
        ...,
        description="PE diagnosed while on therapeutic anticoagulation. Suggests treatment failure and "
                    "need for escalation of therapy or investigation of underlying causes. "
                    "Scores 1 point if yes.",
        example="no"
    )
    
    severe_pain_iv_meds: Literal["yes", "no"] = Field(
        ...,
        description="Severe pain needing IV pain medication for more than 24 hours. Indicates need "
                    "for inpatient pain management that cannot be achieved with oral medications. "
                    "Scores 1 point if yes.",
        example="no"
    )
    
    medical_social_reason: Literal["yes", "no"] = Field(
        ...,
        description="Medical or social reason for admission >24 hours, such as infection, malignancy, "
                    "no support system at home, inability to comply with treatment, or other conditions "
                    "requiring inpatient care. Scores 1 point if yes.",
        example="no"
    )
    
    creatinine_clearance_low: Literal["yes", "no"] = Field(
        ...,
        description="Creatinine clearance <30 mL/min by Cockcroft-Gault formula. Severe renal impairment "
                    "affects anticoagulant dosing and increases bleeding risk. Scores 1 point if yes.",
        example="no"
    )
    
    severe_liver_impairment: Literal["yes", "no"] = Field(
        ...,
        description="Severe liver impairment. Affects coagulation factors and anticoagulant metabolism, "
                    "increasing bleeding risk and complicating management. Scores 1 point if yes.",
        example="no"
    )
    
    pregnant: Literal["yes", "no"] = Field(
        ...,
        description="Pregnant patient. Requires specialized anticoagulation management and monitoring "
                    "for both maternal and fetal well-being. Scores 1 point if yes.",
        example="no"
    )
    
    history_of_hit: Literal["yes", "no"] = Field(
        ...,
        description="Documented history of heparin-induced thrombocytopenia (HIT). Contraindicates "
                    "standard heparin-based anticoagulation and requires alternative agents. "
                    "Scores 1 point if yes.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hemodynamically_unstable": "no",
                "thrombolysis_embolectomy": "no",
                "active_bleeding": "no",
                "oxygen_24hr": "no",
                "pe_on_anticoagulation": "no",
                "severe_pain_iv_meds": "no",
                "medical_social_reason": "no",
                "creatinine_clearance_low": "no",
                "severe_liver_impairment": "no",
                "pregnant": "no",
                "history_of_hit": "no"
            }
        }


class HestiaCriteriaResponse(BaseModel):
    """
    Response model for Hestia Criteria for Outpatient Pulmonary Embolism Treatment
    
    The Hestia Criteria score equals the number of criteria present (0-11).
    - 0 criteria met: Low risk - suitable for outpatient treatment
    - ≥1 criteria met: Not low risk - requires inpatient management
    
    Clinical Application:
    - Patients with 0 criteria can be discharged on anticoagulation with close follow-up
    - This approach has been associated with:
      - 0% mortality rate
      - 2% VTE recurrence rate
      - Reduced healthcare costs
      - High patient satisfaction
    
    Reference: Zondag W, et al. J Thromb Haemost. 2011;9(8):1500-7.
    """
    
    result: int = Field(
        ...,
        description="Number of Hestia criteria met (range: 0-11). A score of 0 indicates low risk.",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="criteria met"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk assessment and management recommendation",
        example="Patient meets criteria for outpatient management. Associated with 0% mortality and 2% VTE recurrence rate. Consider for home treatment with appropriate anticoagulation and close follow-up."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or Not Low Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of suitability for outpatient treatment",
        example="Suitable for outpatient treatment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "criteria met",
                "interpretation": "Patient meets criteria for outpatient management. Associated with 0% mortality and 2% VTE recurrence rate. Consider for home treatment with appropriate anticoagulation and close follow-up.",
                "stage": "Low Risk",
                "stage_description": "Suitable for outpatient treatment"
            }
        }