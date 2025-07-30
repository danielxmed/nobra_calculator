"""
Children's Hospital of Eastern Ontario Pain Scale (CHEOPS) Calculator

Quantifies post-operative pain in pediatric patients aged 1-5 years using behavioral observations.
Provides standardized pain assessment for appropriate analgesic management.

References:
1. McGrath PJ, Johnson G, Goodman JT, Schillinger J, Dunn J, Chapman J. CHEOPS: a 
   behavioral scale for rating postoperative pain in children. In: Fields HL, Dubner R, 
   Cervero F, editors. Advances in pain research and therapy. New York: Raven Press; 1985. 
   p. 395-402.
2. Suraseranivongse S, Santawat U, Kraiprasit K, Petcharatana S, Prakkamodom S, Muntraporn N. 
   Cross-validation of a composite pain scale for preschool children within 24 hours of 
   surgery. Br J Anaesth. 2001 Sep;87(3):400-5.
3. Beyer JE, McGrath PJ, Berde CB. Discordance between self-report and behavioral pain 
   measures in children aged 3-7 years after surgery. J Pain Symptom Manage. 1990 
   Dec;5(6):350-6.
"""

from typing import Dict, Any


class CheopsPainScaleCalculator:
    """Calculator for Children's Hospital of Eastern Ontario Pain Scale (CHEOPS)"""
    
    def __init__(self):
        # Scoring criteria for each behavioral category
        self.scoring_criteria = {
            "cry": {
                "no_crying": 1,
                "moaning_crying": 2,
                "screaming": 3
            },
            "facial": {
                "smiling": 0,
                "composed": 1,
                "grimace": 2
            },
            "verbal": {
                "positive": 0,
                "not_talking_other": 1,
                "pain_complaints": 2
            },
            "torso": {
                "neutral": 1,
                "shifting_tense": 2
            },
            "touch": {
                "not_touching": 1,
                "reaching_touching": 2
            },
            "legs": {
                "neutral": 1,
                "squirming_tensed": 2
            }
        }
        
        # Clinical intervention guidelines
        self.intervention_guidelines = {
            "low": {
                "score_range": "4",
                "level": "No Pain",
                "intervention": "No analgesic intervention required",
                "monitoring": "Continue routine monitoring and comfort measures",
                "reassessment": "Every 3 hours or as needed"
            },
            "moderate": {
                "score_range": "5-7",
                "level": "Mild to Moderate Pain",
                "intervention": "Consider administering analgesic medication",
                "monitoring": "Reassess after intervention and provide comfort measures",
                "reassessment": "15-20 minutes after IV analgesics, 30-45 minutes after oral/rectal"
            },
            "high": {
                "score_range": "8-13",
                "level": "Severe Pain",
                "intervention": "Analgesic medication required immediately",
                "monitoring": "Implement comprehensive pain management strategies",
                "reassessment": "Frequent reassessment until pain controlled"
            }
        }
    
    def calculate(
        self,
        cry: str,
        facial: str,
        verbal: str,
        torso: str,
        touch: str,
        legs: str
    ) -> Dict[str, Any]:
        """
        Calculates CHEOPS pain score based on behavioral observations
        
        Args:
            cry: Vocal response (no_crying/moaning_crying/screaming)
            facial: Facial expression (smiling/composed/grimace)
            verbal: Verbal responses (positive/not_talking_other/pain_complaints)
            torso: Body position (neutral/shifting_tense)
            touch: Wound interaction (not_touching/reaching_touching)
            legs: Leg movement (neutral/squirming_tensed)
            
        Returns:
            Dict with CHEOPS score, pain level, and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(cry, facial, verbal, torso, touch, legs)
        
        # Calculate individual component scores
        cry_points = self.scoring_criteria["cry"][cry]
        facial_points = self.scoring_criteria["facial"][facial]
        verbal_points = self.scoring_criteria["verbal"][verbal]
        torso_points = self.scoring_criteria["torso"][torso]
        touch_points = self.scoring_criteria["touch"][touch]
        legs_points = self.scoring_criteria["legs"][legs]
        
        # Calculate total score
        total_score = cry_points + facial_points + verbal_points + torso_points + touch_points + legs_points
        
        # Get pain assessment and recommendations
        pain_assessment = self._get_pain_assessment(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            cry, cry_points, facial, facial_points, verbal, verbal_points,
            torso, torso_points, touch, touch_points, legs, legs_points
        )
        
        return {
            "result": {
                "total_score": total_score,
                "pain_level": pain_assessment["level"],
                "intervention_required": pain_assessment["intervention_required"],
                "clinical_recommendation": pain_assessment["intervention"],
                "monitoring_guidance": pain_assessment["monitoring"],
                "reassessment_timing": pain_assessment["reassessment"],
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": pain_assessment["interpretation"],
            "stage": pain_assessment["level"],
            "stage_description": pain_assessment["description"]
        }
    
    def _validate_inputs(self, cry, facial, verbal, torso, touch, legs):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "cry": ["no_crying", "moaning_crying", "screaming"],
            "facial": ["smiling", "composed", "grimace"],
            "verbal": ["positive", "not_talking_other", "pain_complaints"],
            "torso": ["neutral", "shifting_tense"],
            "touch": ["not_touching", "reaching_touching"],
            "legs": ["neutral", "squirming_tensed"]
        }
        
        # Validate each parameter
        parameters = [
            ("cry", cry),
            ("facial", facial),
            ("verbal", verbal),
            ("torso", torso),
            ("touch", touch),
            ("legs", legs)
        ]
        
        for param_name, param_value in parameters:
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of {valid_options[param_name]}")
    
    def _get_pain_assessment(self, score: int) -> Dict[str, Any]:
        """
        Determines pain level and clinical recommendations based on CHEOPS score
        
        Args:
            score: Total CHEOPS score (4-13)
            
        Returns:
            Dict with pain assessment and clinical guidance
        """
        
        if score == 4:
            level = "No Pain"
            description = "Minimal discomfort"
            intervention_required = False
            intervention = "No analgesic intervention required"
            monitoring = "Continue routine monitoring and comfort measures"
            reassessment = "Every 3 hours or as clinically indicated"
            interpretation = f"CHEOPS Score {score}: No significant pain. Continue routine post-operative care with standard monitoring. No analgesic intervention required at this time."
            
        elif 5 <= score <= 7:
            level = "Mild to Moderate Pain"
            description = "Consider analgesic intervention"
            intervention_required = True
            intervention = "Consider administering analgesic medication"
            monitoring = "Reassess pain level after intervention and provide comfort measures"
            reassessment = "15-20 minutes after IV analgesics or 30-45 minutes after oral/rectal analgesics"
            interpretation = f"CHEOPS Score {score}: Mild to moderate pain detected. Consider administering appropriate analgesic medication and reassess effectiveness."
            
        else:  # score >= 8
            level = "Severe Pain"
            description = "Analgesic intervention required"
            intervention_required = True
            intervention = "Analgesic medication required immediately"
            monitoring = "Implement comprehensive pain management strategies and frequent monitoring"
            reassessment = "Frequent reassessment until adequate pain control achieved"
            interpretation = f"CHEOPS Score {score}: Severe pain requiring immediate intervention. Administer appropriate analgesic medication and implement comprehensive pain management strategies."
        
        return {
            "level": level,
            "description": description,
            "intervention_required": intervention_required,
            "intervention": intervention,
            "monitoring": monitoring,
            "reassessment": reassessment,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, cry, cry_pts, facial, facial_pts, verbal, verbal_pts, torso, torso_pts, touch, touch_pts, legs, legs_pts):
        """Provides detailed scoring breakdown"""
        
        # Category descriptions
        category_descriptions = {
            "cry": {
                "no_crying": "No crying",
                "moaning_crying": "Moaning or crying",
                "screaming": "Screaming"
            },
            "facial": {
                "smiling": "Smiling",
                "composed": "Composed/neutral expression",
                "grimace": "Grimace or frowning"
            },
            "verbal": {
                "positive": "Positive statements or compliant",
                "not_talking_other": "Not talking or other complaints",
                "pain_complaints": "Pain complaints"
            },
            "torso": {
                "neutral": "Neutral position, resting comfortably",
                "shifting_tense": "Shifting, tense, shivering, upright, or restrained"
            },
            "touch": {
                "not_touching": "Not touching or reaching toward wound",
                "reaching_touching": "Reaching toward, touching, or grabbing wound"
            },
            "legs": {
                "neutral": "Neutral position, relaxed",
                "squirming_tensed": "Squirming, tensed, standing, or restrained"
            }
        }
        
        breakdown = {
            "component_scores": {
                "cry": {
                    "behavior": category_descriptions["cry"][cry],
                    "points": cry_pts,
                    "description": "Vocal response and crying behavior"
                },
                "facial": {
                    "behavior": category_descriptions["facial"][facial],
                    "points": facial_pts,
                    "description": "Facial expression assessment"
                },
                "verbal": {
                    "behavior": category_descriptions["verbal"][verbal],
                    "points": verbal_pts,
                    "description": "Verbal responses and complaints"
                },
                "torso": {
                    "behavior": category_descriptions["torso"][torso],
                    "points": torso_pts,
                    "description": "Body position and movement"
                },
                "touch": {
                    "behavior": category_descriptions["touch"][touch],
                    "points": touch_pts,
                    "description": "Wound evaluation and touching behavior"
                },
                "legs": {
                    "behavior": category_descriptions["legs"][legs],
                    "points": legs_pts,
                    "description": "Leg position and movement"
                }
            },
            "scoring_criteria": {
                "cry": "No crying (1 pt), Moaning/crying (2 pts), Screaming (3 pts)",
                "facial": "Smiling (0 pts), Composed (1 pt), Grimace (2 pts)",
                "verbal": "Positive (0 pts), Not talking/other (1 pt), Pain complaints (2 pts)",
                "torso": "Neutral (1 pt), Shifting/tense (2 pts)",
                "touch": "Not touching wound (1 pt), Reaching/touching wound (2 pts)",
                "legs": "Neutral position (1 pt), Squirming/tensed (2 pts)"
            },
            "clinical_context": {
                "age_range": "Designed for children aged 1-5 years",
                "setting": "Post-operative pain assessment",
                "timing": "Assess every 3 hours during post-operative period",
                "reassessment": "15-20 min after IV or 30-45 min after oral/rectal analgesics",
                "limitations": "Requires direct behavioral observation; not validated for procedural pain"
            },
            "interpretation_thresholds": {
                "no_intervention": "Score 4: No analgesic intervention required",
                "consider_analgesic": "Score 5-7: Consider administering analgesic",
                "immediate_intervention": "Score 8-13: Analgesic medication required immediately"
            }
        }
        
        return breakdown


def calculate_cheops_pain_scale(
    cry: str,
    facial: str,
    verbal: str,
    torso: str,
    touch: str,
    legs: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CheopsPainScaleCalculator()
    return calculator.calculate(
        cry=cry,
        facial=facial,
        verbal=verbal,
        torso=torso,
        touch=touch,
        legs=legs
    )