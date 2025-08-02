"""
Wound Closure Classification Models

Request and response models for wound closure classification calculation.

References (Vancouver style):
1. Hollander JE, Singer AJ. Laceration management. Ann Emerg Med. 1999;34(3):356-367. 
   doi: 10.1016/s0196-0644(99)70131-9
2. Singer AJ, Hollander JE, Quinn JV. Evaluation and management of traumatic lacerations. 
   N Engl J Med. 1997;337(16):1142-1148. doi: 10.1056/NEJM199710163371607
3. Forsch RT. Essentials of skin laceration repair. Am Fam Physician. 2008;78(8):945-951
4. Quinn J, Wells G, Sutcliffe T, et al. A randomized trial comparing octylcyanoacrylate 
   tissue adhesive and sutures in the management of lacerations. JAMA. 1997;277(19):1527-1530

The Wound Closure Classification helps clinicians determine the most appropriate 
closure method for traumatic wounds based on contamination level, tissue loss, 
timing, vascularization, and anatomical location. This evidence-based classification 
system guides wound management strategies to optimize healing and minimize complications.
"""

from pydantic import BaseModel, Field
from typing import Literal, List


class WoundClosureClassificationRequest(BaseModel):
    """
    Request model for Wound Closure Classification
    
    The Wound Closure Classification evaluates wounds based on multiple clinical factors 
    to recommend the most appropriate closure method:
    
    **CLOSURE TYPES:**
    
    1. **Primary Closure:**
       - Direct surgical closure for clean wounds with minimal tissue loss
       - Ideally performed within 6-8 hours of injury
       - Can extend to 24 hours for well-vascularized wounds (especially facial)
       
    2. **Secondary Closure:**
       - Healing by secondary intention for wounds with significant tissue loss
       - Wound left open to heal through granulation tissue formation
       - Requires daily dressing changes and wound care
       
    3. **Tertiary (Delayed Primary) Closure:**
       - Delayed closure after 3-7 days of observation
       - Used for contaminated wounds requiring debridement
       - Allows assessment of wound viability before closure
    
    **ASSESSMENT PARAMETERS:**
    
    Contamination Level:
    - clean: Surgical wounds or clean lacerations with minimal bacterial load
    - contaminated: Wounds exposed to bacteria but without gross contamination
    - grossly_contaminated: Wounds contaminated with soil, feces, foreign material
    
    Tissue Loss:
    - minimal: <1cm tissue gap, edges can be approximated without tension
    - moderate: 1-3cm gap, may require some tension for approximation
    - significant: >3cm gap, cannot achieve tension-free approximation
    
    Time Since Injury:
    - Measured in hours from time of injury to presentation
    - Critical factor affecting bacterial proliferation and closure success
    - Different thresholds based on wound location and vascularization
    
    Vascularization:
    - well_vascularized: Good blood supply, rapid healing expected
    - moderately_vascularized: Adequate blood supply
    - poorly_vascularized: Limited blood supply, higher infection risk
    
    Wound Location:
    - face_scalp: Excellent blood supply, extended closure window
    - extremities: Variable blood supply depending on specific location
    - trunk: Moderate blood supply, standard closure principles apply
    - hands_feet: Specialized considerations for function and healing
    - joints: Complex closure due to movement and tension
    - other: General body areas not specifically categorized
    
    **CLINICAL CONSIDERATIONS:**
    
    Primary Closure Indications:
    - Clean wounds with minimal/moderate tissue loss
    - Presentation within appropriate time window
    - Adequate vascularization for healing
    - Patient able to maintain wound care
    
    Secondary Closure Indications:
    - Significant tissue loss preventing tension-free closure
    - Wounds where primary closure would result in poor cosmetic outcome
    - Patient unable to return for suture removal
    
    Tertiary Closure Indications:
    - Contaminated or infected wounds
    - Wounds with questionable tissue viability
    - Delayed presentation beyond primary closure window
    - Need for wound bed preparation before closure
    
    **LIMITATIONS:**
    
    - Classification has limited application in abdominal and orthopedic wounds
    - Patient-specific factors (comorbidities, medications) affect healing
    - Surgeon experience and judgment remain critical
    - Local institutional protocols may vary
    
    References (Vancouver style):
    1. Hollander JE, Singer AJ. Laceration management. Ann Emerg Med. 1999;34(3):356-367. 
    doi: 10.1016/s0196-0644(99)70131-9
    2. Singer AJ, Hollander JE, Quinn JV. Evaluation and management of traumatic lacerations. 
    N Engl J Med. 1997;337(16):1142-1148. doi: 10.1056/NEJM199710163371607
    3. Forsch RT. Essentials of skin laceration repair. Am Fam Physician. 2008;78(8):945-951
    """
    
    contamination_level: Literal["clean", "contaminated", "grossly_contaminated"] = Field(
        ...,
        description="Level of wound contamination affecting infection risk. Clean: surgical wounds/clean lacerations; Contaminated: bacterial exposure without gross contamination; Grossly contaminated: soil, feces, foreign material",
        example="clean"
    )
    
    tissue_loss: Literal["minimal", "moderate", "significant"] = Field(
        ...,
        description="Extent of tissue loss affecting ability to achieve tension-free closure. Minimal: <1cm gap; Moderate: 1-3cm gap; Significant: >3cm gap preventing tension-free approximation",
        example="minimal"
    )
    
    time_since_injury: float = Field(
        ...,
        description="Time elapsed since injury in hours. Critical factor affecting bacterial proliferation and closure success. Different thresholds apply based on wound characteristics",
        ge=0.0,
        le=168.0,
        example=4.5
    )
    
    vascularization: Literal["well_vascularized", "moderately_vascularized", "poorly_vascularized"] = Field(
        ...,
        description="Wound bed vascularization status affecting healing potential. Well: good blood supply, rapid healing; Moderate: adequate supply; Poor: limited supply, higher risk",
        example="well_vascularized"
    )
    
    wound_location: Literal["face_scalp", "extremities", "trunk", "hands_feet", "joints", "other"] = Field(
        ...,
        description="Anatomical location affecting closure options and healing. Face/scalp: excellent blood supply, extended window; Extremities: variable supply; Hands/feet: functional considerations",
        example="face_scalp"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "contamination_level": "clean",
                "tissue_loss": "minimal",
                "time_since_injury": 4.5,
                "vascularization": "well_vascularized",
                "wound_location": "face_scalp"
            }
        }


