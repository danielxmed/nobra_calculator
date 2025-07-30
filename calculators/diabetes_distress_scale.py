"""
Diabetes Distress Scale (DDS17) Calculator

Measures diabetes-related emotional distress across four domains to identify 
sources of distress and guide targeted interventions for patients with diabetes.

References:
- Polonsky WH, Fisher L, Earles J, et al. Diabetes Care. 2005;28(3):626-631.
- Fisher L, Hessler DM, Polonsky WH, Mullan J. Diabetes Care. 2012;35(2):259-264.
- Fisher L, Glasgow RE, Mullan JT, et al. Ann Fam Med. 2008;6(3):246-252.
"""

from typing import Dict, Any, List
import statistics


class DiabetesDistressScaleCalculator:
    """Calculator for Diabetes Distress Scale (DDS17)"""
    
    def __init__(self):
        # DDS17 subscale item mappings (1-indexed from original questionnaire)
        self.SUBSCALES = {
            "emotional_burden": {
                "items": [1, 2, 3, 6, 12],  # Items: overwhelming_demands, feeling_discouraged, failure_regimen, angry_frustrated, constant_thoughts
                "name": "Emotional Burden",
                "description": "Emotional distress related to living with diabetes"
            },
            "physician_distress": {
                "items": [7, 8, 9, 10],  # Items: unsatisfied_care, physician_communication, physician_doesnt_give_direction, physician_doesnt_take_seriously
                "name": "Physician Distress", 
                "description": "Distress related to healthcare provider relationship"
            },
            "regimen_distress": {
                "items": [4, 11, 13, 14],  # Items: clear_concrete_goals, regimen_overwhelming, blood_sugar_checking, regimen_burden
                "name": "Regimen Distress",
                "description": "Distress related to diabetes management regimen"
            },
            "interpersonal_distress": {
                "items": [5, 15, 16, 17],  # Items: not_motivated, friends_family_nagging, friends_family_interference, friends_family_dont_understand
                "name": "Interpersonal Distress",
                "description": "Distress related to family and social support"
            }
        }
        
        # Parameter name to index mapping
        self.PARAMETER_MAPPING = [
            "overwhelming_demands",      # 1
            "feeling_discouraged",       # 2
            "failure_regimen",          # 3
            "clear_concrete_goals",     # 4
            "not_motivated",            # 5
            "angry_frustrated",         # 6
            "unsatisfied_care",         # 7
            "physician_communication",  # 8
            "physician_doesnt_give_direction",  # 9
            "physician_doesnt_take_seriously",  # 10
            "regimen_overwhelming",     # 11
            "constant_thoughts",        # 12
            "blood_sugar_checking",     # 13
            "regimen_burden",           # 14
            "friends_family_nagging",   # 15
            "friends_family_interference",  # 16
            "friends_family_dont_understand"   # 17
        ]
        
        # Distress interpretation thresholds
        self.DISTRESS_LEVELS = {
            "little_no_distress": {
                "range": (1.0, 1.9),
                "label": "Little or No Distress",
                "description": "Minimal diabetes-related distress",
                "recommendation": "Continue current support and monitor periodically"
            },
            "moderate_distress": {
                "range": (2.0, 2.9), 
                "label": "Moderate Distress",
                "description": "Moderate diabetes-related distress",
                "recommendation": "Consider targeted support and intervention"
            },
            "high_distress": {
                "range": (3.0, 6.0),
                "label": "High Distress", 
                "description": "High diabetes-related distress requiring intervention",
                "recommendation": "Clinical attention and intervention warranted"
            }
        }
        
        # Clinical recommendations by distress level
        self.CLINICAL_RECOMMENDATIONS = {
            "little_no_distress": [
                "Continue current diabetes management approach",
                "Maintain regular follow-up appointments",
                "Monitor for changes in distress levels over time",
                "Provide general diabetes education and support",
                "Encourage continued self-care behaviors"
            ],
            "moderate_distress": [
                "Discuss specific sources of diabetes distress with patient",
                "Develop targeted coping strategies for identified stressors",
                "Consider diabetes education or support group referral",
                "Monitor distress levels more frequently (every 3-6 months)",
                "Address specific subscale areas with elevated scores"
            ],
            "high_distress": [
                "Immediate clinical attention and assessment required",
                "Refer to diabetes educator or certified diabetes care specialist",
                "Consider mental health referral or diabetes psychologist",
                "Develop comprehensive diabetes distress intervention plan",
                "Frequent monitoring and follow-up (monthly to quarterly)",
                "Address underlying causes in high-scoring subscales",
                "Consider medication review and regimen simplification"
            ]
        }
    
    def calculate(self, overwhelming_demands: int, feeling_discouraged: int, failure_regimen: int,
                  clear_concrete_goals: int, not_motivated: int, angry_frustrated: int, unsatisfied_care: int,
                  physician_communication: int, physician_doesnt_give_direction: int,
                  physician_doesnt_take_seriously: int, regimen_overwhelming: int, constant_thoughts: int,
                  blood_sugar_checking: int, regimen_burden: int, friends_family_nagging: int,
                  friends_family_interference: int, friends_family_dont_understand: int) -> Dict[str, Any]:
        """
        Calculates Diabetes Distress Scale (DDS17) scores
        
        Args:
            All 17 DDS items rated on 6-point scale (1=Not a problem to 6=Very serious problem)
            
        Returns:
            Dict with total score, subscale scores, and clinical recommendations
        """
        
        # Collect all responses
        responses = [
            overwhelming_demands, feeling_discouraged, failure_regimen, clear_concrete_goals,
            not_motivated, angry_frustrated, unsatisfied_care, physician_communication,
            physician_doesnt_give_direction, physician_doesnt_take_seriously, regimen_overwhelming,
            constant_thoughts, blood_sugar_checking, regimen_burden,
            friends_family_nagging, friends_family_interference, friends_family_dont_understand
        ]
        
        # Validate inputs
        self._validate_inputs(responses)
        
        # Calculate total DDS17 score (mean of all 17 items)
        total_score = sum(responses) / len(responses)
        
        # Calculate subscale scores
        subscale_scores = self._calculate_subscale_scores(responses)
        
        # Determine distress level
        distress_level = self._determine_distress_level(total_score)
        
        # Get clinical assessment
        clinical_assessment = self._get_clinical_assessment(
            total_score, subscale_scores, distress_level, responses)
        
        # Get recommendations
        recommendations = self._get_recommendations(distress_level, subscale_scores)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, distress_level, subscale_scores)
        
        # Get subscale analysis
        subscale_analysis = self._get_subscale_analysis(subscale_scores)
        
        return {
            "result": round(total_score, 2),
            "unit": "DDS17 Score (1-6 scale)",
            "interpretation": interpretation,
            "stage": self.DISTRESS_LEVELS[distress_level]["label"],
            "stage_description": self.DISTRESS_LEVELS[distress_level]["description"],
            "total_score": round(total_score, 2),
            "distress_level": distress_level,
            "subscale_scores": {k: round(v, 2) for k, v in subscale_scores.items()},
            "clinical_assessment": clinical_assessment,
            "recommendations": recommendations,
            "subscale_analysis": subscale_analysis,
            "intervention_priorities": self._get_intervention_priorities(subscale_scores),
            "follow_up_recommendations": self._get_follow_up_recommendations(distress_level, total_score),
            "referral_considerations": self._get_referral_considerations(distress_level, subscale_scores),
            "monitoring_guidance": self._get_monitoring_guidance(distress_level, total_score)
        }
    
    def _validate_inputs(self, responses: List[int]):
        """Validates input parameters"""
        
        if len(responses) != 17:
            raise ValueError("DDS17 requires exactly 17 item responses")
        
        for i, response in enumerate(responses):
            if not isinstance(response, int):
                raise ValueError(f"Item {i+1} must be an integer")
            
            if response < 1 or response > 6:
                raise ValueError(f"Item {i+1} must be between 1 and 6 (inclusive)")
    
    def _calculate_subscale_scores(self, responses: List[int]) -> Dict[str, float]:
        """Calculates subscale scores"""
        
        subscale_scores = {}
        
        for subscale_name, subscale_info in self.SUBSCALES.items():
            # Get items for this subscale (convert from 1-indexed to 0-indexed)
            subscale_items = [responses[item - 1] for item in subscale_info["items"]]
            
            # Calculate mean score for subscale
            subscale_scores[subscale_name] = sum(subscale_items) / len(subscale_items)
        
        return subscale_scores
    
    def _determine_distress_level(self, total_score: float) -> str:
        """Determines distress level based on total score"""
        
        for level, info in self.DISTRESS_LEVELS.items():
            min_score, max_score = info["range"]
            if min_score <= total_score <= max_score:
                return level
        
        # Handle edge cases
        if total_score < 1.0:
            return "little_no_distress"
        else:
            return "high_distress"
    
    def _get_clinical_assessment(self, total_score: float, subscale_scores: Dict[str, float],
                                distress_level: str, responses: List[int]) -> Dict[str, Any]:
        """Generate comprehensive clinical assessment"""
        
        assessment = {
            "total_score": round(total_score, 2),
            "distress_level": distress_level,
            "clinical_significance": total_score >= 3.0,
            "subscale_breakdown": {},
            "highest_distress_areas": [],
            "individual_item_analysis": {},
            "clinical_indicators": []
        }
        
        # Analyze subscales
        for subscale_name, score in subscale_scores.items():
            assessment["subscale_breakdown"][subscale_name] = {
                "score": round(score, 2),
                "level": self._categorize_subscale_score(score),
                "description": self.SUBSCALES[subscale_name]["description"]
            }
        
        # Identify highest distress areas
        sorted_subscales = sorted(subscale_scores.items(), key=lambda x: x[1], reverse=True)
        assessment["highest_distress_areas"] = [
            {
                "subscale": name,
                "score": round(score, 2),
                "description": self.SUBSCALES[name]["description"]
            }
            for name, score in sorted_subscales[:2]  # Top 2 areas
        ]
        
        # Individual item analysis (identify highest scoring items)
        item_scores = []
        for i, response in enumerate(responses):
            item_scores.append({
                "item_number": i + 1,
                "parameter": self.PARAMETER_MAPPING[i],
                "score": response,
                "severity": self._categorize_item_score(response)
            })
        
        # Get top 3 highest scoring items
        highest_items = sorted(item_scores, key=lambda x: x["score"], reverse=True)[:3]
        assessment["individual_item_analysis"] = {
            "highest_scoring_items": highest_items,
            "items_needing_attention": [item for item in item_scores if item["score"] >= 4]
        }
        
        # Clinical indicators
        assessment["clinical_indicators"] = self._get_clinical_indicators(
            total_score, subscale_scores, distress_level)
        
        return assessment
    
    def _categorize_subscale_score(self, score: float) -> str:
        """Categorize subscale score level"""
        if score < 2.0:
            return "Low"
        elif score < 3.0:
            return "Moderate" 
        else:
            return "High"
    
    def _categorize_item_score(self, score: int) -> str:
        """Categorize individual item score"""
        if score <= 2:
            return "Minimal"
        elif score <= 4:
            return "Moderate"
        else:
            return "High"
    
    def _get_clinical_indicators(self, total_score: float, subscale_scores: Dict[str, float],
                                distress_level: str) -> List[str]:
        """Get clinical indicators based on scores"""
        
        indicators = []
        
        if total_score >= 3.0:
            indicators.append("Clinically significant diabetes distress requiring intervention")
        
        if subscale_scores.get("emotional_burden", 0) >= 3.0:
            indicators.append("High emotional burden - consider mental health support")
        
        if subscale_scores.get("physician_distress", 0) >= 3.0:
            indicators.append("Provider relationship issues - review care coordination")
        
        if subscale_scores.get("regimen_distress", 0) >= 3.0:
            indicators.append("Treatment regimen burden - consider simplification")
        
        if subscale_scores.get("interpersonal_distress", 0) >= 3.0:
            indicators.append("Social support deficits - consider family education")
        
        # Multiple high subscales
        high_subscales = sum(1 for score in subscale_scores.values() if score >= 3.0)
        if high_subscales >= 3:
            indicators.append("Multiple areas of high distress - comprehensive intervention needed")
        
        return indicators
    
    def _get_recommendations(self, distress_level: str, subscale_scores: Dict[str, float]) -> Dict[str, List[str]]:
        """Get clinical recommendations"""
        
        recommendations = {
            "immediate_actions": self.CLINICAL_RECOMMENDATIONS[distress_level].copy(),
            "subscale_specific": [],
            "long_term_strategies": []
        }
        
        # Subscale-specific recommendations
        if subscale_scores.get("emotional_burden", 0) >= 3.0:
            recommendations["subscale_specific"].extend([
                "Address emotional burden through stress management techniques",
                "Consider cognitive-behavioral therapy for diabetes distress",
                "Evaluate for clinical depression or anxiety disorders"
            ])
        
        if subscale_scores.get("physician_distress", 0) >= 3.0:
            recommendations["subscale_specific"].extend([
                "Improve patient-provider communication and shared decision making",
                "Consider diabetes care team consultation or second opinion",
                "Address concerns about diabetes care quality and coordination"
            ])
        
        if subscale_scores.get("regimen_distress", 0) >= 3.0:
            recommendations["subscale_specific"].extend([
                "Simplify diabetes management regimen when possible",
                "Provide additional diabetes self-management education",
                "Consider continuous glucose monitoring to reduce testing burden"
            ])
        
        if subscale_scores.get("interpersonal_distress", 0) >= 3.0:
            recommendations["subscale_specific"].extend([
                "Provide family education about diabetes management support",
                "Address social support needs and family dynamics",
                "Consider peer support groups or diabetes support networks"
            ])
        
        # Long-term strategies
        if distress_level == "high_distress":
            recommendations["long_term_strategies"] = [
                "Develop comprehensive diabetes distress management plan",
                "Regular monitoring with validated distress screening tools",
                "Coordinate care between diabetes team and mental health providers",
                "Consider diabetes-specific psychosocial interventions",
                "Address social determinants of health affecting diabetes management"
            ]
        else:
            recommendations["long_term_strategies"] = [
                "Maintain supportive diabetes care environment",
                "Periodic reassessment of diabetes distress levels",
                "Continue diabetes education and skill building",
                "Promote diabetes self-efficacy and empowerment"
            ]
        
        return recommendations
    
    def _get_subscale_analysis(self, subscale_scores: Dict[str, float]) -> Dict[str, Any]:
        """Provide detailed subscale analysis"""
        
        analysis = {}
        
        for subscale_name, score in subscale_scores.items():
            subscale_info = self.SUBSCALES[subscale_name]
            
            analysis[subscale_name] = {
                "score": round(score, 2),
                "level": self._categorize_subscale_score(score),
                "description": subscale_info["description"],
                "clinical_significance": score >= 3.0,
                "intervention_focus": self._get_subscale_intervention_focus(subscale_name, score)
            }
        
        return analysis
    
    def _get_subscale_intervention_focus(self, subscale_name: str, score: float) -> List[str]:
        """Get intervention focus for specific subscale"""
        
        if score < 3.0:
            return ["Continue current support in this area"]
        
        interventions = {
            "emotional_burden": [
                "Stress management and coping skills training",
                "Diabetes-specific cognitive behavioral therapy",
                "Mindfulness-based stress reduction",
                "Evaluate for clinical depression/anxiety"
            ],
            "physician_distress": [
                "Improve patient-provider communication",
                "Shared decision making in diabetes care",
                "Care coordination optimization",
                "Consider provider team changes if needed"
            ],
            "regimen_distress": [
                "Diabetes self-management education",
                "Regimen simplification when possible",
                "Technology integration (CGM, insulin pumps)",
                "Problem-solving skills for diabetes tasks"
            ],
            "interpersonal_distress": [
                "Family diabetes education and support",
                "Communication skills training",
                "Peer support group participation",
                "Social support network development"
            ]
        }
        
        return interventions.get(subscale_name, ["Targeted intervention needed"])
    
    def _get_intervention_priorities(self, subscale_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Get prioritized intervention areas"""
        
        priorities = []
        
        # Sort subscales by score (highest first)
        sorted_subscales = sorted(subscale_scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (subscale_name, score) in enumerate(sorted_subscales):
            priority_level = "High" if i == 0 else "Medium" if i == 1 else "Low"
            
            priorities.append({
                "priority": i + 1,
                "subscale": subscale_name,
                "score": round(score, 2),
                "priority_level": priority_level,
                "description": self.SUBSCALES[subscale_name]["description"],
                "intervention_needed": score >= 3.0,
                "focus_areas": self._get_subscale_intervention_focus(subscale_name, score)
            })
        
        return priorities
    
    def _get_follow_up_recommendations(self, distress_level: str, total_score: float) -> Dict[str, Any]:
        """Get follow-up recommendations"""
        
        if distress_level == "high_distress":
            return {
                "frequency": "Monthly to quarterly",
                "monitoring_tools": ["DDS17 re-administration", "Clinical assessment", "HbA1c monitoring"],
                "care_coordination": "Multidisciplinary team approach with diabetes educator and mental health provider",
                "response_indicators": ["Reduction in DDS17 score", "Improved glycemic control", "Enhanced self-care behaviors"]
            }
        elif distress_level == "moderate_distress":
            return {
                "frequency": "Every 3-6 months",
                "monitoring_tools": ["DDS17 re-administration", "Routine diabetes care visits"],
                "care_coordination": "Primary care provider with diabetes education support",
                "response_indicators": ["Stable or reduced distress scores", "Maintained diabetes outcomes"]
            }
        else:
            return {
                "frequency": "Annual or as clinically indicated",
                "monitoring_tools": ["Periodic diabetes distress screening", "Routine diabetes care"],
                "care_coordination": "Standard diabetes care team",
                "response_indicators": ["Continued low distress levels", "Optimal diabetes management"]
            }
    
    def _get_referral_considerations(self, distress_level: str, subscale_scores: Dict[str, float]) -> List[str]:
        """Get referral considerations"""
        
        referrals = []
        
        if distress_level == "high_distress":
            referrals.append("Diabetes educator or certified diabetes care specialist")
            referrals.append("Mental health professional with diabetes expertise")
        
        if subscale_scores.get("emotional_burden", 0) >= 3.0:
            referrals.append("Psychologist or counselor for diabetes distress therapy")
        
        if subscale_scores.get("physician_distress", 0) >= 3.0:
            referrals.append("Endocrinologist or diabetes specialist for care optimization")
        
        if subscale_scores.get("regimen_distress", 0) >= 3.0:
            referrals.append("Diabetes educator for self-management skill building")
        
        if subscale_scores.get("interpersonal_distress", 0) >= 3.0:
            referrals.append("Family therapist or diabetes support group facilitator")
        
        return referrals if referrals else ["Continue with current care team"]
    
    def _get_monitoring_guidance(self, distress_level: str, total_score: float) -> Dict[str, Any]:
        """Get monitoring guidance"""
        
        return {
            "reassessment_interval": self._get_reassessment_interval(distress_level),
            "monitoring_parameters": [
                "DDS17 score trends over time",
                "Glycemic control (HbA1c)",
                "Diabetes self-care behaviors",
                "Quality of life indicators",
                "Healthcare utilization patterns"
            ],
            "red_flags": [
                "Increasing DDS17 scores over time",
                "Worsening glycemic control",
                "Decreased self-care adherence",
                "New or worsening mental health symptoms",
                "Social isolation or family conflict"
            ],
            "success_indicators": [
                "Stable or decreasing distress scores",
                "Improved diabetes self-management",
                "Enhanced patient-provider relationship",
                "Better family/social support",
                "Increased diabetes self-efficacy"
            ]
        }
    
    def _get_reassessment_interval(self, distress_level: str) -> str:
        """Get appropriate reassessment interval"""
        
        intervals = {
            "little_no_distress": "Annually or as clinically indicated",
            "moderate_distress": "Every 6 months",
            "high_distress": "Every 3 months initially, then adjust based on response"
        }
        
        return intervals[distress_level]
    
    def _get_interpretation(self, total_score: float, distress_level: str, 
                          subscale_scores: Dict[str, float]) -> str:
        """Get comprehensive interpretation"""
        
        distress_info = self.DISTRESS_LEVELS[distress_level]
        
        base_interpretation = (f"DDS17 total score of {total_score:.2f} indicates {distress_info['label']}. "
                             f"{distress_info['description']}.")
        
        # Add subscale insights
        high_subscales = [name for name, score in subscale_scores.items() if score >= 3.0]
        
        if high_subscales:
            subscale_names = [self.SUBSCALES[name]["name"] for name in high_subscales]
            base_interpretation += f" Highest distress areas: {', '.join(subscale_names)}."
        
        # Add clinical significance
        if total_score >= 3.0:
            base_interpretation += (" This level of distress is clinically significant and warrants "
                                  "targeted intervention and follow-up.")
        elif total_score >= 2.0:
            base_interpretation += (" Monitor for progression and consider targeted support for "
                                  "identified areas of concern.")
        else:
            base_interpretation += " Continue current diabetes management approach with routine monitoring."
        
        return base_interpretation


def calculate_diabetes_distress_scale(overwhelming_demands: int, feeling_discouraged: int, 
                                    failure_regimen: int, clear_concrete_goals: int, not_motivated: int,
                                    angry_frustrated: int, unsatisfied_care: int,
                                    physician_communication: int, physician_doesnt_give_direction: int,
                                    physician_doesnt_take_seriously: int, regimen_overwhelming: int,
                                    constant_thoughts: int, blood_sugar_checking: int, regimen_burden: int,
                                    friends_family_nagging: int, friends_family_interference: int, 
                                    friends_family_dont_understand: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DiabetesDistressScaleCalculator()
    return calculator.calculate(
        overwhelming_demands, feeling_discouraged, failure_regimen, clear_concrete_goals, not_motivated,
        angry_frustrated, unsatisfied_care, physician_communication,
        physician_doesnt_give_direction, physician_doesnt_take_seriously, regimen_overwhelming,
        constant_thoughts, blood_sugar_checking, regimen_burden,
        friends_family_nagging, friends_family_interference, friends_family_dont_understand
    )