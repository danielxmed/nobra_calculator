"""
Confusion Assessment Method for the ICU (CAM-ICU) Calculator

Monitors delirium in ICU patients through systematic assessment of consciousness level,
attention, and organized thinking.

References:
1. Ely EW, Inouye SK, Bernard GR, Gordon S, Francis J, May L, et al. Delirium in mechanically 
   ventilated patients: validity and reliability of the confusion assessment method for the 
   intensive care unit (CAM-ICU). JAMA. 2001 Dec 5;286(21):2703-10. doi: 10.1001/jama.286.21.2703.
2. Ely EW, Margolin R, Francis J, May L, Truman B, Dittus R, et al. Evaluation of delirium in 
   critically ill patients: validation of the Confusion Assessment Method for the Intensive Care 
   Unit (CAM-ICU). Crit Care Med. 2001 Jul;29(7):1370-9. doi: 10.1097/00003246-200107000-00012.
3. Devlin JW, Skrobik Y, Gélinas C, Needham DM, Slooter AJ, Pandharipande PP, et al. Clinical 
   Practice Guidelines for the Prevention and Management of Pain, Agitation/Sedation, Delirium, 
   Immobility, and Sleep Disruption in Adult Patients in the ICU. Crit Care Med. 2018 Sep;46(9):e825-e873. 
   doi: 10.1097/CCM.0000000000003299.
"""

from typing import Dict, Any


