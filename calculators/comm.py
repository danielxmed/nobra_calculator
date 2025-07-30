"""
Current Opioid Misuse Measure (COMM) Calculator

Identifies potential medication misuse in patients who are on long-term opioid therapy.
The COMM is a validated self-report instrument for identifying and monitoring opioid 
misuse in chronic pain patients taking prescription opioids for pain management.

References:
- Butler SF, Budman SH, Fernandez KC, et al. Pain. 2007;130(1-2):144-156.
- Butler SF, Budman SH, Fanciullo GJ, Jamison RN. Clin J Pain. 2010;26(9):770-776.
- Meltzer EC, Rybin D, Saitz R, et al. Pain. 2011;152(2):397-402.
"""

from typing import Dict, Any


class CommCalculator:
    """Calculator for Current Opioid Misuse Measure (COMM)"""
    
    def __init__(self):
        # COMM question categories for analysis
        self.QUESTION_CATEGORIES = {
            "behavioral": ["taking_differently", "taking_more_than_prescribed", "relief_other_sources", 
                          "need_medications_from_others", "borrowing_pain_medication"],
            "psychological": ["thinking_clearly", "thinking_hurting_self", "time_thinking_medications",
                            "being_in_arguments", "trouble_controlling_anger", "getting_angry_with_people"],
            "functional": ["not_completing_tasks"],
            "healthcare_seeking": ["emergency_clinic_visits", "visiting_emergency_room"],
            "substance_concerns": ["worried_handling_medications", "others_worried_handling", 
                                 "using_for_non_pain_symptoms"]
        }
        
        # Response labels
        self.RESPONSE_LABELS = {
            0: "Never",
            1: "Seldom", 
            2: "Sometimes",
            3: "Often",
            4: "Very often"
        }
        
        # High-risk question indicators
        self.HIGH_RISK_QUESTIONS = [
            "taking_more_than_prescribed", "borrowing_pain_medication", 
            "need_medications_from_others", "relief_other_sources",
            "using_for_non_pain_symptoms", "thinking_hurting_self"
        ]
    
    def calculate(self, thinking_clearly: int, not_completing_tasks: int, relief_other_sources: int,
                  taking_differently: int, thinking_hurting_self: int, time_thinking_medications: int,
                  being_in_arguments: int, trouble_controlling_anger: int, need_medications_from_others: int,
                  worried_handling_medications: int, others_worried_handling: int, emergency_clinic_visits: int,
                  getting_angry_with_people: int, taking_more_than_prescribed: int, borrowing_pain_medication: int,
                  using_for_non_pain_symptoms: int, visiting_emergency_room: int) -> Dict[str, Any]:
        """
        Calculates COMM assessment and risk categorization
        
        Args:
            thinking_clearly (int): Trouble thinking clearly or memory problems (0-4)
            not_completing_tasks (int): People complaining about not completing tasks (0-4)
            relief_other_sources (int): Getting pain relief from other sources (0-4)
            taking_differently (int): Taking medications differently than prescribed (0-4)
            thinking_hurting_self (int): Seriously thinking about hurting yourself (0-4)
            time_thinking_medications (int): Time spent thinking about opioid medications (0-4)
            being_in_arguments (int): Being in arguments (0-4)
            trouble_controlling_anger (int): Trouble controlling anger (0-4)
            need_medications_from_others (int): Needing to take pain medications from others (0-4)
            worried_handling_medications (int): Being worried about handling medications (0-4)
            others_worried_handling (int): Others being worried about medication handling (0-4)
            emergency_clinic_visits (int): Making emergency clinic calls/visits (0-4)
            getting_angry_with_people (int): Getting angry with people (0-4)
            taking_more_than_prescribed (int): Taking more medication than prescribed (0-4)
            borrowing_pain_medication (int): Borrowing pain medication from others (0-4)
            using_for_non_pain_symptoms (int): Using pain medicine for non-pain symptoms (0-4)
            visiting_emergency_room (int): Visiting the Emergency Room (0-4)
            
        Returns:
            Dict with total score, risk assessment, and detailed analysis
        """
        
        # Collect all responses
        responses = {
            "thinking_clearly": thinking_clearly,
            "not_completing_tasks": not_completing_tasks,
            "relief_other_sources": relief_other_sources,
            "taking_differently": taking_differently,
            "thinking_hurting_self": thinking_hurting_self,
            "time_thinking_medications": time_thinking_medications,
            "being_in_arguments": being_in_arguments,
            "trouble_controlling_anger": trouble_controlling_anger,
            "need_medications_from_others": need_medications_from_others,
            "worried_handling_medications": worried_handling_medications,
            "others_worried_handling": others_worried_handling,
            "emergency_clinic_visits": emergency_clinic_visits,
            "getting_angry_with_people": getting_angry_with_people,
            "taking_more_than_prescribed": taking_more_than_prescribed,
            "borrowing_pain_medication": borrowing_pain_medication,
            "using_for_non_pain_symptoms": using_for_non_pain_symptoms,
            "visiting_emergency_room": visiting_emergency_room
        }
        
        # Validations
        self._validate_inputs(responses)
        
        # Calculate total score
        total_score = sum(responses.values())
        
        # Determine risk category
        risk_category = self._get_risk_category(total_score)
        
        # Analyze response patterns
        pattern_analysis = self._analyze_response_patterns(responses)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score, pattern_analysis)
        
        # Get recommendations
        recommendations = self._get_clinical_recommendations(total_score, pattern_analysis)
        
        # Generate risk factors summary
        risk_factors = self._identify_risk_factors(responses)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation,
            "stage": risk_category["stage"],
            "stage_description": risk_category["description"],
            "total_score": total_score,
            "risk_level": risk_category["risk_level"],
            "misuse_risk": risk_category["misuse_risk"],
            "pattern_analysis": pattern_analysis,
            "risk_factors": risk_factors,
            "clinical_recommendations": recommendations,
            "monitoring_guidance": self._get_monitoring_guidance(total_score, pattern_analysis),
            "red_flags": self._identify_red_flags(responses),
            "category_scores": self._calculate_category_scores(responses)
        }
    
    def _validate_inputs(self, responses):
        """Validates input parameters"""
        
        if len(responses) != 17:
            raise ValueError("Exactly 17 COMM questions must be answered")
        
        for question, score in responses.items():
            if not isinstance(score, int) or not 0 <= score <= 4:
                raise ValueError(f"{question} must be an integer between 0 and 4")
    
    def _get_risk_category(self, total_score):
        """Determines risk category based on total score"""
        
        if total_score < 9:
            return {
                "stage": "Low Risk",
                "description": "Not misusing or abusing medications",
                "risk_level": "low",
                "misuse_risk": "Low risk for opioid misuse"
            }
        else:
            return {
                "stage": "High Risk", 
                "description": "Possible misuse or abuse of medications",
                "risk_level": "high",
                "misuse_risk": "Elevated risk for opioid misuse"
            }
    
    def _analyze_response_patterns(self, responses):
        """Analyzes response patterns across COMM categories"""
        
        category_scores = self._calculate_category_scores(responses)
        
        # Count responses by frequency
        frequency_counts = {label: 0 for label in self.RESPONSE_LABELS.values()}
        for score in responses.values():
            frequency_counts[self.RESPONSE_LABELS[score]] += 1
        
        # Identify concerning patterns
        concerning_responses = sum(1 for score in responses.values() if score >= 3)
        moderate_responses = sum(1 for score in responses.values() if score == 2)
        
        return {
            "category_scores": category_scores,
            "frequency_distribution": frequency_counts,
            "concerning_responses": concerning_responses,
            "moderate_responses": moderate_responses,
            "total_positive_responses": sum(1 for score in responses.values() if score > 0),
            "severity_pattern": self._assess_severity_pattern(responses)
        }
    
    def _calculate_category_scores(self, responses):
        """Calculates scores for each COMM category"""
        
        category_scores = {}
        
        for category, questions in self.QUESTION_CATEGORIES.items():
            total = sum(responses.get(q, 0) for q in questions)
            max_possible = len(questions) * 4
            percentage = (total / max_possible) * 100 if max_possible > 0 else 0
            
            category_scores[category] = {
                "score": total,
                "max_possible": max_possible,
                "percentage": round(percentage, 1),
                "questions_count": len(questions)
            }
        
        return category_scores
    
    def _assess_severity_pattern(self, responses):
        """Assesses the overall severity pattern of responses"""
        
        high_scores = sum(1 for score in responses.values() if score >= 3)
        moderate_scores = sum(1 for score in responses.values() if score == 2)
        
        if high_scores >= 5:
            return "Severe pattern - Multiple frequent concerning behaviors"
        elif high_scores >= 3:
            return "Moderate-severe pattern - Several frequent concerning behaviors"
        elif high_scores >= 1 or moderate_scores >= 5:
            return "Moderate pattern - Some concerning behaviors"
        elif moderate_scores >= 2:
            return "Mild pattern - Occasional concerning behaviors"
        else:
            return "Minimal pattern - Few concerning behaviors"
    
    def _identify_risk_factors(self, responses):
        """Identifies specific risk factors based on responses"""
        
        risk_factors = []
        
        # High-risk behaviors
        for question in self.HIGH_RISK_QUESTIONS:
            if responses.get(question, 0) >= 2:
                risk_factors.append(f"Reports {self.RESPONSE_LABELS[responses[question]].lower()} {question.replace('_', ' ')}")
        
        # Psychological concerns
        if responses.get("thinking_hurting_self", 0) >= 1:
            risk_factors.append("Endorses thoughts of self-harm")
        
        # Healthcare seeking patterns
        if responses.get("emergency_clinic_visits", 0) >= 2 or responses.get("visiting_emergency_room", 0) >= 2:
            risk_factors.append("Frequent emergency healthcare utilization")
        
        # Functional impairment
        if responses.get("not_completing_tasks", 0) >= 2:
            risk_factors.append("Functional impairment affecting task completion")
        
        # Medication concerns
        if (responses.get("worried_handling_medications", 0) >= 2 or 
            responses.get("others_worried_handling", 0) >= 2):
            risk_factors.append("Medication handling concerns (self or others)")
        
        return risk_factors
    
    def _identify_red_flags(self, responses):
        """Identifies immediate red flag indicators"""
        
        red_flags = []
        
        # Immediate safety concerns
        if responses.get("thinking_hurting_self", 0) >= 2:
            red_flags.append("Significant self-harm ideation")
        
        # Clear misuse behaviors
        if responses.get("taking_more_than_prescribed", 0) >= 3:
            red_flags.append("Frequent dose escalation beyond prescription")
        
        if responses.get("borrowing_pain_medication", 0) >= 2:
            red_flags.append("Obtaining medication from unauthorized sources")
        
        if responses.get("using_for_non_pain_symptoms", 0) >= 2:
            red_flags.append("Using opioids for non-pain indications")
        
        # Loss of control indicators
        if responses.get("time_thinking_medications", 0) >= 3:
            red_flags.append("Preoccupation with opioid medications")
        
        return red_flags
    
    def _get_interpretation(self, total_score, pattern_analysis):
        """Get comprehensive interpretation of COMM results"""
        
        if total_score < 9:
            return (f"COMM total score of {total_score} is below the threshold (≥9) for opioid misuse risk. "
                   f"This suggests low probability of current opioid misuse behaviors. "
                   f"Patient demonstrates {pattern_analysis['severity_pattern'].lower()}. "
                   f"Continue standard monitoring and pain management protocols with routine reassessment.")
        
        else:
            return (f"COMM total score of {total_score} meets or exceeds the threshold (≥9) indicating elevated "
                   f"risk for opioid misuse. Patient demonstrates {pattern_analysis['severity_pattern'].lower()} "
                   f"with {pattern_analysis['concerning_responses']} concerning responses. "
                   f"Further evaluation and enhanced monitoring are recommended. Consider substance abuse "
                   f"consultation and implementation of risk mitigation strategies.")
    
    def _get_clinical_recommendations(self, total_score, pattern_analysis):
        """Get clinical recommendations based on COMM assessment"""
        
        recommendations = []
        
        if total_score < 9:
            recommendations.extend([
                "Continue current pain management approach",
                "Routine monitoring with periodic COMM reassessment",
                "Standard opioid safety education and counseling",
                "Regular pain and function assessment"
            ])
        else:
            recommendations.extend([
                "Enhanced monitoring and more frequent visits",
                "Consider urine drug testing and pill counts",
                "Evaluate for substance use disorder",
                "Consider substance abuse consultation",
                "Review and potentially modify opioid regimen",
                "Implement additional risk mitigation strategies"
            ])
        
        # Add specific recommendations based on red flags
        if pattern_analysis["concerning_responses"] >= 5:
            recommendations.append("Consider intensive intervention due to multiple concerning behaviors")
        
        return recommendations
    
    def _get_monitoring_guidance(self, total_score, pattern_analysis):
        """Get monitoring guidance based on assessment"""
        
        if total_score < 9:
            return {
                "frequency": "Every 3-6 months or as clinically indicated",
                "intensity": "Standard monitoring",
                "methods": ["Clinical assessment", "COMM reassessment", "Pain and function evaluation"],
                "additional_measures": "None routinely required"
            }
        else:
            frequency = "Monthly" if total_score >= 15 else "Every 1-2 months"
            additional = []
            
            if pattern_analysis["concerning_responses"] >= 3:
                additional.extend(["Urine drug testing", "Pill counts", "Prescription monitoring"])
            
            return {
                "frequency": frequency,
                "intensity": "Enhanced monitoring",
                "methods": ["Clinical assessment", "COMM reassessment", "Structured interviews"],
                "additional_measures": additional if additional else ["Consider urine drug testing"]
            }


def calculate_comm(thinking_clearly: int, not_completing_tasks: int, relief_other_sources: int,
                   taking_differently: int, thinking_hurting_self: int, time_thinking_medications: int,
                   being_in_arguments: int, trouble_controlling_anger: int, need_medications_from_others: int,
                   worried_handling_medications: int, others_worried_handling: int, emergency_clinic_visits: int,
                   getting_angry_with_people: int, taking_more_than_prescribed: int, borrowing_pain_medication: int,
                   using_for_non_pain_symptoms: int, visiting_emergency_room: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CommCalculator()
    return calculator.calculate(
        thinking_clearly, not_completing_tasks, relief_other_sources, taking_differently,
        thinking_hurting_self, time_thinking_medications, being_in_arguments, trouble_controlling_anger,
        need_medications_from_others, worried_handling_medications, others_worried_handling,
        emergency_clinic_visits, getting_angry_with_people, taking_more_than_prescribed,
        borrowing_pain_medication, using_for_non_pain_symptoms, visiting_emergency_room
    )