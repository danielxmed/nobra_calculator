"""
Modified Hoehn and Yahr Scale for Parkinson's Disease Models

Request and response models for Modified Hoehn and Yahr Scale assessment of Parkinson's disease severity.

References (Vancouver style):
1. Hoehn MM, Yahr MD. Parkinsonism: onset, progression and mortality. Neurology. 
   1967 May;17(5):427-42. doi: 10.1212/wnl.17.5.427.
2. Goetz CG, Poewe W, Rascol O, Sampaio C, Stebbins GT, Counsell C, Giladi N, 
   Holloway RG, Moore CG, Wenning GK, Yahr MD, Seidl L; Movement Disorder Society 
   Task Force on Rating Scales for Parkinson's Disease. Movement Disorder Society 
   Task Force report on the Hoehn and Yahr staging scale: Status and recommendations. 
   Mov Disord. 2004 Sep;19(9):1020-8. doi: 10.1002/mds.20213.
3. Shulman LM, Gruber-Baldini AL, Anderson KE, Fishman PS, Reich SG, Weiner WJ. 
   The clinically important difference on the unified Parkinson's disease rating scale. 
   Arch Neurol. 2010 Jan;67(1):64-70. doi: 10.1001/archneurol.2009.295.

The Modified Hoehn and Yahr Scale is the most widely used staging system for 
Parkinson's disease, providing a global measure of disease severity based on 
motor symptoms and functional disability. The modified version adds intermediate 
stages (1.5 and 2.5) to better capture disease progression.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedHoehnAndYahrScaleRequest(BaseModel):
    """
    Request model for Modified Hoehn and Yahr Scale for Parkinson's Disease
    
    The Modified Hoehn and Yahr Scale assesses Parkinson's disease severity through clinical staging:
    
    **Stage Definitions:**
    
    **Stage 1**: Unilateral involvement only
    - Signs and symptoms on one side only
    - Usually minimal or no functional disability
    - Tremor of one limb, slight loss of facial expression on one side
    - Normal posture and balance maintained
    
    **Stage 1.5**: Unilateral and axial involvement  
    - Unilateral involvement plus midline involvement (neck, trunk, spine)
    - No impairment of balance
    - Symptoms may include bradykinesia, rigidity, or tremor on one side with axial symptoms
    
    **Stage 2**: Bilateral involvement without impairment of balance
    - Signs and symptoms are bilateral
    - No impairment of balance, minimal disability
    - Posture and gait affected but patient can live independently
    - May have bilateral tremor, rigidity, or bradykinesia
    
    **Stage 2.5**: Mild bilateral disease with recovery on pull test
    - Bilateral signs and symptoms with mild postural instability
    - Patient recovers unaided on pull test (examiner pulls patient backward)
    - Physically independent but may have some balance challenges
    
    **Stage 3**: Bilateral disease; mild to moderate disability
    - Impaired postural reflexes with unsteadiness on pull test
    - Still physically independent but shows postural instability
    - May have falls and difficulty with balance
    - First stage where balance is significantly affected
    
    **Stage 4**: Severe disability; still able to walk or stand unassisted
    - Severely disabling disease but can still walk/stand unassisted
    - Markedly incapacitated with significant functional limitations
    - May require assistance with activities of daily living
    - High fall risk, may need mobility aids
    
    **Stage 5**: Confinement to bed or wheelchair unless aided
    - Complete invalidism - confined to bed or wheelchair
    - Cannot stand or walk even with assistance
    - Constant nursing care required
    - Complete dependency for all activities of daily living
    
    **Clinical Assessment Considerations:**
    - Pull test: Examiner stands behind patient and pulls backward on shoulders
    - Assess during patient's typical "on" medication state when possible
    - Consider motor fluctuations and timing of assessment
    - Stage represents overall functional capacity, not just worst symptoms
    
    **Disease Progression:**
    - Stages 1-3: Considered minimally disabling
    - Stages 4-5: Represent severe disability requiring significant support
    - Progression varies widely between individuals
    - Used for clinical decision-making about treatments and interventions
    
    References (Vancouver style):
    1. Hoehn MM, Yahr MD. Parkinsonism: onset, progression and mortality. Neurology. 
       1967 May;17(5):427-42.
    2. Goetz CG, Poewe W, Rascol O, Sampaio C, Stebbins GT, Counsell C, et al. 
       Movement Disorder Society Task Force report on the Hoehn and Yahr staging scale: 
       Status and recommendations. Mov Disord. 2004 Sep;19(9):1020-8.
    """
    
    clinical_stage: Literal["stage_1", "stage_1_5", "stage_2", "stage_2_5", "stage_3", "stage_4", "stage_5"] = Field(
        ...,
        description="Clinical stage based on motor symptoms and functional disability assessment. Select the stage that best represents the patient's overall functional capacity",
        example="stage_2_5"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clinical_stage": "stage_2_5"
            }
        }


class ModifiedHoehnAndYahrScaleResponse(BaseModel):
    """
    Response model for Modified Hoehn and Yahr Scale for Parkinson's Disease
    
    The Modified Hoehn and Yahr Scale provides staging for Parkinson's disease severity:
    
    **Stage Interpretations and Clinical Implications:**
    
    **Stage 1 (1.0)**: Unilateral involvement only
    - Early-stage disease with minimal functional impact
    - Normal activities of daily living maintained
    - Excellent prognosis for maintaining independence
    - Focus on education, exercise, and lifestyle modifications
    
    **Stage 1.5 (1.5)**: Unilateral and axial involvement
    - Progression to involve midline structures
    - Still minimal functional disability
    - Consider physical therapy for posture and mobility
    
    **Stage 2 (2.0)**: Bilateral involvement without balance impairment
    - Bilateral symptoms but balance preserved
    - May benefit from occupational therapy
    - Continue emphasis on exercise and activity
    
    **Stage 2.5 (2.5)**: Mild bilateral disease with recovery on pull test
    - First signs of balance issues but recovers independently
    - Balance training becomes important
    - Fall prevention strategies should be introduced
    
    **Stage 3 (3.0)**: Bilateral disease with postural instability
    - Significant balance impairment with fall risk
    - May require mobility aids or home modifications
    - Consider gait training and balance programs
    - Medication optimization becomes crucial
    
    **Stage 4 (4.0)**: Severe disability but can walk/stand unassisted
    - Significant functional limitations requiring assistance
    - High fall risk - safety modifications essential
    - May benefit from deep brain stimulation evaluation
    - Caregiver support becomes necessary
    
    **Stage 5 (5.0)**: Wheelchair or bed-bound unless aided
    - End-stage disease requiring constant care
    - Focus on comfort, symptom management, and quality of life
    - Palliative care considerations appropriate
    - Family support and resources crucial
    
    **Clinical Decision-Making Applications:**
    - **Medication Management**: Higher stages may require more complex regimens
    - **Surgical Considerations**: Deep brain stimulation typically considered at stages 3-4
    - **Therapy Referrals**: Physical/occupational therapy needs increase with stage
    - **Safety Planning**: Fall prevention and home modifications based on stage
    - **Prognosis Counseling**: Helps patients and families understand disease trajectory
    
    **Limitations:**
    - Focuses primarily on motor symptoms
    - Does not assess cognitive decline, mood disorders, or other non-motor features
    - Should be used alongside other comprehensive assessments (UPDRS, MoCA, etc.)
    - Inter-rater reliability can vary, especially for intermediate stages
    
    Reference: Hoehn MM, Yahr MD. Neurology. 1967;17(5):427-42.
    """
    
    result: float = Field(
        ...,
        ge=1.0,
        le=5.0,
        description="Modified Hoehn and Yahr stage indicating Parkinson's disease severity (1.0-5.0)",
        example=2.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the stage",
        example="stage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with disease severity assessment and management recommendations based on Hoehn and Yahr stage",
        example="Modified Hoehn and Yahr Stage 2.5: Mild bilateral disease with recovery on pull test. Bilateral signs and symptoms with mild postural instability. Patient recovers unaided on pull test (examiner pulls patient backward by shoulders). Physically independent but may have some balance challenges. Gait may be affected but functional independence maintained."
    )
    
    stage: str = Field(
        ...,
        description="Stage designation (Stage 1-5 with 0.5 increments)",
        example="Stage 2.5"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stage characteristics",
        example="Mild bilateral disease with recovery on pull test"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "stage",
                "interpretation": "Modified Hoehn and Yahr Stage 2.5: Mild bilateral disease with recovery on pull test. Bilateral signs and symptoms with mild postural instability. Patient recovers unaided on pull test (examiner pulls patient backward by shoulders). Physically independent but may have some balance challenges. Gait may be affected but functional independence maintained.",
                "stage": "Stage 2.5",
                "stage_description": "Mild bilateral disease with recovery on pull test"
            }
        }