"""
Eat, Sleep, Console (ESC) Models

Request and response models for Eat, Sleep, Console assessment.

References (Vancouver style):
1. Grossman MR, Berkwitt AK, Osborn RR, Xu Y, Esserman DA, Shapiro ED, et al. 
   An Initiative to Improve the Quality of Care of Infants with Neonatal Abstinence 
   Syndrome. Pediatrics. 2017;139(6):e20163360. doi: 10.1542/peds.2016-3360.
2. Grossman MR, Lipshaw MJ, Osborn RR, Berkwitt AK. A Novel Approach to Assessing 
   Infants with Neonatal Abstinence Syndrome. Hosp Pediatr. 2018;8(1):1-6. 
   doi: 10.1542/hpeds.2017-0128.
3. Young LW, Hu D, Grossman M, Clark M, Sharma J, Hudak ML, et al. Eat, Sleep, 
   Console Approach or Usual Care for Neonatal Opioid Withdrawal. N Engl J Med. 
   2023;388(25):2326-2337. doi: 10.1056/NEJMoa2214470.

The Eat, Sleep, Console (ESC) approach is a function-based care model for managing 
neonatal abstinence syndrome (NAS) or neonatal opioid withdrawal syndrome (NOWS). 
Unlike traditional symptom-based scoring systems (like Finnegan), ESC focuses on 
whether infants can perform three essential functions with nonpharmacologic support, 
emphasizing family-centered care and reducing unnecessary medication use.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EatSleepConsoleRequest(BaseModel):
    """
    Request model for Eat, Sleep, Console (ESC) Assessment
    
    The ESC approach evaluates three essential infant functions to determine if 
    nonpharmacologic interventions are sufficient or if pharmacologic treatment 
    is needed for neonatal abstinence syndrome management:
    
    1. EAT - Adequate Nutritional Intake:
    - Formula-fed infants: Taking ≥1 oz per kg per feeding
    - Breastfed infants: Effective breastfeeding for ≥10 minutes
    - Assessment includes: latching ability, sucking coordination, intake volume
    - Signs of adequate eating: appropriate weight gain, satisfying feedings
    
    2. SLEEP - Restorative Rest:
    - Ability to sleep ≥1 hour undisturbed after routine care
    - Routine care includes: feeding, diaper change, vital signs
    - Assessment considers: sleep quality, duration, ability to self-soothe
    - Environmental factors: quiet, dimly lit, minimal stimulation
    
    3. CONSOLE - Behavioral Regulation:
    - Can be consoled within 10 minutes using standard comfort measures
    - Standard comfort measures include: feeding, diaper change, swaddling, 
      holding, skin-to-skin contact, non-nutritive sucking, rhythmic movement
    - Assessment requires adequate trial of multiple comfort techniques
    - Family/caregiver involvement in consoling efforts is essential
    
    Nonpharmacologic Interventions (First-Line):
    - Breastfeeding or optimized feeding techniques
    - Skin-to-skin contact (kangaroo care)
    - Swaddling and gentle handling
    - Environmental modifications (dim lighting, quiet room)
    - Non-nutritive sucking (pacifier)
    - Rhythmic movement and gentle rocking
    - Family involvement and rooming-in
    - Consistent caregiving routines
    
    Clinical Significance:
    - Reduces hospital length of stay by 45-47% compared to traditional scoring
    - Decreases opioid treatment by approximately 30%
    - Promotes family bonding and involvement in care
    - Evidence-based approach validated in large randomized controlled trials
    - Cost-effective with improved patient/family satisfaction
    
    Assessment Timing:
    - Evaluate every 3-4 hours during awake periods
    - Allow adequate time for nonpharmacologic interventions before assessment
    - Consider infant's natural sleep-wake cycles
    - Document specific interventions attempted
    
    Decision-Making:
    - If all three functions are achieved: Continue nonpharmacologic care
    - If any function is impaired despite optimal interventions: Consider medication
    - Reassess after each pharmacologic intervention
    - Continue nonpharmacologic measures alongside medication when used
    
    Family-Centered Care:
    - Educate families on comfort measures and infant cues
    - Encourage family participation in all care activities
    - Support maternal recovery and bonding
    - Provide resources for ongoing support after discharge
    
    References (Vancouver style):
    1. Grossman MR, Berkwitt AK, Osborn RR, Xu Y, Esserman DA, Shapiro ED, et al. 
       An Initiative to Improve the Quality of Care of Infants with Neonatal Abstinence 
       Syndrome. Pediatrics. 2017;139(6):e20163360.
    2. Young LW, Hu D, Grossman M, Clark M, Sharma J, Hudak ML, et al. Eat, Sleep, 
       Console Approach or Usual Care for Neonatal Opioid Withdrawal. N Engl J Med. 
       2023;388(25):2326-2337.
    """
    
    able_to_eat: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant able to eat adequately? Formula-fed: ≥1 oz per kg per feeding. Breastfed: effective breastfeeding ≥10 minutes with good latch and milk transfer",
        example="yes"
    )
    
    able_to_sleep: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant able to sleep ≥1 hour undisturbed after routine care (feeding, diaper change, vital signs)? Assess in quiet, dimly lit environment",
        example="yes"
    )
    
    able_to_console: Literal["yes", "no"] = Field(
        ...,
        description="Can the infant be consoled within 10 minutes using standard comfort measures (feeding, diaper change, swaddling, holding, skin-to-skin, non-nutritive sucking)? Requires adequate trial of multiple techniques",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "able_to_eat": "yes",
                "able_to_sleep": "yes", 
                "able_to_console": "no"
            }
        }


class EatSleepConsoleResponse(BaseModel):
    """
    Response model for Eat, Sleep, Console (ESC) Assessment
    
    The ESC assessment provides guidance for evidence-based management of neonatal 
    abstinence syndrome with focus on functional outcomes and family-centered care:
    
    ESC Criteria Met (All Functions Achieved):
    - Management: Continue current nonpharmacologic interventions
    - Family Role: Maintain family involvement in comfort measures
    - Monitoring: Assess ESC criteria every 3-4 hours during awake periods
    - Environment: Maintain quiet, dimly lit, low-stimulation environment
    - Feeding: Continue optimized feeding approach (breast or formula)
    - Comfort: Continue skin-to-skin contact, swaddling, gentle handling
    - Goals: Support normal infant neurodevelopment and family bonding
    - Discharge Planning: Prepare family for ongoing care at home
    
    ESC Criteria Not Met (One or More Functions Impaired):
    - Management: Consider pharmacologic intervention with morphine
    - Medication Protocol: Typically morphine 0.05-0.1 mg/kg every 3-4 hours
    - Reassessment: Evaluate ESC criteria after each medication dose
    - Combination Approach: Continue nonpharmacologic interventions alongside medication
    - Family Support: Maintain family involvement despite medication need
    - Monitoring: Frequent assessment for medication effectiveness and side effects
    - Goals: Achieve functional stability with minimal medication exposure
    - Weaning: Gradual medication reduction as ESC criteria are consistently met
    
    Medication Considerations:
    - First-line: Morphine (oral solution preferred)
    - Dosing: Weight-based, typically every 3-4 hours
    - Monitoring: Respiratory status, feeding ability, neurologic response
    - Duration: Variable based on individual response and functional improvement
    - Weaning: Gradual dose reduction (typically 10-20% every 24-48 hours)
    
    Quality Improvement Outcomes:
    - 45-47% reduction in hospital length of stay
    - 30% reduction in opioid treatment requirement
    - Improved family satisfaction and bonding
    - Reduced healthcare costs
    - Enhanced staff satisfaction with care model
    
    Nonpharmacologic Intervention Optimization:
    - Environmental: Consistent caregivers, minimal stimulation, appropriate lighting
    - Feeding: Frequent small feeds, demand feeding, optimized positioning
    - Comfort: Swaddling, pacifiers, gentle movement, music/white noise
    - Family: Rooming-in, skin-to-skin contact, parental comfort measures
    - Staff: Coordinated care approach, staff education, consistent protocols
    
    Discharge Readiness:
    - Consistent achievement of ESC criteria for 24-48 hours
    - Stable vital signs and feeding pattern
    - Family competency in comfort measures
    - Appropriate weight gain trajectory
    - Follow-up arrangements established
    - Home environment assessment completed
    
    Long-term Considerations:
    - Developmental follow-up recommended
    - Family support services
    - Primary care coordination
    - Substance abuse treatment resources for mothers
    - Early intervention services if indicated
    
    Reference: Young LW, et al. N Engl J Med. 2023;388(25):2326-2337.
    """
    
    result: str = Field(
        ...,
        description="ESC assessment result indicating overall functional status",
        example="ESC Criteria Not Met"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="status"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on functional assessment",
        example="ESC criteria not met - Infant is unable to achieve adequate consoling despite optimal nonpharmacologic interventions. Consider pharmacologic intervention with morphine (typical starting dose 0.05-0.1 mg/kg every 3-4 hours). Reassess ESC criteria after each dose. Continue nonpharmacologic interventions alongside medication. Ensure family involvement in care and comfort measures. Re-evaluate environmental factors and feeding approach."
    )
    
    stage: str = Field(
        ...,
        description="ESC status category (ESC Criteria Met, ESC Criteria Not Met)",
        example="ESC Criteria Not Met"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the functional status",
        example="One or more functions impaired"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "ESC Criteria Not Met",
                "unit": "status",
                "interpretation": "ESC criteria not met - Infant is unable to achieve adequate consoling despite optimal nonpharmacologic interventions. Consider pharmacologic intervention with morphine (typical starting dose 0.05-0.1 mg/kg every 3-4 hours). Reassess ESC criteria after each dose. Continue nonpharmacologic interventions alongside medication. Ensure family involvement in care and comfort measures. Re-evaluate environmental factors and feeding approach.",
                "stage": "ESC Criteria Not Met",
                "stage_description": "One or more functions impaired"
            }
        }