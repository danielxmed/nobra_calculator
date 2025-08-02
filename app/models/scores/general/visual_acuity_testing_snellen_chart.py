"""
Visual Acuity Testing (Snellen Chart) Models

Request and response models for Visual Acuity Testing (Snellen Chart) calculation.

References (Vancouver style):
1. Snellen H. Probebuchstaben zur Bestimmung der Sehschärfe. Utrecht: Van de Weijer; 1862.
2. Elliott DB. The good (logMAR), the bad (Snellen) and the ugly (BCVA, number of 
   letters read) of visual acuity measurement. Ophthalmic Physiol Opt. 2016;36(4):355-358. 
   doi: 10.1111/opo.12310
3. Flaxman SR, Bourne RRA, Resnikoff S, et al. Global causes of blindness and distance 
   vision impairment 1990-2020: a systematic review and meta-analysis. Lancet Glob Health. 
   2017;5(12):e1221-e1234. doi: 10.1016/S2214-109X(17)30393-5
4. Bailey IL, Lovie JE. New design principles for visual acuity letter charts. 
   Am J Optom Physiol Opt. 1976;53(11):740-745. doi: 10.1097/00006324-197611000-00006

Visual Acuity Testing (Snellen Chart) assesses binocular and monocular visual acuity 
using standardized Snellen optotypes. This test evaluates the clarity of vision by 
determining the smallest line of letters a patient can accurately read on a standardized 
chart at a specific distance.

The Snellen chart was developed by Dutch ophthalmologist Herman Snellen in 1862 and 
remains the gold standard for visual acuity assessment in clinical practice. The test 
is fundamental for:
- Ophthalmologic examinations
- Neurologic assessments (cranial nerve II evaluation)
- Screening for visual impairment
- Monitoring treatment response
- Legal determination of visual disability

Standard Snellen Chart Lines and Corresponding Visual Acuity:
- Line 1: 20/200 (legally blind threshold in US)
- Line 2: 20/160
- Line 3: 20/125
- Line 4: 20/100
- Line 5: 20/80
- Line 6: 20/63
- Line 7: 20/50
- Line 8: 20/40
- Line 9: 20/32
- Line 10: 20/25
- Line 11: 20/20 (normal vision)

For patients unable to read any letters, sequential testing includes:
- Counting Fingers (CF)
- Hand Motion (HM)
- Light Perception (LP)
- No Light Perception (NLP)

Clinical significance:
- Visual acuity 20/20: Normal vision
- Visual acuity 20/25-20/40: Mild impairment, may need correction
- Visual acuity 20/50-20/100: Moderate impairment affecting daily activities
- Visual acuity 20/125-20/200: Severe impairment approaching legal blindness
- Visual acuity worse than 20/200: Legal blindness in United States
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, List


class VisualAcuityTestingSnellenChartRequest(BaseModel):
    """
    Request model for Visual Acuity Testing (Snellen Chart)
    
    The Snellen chart test assesses visual acuity by determining the smallest line 
    of standardized letters (optotypes) that a patient can read accurately at a 
    specified distance. This test is fundamental for evaluating visual function 
    and detecting visual impairment.
    
    Testing procedure:
    1. Position patient at appropriate distance (20 feet/6 meters standard)
    2. Test each eye independently with opposite eye covered
    3. Ensure proper lighting and patient cooperation
    4. Record smallest line read correctly (≥50% of letters on line)
    5. Note whether corrective lenses were worn during testing
    
    Eye selection:
    - right_eye: Test right eye only (left eye covered)
    - left_eye: Test left eye only (right eye covered)  
    - both_eyes: Test both eyes together (binocular vision)
    
    Snellen chart lines (smallest readable line):
    - line_1_20_200: Largest letters (20/200 vision)
    - line_2_20_160 through line_11_20_20: Progressively smaller letters
    - line_11_20_20: Smallest letters (normal 20/20 vision)
    
    For patients unable to read letters:
    - counting_fingers: Can count fingers at close range
    - hand_motion: Can detect hand movement only
    - light_perception: Can perceive light but not form
    - no_light_perception: Complete blindness
    
    Testing distance options:
    - 20_feet: Standard US testing distance (20 feet)
    - 6_meters: Standard metric testing distance (equivalent to 20 feet)
    - 4_feet_mobile: Mobile device testing (less accurate, screening only)
    
    Corrective lens considerations:
    - Test with patient's usual correction if worn for distance
    - Presbyopes over 40 may need reading glasses removed for distance testing
    - Document whether lenses were worn during testing
    
    Clinical applications:
    - Routine vision screening
    - Ophthalmologic examination
    - Neurologic assessment (cranial nerve II)
    - Pre-operative evaluation
    - Occupational health screening
    - Legal/disability determination
    
    References (Vancouver style):
    1. Snellen H. Probebuchstaben zur Bestimmung der Sehschärfe. Utrecht: Van de Weijer; 1862.
    2. Elliott DB. The good (logMAR), the bad (Snellen) and the ugly (BCVA, number of 
    letters read) of visual acuity measurement. Ophthalmic Physiol Opt. 2016;36(4):355-358.
    3. Bailey IL, Lovie JE. New design principles for visual acuity letter charts. 
    Am J Optom Physiol Opt. 1976;53(11):740-745.
    """
    
    eye_tested: Literal["right_eye", "left_eye", "both_eyes"] = Field(
        ...,
        description="Which eye is being tested. Test each eye independently for accurate assessment of monocular vision",
        example="right_eye"
    )
    
    lowest_line_read: Literal[
        "line_1_20_200", "line_2_20_160", "line_3_20_125", "line_4_20_100",
        "line_5_20_80", "line_6_20_63", "line_7_20_50", "line_8_20_40",
        "line_9_20_32", "line_10_20_25", "line_11_20_20", "counting_fingers",
        "hand_motion", "light_perception", "no_light_perception"
    ] = Field(
        ...,
        description="The lowest (smallest) line that the patient can read correctly on the Snellen chart. If unable to read letters, test counting fingers, hand motion, light perception, and no light perception sequentially",
        example="line_10_20_25"
    )
    
    testing_distance: Literal["20_feet", "6_meters", "4_feet_mobile"] = Field(
        ...,
        description="Distance at which the test was performed. Standard distances are 20 feet (US) or 6 meters (metric). Mobile testing at 4 feet is less accurate",
        example="20_feet"
    )
    
    corrective_lenses: Literal["yes", "no", "unknown"] = Field(
        ...,
        description="Whether the patient was wearing their usual distance corrective lenses during testing. Important for determining corrected vs uncorrected visual acuity",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "eye_tested": "right_eye",
                "lowest_line_read": "line_10_20_25",
                "testing_distance": "20_feet",
                "corrective_lenses": "yes"
            }
        }


class VisualAcuityTestingSnellenChartResponse(BaseModel):
    """
    Response model for Visual Acuity Testing (Snellen Chart)
    
    Returns the visual acuity measurement with clinical interpretation and recommendations
    for follow-up care based on the level of visual impairment detected.
    
    Visual acuity interpretation:
    - 20/20: Normal vision - can read at 20 feet what normal eye reads at 20 feet
    - 20/25-20/40: Mild impairment - may need corrective lenses or early disease
    - 20/50-20/100: Moderate impairment - affects daily activities, needs evaluation
    - 20/125-20/200: Severe impairment - approaching legal blindness threshold
    - 20/200 or worse: Legally blind in United States
    - CF/HM/LP/NLP: Profound impairment requiring immediate evaluation
    
    Clinical categories:
    1. Normal (20/20): Routine eye care sufficient
    2. Mild Impairment (20/25-20/40): Ophthalmologic evaluation within 6 months
    3. Moderate Impairment (20/50-20/100): Evaluation within 3 months
    4. Severe Impairment (20/125-20/200): Urgent evaluation within 1-2 weeks
    5. Profound Impairment (worse than 20/200): Immediate evaluation required
    
    Detailed assessment provides:
    - Decimal equivalent for numerical comparison
    - Clinical significance and implications
    - Follow-up recommendations based on severity
    - Legal blindness status determination
    - Testing method validation notes
    
    Important considerations:
    - Mobile testing is less accurate than standard chart testing
    - Sudden vision changes require urgent evaluation regardless of level
    - Corrected vs uncorrected acuity affects treatment recommendations
    - Age-related presbyopia may affect testing in patients over 40
    
    Reference: Elliott DB. Ophthalmic Physiol Opt. 2016;36(4):355-358.
    """
    
    result: str = Field(
        ...,
        description="Visual acuity measurement in standard Snellen notation (e.g., 20/25) or descriptive notation (CF, HM, LP, NLP)",
        example="20/25"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for visual acuity",
        example="fraction"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations for follow-up care and management based on visual acuity level",
        example="Visual acuity of 20/25 in the right eye indicates mild visual impairment with correction. Ophthalmologic evaluation recommended to determine need for corrective lenses or rule out early eye disease."
    )
    
    stage: str = Field(
        ...,
        description="Visual impairment category (Normal, Mild Impairment, Moderate Impairment, Severe Impairment, Profound Impairment)",
        example="Mild Impairment"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the visual impairment category",
        example="Mild visual impairment"
    )
    
    detailed_assessment: Dict = Field(
        ...,
        description="Comprehensive assessment including decimal equivalent, clinical significance, and follow-up recommendations",
        example={
            "measured_acuity": "20/25",
            "final_acuity": "20/25",
            "decimal_equivalent": 0.8,
            "eye_tested": "Right Eye",
            "testing_method": "Standard Snellen chart at 20 feet",
            "corrective_lenses_worn": "yes",
            "clinical_significance": [
                "Mild reduction in visual acuity",
                "May benefit from corrective lenses"
            ],
            "legal_blindness_criteria": False,
            "recommendations": [
                "Ophthalmologic evaluation within 6 months",
                "Consider refractive evaluation"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "20/25",
                "unit": "fraction",
                "interpretation": "Visual acuity of 20/25 in the right eye indicates mild visual impairment with correction. Ophthalmologic evaluation recommended to determine need for corrective lenses or rule out early eye disease.",
                "stage": "Mild Impairment",
                "stage_description": "Mild visual impairment",
                "detailed_assessment": {
                    "measured_acuity": "20/25",
                    "final_acuity": "20/25",
                    "decimal_equivalent": 0.8,
                    "eye_tested": "Right Eye",
                    "testing_method": "Standard Snellen chart at 20 feet",
                    "corrective_lenses_worn": "yes",
                    "clinical_significance": [
                        "Mild reduction in visual acuity"
                    ],
                    "legal_blindness_criteria": False,
                    "recommendations": [
                        "Ophthalmologic evaluation within 6 months",
                        "Confirm corrective lens status"
                    ]
                }
            }
        }