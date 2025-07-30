"""
Danger Assessment Tool for Domestic Abuse Calculator

Predicts risk of death by intimate partner (IP) in violent intimate relationship.
Validated lethality risk assessment instrument for intimate partner femicide.

References:
- Campbell JC, et al. Am J Public Health. 2003;93(7):1089-1097.
- Campbell JC, et al. J Interpers Violence. 2009;24(4):653-674.
- Messing JT, et al. Soc Serv Rev. 2015;89(3):499-530.
"""

from typing import Dict, Any


class DangerAssessmentToolCalculator:
    """Calculator for Danger Assessment Tool for Domestic Abuse"""
    
    def __init__(self):
        # Risk factor weights based on adjusted odds ratios from validation study
        self.RISK_WEIGHTS = {
            "physical_violence_increased": 1.2,  # OR 2.3
            "owns_gun": 2.1,  # OR 5.1 - highest risk factor
            "threatened_weapon": 1.8,  # OR 4.3
            "threatened_kill_you": 1.7,  # OR 4.0
            "avoided_killing": 1.5,  # OR 3.5
            "beaten_pregnant": 1.4,  # OR 3.2
            "jealous_controlling": 1.3,  # OR 3.0
            "controls_activities": 1.1,  # OR 2.1
            "controls_daily_activities": 1.2,  # OR 2.4
            "violent_others": 1.3,  # OR 2.8
            "violent_toward_others": 1.0,  # OR 1.9
            "threatened_suicide": 1.1,  # OR 2.0
            "threatened_kill_children": 1.6,  # OR 3.8
            "child_not_his": 1.0,  # OR 1.8
            "employment_problems": 0.8,  # OR 1.5
            "follows_spies": 1.1,  # OR 2.0
            "forced_sex": 1.0,  # OR 1.9
            "tried_to_strangle": 1.9,  # OR 4.6
            "drugs_alcohol_problems": 0.9,  # OR 1.7
            "stepchild_present": 0.8   # OR 1.6
        }
        
        # Risk level thresholds
        self.RISK_THRESHOLDS = {
            "variable": {"min": 0, "max": 7},
            "increased": {"min": 8, "max": 13},
            "extreme": {"min": 14, "max": 20}
        }
        
        # Safety planning recommendations by risk level
        self.SAFETY_RECOMMENDATIONS = {
            "variable": [
                "Develop basic safety plan with trusted friend or family member",
                "Keep emergency contact numbers readily available",
                "Identify safe places to go if needed",
                "Consider documenting incidents with photos and dates",
                "Monitor situation for changes in risk factors",
                "Connect with local domestic violence resources"
            ],
            "increased": [
                "Implement comprehensive safety plan immediately",
                "Prepare emergency bag with essentials (documents, medications, clothes)",
                "Establish code words with trusted contacts for emergency help",
                "Consider temporary relocation or shelter placement",
                "Engage with domestic violence advocate or counselor",
                "Explore legal protection options (restraining order)",
                "Inform trusted friends, family, or coworkers about situation",
                "Plan safe routes and transportation methods"
            ],
            "extreme": [
                "Activate emergency safety plan immediately",
                "Consider immediate shelter placement or safe relocation",
                "Contact law enforcement for immediate protection",
                "Obtain emergency protection order if possible",
                "Notify workplace security about potential danger",
                "Change daily routines and avoid predictable patterns",
                "Consider temporary custody arrangements for children",
                "Coordinate with high-risk domestic violence team",
                "Implement technology safety measures (new phone, secure communications)",
                "Consider temporary housing assistance programs"
            ]
        }
    
    def calculate(self, physical_violence_increased: str, owns_gun: str, threatened_weapon: str,
                  threatened_kill_you: str, avoided_killing: str, beaten_pregnant: str,
                  jealous_controlling: str, controls_activities: str, controls_daily_activities: str,
                  violent_others: str, violent_toward_others: str, threatened_suicide: str,
                  threatened_kill_children: str, child_not_his: str, employment_problems: str,
                  follows_spies: str, forced_sex: str, tried_to_strangle: str,
                  drugs_alcohol_problems: str, stepchild_present: str) -> Dict[str, Any]:
        """
        Calculates danger assessment score based on risk factors
        
        Args:
            All 20 risk factor parameters as strings ("yes", "no", or "not_applicable")
            
        Returns:
            Dict with danger assessment score, risk level, and safety recommendations
        """
        
        # Collect all parameters
        parameters = {
            "physical_violence_increased": physical_violence_increased,
            "owns_gun": owns_gun,
            "threatened_weapon": threatened_weapon,
            "threatened_kill_you": threatened_kill_you,
            "avoided_killing": avoided_killing,
            "beaten_pregnant": beaten_pregnant,
            "jealous_controlling": jealous_controlling,
            "controls_activities": controls_activities,
            "controls_daily_activities": controls_daily_activities,
            "violent_others": violent_others,
            "violent_toward_others": violent_toward_others,
            "threatened_suicide": threatened_suicide,
            "threatened_kill_children": threatened_kill_children,
            "child_not_his": child_not_his,
            "employment_problems": employment_problems,
            "follows_spies": follows_spies,
            "forced_sex": forced_sex,
            "tried_to_strangle": tried_to_strangle,
            "drugs_alcohol_problems": drugs_alcohol_problems,
            "stepchild_present": stepchild_present
        }
        
        # Validations
        self._validate_inputs(parameters)
        
        # Calculate weighted score
        weighted_score = self._calculate_weighted_score(parameters)
        
        # Determine risk level
        risk_level = self._determine_risk_level(weighted_score)
        
        # Get risk analysis
        risk_analysis = self._get_risk_analysis(parameters, weighted_score, risk_level)
        
        # Get safety recommendations
        safety_recommendations = self._get_safety_recommendations(risk_level, parameters)
        
        # Generate interpretation
        interpretation = self._get_interpretation(risk_level, weighted_score, parameters)
        
        # Get immediate actions
        immediate_actions = self._get_immediate_actions(risk_level)
        
        return {
            "result": weighted_score,
            "unit": "danger score",
            "interpretation": interpretation,
            "stage": self._get_risk_stage(risk_level),
            "stage_description": self._get_risk_description(risk_level),
            "risk_level": risk_level,
            "weighted_score": weighted_score,
            "simple_score": self._calculate_simple_score(parameters),
            "risk_analysis": risk_analysis,
            "safety_recommendations": safety_recommendations,
            "immediate_actions": immediate_actions,
            "high_risk_factors": self._identify_high_risk_factors(parameters),
            "protective_factors": self._identify_protective_factors(parameters),
            "counseling_points": self._get_counseling_points(risk_level),
            "professional_referrals": self._get_professional_referrals(risk_level)
        }
    
    def _validate_inputs(self, parameters):
        """Validates input parameters"""
        
        valid_values = ["yes", "no", "not_applicable"]
        
        for param_name, value in parameters.items():
            if value not in valid_values:
                raise ValueError(f"{param_name} must be one of: {valid_values}")
    
    def _calculate_weighted_score(self, parameters):
        """Calculates weighted danger assessment score"""
        
        total_score = 0.0
        
        for param_name, value in parameters.items():
            if value == "yes" and param_name in self.RISK_WEIGHTS:
                total_score += self.RISK_WEIGHTS[param_name]
        
        return round(total_score, 1)
    
    def _calculate_simple_score(self, parameters):
        """Calculates simple count of 'yes' responses"""
        
        return sum(1 for value in parameters.values() if value == "yes")
    
    def _determine_risk_level(self, weighted_score):
        """Determines risk level based on weighted score"""
        
        if weighted_score <= self.RISK_THRESHOLDS["variable"]["max"]:
            return "variable"
        elif weighted_score <= self.RISK_THRESHOLDS["increased"]["max"]:
            return "increased"
        else:
            return "extreme"
    
    def _get_risk_stage(self, risk_level):
        """Get risk stage label"""
        
        stage_labels = {
            "variable": "Variable Danger",
            "increased": "Increased Danger", 
            "extreme": "Extreme Danger"
        }
        
        return stage_labels[risk_level]
    
    def _get_risk_description(self, risk_level):
        """Get risk level description"""
        
        descriptions = {
            "variable": "Low to moderate risk",
            "increased": "Moderate to high risk",
            "extreme": "High to extreme risk"
        }
        
        return descriptions[risk_level]
    
    def _get_risk_analysis(self, parameters, weighted_score, risk_level):
        """Generate detailed risk analysis"""
        
        analysis = {
            "weighted_score": weighted_score,
            "simple_count": self._calculate_simple_score(parameters),
            "risk_level": risk_level,
            "key_risk_factors": [],
            "severity_indicators": []
        }
        
        # Identify key risk factors present
        high_weight_factors = []
        for param_name, value in parameters.items():
            if value == "yes" and param_name in self.RISK_WEIGHTS:
                weight = self.RISK_WEIGHTS[param_name]
                if weight >= 1.5:  # High-weight factors
                    high_weight_factors.append({
                        "factor": param_name.replace("_", " ").title(),
                        "weight": weight
                    })
        
        analysis["key_risk_factors"] = sorted(high_weight_factors, 
                                            key=lambda x: x["weight"], reverse=True)
        
        # Severity indicators
        if parameters.get("owns_gun") == "yes":
            analysis["severity_indicators"].append("Gun ownership present - highest lethality risk factor")
        
        if parameters.get("tried_to_strangle") == "yes":
            analysis["severity_indicators"].append("History of strangulation - strong predictor of homicide")
        
        if parameters.get("threatened_weapon") == "yes":
            analysis["severity_indicators"].append("Weapon threats - indicates escalation potential")
        
        if parameters.get("threatened_kill_you") == "yes":
            analysis["severity_indicators"].append("Death threats - direct indication of lethal intent")
        
        return analysis
    
    def _get_safety_recommendations(self, risk_level, parameters):
        """Get safety recommendations based on risk level and specific factors"""
        
        base_recommendations = self.SAFETY_RECOMMENDATIONS[risk_level].copy()
        specific_recommendations = []
        
        # Add specific recommendations based on risk factors
        if parameters.get("owns_gun") == "yes":
            specific_recommendations.append("Gun in home - consider immediate relocation for safety")
        
        if parameters.get("tried_to_strangle") == "yes":
            specific_recommendations.append("History of strangulation - seek immediate medical evaluation and safety planning")
        
        if parameters.get("threatened_kill_children") == "yes":
            specific_recommendations.append("Threats against children - consider child protective services notification")
        
        if parameters.get("follows_spies") == "yes":
            specific_recommendations.append("Stalking behavior - document incidents and consider technology safety measures")
        
        return {
            "general_recommendations": base_recommendations,
            "specific_recommendations": specific_recommendations,
            "emergency_contacts": self._get_emergency_contacts(),
            "safety_planning_steps": self._get_safety_planning_steps(risk_level)
        }
    
    def _get_emergency_contacts(self):
        """Get emergency contact information"""
        
        return {
            "national_hotline": "1-800-799-7233 (National Domestic Violence Hotline)",
            "emergency_services": "911 for immediate danger",
            "text_line": "Text START to 88788 (Crisis Text Line)",
            "online_chat": "Available at thehotline.org",
            "local_resources": "Contact local domestic violence shelter or advocacy organization"
        }
    
    def _get_safety_planning_steps(self, risk_level):
        """Get step-by-step safety planning guidance"""
        
        basic_steps = [
            "Identify safe friends, family, or shelters where you can go",
            "Keep emergency bag ready with essentials",
            "Plan escape routes from home and work",
            "Establish code words with trusted contacts",
            "Keep important documents in safe location",
            "Have emergency money and transportation arranged"
        ]
        
        if risk_level in ["increased", "extreme"]:
            enhanced_steps = [
                "Change daily routines to be less predictable",
                "Inform school/childcare about safety concerns",
                "Consider changing phone number or getting new phone",
                "Review and update security at home and work",
                "Plan for pet safety if applicable",
                "Consider legal protection options"
            ]
            return basic_steps + enhanced_steps
        
        return basic_steps
    
    def _identify_high_risk_factors(self, parameters):
        """Identify highest risk factors present"""
        
        high_risk_factors = []
        
        critical_factors = {
            "owns_gun": "Gun ownership",
            "tried_to_strangle": "History of strangulation",
            "threatened_weapon": "Weapon threats",
            "threatened_kill_you": "Death threats",
            "threatened_kill_children": "Threats against children"
        }
        
        for param, description in critical_factors.items():
            if parameters.get(param) == "yes":
                high_risk_factors.append(description)
        
        return high_risk_factors
    
    def _identify_protective_factors(self, parameters):
        """Identify potential protective factors"""
        
        protective_factors = []
        
        # These are implied protective factors (absence of certain risks)
        if parameters.get("owns_gun") == "no":
            protective_factors.append("No gun in home")
        
        if parameters.get("drugs_alcohol_problems") == "no":
            protective_factors.append("No substance abuse issues")
        
        if parameters.get("violent_toward_others") == "no":
            protective_factors.append("No history of violence toward others")
        
        return protective_factors
    
    def _get_immediate_actions(self, risk_level):
        """Get immediate actions needed based on risk level"""
        
        if risk_level == "variable":
            return [
                "Create basic safety plan",
                "Connect with domestic violence resources",
                "Document any future incidents",
                "Monitor for changes in behavior or risk factors"
            ]
        elif risk_level == "increased":
            return [
                "Develop comprehensive safety plan immediately",
                "Contact domestic violence advocate",
                "Prepare emergency bag",
                "Consider legal protection options",
                "Inform trusted contacts about situation"
            ]
        else:  # extreme
            return [
                "Consider immediate safety measures (shelter, relocation)",
                "Contact law enforcement if in immediate danger",
                "Activate emergency safety plan",
                "Obtain emergency protection order if possible",
                "Coordinate with high-risk domestic violence team"
            ]
    
    def _get_counseling_points(self, risk_level):
        """Get key counseling points for victim"""
        
        general_points = [
            "You are not alone - help and support are available",
            "The abuse is not your fault",
            "Your safety and the safety of your children is the priority",
            "You have the right to live free from violence and fear",
            "There are people trained to help you navigate this situation safely"
        ]
        
        if risk_level == "extreme":
            critical_points = [
                "Your life may be in immediate danger",
                "Professional intervention is strongly recommended",
                "Emergency safety planning is critical",
                "Consider temporary relocation for immediate safety"
            ]
            return general_points + critical_points
        
        return general_points
    
    def _get_professional_referrals(self, risk_level):
        """Get professional referral recommendations"""
        
        base_referrals = [
            "Domestic violence advocate or counselor",
            "Legal advocacy services",
            "Mental health counseling services",
            "Healthcare provider for medical evaluation"
        ]
        
        if risk_level in ["increased", "extreme"]:
            enhanced_referrals = [
                "Law enforcement victim advocate",
                "Court-based victim services",
                "Emergency shelter services",
                "Legal aid for protection orders",
                "Trauma-informed therapy services",
                "Economic empowerment programs"
            ]
            return base_referrals + enhanced_referrals
        
        return base_referrals
    
    def _get_interpretation(self, risk_level, weighted_score, parameters):
        """Get comprehensive interpretation of assessment"""
        
        if risk_level == "variable":
            return (f"Danger Assessment score of {weighted_score} indicates variable danger level. "
                   f"While the immediate risk may not be extreme, safety planning is still important. "
                   f"Monitor situation for changes and connect with domestic violence resources for support.")
        
        elif risk_level == "increased":
            return (f"Danger Assessment score of {weighted_score} indicates increased danger level. "
                   f"There is elevated risk of intimate partner homicide. Enhanced safety planning is essential. "
                   f"Professional intervention is strongly recommended, including coordinated community response.")
        
        else:  # extreme
            return (f"Danger Assessment score of {weighted_score} indicates extreme danger level. "
                   f"There is severe and immediate risk of intimate partner homicide. Emergency safety planning "
                   f"is critical. Immediate professional intervention, law enforcement notification, and "
                   f"coordinated high-risk response may be necessary.")


def calculate_danger_assessment_tool(physical_violence_increased: str, owns_gun: str, threatened_weapon: str,
                                   threatened_kill_you: str, avoided_killing: str, beaten_pregnant: str,
                                   jealous_controlling: str, controls_activities: str, controls_daily_activities: str,
                                   violent_others: str, violent_toward_others: str, threatened_suicide: str,
                                   threatened_kill_children: str, child_not_his: str, employment_problems: str,
                                   follows_spies: str, forced_sex: str, tried_to_strangle: str,
                                   drugs_alcohol_problems: str, stepchild_present: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DangerAssessmentToolCalculator()
    return calculator.calculate(
        physical_violence_increased, owns_gun, threatened_weapon, threatened_kill_you,
        avoided_killing, beaten_pregnant, jealous_controlling, controls_activities,
        controls_daily_activities, violent_others, violent_toward_others, threatened_suicide,
        threatened_kill_children, child_not_his, employment_problems, follows_spies,
        forced_sex, tried_to_strangle, drugs_alcohol_problems, stepchild_present
    )