"""
Coronavirus Anxiety Scale (CAS) Calculator

Assesses dysfunctional anxiety associated with the COVID-19 crisis through a brief 
5-item self-report screening tool.

References:
1. Lee SA. Coronavirus Anxiety Scale: A brief mental health screener for COVID-19 related anxiety. 
   Death Stud. 2020;44(7):393-401. doi: 10.1080/07481187.2020.1748481.
2. Lee SA, Jobe MC, Mathis AA, Gibbons JA. Incremental validity of coronaphobia: Coronavirus anxiety 
   explains depression, generalized anxiety, and death anxiety. J Anxiety Disord. 2020;74:102263. 
   doi: 10.1016/j.janxdis.2020.102263.
3. Lieven T, Kujath P, Araya M, et al. Global validation of the Coronavirus Anxiety Scale (CAS). 
   Curr Psychol. 2021;1-8. doi: 10.1007/s12144-021-01837-w.
"""

from typing import Dict, Any


class CasCalculator:
    """Calculator for Coronavirus Anxiety Scale (CAS)"""
    
    def __init__(self):
        # CAS scoring parameters
        self.MIN_SCORE = 0
        self.MAX_SCORE = 20  # 5 items × 4 points each
        self.DYSFUNCTIONAL_THRESHOLD = 9  # ≥9 indicates dysfunctional anxiety
        
        # Diagnostic performance characteristics
        self.SENSITIVITY = 0.90  # 90% sensitivity
        self.SPECIFICITY = 0.85  # 85% specificity
        
        # Item descriptions for reference
        self.ITEMS = {
            "dizzy_news": "I felt dizzy, lightheaded, or faint when I read or listened to news about the coronavirus",
            "sleep_problems": "I had trouble falling or staying asleep because I was thinking about the coronavirus",
            "paralyzed_frozen": "I felt paralyzed or frozen when I thought about or was exposed to information about the coronavirus",
            "appetite_loss": "I lost interest in eating when I thought about or was exposed to information about the coronavirus",
            "nausea_stomach": "I felt nauseous or had stomach problems when I thought about or was exposed to information about the coronavirus"
        }
        
        # Response option descriptions
        self.RESPONSE_OPTIONS = {
            0: "Not at all",
            1: "Rare, less than a day or two",
            2: "Several days",
            3: "More than 7 days",
            4: "Nearly every day over the last 2 weeks"
        }
    
    def calculate(
        self,
        dizzy_news: int,
        sleep_problems: int,
        paralyzed_frozen: int,
        appetite_loss: int,
        nausea_stomach: int
    ) -> Dict[str, Any]:
        """
        Calculates the Coronavirus Anxiety Scale (CAS) score
        
        Args:
            dizzy_news: Score for dizziness/lightheadedness when exposed to coronavirus news (0-4)
            sleep_problems: Score for sleep difficulties due to coronavirus thoughts (0-4)
            paralyzed_frozen: Score for feeling paralyzed/frozen when exposed to coronavirus info (0-4)
            appetite_loss: Score for appetite loss when thinking about coronavirus (0-4)
            nausea_stomach: Score for nausea/stomach problems when thinking about coronavirus (0-4)
            
        Returns:
            Dict with CAS assessment results and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(dizzy_news, sleep_problems, paralyzed_frozen, appetite_loss, nausea_stomach)
        
        # Calculate total score
        item_scores = {
            "dizzy_news": dizzy_news,
            "sleep_problems": sleep_problems,
            "paralyzed_frozen": paralyzed_frozen,
            "appetite_loss": appetite_loss,
            "nausea_stomach": nausea_stomach
        }
        
        total_score = sum(item_scores.values())
        
        # Determine anxiety level
        dysfunctional_anxiety = total_score >= self.DYSFUNCTIONAL_THRESHOLD
        
        # Analyze item responses
        item_analysis = self._analyze_items(item_scores)
        
        # Get clinical interpretation
        clinical_interpretation = self._get_clinical_interpretation(dysfunctional_anxiety, total_score)
        
        # Generate recommendations
        recommendations = self._get_recommendations(dysfunctional_anxiety, total_score, item_analysis)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": clinical_interpretation["interpretation"],
            "stage": clinical_interpretation["stage"],
            "stage_description": clinical_interpretation["description"],
            "assessment_details": {
                "dysfunctional_anxiety": dysfunctional_anxiety,
                "total_score": total_score,
                "max_possible_score": self.MAX_SCORE,
                "threshold": self.DYSFUNCTIONAL_THRESHOLD,
                "item_scores": item_analysis,
                "severity_level": clinical_interpretation["severity"],
                "diagnostic_performance": {
                    "sensitivity": f"{self.SENSITIVITY:.0%}",
                    "specificity": f"{self.SPECIFICITY:.0%}",
                    "note": "Diagnostic performance for identifying dysfunctional coronavirus-related anxiety"
                },
                "clinical_recommendations": recommendations,
                "assessment_context": self._get_assessment_context()
            }
        }
    
    def _validate_inputs(self, dizzy_news, sleep_problems, paralyzed_frozen, appetite_loss, nausea_stomach):
        """Validates input parameters"""
        
        scores = [dizzy_news, sleep_problems, paralyzed_frozen, appetite_loss, nausea_stomach]
        score_names = ["dizzy_news", "sleep_problems", "paralyzed_frozen", "appetite_loss", "nausea_stomach"]
        
        for score, name in zip(scores, score_names):
            if not isinstance(score, int):
                raise ValueError(f"{name} must be an integer")
            if score < 0 or score > 4:
                raise ValueError(f"{name} must be between 0 and 4")
    
    def _analyze_items(self, item_scores: Dict[str, int]) -> Dict[str, Dict]:
        """Analyzes individual item responses with clinical context"""
        
        analysis = {}
        
        for item, score in item_scores.items():
            severity = self._get_item_severity(score)
            analysis[item] = {
                "score": score,
                "max_score": 4,
                "description": self.ITEMS[item],
                "response": self.RESPONSE_OPTIONS[score],
                "severity": severity,
                "clinical_significance": self._get_item_significance(item, score)
            }
        
        return analysis
    
    def _get_item_severity(self, score: int) -> str:
        """Determines severity level for individual item scores"""
        
        if score == 0:
            return "None"
        elif score == 1:
            return "Minimal"
        elif score == 2:
            return "Mild"
        elif score == 3:
            return "Moderate"
        else:  # score == 4
            return "Severe"
    
    def _get_item_significance(self, item: str, score: int) -> str:
        """Provides clinical significance for individual item scores"""
        
        significance_map = {
            "dizzy_news": {
                0: "No physical anxiety response to coronavirus news",
                1: "Minimal physical anxiety symptoms with coronavirus news exposure",
                2: "Mild physical anxiety symptoms affecting news consumption",
                3: "Moderate physical anxiety symptoms limiting news exposure",
                4: "Severe physical anxiety symptoms severely limiting news consumption"
            },
            "sleep_problems": {
                0: "No sleep disruption from coronavirus thoughts",
                1: "Minimal sleep disruption from coronavirus concerns",
                2: "Mild sleep difficulties affecting rest quality",
                3: "Moderate sleep problems impacting daily functioning",
                4: "Severe sleep disruption significantly affecting health and functioning"
            },
            "paralyzed_frozen": {
                0: "No paralytic anxiety response to coronavirus information",
                1: "Minimal feelings of being overwhelmed by coronavirus information",
                2: "Mild paralytic response affecting information processing",
                3: "Moderate paralytic response limiting daily activities",
                4: "Severe paralytic response significantly impairing functioning"
            },
            "appetite_loss": {
                0: "No appetite changes related to coronavirus thoughts",
                1: "Minimal appetite changes with coronavirus concerns",
                2: "Mild appetite loss affecting eating patterns",
                3: "Moderate appetite loss impacting nutrition",
                4: "Severe appetite loss posing health risks"
            },
            "nausea_stomach": {
                0: "No gastrointestinal anxiety symptoms with coronavirus thoughts",
                1: "Minimal gastrointestinal discomfort with coronavirus concerns",
                2: "Mild gastrointestinal symptoms affecting comfort",
                3: "Moderate gastrointestinal symptoms impacting daily activities",
                4: "Severe gastrointestinal symptoms significantly affecting functioning"
            }
        }
        
        return significance_map.get(item, {}).get(score, "Score significance not available")
    
    def _get_clinical_interpretation(self, dysfunctional_anxiety: bool, total_score: int) -> Dict[str, str]:
        """Generates clinical interpretation of CAS results"""
        
        if dysfunctional_anxiety:
            stage = "Dysfunctional Anxiety"
            description = "Clinically significant coronavirus-related anxiety"
            
            if total_score >= 16:
                severity = "severe"
                interpretation = (f"CAS score of {total_score}/{self.MAX_SCORE} indicates severe dysfunctional "
                                f"coronavirus-related anxiety. Comprehensive mental health evaluation and "
                                f"immediate intervention recommended.")
            elif total_score >= 12:
                severity = "moderate"
                interpretation = (f"CAS score of {total_score}/{self.MAX_SCORE} indicates moderate dysfunctional "
                                f"coronavirus-related anxiety. Mental health evaluation and therapeutic "
                                f"intervention recommended.")
            else:
                severity = "mild"
                interpretation = (f"CAS score of {total_score}/{self.MAX_SCORE} indicates mild dysfunctional "
                                f"coronavirus-related anxiety. Monitoring and supportive interventions "
                                f"recommended.")
        else:
            stage = "No Dysfunctional Anxiety"
            description = "Normal coronavirus-related concerns"
            severity = "none"
            interpretation = (f"CAS score of {total_score}/{self.MAX_SCORE} is below the threshold of "
                            f"{self.DYSFUNCTIONAL_THRESHOLD} for dysfunctional anxiety. Individual may "
                            f"experience normal concerns about COVID-19 but these do not significantly "
                            f"impair functioning.")
        
        return {
            "stage": stage,
            "description": description,
            "severity": severity,
            "interpretation": interpretation
        }
    
    def _get_recommendations(self, dysfunctional_anxiety: bool, total_score: int, item_analysis: Dict) -> Dict[str, list]:
        """Generates clinical recommendations based on CAS results"""
        
        recommendations = {
            "immediate_actions": [],
            "therapeutic_interventions": [],
            "self_care_strategies": [],
            "monitoring": [],
            "follow_up": []
        }
        
        if dysfunctional_anxiety:
            if total_score >= 16:
                recommendations["immediate_actions"] = [
                    "Comprehensive mental health evaluation recommended",
                    "Consider immediate professional intervention",
                    "Assess for risk of self-harm or suicide",
                    "Evaluate need for crisis intervention services"
                ]
                
                recommendations["therapeutic_interventions"] = [
                    "Cognitive-behavioral therapy (CBT) for anxiety management",
                    "Exposure therapy for coronavirus-related avoidance",
                    "Consider pharmacological intervention consultation",
                    "Trauma-informed care if applicable"
                ]
                
                recommendations["follow_up"] = [
                    "Weekly clinical monitoring initially",
                    "Reassess CAS score in 2-4 weeks",
                    "Coordinate with primary care provider"
                ]
                
            elif total_score >= 12:
                recommendations["immediate_actions"] = [
                    "Mental health evaluation recommended",
                    "Assess functional impairment levels",
                    "Screen for comorbid mental health conditions"
                ]
                
                recommendations["therapeutic_interventions"] = [
                    "Cognitive-behavioral therapy for anxiety",
                    "Mindfulness-based interventions",
                    "Stress management techniques",
                    "Consider group therapy for pandemic-related anxiety"
                ]
                
                recommendations["follow_up"] = [
                    "Bi-weekly monitoring recommended",
                    "Reassess in 4-6 weeks"
                ]
                
            else:  # Score 9-11
                recommendations["immediate_actions"] = [
                    "Supportive counseling recommended",
                    "Assess coping mechanisms and support systems"
                ]
                
                recommendations["therapeutic_interventions"] = [
                    "Brief supportive therapy",
                    "Psychoeducation about anxiety management",
                    "Relaxation techniques training"
                ]
        
        else:
            recommendations["immediate_actions"] = [
                "Continue current coping strategies",
                "Maintain healthy lifestyle habits"
            ]
            
            recommendations["therapeutic_interventions"] = [
                "Preventive psychoeducation if desired",
                "Stress management skills building"
            ]
            
            recommendations["follow_up"] = [
                "Routine monitoring as needed",
                "Re-screen if circumstances change"
            ]
        
        # Add general recommendations for all scores
        recommendations["self_care_strategies"] = [
            "Limit excessive coronavirus news consumption",
            "Maintain regular sleep and exercise routines",
            "Practice relaxation and mindfulness techniques",
            "Stay connected with social support networks",
            "Engage in pleasant and meaningful activities"
        ]
        
        recommendations["monitoring"] = [
            "Monitor for changes in anxiety symptoms",
            "Track functional impairment levels",
            "Assess coping strategy effectiveness",
            "Watch for development of other mental health symptoms"
        ]
        
        # Add symptom-specific recommendations
        high_scoring_items = [item for item, data in item_analysis.items() if data["score"] >= 3]
        if high_scoring_items:
            if "sleep_problems" in high_scoring_items:
                recommendations["self_care_strategies"].append("Implement sleep hygiene practices")
            if "appetite_loss" in high_scoring_items:
                recommendations["monitoring"].append("Monitor nutritional status and weight")
            if "nausea_stomach" in high_scoring_items:
                recommendations["immediate_actions"].append("Consider medical evaluation for physical symptoms")
        
        return recommendations
    
    def _get_assessment_context(self) -> Dict[str, str]:
        """Provides context about the CAS assessment"""
        
        return {
            "time_frame": "Last 2 weeks",
            "purpose": "Screening for dysfunctional coronavirus-related anxiety",
            "target_population": "Adults experiencing potential COVID-19 related anxiety",
            "administration": "Self-report questionnaire",
            "limitations": [
                "Screening tool only - does not replace comprehensive mental health evaluation",
                "Specific to coronavirus-related anxiety, not general anxiety disorders",
                "Cultural and linguistic considerations may affect interpretation",
                "May need periodic re-administration as pandemic conditions change"
            ],
            "validation_note": f"Cut-off score ≥{self.DYSFUNCTIONAL_THRESHOLD} has {self.SENSITIVITY:.0%} sensitivity and {self.SPECIFICITY:.0%} specificity"
        }


def calculate_cas(
    dizzy_news: int,
    sleep_problems: int,
    paralyzed_frozen: int,
    appetite_loss: int,
    nausea_stomach: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CasCalculator()
    return calculator.calculate(
        dizzy_news=dizzy_news,
        sleep_problems=sleep_problems,
        paralyzed_frozen=paralyzed_frozen,
        appetite_loss=appetite_loss,
        nausea_stomach=nausea_stomach
    )