"""
Children's Hospital of Eastern Ontario Pain Scale (CHEOPS) Models

Request and response models for CHEOPS pain scale calculation.

References (Vancouver style):
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

The Children's Hospital of Eastern Ontario Pain Scale (CHEOPS) is a behavioral pain 
assessment tool designed specifically for post-operative pain evaluation in pediatric 
patients aged 1-5 years. This observational scale quantifies pain through systematic 
assessment of six behavioral categories, providing objective guidance for analgesic 
management in the post-operative setting.

CHEOPS Behavioral Assessment Categories:

Cry (1-3 points):
- No crying (1 point): Child is not crying or vocalizing distress
- Moaning/crying (2 points): Child is moaning, whimpering, or crying intermittently
- Screaming (3 points): Child is screaming, crying loudly, or exhibiting intense vocal distress

Facial Expression (0-2 points):
- Smiling (0 points): Child appears happy, content, or smiling
- Composed/neutral (1 point): Child has neutral facial expression, appears calm
- Grimace (2 points): Child is frowning, grimacing, or showing facial tension

Verbal Response (0-2 points):
- Positive statements (0 points): Child makes positive comments or appears compliant
- Not talking/other complaints (1 point): Child is silent or makes non-pain related complaints
- Pain complaints (2 points): Child verbalizes pain, discomfort, or requests help

Torso Position (1-2 points):
- Neutral (1 point): Child is in neutral position, resting comfortably
- Shifting/tense (2 points): Child is shifting, tense, shivering, sitting upright, or restrained

Touch/Wound Evaluation (1-2 points):
- Not touching wound (1 point): Child is not reaching toward or touching surgical site
- Reaching/touching wound (2 points): Child is reaching toward, touching, or grabbing wound area

Legs Position (1-2 points):
- Neutral position (1 point): Child's legs are in neutral, relaxed position
- Squirming/tensed (2 points): Child is squirming, legs tensed, standing, or restrained

Clinical Interpretation Guidelines:

Score 4 (Minimum Score): No Pain
- Clinical significance: Minimal or no pain present
- Intervention: No analgesic intervention required
- Monitoring: Continue routine post-operative monitoring and comfort measures
- Reassessment: Every 3 hours or as clinically indicated

Score 5-7: Mild to Moderate Pain
- Clinical significance: Pain present, consider intervention
- Intervention: Consider administering appropriate analgesic medication
- Monitoring: Reassess pain level after intervention, provide comfort measures
- Reassessment: 15-20 minutes after IV analgesics, 30-45 minutes after oral/rectal

Score 8-13 (Maximum Score): Severe Pain
- Clinical significance: Significant pain requiring immediate intervention
- Intervention: Analgesic medication required immediately
- Monitoring: Implement comprehensive pain management strategies
- Reassessment: Frequent reassessment until adequate pain control achieved

Clinical Applications:
- Post-operative pain assessment in pediatric surgical patients
- Standardized pain evaluation for children unable to self-report
- Objective tool for analgesic decision-making
- Quality improvement in pediatric pain management
- Research applications in pediatric pain studies

Assessment Guidelines:
- Perform systematic observation of all six behavioral categories
- Assess child in natural state without stimulation when possible
- Consider developmental age and individual behavioral patterns
- Use in conjunction with physiological indicators when available
- Document observations and interventions systematically

Limitations and Considerations:
- Requires direct behavioral observation by trained healthcare provider
- Not validated for procedural pain assessment (designed for post-operative use)
- May have limited validity beyond immediate post-operative period
- Individual behavioral variations may affect scoring accuracy
- Should be interpreted within broader clinical context
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CheopsPainScaleRequest(BaseModel):
    """
    Request model for Children's Hospital of Eastern Ontario Pain Scale (CHEOPS)
    
    The CHEOPS scale assesses post-operative pain in pediatric patients aged 1-5 years 
    through systematic behavioral observation. Each of the six behavioral categories 
    is scored based on observed behaviors, with higher scores indicating greater pain 
    intensity and need for intervention.
    
    Behavioral Assessment Categories:
    
    Cry Assessment:
    Evaluates vocal responses and crying behavior as indicators of pain intensity.
    Scoring provides progressive assessment from no distress to severe vocal distress.
    - No crying: Child is quiet, not vocalizing distress (1 point)
    - Moaning/crying: Intermittent moaning, whimpering, or mild crying (2 points)  
    - Screaming: Loud crying, screaming, or intense vocal distress (3 points)
    
    Facial Expression Assessment:
    Assesses facial expressions that correlate with pain intensity and emotional state.
    Facial expressions are reliable indicators of pain in non-verbal children.
    - Smiling: Happy, content facial expression (0 points)
    - Composed/neutral: Calm, neutral facial expression (1 point)
    - Grimace: Frowning, grimacing, facial tension indicating distress (2 points)
    
    Verbal Response Assessment:
    Evaluates verbal communications related to pain and comfort level.
    Considers developmental stage and verbal capacity of individual child.
    - Positive statements: Positive comments, appears compliant and comfortable (0 points)
    - Not talking/other: Silent or non-pain related complaints (1 point)
    - Pain complaints: Verbalizes pain, discomfort, or requests for help (2 points)
    
    Torso Position Assessment:
    Observes body positioning and posture as indicators of comfort and pain.
    Physical positioning often reflects attempts to minimize pain or discomfort.
    - Neutral: Comfortable resting position, appears relaxed (1 point)
    - Shifting/tense: Restless, tense, shivering, upright, or requires restraint (2 points)
    
    Touch/Wound Interaction Assessment:
    Evaluates child's interaction with surgical site or wound area.
    Protective behaviors toward wound often indicate pain and discomfort.
    - Not touching: No reaching toward or touching of wound area (1 point)
    - Reaching/touching: Reaching toward, touching, or protecting wound area (2 points)
    
    Legs Position Assessment:
    Assesses leg positioning and movement patterns related to pain response.
    Lower extremity positioning can indicate overall comfort and pain level.
    - Neutral: Legs in relaxed, comfortable position (1 point)
    - Squirming/tensed: Squirming, tensed legs, standing, or requires restraint (2 points)
    
    Clinical Context and Implementation:
    
    Target Population:
    - Age range: 1-5 years (preschool children)
    - Post-operative patients in recovery or ward settings
    - Children unable to reliably self-report pain intensity
    - Both verbal and non-verbal pediatric patients
    
    Assessment Timing:
    - Routine assessment every 3 hours during post-operative period
    - Reassessment 15-20 minutes after intravenous analgesics
    - Reassessment 30-45 minutes after oral or rectal analgesics  
    - Additional assessments based on clinical judgment and patient needs
    
    Observer Requirements:
    - Trained healthcare providers familiar with pediatric behavior
    - Understanding of normal developmental behaviors for age group
    - Ability to observe child in natural state without unnecessary stimulation
    - Knowledge of individual patient's baseline behaviors when possible
    
    Clinical Decision Framework:
    The CHEOPS score guides analgesic intervention decisions:
    - Score 4: Routine monitoring, no intervention typically required
    - Score 5-7: Consider analgesic intervention based on clinical judgment
    - Score 8-13: Immediate analgesic intervention recommended
    
    Quality Considerations:
    - Systematic observation of all six behavioral categories required
    - Consider developmental variations in behavioral expression
    - Integrate with other clinical indicators (vital signs, medical history)
    - Document assessment findings and interventions systematically
    - Reassess effectiveness of pain management interventions
    
    References (Vancouver style):
    1. McGrath PJ, Johnson G, Goodman JT, Schillinger J, Dunn J, Chapman J. CHEOPS: a 
    behavioral scale for rating postoperative pain in children. In: Fields HL, Dubner R, 
    Cervero F, editors. Advances in pain research and therapy. New York: Raven Press; 1985. 
    p. 395-402.
    2. Suraseranivongse S, Santawat U, Kraiprasit K, Petcharatana S, Prakkamodom S, Muntraporn N. 
    Cross-validation of a composite pain scale for preschool children within 24 hours of 
    surgery. Br J Anaesth. 2001 Sep;87(3):400-5.
    """
    
    cry: Literal["no_crying", "moaning_crying", "screaming"] = Field(
        ...,
        description="Vocal response assessment. No crying (1 pt), moaning/crying (2 pts), screaming (3 pts)",
        example="moaning_crying"
    )
    
    facial: Literal["smiling", "composed", "grimace"] = Field(
        ...,
        description="Facial expression assessment. Smiling (0 pts), composed/neutral (1 pt), grimace (2 pts)",
        example="composed"
    )
    
    verbal: Literal["positive", "not_talking_other", "pain_complaints"] = Field(
        ...,
        description="Verbal response assessment. Positive statements (0 pts), not talking/other (1 pt), pain complaints (2 pts)",
        example="not_talking_other"
    )
    
    torso: Literal["neutral", "shifting_tense"] = Field(
        ...,
        description="Body position assessment. Neutral/resting (1 pt), shifting/tense/restrained (2 pts)",
        example="shifting_tense"
    )
    
    touch: Literal["not_touching", "reaching_touching"] = Field(
        ...,
        description="Wound interaction assessment. Not touching wound (1 pt), reaching/touching wound (2 pts)",
        example="not_touching"
    )
    
    legs: Literal["neutral", "squirming_tensed"] = Field(
        ...,
        description="Leg position assessment. Neutral position (1 pt), squirming/tensed/restrained (2 pts)",
        example="neutral"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cry": "moaning_crying",
                "facial": "composed", 
                "verbal": "not_talking_other",
                "torso": "shifting_tense",
                "touch": "not_touching",
                "legs": "neutral"
            }
        }


class CheopsPainScaleResponse(BaseModel):
    """
    Response model for Children's Hospital of Eastern Ontario Pain Scale (CHEOPS)
    
    The CHEOPS response provides comprehensive pain assessment with clinical guidance 
    for post-operative pain management in pediatric patients. The scale ranges from 
    4-13 points and provides evidence-based recommendations for analgesic intervention.
    
    Pain Level Classifications:
    
    No Pain (Score 4):
    - Clinical significance: Minimal or no pain present
    - Patient presentation: Child appears comfortable, relaxed, not distressed
    - Intervention guidance: No analgesic intervention typically required
    - Monitoring approach: Continue routine post-operative monitoring and comfort measures
    - Reassessment frequency: Every 3 hours or as clinically indicated
    - Family education: Normal post-operative recovery, continue comfort measures
    
    Mild to Moderate Pain (Score 5-7):
    - Clinical significance: Pain present requiring clinical judgment for intervention
    - Patient presentation: Some distress behaviors present, variable comfort level
    - Intervention guidance: Consider administering appropriate analgesic medication
    - Monitoring approach: Reassess pain level after intervention, provide comfort measures
    - Reassessment frequency: 15-20 minutes after IV, 30-45 minutes after PO/PR analgesics
    - Clinical considerations: Evaluate pain versus anxiety, consider non-pharmacologic measures
    
    Severe Pain (Score 8-13):
    - Clinical significance: Significant pain requiring immediate intervention
    - Patient presentation: Multiple distress behaviors, clear pain indicators
    - Intervention guidance: Analgesic medication required immediately
    - Monitoring approach: Comprehensive pain management strategies, frequent monitoring
    - Reassessment frequency: Frequent reassessment until adequate pain control achieved
    - Clinical escalation: Consider multimodal pain management, specialist consultation
    
    Clinical Implementation Framework:
    
    Assessment Protocol:
    - Systematic observation of all six behavioral categories
    - Observe child in natural state when possible (avoid stimulation during assessment)
    - Consider individual developmental and behavioral patterns
    - Document specific behaviors observed in each category
    - Integrate with physiological indicators when available
    
    Intervention Guidelines:
    - Score-based recommendations provide starting point for clinical decision-making
    - Consider individual patient factors: age, developmental stage, medical history
    - Evaluate effectiveness of previous interventions
    - Implement age-appropriate comfort measures alongside pharmacologic interventions
    - Consider family preferences and cultural factors in pain management approach
    
    Quality Improvement Applications:
    - Standardized pain assessment across pediatric units
    - Performance metrics for adequate pain management
    - Training tool for healthcare providers in pediatric pain recognition
    - Research applications for pediatric pain management studies
    - Documentation support for pain management protocols
    
    Multidisciplinary Considerations:
    
    Nursing Implications:
    - Primary assessment tool for bedside pain evaluation
    - Guide for timing and effectiveness of analgesic administration
    - Support for family education about pain management
    - Documentation framework for pain assessment and interventions
    
    Physician Decision-Making:
    - Objective data for analgesic prescribing decisions
    - Standardized communication about pain levels
    - Evidence base for pain management plan modifications
    - Support for discharge planning and pain management education
    
    Family Education and Involvement:
    - Help families understand pain assessment process
    - Teach recognition of pain behaviors in children
    - Support for home pain management planning
    - Improve communication between families and healthcare team
    
    Special Considerations:
    
    Developmental Factors:
    - Consider normal behavioral patterns for age group
    - Account for individual developmental variations
    - Recognize impact of hospitalization and separation anxiety
    - Differentiate pain behaviors from general distress
    
    Clinical Context:
    - Integrate with other clinical indicators (vital signs, medical condition)
    - Consider surgical procedure type and expected pain trajectory
    - Account for pre-existing conditions affecting pain expression
    - Evaluate effectiveness within broader recovery context
    
    Limitations and Clinical Judgment:
    - Tool provides objective framework but requires clinical interpretation
    - Individual variations in pain expression must be considered
    - Not validated for procedural pain (designed for post-operative assessment)
    - Should be used alongside other pain assessment methods when available
    
    Reference: McGrath PJ, et al. Advances in pain research and therapy. 1985:395-402.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CHEOPS assessment including score, pain level, and clinical recommendations",
        example={
            "total_score": 7,
            "pain_level": "Mild to Moderate Pain",
            "intervention_required": True,
            "clinical_recommendation": "Consider administering analgesic medication",
            "monitoring_guidance": "Reassess pain level after intervention and provide comfort measures",
            "reassessment_timing": "15-20 minutes after IV analgesics or 30-45 minutes after oral/rectal analgesics",
            "scoring_breakdown": {
                "component_scores": {
                    "cry": {
                        "behavior": "Moaning or crying",
                        "points": 2,
                        "description": "Vocal response and crying behavior"
                    },
                    "facial": {
                        "behavior": "Composed/neutral expression",
                        "points": 1,
                        "description": "Facial expression assessment"
                    },
                    "verbal": {
                        "behavior": "Not talking or other complaints",
                        "points": 1,
                        "description": "Verbal responses and complaints"
                    },
                    "torso": {
                        "behavior": "Shifting, tense, shivering, upright, or restrained",
                        "points": 2,
                        "description": "Body position and movement"
                    },
                    "touch": {
                        "behavior": "Not touching or reaching toward wound",
                        "points": 1,
                        "description": "Wound evaluation and touching behavior"
                    },
                    "legs": {
                        "behavior": "Neutral position, relaxed",
                        "points": 1,
                        "description": "Leg position and movement"
                    }
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with pain level assessment and intervention recommendations",
        example="CHEOPS Score 7: Mild to moderate pain detected. Consider administering appropriate analgesic medication and reassess effectiveness."
    )
    
    stage: str = Field(
        ...,
        description="Pain level classification (No Pain, Mild to Moderate Pain, Severe Pain)",
        example="Mild to Moderate Pain"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the pain level category",
        example="Consider analgesic intervention"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 7,
                    "pain_level": "Mild to Moderate Pain",
                    "intervention_required": True,
                    "clinical_recommendation": "Consider administering analgesic medication",
                    "monitoring_guidance": "Reassess pain level after intervention and provide comfort measures",
                    "reassessment_timing": "15-20 minutes after IV analgesics or 30-45 minutes after oral/rectal analgesics",
                    "scoring_breakdown": {
                        "component_scores": {
                            "cry": {
                                "behavior": "Moaning or crying",
                                "points": 2,
                                "description": "Vocal response and crying behavior"
                            },
                            "facial": {
                                "behavior": "Composed/neutral expression",
                                "points": 1,
                                "description": "Facial expression assessment"
                            },
                            "verbal": {
                                "behavior": "Not talking or other complaints",
                                "points": 1,
                                "description": "Verbal responses and complaints"
                            },
                            "torso": {
                                "behavior": "Shifting, tense, shivering, upright, or restrained",
                                "points": 2,
                                "description": "Body position and movement"
                            },
                            "touch": {
                                "behavior": "Not touching or reaching toward wound",
                                "points": 1,
                                "description": "Wound evaluation and touching behavior"
                            },
                            "legs": {
                                "behavior": "Neutral position, relaxed",
                                "points": 1,
                                "description": "Leg position and movement"
                            }
                        }
                    }
                },
                "unit": "points",
                "interpretation": "CHEOPS Score 7: Mild to moderate pain detected. Consider administering appropriate analgesic medication and reassess effectiveness.",
                "stage": "Mild to Moderate Pain",
                "stage_description": "Consider analgesic intervention"
            }
        }