"""
tPA (Alteplase) Dosing for Ischemic Stroke Calculator Models

Request and response models for tPA alteplase dosing calculation.

References (Vancouver style):
1. The National Institute of Neurological Disorders and Stroke rt-PA Stroke 
   Study Group. Tissue plasminogen activator for acute ischemic stroke. 
   N Engl J Med. 1995 Dec 14;333(24):1581-7. doi: 10.1056/NEJM199512143332401.
2. Hacke W, Kaste M, Bluhmki E, Brozman M, Dávalos A, Guidetti D, et al. 
   Thrombolysis with alteplase 3 to 4.5 hours after acute ischemic stroke. 
   N Engl J Med. 2008 Sep 25;359(13):1317-29. doi: 10.1056/NEJMoa0804656.
3. Powers WJ, Rabinstein AA, Ackerson T, Adeoye OM, Bambakidis NC, Becker K, 
   et al. Guidelines for the Early Management of Patients With Acute Ischemic 
   Stroke: 2019 Update to the 2018 Guidelines for the Early Management of 
   Acute Ischemic Stroke. Stroke. 2019 Dec;50(12):e344-e418. 
   doi: 10.1161/STR.0000000000000211.

The tPA (Alteplase) Dosing Calculator provides precise weight-based dosing 
for acute ischemic stroke treatment, ensuring safe and effective thrombolytic 
therapy administration within the critical time window for optimal patient outcomes.
"""

from pydantic import BaseModel, Field
from typing import Dict