class CamIcuCalculator:
    """Calculator for Confusion Assessment Method for the ICU (CAM-ICU)"""
    
    def __init__(self):
        # RASS scale definitions
        self.RASS_LEVELS = {
            4: "Combative",
            3: "Very agitated", 
            2: "Agitated",
            1: "Restless",
            0: "Alert and calm",
            -1: "Drowsy",
            -2: "Light sedation",
            -3: "Moderate sedation",
            -4: "Deep sedation",
            -5: "Unarousable"
        }
        
        # Minimum RASS for assessment
        self.MIN_RASS_FOR_ASSESSMENT = -3
        
        # Thresholds for positive features
        self.ATTENTION_ERROR_THRESHOLD = 2  # >2 errors indicates inattention
        self.THINKING_ERROR_THRESHOLD = 1   # >1 error indicates disorganized thinking
    
    def calculate(
        self,
        rass_score: int,
        acute_onset_fluctuating: str,
        attention_errors: int,
        thinking_errors: int
    ) -> Dict[str, Any]:
        """
        Evaluates delirium using CAM-ICU criteria
        
        Args:
            rass_score: Richmond Agitation-Sedation Scale score (-5 to +4)
            acute_onset_fluctuating: Acute onset or fluctuating course (yes/no)
            attention_errors: Number of errors in attention test (0-10)
            thinking_errors: Number of errors in organized thinking test (0-4)
            
        Returns:
            Dict with CAM-ICU assessment results and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(rass_score, acute_onset_fluctuating, attention_errors, thinking_errors)
        
        # Assess each CAM-ICU feature
        features = self._assess_cam_icu_features(
            rass_score, acute_onset_fluctuating, attention_errors, thinking_errors
        )
        
        # Determine overall CAM-ICU result
        cam_icu_positive = self._determine_cam_icu_result(features)
        
        # Generate clinical interpretation
        interpretation = self._get_clinical_interpretation(cam_icu_positive, features)
        
        # Get management recommendations
        management = self._get_management_recommendations(cam_icu_positive, features)
        
        return {
            "result": {
                "cam_icu_positive": cam_icu_positive,
                "features": features,
                "clinical_interpretation": interpretation,
                "management_recommendations": management,
                "assessment_validity": self._get_assessment_validity(rass_score)
            },
            "unit": "assessment",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, rass_score, acute_onset_fluctuating, attention_errors, thinking_errors):
        """Validates input parameters"""
        
        # Validate RASS score
        if not isinstance(rass_score, int) or rass_score < -5 or rass_score > 4:
            raise ValueError("RASS score must be integer between -5 and +4")
        
        # Validate acute onset/fluctuating
        if acute_onset_fluctuating not in ["yes", "no"]:
            raise ValueError("Acute onset/fluctuating must be 'yes' or 'no'")
        
        # Validate attention errors
        if not isinstance(attention_errors, int) or attention_errors < 0 or attention_errors > 10:
            raise ValueError("Attention errors must be integer between 0 and 10")
        
        # Validate thinking errors
        if not isinstance(thinking_errors, int) or thinking_errors < 0 or thinking_errors > 4:
            raise ValueError("Thinking errors must be integer between 0 and 4")
    
    def _assess_cam_icu_features(self, rass_score, acute_onset_fluctuating, attention_errors, thinking_errors):
        """Assesses individual CAM-ICU features"""
        
        # Feature 1: Acute onset or fluctuating course
        feature_1_positive = acute_onset_fluctuating == "yes"
        
        # Feature 2: Inattention (>2 errors in attention test)
        feature_2_positive = attention_errors > self.ATTENTION_ERROR_THRESHOLD
        
        # Feature 3: Altered level of consciousness (RASS ≠ 0)
        feature_3_positive = rass_score != 0
        
        # Feature 4: Disorganized thinking (>1 error in thinking test)
        feature_4_positive = thinking_errors > self.THINKING_ERROR_THRESHOLD
        
        return {
            "feature_1": {
                "name": "Acute Onset or Fluctuating Course",
                "positive": feature_1_positive,
                "description": "Acute change in mental status or fluctuating course in past 24 hours",
                "assessment": "Present" if feature_1_positive else "Absent"
            },
            "feature_2": { 
                "name": "Inattention",
                "positive": feature_2_positive,
                "description": f"Attention test errors: {attention_errors} (>2 errors indicates inattention)",
                "assessment": "Present" if feature_2_positive else "Absent"
            },
            "feature_3": {
                "name": "Altered Level of Consciousness", 
                "positive": feature_3_positive,
                "description": f"RASS score: {rass_score} ({self.RASS_LEVELS[rass_score]})",
                "assessment": "Present" if feature_3_positive else "Absent"
            },
            "feature_4": {
                "name": "Disorganized Thinking",
                "positive": feature_4_positive,
                "description": f"Thinking test errors: {thinking_errors} (>1 error indicates disorganized thinking)",
                "assessment": "Present" if feature_4_positive else "Absent"
            }
        }
    
    def _determine_cam_icu_result(self, features):
        """Determines if CAM-ICU is positive based on features"""
        
        # CAM-ICU is positive if:
        # Feature 1 (acute onset/fluctuating) AND
        # Feature 2 (inattention) AND
        # (Feature 3 (altered consciousness) OR Feature 4 (disorganized thinking))
        
        feature_1_present = features["feature_1"]["positive"]
        feature_2_present = features["feature_2"]["positive"] 
        feature_3_present = features["feature_3"]["positive"]
        feature_4_present = features["feature_4"]["positive"]
        
        return (feature_1_present and 
                feature_2_present and 
                (feature_3_present or feature_4_present))
    
    def _get_clinical_interpretation(self, cam_icu_positive, features):
        """Generates clinical interpretation of results"""
        
        if cam_icu_positive:
            stage = "CAM-ICU Positive"
            description = "Delirium present"
            interpretation = ("Patient meets CAM-ICU criteria for delirium. Immediate implementation of "
                            "delirium management protocols is recommended. Evaluate and address underlying "
                            "causes, optimize medications, and implement non-pharmacological interventions.")
        else:
            stage = "CAM-ICU Negative"
            description = "No delirium detected"
            interpretation = ("Patient does not meet CAM-ICU criteria for delirium at this time. Continue "
                            "routine monitoring and reassess regularly as delirium can fluctuate throughout "
                            "the day.")
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_management_recommendations(self, cam_icu_positive, features):
        """Generates management recommendations based on results"""
        
        recommendations = {
            "immediate_actions": [],
            "ongoing_monitoring": [],
            "prevention_strategies": [],
            "reassessment_timing": ""
        }
        
        if cam_icu_positive:
            recommendations["immediate_actions"] = [
                "Implement delirium management protocol",
                "Evaluate and treat underlying causes (infection, metabolic disturbances, medications)",
                "Review and optimize sedative medications",
                "Ensure adequate sleep-wake cycles",
                "Consider antipsychotic therapy if agitation present and non-pharmacological measures insufficient"
            ]
            
            recommendations["ongoing_monitoring"] = [
                "Continue CAM-ICU assessments every shift",
                "Monitor for complications (falls, self-extubation, longer ICU stay)",
                "Assess functional status and cognitive recovery",
                "Family involvement in care and orientation"
            ]
            
            recommendations["prevention_strategies"] = [
                "Maintain normal sleep-wake cycles",
                "Early mobilization when appropriate",
                "Minimize unnecessary medications",
                "Frequent reorientation",
                "Noise reduction strategies"
            ]
            
            recommendations["reassessment_timing"] = "Every nursing shift or with change in clinical status"
            
        else:
            recommendations["immediate_actions"] = [
                "Continue current care plan",
                "Maintain delirium prevention strategies"
            ]
            
            recommendations["ongoing_monitoring"] = [
                "Continue routine CAM-ICU screening",
                "Monitor for risk factors that could precipitate delirium"
            ]
            
            recommendations["prevention_strategies"] = [
                "Maintain normal sleep-wake cycles",
                "Early mobilization",
                "Minimize sedating medications",
                "Frequent reorientation",
                "Family involvement in care"
            ]
            
            recommendations["reassessment_timing"] = "Every nursing shift as per ICU protocol"
        
        return recommendations
    
    def _get_assessment_validity(self, rass_score):
        """Assesses the validity of the CAM-ICU assessment"""
        
        if rass_score < self.MIN_RASS_FOR_ASSESSMENT:
            return {
                "valid": False,
                "reason": f"RASS score {rass_score} too low for assessment (requires ≥ -3)",
                "recommendation": "Patient too sedated for CAM-ICU assessment. Reassess when RASS ≥ -3"
            }
        else:
            return {
                "valid": True,
                "reason": f"RASS score {rass_score} adequate for assessment",
                "recommendation": "Assessment results are valid"
            }


def calculate_cam_icu(
    rass_score: int,
    acute_onset_fluctuating: str,
    attention_errors: int,
    thinking_errors: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CamIcuCalculator()
    return calculator.calculate(
        rass_score=rass_score,
        acute_onset_fluctuating=acute_onset_fluctuating,
        attention_errors=attention_errors,
        thinking_errors=thinking_errors
    )