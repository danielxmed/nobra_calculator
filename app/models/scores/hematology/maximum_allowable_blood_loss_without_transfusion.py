"""
Maximum Allowable Blood Loss (ABL) Without Transfusion Models

Request and response models for ABL calculation in surgical blood loss management.

References (Vancouver style):
1. Gross JB. Estimating allowable blood loss: corrected for dilution. 
   Anesthesiology. 1983 Mar;58(3):277-80. doi: 10.1097/00000542-198303000-00016.
2. Miller RD, ed. Miller's Anesthesia. 8th ed. Philadelphia, PA: Elsevier Saunders; 2015.
3. American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
   Practice guidelines for perioperative blood management: an updated report by the 
   American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
   Anesthesiology. 2015;122(2):241-75. doi: 10.1097/ALN.0000000000000463.
4. Carson JL, Grossman BJ, Kleinman S, Tinmouth AT, Marques MB, Fung MK, et al. 
   Red blood cell transfusion: a clinical practice guideline from the AABB. 
   Ann Intern Med. 2012;157(1):49-58. doi: 10.7326/0003-4819-157-1-201206190-00429.

The Maximum Allowable Blood Loss (ABL) calculator is a critical perioperative tool 
developed by Jeffrey Gross in 1983 to estimate the maximum volume of blood loss that 
can be tolerated during surgery before transfusion becomes necessary. This calculation 
helps anesthesiologists and surgeons make evidence-based decisions about blood 
transfusion timing, guide intraoperative blood management strategies, and optimize 
patient safety during procedures with potential for significant blood loss.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MaximumAllowableBloodLossWithoutTransfusionRequest(BaseModel):
    """
    Request model for Maximum Allowable Blood Loss (ABL) Without Transfusion
    
    This calculator estimates the maximum allowable blood loss during surgery before 
    transfusion should be considered, using the Gross formula developed in 1983.
    
    **Clinical Background:**
    
    Surgical blood loss is a major concern in perioperative medicine, and the decision 
    to transfuse blood products carries both benefits and risks. The ABL calculation 
    provides an objective, evidence-based approach to guide transfusion decisions by 
    estimating how much blood loss a patient can tolerate while maintaining adequate 
    oxygen delivery and hemodynamic stability.
    
    **Calculation Methodology:**
    
    **Gross Formula:** ABL = [EBV × (Hi - Hf)] / Hav
    
    Where:
    - **ABL** = Maximum allowable blood loss (mL)
    - **EBV** = Estimated blood volume (body weight × blood volume coefficient)
    - **Hi** = Initial preoperative hemoglobin (g/dL)
    - **Hf** = Final acceptable hemoglobin (g/dL)
    - **Hav** = Average hemoglobin = (Hi + Hf) / 2
    
    **Key Parameters:**
    
    1. **Age Group (Blood Volume Coefficients)**:
       - **Adult Male**: 75 mL/kg - Highest blood volume due to greater muscle mass
       - **Adult Female**: 65 mL/kg - Lower than males due to body composition differences
       - **Infant (1 month - 2 years)**: 80 mL/kg - Higher relative blood volume
       - **Neonate (birth - 1 month)**: 85 mL/kg - High relative blood volume for growth
       - **Premature Neonate (<37 weeks)**: 96 mL/kg - Highest coefficient due to developmental needs
    
    2. **Body Weight (0.5-200 kg)**:
       - Direct multiplier for blood volume calculation
       - Critical for accurate ABL estimation, especially in pediatric patients
       - Small changes in weight significantly impact calculated blood volume
    
    3. **Initial Hemoglobin (3.0-25.0 g/dL)**:
       - Preoperative baseline hemoglobin level
       - Normal ranges: Men 13.5-17.5 g/dL, Women 12.0-15.5 g/dL, Children 11.0-15.0 g/dL
       - Higher initial levels allow for greater blood loss tolerance
    
    4. **Final Hemoglobin (3.0-15.0 g/dL)**:
       - Lowest acceptable hemoglobin before transfusion
       - **Standard Thresholds**:
         - Most patients: 7-10 g/dL
         - Critical patients (cardiac disease): 8-10 g/dL
         - Healthy patients: 6-8 g/dL may be acceptable
         - Emergency threshold: <6 g/dL almost always requires transfusion
    
    **Clinical Applications:**
    
    **Preoperative Planning:**
    - Calculate ABL for all procedures with anticipated significant blood loss
    - Guide preoperative optimization strategies
    - Determine need for preoperative autologous blood donation
    - Plan intraoperative monitoring frequency
    
    **Intraoperative Management:**
    - Real-time guidance for transfusion decisions
    - Monitor cumulative blood loss against calculated threshold
    - Adjust anesthesia and surgical techniques based on tolerance
    - Guide blood conservation strategies
    
    **Patient Categories:**
    
    **Pediatric Considerations:**
    - Small blood volumes make calculation particularly important
    - Higher blood volume coefficients reflect developmental physiology
    - Even small absolute blood losses can be clinically significant
    - Frequent monitoring required due to limited reserves
    
    **Adult Considerations:**
    - Gender differences in blood volume coefficients
    - Comorbidities affect transfusion thresholds
    - Cardiac patients may require higher hemoglobin targets
    - Age-related changes in physiologic reserve
    
    **Limitations and Considerations:**
    
    **Calculation Accuracy:**
    - Becomes unreliable when blood loss >20% of estimated blood volume
    - Assumes steady-state conditions and gradual blood loss
    - May not apply to acute massive hemorrhage
    - Requires clinical correlation with hemodynamic status
    
    **Clinical Factors Not Included:**
    - Patient cardiac function and oxygen demand
    - Rate of blood loss (acute vs. gradual)
    - Coexisting medical conditions
    - Surgical complexity and duration
    - Ambient temperature and metabolic demands
    
    **Quality Assurance:**
    - Always correlate with clinical assessment
    - Monitor hemodynamic parameters continuously
    - Consider individual patient factors
    - Reassess if clinical condition changes
    
    References (Vancouver style):
    1. Gross JB. Estimating allowable blood loss: corrected for dilution. 
       Anesthesiology. 1983 Mar;58(3):277-80. doi: 10.1097/00000542-198303000-00016.
    2. American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
       Practice guidelines for perioperative blood management: an updated report by the 
       American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
       Anesthesiology. 2015;122(2):241-75. doi: 10.1097/ALN.0000000000000463.
    """
    
    age_group: Literal["adult_man", "adult_woman", "infant", "neonate", "premature_neonate"] = Field(
        ...,
        description="Patient age group determining blood volume coefficient. Adult man (75 mL/kg), adult woman (65 mL/kg), infant 1 month-2 years (80 mL/kg), neonate birth-1 month (85 mL/kg), premature neonate <37 weeks (96 mL/kg)",
        example="adult_woman"
    )
    
    body_weight: float = Field(
        ...,
        ge=0.5,
        le=200,
        description="Patient body weight in kg. Used to calculate estimated blood volume (EBV = weight × blood volume coefficient). Critical parameter as blood volume directly correlates with weight, particularly important in pediatric patients",
        example=70.0
    )
    
    initial_hemoglobin: float = Field(
        ...,
        ge=3.0,
        le=25.0,
        description="Preoperative hemoglobin level in g/dL. Baseline value before surgical blood loss. Normal ranges: men 13.5-17.5 g/dL, women 12.0-15.5 g/dL, children 11.0-15.0 g/dL. Higher initial levels allow greater blood loss tolerance",
        example=12.5
    )
    
    final_hemoglobin: float = Field(
        ...,
        ge=3.0,
        le=15.0,
        description="Lowest acceptable hemoglobin level in g/dL before transfusion is indicated. Typical thresholds: most patients 7-10 g/dL, critical patients 8-10 g/dL, healthy patients 6-8 g/dL. Emergency threshold <6 g/dL almost always requires transfusion",
        example=8.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_group": "adult_woman",
                "body_weight": 70.0,
                "initial_hemoglobin": 12.5,
                "final_hemoglobin": 8.0
            }
        }


class MaximumAllowableBloodLossWithoutTransfusionResponse(BaseModel):
    """
    Response model for Maximum Allowable Blood Loss (ABL) Without Transfusion
    
    Provides comprehensive blood loss tolerance assessment with clinical guidance 
    for perioperative blood management and transfusion decision-making.
    
    **Interpretation Categories:**
    
    **Low Volume Loss (≤500 mL):**
    - Limited blood loss tolerance
    - Requires meticulous hemostasis and frequent monitoring
    - Consider blood conservation strategies early
    - Prepare for potential early transfusion
    - Often seen in small patients, low baseline hemoglobin, or conservative thresholds
    
    **Moderate Volume Loss (501-1,500 mL):**
    - Standard blood loss tolerance for routine procedures
    - Appropriate for most surgical interventions
    - Standard monitoring protocols sufficient
    - Transfusion consideration when approaching threshold
    - Typical for average-sized patients with normal hemoglobin
    
    **High Volume Loss (1,501-3,000 mL):**
    - Good tolerance for significant blood loss
    - Suitable for major surgical procedures
    - Allows for substantial bleeding before transfusion
    - Enhanced monitoring recommended
    - Often reflects large patients or high initial hemoglobin
    
    **Very High Volume Loss (>3,000 mL):**
    - Excellent blood loss tolerance
    - Appropriate for extensive, high-volume procedures
    - Significant bleeding tolerance before transfusion
    - Consider advanced blood conservation techniques
    - Reflects optimal baseline parameters
    
    **Clinical Management Strategies:**
    
    **Blood Conservation Techniques:**
    - Preoperative autologous blood donation
    - Intraoperative cell salvage (Cell Saver)
    - Acute normovolemic hemodilution
    - Antifibrinolytic agents (tranexamic acid, aminocaproic acid)
    - Topical hemostatic agents
    - Controlled hypotension when appropriate
    
    **Monitoring Protocols:**
    - Serial hemoglobin/hematocrit measurements
    - Continuous hemodynamic monitoring
    - Urine output assessment
    - Arterial blood gas analysis
    - Coagulation studies for ongoing bleeding
    - Central venous pressure monitoring
    
    **Transfusion Considerations:**
    - Clinical symptoms outweigh calculated values
    - Hemodynamic instability may require earlier transfusion
    - Ongoing bleeding affects threshold decisions
    - Patient comorbidities influence transfusion timing
    - Rate of blood loss impacts tolerance
    
    **Quality Metrics:**
    - Calculation reliability (accurate when blood loss <20% EBV)
    - Percentage of estimated blood volume lost
    - Clinical correlation with patient status
    - Hemoglobin reserve available
    - Risk stratification based on calculated tolerance
    
    **Documentation Requirements:**
    - Preoperative ABL calculation
    - Intraoperative blood loss measurement
    - Transfusion rationale if threshold exceeded
    - Hemodynamic response to blood loss
    - Post-operative hemoglobin levels
    
    Reference: Gross JB. Anesthesiology. 1983;58(3):277-80.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive ABL assessment including calculated blood loss tolerance, blood volume parameters, clinical assessment, and risk stratification",
        example={
            "maximum_allowable_blood_loss_ml": 1462.5,
            "estimated_blood_volume_ml": 4550.0,
            "blood_volume_coefficient_ml_kg": 65,
            "average_hemoglobin_g_dl": 10.25,
            "hemoglobin_difference_g_dl": 4.5,
            "percentage_of_blood_volume": 32.1,
            "clinical_assessment": {
                "age_group_description": "Adult female (≥18 years)",
                "percentage_of_blood_volume": 32.1,
                "accuracy_reliable": False,
                "accuracy_note": "Calculation may be inaccurate >20% EBV loss",
                "transfusion_threshold_assessment": "Within typical transfusion threshold range",
                "patient_size_category": "Average-sized patient - standard monitoring",
                "risk_stratification": "Standard risk - typical blood loss tolerance",
                "hemoglobin_reserve": 4.5,
                "clinical_significance": "High"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the blood loss volume",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with blood loss tolerance assessment, management recommendations, monitoring requirements, and clinical considerations",
        example="Maximum allowable blood loss of 1462.5 mL represents moderate tolerance for surgical bleeding, suitable for most routine procedures. Standard intraoperative monitoring protocols apply, including periodic hemoglobin checks and vital sign assessment. Consider blood conservation measures for procedures with anticipated moderate blood loss. Transfusion should be considered when blood loss approaches this calculated threshold, taking into account patient hemodynamic status, ongoing bleeding, and clinical condition. Ensure type and screen or crossmatch is current."
    )
    
    stage: str = Field(
        ...,
        description="Blood loss tolerance category (Low Volume Loss, Moderate Volume Loss, High Volume Loss, Very High Volume Loss)",
        example="Moderate Volume Loss"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the blood loss tolerance category",
        example="Moderate allowable blood loss"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "maximum_allowable_blood_loss_ml": 1462.5,
                    "estimated_blood_volume_ml": 4550.0,
                    "blood_volume_coefficient_ml_kg": 65,
                    "average_hemoglobin_g_dl": 10.25,
                    "hemoglobin_difference_g_dl": 4.5,
                    "percentage_of_blood_volume": 32.1,
                    "clinical_assessment": {
                        "age_group_description": "Adult female (≥18 years)",
                        "percentage_of_blood_volume": 32.1,
                        "accuracy_reliable": False,
                        "accuracy_note": "Calculation may be inaccurate >20% EBV loss",
                        "transfusion_threshold_assessment": "Within typical transfusion threshold range",
                        "patient_size_category": "Average-sized patient - standard monitoring",
                        "risk_stratification": "Standard risk - typical blood loss tolerance",
                        "hemoglobin_reserve": 4.5,
                        "clinical_significance": "High"
                    }
                },
                "unit": "mL",
                "interpretation": "Maximum allowable blood loss of 1462.5 mL represents moderate tolerance for surgical bleeding, suitable for most routine procedures. Standard intraoperative monitoring protocols apply, including periodic hemoglobin checks and vital sign assessment. Consider blood conservation measures for procedures with anticipated moderate blood loss. Transfusion should be considered when blood loss approaches this calculated threshold, taking into account patient hemodynamic status, ongoing bleeding, and clinical condition. Ensure type and screen or crossmatch is current.",
                "stage": "Moderate Volume Loss",
                "stage_description": "Moderate allowable blood loss"
            }
        }