class TpaAlteplaseDosingStrokeRequest(BaseModel):
    """
    Request model for tPA (Alteplase) Dosing for Ischemic Stroke Calculator
    
    This calculator determines the appropriate dose of tissue plasminogen activator 
    (alteplase) for acute ischemic stroke treatment based on patient weight. The 
    standard protocol uses 0.9 mg/kg with a maximum dose of 90 mg, administered 
    as 10% IV bolus over 1 minute followed by 90% continuous infusion over 60 minutes.
    
    Clinical Context and Therapeutic Background:
    
    Mechanism of Action:
    Alteplase is a recombinant tissue plasminogen activator that converts plasminogen 
    to plasmin, which then dissolves fibrin clots. In acute ischemic stroke, rapid 
    clot dissolution can restore cerebral blood flow and minimize brain tissue damage 
    if administered within the therapeutic time window.
    
    Evidence Base and Clinical Trials:
    The efficacy of alteplase in acute ischemic stroke was established through landmark 
    clinical trials, including the NINDS rt-PA Stroke Study (1995) which demonstrated 
    significant improvement in functional outcomes when treatment was initiated within 
    3 hours of symptom onset. Subsequent studies, including ECASS III (2008), extended 
    the treatment window to 4.5 hours for carefully selected patients.
    
    Dosing Rationale and Safety Profile:
    
    Weight-Based Dosing Protocol:
    The 0.9 mg/kg dosing regimen was established through dose-finding studies that 
    balanced efficacy with bleeding risk. This dose provides optimal clot lysis 
    while minimizing the risk of intracranial hemorrhage, the most serious 
    complication of thrombolytic therapy.
    
    Maximum Dose Limitation:
    The 90 mg maximum dose cap ensures safety in larger patients, as higher absolute 
    doses may increase bleeding risk without proportional efficacy benefits. Patients 
    weighing more than 100 kg receive a lower per-kilogram dose due to this cap.
    
    Administration Protocol:
    
    Two-Phase Delivery System:
    The split dosing regimen (10% bolus + 90% infusion) provides immediate 
    thrombolytic activity while maintaining sustained drug levels throughout 
    the treatment period. The initial bolus achieves rapid therapeutic levels, 
    while the prolonged infusion ensures continued clot dissolution.
    
    Timing Considerations:
    - Bolus: 10% of total dose over exactly 1 minute
    - Infusion: Remaining 90% over exactly 60 minutes
    - Total treatment duration: 61 minutes
    
    Clinical Monitoring and Safety:
    
    Contraindications Assessment:
    Before administration, patients must be carefully screened for contraindications 
    including recent surgery, active bleeding, uncontrolled hypertension, and 
    hemorrhagic stroke. Imaging studies (CT or MRI) are mandatory to exclude 
    intracranial hemorrhage.
    
    Monitoring Parameters:
    - Neurological status every 15 minutes during infusion
    - Blood pressure monitoring (maintain <185/110 mmHg)
    - Signs of bleeding complications
    - Post-treatment imaging at 24 hours
    
    Special Considerations:
    
    Time Window Optimization:
    Treatment benefit is time-dependent, with maximal benefit achieved when treatment 
    is initiated within 90 minutes of symptom onset. The "time is brain" principle 
    emphasizes rapid evaluation and treatment to preserve viable brain tissue.
    
    Patient Selection Criteria:
    Careful patient selection based on clinical presentation, imaging findings, 
    and absence of contraindications is crucial for optimizing benefit-to-risk 
    ratio. Age, stroke severity, and time from onset are key considerations.
    
    Facility Requirements:
    Treatment should only be administered in stroke-capable facilities with 
    immediate access to neurology consultation, advanced imaging, and 
    neurosurgical capabilities for managing potential complications.
    
    Practical Administration Considerations:
    
    Preparation and Mixing:
    Alteplase requires careful reconstitution and preparation according to 
    manufacturer guidelines. The medication should be mixed just before 
    administration and used immediately to maintain potency.
    
    Pump Considerations:
    Up to 20 mL (20 mg) of medication may remain in IV pump tubing after 
    infusion completion. Standard practice includes flushing with 50 mL 
    of normal saline to ensure complete drug delivery.
    
    Post-Treatment Care:
    
    Antiplatelet and Anticoagulant Management:
    Aspirin and other antiplatelet agents should be held for 24 hours post-treatment. 
    Anticoagulation should be avoided for 24-48 hours unless specifically indicated 
    and bleeding risk is carefully assessed.
    
    Complications Management:
    Immediate availability of reversal agents (cryoprecipitate, fresh frozen plasma) 
    and neurosurgical consultation is essential. Any decline in neurological status 
    requires immediate evaluation for intracranial hemorrhage.
    
    Quality Measures and Outcomes:
    
    Performance Metrics:
    Door-to-needle time is a key quality metric, with guidelines recommending 
    treatment initiation within 60 minutes of hospital arrival. This requires 
    streamlined protocols and multidisciplinary coordination.
    
    Long-term Outcomes:
    When administered appropriately, alteplase significantly improves functional 
    independence at 90 days, reduces disability, and decreases long-term 
    healthcare costs despite the initial complexity of acute treatment.
    
    References (Vancouver style):
    1. The National Institute of Neurological Disorders and Stroke rt-PA Stroke 
       Study Group. Tissue plasminogen activator for acute ischemic stroke. 
       N Engl J Med. 1995 Dec 14;333(24):1581-7. doi: 10.1056/NEJM199512143332401.
    2. Hacke W, Kaste M, Bluhmki E, Brozman M, Dávalos A, Guidetti D, et al. 
       Thrombolysis with alteplase 3 to 4.5 hours after acute ischemic stroke. 
       N Engl J Med. 2008 Sep 25;359(13):1317-29. doi: 10.1056/NEJMoa0804656.
    3. Powers WJ, Rabinstein AA, Ackerson T, Adeoye OM, Bambakidis NC, Becker K, 
       et al. Guidelines for the Early Management of Patients With Acute Ischemic 
       Stroke: 2019 Update to the 2018 Guidelines for the Early Management of 
       Acute Ischemic Stroke. Stroke. 2019 Dec;50(12):e344-e418. 
       doi: 10.1161/STR.0000000000000211.
    """
    
    weight: float = Field(
        ...,
        ge=30.0,
        le=200.0,
        description="Patient weight in kilograms. Must be between 30-200 kg for safe calculation. "
                   "Accurate weight measurement is critical as tPA dosing is weight-based at 0.9 mg/kg "
                   "with a maximum dose of 90 mg. Weight estimation errors can lead to underdosing or "
                   "overdosing, affecting both efficacy and safety outcomes.",
        example=75.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight": 75.0
            }
        }


class TpaDosingResult(BaseModel):
    """
    Detailed dosing calculation results for tPA administration
    """
    
    total_dose: float = Field(
        ...,
        description="Total alteplase dose in mg (0.9 mg/kg, maximum 90 mg)",
        example=67.5
    )
    
    bolus_dose: float = Field(
        ...,
        description="Initial bolus dose in mg (10% of total dose, administered over 1 minute)",
        example=6.8
    )
    
    infusion_dose: float = Field(
        ...,
        description="Continuous infusion dose in mg (90% of total dose, administered over 60 minutes)",
        example=60.8
    )
    
    bolus_duration_minutes: int = Field(
        ...,
        description="Duration for bolus administration in minutes",
        example=1
    )
    
    infusion_duration_minutes: int = Field(
        ...,
        description="Duration for continuous infusion in minutes",
        example=60
    )
    
    max_dose_applied: bool = Field(
        ...,
        description="Whether the 90 mg maximum dose cap was applied (for patients >100 kg)",
        example=False
    )
    
    actual_dose_per_kg: float = Field(
        ...,
        description="Actual dose per kg administered (may be <0.9 mg/kg if maximum dose applied)",
        example=0.9
    )


