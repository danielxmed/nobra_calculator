"""
Cornell Assessment of Pediatric Delirium (CAPD) Calculator

Screens for delirium in pediatric patients through behavioral assessment of awareness,
cognition, and psychomotor symptoms.

References:
1. Traube C, Silver G, Kearney J, Patel A, Atkinson TM, Yoon MJ, et al. Cornell Assessment 
   of Pediatric Delirium: a valid, rapid, observational tool for screening delirium in the PICU. 
   Crit Care Med. 2014 Mar;42(3):656-63. doi: 10.1097/CCM.0b013e3182a66b76.
2. Silver G, Traube C, Gerber LM, Sun X, Kearney J, Patel A, et al. Pediatric delirium and 
   associated risk factors: a single-center prospective observational study. Pediatr Crit Care Med. 
   2015 May;16(4):303-9. doi: 10.1097/PCC.0000000000000356.
3. Traube C, Silver G, Gerber LM, Kaur S, Mauer EA, Kerson A, et al. Delirium and mortality in 
   critically ill children: epidemiology and outcomes of pediatric delirium. Crit Care Med. 
   2017 May;45(5):891-898. doi: 10.1097/CCM.0000000000002324.
"""

from typing import Dict, Any


class CapdCalculator:
    """Calculator for Cornell Assessment of Pediatric Delirium (CAPD)"""
    
    def __init__(self):
        # CAPD scoring parameters
        self.MIN_SCORE = 0
        self.MAX_SCORE = 32  # 8 domains × 4 points each
        self.DELIRIUM_THRESHOLD = 9  # ≥9 indicates delirium
        
        # Age groups for developmental context
        self.AGE_GROUPS = {
            "newborn": (0, 0.08),      # 0-1 month
            "infant_early": (0.08, 0.5), # 1-6 months  
            "infant_late": (0.5, 1),    # 6-12 months
            "toddler": (1, 3),          # 1-3 years
            "preschool": (3, 6),        # 3-6 years
            "school_age": (6, 13),      # 6-13 years
            "adolescent": (13, 21)      # 13-21 years
        }
        
        # Domain descriptions
        self.DOMAINS = {
            "eye_contact": "Makes eye contact with caregiver",
            "purposeful_actions": "Actions are purposeful", 
            "aware_surroundings": "Aware of surroundings",
            "communicates_needs": "Communicates needs and wants",
            "restless": "Restless",
            "inconsolable": "Inconsolable",
            "underactive": "Underactive (very little movement while awake)",
            "slow_response": "Takes long time to respond to interactions"
        }
    
    def calculate(
        self,
        eye_contact: int,
        purposeful_actions: int,
        aware_surroundings: int,
        communicates_needs: int,
        restless: int,
        inconsolable: int,
        underactive: int,
        slow_response: int,
        patient_age: int
    ) -> Dict[str, Any]:
        """
        Evaluates pediatric delirium using CAPD criteria
        
        Args:
            eye_contact: Eye contact with caregiver (0-4 points)
            purposeful_actions: Actions are purposeful (0-4 points)
            aware_surroundings: Aware of surroundings (0-4 points)
            communicates_needs: Communicates needs and wants (0-4 points)
            restless: Restless behavior (0-4 points)
            inconsolable: Inconsolable behavior (0-4 points)
            underactive: Underactive behavior (0-4 points)
            slow_response: Slow response to interactions (0-4 points)
            patient_age: Patient age in years (0-21)
            
        Returns:
            Dict with CAPD assessment results and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            eye_contact, purposeful_actions, aware_surroundings, communicates_needs,
            restless, inconsolable, underactive, slow_response, patient_age
        )
        
        # Calculate total score
        domain_scores = {
            "eye_contact": eye_contact,
            "purposeful_actions": purposeful_actions,
            "aware_surroundings": aware_surroundings,
            "communicates_needs": communicates_needs,
            "restless": restless,
            "inconsolable": inconsolable,
            "underactive": underactive,
            "slow_response": slow_response
        }
        
        total_score = sum(domain_scores.values())
        
        # Determine delirium status
        capd_positive = total_score >= self.DELIRIUM_THRESHOLD
        
        # Get age group and developmental context
        age_group = self._get_age_group(patient_age)
        
        # Generate detailed assessment
        domain_analysis = self._analyze_domains(domain_scores)
        clinical_interpretation = self._get_clinical_interpretation(capd_positive, total_score, age_group)
        management_recommendations = self._get_management_recommendations(capd_positive, domain_analysis, age_group)
        
        return {
            "result": {
                "capd_positive": capd_positive,
                "total_score": total_score,
                "max_possible_score": self.MAX_SCORE,
                "delirium_threshold": self.DELIRIUM_THRESHOLD,
                "domain_scores": domain_analysis,
                "age_group": age_group,
                "clinical_interpretation": clinical_interpretation,
                "management_recommendations": management_recommendations,
                "screening_performance": self._get_screening_performance(age_group)
            },
            "unit": "assessment",
            "interpretation": clinical_interpretation["interpretation"],
            "stage": clinical_interpretation["stage"],
            "stage_description": clinical_interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        if len(args) != 9:
            raise ValueError("Expected 9 parameters: 8 domain scores and patient_age")
        
        scores = args[:-1]  # First 8 parameters (domain scores)
        patient_age = args[-1]  # Last parameter (patient_age)
        
        # Validate domain scores (first 8 parameters)
        for i, score in enumerate(scores):
            if not isinstance(score, int) or score < 0 or score > 4:
                domain_name = list(self.DOMAINS.keys())[i]
                raise ValueError(f"{domain_name} score must be integer between 0 and 4")
        
        # Validate patient age
        if not isinstance(patient_age, int) or patient_age < 0 or patient_age > 21:
            raise ValueError("Patient age must be integer between 0 and 21 years")
    
    def _get_age_group(self, age):
        """Determines age group for developmental context"""
        
        for group_name, (min_age, max_age) in self.AGE_GROUPS.items():
            if min_age <= age < max_age:
                return {
                    "group": group_name.replace("_", " ").title(),
                    "age_range": f"{min_age}-{max_age} years" if max_age >= 1 else f"{int(min_age*12)}-{int(max_age*12)} months",
                    "developmental_considerations": self._get_developmental_considerations(group_name)
                }
        
        # Handle edge case for exactly 21 years
        if age == 21:
            return {
                "group": "Adolescent",
                "age_range": "13-21 years",
                "developmental_considerations": self._get_developmental_considerations("adolescent")
            }
    
    def _get_developmental_considerations(self, age_group):
        """Provides age-specific developmental considerations"""
        
        considerations = {
            "newborn": [
                "Limited eye contact and social interaction abilities",
                "Communication primarily through crying and basic reflexes",
                "Movement patterns are largely reflexive",
                "Assessment relies heavily on changes from baseline behavior"
            ],
            "infant_early": [
                "Developing social smile and eye contact patterns",
                "Beginning purposeful reaching and grasping",
                "Increased responsiveness to caregivers",
                "Sleep-wake cycles becoming more established"
            ],
            "infant_late": [
                "Clear recognition of familiar caregivers",
                "Purposeful object manipulation and exploration",
                "Beginning stranger anxiety may affect assessment",
                "More predictable behavioral patterns"
            ],
            "toddler": [
                "Language development affects communication assessment",
                "Increased mobility and exploration behaviors",
                "Normal oppositional behaviors may complicate assessment",
                "Separation anxiety common in hospital settings"
            ],
            "preschool": [
                "Improved verbal communication abilities",
                "Fantasy play and imagination may affect reality testing",
                "Increased cooperation with assessment procedures",
                "Beginning understanding of illness and hospitalization"
            ],
            "school_age": [
                "Concrete operational thinking develops",
                "Increased ability to articulate experiences",
                "Better cooperation with medical procedures",
                "Peer relationships become important"
            ],
            "adolescent": [
                "Abstract thinking and reasoning abilities",
                "Identity formation and independence seeking",
                "May be less cooperative with assessment",
                "Privacy concerns and body image issues"
            ]
        }
        
        return considerations.get(age_group, [])
    
    def _analyze_domains(self, domain_scores):
        """Analyzes individual domain scores with clinical context"""
        
        analysis = {}
        
        for domain, score in domain_scores.items():
            severity = self._get_severity_level(score)
            analysis[domain] = {
                "score": score,
                "max_score": 4,
                "description": self.DOMAINS[domain],
                "severity": severity,
                "clinical_significance": self._get_domain_significance(domain, score)
            }
        
        return analysis
    
    def _get_severity_level(self, score):
        """Determines severity level for individual domain scores"""
        
        if score == 0:
            return "Normal"
        elif score == 1:
            return "Mild"
        elif score == 2:
            return "Moderate"  
        elif score == 3:
            return "Severe"
        else:  # score == 4
            return "Very Severe"
    
    def _get_domain_significance(self, domain, score):
        """Provides clinical significance for domain scores"""
        
        significance_map = {
            "eye_contact": {
                0: "Normal eye contact pattern for age",
                1: "Slightly reduced eye contact", 
                2: "Moderately impaired eye contact",
                3: "Severely impaired eye contact",
                4: "No eye contact observed"
            },
            "purposeful_actions": {
                0: "All actions appear purposeful and goal-directed",
                1: "Slightly reduced purposeful actions",
                2: "Moderately impaired purposeful behavior", 
                3: "Severely disorganized actions",
                4: "No purposeful actions observed"
            },
            "aware_surroundings": {
                0: "Fully aware of environment and situation",
                1: "Slightly reduced environmental awareness",
                2: "Moderately impaired situational awareness",
                3: "Severely reduced awareness of surroundings", 
                4: "No apparent awareness of environment"
            },
            "communicates_needs": {
                0: "Effectively communicates needs and wants",
                1: "Slightly impaired communication",
                2: "Moderately reduced communication ability",
                3: "Severely impaired communication",
                4: "Unable to communicate needs"
            },
            "restless": {
                0: "No restless behavior observed",
                1: "Rare episodes of restlessness",
                2: "Occasional restless behavior",
                3: "Frequent restlessness",
                4: "Constant restless behavior"
            },
            "inconsolable": {
                0: "Easily consoled when distressed",
                1: "Rarely inconsolable",
                2: "Sometimes difficult to console",
                3: "Often inconsolable",
                4: "Always inconsolable when distressed"
            },
            "underactive": {
                0: "Normal activity level for age",
                1: "Slightly reduced activity",
                2: "Moderately underactive",
                3: "Markedly reduced activity",
                4: "Very little movement while awake"
            },
            "slow_response": {
                0: "Normal response time to interactions",
                1: "Slightly delayed responses",
                2: "Moderately slow to respond",
                3: "Markedly delayed responses",
                4: "Very slow or no response to interactions"
            }
        }
        
        return significance_map.get(domain, {}).get(score, "Score interpretation not available")
    
    def _get_clinical_interpretation(self, capd_positive, total_score, age_group):
        """Generates clinical interpretation of CAPD results"""
        
        if capd_positive:
            stage = "CAPD Positive"
            description = "Delirium present"
            
            if total_score >= 20:
                severity = "severe"
                interpretation = (f"Patient meets CAPD criteria for delirium with a high score of {total_score}/32, "
                                f"suggesting severe delirium symptoms. Immediate comprehensive evaluation and "
                                f"intervention are required.")
            elif total_score >= 15:
                severity = "moderate"
                interpretation = (f"Patient meets CAPD criteria for delirium with a score of {total_score}/32, "
                                f"indicating moderate delirium symptoms. Prompt evaluation and management "
                                f"are recommended.")
            else:
                severity = "mild"
                interpretation = (f"Patient meets CAPD criteria for delirium with a score of {total_score}/32, "
                                f"suggesting mild delirium symptoms. Early intervention may prevent progression.")
        else:
            stage = "CAPD Negative"
            description = "No delirium detected"
            severity = "none"
            interpretation = (f"Patient does not meet CAPD criteria for delirium with a score of {total_score}/32 "
                            f"(below threshold of {self.DELIRIUM_THRESHOLD}). Continue routine monitoring as "
                            f"delirium can fluctuate or develop suddenly.")
        
        return {
            "stage": stage,
            "description": description,
            "severity": severity,
            "interpretation": interpretation,
            "age_considerations": f"Assessment performed in {age_group['group'].lower()} age group"
        }
    
    def _get_management_recommendations(self, capd_positive, domain_analysis, age_group):
        """Generates management recommendations based on CAPD results"""
        
        recommendations = {
            "immediate_actions": [],
            "ongoing_monitoring": [],
            "prevention_strategies": [],
            "family_involvement": [],
            "reassessment_timing": ""
        }
        
        if capd_positive:
            recommendations["immediate_actions"] = [
                "Implement pediatric delirium management protocol",
                "Evaluate for underlying causes (infection, metabolic disturbances, medications)",
                "Review and optimize all medications for deliriogenic effects",
                "Ensure adequate pain control without oversedation",
                "Optimize sleep-wake cycles and environmental conditions"
            ]
            
            recommendations["ongoing_monitoring"] = [
                "Continue CAPD assessments every nursing shift",
                "Monitor for delirium-related complications and safety issues",
                "Assess response to interventions and adjust treatment plan",
                "Document behavioral changes and intervention effectiveness"
            ]
            
            recommendations["prevention_strategies"] = [
                "Minimize environmental stimulation during rest periods",
                "Provide age-appropriate comfort items and familiar objects",
                "Maintain consistent caregiving staff when possible",
                "Encourage early mobilization as medically appropriate"
            ]
            
            recommendations["family_involvement"] = [
                "Educate family about pediatric delirium and management strategies",
                "Encourage family presence and participation in care",
                "Provide comfort items from home when appropriate",
                "Support family coping with child's behavioral changes"
            ]
            
            recommendations["reassessment_timing"] = "Every nursing shift and with any significant clinical changes"
            
        else:
            recommendations["immediate_actions"] = [
                "Continue current care plan with delirium prevention focus",
                "Maintain optimal environmental conditions"
            ]
            
            recommendations["ongoing_monitoring"] = [
                "Continue routine CAPD screening every shift",
                "Monitor for risk factors that could precipitate delirium"
            ]
            
            recommendations["prevention_strategies"] = [
                "Maintain normal sleep-wake cycles",
                "Provide age-appropriate stimulation and comfort",
                "Minimize unnecessary procedures and medications",
                "Support family involvement in care"
            ]
            
            recommendations["family_involvement"] = [
                "Continue family-centered care practices",
                "Educate about delirium risk factors and prevention"
            ]
            
            recommendations["reassessment_timing"] = "Every nursing shift as per pediatric protocol"
        
        # Add age-specific recommendations
        age_specific = self._get_age_specific_recommendations(age_group, capd_positive)
        recommendations["age_specific_considerations"] = age_specific
        
        return recommendations
    
    def _get_age_specific_recommendations(self, age_group, capd_positive):
        """Provides age-specific management recommendations"""
        
        group_name = age_group["group"].lower().replace(" ", "_")
        
        age_recommendations = {
            "newborn": [
                "Focus on maintaining stable physiologic parameters",
                "Minimize handling and invasive procedures",
                "Support maternal bonding and skin-to-skin contact when possible"
            ],
            "infant_early": [
                "Maintain consistent feeding and sleep schedules",
                "Provide appropriate sensory stimulation",
                "Support caregiver bonding and attachment"
            ],
            "infant_late": [
                "Encourage developmental activities appropriate for age",
                "Maintain familiar routines and comfort objects",
                "Support social interaction with caregivers"
            ],
            "toddler": [
                "Use simple, concrete language for explanations",
                "Provide choices when possible to maintain sense of control",
                "Use distraction and comfort techniques for procedures"
            ],
            "preschool": [
                "Provide age-appropriate explanations about medical care",
                "Use play therapy and art activities for expression",
                "Maintain school-like routines when possible"
            ],
            "school_age": [
                "Involve child in age-appropriate care decisions",
                "Provide educational activities to maintain cognitive engagement",
                "Support peer contact and social connections"
            ],
            "adolescent": [
                "Respect privacy and independence needs",
                "Involve in care planning and decision-making",
                "Address concerns about body image and peer relationships"
            ]
        }
        
        return age_recommendations.get(group_name, [])
    
    def _get_screening_performance(self, age_group):
        """Provides information about CAPD performance in different age groups"""
        
        group_name = age_group["group"].lower()
        
        if "adolescent" in group_name:
            return {
                "sensitivity": "50%",
                "specificity": "98.1%",
                "note": "Lower sensitivity in adolescents, consider additional assessment tools"
            }
        else:
            return {
                "sensitivity": "94.1%",
                "specificity": "Variable by age group",
                "note": "High sensitivity across pediatric age groups"
            }


def calculate_capd(
    eye_contact: int,
    purposeful_actions: int,
    aware_surroundings: int,
    communicates_needs: int,
    restless: int,
    inconsolable: int,
    underactive: int,
    slow_response: int,
    patient_age: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CapdCalculator()
    return calculator.calculate(
        eye_contact=eye_contact,
        purposeful_actions=purposeful_actions,
        aware_surroundings=aware_surroundings,
        communicates_needs=communicates_needs,
        restless=restless,
        inconsolable=inconsolable,
        underactive=underactive,
        slow_response=slow_response,
        patient_age=patient_age
    )