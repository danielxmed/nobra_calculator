"""
Modified Mallampati Classification Models

Request and response models for Modified Mallampati Classification assessment of airway difficulty.

References (Vancouver style):
1. Mallampati SR, Gatt SP, Gugino LD, Desai SP, Waraksa B, Freiberger D, Liu PL. 
   A clinical sign to predict difficult tracheal intubation: a prospective study. 
   Can Anaesth Soc J. 1985 Jul;32(4):429-34. doi: 10.1007/BF03011357.
2. Samsoon GL, Young JR. Difficult tracheal intubation: a retrospective study. 
   Anaesthesia. 1987 May;42(5):487-90. doi: 10.1111/j.1365-2044.1987.tb04039.x.
3. Lee A, Fan LT, Gin T, Karmakar MK, Ngan Kee WD. A systematic review 
   (meta-analysis) of the accuracy of the Mallampati tests to predict the difficult 
   airway. Anesth Analg. 2006 Jun;102(6):1867-78. doi: 10.1213/01.ane.0000217211.12232.ea.

The Modified Mallampati Classification is a widely used bedside test for predicting 
difficult intubation based on the visibility of oropharyngeal structures. The 
modified version adds Class IV to the original 3-class system, providing better 
discrimination for severely difficult airways.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedMallampatiClassificationRequest(BaseModel):
    """
    Request model for Modified Mallampati Classification
    
    The Modified Mallampati Classification assesses airway difficulty through visual examination:
    
    **Assessment Technique:**
    - Patient positioned seated upright
    - Patient opens mouth maximally and protrudes tongue fully
    - Examination performed without phonation (patient should not say "ah")
    - Classify based on visible oropharyngeal structures
    
    **Classification System:**
    
    **Class I**: Faucial pillars, soft palate, and uvula visualized
    - All major oropharyngeal structures clearly visible
    - Easy intubation predicted
    - Low risk of difficult laryngoscopy
    - Standard direct laryngoscopy typically successful
    
    **Class II**: Faucial pillars and soft palate visualized, uvula masked by tongue base
    - Partial visualization of structures
    - Uvula obscured by tongue base
    - Mild increase in intubation difficulty
    - Standard laryngoscopy usually successful with slight increase in laryngoscopy grade
    
    **Class III**: Only soft palate visualized
    - Faucial pillars and uvula not visible
    - Base of uvula may be partially visible
    - Moderate difficulty predicted
    - Increased risk of poor laryngoscopic view
    - Consider alternative intubation strategies
    
    **Class IV**: Only hard palate visualized
    - Soft palate not visible
    - Most restricted view of oropharyngeal structures
    - High risk of difficult intubation
    - Likely poor or impossible laryngoscopic view
    - Alternative airway management strongly recommended
    
    **Clinical Context:**
    - Should be part of comprehensive airway assessment
    - Consider additional factors: neck mobility, mouth opening, thyromental distance
    - Mnemonic "PUSH": Pillars, Uvula, Soft palate, Hard palate (Class I has all)
    
    **Limitations:**
    - Sensitivity 0.51, specificity 0.87 for predicting difficult intubation
    - Should not be used in isolation for airway management decisions
    - Inter-observer variability exists, especially between Classes II and III
    - Does not account for other anatomical factors affecting intubation
    
    **Additional Applications:**
    - Sleep apnea risk assessment (Classes III-IV associated with higher OSA risk)
    - Procedural sedation risk stratification
    - Pre-operative anesthetic planning
    
    References (Vancouver style):
    1. Mallampati SR, Gatt SP, Gugino LD, Desai SP, Waraksa B, Freiberger D, Liu PL. 
       A clinical sign to predict difficult tracheal intubation: a prospective study. 
       Can Anaesth Soc J. 1985 Jul;32(4):429-34.
    2. Samsoon GL, Young JR. Difficult tracheal intubation: a retrospective study. 
       Anaesthesia. 1987 May;42(5):487-90.
    """
    
    visible_structures: Literal["class_1", "class_2", "class_3", "class_4"] = Field(
        ...,
        description="Oropharyngeal structures visible with mouth open and tongue protruded. Class 1: faucial pillars + soft palate + uvula, Class 2: faucial pillars + soft palate (uvula masked), Class 3: soft palate only, Class 4: hard palate only",
        example="class_2"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "visible_structures": "class_2"
            }
        }


class ModifiedMallampatiClassificationResponse(BaseModel):
    """
    Response model for Modified Mallampati Classification
    
    The Modified Mallampati Classification stratifies intubation difficulty:
    
    **Class I (Easy Intubation):**
    - Faucial pillars, soft palate, and uvula all visible
    - Low risk of difficult intubation
    - Standard direct laryngoscopy typically successful
    - No special airway preparation usually required
    
    **Class II (Mild Difficulty):**
    - Faucial pillars and soft palate visible, uvula masked
    - Slightly increased intubation difficulty
    - Standard laryngoscopy usually successful
    - Consider having backup airway devices available
    
    **Class III (Moderate Difficulty):**
    - Only soft palate visualized
    - Moderately difficult intubation predicted
    - Increased risk of poor laryngoscopic view
    - Consider video laryngoscopy, stylet, or bougie
    - Have rescue airway devices readily available
    
    **Class IV (Severe Difficulty):**
    - Only hard palate visible
    - High risk of difficult intubation
    - Likely poor or impossible laryngoscopic view
    - Consider awake fiber-optic intubation or video laryngoscopy
    - Prepare for potential surgical airway
    
    **Management Recommendations by Class:**
    
    **Classes I-II (Low-Moderate Risk):**
    - Standard direct laryngoscopy appropriate
    - Basic airway equipment sufficient
    - Routine pre-oxygenation and positioning
    
    **Classes III-IV (High Risk):**
    - Consider alternative intubation techniques
    - Video laryngoscopy, fiber-optic intubation, or awake intubation
    - Involve experienced airway specialist if available
    - Prepare rescue airway devices (LMA, cricothyrotomy kit)
    - Consider surgical airway backup plan
    
    **Additional Considerations:**
    - Assess other difficult airway predictors (neck mobility, mouth opening, BMI)
    - Consider patient positioning optimization
    - Ensure adequate muscle relaxation if using neuromuscular blocking agents
    - Have multiple intubation attempts strategy prepared
    
    **Limitations and Cautions:**
    - Not 100% predictive - easy Mallampati can still have difficult intubation
    - Should be combined with clinical judgment and other airway assessments
    - Patient cooperation and positioning affect accuracy
    - Consider emergency vs elective setting differences
    
    Reference: Mallampati SR, et al. Can Anaesth Soc J. 1985;32(4):429-34.
    """
    
    result: int = Field(
        ...,
        ge=1,
        le=4,
        description="Modified Mallampati class indicating predicted intubation difficulty (1-4)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="class"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with intubation difficulty prediction and airway management recommendations based on Mallampati class",
        example="Modified Mallampati Class 2: Faucial pillars and soft palate are visualized, but the uvula is masked by the tongue base. This suggests mildly increased intubation difficulty compared to Class I. Standard laryngoscopy should still be successful in most cases, but consider having backup airway devices available. Slight increase in laryngoscopy grade possible."
    )
    
    stage: str = Field(
        ...,
        description="Mallampati class designation (Class I-IV)",
        example="Class II"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of predicted intubation difficulty",
        example="Mild difficulty possible"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "class",
                "interpretation": "Modified Mallampati Class 2: Faucial pillars and soft palate are visualized, but the uvula is masked by the tongue base. This suggests mildly increased intubation difficulty compared to Class I. Standard laryngoscopy should still be successful in most cases, but consider having backup airway devices available. Slight increase in laryngoscopy grade possible.",
                "stage": "Class II",
                "stage_description": "Mild difficulty possible"
            }
        }