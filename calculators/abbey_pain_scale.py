"""
Abbey Pain Scale for Dementia Patients Calculator

Assesses pain in patients with advanced dementia through behavioral observation.
Reference: Abbey J, Piller N, De Bellis A, et al. Int J Palliat Nurs. 2004;10(1):6-13.
"""

from typing import Dict, Any


class AbbeyPainScaleCalculator:
    """Calculator for Abbey Pain Scale"""
    
    def __init__(self):
        # Detailed descriptions for each domain and score
        self.domain_descriptions = {
            "vocalization": {
                0: "Absent - No vocalization of pain",
                1: "Mild - Occasional moans or sighs",
                2: "Moderate - Frequent moans, occasional crying",
                3: "Severe - Constant crying, screams, wails"
            },
            "facial_expression": {
                0: "Absent - Relaxed facial expression",
                1: "Mild - Occasional frown, slight facial tension",
                2: "Moderate - Frequent frown, tense look",
                3: "Severe - Constant grimace, look of distress"
            },
            "body_language": {
                0: "Absent - Relaxed posture",
                1: "Mild - Occasional restlessness, slight muscle tension",
                2: "Moderate - Defensive movements, moderate rigidity",
                3: "Severe - Extremely tense posture, constant protective movements"
            },
            "behavioral_change": {
                0: "Absent - Usual behavior",
                1: "Mild - Slight irritability or confusion",
                2: "Moderate - Moderate refusal to cooperate, agitation",
                3: "Severe - Aggressiveness, total refusal to cooperate"
            },
            "physiological_change": {
                0: "Absent - Stable vital signs",
                1: "Mild - Small changes in HR/BP/temperature",
                2: "Moderate - Moderate changes in vital signs, sweating",
                3: "Severe - Significant changes, profuse sweating, pallor"
            },
            "physical_change": {
                0: "Absent - No physical signs of pain",
                1: "Mild - Minimal physical signs (mild arthritis, small lesions)",
                2: "Moderate - Clear evidence of physical discomfort",
                3: "Severe - Severe evidence of physical pain (ulcers, contractures)"
            }
        }
    
    def calculate(self, vocalization: int, facial_expression: int, body_language: int,
                 behavioral_change: int, physiological_change: int, physical_change: int) -> Dict[str, Any]:
        """
        Calculates the Abbey Pain Scale
        
        Args:
            vocalization: Vocalization (0-3)
            facial_expression: Facial expression (0-3)
            body_language: Body language (0-3)
            behavioral_change: Behavioral change (0-3)
            physiological_change: Physiological change (0-3)
            physical_change: Physical change (0-3)
            
        Returns:
            Dict with result and interpretation
        """
        
        # Validations
        self._validate_inputs(vocalization, facial_expression, body_language,
                            behavioral_change, physiological_change, physical_change)
        
        # Calculate total score
        total_score = (vocalization + facial_expression + body_language +
                      behavioral_change + physiological_change + physical_change)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Get details for each domain
        domain_details = self._get_domain_details(
            vocalization, facial_expression, body_language,
            behavioral_change, physiological_change, physical_change
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "vocalization_score": vocalization,
            "facial_expression_score": facial_expression,
            "body_language_score": body_language,
            "behavioral_change_score": behavioral_change,
            "physiological_change_score": physiological_change,
            "physical_change_score": physical_change,
            "domain_details": domain_details,
            "pain_present": total_score > 2,  # Pain present if score > 2
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, vocalization: int, facial_expression: int, body_language: int,
                        behavioral_change: int, physiological_change: int, physical_change: int):
        """Validates input parameters"""
        
        parameters = {
            "vocalization": vocalization,
            "facial_expression": facial_expression,
            "body_language": body_language,
            "behavioral_change": behavioral_change,
            "physiological_change": physiological_change,
            "physical_change": physical_change
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name} must be an integer")
            
            if value < 0 or value > 3:
                raise ValueError(f"{param_name} must be between 0 and 3")
    
    def _get_domain_details(self, vocalization: int, facial_expression: int, body_language: int,
                           behavioral_change: int, physiological_change: int, physical_change: int) -> Dict[str, str]:
        """
        Gets detailed descriptions for each domain based on the score
        """
        
        return {
            "vocalization": self.domain_descriptions["vocalization"][vocalization],
            "facial_expression": self.domain_descriptions["facial_expression"][facial_expression],
            "body_language": self.domain_descriptions["body_language"][body_language],
            "behavioral_change": self.domain_descriptions["behavioral_change"][behavioral_change],
            "physiological_change": self.domain_descriptions["physiological_change"][physiological_change],
            "physical_change": self.domain_descriptions["physical_change"][physical_change]
        }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Interprets the total Abbey Pain Scale score
        
        Args:
            total_score: Total score (0-18)
            
        Returns:
            Dict with interpretation
        """
        
        if total_score <= 2:
            return {
                "stage": "No Pain",
                "description": "Absence of pain",
                "interpretation": f"Score {total_score}/18 indicates absence of pain. No behavioral evidence of pain. Patient appears comfortable. Continue routine observation and maintain preventive comfort measures."
            }
        elif total_score <= 7:
            return {
                "stage": "Mild Pain",
                "description": "Mild pain present",
                "interpretation": f"Score {total_score}/18 indicates mild pain. Evidence of mild discomfort. Consider non-pharmacological interventions (comfort, repositioning, relaxation, music therapy). Monitor response and re-evaluate in 30 minutes."
            }
        elif total_score <= 13:
            return {
                "stage": "Moderate Pain",
                "description": "Moderate pain present",
                "interpretation": f"Score {total_score}/18 indicates moderate pain. Clear evidence of moderate pain requiring intervention. Consider adequate analgesia (paracetamol, anti-inflammatories) and non-pharmacological interventions. Re-evaluate after 30-60 minutes."
            }
        else:
            return {
                "stage": "Severe Pain",
                "description": "Severe pain present",
                "interpretation": f"Score {total_score}/18 indicates severe pain. Evidence of severe pain requiring immediate analgesia. Use WHO analgesic ladder (consider opioids if appropriate). Re-evaluate frequently (15-30 min) and adjust treatment as needed."
            }


def calculate_abbey_pain_scale(vocalization: int, facial_expression: int, body_language: int,
                             behavioral_change: int, physiological_change: int, 
                             physical_change: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AbbeyPainScaleCalculator()
    return calculator.calculate(vocalization, facial_expression, body_language,
                              behavioral_change, physiological_change, physical_change)
