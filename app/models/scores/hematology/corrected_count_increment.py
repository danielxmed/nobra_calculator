"""
Corrected Count Increment (CCI) for Platelet Transfusion Models

Request and response models for CCI platelet transfusion response assessment calculation.

References (Vancouver style):
1. Davis KB, Slichter SJ, Corash L. Corrected count increment and percent platelet recovery 
   as measures of posttransfusion platelet response: problems and a solution. 
   Transfusion. 1999;39(6):586-92.
2. Bishop JF, Matthews JP, McGrath K, Yuen K, Wolf MM, Szer J. Factors influencing 20-hour 
   increments after platelet transfusion. Transfusion. 1991;31(5):392-6.
3. Slichter SJ, Davis K, Enright H, et al. Factors affecting posttransfusion platelet increments, 
   platelet refractoriness, and platelet transfusion intervals in thrombocytopenic patients. 
   Blood. 2005;105(10):4106-14.

The Corrected Count Increment (CCI) is a standardized measure used to assess the adequacy 
of response to platelet transfusion. It quantifies the expected increase in platelet count 
following transfusion, adjusted for patient body surface area and the number of platelets 
transfused, providing an objective assessment of platelet transfusion effectiveness.

Clinical Background and Development:

Platelet Transfusion Assessment:
Platelet transfusions are critical therapeutic interventions for patients with thrombocytopenia 
or platelet dysfunction. However, not all patients respond adequately to platelet transfusions, 
a condition known as platelet refractoriness. The CCI provides a standardized method to 
evaluate transfusion effectiveness and identify patients who may be refractory to platelet 
transfusions.

Formula and Calculation:
The CCI is calculated using the formula:
CCI = (Count Increment × Body Surface Area) / Platelet Dose

Where:
- Count Increment = Post-transfusion platelet count - Pre-transfusion platelet count
- Body Surface Area = sqrt((height_cm × weight_kg) / 3600) using DuBois formula
- Platelet Dose = Total platelet content in transfused units (×10¹¹ platelets)

Interpretation Thresholds and Clinical Significance:

1-Hour Post-Transfusion Assessment:
- CCI >7,500: Indicates successful platelet transfusion with adequate response
- CCI ≤7,500: Suggests poor platelet response requiring further evaluation

20-Hour Post-Transfusion Assessment:
- CCI >4,800: Indicates successful platelet transfusion with adequate response  
- CCI ≤4,800: Suggests poor platelet response requiring further evaluation

The different thresholds reflect the natural decline in platelet count over time due to 
normal platelet consumption and clearance mechanisms.

Platelet Refractoriness:
Platelet refractoriness is defined as the failure to achieve an acceptable platelet count 
increment following platelet transfusion on at least two consecutive occasions, in the 
absence of other identifiable causes of poor response.

Causes of Poor Platelet Response:
- Immune factors: HLA alloimmunization, platelet-specific antibodies
- Non-immune factors: Fever, sepsis, DIC, active bleeding, splenomegaly
- Drug interactions: Amphotericin B, vancomycin, heparin
- Patient factors: ABO incompatibility, massive transfusion

Clinical Applications and Use Cases:

Transfusion Medicine Practice:
The CCI is widely used in transfusion medicine to:
- Assess platelet transfusion effectiveness objectively
- Identify patients with platelet refractoriness
- Guide decisions regarding alternative transfusion strategies
- Monitor treatment response in refractory patients
- Optimize platelet inventory management

Patient Management Implications:
- Normal CCI: Continue standard platelet transfusion protocols
- Low CCI: Investigate underlying causes, consider HLA-matched platelets
- Persistent low CCI: Evaluate for alternative bleeding management strategies

Quality Assurance:
The CCI serves as a quality metric for transfusion services to monitor the effectiveness 
of their platelet products and transfusion practices.

Implementation Guidelines:

Timing of Assessment:
- 1-hour post-transfusion: Optimal for assessing immediate response
- 10-minute post-transfusion: Alternative timing that yields similar information
- 20-hour post-transfusion: Assesses platelet survival and longer-term response

Patient Selection:
- Appropriate for all patients receiving platelet transfusions
- Particularly important in patients with recurrent thrombocytopenia
- Essential for patients with suspected platelet refractoriness

Data Collection Requirements:
- Accurate pre- and post-transfusion platelet counts
- Precise timing of blood collection relative to transfusion
- Complete patient anthropometric data (height and weight)
- Accurate platelet unit content information

Limitations and Considerations:

Technical Limitations:
- Requires accurate platelet counting methodology
- Dependent on precise timing of blood collection
- May be affected by sample collection and processing variables

Clinical Limitations:
- Does not assess platelet function, only count increment
- May be influenced by concurrent medications or medical conditions
- Normal CCI does not guarantee hemostatic effectiveness

Interpretation Context:
- Results should be interpreted within the broader clinical context
- Consider concurrent medical conditions affecting platelet function
- Account for patient-specific factors that may influence platelet survival

Alternative Assessment Methods:
- Percent Platelet Recovery (PPR): Alternative measure of transfusion response
- Platelet function testing: Assesses qualitative platelet function
- Bleeding assessment tools: Evaluate clinical hemostatic effectiveness

Research and Quality Improvement Applications:

Clinical Research:
The CCI is used in research studies to:
- Compare effectiveness of different platelet products
- Evaluate new transfusion strategies and protocols
- Assess impact of storage conditions on platelet viability
- Study factors affecting platelet transfusion outcomes

Quality Improvement:
- Monitor transfusion service performance metrics
- Identify trends in platelet transfusion effectiveness
- Guide inventory management and product selection decisions
- Support evidence-based transfusion practice development

This calculator provides a standardized, validated approach to assessing platelet transfusion 
effectiveness, supporting evidence-based transfusion medicine practice and optimal patient care.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CorrectedCountIncrementRequest(BaseModel):
    """
    Request model for Corrected Count Increment (CCI) for Platelet Transfusion
    
    The CCI is a standardized measure used to assess the adequacy of response to platelet 
    transfusion. It quantifies the expected increase in platelet count following transfusion, 
    adjusted for patient body surface area and the number of platelets transfused.
    
    Assessment Framework and Parameter Specifications:
    
    The CCI calculation requires six key parameters to accurately assess platelet transfusion response:
    
    Pre-Transfusion Platelet Count:
    The baseline platelet count measured immediately before platelet transfusion, typically 
    within 1-2 hours of transfusion. This establishes the starting point for calculating 
    the count increment achieved by transfusion.
    
    Clinical Significance:
    - Provides baseline for increment calculation
    - Helps assess degree of thrombocytopenia
    - Important for determining transfusion indication
    - Should be drawn from peripheral blood sample
    
    Measurement Guidelines:
    - Use automated cell counter for accuracy
    - Avoid samples from central lines if possible (may be diluted)
    - Ensure proper EDTA anticoagulation
    - Process sample within 1-2 hours of collection
    
    Post-Transfusion Platelet Count:
    The platelet count measured at either 1 hour or 20 hours following completion of 
    platelet transfusion. The timing affects the interpretation threshold used for 
    assessing transfusion adequacy.
    
    Clinical Significance:
    - Measures actual platelet increment achieved
    - Timing determines which threshold to apply
    - 1-hour sample assesses immediate response
    - 20-hour sample evaluates platelet survival
    
    Measurement Guidelines:
    - Same methodology as pre-transfusion sample
    - Precise timing documentation is critical
    - Avoid samples during active bleeding
    - Consider patient's clinical status when interpreting
    
    Time After Transfusion:
    The specific time point when the post-transfusion sample was collected, either 
    1 hour or 20 hours after completion of transfusion. This parameter determines 
    which threshold is used for clinical interpretation.
    
    Assessment Options:
    - 1 Hour: Optimal for immediate response assessment (threshold >7,500)
    - 20 Hours: Evaluates platelet survival (threshold >4,800)
    
    Clinical Considerations:
    - 1-hour timing is most commonly used in clinical practice
    - 10-minute post-transfusion sampling yields similar results
    - 20-hour timing better reflects platelet survival
    - Choose timing based on clinical question and practical considerations
    
    Patient Height:
    Patient height measurement in inches, used to calculate body surface area (BSA) 
    for the CCI correction factor. Accurate anthropometric data is essential for 
    proper CCI calculation.
    
    Measurement Guidelines:
    - Use standardized height measurement techniques
    - Standing height preferred when possible
    - For bedridden patients, use recumbent length
    - Document measurement method used
    - Convert to inches if measured in centimeters
    
    Clinical Significance:
    - Required for BSA calculation using DuBois formula
    - Affects interpretation of platelet increment
    - Larger patients require higher absolute increments for same CCI
    - Important for standardizing response across patient populations
    
    Patient Weight:
    Patient weight measurement in pounds, used in combination with height to calculate 
    body surface area for the CCI correction factor.
    
    Measurement Guidelines:
    - Use calibrated scales for accuracy
    - Measure at consistent time (ideally morning)
    - Account for clothing weight if applicable
    - For critically ill patients, use bed scale
    - Convert to pounds if measured in kilograms
    
    Clinical Significance:
    - Essential component of BSA calculation
    - Affects expected platelet increment
    - May fluctuate in critically ill patients
    - Consider fluid status when interpreting
    
    Platelet Unit Content:
    The total platelet content in all transfused units, expressed as ×10¹¹ platelets. 
    This represents the actual dose of platelets administered and is critical for 
    accurate CCI calculation.
    
    Determination Guidelines:
    - Use platelet count from unit labels when available
    - Standard apheresis units typically contain 3-6 × 10¹¹ platelets
    - Pooled random donor units vary more widely
    - For multiple units, sum the total content
    - Consider unit age and storage conditions
    
    Clinical Significance:
    - Represents the denominator in CCI calculation
    - Higher platelet doses should yield higher increments
    - Quality indicator for blood bank operations
    - Affects cost-effectiveness of transfusion therapy
    
    Calculation Process and Formula Application:
    
    Body Surface Area Calculation:
    BSA (m²) = sqrt((height_cm × weight_kg) / 3600)
    
    This uses the DuBois formula, which is widely accepted for clinical applications 
    and provides accurate BSA estimates across diverse patient populations.
    
    Count Increment Calculation:
    Count Increment = Post-transfusion count - Pre-transfusion count
    
    This represents the actual increase in platelet count achieved by transfusion.
    
    Final CCI Calculation:
    CCI = (Count Increment × BSA) / Platelet Dose
    
    The resulting value is expressed in units of platelets/μL/m²/(×10¹¹ platelets).
    
    Clinical Interpretation Framework:
    
    Threshold-Based Assessment:
    - CCI >7,500 at 1 hour: Successful transfusion
    - CCI ≤7,500 at 1 hour: Poor response, evaluate for refractoriness
    - CCI >4,800 at 20 hours: Successful transfusion
    - CCI ≤4,800 at 20 hours: Poor response, evaluate for refractoriness
    
    Clinical Decision Making:
    Successful Response:
    - Continue standard transfusion protocols
    - Monitor for future transfusion needs
    - Document successful response in patient record
    
    Poor Response:
    - Investigate underlying causes of refractoriness
    - Consider HLA-matched or crossmatched platelets
    - Evaluate for non-immune causes (fever, sepsis, medications)
    - Consider alternative bleeding management strategies
    
    Quality Assurance and Validation:
    
    Data Validation:
    - Verify all input parameters for accuracy
    - Check timing documentation
    - Confirm unit content information
    - Review for data entry errors
    
    Clinical Context:
    - Consider patient's overall clinical condition
    - Account for concurrent medications
    - Evaluate for active bleeding or consumption
    - Document any confounding factors
    
    Limitations and Considerations:
    
    Technical Limitations:
    - Requires accurate platelet counting
    - Dependent on precise timing
    - May be affected by sample quality
    - Limited to quantitative assessment only
    
    Clinical Limitations:
    - Does not assess platelet function
    - May not predict hemostatic effectiveness
    - Affected by patient-specific factors
    - Normal CCI does not guarantee bleeding cessation
    
    References (Vancouver style):
    1. Davis KB, Slichter SJ, Corash L. Corrected count increment and percent platelet recovery 
       as measures of posttransfusion platelet response: problems and a solution. 
       Transfusion. 1999;39(6):586-92.
    2. Bishop JF, Matthews JP, McGrath K, Yuen K, Wolf MM, Szer J. Factors influencing 20-hour 
       increments after platelet transfusion. Transfusion. 1991;31(5):392-6.
    3. Slichter SJ, Davis K, Enright H, et al. Factors affecting posttransfusion platelet increments, 
       platelet refractoriness, and platelet transfusion intervals in thrombocytopenic patients. 
       Blood. 2005;105(10):4106-14.
    """
    
    pre_transfusion_count: int = Field(
        ...,
        ge=0,
        le=500000,
        description="Pre-transfusion platelet count measured immediately before platelet transfusion. Use automated cell counter for accuracy, avoid central line samples if possible",
        example=25000
    )
    
    post_transfusion_count: int = Field(
        ...,
        ge=0,
        le=500000,
        description="Post-transfusion platelet count measured at either 1 hour or 20 hours after transfusion completion. Timing affects interpretation threshold",
        example=75000
    )
    
    time_after_transfusion: Literal["1_hour", "20_hour"] = Field(
        ...,
        description="Time point when post-transfusion sample was collected. 1_hour (threshold >7,500) for immediate response, 20_hour (threshold >4,800) for survival assessment",
        example="1_hour"
    )
    
    patient_height: float = Field(
        ...,
        ge=48,
        le=90,
        description="Patient height in inches. Used to calculate body surface area for CCI correction. Use standing height when possible, recumbent length for bedridden patients",
        example=68.0
    )
    
    patient_weight: float = Field(
        ...,
        ge=0.5,
        le=620,
        description="Patient weight in pounds. Used with height to calculate body surface area. Use calibrated scales, consider fluid status in critically ill patients",
        example=150.0
    )
    
    platelet_unit_content: float = Field(
        ...,
        ge=0.5,
        le=500,
        description="Total platelet content in all transfused units (×10¹¹ platelets). Use unit labels when available, sum for multiple units. Standard apheresis units: 3-6 × 10¹¹",
        example=4.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pre_transfusion_count": 25000,
                "post_transfusion_count": 75000,
                "time_after_transfusion": "1_hour",
                "patient_height": 68.0,
                "patient_weight": 150.0,
                "platelet_unit_content": 4.5
            }
        }


class CalculationDetails(BaseModel):
    """Detailed calculation information for CCI assessment"""
    
    count_increment: int = Field(
        ...,
        description="Actual platelet count increase (post - pre transfusion counts)",
        example=50000
    )
    
    body_surface_area: float = Field(
        ...,
        description="Patient body surface area calculated using DuBois formula (m²)",
        example=1.72
    )
    
    platelet_dose: float = Field(
        ...,
        description="Total platelet dose transfused (×10¹¹ platelets)",
        example=4.5
    )
    
    time_point: str = Field(
        ...,
        description="Time point for assessment (1_hour or 20_hour)",
        example="1_hour"
    )
    
    threshold: int = Field(
        ...,
        description="CCI threshold value for adequate response at this time point",
        example=7500
    )
    
    response_adequate: bool = Field(
        ...,
        description="Whether the CCI indicates adequate platelet transfusion response",
        example=True
    )


class CorrectedCountIncrementResponse(BaseModel):
    """
    Response model for Corrected Count Increment (CCI) for Platelet Transfusion
    
    Provides comprehensive assessment of platelet transfusion effectiveness with clinical 
    interpretation, threshold-based analysis, and evidence-based recommendations for 
    transfusion medicine practice and patient management.
    
    CCI Assessment Framework and Clinical Interpretation:
    
    Scale Overview and Purpose:
    The CCI is a standardized measure that quantifies platelet transfusion effectiveness 
    by adjusting the observed platelet count increment for patient body surface area 
    and the number of platelets transfused. This normalization allows for objective 
    comparison of transfusion responses across patients of different sizes and with 
    varying platelet doses.
    
    Clinical Significance and Applications:
    
    Transfusion Effectiveness Assessment:
    The CCI provides an objective measure of whether a platelet transfusion achieved 
    an adequate therapeutic response, helping clinicians determine if additional 
    transfusions are needed or if alternative strategies should be considered.
    
    Platelet Refractoriness Detection:
    Consistently low CCI values across multiple transfusions can indicate platelet 
    refractoriness, a condition requiring specialized management approaches including 
    HLA-matched platelets or alternative bleeding management strategies.
    
    Quality Assurance Applications:
    Transfusion services use CCI data to monitor the effectiveness of their platelet 
    products, assess storage and handling practices, and ensure optimal patient outcomes.
    
    Scoring System and Diagnostic Framework:
    
    Time-Dependent Thresholds:
    The CCI interpretation depends on the timing of the post-transfusion sample:
    
    1-Hour Assessment (Most Common):
    - CCI >7,500: Indicates successful transfusion with adequate immediate response
    - CCI ≤7,500: Suggests poor response requiring further evaluation
    - Optimal timing for assessing immediate platelet increment
    - Most practical for routine clinical use
    
    20-Hour Assessment:
    - CCI >4,800: Indicates successful transfusion with adequate platelet survival
    - CCI ≤4,800: Suggests poor survival requiring further evaluation
    - Better reflects long-term platelet viability and function
    - Useful for research and specialized clinical applications
    
    Clinical Decision-Making Framework:
    
    Successful Transfusion Response (CCI Above Threshold):
    
    Clinical Significance:
    - Indicates adequate platelet increment for patient size and platelet dose
    - Suggests normal platelet survival and lack of major consumption
    - Predicts likely hemostatic benefit from transfusion
    - Supports continuation of standard transfusion protocols
    
    Management Recommendations:
    - Continue current transfusion strategy
    - Monitor for future transfusion needs based on clinical indications
    - Document successful response for future reference
    - Consider reducing transfusion frequency if clinically appropriate
    
    Follow-up Considerations:
    - Routine monitoring of platelet counts as clinically indicated
    - Reassess transfusion thresholds based on bleeding risk
    - Monitor for development of refractoriness over time
    
    Poor Transfusion Response (CCI At or Below Threshold):
    
    Clinical Significance:
    - Indicates inadequate platelet increment relative to dose and patient size
    - May suggest platelet refractoriness or underlying consumption
    - Requires investigation of underlying causes
    - May necessitate alternative transfusion strategies
    
    Immediate Assessment and Actions:
    - Verify accuracy of platelet counts and timing
    - Review patient's clinical status for confounding factors
    - Assess for active bleeding, fever, sepsis, or medication effects
    - Consider early repeat transfusion if bleeding risk is high
    
    Refractoriness Evaluation:
    If poor response persists across multiple transfusions:
    - Obtain HLA typing and antibody screening
    - Consider platelet crossmatching
    - Evaluate for platelet-specific antibodies
    - Assess for non-immune causes of refractoriness
    
    Alternative Management Strategies:
    - HLA-matched platelet products
    - Platelet crossmatched units
    - Alternative bleeding management approaches
    - Consideration of platelet function enhancing medications
    
    Factors Affecting CCI and Clinical Interpretation:
    
    Immune Factors:
    - HLA alloimmunization: Most common cause of refractoriness
    - Platelet-specific antibodies: Can cause rapid platelet destruction
    - ABO incompatibility: May reduce transfusion effectiveness
    - Previous pregnancy or transfusion history: Risk factors for alloimmunization
    
    Non-Immune Factors:
    - Fever and infection: Increase platelet consumption
    - Splenomegaly: Causes platelet sequestration
    - DIC and bleeding: Increase platelet consumption
    - Medications: Certain drugs can affect platelet survival
    
    Technical Factors:
    - Platelet product quality: Age and storage conditions
    - Sample timing and collection: Affects accuracy of measurements
    - Laboratory methodology: Different counters may yield varying results
    - Patient factors: Hydration status, sample site selection
    
    Quality Assurance and Implementation Guidelines:
    
    Data Collection Standards:
    - Use standardized timing for sample collection
    - Ensure accurate platelet unit content documentation
    - Verify patient anthropometric measurements
    - Document any confounding clinical factors
    
    Clinical Documentation:
    - Record CCI values in patient medical record
    - Document timing and circumstances of assessment
    - Note any factors that may affect interpretation
    - Track trends over multiple transfusions
    
    Quality Improvement Applications:
    - Monitor CCI trends across patient populations
    - Assess effectiveness of different platelet products
    - Evaluate impact of storage and handling practices
    - Guide inventory management and product selection
    
    Limitations and Clinical Considerations:
    
    Assessment Limitations:
    - CCI measures count increment only, not platelet function
    - Normal CCI does not guarantee hemostatic effectiveness
    - May be affected by concurrent medical conditions
    - Limited utility during active bleeding episodes
    
    Patient-Specific Considerations:
    - Consider individual bleeding risk and clinical status
    - Account for concurrent medications affecting hemostasis
    - Evaluate patient's overall prognosis and treatment goals
    - Balance transfusion benefits against potential risks
    
    Interpretation Context:
    - Use CCI as part of comprehensive clinical assessment
    - Consider trends over time rather than single values
    - Account for patient-specific factors affecting response
    - Integrate with other measures of hemostatic function
    
    Research and Future Directions:
    
    Clinical Research Applications:
    The CCI is used in research studies to evaluate new platelet products, storage 
    methods, and transfusion strategies, contributing to evidence-based improvements 
    in transfusion medicine practice.
    
    Emerging Technologies:
    Future developments may include point-of-care platelet function testing and 
    advanced prediction models for transfusion response, complementing traditional 
    CCI assessment.
    
    This comprehensive assessment provides clinicians with the information needed to 
    make evidence-based decisions about platelet transfusion effectiveness and guide 
    optimal patient management strategies.
    
    Reference: Davis KB, et al. Transfusion. 1999;39(6):586-92.
    """
    
    result: float = Field(
        ...,
        description="Corrected Count Increment (CCI) value indicating platelet transfusion effectiveness",
        example=19300.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CCI assessment",
        example="platelets/μL/m²/(×10¹¹ platelets)"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the CCI value with specific recommendations and contextual information for patient management",
        example="CCI of 19300.0 at 1 hour post-transfusion is above the threshold of 7,500, indicating successful platelet transfusion with adequate platelet response."
    )
    
    stage: str = Field(
        ...,
        description="Overall transfusion response classification (Successful Transfusion, Poor Response)",
        example="Successful Transfusion"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the transfusion response category",
        example="Good platelet response at 1 hour"
    )
    
    calculation_details: CalculationDetails = Field(
        ...,
        description="Detailed calculation information including intermediate values and assessment parameters"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 19300.0,
                "unit": "platelets/μL/m²/(×10¹¹ platelets)",
                "interpretation": "CCI of 19300.0 at 1 hour post-transfusion is above the threshold of 7,500, indicating successful platelet transfusion with adequate platelet response. This suggests good platelet survival and function.",
                "stage": "Successful Transfusion",
                "stage_description": "Good platelet response at 1 hour",
                "calculation_details": {
                    "count_increment": 50000,
                    "body_surface_area": 1.72,
                    "platelet_dose": 4.5,
                    "time_point": "1_hour",
                    "threshold": 7500,
                    "response_adequate": True
                }
            }
        }