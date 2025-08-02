"""
Modified Hoehn and Yahr Scale for Parkinson's Disease Calculator

Grades severity of symptoms in Parkinson's disease using the modified staging system
that includes intermediate stages (1.5 and 2.5) for better disease progression tracking.
The scale assesses motor symptoms and functional disability.

References:
1. Hoehn MM, Yahr MD. Neurology. 1967;17(5):427-42.
2. Goetz CG, et al. Mov Disord. 2004;19(9):1020-8.
3. Shulman LM, et al. Arch Neurol. 2010;67(1):64-70.
"""

from typing import Dict, Any


class ModifiedHoehnAndYahrScaleCalculator:
    """Calculator for Modified Hoehn and Yahr Scale for Parkinson's Disease"""
    
    def __init__(self):
        # Stage mappings
        self.STAGE_VALUES = {
            "stage_1": 1.0,
            "stage_1_5": 1.5,
            "stage_2": 2.0,
            "stage_2_5": 2.5,
            "stage_3": 3.0,
            "stage_4": 4.0,
            "stage_5": 5.0
        }
        
        # Stage descriptions
        self.STAGE_DESCRIPTIONS = {
            "stage_1": "Unilateral involvement only",
            "stage_1_5": "Unilateral and axial involvement",
            "stage_2": "Bilateral involvement without impairment of balance",
            "stage_2_5": "Mild bilateral disease with recovery on pull test",
            "stage_3": "Bilateral disease; mild to moderate disability",
            "stage_4": "Severe disability; still able to walk or stand unassisted",
            "stage_5": "Confinement to bed or wheelchair unless aided"
        }
    
    def calculate(self, clinical_stage: str) -> Dict[str, Any]:
        """
        Determines the Modified Hoehn and Yahr stage for Parkinson's disease
        
        Args:
            clinical_stage (str): Clinical stage based on motor symptoms and functional status
            
        Returns:
            Dict with Hoehn and Yahr stage and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(clinical_stage)
        
        # Get stage value
        stage_value = self.STAGE_VALUES[clinical_stage]
        
        # Get interpretation
        interpretation = self._get_interpretation(clinical_stage, stage_value)
        
        return {
            "result": stage_value,
            "unit": "stage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, clinical_stage: str):
        """Validates input parameters"""
        
        if clinical_stage not in self.STAGE_VALUES:
            valid_stages = ", ".join(self.STAGE_VALUES.keys())
            raise ValueError(f"clinical_stage must be one of: {valid_stages}")
    
    def _get_interpretation(self, clinical_stage: str, stage_value: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Hoehn and Yahr stage
        
        Args:
            clinical_stage: Stage identifier
            stage_value: Numeric stage value
            
        Returns:
            Dict with interpretation details
        """
        
        stage_interpretations = {
            "stage_1": {
                "stage": "Stage 1",
                "description": "Unilateral involvement only",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Unilateral involvement only. "
                                f"Signs and symptoms on one side only, usually with minimal or no functional "
                                f"disability. Tremor of one limb, slight loss of expression of one side of face. "
                                f"Symptoms are mild and do not interfere with activities of daily living. "
                                f"Patient maintains normal posture and balance.")
            },
            "stage_1_5": {
                "stage": "Stage 1.5",
                "description": "Unilateral and axial involvement",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Unilateral and axial involvement. "
                                f"Unilateral involvement plus midline involvement (neck, trunk, spine) without "
                                f"impairment of balance. Symptoms may include bradykinesia, rigidity, or tremor "
                                f"affecting one side of the body with some axial symptoms. Functional disability "
                                f"remains minimal.")
            },
            "stage_2": {
                "stage": "Stage 2",
                "description": "Bilateral involvement without impairment of balance",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Bilateral involvement without "
                                f"impairment of balance. Signs and symptoms are bilateral but without impairment "
                                f"of balance. Minimal disability. Posture and gait are affected but patient can "
                                f"still live independently. May have bilateral tremor, rigidity, or bradykinesia "
                                f"but maintains normal balance responses.")
            },
            "stage_2_5": {
                "stage": "Stage 2.5", 
                "description": "Mild bilateral disease with recovery on pull test",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Mild bilateral disease with "
                                f"recovery on pull test. Bilateral signs and symptoms with mild postural "
                                f"instability. Patient recovers unaided on pull test (examiner pulls patient "
                                f"backward by shoulders). Physically independent but may have some balance "
                                f"challenges. Gait may be affected but functional independence maintained.")
            },
            "stage_3": {
                "stage": "Stage 3",
                "description": "Bilateral disease; mild to moderate disability",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Bilateral disease with mild "
                                f"to moderate disability. Impaired postural reflexes demonstrated by unsteadiness "
                                f"on pull test. Patient is still physically independent but shows clear postural "
                                f"instability. May have falls, difficulty with balance, and some functional "
                                f"limitations but can still live independently with careful attention to safety.")
            },
            "stage_4": {
                "stage": "Stage 4",
                "description": "Severe disability; still able to walk or stand unassisted",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Severe disability, still able "
                                f"to walk or stand unassisted. Severely disabling disease but patient can still "
                                f"walk and stand unassisted, though markedly incapacitated. Significant functional "
                                f"limitations, may require assistance with activities of daily living. High fall "
                                f"risk and may need mobility aids. Consider caregiver support and safety modifications.")
            },
            "stage_5": {
                "stage": "Stage 5",
                "description": "Confinement to bed or wheelchair unless aided",
                "interpretation": (f"Modified Hoehn and Yahr Stage {stage_value}: Confinement to bed or wheelchair "
                                f"unless aided. Complete invalidism - confined to bed or wheelchair. Constant "
                                f"nursing care required. Cannot stand or walk even with assistance. Represents "
                                f"end-stage disease with complete dependency for all activities of daily living. "
                                f"Focus on comfort care, symptom management, and quality of life.")
            }
        }
        
        return stage_interpretations.get(clinical_stage, {
            "stage": f"Stage {stage_value}",
            "description": "Unknown stage",
            "interpretation": f"Unknown Modified Hoehn and Yahr stage: {stage_value}"
        })


def calculate_modified_hoehn_and_yahr_scale(clinical_stage: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedHoehnAndYahrScaleCalculator()
    return calculator.calculate(clinical_stage)