class TpaAlteplaseDosingStrokeResponse(BaseModel):
    """
    Response model for tPA (Alteplase) Dosing for Ischemic Stroke Calculator
    
    Provides comprehensive dosing information including total dose calculation, 
    bolus and infusion components, administration timing, and clinical guidance 
    for safe and effective alteplase therapy in acute ischemic stroke.
    
    Clinical Interpretation Framework:
    
    Standard Weight-Based Dosing (≤100 kg patients):
    Patients weighing 100 kg or less receive the full 0.9 mg/kg dose, providing 
    optimal balance between efficacy and safety. This dosing has been validated 
    in multiple clinical trials and provides the best functional outcomes when 
    administered within the appropriate time window.
    
    Maximum Dose Application (>100 kg patients):
    For patients exceeding 100 kg, the 90 mg maximum dose cap is applied, resulting 
    in a lower per-kilogram dose. This safety measure prevents excessive drug 
    exposure while maintaining therapeutic efficacy. Clinical outcomes remain 
    favorable despite the reduced per-kilogram dosing.
    
    Administration Protocol:
    
    Bolus Phase (First minute):
    The initial 10% bolus provides immediate therapeutic drug levels to initiate 
    clot dissolution. This rapid delivery is critical for early reperfusion and 
    optimal neurological outcomes.
    
    Infusion Phase (Following 60 minutes):
    The prolonged infusion maintains therapeutic drug levels throughout the 
    critical period for clot dissolution. This sustained delivery maximizes 
    the likelihood of complete recanalization.
    
    Safety Monitoring:
    
    Critical Monitoring Parameters:
    - Neurological assessments every 15 minutes during infusion
    - Blood pressure control (maintain <185/110 mmHg)
    - Continuous cardiac monitoring
    - Assessment for bleeding complications
    
    Warning Signs Requiring Immediate Intervention:
    - Neurological deterioration (possible hemorrhagic conversion)
    - Severe headache or nausea/vomiting
    - Blood pressure elevation above target range
    - Signs of systemic bleeding
    
    Post-Treatment Management:
    
    Immediate Post-Infusion Care:
    - Flush IV line with 50 mL normal saline
    - Continue neurological monitoring for 24 hours
    - Maintain blood pressure control
    - Hold antiplatelet therapy for 24 hours
    
    Follow-up Imaging:
    Repeat brain imaging at 24 hours or sooner if neurological deterioration 
    occurs. This imaging assesses for hemorrhagic transformation and guides 
    further management decisions.
    
    Quality Assurance Considerations:
    
    Dose Verification:
    Always perform independent double-check of weight-based calculations before 
    administration. Dosing errors can have serious clinical consequences in this 
    high-risk, time-sensitive treatment scenario.
    
    Documentation Requirements:
    Document exact timing of symptom onset, contraindication assessment, dose 
    calculations, and monitoring parameters for quality assurance and potential 
    research purposes.
    
    Reference: Powers WJ, et al. Stroke. 2019;50(12):e344-e418.
    """
    
    result: TpaDosingResult = Field(
        ...,
        description="Detailed dosing calculation results including total dose, bolus, infusion components, "
                   "timing parameters, and safety considerations for tPA administration"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for dosing calculations",
        example="mg"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with specific administration instructions, "
                   "monitoring requirements, safety considerations, and practical guidance for "
                   "tPA therapy in acute ischemic stroke",
        example="Patient weighs 75.0 kg. Total dose: 67.5 mg (0.9 mg/kg). Administer 6.8 mg as IV bolus "
                "over 1 minute, followed by 60.8 mg as continuous infusion over 60 minutes. Ensure "
                "treatment is initiated within 3-4.5 hours of stroke symptom onset. Monitor for bleeding "
                "complications and neurological changes. Note: Up to 20 mg may remain in pump tubing; "
                "flush with 50 mL normal saline after infusion."
    )
    
    stage: str = Field(
        ...,
        description="Dosing category based on patient weight and maximum dose considerations",
        example="Standard Weight-Based Dosing"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the dosing approach applied",
        example="0.9 mg/kg dosing protocol applied"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_dose": 67.5,
                    "bolus_dose": 6.8,
                    "infusion_dose": 60.8,
                    "bolus_duration_minutes": 1,
                    "infusion_duration_minutes": 60,
                    "max_dose_applied": False,
                    "actual_dose_per_kg": 0.9
                },
                "unit": "mg",
                "interpretation": "Patient weighs 75.0 kg. Total dose: 67.5 mg (0.9 mg/kg). Administer 6.8 mg as IV bolus over 1 minute, followed by 60.8 mg as continuous infusion over 60 minutes. Ensure treatment is initiated within 3-4.5 hours of stroke symptom onset. Monitor for bleeding complications and neurological changes. Note: Up to 20 mg may remain in pump tubing; flush with 50 mL normal saline after infusion.",
                "stage": "Standard Weight-Based Dosing",
                "stage_description": "0.9 mg/kg dosing protocol applied"
            }
        }