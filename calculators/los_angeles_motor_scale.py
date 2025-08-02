"""
Los Angeles Motor Scale (LAMS) Calculator

Stratifies stroke severity in the field to identify patients with large vessel occlusion.
Rapid screening tool for prehospital providers to guide transport decisions.

References:
1. Llanes JN, Kidwell CS, Starkman S, Leary MC, Eckstein M, Saver JL. The Los Angeles 
   Motor Scale (LAMS): a new measure to characterize stroke severity in the field. 
   Prehosp Emerg Care. 2004 Jan-Mar;8(1):46-50. doi: 10.1080/312703002806.
2. Nazliel B, Starkman S, Liebeskind DS, Ovbiagele B, Kim D, Sanossian N, et al. A brief 
   prehospital stroke severity scale identifies ischemic stroke patients harboring 
   persisting large arterial occlusions. Stroke. 2008 Aug;39(8):2264-7.
"""

from typing import Dict, Any


class LosAngelesMotorScaleCalculator:
    """Calculator for Los Angeles Motor Scale (LAMS)"""
    
    def __init__(self):
        # Scoring system for each component
        self.FACIAL_DROOP_SCORES = {
            "absent": 0,
            "present": 1
        }
        
        self.ARM_DRIFT_SCORES = {
            "absent": 0,
            "drifts_down": 1,
            "falls_rapidly": 2
        }
        
        self.GRIP_STRENGTH_SCORES = {
            "normal": 0,
            "weak_grip": 1,
            "no_grip": 2
        }
        
        # Clinical interpretation thresholds
        self.LVO_THRESHOLD = 4  # Score ≥4 suggests large vessel occlusion
        
        # Transport recommendations
        self.TRANSPORT_RECOMMENDATIONS = {
            "minor_moderate": {
                "recommendation": "Transport to nearest stroke-capable facility",
                "urgency": "Moderate - stroke treatment beneficial but less time-sensitive",
                "interventions": "IV thrombolysis (tPA) if within time window"
            },
            "severe": {
                "recommendation": "Direct transport to comprehensive stroke center with endovascular capabilities",
                "urgency": "High - time-sensitive large vessel occlusion likely",
                "interventions": "Mechanical thrombectomy + IV thrombolysis if within time windows"
            }
        }
    
    def calculate(self, facial_droop: str, arm_drift: str, grip_strength: str) -> Dict[str, Any]:
        """
        Calculates LAMS score using motor assessment components
        
        Args:
            facial_droop (str): Facial droop assessment (absent, present)
            arm_drift (str): Arm drift assessment (absent, drifts_down, falls_rapidly)
            grip_strength (str): Grip strength assessment (normal, weak_grip, no_grip)
            
        Returns:
            Dict with LAMS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(facial_droop, arm_drift, grip_strength)
        
        # Calculate component scores
        facial_score = self.FACIAL_DROOP_SCORES[facial_droop]
        arm_score = self.ARM_DRIFT_SCORES[arm_drift]
        grip_score = self.GRIP_STRENGTH_SCORES[grip_strength]
        
        # Calculate total LAMS score
        total_score = facial_score + arm_score + grip_score
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score, facial_score, arm_score, grip_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, facial_droop, arm_drift, grip_strength):
        """Validates input parameters"""
        
        if facial_droop not in self.FACIAL_DROOP_SCORES:
            valid_options = list(self.FACIAL_DROOP_SCORES.keys())
            raise ValueError(f"Facial droop must be one of: {valid_options}")
        
        if arm_drift not in self.ARM_DRIFT_SCORES:
            valid_options = list(self.ARM_DRIFT_SCORES.keys())
            raise ValueError(f"Arm drift must be one of: {valid_options}")
        
        if grip_strength not in self.GRIP_STRENGTH_SCORES:
            valid_options = list(self.GRIP_STRENGTH_SCORES.keys())
            raise ValueError(f"Grip strength must be one of: {valid_options}")
    
    def _get_interpretation(self, total_score: int, facial_score: int, arm_score: int, grip_score: int) -> Dict[str, str]:
        """
        Provides comprehensive clinical interpretation and transport recommendations
        """
        
        # Determine severity category
        if total_score >= self.LVO_THRESHOLD:
            severity = "severe"
            stage = "Severe Stroke"
            stage_description = "LVO likely"
            transport = self.TRANSPORT_RECOMMENDATIONS["severe"]
        else:
            severity = "minor_moderate"
            stage = "Minor to Moderate Stroke"
            stage_description = "LVO less likely"
            transport = self.TRANSPORT_RECOMMENDATIONS["minor_moderate"]
        
        # Build detailed interpretation
        interpretation = (
            f"Los Angeles Motor Scale (LAMS) Score Assessment:\\n\\n"
            f"Component Scores:\\n"
            f"• Facial droop: {facial_score} point{'s' if facial_score != 1 else ''}\\n"
            f"• Arm drift: {arm_score} point{'s' if arm_score != 1 else ''}\\n"
            f"• Grip strength: {grip_score} point{'s' if grip_score != 1 else ''}\\n"
            f"• Total LAMS score: {total_score}/5 points\\n\\n"
            f"Clinical Interpretation:\\n"
            f"• Stroke severity: {stage}\\n"
            f"• Large vessel occlusion (LVO): {stage_description}\\n\\n"
            f"Transport Recommendations:\\n"
            f"• Destination: {transport['recommendation']}\\n"
            f"• Urgency: {transport['urgency']}\\n"
            f"• Expected interventions: {transport['interventions']}\\n\\n"
        )
        
        # Add severity-specific clinical guidance
        if severity == "severe":
            interpretation += (
                f"Severe Stroke Management (LAMS ≥4):\\n"
                f"• High probability of large vessel occlusion (81% sensitivity)\\n"
                f"• 7-fold increased likelihood of persisting arterial occlusion\\n"
                f"• Time-critical for mechanical thrombectomy (optimal <6 hours from onset)\\n"
                f"• Bypass primary stroke centers if comprehensive stroke center available\\n"
                f"• Notify receiving facility of incoming severe stroke alert\\n"
                f"• Consider advanced airway management if decreased consciousness\\n"
                f"• Monitor blood pressure - avoid excessive reduction (goal <220/120 mmHg)\\n"
                f"• Document exact time of symptom onset or last known normal\\n\\n"
            )
        else:
            interpretation += (
                f"Minor to Moderate Stroke Management (LAMS <4):\\n"
                f"• Lower probability of large vessel occlusion\\n"
                f"• May still benefit from IV thrombolysis if within time window\\n"
                f"• Transport to nearest stroke-capable facility appropriate\\n"
                f"• Standard stroke protocol and supportive care\\n"
                f"• Monitor for neurological deterioration during transport\\n\\n"
            )
        
        # Add general prehospital care guidance
        interpretation += (
            f"General Prehospital Stroke Care:\\n"
            f"• LAMS should be completed rapidly (<2 minutes)\\n"
            f"• Document time of assessment and symptom onset\\n"
            f"• Check blood glucose and treat if <60 mg/dL or >400 mg/dL\\n"
            f"• Maintain oxygen saturation >94%\\n"
            f"• Position patient with head elevated 30 degrees if no spinal injury\\n"
            f"• Establish IV access but avoid delays in transport\\n"
            f"• LAMS correlates strongly with NIHSS (r=0.75) but is not a substitute\\n"
            f"• Consider stroke mimic conditions in appropriate clinical context\\n\\n"
            f"Key Validation Data:\\n"
            f"• Sensitivity: 81% for large vessel occlusion detection\\n"
            f"• Specificity: 89% for large vessel occlusion detection\\n"
            f"• Strong correlation with functional outcomes at 3 months\\n"
            f"• Validated for use by paramedics and emergency medical technicians"
        )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_los_angeles_motor_scale(facial_droop: str, arm_drift: str, grip_strength: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_los_angeles_motor_scale pattern
    """
    calculator = LosAngelesMotorScaleCalculator()
    return calculator.calculate(facial_droop, arm_drift, grip_strength)