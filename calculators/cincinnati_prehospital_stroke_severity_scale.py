"""
Cincinnati Prehospital Stroke Severity Scale (CP-SSS) Calculator

Predicts large vessel occlusion (LVO) and severe stroke in patients with stroke symptoms.
Designed for use by emergency medical services personnel to guide triage decisions.

References:
1. Katz BS, McMullan JT, Sucharew H, Adeoye O, Broderick JP. Design and validation of a 
   prehospital scale to predict stroke severity: the Cincinnati Prehospital Stroke 
   Severity Scale. Stroke. 2015 Jun;46(6):1508-12.
2. McMullan JT, Katz B, Broderick J, Schmit P, Sucharew H, Adeoye O. Prospective 
   prehospital evaluation of the Cincinnati stroke triage assessment tool. Prehosp 
   Emerg Care. 2017 Jan-Feb;21(1):68-75.
3. Zhao H, Coote S, Pesavento L, Churilov L, Dewey HM, Davis SM, et al. Large vessel 
   occlusion scales increase delivery to endovascular centers without excessive harm 
   from misclassifications. Stroke. 2017 Mar;48(3):568-573.
"""

from typing import Dict, Any


class CincinnatiPrehospitalStrokeSeverityScaleCalculator:
    """Calculator for Cincinnati Prehospital Stroke Severity Scale (CP-SSS)"""
    
    def __init__(self):
        # Scoring criteria for each component
        self.scoring_criteria = {
            "conjugate_gaze_deviation": {
                "yes": 2,
                "no": 0
            },
            "level_of_consciousness_questions": {
                "both_correct": 0,
                "one_correct": 1,
                "neither_correct": 2
            },
            "following_commands": {
                "both_commands": 0,
                "one_command": 1,
                "neither_command": 2
            },
            "arm_holding_ability": {
                "can_hold": 0,
                "cannot_hold": 1
            }
        }
        
        # Performance characteristics
        self.performance_metrics = {
            "sensitivity_severe_stroke": 0.89,
            "specificity_severe_stroke": 0.78,
            "auc_severe_stroke": 0.89,
            "cutpoint": 2,
            "lvo_sensitivity": 0.83,
            "lvo_specificity": 0.40
        }
    
    def calculate(
        self,
        conjugate_gaze_deviation: str,
        level_of_consciousness_questions: str,
        following_commands: str,
        arm_holding_ability: str
    ) -> Dict[str, Any]:
        """
        Calculates Cincinnati Prehospital Stroke Severity Scale score
        
        Args:
            conjugate_gaze_deviation: Presence of conjugate gaze deviation (yes/no)
            level_of_consciousness_questions: LOC questions performance (both_correct/one_correct/neither_correct)
            following_commands: Command following ability (both_commands/one_command/neither_command)
            arm_holding_ability: Arm holding ability (can_hold/cannot_hold)
            
        Returns:
            Dict with CP-SSS score, risk assessment, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(conjugate_gaze_deviation, level_of_consciousness_questions, 
                            following_commands, arm_holding_ability)
        
        # Calculate component scores
        gaze_points = self._score_conjugate_gaze(conjugate_gaze_deviation)
        loc_questions_points = self._score_loc_questions(level_of_consciousness_questions)
        commands_points = self._score_commands(following_commands)
        arm_points = self._score_arm_holding(arm_holding_ability)
        
        # Calculate total score
        total_score = gaze_points + loc_questions_points + commands_points + arm_points
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            conjugate_gaze_deviation, gaze_points,
            level_of_consciousness_questions, loc_questions_points,
            following_commands, commands_points,
            arm_holding_ability, arm_points,
            total_score
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"],
            "scoring_breakdown": scoring_breakdown
        }
    
    def _validate_inputs(self, conjugate_gaze_deviation, level_of_consciousness_questions, 
                        following_commands, arm_holding_ability):
        """Validates input parameters"""
        
        # Validate conjugate gaze deviation
        if conjugate_gaze_deviation not in ["yes", "no"]:
            raise ValueError("Conjugate gaze deviation must be 'yes' or 'no'")
        
        # Validate LOC questions
        valid_loc_options = ["both_correct", "one_correct", "neither_correct"]
        if level_of_consciousness_questions not in valid_loc_options:
            raise ValueError(f"Level of consciousness questions must be one of {valid_loc_options}")
        
        # Validate following commands
        valid_command_options = ["both_commands", "one_command", "neither_command"]
        if following_commands not in valid_command_options:
            raise ValueError(f"Following commands must be one of {valid_command_options}")
        
        # Validate arm holding ability
        if arm_holding_ability not in ["can_hold", "cannot_hold"]:
            raise ValueError("Arm holding ability must be 'can_hold' or 'cannot_hold'")
    
    def _score_conjugate_gaze(self, conjugate_gaze_deviation: str) -> int:
        """Scores conjugate gaze deviation component"""
        return self.scoring_criteria["conjugate_gaze_deviation"][conjugate_gaze_deviation]
    
    def _score_loc_questions(self, level_of_consciousness_questions: str) -> int:
        """Scores level of consciousness questions component"""
        return self.scoring_criteria["level_of_consciousness_questions"][level_of_consciousness_questions]
    
    def _score_commands(self, following_commands: str) -> int:
        """Scores following commands component"""
        return self.scoring_criteria["following_commands"][following_commands]
    
    def _score_arm_holding(self, arm_holding_ability: str) -> int:
        """Scores arm holding ability component"""
        return self.scoring_criteria["arm_holding_ability"][arm_holding_ability]
    
    def _get_risk_assessment(self, score: int) -> Dict[str, str]:
        """
        Determines risk category and clinical interpretation based on CP-SSS score
        
        Args:
            score: Total CP-SSS score (0-4)
            
        Returns:
            Dict with risk assessment and clinical recommendations
        """
        
        if score < 2:
            stage = "Low Risk"
            description = "LVO and severe stroke less likely"
            interpretation = f"CP-SSS Score {score}: Low probability of large vessel occlusion and severe stroke (NIHSS <15). Standard stroke protocol appropriate with transport to nearest stroke-capable facility."
            
        else:  # score >= 2
            stage = "High Risk"
            description = "LVO and severe stroke likely"
            interpretation = f"CP-SSS Score {score}: High probability of large vessel occlusion and severe stroke (NIHSS ≥15). Strong consideration for direct transport to comprehensive stroke center capable of endovascular thrombectomy."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, conjugate_gaze_deviation, gaze_points,
                             level_of_consciousness_questions, loc_questions_points,
                             following_commands, commands_points,
                             arm_holding_ability, arm_points, total_score) -> Dict[str, Any]:
        """Provides detailed scoring breakdown and clinical context"""
        
        # Format response descriptions
        gaze_desc = "Present" if conjugate_gaze_deviation == "yes" else "Absent"
        
        loc_mapping = {
            "both_correct": "Both questions answered correctly",
            "one_correct": "One question answered correctly",
            "neither_correct": "Neither question answered correctly"
        }
        
        commands_mapping = {
            "both_commands": "Follows both commands",
            "one_command": "Follows one command",
            "neither_command": "Follows neither command"
        }
        
        arm_desc = "Cannot hold arm up for 10 seconds" if arm_holding_ability == "cannot_hold" else "Can hold arm up for 10 seconds"
        
        breakdown = {
            "component_scores": {
                "conjugate_gaze_deviation": {
                    "finding": gaze_desc,
                    "points": gaze_points,
                    "max_points": 2,
                    "description": "Horizontal conjugate gaze deviation",
                    "clinical_significance": "Strong predictor of cortical involvement and large vessel occlusion"
                },
                "level_of_consciousness_questions": {
                    "finding": loc_mapping[level_of_consciousness_questions],
                    "points": loc_questions_points,
                    "max_points": 2,
                    "description": "Level of consciousness - questions component",
                    "clinical_significance": "Assesses alertness and cognitive function"
                },
                "following_commands": {
                    "finding": commands_mapping[following_commands],
                    "points": commands_points,
                    "max_points": 2,
                    "description": "Level of consciousness - commands component",
                    "clinical_significance": "Evaluates comprehension and motor response"
                },
                "arm_holding_ability": {
                    "finding": arm_desc,
                    "points": arm_points,
                    "max_points": 1,
                    "description": "Arm weakness assessment",
                    "clinical_significance": "Motor function indicator"
                }
            },
            "score_summary": {
                "total_score": total_score,
                "max_possible_score": 7,
                "cutpoint_threshold": 2,
                "risk_category": "High Risk" if total_score >= 2 else "Low Risk"
            },
            "performance_characteristics": {
                "severe_stroke_prediction": {
                    "sensitivity": "89% (at cutpoint ≥2)",
                    "specificity": "78% (at cutpoint ≥2)",
                    "auc": "0.89",
                    "definition": "Severe stroke defined as NIHSS ≥15"
                },
                "lvo_prediction": {
                    "sensitivity": "83% (at cutpoint ≥2)",
                    "specificity": "40% (at cutpoint ≥2)",
                    "auc": "0.67",
                    "definition": "LVO includes ICA, M1, tandem ICA+M2, or basilar occlusions"
                }
            },
            "clinical_applications": {
                "primary_use": "Prehospital triage tool for emergency medical services",
                "target_population": "Patients with acute stroke symptoms",
                "decision_support": [
                    "Direct transport to comprehensive stroke center vs. nearest facility",
                    "Early activation of stroke team and interventional services",
                    "Resource allocation and preparation for potential thrombectomy"
                ],
                "limitations": [
                    "Should not delay IV thrombolysis when indicated",
                    "Does not replace clinical judgment",
                    "Requires immediate neurological consultation",
                    "Not validated for posterior circulation strokes"
                ]
            },
            "stroke_care_pathway": {
                "low_risk_management": [
                    "Transport to nearest stroke-capable facility",
                    "Standard stroke protocol activation",
                    "IV thrombolysis evaluation if within time window",
                    "Consider transfer if large vessel occlusion identified"
                ],
                "high_risk_management": [
                    "Direct transport to comprehensive stroke center if feasible",
                    "Pre-notification of interventional team",
                    "Expedited imaging and evaluation",
                    "Parallel processing for IV thrombolysis and thrombectomy"
                ]
            }
        }
        
        return breakdown


def calculate_cincinnati_prehospital_stroke_severity_scale(
    conjugate_gaze_deviation: str,
    level_of_consciousness_questions: str,
    following_commands: str,
    arm_holding_ability: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CincinnatiPrehospitalStrokeSeverityScaleCalculator()
    return calculator.calculate(
        conjugate_gaze_deviation=conjugate_gaze_deviation,
        level_of_consciousness_questions=level_of_consciousness_questions,
        following_commands=following_commands,
        arm_holding_ability=arm_holding_ability
    )