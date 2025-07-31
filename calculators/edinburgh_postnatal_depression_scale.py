"""
Edinburgh Postnatal Depression Scale (EPDS) Calculator

Screens for depression in the postnatal period through a validated 10-item self-report 
questionnaire. The most widely used postpartum depression screening tool worldwide, 
also valid for antenatal screening.

References:
1. Cox JL, Holden JM, Sagovsky R. Detection of postnatal depression. Development of the 
   10-item Edinburgh Postnatal Depression Scale. Br J Psychiatry. 1987;150:782-6. 
   doi: 10.1192/bjp.150.6.782.
2. Levis B, Negeri Z, Sun Y, Benedetti A, Thombs BD; DEPRESsion Screening Data (DEPRESSD) 
   EPDS Group. Accuracy of the Edinburgh Postnatal Depression Scale (EPDS) for screening to 
   detect major depression among pregnant and postpartum women: systematic review and 
   meta-analysis of individual participant data. BMJ. 2020;371:m4022. doi: 10.1136/bmj.m4022.
"""

from typing import Dict, Any


class EdinburghPostnatalDepressionScaleCalculator:
    """Calculator for Edinburgh Postnatal Depression Scale (EPDS)"""
    
    def __init__(self):
        # EPDS question definitions with scoring instructions
        self.QUESTIONS = {
            'able_to_laugh': {
                'text': 'I have been able to laugh and see the funny side of things',
                'reverse_scored': True,
                'options': {
                    0: 'As much as I always could',
                    1: 'Not quite so much now',
                    2: 'Definitely not so much now',
                    3: 'Not at all'
                }
            },
            'looked_forward': {
                'text': 'I have looked forward with enjoyment to things',
                'reverse_scored': True,
                'options': {
                    0: 'As much as I ever did',
                    1: 'Rather less than I used to',
                    2: 'Definitely less than I used to',
                    3: 'Hardly at all'
                }
            },
            'blamed_myself': {
                'text': 'I have blamed myself unnecessarily when things went wrong',
                'reverse_scored': False,
                'options': {
                    0: 'No, never',
                    1: 'Not very often',
                    2: 'Yes, some of the time',
                    3: 'Yes, most of the time'
                }
            },
            'anxious_worried': {
                'text': 'I have been anxious or worried for no good reason',
                'reverse_scored': True,
                'options': {
                    0: 'No, not at all',
                    1: 'Hardly ever',
                    2: 'Yes, sometimes',
                    3: 'Yes, very often'
                }
            },
            'scared_panicky': {
                'text': 'I have felt scared or panicky for no very good reason',
                'reverse_scored': False,
                'options': {
                    0: 'No, not at all',
                    1: 'No, not much',
                    2: 'Yes, sometimes',
                    3: 'Yes, quite a lot'
                }
            },
            'things_on_top': {
                'text': 'Things have been getting on top of me',
                'reverse_scored': False,
                'options': {
                    0: 'No, I have been coping as well as ever',
                    1: 'No, most of the time I have coped quite well',
                    2: 'Yes, sometimes I have not been coping as well as usual',
                    3: 'Yes, most of the time I have not been able to cope at all'
                }
            },
            'unhappy_sleeping': {
                'text': 'I have been so unhappy that I have had difficulty sleeping',
                'reverse_scored': False,
                'options': {
                    0: 'No, not at all',
                    1: 'Not very often',
                    2: 'Yes, sometimes',
                    3: 'Yes, most of the time'
                }
            },
            'sad_miserable': {
                'text': 'I have felt sad or miserable',
                'reverse_scored': False,
                'options': {
                    0: 'No, not at all',
                    1: 'Not very often',
                    2: 'Yes, quite often',
                    3: 'Yes, most of the time'
                }
            },
            'unhappy_crying': {
                'text': 'I have been so unhappy that I have been crying',
                'reverse_scored': False,
                'options': {
                    0: 'No, never',
                    1: 'Only occasionally',
                    2: 'Yes, quite often',
                    3: 'Yes, most of the time'
                }
            },
            'self_harm_thoughts': {
                'text': 'The thought of harming myself has occurred to me',
                'reverse_scored': False,
                'options': {
                    0: 'Never',
                    1: 'Hardly ever',
                    2: 'Sometimes',
                    3: 'Yes, quite often'
                }
            }
        }
        
        # Items that are reverse scored (higher response = lower score)
        self.REVERSE_SCORED_ITEMS = ['able_to_laugh', 'looked_forward', 'anxious_worried']
        
        # Risk thresholds based on latest research
        self.RISK_THRESHOLDS = {
            'low': (0, 9),      # Minimal symptoms
            'moderate': (10, 12), # Possible depression
            'high': (13, 30)    # Likely depression
        }
    
    def calculate(self, able_to_laugh: int, looked_forward: int, blamed_myself: int,
                  anxious_worried: int, scared_panicky: int, things_on_top: int,
                  unhappy_sleeping: int, sad_miserable: int, unhappy_crying: int,
                  self_harm_thoughts: int) -> Dict[str, Any]:
        """
        Calculates the EPDS score using the provided parameters
        
        Args:
            able_to_laugh (int): I have been able to laugh and see the funny side of things (0-3, reverse scored)
            looked_forward (int): I have looked forward with enjoyment to things (0-3, reverse scored)
            blamed_myself (int): I have blamed myself unnecessarily when things went wrong (0-3)
            anxious_worried (int): I have been anxious or worried for no good reason (0-3, reverse scored)
            scared_panicky (int): I have felt scared or panicky for no very good reason (0-3)
            things_on_top (int): Things have been getting on top of me (0-3)
            unhappy_sleeping (int): I have been so unhappy that I have had difficulty sleeping (0-3)
            sad_miserable (int): I have felt sad or miserable (0-3)
            unhappy_crying (int): I have been so unhappy that I have been crying (0-3)
            self_harm_thoughts (int): The thought of harming myself has occurred to me (0-3)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'able_to_laugh': able_to_laugh,
            'looked_forward': looked_forward,
            'blamed_myself': blamed_myself,
            'anxious_worried': anxious_worried,
            'scared_panicky': scared_panicky,
            'things_on_top': things_on_top,
            'unhappy_sleeping': unhappy_sleeping,
            'sad_miserable': sad_miserable,
            'unhappy_crying': unhappy_crying,
            'self_harm_thoughts': self_harm_thoughts
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate EPDS score
        epds_score = self._calculate_epds_score(parameters)
        
        # Check for self-harm risk
        self_harm_risk = self._assess_self_harm_risk(parameters['self_harm_thoughts'])
        
        # Get interpretation
        interpretation = self._get_interpretation(epds_score, self_harm_risk)
        
        return {
            "result": epds_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"Parameter '{param_name}' must be an integer")
            
            if value < 0 or value > 3:
                raise ValueError(f"Parameter '{param_name}' must be between 0 and 3, got {value}")
    
    def _calculate_epds_score(self, parameters: Dict[str, Any]) -> int:
        """Calculates the EPDS total score with proper reverse scoring"""
        
        total_score = 0
        
        for item_name, raw_score in parameters.items():
            if item_name in self.REVERSE_SCORED_ITEMS:
                # Reverse score: 0=3, 1=2, 2=1, 3=0
                scored_value = 3 - raw_score
            else:
                # Regular scoring: score as marked
                scored_value = raw_score
            
            total_score += scored_value
        
        return total_score
    
    def _assess_self_harm_risk(self, self_harm_score: int) -> Dict[str, Any]:
        """Assesses self-harm risk based on question 10"""
        
        if self_harm_score == 0:
            return {
                "risk_present": False,
                "risk_level": "No risk",
                "immediate_action": False
            }
        elif self_harm_score == 1:
            return {
                "risk_present": True,
                "risk_level": "Low risk",
                "immediate_action": True
            }
        elif self_harm_score == 2:
            return {
                "risk_present": True,
                "risk_level": "Moderate risk",
                "immediate_action": True
            }
        else:  # self_harm_score == 3
            return {
                "risk_present": True,
                "risk_level": "High risk",
                "immediate_action": True
            }
    
    def _get_interpretation(self, epds_score: int, self_harm_risk: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines the interpretation based on the EPDS score and self-harm risk
        
        Args:
            epds_score (int): Calculated EPDS score
            self_harm_risk (Dict): Self-harm risk assessment
            
        Returns:
            Dict with interpretation
        """
        
        # Determine primary risk category based on score
        if epds_score <= 9:
            base_interpretation = {
                "stage": "Low Risk",
                "description": "Minimal depression symptoms",
                "base_text": ("Low risk for depression. Score suggests minimal depressive symptoms. "
                            "Continue routine care and screening. Provide general postpartum support "
                            "and education about warning signs of depression.")
            }
        elif epds_score <= 12:
            base_interpretation = {
                "stage": "Moderate Risk", 
                "description": "Possible depression - further assessment needed",
                "base_text": ("Moderate risk for depression. Score suggests possible depressive symptoms "
                            "requiring further evaluation. Consider clinical assessment by healthcare "
                            "provider within 2 weeks. Provide mental health resources and support information.")
            }
        else:  # epds_score >= 13
            base_interpretation = {
                "stage": "High Risk",
                "description": "Likely depression - clinical assessment recommended", 
                "base_text": ("High risk for depression. Score indicates likely depressive symptoms requiring "
                            "clinical assessment and potential intervention. Refer to healthcare provider, "
                            "preferably general practitioner or mental health professional, for comprehensive "
                            "evaluation and treatment planning.")
            }
        
        # Add self-harm risk considerations
        interpretation_text = base_interpretation["base_text"]
        
        if self_harm_risk["risk_present"]:
            if self_harm_risk["risk_level"] == "Low risk":
                interpretation_text += (" IMPORTANT: Patient endorsed thoughts of self-harm (low frequency). "
                                      "Safety assessment required. Consider same-day clinical evaluation and "
                                      "provide crisis resources and support.")
            elif self_harm_risk["risk_level"] == "Moderate risk":
                interpretation_text += (" URGENT: Patient endorsed thoughts of self-harm (moderate frequency). "
                                      "Immediate safety assessment required. Arrange prompt clinical evaluation "
                                      "within 24 hours. Provide crisis hotline information and ensure support system activated.")
            else:  # High risk
                interpretation_text += (" CRITICAL: Patient endorsed frequent thoughts of self-harm. "
                                      "Immediate safety assessment and intervention required. Consider emergency "
                                      "psychiatric evaluation. Do not leave patient alone. Activate crisis protocols "
                                      "and provide immediate crisis resources.")
        
        # Add general follow-up recommendations
        if epds_score >= 13:
            interpretation_text += (" Recommend rescreening in 2-4 weeks if clinical assessment indicates "
                                   "ongoing monitoring is appropriate.")
        
        return {
            "stage": base_interpretation["stage"],
            "description": base_interpretation["description"],
            "interpretation": interpretation_text
        }


def calculate_edinburgh_postnatal_depression_scale(able_to_laugh: int, looked_forward: int, blamed_myself: int,
                                                 anxious_worried: int, scared_panicky: int, things_on_top: int,
                                                 unhappy_sleeping: int, sad_miserable: int, unhappy_crying: int,
                                                 self_harm_thoughts: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_edinburgh_postnatal_depression_scale pattern
    """
    calculator = EdinburghPostnatalDepressionScaleCalculator()
    return calculator.calculate(able_to_laugh, looked_forward, blamed_myself,
                              anxious_worried, scared_panicky, things_on_top,
                              unhappy_sleeping, sad_miserable, unhappy_crying,
                              self_harm_thoughts)