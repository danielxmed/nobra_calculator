"""
Color Vision Screening (Ishihara Test) Models

Request and response models for Color Vision Screening calculation.

References (Vancouver style):
1. Ishihara S. Tests for Colour-Blindness. Tokyo: Kanehara Trading Inc; 1917.
2. Birch J. Worldwide prevalence of red-green color deficiency. J Opt Soc Am A Opt Image Sci Vis. 
   2012;29(3):313-20. doi: 10.1364/JOSAA.29.000313.
3. Dain SJ. Clinical colour vision tests. Clin Exp Optom. 2004;87(4-5):276-93. 
   doi: 10.1111/j.1444-0938.2004.tb05062.x.
4. Perera C, Chakrabarti R, Islam FM, Crowston J. The Eye Phone Study: reliability and 
   accuracy of assessing Neitz color vision with smartphone technology. Am J Ophthalmol. 
   2015;160(5):944-50.e1. doi: 10.1016/j.ajo.2015.08.014.

The Ishihara color vision test is the most widely used screening tool for detecting 
red-green color blindness. This abbreviated 14-plate version provides efficient screening 
while maintaining clinical accuracy for identifying protanomaly (red-weak) and 
deuteranomaly (green-weak) color vision defects.

Clinical Background:

Color Vision Deficiencies:
- Red-green color blindness affects approximately 8% of males and 0.5% of females
- Most common forms are protanomaly (reduced red sensitivity) and deuteranomaly (reduced green sensitivity)
- Usually congenital, X-linked recessive inheritance pattern
- Rarely affects overall visual acuity or eye health

Ishihara Test Methodology:
- Uses pseudoisochromatic plates with colored dots forming numbers or patterns
- Normal color vision allows identification of embedded numbers/patterns
- Color deficient individuals may see different numbers or no patterns
- Each eye tested independently with adequate lighting

Test Interpretation:
- Normal: 12-14 correct plates (≤2 errors)
- Possible deficiency: 8-11 correct plates (3-6 errors)
- Deficiency likely: 0-7 correct plates (≥7 errors)

Clinical Applications:
- Occupational screening (pilots, electricians, medical professionals)
- Military and transportation industry requirements
- Educational assessment and career counseling
- Acute optic neuropathy screening (optic neuritis)
- General health screening and sports physicals

Test Limitations:
- Primarily detects red-green deficiencies, not blue-yellow (tritanomaly)
- Less accurate with visual acuity below 20/100
- Reliability reduced in children under 5 years
- Lighting conditions and display calibration affect digital versions
- Screening tool only - formal assessment may be needed for diagnosis

Clinical Decision Making:
- Normal results: No further testing usually needed
- Possible deficiency: Consider repeat testing or ophthalmology referral
- Likely deficiency: Ophthalmology referral for comprehensive evaluation
- Consider occupational implications and adaptive strategies
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class ColorVisionScreeningRequest(BaseModel):
    """
    Request model for Color Vision Screening (Ishihara Test)
    
    The Ishihara color vision screening test uses pseudoisochromatic plates to detect 
    red-green color blindness. This abbreviated 14-plate version provides efficient 
    screening while maintaining clinical accuracy. Each eye is tested independently 
    to identify unilateral or bilateral color vision deficiencies.
    
    Test Administration:
    
    Preparation:
    - Ensure adequate lighting (natural daylight preferred, bright white LED acceptable)
    - Test distance of 75cm (30 inches) for physical plates
    - Correct refractive errors with glasses/contacts if needed
    - Allow time for light adaptation before testing
    
    Plate Presentation:
    - Present each plate for 3-4 seconds maximum
    - Test each eye independently, covering the other eye
    - Record patient's response for each plate (number/pattern identified)
    - Do not provide feedback during testing
    
    Scoring Method:
    - Count total number of plates correctly identified per eye
    - More than 2 incorrect plates indicates possible color vision deficiency
    - Normal color vision: 12-14 correct plates (≤2 errors)
    - Borderline: 9-11 correct plates (3-5 errors)
    - Deficiency likely: ≤8 correct plates (≥6 errors)
    
    Right Eye Assessment:
    Count the number of Ishihara plates correctly identified by the right eye out of 
    14 total plates presented. Include only clear, confident responses as correct.
    
    Scoring Guidelines:
    - Plate 1: Usually a demonstration plate (number visible to all)
    - Plates 2-14: Test plates for red-green color discrimination
    - Record exact number/pattern seen, not interpretation
    - Uncertain responses should be counted as incorrect
    
    Left Eye Assessment:
    Repeat the same 14-plate assessment for the left eye independently. Cover the 
    right eye completely during left eye testing to ensure monocular assessment.
    
    Visual Acuity Considerations:
    The test accuracy is significantly reduced when visual acuity is below 20/100. 
    Patients should wear appropriate refractive correction during testing.
    
    Impact of Poor Visual Acuity:
    - Reduced ability to discriminate fine details in plates
    - May cause false positive results
    - Consider addressing refractive errors before testing
    - Ophthalmologic evaluation recommended if acuity inadequate
    
    Age Considerations:
    
    Pediatric Testing (Ages 1-4):
    - Test reliability significantly reduced
    - Attention span and comprehension limitations
    - May require modified testing approaches
    - Consider repeat testing at age 5-6 years
    
    School Age (Ages 5-17):
    - Standard testing usually reliable
    - Important for educational and career planning
    - May identify previously unrecognized deficiencies
    
    Adult Testing (Ages 18+):
    - Highly reliable with standard methodology
    - Occupational and licensing considerations
    - Stable results expected (congenital condition)
    
    Clinical Interpretation Framework:
    
    Normal Color Vision (12-14 correct):
    - Intact red-green color discrimination
    - No occupational restrictions typically needed
    - Routine follow-up appropriate
    
    Possible Deficiency (8-11 correct):
    - Mild color discrimination difficulties
    - May affect color-critical tasks
    - Consider repeat testing or specialist referral
    
    Likely Deficiency (0-7 correct):
    - Significant red-green color vision impairment
    - Occupational counseling recommended
    - Ophthalmology referral for comprehensive evaluation
    - Adaptive strategies and accommodations may be needed
    
    Special Considerations:
    
    Occupational Screening:
    - Aviation: Strict color vision requirements
    - Transportation: Variable requirements by position
    - Medical fields: May affect certain specialties
    - Electronics/Electrical: Color-coded wire identification
    
    Educational Implications:
    - Early identification allows for educational accommodations
    - Career counseling based on color vision status
    - Adaptive technologies and techniques available
    
    Quality Assurance:
    - Consistent lighting conditions essential
    - Proper test distance and viewing angle
    - Standardized presentation timing
    - Documentation of testing conditions
    
    References (Vancouver style):
    1. Ishihara S. Tests for Colour-Blindness. Tokyo: Kanehara Trading Inc; 1917.
    2. Birch J. Worldwide prevalence of red-green color deficiency. J Opt Soc Am A Opt Image Sci Vis. 
    2012;29(3):313-20. doi: 10.1364/JOSAA.29.000313.
    3. Dain SJ. Clinical colour vision tests. Clin Exp Optom. 2004;87(4-5):276-93. 
    doi: 10.1111/j.1444-0938.2004.tb05062.x.
    """
    
    correct_plates_right_eye: int = Field(
        ...,
        ge=0,
        le=14,
        description="Number of Ishihara plates correctly identified by the right eye (out of 14 total plates). Count only clear, confident responses as correct",
        example=13
    )
    
    correct_plates_left_eye: int = Field(
        ...,
        ge=0,
        le=14,
        description="Number of Ishihara plates correctly identified by the left eye (out of 14 total plates). Test each eye independently",
        example=12
    )
    
    visual_acuity_adequate: Literal["yes", "no"] = Field(
        ...,
        description="Is visual acuity 20/100 or better in both eyes with appropriate correction? Test accuracy is significantly reduced below this threshold",
        example="yes"
    )
    
    patient_age: int = Field(
        ...,
        ge=1,
        le=120,
        description="Patient age in years. Test reliability is reduced in children under 5 years due to attention and comprehension limitations",
        example=25
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "correct_plates_right_eye": 13,
                "correct_plates_left_eye": 12,
                "visual_acuity_adequate": "yes",
                "patient_age": 25
            }
        }


class ColorVisionScreeningResponse(BaseModel):
    """
    Response model for Color Vision Screening (Ishihara Test)
    
    Provides comprehensive assessment of color vision screening results with clinical 
    interpretation, recommendations, and occupational considerations. The response 
    includes bilateral assessment, overall interpretation, and evidence-based 
    management guidance.
    
    Result Interpretation:
    
    Normal Color Vision:
    - Both eyes correctly identify 12-14 plates (≤2 errors per eye)
    - Intact red-green color discrimination ability
    - No significant occupational restrictions expected
    - Routine eye care appropriate
    
    Possible Color Vision Deficiency:
    - One or both eyes correctly identify 8-11 plates (3-6 errors)
    - Mild color discrimination difficulties possible
    - May affect performance in color-critical tasks
    - Consider repeat testing or specialist evaluation
    
    Color Vision Deficiency Likely:
    - One or both eyes correctly identify ≤7 plates (≥7 errors)
    - Significant red-green color vision impairment probable
    - Occupational limitations likely in color-critical roles
    - Ophthalmology referral recommended for definitive diagnosis
    
    Clinical Management Framework:
    
    Normal Results - Management:
    - Reassure patient of normal color vision
    - No restrictions on color-dependent activities
    - Routine eye care as appropriate for age
    - Re-screen if new symptoms or concerns arise
    
    Possible Deficiency - Management:
    - Explain potential mild color vision difficulties
    - Discuss impact on daily activities (usually minimal)
    - Consider repeat testing in 6-12 months
    - Ophthalmology referral if persistent concerns
    - Occupational counseling for color-critical careers
    
    Likely Deficiency - Management:
    - Comprehensive ophthalmologic evaluation recommended
    - Formal color vision testing (Farnsworth-Munsell 100 Hue)
    - Genetic counseling if family planning considerations
    - Occupational assessment and accommodations
    - Patient education about adaptive strategies
    
    Occupational Considerations:
    
    High Color-Dependence Occupations:
    - Commercial aviation (pilots, air traffic controllers)
    - Transportation (train operators, ship officers)
    - Electrical work (wire color coding systems)
    - Medical specialties (pathology, dermatology)
    - Military positions with color-critical tasks
    
    Moderate Color-Dependence:
    - Graphic design and visual arts
    - Laboratory work (colorimetric assays)
    - Quality control in manufacturing
    - Emergency services (signal recognition)
    - Photography and printing industries
    
    Accommodations and Adaptations:
    - Digital color identification tools and apps
    - Enhanced lighting for color discrimination
    - Pattern and shape recognition training
    - Color-labeling systems and mnemonics
    - Colleague assistance for color-critical tasks
    
    Patient Education Points:
    
    Nature of Condition:
    - Usually congenital and stable throughout life
    - Does not affect overall visual acuity or eye health
    - X-linked inheritance pattern (more common in males)
    - Cannot be corrected with glasses or surgery
    
    Daily Life Impact:
    - Most activities unaffected or minimally impacted
    - Difficulty distinguishing certain red-green combinations
    - Traffic lights recognizable by position and brightness
    - Clothing coordination may require assistance
    
    Coping Strategies:
    - Learn alternative cues (brightness, position, texture)
    - Use technology aids when available
    - Inform colleagues/supervisors in relevant situations
    - Seek accommodations when legally entitled
    
    Follow-up Recommendations:
    
    Normal Results:
    - Routine eye care as appropriate for age
    - Re-screen if new visual symptoms develop
    - No specific follow-up for color vision needed
    
    Abnormal Results:
    - Ophthalmology referral for comprehensive assessment
    - Consider formal color vision testing
    - Occupational counseling if career implications
    - Genetic counseling for family planning
    - Annual reassessment if occupationally relevant
    
    Quality Assurance Considerations:
    
    Test Validity Factors:
    - Adequate visual acuity essential for accuracy
    - Proper lighting conditions required
    - Patient attention and cooperation important
    - Standardized presentation methodology
    
    Result Reliability:
    - High reliability in adults with good visual acuity
    - Reduced reliability in young children (<5 years)
    - Consider repeat testing if results unexpected
    - Document testing conditions and limitations
    
    Documentation Requirements:
    - Record exact scores for each eye
    - Note visual acuity status and corrections used
    - Document testing conditions and patient cooperation
    - Include recommendations and referrals made
    
    Reference: Dain SJ. Clin Exp Optom. 2004;87(4-5):276-93.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive color vision screening assessment including bilateral results, clinical recommendations, and test performance data",
        example={
            "right_eye": {
                "eye": "Right",
                "correct_plates": 13,
                "incorrect_plates": 1,
                "total_plates": 14,
                "accuracy_percentage": 92.9,
                "status": "Normal",
                "risk_level": "Low",
                "description": "Normal color vision",
                "clinical_significance": "No color vision deficiency detected"
            },
            "left_eye": {
                "eye": "Left",
                "correct_plates": 12,
                "incorrect_plates": 2,
                "total_plates": 14,
                "accuracy_percentage": 85.7,
                "status": "Normal",
                "risk_level": "Low",
                "description": "Normal color vision",
                "clinical_significance": "No color vision deficiency detected"
            },
            "overall_assessment": {
                "stage": "Normal",
                "description": "Normal color vision both eyes",
                "interpretation": "Both eyes demonstrate normal color vision (>12/14 plates correct with ≤2 errors). No further color vision testing indicated unless clinical suspicion remains high.",
                "recommendation": "No additional color vision testing needed",
                "bilateral_status": "Right: Normal, Left: Normal"
            },
            "clinical_recommendations": {
                "primary_recommendation": "No additional color vision testing needed",
                "follow_up_actions": ["Routine eye care as appropriate for age"],
                "patient_counseling": ["Normal color vision confirmed"],
                "occupational_considerations": []
            },
            "test_performance": {
                "sensitivity": "92%",
                "specificity": "100%",
                "applicable_deficiencies": "Red-green color vision defects (protanomaly, deuteranomaly)"
            },
            "test_limitations": {
                "general_limitations": [
                    "Screening test only - not definitive diagnosis",
                    "Primarily detects red-green color deficiencies",
                    "Does not reliably detect blue-yellow (tritanomaly) defects",
                    "Results may vary with lighting conditions and display calibration"
                ],
                "patient_specific_warnings": [],
                "test_reliability": "High"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="assessment"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with screening results and evidence-based recommendations",
        example="Both eyes demonstrate normal color vision (>12/14 plates correct with ≤2 errors). No further color vision testing indicated unless clinical suspicion remains high."
    )
    
    stage: str = Field(
        ...,
        description="Overall color vision status classification (Normal, Possible Deficiency, Color Vision Deficiency)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the color vision status",
        example="Normal color vision both eyes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "right_eye": {
                        "eye": "Right",
                        "correct_plates": 13,
                        "incorrect_plates": 1,
                        "total_plates": 14,
                        "accuracy_percentage": 92.9,
                        "status": "Normal",
                        "risk_level": "Low",
                        "description": "Normal color vision",
                        "clinical_significance": "No color vision deficiency detected"
                    },
                    "left_eye": {
                        "eye": "Left",
                        "correct_plates": 12,
                        "incorrect_plates": 2,
                        "total_plates": 14,
                        "accuracy_percentage": 85.7,
                        "status": "Normal",
                        "risk_level": "Low",
                        "description": "Normal color vision",
                        "clinical_significance": "No color vision deficiency detected"
                    },
                    "overall_assessment": {
                        "stage": "Normal",
                        "description": "Normal color vision both eyes",
                        "interpretation": "Both eyes demonstrate normal color vision (>12/14 plates correct with ≤2 errors). No further color vision testing indicated unless clinical suspicion remains high.",
                        "recommendation": "No additional color vision testing needed",
                        "bilateral_status": "Right: Normal, Left: Normal"
                    },
                    "clinical_recommendations": {
                        "primary_recommendation": "No additional color vision testing needed",
                        "follow_up_actions": ["Routine eye care as appropriate for age"],
                        "patient_counseling": ["Normal color vision confirmed"],
                        "occupational_considerations": []
                    },
                    "test_performance": {
                        "sensitivity": "92%",
                        "specificity": "100%",
                        "applicable_deficiencies": "Red-green color vision defects (protanomaly, deuteranomaly)"
                    },
                    "test_limitations": {
                        "general_limitations": [
                            "Screening test only - not definitive diagnosis",
                            "Primarily detects red-green color deficiencies",
                            "Does not reliably detect blue-yellow (tritanomaly) defects",
                            "Results may vary with lighting conditions and display calibration"
                        ],
                        "patient_specific_warnings": [],
                        "test_reliability": "High"
                    }
                },
                "unit": "assessment",
                "interpretation": "Both eyes demonstrate normal color vision (>12/14 plates correct with ≤2 errors). No further color vision testing indicated unless clinical suspicion remains high.",
                "stage": "Normal",
                "stage_description": "Normal color vision both eyes"
            }
        }