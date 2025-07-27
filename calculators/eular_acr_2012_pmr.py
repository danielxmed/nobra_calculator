"""
2012 EULAR/ACR Classification Criteria for Polymyalgia Rheumatica Calculator

Classifies polymyalgia rheumatica using clinical and ultrasonographic criteria.
Reference: Dasgupta et al., Ann Rheum Dis 2012;71(4):484-92
"""

from typing import Dict, Any


class EularAcr2012PmrCalculator:
    """Calculator for EULAR/ACR 2012 PMR classification criteria"""
    
    def calculate(self, morning_stiffness: str, hip_pain_limited_rom: str,
                 rf_or_acpa: str, other_joint_pain: str,
                 ultrasound_shoulder_hip: str = "not_performed",
                 ultrasound_both_shoulders: str = "not_performed") -> Dict[str, Any]:
        """
        Calculates the EULAR/ACR 2012 score for polymyalgia rheumatica
        
        Args:
            morning_stiffness: "<=45min" or ">45min" - duration of morning stiffness
            hip_pain_limited_rom: "no" or "yes" - hip pain or limited ROM
            rf_or_acpa: "present" or "absent" - RF or ACPA present
            other_joint_pain: "present" or "absent" - pain in other joints
            ultrasound_shoulder_hip: "no", "yes", "not_performed" - shoulder/hip US
            ultrasound_both_shoulders: "no", "yes", "not_performed" - both shoulders US
            
        Returns:
            Dict with result, interpretation, and classification
        """
        
        # Validations
        self._validate_inputs(morning_stiffness, hip_pain_limited_rom, rf_or_acpa,
                            other_joint_pain, ultrasound_shoulder_hip,
                            ultrasound_both_shoulders)
        
        # Calculate score
        score = 0
        
        # Morning stiffness >45min: 2 points
        if morning_stiffness == ">45min":
            score += 2
        
        # Hip pain or limited ROM: 1 point
        if hip_pain_limited_rom == "yes":
            score += 1
        
        # Absence of RF or ACPA: 2 points
        if rf_or_acpa == "absent":
            score += 2
        
        # Absence of pain in other joints: 1 point
        if other_joint_pain == "absent":
            score += 1
        
        # Determine if ultrasound was performed
        us_performed = (ultrasound_shoulder_hip != "not_performed" or 
                       ultrasound_both_shoulders != "not_performed")
        
        # Add ultrasound points if performed
        if us_performed:
            if ultrasound_shoulder_hip == "yes":
                score += 1
            if ultrasound_both_shoulders == "yes":
                score += 1
        
        # Get interpretation based on score and if US was performed
        interpretation = self._get_interpretation(score, us_performed)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, morning_stiffness: str, hip_pain_limited_rom: str,
                        rf_or_acpa: str, other_joint_pain: str,
                        ultrasound_shoulder_hip: str, ultrasound_both_shoulders: str):
        """Validates input parameters"""
        
        if morning_stiffness not in ["<=45min", ">45min"]:
            raise ValueError("Morning stiffness must be '<=45min' or '>45min'")
        
        if hip_pain_limited_rom not in ["no", "yes"]:
            raise ValueError("Hip pain/limited ROM must be 'no' or 'yes'")
        
        if rf_or_acpa not in ["present", "absent"]:
            raise ValueError("RF or ACPA must be 'present' or 'absent'")
        
        if other_joint_pain not in ["present", "absent"]:
            raise ValueError("Pain in other joints must be 'present' or 'absent'")
        
        valid_us_options = ["no", "yes", "not_performed"]
        if ultrasound_shoulder_hip not in valid_us_options:
            raise ValueError(f"Shoulder/hip ultrasound must be: {', '.join(valid_us_options)}")
        
        if ultrasound_both_shoulders not in valid_us_options:
            raise ValueError(f"Both shoulders ultrasound must be: {', '.join(valid_us_options)}")
        
        # Validate ultrasound consistency
        if ((ultrasound_shoulder_hip == "not_performed" and 
             ultrasound_both_shoulders != "not_performed") or
            (ultrasound_shoulder_hip != "not_performed" and 
             ultrasound_both_shoulders == "not_performed")):
            raise ValueError("If ultrasound was performed, both US parameters must be provided")
    
    def _get_interpretation(self, score: int, us_performed: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and if US was performed
        
        Args:
            score: Calculated score
            us_performed: Whether ultrasound was performed
            
        Returns:
            Dict with interpretation
        """
        
        if not us_performed:
            # Without ultrasound: cutoff point ≥4
            if score >= 4:
                return {
                    "stage": "PMR",
                    "description": "Classifies as PMR (without ultrasound)",
                    "interpretation": f"Score of {score} points (≥4) classifies as polymyalgia rheumatica by EULAR/ACR 2012 criteria. Sensitivity 72%, specificity 65%."
                }
            else:
                return {
                    "stage": "Non-PMR",
                    "description": "Does not classify as PMR (without ultrasound)",
                    "interpretation": f"Score of {score} points (<4) does not classify as polymyalgia rheumatica. Consider alternative diagnoses."
                }
        else:
            # With ultrasound: cutoff point ≥5
            if score >= 5:
                return {
                    "stage": "PMR (US)",
                    "description": "Classifies as PMR (with ultrasound)",
                    "interpretation": f"Score of {score} points (≥5) classifies as polymyalgia rheumatica by EULAR/ACR 2012 criteria with ultrasound. Sensitivity 71%, specificity 70%."
                }
            else:
                return {
                    "stage": "Non-PMR (US)",
                    "description": "Does not classify as PMR (with ultrasound)",
                    "interpretation": f"Score of {score} points (<5) does not classify as polymyalgia rheumatica with ultrasonography. Consider alternative diagnoses."
                }


def calculate_eular_acr_2012_pmr(morning_stiffness: str, hip_pain_limited_rom: str,
                                 rf_or_acpa: str, other_joint_pain: str,
                                 ultrasound_shoulder_hip: str = "not_performed",
                                 ultrasound_both_shoulders: str = "not_performed") -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = EularAcr2012PmrCalculator()
    return calculator.calculate(morning_stiffness, hip_pain_limited_rom,
                              rf_or_acpa, other_joint_pain,
                              ultrasound_shoulder_hip, ultrasound_both_shoulders)
