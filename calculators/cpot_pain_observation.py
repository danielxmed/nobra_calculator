"""
Critical Care Pain Observation Tool (CPOT) Calculator

Pain assessment tool for critically ill adults who are unable to self-report pain.
Evaluates pain using behavioral indicators across four domains.

References:
- Gélinas C, Fillion L, Puntillo KA, et al. Am J Crit Care. 2006;15(4):420-427.
- Gélinas C, Harel F, Fillion L, et al. J Pain Symptom Manage. 2009;37(1):58-67.
"""

from typing import Dict, Any, Optional, List


class CpotPainObservationCalculator:
    """Calculator for Critical Care Pain Observation Tool (CPOT)"""
    
    def __init__(self):
        # Scoring dictionaries for each domain
        self.FACIAL_EXPRESSION_SCORES = {
            "relaxed_neutral": 0,      # No muscular tension observed
            "tense": 1,                # Frowning, brow lowering, orbit tightening
            "grimacing": 2             # All previous facial movements plus eyelids tightly closed
        }
        
        self.BODY_MOVEMENTS_SCORES = {
            "absence_of_movements": 0,  # Does not move at all
            "protection": 1,            # Slow cautious movements, touching pain site
            "restlessness": 2           # Pulling tube, attempting to sit up, thrashing
        }
        
        self.MUSCLE_TENSION_SCORES = {
            "relaxed": 0,              # No resistance to passive movements
            "tense_rigid": 1,          # Resistance to passive movements
            "very_tense_rigid": 2      # Strong resistance, unable to complete movements
        }
        
        # For intubated patients
        self.VENTILATOR_COMPLIANCE_SCORES = {
            "tolerating": 0,           # Tolerating ventilator or movement
            "coughing_tolerating": 1,  # Coughing but tolerating
            "fighting_ventilator": 2   # Fighting ventilator
        }
        
        # For extubated patients
        self.VOCALIZATION_SCORES = {
            "normal_tone_no_sound": 0, # Talking in normal tone or no sound
            "sighing_moaning": 1,      # Sighing, moaning
            "crying_sobbing": 2        # Crying out, sobbing
        }
    
    def calculate(self, facial_expression: str, body_movements: str, muscle_tension: str, 
                  patient_status: str, ventilator_compliance: Optional[str] = None, 
                  vocalization: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates the CPOT score using behavioral pain indicators
        
        Args:
            facial_expression (str): Facial expression assessment
            body_movements (str): Body movements assessment  
            muscle_tension (str): Muscle tension assessment
            patient_status (str): Patient intubation status (intubated/extubated)
            ventilator_compliance (str, optional): For intubated patients only
            vocalization (str, optional): For extubated patients only
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(facial_expression, body_movements, muscle_tension, 
                            patient_status, ventilator_compliance, vocalization)
        
        # Calculate score for each domain
        facial_score = self.FACIAL_EXPRESSION_SCORES[facial_expression]
        movements_score = self.BODY_MOVEMENTS_SCORES[body_movements]
        tension_score = self.MUSCLE_TENSION_SCORES[muscle_tension]
        
        # Calculate fourth domain score based on patient status
        if patient_status == "intubated":
            if ventilator_compliance is None:
                raise ValueError("Ventilator compliance assessment required for intubated patients")
            fourth_domain_score = self.VENTILATOR_COMPLIANCE_SCORES[ventilator_compliance]
            fourth_domain_name = "Ventilator Compliance"
            fourth_domain_value = ventilator_compliance.replace("_", " ").title()
        else:  # extubated
            if vocalization is None:
                raise ValueError("Vocalization assessment required for extubated patients")
            fourth_domain_score = self.VOCALIZATION_SCORES[vocalization]
            fourth_domain_name = "Vocalization"
            fourth_domain_value = vocalization.replace("_", " ").title()
        
        # Calculate total score
        total_score = facial_score + movements_score + tension_score + fourth_domain_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Create detailed scoring breakdown
        scoring_breakdown = {
            "facial_expression": {
                "value": facial_expression.replace("_", " ").title(),
                "score": facial_score,
                "description": self._get_domain_description("facial_expression", facial_expression)
            },
            "body_movements": {
                "value": body_movements.replace("_", " ").title(),
                "score": movements_score,
                "description": self._get_domain_description("body_movements", body_movements)
            },
            "muscle_tension": {
                "value": muscle_tension.replace("_", " ").title(),
                "score": tension_score,
                "description": self._get_domain_description("muscle_tension", muscle_tension)
            },
            fourth_domain_name.lower().replace(" ", "_"): {
                "value": fourth_domain_value,
                "score": fourth_domain_score,
                "description": self._get_domain_description(patient_status, 
                                                          ventilator_compliance if patient_status == "intubated" else vocalization)
            }
        }
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "scoring_breakdown": scoring_breakdown,
            "clinical_recommendations": self._get_clinical_recommendations(total_score),
            "assessment_notes": self._get_assessment_notes(patient_status)
        }
    
    def _validate_inputs(self, facial_expression: str, body_movements: str, muscle_tension: str,
                        patient_status: str, ventilator_compliance: Optional[str], 
                        vocalization: Optional[str]):
        """Validates input parameters"""
        
        if facial_expression not in self.FACIAL_EXPRESSION_SCORES:
            valid_options = list(self.FACIAL_EXPRESSION_SCORES.keys())
            raise ValueError(f"Invalid facial_expression. Must be one of: {valid_options}")
        
        if body_movements not in self.BODY_MOVEMENTS_SCORES:
            valid_options = list(self.BODY_MOVEMENTS_SCORES.keys())
            raise ValueError(f"Invalid body_movements. Must be one of: {valid_options}")
        
        if muscle_tension not in self.MUSCLE_TENSION_SCORES:
            valid_options = list(self.MUSCLE_TENSION_SCORES.keys())
            raise ValueError(f"Invalid muscle_tension. Must be one of: {valid_options}")
        
        if patient_status not in ["intubated", "extubated"]:
            raise ValueError("Patient status must be either 'intubated' or 'extubated'")
        
        if patient_status == "intubated":
            if ventilator_compliance is None:
                raise ValueError("Ventilator compliance assessment required for intubated patients")
            if ventilator_compliance not in self.VENTILATOR_COMPLIANCE_SCORES:
                valid_options = list(self.VENTILATOR_COMPLIANCE_SCORES.keys())
                raise ValueError(f"Invalid ventilator_compliance. Must be one of: {valid_options}")
        
        if patient_status == "extubated":
            if vocalization is None:
                raise ValueError("Vocalization assessment required for extubated patients")
            if vocalization not in self.VOCALIZATION_SCORES:
                valid_options = list(self.VOCALIZATION_SCORES.keys())
                raise ValueError(f"Invalid vocalization. Must be one of: {valid_options}")
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the total score
        
        Args:
            total_score (int): Total CPOT score (0-8)
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= 2:
            return {
                "stage": "Minimal to No Pain",
                "description": "Acceptable pain level",
                "interpretation": (f"CPOT score of {total_score} indicates minimal to no pain. "
                                 "Continue current pain management plan and routine monitoring. "
                                 "Patient appears comfortable with current interventions.")
            }
        else:  # score > 2
            return {
                "stage": "Unacceptable Pain",
                "description": "Significant pain requiring intervention",
                "interpretation": (f"CPOT score of {total_score} indicates unacceptable pain level. "
                                 "Consider alternative analgesia, reassess pain management plan, "
                                 "and provide non-pharmacological comfort measures. Reassess "
                                 "within 30 minutes of intervention.")
            }
    
    def _get_domain_description(self, domain: str, value: str) -> str:
        """Get detailed description for each domain assessment"""
        
        descriptions = {
            "facial_expression": {
                "relaxed_neutral": "No muscular tension observed",
                "tense": "Frowning, brow lowering, orbit tightening",
                "grimacing": "All previous facial movements plus eyelids tightly closed"
            },
            "body_movements": {
                "absence_of_movements": "Does not move at all",
                "protection": "Slow cautious movements, touching or guarding pain site",
                "restlessness": "Pulling tube, attempting to sit up, moving limbs, thrashing"
            },
            "muscle_tension": {
                "relaxed": "No resistance to passive movements",
                "tense_rigid": "Resistance to passive movements",
                "very_tense_rigid": "Strong resistance, unable to complete passive movements"
            },
            "intubated": {
                "tolerating": "Tolerating ventilator or movement",
                "coughing_tolerating": "Coughing but tolerating ventilation",
                "fighting_ventilator": "Fighting ventilator, alarms frequently"
            },
            "extubated": {
                "normal_tone_no_sound": "Talking in normal tone or no vocalization",
                "sighing_moaning": "Sighing, moaning, whimpering",
                "crying_sobbing": "Crying out, sobbing, verbal complaints"
            }
        }
        
        return descriptions.get(domain, {}).get(value, "Assessment description")
    
    def _get_clinical_recommendations(self, total_score: int) -> Dict[str, Any]:
        """Get clinical recommendations based on score"""
        
        if total_score <= 2:
            return {
                "pain_management": "Continue current analgesic regimen",
                "monitoring": "Routine pain assessments every 4 hours or per protocol",
                "interventions": [
                    "Maintain current comfort measures",
                    "Assess for positioning needs",
                    "Continue environmental modifications"
                ],
                "reassessment": "Next scheduled assessment or if patient condition changes"
            }
        else:
            return {
                "pain_management": "Consider increasing analgesic dose or alternative medications",
                "monitoring": "Frequent pain assessments (every 30 minutes after intervention)",
                "interventions": [
                    "Administer additional analgesic as ordered",
                    "Non-pharmacological comfort measures (positioning, massage, distraction)",
                    "Environmental modifications (noise reduction, dimmed lighting)",
                    "Consider multimodal pain management approach",
                    "Notify physician if score remains >2 after interventions"
                ],
                "reassessment": "Within 30 minutes of pain intervention"
            }
    
    def _get_assessment_notes(self, patient_status: str) -> List[str]:
        """Get assessment-specific notes"""
        
        base_notes = [
            "Observe patient at rest for 60 seconds before scoring",
            "Consider patient's baseline behavior and cultural expressions",
            "Use in conjunction with physiological indicators when available",
            "Document specific behaviors observed for each domain"
        ]
        
        if patient_status == "intubated":
            base_notes.extend([
                "Monitor ventilator synchrony and breathing patterns",
                "Assess for appropriate sedation level",
                "Consider impact of sedatives on behavioral responses"
            ])
        else:
            base_notes.extend([
                "Listen for verbal expressions of pain or discomfort",
                "Consider patient's ability to communicate effectively",
                "Assess for non-verbal communication attempts"
            ])
        
        return base_notes


def calculate_cpot_pain_observation(facial_expression: str, body_movements: str, muscle_tension: str,
                                  patient_status: str, ventilator_compliance: Optional[str] = None,
                                  vocalization: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CpotPainObservationCalculator()
    return calculator.calculate(facial_expression, body_movements, muscle_tension, 
                              patient_status, ventilator_compliance, vocalization)