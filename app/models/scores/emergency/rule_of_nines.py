"""
Rule of Nines Models

Request and response models for Rule of Nines calculation.

References (Vancouver style):
1. Pulaski EJ, Tennison CW. Burn therapy; a comparative study of various methods 
   of treatment; review of the literature and report of 300 cases. AMA Arch Surg. 
   1947 Dec;55(6):689-723. doi: 10.1001/archsurg.1947.01230180111007.
2. Wallace AB. The exposure treatment of burns. Lancet. 1951 Mar 17;1(6659):501-4. 
   doi: 10.1016/s0140-6736(51)91975-7.
3. Hettiaratchy S, Papini R. Initial management of a major burn: II--assessment 
   and resuscitation. BMJ. 2004 Jul 17;329(7458):101-3. doi: 10.1136/bmj.329.7458.101.
4. American Burn Association. Guidelines for the operation of burn centers. 
   J Burn Care Res. 2007 Jan-Feb;28(1):134-41. doi: 10.1097/BCR.0B013E318031AA21.

The Rule of Nines is a rapid assessment tool that estimates total body surface 
area (TBSA) burned by dividing the body into segments representing 9% (or multiples 
of 9%) of total body surface area. It helps emergency providers make critical 
decisions about fluid resuscitation, burn center transfer, and initial treatment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class RuleOfNinesRequest(BaseModel):
    """
    Request model for Rule of Nines burn assessment
    
    The Rule of Nines is a standardized method for rapidly estimating the total 
    body surface area (TBSA) affected by burns. This assessment tool is essential 
    for emergency medicine providers to make critical decisions regarding fluid 
    resuscitation, burn center transfer, and initial treatment planning.
    
    Historical Development and Clinical Significance:
    Originally developed by Pulaski and Tennison in 1947 and refined by Alexander 
    Burns Wallace in 1951, the Rule of Nines has become the standard rapid assessment 
    tool for burn evaluation worldwide. The method divides the adult human body into 
    anatomical regions that each represent approximately 9% (or multiples of 9%) 
    of the total body surface area.
    
    The clinical importance of accurate TBSA estimation cannot be overstated, as it 
    directly influences fluid resuscitation requirements, determines the need for 
    burn center transfer, guides initial treatment decisions, and provides prognostic 
    information about patient outcomes.
    
    Anatomical Basis and Body Proportion Considerations:
    
    Adult Body Proportions (Age >14 years):
    The Rule of Nines for adults is based on the anatomical proportions of a 
    standard adult body, where the following regions each represent specific 
    percentages of total body surface area:
    
    - Head and Neck: 9% (4.5% anterior face/scalp, 4.5% posterior head/neck)
    - Each Upper Extremity: 9% (entire arm including hand)
    - Anterior Torso: 18% (chest and anterior abdomen)
    - Posterior Torso: 18% (back and posterior abdomen)
    - Each Lower Extremity: 18% (entire leg including foot)
    - Genitalia/Perineum: 1%
    Total: 100%
    
    Pediatric Body Proportions (Age 1-14 years):
    Children have different body proportions compared to adults, with proportionally 
    larger heads and smaller legs. The pediatric Rule of Nines adjusts for these 
    anatomical differences:
    
    - Head and Neck: 18% (significantly larger proportion than adults)
    - Each Upper Extremity: 9% (same as adults)
    - Anterior Torso: 18% (same as adults)
    - Posterior Torso: 18% (same as adults)
    - Each Lower Extremity: 13.5% (smaller proportion than adults)
    - Genitalia/Perineum: 1%
    Total: 100%
    
    Infant Body Proportions (Age <1 year):
    Infants have even more pronounced differences in body proportions, with the 
    largest relative head size and smallest leg proportions. The same percentages 
    as pediatric patients are typically used for infants.
    
    Clinical Assessment Protocol and Methodology:
    
    Burn Depth Assessment:
    Before applying the Rule of Nines, healthcare providers must assess burn depth 
    to determine which burns should be included in TBSA calculations:
    
    - First-degree burns (superficial): Typically excluded from TBSA calculations
    - Second-degree burns (partial thickness): Included in TBSA calculations
    - Third-degree burns (full thickness): Included in TBSA calculations
    - Fourth-degree burns (deep full thickness): Included in TBSA calculations
    
    Assessment Technique:
    - Examine the patient systematically, assessing each anatomical region
    - Estimate the percentage of each body region affected by second-degree or deeper burns
    - Record findings for each region separately to maintain accuracy
    - Consider using body diagrams or burn charts for documentation
    - Account for scattered burns by estimating total area within each region
    
    Clinical Applications and Decision-Making Thresholds:
    
    Fluid Resuscitation Requirements:
    The TBSA calculation directly determines fluid resuscitation needs:
    - Adults: Burns ≥10% TBSA require formal fluid resuscitation
    - Children: Burns ≥5% TBSA require formal fluid resuscitation
    - Parkland Formula: 4 mL/kg/% TBSA of lactated Ringer's over first 24 hours
    - First half of calculated volume given in first 8 hours post-burn
    
    Burn Center Transfer Criteria:
    American Burn Association guidelines specify transfer criteria including:
    - Burns >10% TBSA in patients <10 or >50 years old
    - Burns >20% TBSA in other age groups
    - Burns involving face, hands, feet, genitalia, perineum, or major joints
    - Third-degree burns >5% TBSA in any age group
    - Electrical burns, chemical burns, or inhalation injury
    
    Severity Classification and Prognosis:
    - Minor burns (<10% TBSA): Generally manageable as outpatient
    - Moderate burns (10-19% TBSA): May require hospitalization
    - Major burns (20-29% TBSA): Require burn center care
    - Severe burns (≥30% TBSA): Life-threatening with significant mortality risk
    
    Limitations and Alternative Assessment Methods:
    
    Rule of Nines Limitations:
    - Less accurate in obese patients due to altered body proportions
    - May be imprecise for very young children despite pediatric adjustments
    - Rapid estimation tool - not as precise as detailed assessment methods
    - Assumes standard body proportions that may not apply to all patients
    
    Alternative Assessment Methods:
    
    Lund-Browder Chart:
    - More accurate than Rule of Nines, especially for children
    - Adjusts for age-specific body proportions with greater precision
    - Recommended for definitive TBSA assessment in burn centers
    - More complex to use in emergency situations
    
    Rule of Palms:
    - Patient's palm (including fingers) represents approximately 1% TBSA
    - Useful for estimating small or scattered burns
    - Can be combined with Rule of Nines for complex burn patterns
    - May overestimate burn size by 10-20% in some studies
    
    Digital Assessment Tools:
    - Smartphone applications with body mapping capabilities
    - Digital photography with burn area analysis software
    - Computer-assisted burn assessment programs
    - May reduce human error and improve consistency
    
    Special Considerations and Clinical Scenarios:
    
    Circumferential Burns:
    - Burns completely encircling an extremity or the torso
    - May cause compartment syndrome requiring emergency escharotomy
    - Requires immediate surgical consultation regardless of total TBSA
    - Monitor distal perfusion and compartment pressures closely
    
    Inhalation Injury:
    - Significantly increases morbidity and mortality independent of TBSA
    - May require increased fluid resuscitation beyond standard formulas
    - Consider early intubation and respiratory support
    - Often associated with facial burns but can occur without external burns
    
    Electrical Burns:
    - May have extensive internal tissue damage despite small skin burns
    - TBSA calculation may underestimate true injury severity
    - Require cardiac monitoring and assessment for rhabdomyolysis
    - Entry and exit wounds should be carefully documented
    
    Chemical Burns:
    - Require immediate and prolonged decontamination
    - Depth and extent of injury may evolve over time
    - Initial TBSA assessment may underestimate final burn size
    - Specific antidotes may be required for certain chemical exposures
    
    Quality Assurance and Documentation Standards:
    
    Assessment Accuracy:
    - Use standardized body diagrams for burn documentation
    - Consider second opinion assessment for large or complex burns
    - Regular training for healthcare providers on burn assessment techniques
    - Validation of assessments against more precise methods when available
    
    Documentation Requirements:
    - Record percentage of each body region affected
    - Note burn depth and characteristics for each area
    - Document time of injury and assessment
    - Include photographs when possible and appropriate
    - Specify method used for TBSA calculation (Rule of Nines, Lund-Browder, etc.)
    
    Clinical Decision Support:
    - Integration with electronic health records for automatic calculations
    - Clinical alerts for burns meeting transfer criteria
    - Fluid resuscitation calculators based on TBSA and patient weight
    - Quality metrics tracking for burn assessment accuracy
    
    The Rule of Nines remains an essential tool for rapid burn assessment in 
    emergency settings, providing critical information for immediate clinical 
    decision-making while recognizing its limitations and the need for more 
    precise assessment methods in definitive care settings.
    
    References (Vancouver style):
    1. Pulaski EJ, Tennison CW. Burn therapy; a comparative study of various methods 
       of treatment; review of the literature and report of 300 cases. AMA Arch Surg. 
       1947 Dec;55(6):689-723. doi: 10.1001/archsurg.1947.01230180111007.
    2. Wallace AB. The exposure treatment of burns. Lancet. 1951 Mar 17;1(6659):501-4. 
       doi: 10.1016/s0140-6736(51)91975-7.
    3. Hettiaratchy S, Papini R. Initial management of a major burn: II--assessment 
       and resuscitation. BMJ. 2004 Jul 17;329(7458):101-3. doi: 10.1136/bmj.329.7458.101.
    4. American Burn Association. Guidelines for the operation of burn centers. 
       J Burn Care Res. 2007 Jan-Feb;28(1):134-41. doi: 10.1097/BCR.0B013E318031AA21.
    """
    
    patient_age_group: Literal["adult", "child", "infant"] = Field(
        ...,
        description="Patient age group determining appropriate body proportion calculations. "
                   "Adult (>14 years): head 9%, legs 18% each. "
                   "Child/Infant (≤14 years): head 18%, legs 13.5% each. "
                   "Age-specific proportions account for developmental anatomy differences.",
        example="adult"
    )
    
    head_neck_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of head and neck region affected by partial or full-thickness burns. "
                   "Includes face, scalp, ears, and neck. Only second-degree or deeper burns should "
                   "be included in TBSA calculations. Represents 9% TBSA in adults, 18% in children/infants.",
        example=0.0
    )
    
    anterior_torso_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of anterior torso (chest and front abdomen) affected by partial or "
                   "full-thickness burns. Includes chest wall, breasts, and anterior abdominal wall. "
                   "Represents 18% TBSA in all age groups.",
        example=50.0
    )
    
    posterior_torso_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of posterior torso (back and posterior abdomen) affected by partial "
                   "or full-thickness burns. Includes upper back, lower back, and posterior abdominal wall. "
                   "Represents 18% TBSA in all age groups.",
        example=25.0
    )
    
    right_arm_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of right upper extremity affected by partial or full-thickness burns. "
                   "Includes entire arm from shoulder to fingertips (shoulder, upper arm, forearm, hand). "
                   "Represents 9% TBSA in all age groups.",
        example=0.0
    )
    
    left_arm_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of left upper extremity affected by partial or full-thickness burns. "
                   "Includes entire arm from shoulder to fingertips (shoulder, upper arm, forearm, hand). "
                   "Represents 9% TBSA in all age groups.",
        example=0.0
    )
    
    right_leg_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of right lower extremity affected by partial or full-thickness burns. "
                   "Includes entire leg from hip to toes (thigh, knee, lower leg, foot). "
                   "Represents 18% TBSA in adults, 13.5% in children/infants.",
        example=0.0
    )
    
    left_leg_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of left lower extremity affected by partial or full-thickness burns. "
                   "Includes entire leg from hip to toes (thigh, knee, lower leg, foot). "
                   "Represents 18% TBSA in adults, 13.5% in children/infants.",
        example=0.0
    )
    
    genitalia_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of genitalia and perineum affected by partial or full-thickness burns. "
                   "Includes external genitalia and perineal region. Represents 1% TBSA in all age groups. "
                   "Burns in this area always require specialized burn center care regardless of size.",
        example=0.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "patient_age_group": "adult",
                "head_neck_percentage": 0.0,
                "anterior_torso_percentage": 50.0,
                "posterior_torso_percentage": 25.0,
                "right_arm_percentage": 0.0,
                "left_arm_percentage": 0.0,
                "right_leg_percentage": 0.0,
                "left_leg_percentage": 0.0,
                "genitalia_percentage": 0.0
            }
        }


class RuleOfNinesResponse(BaseModel):
    """
    Response model for Rule of Nines burn assessment
    
    The Rule of Nines provides rapid estimation of total body surface area (TBSA) 
    burned, enabling critical clinical decisions about fluid resuscitation, burn 
    center transfer, and initial treatment planning. Results are categorized into 
    four severity levels with specific management recommendations for each.
    
    Clinical Severity Categories and Management Framework:
    
    Minor Burns (<10% TBSA):
    
    Clinical Characteristics:
    - Limited body surface area involvement with preserved physiologic function
    - Generally does not require formal fluid resuscitation
    - Low risk for burn shock or systemic complications
    - May be suitable for outpatient management with appropriate follow-up
    
    Management Approach:
    - Comprehensive wound assessment and cleaning
    - Appropriate topical antimicrobial therapy (silver sulfadiazine, bacitracin)
    - Pain management with oral analgesics and topical anesthetics
    - Tetanus prophylaxis based on immunization history
    - Patient and family education on wound care and signs of infection
    - Scheduled follow-up within 24-48 hours for wound assessment
    - Clear return precautions for signs of infection or complications
    
    Special Considerations for Minor Burns:
    - Burns involving face, hands, feet, genitalia, or major joints require specialist consultation
    - Chemical or electrical burns need specialized evaluation regardless of size
    - Consider social factors and ability to provide adequate home care
    - Inhalation injury possibility must be assessed and excluded
    
    Moderate Burns (10-19% TBSA):
    
    Clinical Characteristics:
    - Significant body surface area involvement requiring careful assessment
    - May require formal fluid resuscitation to prevent hypovolemic shock
    - Increased risk for complications including infection and delayed healing
    - Generally requires hospital admission for monitoring and specialized care
    
    Management Approach:
    - Establish IV access and begin fluid resuscitation if indicated
    - Calculate fluid requirements using Parkland formula: 4 mL/kg/% TBSA over 24 hours
    - Monitor urine output (goal: 0.5-1 mL/kg/hr in adults, 1-1.5 mL/kg/hr in children)
    - Serial assessment of vital signs and hemodynamic status
    - Comprehensive pain management with IV analgesics
    - Early burn center consultation for specialized care coordination
    - Nutritional assessment and support planning
    - Infection prevention measures and monitoring
    
    Transfer Considerations:
    - Early burn center consultation for optimal care coordination
    - Consider transfer if specialized burn care not available locally
    - Ensure appropriate stabilization before transfer
    - Provide detailed transfer summary including fluid resuscitation details
    
    Major Burns (20-29% TBSA):
    
    Clinical Characteristics:
    - Extensive body surface area involvement with significant physiologic impact
    - High risk for burn shock requiring aggressive fluid resuscitation
    - Substantial risk for complications including respiratory compromise
    - Requires immediate burn center care and specialized treatment
    
    Management Approach:
    - Immediate IV access with large-bore catheters (consider central access)
    - Aggressive fluid resuscitation using Parkland formula with careful monitoring
    - Continuous hemodynamic monitoring and frequent vital sign assessment
    - Indwelling urinary catheter for accurate urine output monitoring
    - Nasogastric tube placement for gastric decompression
    - Early assessment for inhalation injury and respiratory support needs
    - Comprehensive pain management with IV opioids and adjuvant medications
    - Early surgical consultation for escharotomy if circumferential burns present
    - Immediate burn center transfer for specialized multidisciplinary care
    
    Complications Monitoring:
    - Compartment syndrome in circumferential extremity burns
    - Respiratory compromise from chest wall burn eschar
    - Acute kidney injury from hypovolemia or rhabdomyolysis
    - Sepsis and multi-organ dysfunction syndrome
    - Gastrointestinal complications including stress ulceration
    
    Severe Burns (≥30% TBSA):
    
    Clinical Characteristics:
    - Life-threatening injury with high mortality risk
    - Massive physiologic derangement requiring intensive care
    - High risk for multiple organ system failure
    - Requires immediate specialized burn center care with multidisciplinary team
    
    Management Approach:
    - Immediate airway assessment and respiratory support as needed
    - Multiple large-bore IV access or central venous access
    - Massive fluid resuscitation with invasive hemodynamic monitoring
    - Early intubation consideration for airway protection and ventilatory support
    - Comprehensive monitoring including arterial line and central venous pressure
    - Early surgical intervention for life-saving procedures (escharotomy, fasciotomy)
    - Aggressive nutritional support with enteral feeding when possible
    - Infection prevention and surveillance protocols
    - Psychological support for patient and family
    
    Prognostic Considerations:
    - Mortality risk significantly increased with age and comorbidities
    - Associated injuries compound complexity and worsen prognosis
    - Early aggressive care in specialized center improves outcomes
    - Long-term rehabilitation and reconstruction planning needed
    
    Fluid Resuscitation Protocols and Monitoring:
    
    Parkland Formula Application:
    - Calculate total fluid requirement: 4 mL/kg/% TBSA burned
    - Administer first half in first 8 hours post-burn
    - Administer second half over subsequent 16 hours
    - Use lactated Ringer's solution as preferred crystalloid
    - Adjust rate based on urine output and hemodynamic response
    
    Monitoring Parameters:
    - Urine output: 0.5-1 mL/kg/hr (adults), 1-1.5 mL/kg/hr (children)
    - Mean arterial pressure >65 mmHg
    - Heart rate appropriate for age and clinical condition
    - Central venous pressure 8-12 mmHg if central access available
    - Lactate levels and base deficit for tissue perfusion assessment
    
    Burn Center Transfer Criteria and Coordination:
    
    American Burn Association Transfer Guidelines:
    - Burns >10% TBSA in patients <10 or >50 years old
    - Burns >20% TBSA in other age groups
    - Full-thickness burns >5% TBSA in any age group
    - Burns involving face, hands, feet, genitalia, perineum, or major joints
    - Chemical burns, electrical burns, or lightning injuries
    - Inhalation injury or burns with concomitant trauma
    - Patients with preexisting conditions that could complicate management
    
    Transfer Preparation:
    - Stabilize airway, breathing, and circulation before transfer
    - Establish adequate IV access and begin appropriate fluid resuscitation
    - Pain management and wound care as appropriate
    - Detailed documentation of injury mechanism, time, and initial treatment
    - Communication with receiving burn center for care coordination
    - Appropriate transport team with burn care experience when available
    
    Quality Assurance and Outcome Monitoring:
    
    Assessment Accuracy:
    - Regular validation of Rule of Nines estimates against more precise methods
    - Inter-observer reliability testing for consistent TBSA assessment
    - Correlation of initial estimates with final burn size after resuscitation
    - Documentation of factors affecting assessment accuracy
    
    Clinical Outcomes Tracking:
    - Fluid resuscitation adequacy and complications
    - Length of stay and resource utilization
    - Infection rates and antimicrobial resistance patterns
    - Functional outcomes and quality of life measures
    - Mortality and morbidity associated with different TBSA ranges
    
    Continuous Quality Improvement:
    - Regular review of burn assessment and management protocols
    - Staff education and training programs for burn care
    - Integration of new technologies and assessment methods
    - Collaboration with burn centers for optimal care coordination
    
    The Rule of Nines serves as a critical foundation for emergency burn 
    assessment, enabling rapid clinical decision-making while emphasizing 
    the importance of early specialized care for significant burn injuries.
    
    Reference: American Burn Association. J Burn Care Res. 2007;28(1):134-41.
    """
    
    result: float = Field(
        ...,
        ge=0,
        le=100,
        description="Total body surface area (TBSA) burned calculated using Rule of Nines methodology. "
                   "Expressed as percentage of total body surface area affected by partial or full-thickness burns. "
                   "Critical for determining fluid resuscitation needs, burn center transfer criteria, and prognosis.",
        example=13.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the burn assessment result",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of the Rule of Nines assessment with specific "
                   "recommendations for patient management, fluid resuscitation, burn center transfer decisions, "
                   "and monitoring protocols. Includes severity classification and evidence-based treatment guidance.",
        example="Moderate burn (13.5% TBSA) requires careful assessment for hospital admission and burn center "
                "consultation. Initiate fluid resuscitation if ≥10% TBSA. Adult patients require fluid "
                "resuscitation at ≥10% TBSA. Calculate Parkland formula: 4 mL/kg/% TBSA over 24 hours. "
                "Monitor urine output, vital signs, and pain control. Consider early burn center transfer for optimal care."
    )
    
    stage: str = Field(
        ...,
        description="Burn severity classification based on total body surface area burned",
        example="Moderate Burn"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the burn severity category and recommended management approach",
        example="Consider hospital admission and burn center consultation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 13.5,
                "unit": "%",
                "interpretation": "Moderate burn (13.5% TBSA) requires careful assessment for hospital admission and burn center consultation. Initiate fluid resuscitation if ≥10% TBSA. Adult patients require fluid resuscitation at ≥10% TBSA. Calculate Parkland formula: 4 mL/kg/% TBSA over 24 hours. Monitor urine output, vital signs, and pain control. Consider early burn center transfer for optimal care. Establish IV access and begin appropriate fluid management.",
                "stage": "Moderate Burn",
                "stage_description": "Consider hospital admission and burn center consultation"
            }
        }