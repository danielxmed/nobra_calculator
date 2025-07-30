"""
Clinical Opiate Withdrawal Scale (COWS) for Opiate Withdrawal Calculator

Quantifies severity of opiate withdrawal symptoms using 11 clinical criteria 
to guide treatment decisions and assess withdrawal progression.

References:
1. Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). 
   Journal of Psychoactive Drugs. 2003;35(2):253-259. 
   doi:10.1080/02791072.2003.10400007
2. Tompkins DA, Bigelow GE, Harrison JA, Johnson RE, Fudala PJ, Strain EC. 
   Concurrent validation of the Clinical Opiate Withdrawal Scale (COWS) and 
   single-item indices against the Clinical Institute Withdrawal Assessment 
   for Alcohol-revised (CIWA-Ar). Drug Alcohol Depend. 2009;105(1-2):154-159.
"""

from typing import Dict, Any


class CowsOpiateWithdrawalCalculator:
    """Calculator for Clinical Opiate Withdrawal Scale (COWS)"""
    
    def __init__(self):
        # Scoring criteria for each symptom
        self.PULSE_SCORES = {
            "<=80": 0,
            "81-100": 1,
            "101-120": 2,
            ">120": 4
        }
        
        self.SWEATING_SCORES = {
            "no_chills_flushing": 0,
            "subjective_chills": 1,
            "flushed_moist_face": 2,
            "beads_on_brow": 3,
            "streaming_sweat": 4
        }
        
        self.RESTLESSNESS_SCORES = {
            "sits_still": 0,
            "difficulty_sitting": 1,
            "frequent_shifting": 3,
            "unable_to_sit": 5
        }
        
        self.PUPIL_SCORES = {
            "normal_pinned": 0,
            "possibly_larger": 1,
            "moderately_dilated": 2,
            "extremely_dilated": 5
        }
        
        self.BONE_JOINT_SCORES = {
            "not_present": 0,
            "mild_diffuse": 1,
            "severe_diffuse": 2,
            "unable_to_sit_discomfort": 4
        }
        
        self.RUNNY_NOSE_SCORES = {
            "not_present": 0,
            "nasal_stuffiness": 1,
            "runny_nose_tearing": 2,
            "constant_streaming": 4
        }
        
        self.GI_UPSET_SCORES = {
            "no_symptoms": 0,
            "stomach_cramps": 1,
            "nausea_loose_stool": 2,
            "vomiting_diarrhea": 3,
            "multiple_episodes": 5
        }
        
        self.TREMOR_SCORES = {
            "no_tremor": 0,
            "barely_perceptible": 1,
            "moderate_arms_extended": 2,
            "severe_rest_tremor": 4
        }
        
        self.ANXIETY_SCORES = {
            "none": 0,
            "occasionally_anxious": 1,
            "moderately_anxious": 2,
            "extremely_anxious": 4
        }
        
        self.GOOSEFLESH_SCORES = {
            "no_piloerection": 0,
            "barely_perceptible": 1,
            "prominent_arms": 2,
            "extensive_body": 3
        }
        
        self.YAWNING_SCORES = {
            "no_yawning": 0,
            "yawning_once_twice": 1,
            "yawning_three_times": 2,
            "unable_to_conduct": 3
        }
    
    def calculate(
        self,
        resting_pulse_rate: str,
        sweating: str,
        restlessness: str,
        pupil_size: str,
        bone_joint_aches: str,
        runny_nose_tearing: str,
        gi_upset: str,
        tremor: str,
        anxiety_irritability: str,
        gooseflesh_skin: str,
        yawning: str
    ) -> Dict[str, Any]:
        """
        Calculates the COWS score for opiate withdrawal assessment
        
        Args:
            resting_pulse_rate: Pulse rate category
            sweating: Sweating severity
            restlessness: Restlessness level
            pupil_size: Pupil dilation level
            bone_joint_aches: Bone/joint pain level
            runny_nose_tearing: Rhinorrhea/tearing level
            gi_upset: GI symptoms level
            tremor: Tremor severity
            anxiety_irritability: Anxiety/irritability level
            gooseflesh_skin: Piloerection level
            yawning: Yawning frequency during assessment
            
        Returns:
            Dict with total score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            resting_pulse_rate, sweating, restlessness, pupil_size,
            bone_joint_aches, runny_nose_tearing, gi_upset, tremor,
            anxiety_irritability, gooseflesh_skin, yawning
        )
        
        # Calculate individual scores
        pulse_score = self.PULSE_SCORES[resting_pulse_rate]
        sweating_score = self.SWEATING_SCORES[sweating]
        restlessness_score = self.RESTLESSNESS_SCORES[restlessness]
        pupil_score = self.PUPIL_SCORES[pupil_size]
        bone_joint_score = self.BONE_JOINT_SCORES[bone_joint_aches]
        runny_nose_score = self.RUNNY_NOSE_SCORES[runny_nose_tearing]
        gi_score = self.GI_UPSET_SCORES[gi_upset]
        tremor_score = self.TREMOR_SCORES[tremor]
        anxiety_score = self.ANXIETY_SCORES[anxiety_irritability]
        gooseflesh_score = self.GOOSEFLESH_SCORES[gooseflesh_skin]
        yawning_score = self.YAWNING_SCORES[yawning]
        
        # Calculate total score
        total_score = (
            pulse_score + sweating_score + restlessness_score + pupil_score +
            bone_joint_score + runny_nose_score + gi_score + tremor_score +
            anxiety_score + gooseflesh_score + yawning_score
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "symptom_scores": {
                    "resting_pulse": pulse_score,
                    "sweating": sweating_score,
                    "restlessness": restlessness_score,
                    "pupil_size": pupil_score,
                    "bone_joint_aches": bone_joint_score,
                    "runny_nose_tearing": runny_nose_score,
                    "gi_upset": gi_score,
                    "tremor": tremor_score,
                    "anxiety_irritability": anxiety_score,
                    "gooseflesh_skin": gooseflesh_score,
                    "yawning": yawning_score
                },
                "treatment_recommendations": interpretation["treatment"],
                "monitoring_recommendations": interpretation["monitoring"]
            }
        }
    
    def _validate_inputs(
        self, resting_pulse_rate, sweating, restlessness, pupil_size,
        bone_joint_aches, runny_nose_tearing, gi_upset, tremor,
        anxiety_irritability, gooseflesh_skin, yawning
    ):
        """Validates input parameters"""
        
        # Check pulse rate
        if resting_pulse_rate not in self.PULSE_SCORES:
            raise ValueError(f"Invalid resting_pulse_rate: {resting_pulse_rate}")
        
        # Check sweating
        if sweating not in self.SWEATING_SCORES:
            raise ValueError(f"Invalid sweating level: {sweating}")
        
        # Check restlessness
        if restlessness not in self.RESTLESSNESS_SCORES:
            raise ValueError(f"Invalid restlessness level: {restlessness}")
        
        # Check pupil size
        if pupil_size not in self.PUPIL_SCORES:
            raise ValueError(f"Invalid pupil_size: {pupil_size}")
        
        # Check bone/joint aches
        if bone_joint_aches not in self.BONE_JOINT_SCORES:
            raise ValueError(f"Invalid bone_joint_aches: {bone_joint_aches}")
        
        # Check runny nose/tearing
        if runny_nose_tearing not in self.RUNNY_NOSE_SCORES:
            raise ValueError(f"Invalid runny_nose_tearing: {runny_nose_tearing}")
        
        # Check GI upset
        if gi_upset not in self.GI_UPSET_SCORES:
            raise ValueError(f"Invalid gi_upset: {gi_upset}")
        
        # Check tremor
        if tremor not in self.TREMOR_SCORES:
            raise ValueError(f"Invalid tremor: {tremor}")
        
        # Check anxiety/irritability
        if anxiety_irritability not in self.ANXIETY_SCORES:
            raise ValueError(f"Invalid anxiety_irritability: {anxiety_irritability}")
        
        # Check gooseflesh skin
        if gooseflesh_skin not in self.GOOSEFLESH_SCORES:
            raise ValueError(f"Invalid gooseflesh_skin: {gooseflesh_skin}")
        
        # Check yawning
        if yawning not in self.YAWNING_SCORES:
            raise ValueError(f"Invalid yawning: {yawning}")
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on COWS total score
        
        Args:
            total_score: Total COWS score (0-48)
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= 4:
            stage = "None to Minimal"
            description = "None to minimal withdrawal symptoms"
            treatment = "No withdrawal treatment necessary"
            monitoring = "Monitor for symptom development"
            
            interpretation = (
                f"COWS score of {total_score} indicates none to minimal withdrawal symptoms. "
                f"No withdrawal treatment is necessary at this time. Continue monitoring "
                f"for potential symptom development and patient comfort."
            )
            
        elif total_score <= 12:
            stage = "Mild"
            description = "Mild withdrawal symptoms"
            treatment = "Supportive care and comfort medications"
            monitoring = "Regular symptom monitoring"
            
            interpretation = (
                f"COWS score of {total_score} indicates mild withdrawal symptoms. "
                f"Consider supportive care measures including comfort medications, "
                f"hydration, and symptom-specific treatments. Monitor progression."
            )
            
        elif total_score <= 24:
            stage = "Moderate"
            description = "Moderate withdrawal symptoms"
            treatment = "Pharmacologic treatment indicated, consider buprenorphine induction"
            monitoring = "Frequent assessments and symptom management"
            
            interpretation = (
                f"COWS score of {total_score} indicates moderate withdrawal symptoms. "
                f"Pharmacologic treatment is indicated. Consider buprenorphine induction "
                f"if appropriate. Provide supportive care and frequent monitoring."
            )
            
        elif total_score <= 36:
            stage = "Moderately Severe"
            description = "Moderately severe withdrawal symptoms"
            treatment = "Medication-assisted treatment strongly recommended"
            monitoring = "Intensive monitoring and medical supervision"
            
            interpretation = (
                f"COWS score of {total_score} indicates moderately severe withdrawal symptoms. "
                f"Medication-assisted treatment (MAT) is strongly recommended. Consider "
                f"intensive outpatient or inpatient treatment with close medical supervision."
            )
            
        else:  # score >= 37
            stage = "Severe"
            description = "Severe withdrawal symptoms"
            treatment = "Immediate medical intervention and intensive treatment required"
            monitoring = "Continuous medical monitoring and immediate intervention"
            
            interpretation = (
                f"COWS score of {total_score} indicates severe withdrawal symptoms. "
                f"Immediate medical intervention is required. Consider inpatient treatment "
                f"with intensive monitoring and comprehensive medication management."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "treatment": treatment,
            "monitoring": monitoring
        }


def calculate_cows_opiate_withdrawal(
    resting_pulse_rate: str,
    sweating: str,
    restlessness: str,
    pupil_size: str,
    bone_joint_aches: str,
    runny_nose_tearing: str,
    gi_upset: str,
    tremor: str,
    anxiety_irritability: str,
    gooseflesh_skin: str,
    yawning: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CowsOpiateWithdrawalCalculator()
    return calculator.calculate(
        resting_pulse_rate=resting_pulse_rate,
        sweating=sweating,
        restlessness=restlessness,
        pupil_size=pupil_size,
        bone_joint_aches=bone_joint_aches,
        runny_nose_tearing=runny_nose_tearing,
        gi_upset=gi_upset,
        tremor=tremor,
        anxiety_irritability=anxiety_irritability,
        gooseflesh_skin=gooseflesh_skin,
        yawning=yawning
    )