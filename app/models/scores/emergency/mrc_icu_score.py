"""
Medication Regimen Complexity-Intensive Care Unit (MRC-ICU) Score Models

Request and response models for MRC-ICU score calculation.

References (Vancouver style):
1. Gwynn ME, Poisson MO, Hatton KM, Donihi AC, Campbell MJ, Al-Mamun MA, et al. 
   Development and validation of a medication regimen complexity scoring tool for 
   critically ill patients. Am J Health Syst Pharm. 2019 May 17;76(Supplement_2):S34-S40. 
   doi: 10.1093/ajhp/zxy054.
2. Sikora A, Ayyala D, Rech MA, Donihi AC, Campbell M, Al-Mamun MA. Impact of 
   Pharmacists to Improve Patient Care in the Critically Ill: A Large Multicenter 
   Analysis Using Meaningful Metrics With the Medication Regimen Complexity-ICU 
   (MRC-ICU) Score. Crit Care Med. 2022 Sep 1;50(9):1318-1328. 
   doi: 10.1097/CCM.0000000000005585.
3. Olney K, Rech M, Campbell M, Prunty J, Mancuso S, Al-Mamun MA, et al. Development 
   of Machine Learning Models to Validate a Medication Regimen Complexity Scoring Tool 
   for Critically Ill Patients. Ann Pharmacother. 2021 Apr;55(4):421-429. 
   doi: 10.1177/1060028020959042.

The MRC-ICU is an objective, quantitative scoring tool that describes the relative 
complexity of medication regimens in critically ill patients. It consists of 39 
discrete medication items, each assigned a weighted value (1-3 points) that is 
summed to create a total MRC-ICU score. Higher scores correlate with increased 
mortality, longer ICU length of stay, and greater pharmacist workload.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MrcIcuScoreRequest(BaseModel):
    """
    Request model for Medication Regimen Complexity-ICU (MRC-ICU) Score
    
    The MRC-ICU Score quantifies medication regimen complexity in ICU patients using
    weighted values for different medication categories. Each medication type is
    assigned 1-3 points based on complexity, with some categories multiplied by the
    number of medications used.
    
    Key findings from validation studies:
    - Mean MRC-ICU score at 24 hours: 10.3 (SD 7.7)
    - Every 1-point increase associated with 7% increased odds of mortality
    - Every 1-point increase associated with 0.25 day increase in ICU LOS
    - Scores >10 indicate higher complexity and increased pharmacist workload
    
    This simplified version includes the most commonly used high-impact medications
    from the full 39-item validated tool.
    
    References (Vancouver style):
    1. Gwynn ME, Poisson MO, Hatton KM, Donihi AC, Campbell MJ, Al-Mamun MA, et al. 
       Development and validation of a medication regimen complexity scoring tool for 
       critically ill patients. Am J Health Syst Pharm. 2019 May 17;76(Supplement_2):S34-S40. 
       doi: 10.1093/ajhp/zxy054.
    2. Sikora A, Ayyala D, Rech MA, Donihi AC, Campbell M, Al-Mamun MA. Impact of 
       Pharmacists to Improve Patient Care in the Critically Ill: A Large Multicenter 
       Analysis Using Meaningful Metrics With the Medication Regimen Complexity-ICU 
       (MRC-ICU) Score. Crit Care Med. 2022 Sep 1;50(9):1318-1328. 
       doi: 10.1097/CCM.0000000000005585.
    """
    
    aminoglycosides: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of aminoglycosides (e.g., gentamicin, tobramycin, amikacin). "
                    "Each aminoglycoside scores 3 points due to need for therapeutic drug "
                    "monitoring, nephrotoxicity risk, and dosing complexity.",
        example=1
    )
    
    amphotericin_b: Literal["yes", "no"] = Field(
        ...,
        description="Presence of amphotericin B. Scores 1 point due to infusion reactions, "
                    "electrolyte monitoring requirements, and nephrotoxicity risk.",
        example="no"
    )
    
    antiarrhythmics: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of antiarrhythmic medications (e.g., amiodarone, lidocaine). "
                    "Each scores 1 point due to cardiac monitoring requirements and drug interactions.",
        example=1
    )
    
    anticoagulants: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of anticoagulant medications (e.g., heparin, warfarin, DOACs). "
                    "Each scores 1 point due to bleeding risk and monitoring requirements.",
        example=1
    )
    
    anticonvulsants: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of anticonvulsant medications (e.g., phenytoin, levetiracetam). "
                    "Each scores 3 points due to drug levels, interactions, and seizure monitoring.",
        example=0
    )
    
    argatroban: Literal["yes", "no"] = Field(
        ...,
        description="Presence of argatroban. Scores 2 points due to complex dosing, "
                    "hepatic adjustment requirements, and specialized monitoring.",
        example="no"
    )
    
    azole_antifungals: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of azole antifungal medications (e.g., fluconazole, voriconazole). "
                    "Each scores 2 points due to drug interactions and QTc prolongation risk.",
        example=0
    )
    
    blood_products: int = Field(
        ...,
        ge=0,
        le=10,
        description="Number of blood products (PRBCs, FFP, platelets, cryoprecipitate). "
                    "Each scores 2 points due to transfusion reactions and volume management.",
        example=2
    )
    
    chemotherapy: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of chemotherapy agents. Each scores 3 points due to toxicity "
                    "monitoring, supportive care requirements, and complexity.",
        example=0
    )
    
    clozapine: Literal["yes", "no"] = Field(
        ...,
        description="Presence of clozapine. Scores 3 points due to agranulocytosis risk, "
                    "required monitoring, and multiple drug interactions.",
        example="no"
    )
    
    digoxin: Literal["yes", "no"] = Field(
        ...,
        description="Presence of digoxin. Scores 3 points due to narrow therapeutic index, "
                    "drug level monitoring, and toxicity risk.",
        example="no"
    )
    
    vancomycin: Literal["yes", "no"] = Field(
        ...,
        description="Presence of vancomycin. Scores 3 points due to therapeutic drug "
                    "monitoring requirements, nephrotoxicity, and dosing complexity.",
        example="yes"
    )
    
    continuous_infusion_crystalloids: Literal["yes", "no"] = Field(
        ...,
        description="Continuous infusion of crystalloid fluids (e.g., normal saline, LR). "
                    "Scores 1 point due to volume status monitoring requirements.",
        example="yes"
    )
    
    vasopressors_inotropes: int = Field(
        ...,
        ge=0,
        le=5,
        description="Number of vasopressor/inotrope infusions (e.g., norepinephrine, epinephrine, "
                    "dopamine, dobutamine). Each scores 1 point due to hemodynamic monitoring.",
        example=1
    )
    
    continuous_opioid_infusions: int = Field(
        ...,
        ge=0,
        le=3,
        description="Number of continuous opioid infusions (e.g., fentanyl, morphine, hydromorphone). "
                    "Each scores 2 points due to sedation monitoring and withdrawal risk.",
        example=1
    )
    
    continuous_sedative_infusions: int = Field(
        ...,
        ge=0,
        le=3,
        description="Number of continuous sedative infusions (e.g., propofol, midazolam, "
                    "dexmedetomidine). Each scores 2 points due to sedation scales and delirium risk.",
        example=1
    )
    
    parenteral_nutrition: Literal["yes", "no"] = Field(
        ...,
        description="Presence of parenteral nutrition (TPN). Scores 2 points due to metabolic "
                    "monitoring, infection risk, and complexity of administration.",
        example="no"
    )
    
    insulin_infusion: Literal["yes", "no"] = Field(
        ...,
        description="Continuous insulin infusion. Scores 1 point due to frequent glucose "
                    "monitoring and hypoglycemia risk.",
        example="yes"
    )
    
    prn_opioids: Literal["yes", "no"] = Field(
        ...,
        description="As-needed (PRN) opioid medications. Scores 1 point due to pain "
                    "assessment requirements and administration frequency.",
        example="yes"
    )
    
    other_high_complexity_meds: int = Field(
        ...,
        ge=0,
        le=20,
        description="Number of other high-complexity medications not listed above (estimate). "
                    "Used to approximate additional complexity from the full 39-item tool.",
        example=3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "aminoglycosides": 1,
                "amphotericin_b": "no",
                "antiarrhythmics": 1,
                "anticoagulants": 1,
                "anticonvulsants": 0,
                "argatroban": "no",
                "azole_antifungals": 0,
                "blood_products": 2,
                "chemotherapy": 0,
                "clozapine": "no",
                "digoxin": "no",
                "vancomycin": "yes",
                "continuous_infusion_crystalloids": "yes",
                "vasopressors_inotropes": 1,
                "continuous_opioid_infusions": 1,
                "continuous_sedative_infusions": 1,
                "parenteral_nutrition": "no",
                "insulin_infusion": "yes",
                "prn_opioids": "yes",
                "other_high_complexity_meds": 3
            }
        }


class MrcIcuScoreResponse(BaseModel):
    """
    Response model for Medication Regimen Complexity-ICU (MRC-ICU) Score
    
    The MRC-ICU score predicts:
    - Mortality risk (7% increased odds per point increase)
    - ICU length of stay (0.25 day increase per point)
    - Pharmacist workload and intervention requirements
    - Overall medication regimen complexity
    
    Score interpretation:
    - <10: Low complexity
    - 10-19: Moderate complexity (mean score ~10.3)
    - ≥20: High complexity
    
    Reference: Gwynn ME, et al. Am J Health Syst Pharm. 2019;76(Supplement_2):S34-S40.
    """
    
    result: int = Field(
        ...,
        description="Total MRC-ICU score calculated from weighted medication values",
        example=15
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the MRC-ICU score including implications "
                    "for patient outcomes and pharmacist workload",
        example="Moderate MRC-ICU score indicates intermediate medication regimen complexity. "
                "Mean score in validation studies was approximately 10.3. Each 1-point increase "
                "is associated with 7% increased odds of mortality and 0.25 day increase in ICU LOS."
    )
    
    stage: str = Field(
        ...,
        description="Complexity category (Low, Moderate, or High Complexity)",
        example="Moderate Complexity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the complexity level",
        example="Moderate medication regimen complexity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 15,
                "unit": "points",
                "interpretation": "Moderate MRC-ICU score indicates intermediate medication regimen "
                                "complexity. Mean score in validation studies was approximately 10.3. "
                                "Each 1-point increase is associated with 7% increased odds of "
                                "mortality and 0.25 day increase in ICU LOS.",
                "stage": "Moderate Complexity",
                "stage_description": "Moderate medication regimen complexity"
            }
        }