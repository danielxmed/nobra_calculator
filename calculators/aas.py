"""
Abuse Assessment Screen (AAS) Calculator

Detects domestic abuse (intimate partner violence) in pregnant
and non-pregnant women in healthcare settings.
"""

from typing import Dict, Any


class AasCalculator:
    """Calculator for Abuse Assessment Screen (AAS)"""
    
    def calculate(self, emotional_physical_abuse: str, physical_hurt_recently: str,
                 physical_hurt_pregnancy: str, sexual_abuse: str, 
                 afraid_of_partner: str) -> Dict[str, Any]:
        """
        Calculates the AAS result
        
        Args:
            emotional_physical_abuse (str): History of emotional/physical abuse ("yes" or "no")
            physical_hurt_recently (str): Recent physical harm ("yes" or "no")
            physical_hurt_pregnancy (str): Harm during pregnancy ("yes", "no", or "not_applicable")
            sexual_abuse (str): Sexual abuse in the last year ("yes" or "no")
            afraid_of_partner (str): Fear of partner ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(
            emotional_physical_abuse, physical_hurt_recently, 
            physical_hurt_pregnancy, sexual_abuse, afraid_of_partner
        )
        
        # Count positive responses (excluding "not_applicable")
        positive_responses = 0
        responses_details = {}
        
        # Question 1: Historical emotional/physical abuse
        if emotional_physical_abuse == "yes":
            positive_responses += 1
            responses_details["emotional_physical_abuse"] = True
        else:
            responses_details["emotional_physical_abuse"] = False
        
        # Question 2: Recent physical harm
        if physical_hurt_recently == "yes":
            positive_responses += 1
            responses_details["physical_hurt_recently"] = True
        else:
            responses_details["physical_hurt_recently"] = False
        
        # Question 3: Harm during pregnancy
        if physical_hurt_pregnancy == "yes":
            positive_responses += 1
            responses_details["physical_hurt_pregnancy"] = True
        elif physical_hurt_pregnancy == "no":
            responses_details["physical_hurt_pregnancy"] = False
        else:  # "not_applicable"
            responses_details["physical_hurt_pregnancy"] = None
        
        # Question 4: Sexual abuse
        if sexual_abuse == "yes":
            positive_responses += 1
            responses_details["sexual_abuse"] = True
        else:
            responses_details["sexual_abuse"] = False
        
        # Question 5: Fear of partner
        if afraid_of_partner == "yes":
            positive_responses += 1
            responses_details["afraid_of_partner"] = True
        else:
            responses_details["afraid_of_partner"] = False
        
        # Determine screening result
        is_positive = positive_responses > 0
        
        # Get interpretation
        interpretation = self._get_interpretation(is_positive, positive_responses)
        
        # Assess risk
        risk_assessment = self._assess_risk(positive_responses, responses_details)
        
        return {
            "result": "Positive" if is_positive else "Negative",
            "unit": "result",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "positive_responses_count": positive_responses,
            "is_positive": is_positive,
            "responses_details": responses_details,
            "risk_assessment": risk_assessment
        }
    
    def _validate_inputs(self, emotional_physical_abuse, physical_hurt_recently,
                        physical_hurt_pregnancy, sexual_abuse, afraid_of_partner):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_pregnancy = ["yes", "no", "not_applicable"]
        
        if emotional_physical_abuse not in valid_yes_no:
            raise ValueError(f"emotional_physical_abuse must be: {', '.join(valid_yes_no)}")
        
        if physical_hurt_recently not in valid_yes_no:
            raise ValueError(f"physical_hurt_recently must be: {', '.join(valid_yes_no)}")
        
        if physical_hurt_pregnancy not in valid_pregnancy:
            raise ValueError(f"physical_hurt_pregnancy must be: {', '.join(valid_pregnancy)}")
        
        if sexual_abuse not in valid_yes_no:
            raise ValueError(f"sexual_abuse must be: {', '.join(valid_yes_no)}")
        
        if afraid_of_partner not in valid_yes_no:
            raise ValueError(f"afraid_of_partner must be: {', '.join(valid_yes_no)}")
    
    def _assess_risk(self, positive_responses: int, responses_details: Dict) -> Dict[str, Any]:
        """
        Assesses risk based on responses
        
        Args:
            positive_responses (int): Number of positive responses
            responses_details (Dict): Details of responses
            
        Returns:
            Dict with risk assessment
        """
        
        if positive_responses == 0:
            return {
                "level": "low",
                "description": "No indicators of domestic violence",
                "recommendation": "Continue routine monitoring"
            }
        elif positive_responses == 1:
            return {
                "level": "moderate",
                "description": "One indicator of domestic violence",
                "recommendation": "Further investigation recommended"
            }
        elif positive_responses <= 3:
            return {
                "level": "high",
                "description": "Multiple indicators of domestic violence",
                "recommendation": "Immediate assessment and referral to specialized resources"
            }
        else:
            return {
                "level": "very high",
                "description": "Multiple severe indicators of domestic violence",
                "recommendation": "Immediate intervention, safety plan, and urgent referral"
            }
    
    def _get_interpretation(self, is_positive: bool, positive_responses: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            is_positive (bool): Whether the result is positive
            positive_responses (int): Number of positive responses
            
        Returns:
            Dict with clinical interpretation
        """
        
        if not is_positive:
            return {
                "stage": "Negative Screening",
                "description": "No indication of domestic abuse",
                "interpretation": "Negative result for domestic violence. Continue to offer support and information about available resources. Re-evaluate in future consultations."
            }
        else:
            return {
                "stage": "Positive Screening",
                "description": "Indication of possible domestic abuse",
                "interpretation": "Positive result for domestic violence. Requires more detailed assessment, offering support, and referral to specialized resources. Document appropriately and follow institutional protocols."
            }


def calculate_aas(emotional_physical_abuse: str, physical_hurt_recently: str,
                 physical_hurt_pregnancy: str, sexual_abuse: str, 
                 afraid_of_partner: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AasCalculator()
    return calculator.calculate(
        emotional_physical_abuse, physical_hurt_recently, 
        physical_hurt_pregnancy, sexual_abuse, afraid_of_partner
    )