class WoundClosureClassificationResponse(BaseModel):
    """
    Response model for Wound Closure Classification
    
    The Wound Closure Classification provides evidence-based recommendations for 
    wound management strategies. Results include the recommended closure type, 
    clinical rationale, and comprehensive management guidance.
    
    **CLOSURE TYPE CATEGORIES:**
    
    1. **primary_closure**: Direct surgical closure indicated
       - Clean wounds with minimal tissue loss
       - Within appropriate time window for closure
       - Well-vascularized tissue with good healing potential
       - Management includes irrigation, debridement, and layered closure
    
    2. **secondary_closure**: Healing by secondary intention
       - Significant tissue loss preventing tension-free closure
       - Wounds where primary closure would compromise outcomes
       - Management includes daily dressing changes and moist wound environment
    
    3. **tertiary_closure**: Delayed closure after observation period
       - Contaminated wounds requiring debridement and observation
       - Delayed presentation beyond primary closure window
       - Management includes 3-7 day observation before closure attempt
    
    **CLINICAL MANAGEMENT IMPLICATIONS:**
    
    Primary Closure:
    - Thorough irrigation and debridement before closure
    - Appropriate anesthesia and suture selection
    - Layered closure for deep wounds
    - Post-procedure wound care education
    
    Secondary Closure:
    - Daily wound assessment and dressing changes
    - Moist wound environment maintenance
    - Nutritional optimization for healing
    - Monitor for infection and healing progress
    
    Tertiary Closure:
    - Immediate thorough debridement and irrigation
    - Daily wound care during observation period
    - Antibiotic prophylaxis consideration
    - Re-evaluation in 3-7 days for closure feasibility
    
    **PROGNOSTIC CONSIDERATIONS:**
    
    Healing Times:
    - Primary closure: 7-14 days for suture removal
    - Secondary closure: 2-6 weeks depending on size
    - Tertiary closure: 10-21 days (3-7 day delay + healing time)
    
    Complication Risks:
    - Primary: Low infection risk if appropriate timing
    - Secondary: Prolonged healing, larger scar
    - Tertiary: Moderate infection risk, requires observation
    
    Reference: Hollander JE, Singer AJ. Ann Emerg Med. 1999;34(3):356-367.
    """
    
    result: str = Field(
        ...,
        description="Recommended wound closure classification (primary_closure, secondary_closure, tertiary_closure)",
        example="primary_closure"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="categorical"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management strategy and rationale for the recommended closure type",
        example="PRIMARY CLOSURE recommended. Clean wound with minimal tissue loss, within ideal time window, well-vascularized wound bed. Perform thorough irrigation and debridement before closure. Consider layered closure for deep wounds."
    )
    
    stage: str = Field(
        ...,
        description="Closure type classification stage",
        example="Primary Closure"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the closure classification",
        example="Direct surgical closure indicated"
    )
    
    rationale: str = Field(
        ...,
        description="Clinical rationale explaining why this closure type was selected based on wound characteristics",
        example="Clean wound with minimal tissue loss, within ideal time window, well-vascularized wound bed"
    )
    
    recommendations: List[str] = Field(
        ...,
        description="Specific clinical management recommendations for the selected closure type",
        example=[
            "Thorough wound irrigation with normal saline",
            "Adequate anesthesia (local, regional, or systemic)",
            "Careful debridement of devitalized tissue",
            "Layered closure if deep subcutaneous involvement",
            "Appropriate suture selection based on location",
            "Post-procedure wound care instructions"
        ]
    )
    
    contraindications: List[str] = Field(
        ...,
        description="Absolute and relative contraindications for the recommended closure type",
        example=[
            "Signs of infection",
            "Grossly contaminated wound",
            "Significant tissue loss",
            "Patient unable to maintain wound care"
        ]
    )
    
    timing_guidance: str = Field(
        ...,
        description="Specific timing recommendations for the closure procedure or observation period",
        example="Closure within 24 hours optimal"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "primary_closure",
                "unit": "categorical",
                "interpretation": "PRIMARY CLOSURE recommended. Clean wound with minimal tissue loss, within ideal time window, well-vascularized wound bed. Perform thorough irrigation and debridement before closure. Consider layered closure for deep wounds.",
                "stage": "Primary Closure",
                "stage_description": "Direct surgical closure indicated",
                "rationale": "Clean wound with minimal tissue loss, within ideal time window, well-vascularized wound bed",
                "recommendations": [
                    "Thorough wound irrigation with normal saline",
                    "Adequate anesthesia (local, regional, or systemic)",
                    "Careful debridement of devitalized tissue",
                    "Layered closure if deep subcutaneous involvement",
                    "Appropriate suture selection based on location",
                    "Post-procedure wound care instructions"
                ],
                "contraindications": [
                    "Signs of infection",
                    "Grossly contaminated wound",
                    "Significant tissue loss",
                    "Patient unable to maintain wound care"
                ],
                "timing_guidance": "Closure within 24 hours optimal"
            }
        }