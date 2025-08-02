"""
Woman Abuse Screening Tool (WAST) Calculator

Validated screening instrument for detecting intimate partner violence in healthcare settings.

References:
1. Brown JB, Lent B, Brett PJ, Sas G, Pederson LL. Development of the Woman Abuse 
   Screening Tool for use in family practice. Fam Med. 1996;28(6):422-428.
2. Brown JB, Lent B, Schmidt G, Sas G. Application of the Woman Abuse Screening Tool 
   (WAST) and WAST-short in the family practice setting. J Fam Pract. 2000;49(10):896-903.
3. MacMillan HL, Wathen CN, Jamieson E, et al. Screening for intimate partner violence 
   in health care settings: a randomized trial. JAMA. 2009;302(5):493-501. 
   doi: 10.1001/jama.2009.1089
4. Rabin RF, Jennings JM, Campbell JC, Bair-Merritt MH. Intimate partner violence 
   screening tools: a systematic review. Am J Prev Med. 2009;36(5):439-445.e4. 
   doi: 10.1016/j.amepre.2009.01.024
"""

from typing import Dict, Any


class WomanAbuseScreeningToolCalculator:
    """Calculator for Woman Abuse Screening Tool (WAST)"""
    
    def __init__(self):
        # WAST scoring parameters
        self.RELATIONSHIP_SCORES = {
            "lots_of_tension": 1,
            "some_tension": 2,
            "no_tension": 3
        }
        
        self.DIFFICULTY_SCORES = {
            "great_difficulty": 1,
            "some_difficulty": 2,
            "no_difficulty": 3
        }
        
        self.FREQUENCY_SCORES = {
            "often": 1,
            "sometimes": 2,
            "never": 3
        }
        
        self.YES_NO_SCORES = {
            "yes": 1,  # Yes indicates abuse (higher risk)
            "no": 2    # No indicates no abuse (lower risk)
        }
        
        # Question descriptions for clinical interpretation
        self.QUESTION_DESCRIPTIONS = {
            "tension_arguments_relationship": "Relationship tension level",
            "partner_jealousy_possessiveness": "Argument resolution difficulty",
            "arguments_resolution": "Arguments causing negative self-feelings",
            "arguments_feeling_bad": "Arguments resulting in physical violence",
            "physical_violence_frequency": "Feeling frightened by partner",
            "feel_frightened": "History of physical abuse",
            "physical_abuse_history": "History of emotional abuse",
            "emotional_abuse_history": "History of sexual abuse"
        }
        
        # Risk thresholds
        self.HIGH_RISK_THRESHOLD = 12  # Score ≤12 = high risk
        self.MODERATE_RISK_THRESHOLD = 17  # Score 13-17 = moderate risk
        self.MAX_SCORE = 24  # Maximum possible score (lowest risk)
        self.MIN_SCORE = 8   # Minimum possible score (highest risk)
    
    def calculate(self, tension_arguments_relationship: str, partner_jealousy_possessiveness: str,
                 arguments_resolution: str, arguments_feeling_bad: str, physical_violence_frequency: str,
                 feel_frightened: str, physical_abuse_history: str, emotional_abuse_history: str) -> Dict[str, Any]:
        """
        Calculates the WAST score for intimate partner violence screening
        
        Args:
            tension_arguments_relationship (str): Relationship tension level
            partner_jealousy_possessiveness (str): Argument resolution difficulty
            arguments_resolution (str): Arguments causing negative feelings
            arguments_feeling_bad (str): Arguments resulting in physical violence
            physical_violence_frequency (str): Feeling frightened by partner
            feel_frightened (str): History of physical abuse
            physical_abuse_history (str): History of emotional abuse
            emotional_abuse_history (str): History of sexual abuse
            
        Returns:
            Dict with the WAST score and risk assessment
        """
        
        # Organize parameters
        parameters = {
            "tension_arguments_relationship": tension_arguments_relationship,
            "partner_jealousy_possessiveness": partner_jealousy_possessiveness,
            "arguments_resolution": arguments_resolution,
            "arguments_feeling_bad": arguments_feeling_bad,
            "physical_violence_frequency": physical_violence_frequency,
            "feel_frightened": feel_frightened,
            "physical_abuse_history": physical_abuse_history,
            "emotional_abuse_history": emotional_abuse_history
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total WAST score
        total_score = self._calculate_total_score(parameters)
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Generate detailed assessment
        detailed_assessment = self._generate_detailed_assessment(total_score, parameters)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["stage_description"],
            "risk_level": risk_assessment["risk_level"],
            "safety_recommendations": detailed_assessment["safety_recommendations"],
            "detailed_assessment": detailed_assessment
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        # Define valid values for each parameter type
        valid_relationship_values = ["lots_of_tension", "some_tension", "no_tension"]
        valid_difficulty_values = ["great_difficulty", "some_difficulty", "no_difficulty"]
        valid_frequency_values = ["often", "sometimes", "never"]
        valid_yes_no_values = ["yes", "no"]
        
        # Validate each parameter
        if parameters["tension_arguments_relationship"] not in valid_relationship_values:
            raise ValueError("tension_arguments_relationship must be one of: lots_of_tension, some_tension, no_tension")
        
        if parameters["partner_jealousy_possessiveness"] not in valid_difficulty_values:
            raise ValueError("partner_jealousy_possessiveness must be one of: great_difficulty, some_difficulty, no_difficulty")
        
        if parameters["arguments_resolution"] not in valid_frequency_values:
            raise ValueError("arguments_resolution must be one of: often, sometimes, never")
        
        if parameters["arguments_feeling_bad"] not in valid_frequency_values:
            raise ValueError("arguments_feeling_bad must be one of: often, sometimes, never")
        
        if parameters["physical_violence_frequency"] not in valid_frequency_values:
            raise ValueError("physical_violence_frequency must be one of: often, sometimes, never")
        
        if parameters["feel_frightened"] not in valid_yes_no_values:
            raise ValueError("feel_frightened must be one of: yes, no")
        
        if parameters["physical_abuse_history"] not in valid_yes_no_values:
            raise ValueError("physical_abuse_history must be one of: yes, no")
        
        if parameters["emotional_abuse_history"] not in valid_yes_no_values:
            raise ValueError("emotional_abuse_history must be one of: yes, no")
    
    def _calculate_total_score(self, parameters: Dict[str, str]) -> int:
        """
        Calculates the total WAST score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            
        Returns:
            int: Total WAST score
        """
        
        total_score = 0
        
        # Questions 1-5: scored 1-3 (1=highest risk)
        total_score += self.RELATIONSHIP_SCORES[parameters["tension_arguments_relationship"]]
        total_score += self.DIFFICULTY_SCORES[parameters["partner_jealousy_possessiveness"]]
        total_score += self.FREQUENCY_SCORES[parameters["arguments_resolution"]]
        total_score += self.FREQUENCY_SCORES[parameters["arguments_feeling_bad"]]
        total_score += self.FREQUENCY_SCORES[parameters["physical_violence_frequency"]]
        
        # Questions 6-8: scored 1-2 (1=yes=highest risk)
        total_score += self.YES_NO_SCORES[parameters["feel_frightened"]]
        total_score += self.YES_NO_SCORES[parameters["physical_abuse_history"]]
        total_score += self.YES_NO_SCORES[parameters["emotional_abuse_history"]]
        
        return total_score
    
    def _get_risk_assessment(self, score: int) -> Dict[str, str]:
        """
        Determines the risk level based on WAST score
        
        Args:
            score (int): Calculated WAST score
            
        Returns:
            Dict with risk assessment details
        """
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "High Risk",
                "stage_description": "High probability of intimate partner violence",
                "risk_level": "high",
                "interpretation": f"WAST score of {score} indicates high likelihood of domestic violence. "
                               f"Immediate safety assessment and intervention planning required. Provide resources, "
                               f"safety planning, and appropriate referrals to domestic violence services. Consider "
                               f"immediate safety concerns and follow institutional protocols for high-risk situations. "
                               f"Ensure patient privacy and confidentiality throughout the intervention process."
            }
        elif score <= self.MODERATE_RISK_THRESHOLD:
            return {
                "stage": "Moderate Risk",
                "stage_description": "Moderate probability of intimate partner violence",
                "risk_level": "moderate",
                "interpretation": f"WAST score of {score} suggests possible intimate partner violence. "
                               f"Further assessment recommended to clarify risk level and provide appropriate support. "
                               f"Provide information about domestic violence resources and support services. Consider "
                               f"follow-up screening and offer referrals to domestic violence counselors or social services. "
                               f"Document findings appropriately and ensure patient safety."
            }
        else:
            return {
                "stage": "Low Risk",
                "stage_description": "Low probability of intimate partner violence",
                "risk_level": "low",
                "interpretation": f"WAST score of {score} indicates low likelihood of domestic violence based on current "
                               f"responses. Continue routine care and provide general information about healthy relationships "
                               f"if appropriate. Consider periodic re-screening as relationship dynamics may change over time. "
                               f"Remain alert to other signs or symptoms that may indicate domestic violence."
            }
    
    def _generate_detailed_assessment(self, total_score: int, parameters: Dict[str, str]) -> Dict[str, Any]:
        """
        Generates detailed clinical assessment and recommendations
        
        Args:
            total_score (int): Total WAST score
            parameters (Dict): All input parameters
            
        Returns:
            Dict with detailed assessment
        """
        
        assessment = {
            "score_breakdown": self._analyze_score_breakdown(total_score, parameters),
            "risk_factors": self._identify_risk_factors(parameters),
            "safety_recommendations": self._get_safety_recommendations(total_score, parameters),
            "intervention_guidelines": self._get_intervention_guidelines(total_score),
            "documentation_guidance": self._get_documentation_guidance(total_score),
            "resource_recommendations": self._get_resource_recommendations(total_score),
            "follow_up_recommendations": self._get_follow_up_recommendations(total_score)
        }
        
        return assessment
    
    def _analyze_score_breakdown(self, total_score: int, parameters: Dict[str, str]) -> Dict[str, Any]:
        """Analyzes individual question contributions to overall score"""
        
        breakdown = {}
        high_risk_indicators = []
        
        # Analyze each question
        for param, value in parameters.items():
            if param in ["tension_arguments_relationship"]:
                score = self.RELATIONSHIP_SCORES[value]
            elif param in ["partner_jealousy_possessiveness"]:
                score = self.DIFFICULTY_SCORES[value]
            elif param in ["arguments_resolution", "arguments_feeling_bad", "physical_violence_frequency"]:
                score = self.FREQUENCY_SCORES[value]
            else:  # yes/no questions
                score = self.YES_NO_SCORES[value]
            
            breakdown[param] = {
                "response": value,
                "score": score,
                "description": self.QUESTION_DESCRIPTIONS[param]
            }
            
            # Identify high-risk responses
            if score == 1:  # Highest risk responses
                high_risk_indicators.append({
                    "question": param,
                    "response": value,
                    "description": self.QUESTION_DESCRIPTIONS[param]
                })
        
        return {
            "individual_scores": breakdown,
            "high_risk_indicators": high_risk_indicators,
            "total_possible_score": self.MAX_SCORE,
            "risk_percentage": round(((self.MAX_SCORE - total_score) / (self.MAX_SCORE - self.MIN_SCORE)) * 100, 1)
        }
    
    def _identify_risk_factors(self, parameters: Dict[str, str]) -> list:
        """Identifies specific risk factors based on responses"""
        
        risk_factors = []
        
        if parameters["tension_arguments_relationship"] == "lots_of_tension":
            risk_factors.append("High relationship tension reported")
        
        if parameters["partner_jealousy_possessiveness"] == "great_difficulty":
            risk_factors.append("Significant difficulty resolving arguments")
        
        if parameters["arguments_resolution"] == "often":
            risk_factors.append("Arguments frequently result in negative self-feelings")
        
        if parameters["arguments_feeling_bad"] == "often":
            risk_factors.append("Arguments frequently escalate to physical violence")
        
        if parameters["physical_violence_frequency"] == "often":
            risk_factors.append("Patient frequently feels frightened by partner")
        
        if parameters["feel_frightened"] == "yes":
            risk_factors.append("History of physical abuse reported")
        
        if parameters["physical_abuse_history"] == "yes":
            risk_factors.append("History of emotional abuse reported")
        
        if parameters["emotional_abuse_history"] == "yes":
            risk_factors.append("History of sexual abuse reported")
        
        return risk_factors
    
    def _get_safety_recommendations(self, score: int, parameters: Dict[str, str]) -> list:
        """Generates safety recommendations based on risk level"""
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return [
                "Immediate safety assessment required",
                "Develop safety plan with patient",
                "Provide emergency contact information (National DV Hotline: 1-800-799-7233)",
                "Consider immediate referral to domestic violence services",
                "Assess for immediate danger and need for emergency shelter",
                "Document injuries if present using body maps",
                "Follow mandatory reporting requirements if applicable",
                "Ensure patient privacy during assessment and discharge"
            ]
        elif score <= self.MODERATE_RISK_THRESHOLD:
            return [
                "Provide domestic violence resource information",
                "Offer referral to domestic violence counselor",
                "Discuss safety planning basics",
                "Provide National DV Hotline number (1-800-799-7233)",
                "Schedule follow-up appointment for re-assessment",
                "Document findings appropriately",
                "Offer social services consultation"
            ]
        else:
            return [
                "Continue routine screening at future visits",
                "Provide general relationship health information if appropriate",
                "Remain alert for other indicators of domestic violence",
                "Document negative screening results"
            ]
    
    def _get_intervention_guidelines(self, score: int) -> list:
        """Generates intervention guidelines based on risk level"""
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return [
                "Use trauma-informed care approach",
                "Validate patient's experiences and feelings",
                "Emphasize that abuse is not the patient's fault",
                "Respect patient autonomy in decision-making",
                "Provide non-judgmental support",
                "Coordinate with domestic violence advocates",
                "Consider multi-disciplinary team involvement",
                "Follow institutional domestic violence protocols"
            ]
        elif score <= self.MODERATE_RISK_THRESHOLD:
            return [
                "Provide supportive, non-judgmental environment",
                "Offer information about healthy relationships",
                "Discuss available resources and support services",
                "Respect patient's readiness to disclose or seek help",
                "Offer follow-up screening and support"
            ]
        else:
            return [
                "Continue supportive care",
                "Maintain awareness of domestic violence indicators",
                "Provide general health and wellness information"
            ]
    
    def _get_documentation_guidance(self, score: int) -> list:
        """Provides documentation guidance based on risk level"""
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return [
                "Document exact quotes when possible",
                "Use body maps to document any injuries",
                "Record WAST score and interpretation",
                "Document safety plan discussion",
                "Record referrals made and resources provided",
                "Note any immediate safety concerns",
                "Follow institutional documentation policies"
            ]
        else:
            return [
                "Document WAST score and risk level",
                "Record any resources or information provided",
                "Note plan for follow-up screening",
                "Maintain confidential documentation"
            ]
    
    def _get_resource_recommendations(self, score: int) -> list:
        """Generates resource recommendations based on risk level"""
        
        base_resources = [
            "National Domestic Violence Hotline: 1-800-799-7233 (24/7)",
            "Local domestic violence shelter and advocacy services",
            "Legal advocacy and protection order assistance",
            "Counseling and support groups for domestic violence survivors"
        ]
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return base_resources + [
                "Emergency shelter and housing assistance",
                "Safety planning resources and apps (e.g., myPlan app)",
                "Financial assistance and emergency funds",
                "Child protective services if children are involved",
                "Law enforcement liaison if immediate danger"
            ]
        elif score <= self.MODERATE_RISK_THRESHOLD:
            return base_resources + [
                "Support groups and counseling services",
                "Educational materials about domestic violence",
                "Community mental health resources"
            ]
        else:
            return [
                "General relationship health resources",
                "Mental health and wellness resources"
            ]
    
    def _get_follow_up_recommendations(self, score: int) -> list:
        """Generates follow-up recommendations based on risk level"""
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return [
                "Follow up within 1-2 weeks or sooner if needed",
                "Coordinate follow-up with domestic violence advocate",
                "Monitor for escalating violence or safety concerns",
                "Re-assess safety plan effectiveness",
                "Consider more frequent monitoring"
            ]
        elif score <= self.MODERATE_RISK_THRESHOLD:
            return [
                "Follow up within 4-6 weeks",
                "Re-screen with WAST at follow-up visits",
                "Monitor for changes in relationship dynamics",
                "Assess utilization of resources provided"
            ]
        else:
            return [
                "Continue routine screening at regular intervals",
                "Re-screen annually or as clinically indicated",
                "Remain alert for changes in presentation"
            ]


def calculate_woman_abuse_screening_tool(tension_arguments_relationship, partner_jealousy_possessiveness,
                                       arguments_resolution, arguments_feeling_bad, physical_violence_frequency,
                                       feel_frightened, physical_abuse_history, emotional_abuse_history) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_woman_abuse_screening_tool pattern
    """
    calculator = WomanAbuseScreeningToolCalculator()
    return calculator.calculate(
        tension_arguments_relationship, partner_jealousy_possessiveness, arguments_resolution,
        arguments_feeling_bad, physical_violence_frequency, feel_frightened,
        physical_abuse_history, emotional_abuse_history
    )