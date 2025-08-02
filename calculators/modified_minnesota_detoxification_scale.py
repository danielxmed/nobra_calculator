"""
Modified Minnesota Detoxification Scale (mMINDS) Calculator

Scores symptoms for patients with alcohol withdrawal syndrome, particularly useful 
in critically ill patients and ICU settings where subjective assessment tools like 
CIWA-Ar may not be applicable.

References:
1. Hack JB, et al. J Med Toxicol. 2006;2(2):55-60.
2. Awissi DK, et al. Crit Care Med. 2013;41(9 Suppl 1):S57-68.
3. DeCarolis DD, et al. Pharmacotherapy. 2007;27(4):510-8.
"""

from typing import Dict, Any


class ModifiedMinnesotaDetoxificationScaleCalculator:
    """Calculator for Modified Minnesota Detoxification Scale (mMINDS)"""
    
    def __init__(self):
        # Scoring mappings for each parameter
        self.PULSE_SCORES = {
            "under_90": 0,
            "90_to_110": 1,
            "over_110": 2
        }
        
        self.DBP_SCORES = {
            "under_90": 0,
            "90_to_110": 1,
            "over_110": 2
        }
        
        self.TREMOR_SCORES = {
            "absent": 0,
            "slightly_visible": 2,
            "moderate_with_arms_extended": 4,
            "severe_without_extending_arms": 6
        }
        
        self.SWEAT_SCORES = {
            "absent": 0,
            "barely_moist_palms": 2,
            "beads_visible": 4,
            "drenching": 6
        }
        
        self.HALLUCINATION_SCORES = {
            "absent": 0,
            "mild_sporadic": 1,
            "moderate_intermittent": 2,
            "severe_continuous": 3
        }
        
        self.AGITATION_SCORES = {
            "normal_sedated": 0,
            "somewhat_increased": 3,
            "moderately_fidgety": 6,
            "pacing_thrashing": 9
        }
        
        self.ORIENTATION_SCORES = {
            "oriented_x3": 0,
            "oriented_x2": 2,
            "oriented_x1": 4,
            "disoriented": 6
        }
        
        self.DELUSION_SCORES = {
            "absent_unable_to_assess": 0,
            "present": 6
        }
        
        self.SEIZURE_SCORES = {
            "not_actively_seizing": 0,
            "actively_seizing": 6
        }
    
    def calculate(self, pulse: int, diastolic_bp: int, tremor: str, sweat: str,
                  hallucinations: str, agitation: str, orientation: str,
                  delusions: str, seizures: str) -> Dict[str, Any]:
        """
        Calculates the Modified Minnesota Detoxification Scale score
        
        Args:
            pulse (int): Pulse rate in beats per minute
            diastolic_bp (int): Diastolic blood pressure in mmHg
            tremor (str): Tremor severity
            sweat (str): Diaphoresis severity
            hallucinations (str): Hallucination presence and severity
            agitation (str): Agitation level
            orientation (str): Orientation level
            delusions (str): Delusion presence
            seizures (str): Active seizure status
            
        Returns:
            Dict with mMINDS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pulse, diastolic_bp, tremor, sweat, hallucinations,
                             agitation, orientation, delusions, seizures)
        
        # Calculate pulse score
        pulse_score = self._get_pulse_score(pulse)
        
        # Calculate diastolic BP score
        dbp_score = self._get_dbp_score(diastolic_bp)
        
        # Get scores for categorical parameters
        tremor_score = self.TREMOR_SCORES[tremor]
        sweat_score = self.SWEAT_SCORES[sweat]
        hallucination_score = self.HALLUCINATION_SCORES[hallucinations]
        agitation_score = self.AGITATION_SCORES[agitation]
        orientation_score = self.ORIENTATION_SCORES[orientation]
        delusion_score = self.DELUSION_SCORES[delusions]
        seizure_score = self.SEIZURE_SCORES[seizures]
        
        # Calculate total score
        total_score = (pulse_score + dbp_score + tremor_score + sweat_score +
                      hallucination_score + agitation_score + orientation_score +
                      delusion_score + seizure_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, pulse: int, diastolic_bp: int, tremor: str,
                        sweat: str, hallucinations: str, agitation: str,
                        orientation: str, delusions: str, seizures: str):
        """Validates input parameters"""
        
        # Validate pulse
        if not isinstance(pulse, int) or pulse < 40 or pulse > 200:
            raise ValueError("Pulse must be an integer between 40 and 200 bpm")
        
        # Validate diastolic BP
        if not isinstance(diastolic_bp, int) or diastolic_bp < 40 or diastolic_bp > 150:
            raise ValueError("Diastolic BP must be an integer between 40 and 150 mmHg")
        
        # Validate categorical parameters
        valid_tremor = list(self.TREMOR_SCORES.keys())
        if tremor not in valid_tremor:
            raise ValueError(f"Tremor must be one of: {', '.join(valid_tremor)}")
        
        valid_sweat = list(self.SWEAT_SCORES.keys())
        if sweat not in valid_sweat:
            raise ValueError(f"Sweat must be one of: {', '.join(valid_sweat)}")
        
        valid_hallucinations = list(self.HALLUCINATION_SCORES.keys())
        if hallucinations not in valid_hallucinations:
            raise ValueError(f"Hallucinations must be one of: {', '.join(valid_hallucinations)}")
        
        valid_agitation = list(self.AGITATION_SCORES.keys())
        if agitation not in valid_agitation:
            raise ValueError(f"Agitation must be one of: {', '.join(valid_agitation)}")
        
        valid_orientation = list(self.ORIENTATION_SCORES.keys())
        if orientation not in valid_orientation:
            raise ValueError(f"Orientation must be one of: {', '.join(valid_orientation)}")
        
        valid_delusions = list(self.DELUSION_SCORES.keys())
        if delusions not in valid_delusions:
            raise ValueError(f"Delusions must be one of: {', '.join(valid_delusions)}")
        
        valid_seizures = list(self.SEIZURE_SCORES.keys())
        if seizures not in valid_seizures:
            raise ValueError(f"Seizures must be one of: {', '.join(valid_seizures)}")
    
    def _get_pulse_score(self, pulse: int) -> int:
        """Calculates pulse score based on heart rate"""
        if pulse < 90:
            return 0
        elif pulse <= 110:
            return 1
        else:
            return 2
    
    def _get_dbp_score(self, diastolic_bp: int) -> int:
        """Calculates diastolic blood pressure score"""
        if diastolic_bp < 90:
            return 0
        elif diastolic_bp <= 110:
            return 1
        else:
            return 2
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mMINDS score
        
        Args:
            score (int): Total mMINDS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 10:
            return {
                "stage": "Minimal Withdrawal",
                "description": "Minimal to no withdrawal symptoms",
                "interpretation": (f"mMINDS Score {score}: Minimal alcohol withdrawal symptoms present. "
                                f"Clinical observation may be sufficient with close monitoring for symptom "
                                f"progression. Consider implementing symptom-triggered therapy protocols. "
                                f"Patient may not require benzodiazepine therapy at this time, but frequent "
                                f"reassessment is recommended as withdrawal can progress rapidly.")
            }
        elif score <= 20:
            return {
                "stage": "Mild Withdrawal",
                "description": "Mild withdrawal symptoms",
                "interpretation": (f"mMINDS Score {score}: Mild alcohol withdrawal syndrome is present. "
                                f"Consider initiating benzodiazepine therapy with symptom-triggered dosing "
                                f"protocols. Monitor closely for symptom progression, as withdrawal can worsen "
                                f"over the first 24-72 hours. Reassess frequently and be prepared to escalate "
                                f"treatment if scores increase or clinical condition deteriorates.")
            }
        elif score <= 30:
            return {
                "stage": "Moderate Withdrawal",
                "description": "Moderate withdrawal symptoms",
                "interpretation": (f"mMINDS Score {score}: Moderate alcohol withdrawal syndrome requiring "
                                f"active treatment. Benzodiazepine therapy is indicated with consideration "
                                f"for higher doses or more frequent administration. Consider ICU-level "
                                f"monitoring if score is increasing or patient has risk factors for severe "
                                f"withdrawal. Monitor for progression to delirium tremens and ensure adequate "
                                f"supportive care including thiamine supplementation and electrolyte management.")
            }
        else:  # score > 30
            return {
                "stage": "Severe Withdrawal",
                "description": "Severe withdrawal symptoms",
                "interpretation": (f"mMINDS Score {score}: Severe alcohol withdrawal syndrome with high risk "
                                f"for delirium tremens and life-threatening complications. Aggressive "
                                f"benzodiazepine therapy is required, potentially including high-dose or "
                                f"continuous infusion protocols. ICU monitoring is strongly recommended for "
                                f"hemodynamic support, airway protection, and intensive nursing care. "
                                f"Consider additional medications such as phenobarbital or propofol if "
                                f"benzodiazepines are insufficient. Ensure comprehensive supportive care.")
            }


def calculate_modified_minnesota_detoxification_scale(pulse: int, diastolic_bp: int,
                                                    tremor: str, sweat: str,
                                                    hallucinations: str, agitation: str,
                                                    orientation: str, delusions: str,
                                                    seizures: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedMinnesotaDetoxificationScaleCalculator()
    return calculator.calculate(pulse, diastolic_bp, tremor, sweat, hallucinations,
                               agitation, orientation, delusions, seizures)