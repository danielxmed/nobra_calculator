"""
Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal Calculator

Validated assessment tool for evaluating opioid and benzodiazepine withdrawal severity in children.

References:
1. Franck LS, Harris SK, Soetenga DJ, et al. The Withdrawal Assessment Tool-1 
   (WAT-1): an assessment instrument for monitoring opioid and benzodiazepine 
   withdrawal symptoms in pediatric patients. Pediatr Crit Care Med. 
   2008;9(6):573-580. doi: 10.1097/PCC.0b013e31818c8328
2. Anand KJ, Willson DF, Berger J, et al. Tolerance and withdrawal from prolonged 
   opioid use in critically ill children. Pediatrics. 2010;125(5):e1208-e1225. 
   doi: 10.1542/peds.2009-0489
3. Ista E, van Dijk M, Gamel C, et al. Withdrawal symptoms in children after 
   long-term administration of sedatives and/or analgesics: a literature review. 
   Assessment remains troublesome. Intensive Care Med. 2007;33(8):1396-1406. 
   doi: 10.1007/s00134-007-0696-x
"""

from typing import Dict, Any


class Wat1PediatricWithdrawalCalculator:
    """Calculator for WAT-1 Pediatric Withdrawal Assessment"""
    
    def __init__(self):
        # WAT-1 assessment parameters
        self.WAT1_PARAMETERS = [
            "state_sleep_wake_cycle",
            "tremor",
            "increased_muscle_tone", 
            "excoriation",
            "myoclonus_seizures",
            "tachypnea",
            "sweating",
            "fever",
            "frequent_yawning_sneezing",
            "nasal_stuffiness",
            "poor_feeding_vomiting"
        ]
        
        # Parameter descriptions for clinical interpretation
        self.PARAMETER_DESCRIPTIONS = {
            "state_sleep_wake_cycle": "State/sleep-wake cycle disturbance",
            "tremor": "Tremor severity",
            "increased_muscle_tone": "Increased muscle tone/hypertonia",
            "excoriation": "Excoriation marks from scratching",
            "myoclonus_seizures": "Myoclonus/seizure activity",
            "tachypnea": "Tachypnea/respiratory distress",
            "sweating": "Sweating/diaphoresis",
            "fever": "Fever/hyperthermia",
            "frequent_yawning_sneezing": "Frequent yawning/sneezing",
            "nasal_stuffiness": "Nasal stuffiness/rhinorrhea",
            "poor_feeding_vomiting": "Poor feeding/vomiting"
        }
        
        # Score descriptions for each parameter
        self.SCORE_DESCRIPTIONS = {
            "state_sleep_wake_cycle": {
                0: "Normal sleep pattern",
                1: "Mild restlessness",
                2: "Moderate agitation",
                3: "Severe sleep disturbance"
            },
            "tremor": {
                0: "No tremor",
                1: "Mild tremor when stimulated",
                2: "Moderate tremor when awake",
                3: "Severe continuous tremor"
            },
            "increased_muscle_tone": {
                0: "Normal muscle tone",
                1: "Mild increase in tone",
                2: "Moderate increase in tone",
                3: "Severe rigidity"
            },
            "excoriation": {
                0: "No excoriation marks",
                1: "Red marks from scratching",
                2: "Scratches without bleeding",
                3: "Bleeding scratches"
            },
            "myoclonus_seizures": {
                0: "No myoclonus or seizures",
                1: "Occasional jerky movements",
                2: "Frequent jerky movements",
                3: "Continuous movements or seizures"
            },
            "tachypnea": {
                0: "Normal respiratory rate",
                1: "Mildly elevated rate",
                2: "Moderately elevated rate",
                3: "Severely elevated or distressed"
            },
            "sweating": {
                0: "No sweating",
                1: "Mild sweating",
                2: "Moderate sweating",
                3: "Profuse sweating"
            },
            "fever": {
                0: "Temperature <37.2°C",
                1: "Temperature 37.2-37.8°C",
                2: "Temperature 37.9-38.3°C",
                3: "Temperature >38.3°C"
            },
            "frequent_yawning_sneezing": {
                0: "No yawning/sneezing",
                1: "Occasional yawning/sneezing",
                2: "Frequent yawning/sneezing",
                3: "Continuous yawning/sneezing"
            },
            "nasal_stuffiness": {
                0: "No nasal symptoms",
                1: "Mild nasal stuffiness",
                2: "Moderate nasal stuffiness",
                3: "Severe nasal stuffiness"
            },
            "poor_feeding_vomiting": {
                0: "Normal feeding",
                1: "Poor feeding",
                2: "Refusal to feed",
                3: "Vomiting"
            }
        }
        
        # Age-related considerations for scoring
        self.AGE_THRESHOLDS = {
            "preterm": 37,  # weeks post-menstrual age
            "young_infant": 52,  # 3 months corrected
            "older_infant": 104  # 12 months corrected
        }
        
        # Clinical intervention thresholds
        self.INTERVENTION_THRESHOLD_MILD = 3
        self.INTERVENTION_THRESHOLD_MODERATE = 9
        self.MAX_SCORE = 33  # 11 parameters × 3 points each
    
    def calculate(self, post_menstrual_age_weeks: int, state_sleep_wake_cycle: int, tremor: int,
                 increased_muscle_tone: int, excoriation: int, myoclonus_seizures: int,
                 tachypnea: int, sweating: int, fever: int, frequent_yawning_sneezing: int,
                 nasal_stuffiness: int, poor_feeding_vomiting: int) -> Dict[str, Any]:
        """
        Calculates the WAT-1 score for pediatric withdrawal assessment
        
        Args:
            post_menstrual_age_weeks (int): Post-menstrual age in weeks
            state_sleep_wake_cycle (int): Sleep-wake cycle disturbance (0-3)
            tremor (int): Tremor severity (0-3)
            increased_muscle_tone (int): Muscle tone increase (0-3)
            excoriation (int): Excoriation marks (0-3)
            myoclonus_seizures (int): Myoclonus/seizure activity (0-3)
            tachypnea (int): Respiratory distress (0-3)
            sweating (int): Diaphoresis (0-3)
            fever (int): Hyperthermia (0-3)
            frequent_yawning_sneezing (int): Yawning/sneezing frequency (0-3)
            nasal_stuffiness (int): Nasal symptoms (0-3)
            poor_feeding_vomiting (int): Feeding problems (0-3)
            
        Returns:
            Dict with the WAT-1 score and clinical interpretation
        """
        
        # Organize parameters
        parameters = {
            "post_menstrual_age_weeks": post_menstrual_age_weeks,
            "state_sleep_wake_cycle": state_sleep_wake_cycle,
            "tremor": tremor,
            "increased_muscle_tone": increased_muscle_tone,
            "excoriation": excoriation,
            "myoclonus_seizures": myoclonus_seizures,
            "tachypnea": tachypnea,
            "sweating": sweating,
            "fever": fever,
            "frequent_yawning_sneezing": frequent_yawning_sneezing,
            "nasal_stuffiness": nasal_stuffiness,
            "poor_feeding_vomiting": poor_feeding_vomiting
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total WAT-1 score
        total_score = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, post_menstrual_age_weeks)
        
        # Generate detailed assessment
        detailed_assessment = self._generate_detailed_assessment(total_score, post_menstrual_age_weeks, parameters)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"],
            "age_category": detailed_assessment["age_category"],
            "parameter_breakdown": detailed_assessment["parameter_breakdown"],
            "detailed_assessment": detailed_assessment
        }
    
    def _validate_inputs(self, parameters: Dict[str, int]):
        """Validates input parameters"""
        
        # Validate post-menstrual age
        if not isinstance(parameters["post_menstrual_age_weeks"], int):
            raise ValueError("Post-menstrual age must be an integer")
        
        if parameters["post_menstrual_age_weeks"] < 25 or parameters["post_menstrual_age_weeks"] > 200:
            raise ValueError("Post-menstrual age must be between 25 and 200 weeks")
        
        # Validate WAT-1 parameters
        for param in self.WAT1_PARAMETERS:
            if not isinstance(parameters[param], int):
                raise ValueError(f"{param} must be an integer")
            
            if parameters[param] < 0 or parameters[param] > 3:
                raise ValueError(f"{param} must be between 0 and 3")
    
    def _calculate_total_score(self, parameters: Dict[str, int]) -> int:
        """
        Calculates the total WAT-1 score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            
        Returns:
            int: Total WAT-1 score
        """
        
        total_score = 0
        for param in self.WAT1_PARAMETERS:
            total_score += parameters[param]
        
        return total_score
    
    def _get_interpretation(self, score: int, post_menstrual_age_weeks: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on WAT-1 score
        
        Args:
            score (int): Calculated WAT-1 score
            post_menstrual_age_weeks (int): Post-menstrual age
            
        Returns:
            Dict with interpretation details
        """
        
        age_considerations = self._get_age_considerations(post_menstrual_age_weeks)
        
        if score < self.INTERVENTION_THRESHOLD_MILD:
            return {
                "stage": "None to Mild",
                "stage_description": "No withdrawal or mild withdrawal symptoms",
                "interpretation": f"WAT-1 score of {score} indicates no significant withdrawal or very mild "
                               f"withdrawal symptoms. {age_considerations} Continue current management and "
                               f"monitor for symptom progression. Consider comfort measures and supportive care "
                               f"as needed. Reassess every 4-12 hours or as clinically indicated. Environmental "
                               f"modifications and family presence may help maintain comfort."
            }
        elif score < self.INTERVENTION_THRESHOLD_MODERATE:
            return {
                "stage": "Mild to Moderate",
                "stage_description": "Mild to moderate withdrawal symptoms",
                "interpretation": f"WAT-1 score of {score} suggests mild to moderate withdrawal symptoms requiring "
                               f"intervention. {age_considerations} Consider pharmacological management with "
                               f"appropriate medications (methadone, morphine, or clonidine as per protocol). "
                               f"Increase monitoring frequency to every 2-4 hours. Provide comfort measures, "
                               f"environmental modifications, and consider non-pharmacological interventions. "
                               f"Notify attending physician for medication orders."
            }
        else:
            return {
                "stage": "Moderate to Severe",
                "stage_description": "Moderate to severe withdrawal symptoms",
                "interpretation": f"WAT-1 score of {score} indicates moderate to severe withdrawal requiring "
                               f"immediate pharmacological intervention. {age_considerations} Consider urgent "
                               f"treatment with methadone, morphine, or clonidine as appropriate for age and "
                               f"clinical status. Provide intensive monitoring (every 1-2 hours) and comprehensive "
                               f"supportive care. Consider ICU-level monitoring if symptoms are severe. "
                               f"Immediately notify attending physician and consider specialist consultation."
            }
    
    def _get_age_considerations(self, post_menstrual_age_weeks: int) -> str:
        """Returns age-specific considerations for interpretation"""
        
        if post_menstrual_age_weeks < self.AGE_THRESHOLDS["preterm"]:
            return "For preterm infants, consider developmental differences in withdrawal manifestations. "
        elif post_menstrual_age_weeks < self.AGE_THRESHOLDS["young_infant"]:
            return "For young infants, withdrawal may manifest differently than in older children. "
        elif post_menstrual_age_weeks < self.AGE_THRESHOLDS["older_infant"]:
            return "For infants, consider age-appropriate assessment and intervention strategies. "
        else:
            return "For older children, consider developmental stage and communication abilities. "
    
    def _generate_detailed_assessment(self, total_score: int, post_menstrual_age_weeks: int, 
                                    parameters: Dict[str, int]) -> Dict[str, Any]:
        """
        Generates detailed clinical assessment and recommendations
        
        Args:
            total_score (int): Total WAT-1 score
            post_menstrual_age_weeks (int): Post-menstrual age
            parameters (Dict): All input parameters
            
        Returns:
            Dict with detailed assessment
        """
        
        assessment = {
            "age_category": self._categorize_age(post_menstrual_age_weeks),
            "parameter_breakdown": self._analyze_parameter_breakdown(parameters),
            "severity_assessment": self._assess_severity(total_score),
            "intervention_recommendations": self._get_intervention_recommendations(total_score, post_menstrual_age_weeks),
            "monitoring_recommendations": self._get_monitoring_recommendations(total_score),
            "comfort_measures": self._get_comfort_measures(post_menstrual_age_weeks, parameters),
            "medication_considerations": self._get_medication_considerations(total_score, post_menstrual_age_weeks),
            "family_education": self._get_family_education_points(total_score, post_menstrual_age_weeks)
        }
        
        return assessment
    
    def _categorize_age(self, post_menstrual_age_weeks: int) -> Dict[str, Any]:
        """Categorizes patient age for developmental considerations"""
        
        if post_menstrual_age_weeks < self.AGE_THRESHOLDS["preterm"]:
            category = "preterm"
            description = "Preterm infant"
            considerations = "Consider developmental immaturity and different withdrawal manifestations"
        elif post_menstrual_age_weeks < self.AGE_THRESHOLDS["young_infant"]:
            category = "term_infant"
            description = "Term infant"
            considerations = "Standard infant withdrawal assessment applicable"
        elif post_menstrual_age_weeks < self.AGE_THRESHOLDS["older_infant"]:
            category = "young_infant"
            description = "Young infant (3-12 months)"
            considerations = "Consider motor development and behavioral expectations"
        else:
            category = "older_child"
            description = "Older infant/child (>12 months)"
            considerations = "Consider communication abilities and developmental milestones"
        
        return {
            "category": category,
            "description": description,
            "post_menstrual_age": post_menstrual_age_weeks,
            "considerations": considerations
        }
    
    def _analyze_parameter_breakdown(self, parameters: Dict[str, int]) -> Dict[str, Any]:
        """Analyzes individual parameter contributions to overall score"""
        
        breakdown = {}
        high_scoring_parameters = []
        total_possible = len(self.WAT1_PARAMETERS) * 3
        
        for param in self.WAT1_PARAMETERS:
            score = parameters[param]
            breakdown[param] = {
                "score": score,
                "description": self.PARAMETER_DESCRIPTIONS[param],
                "score_description": self.SCORE_DESCRIPTIONS[param][score],
                "severity": "none" if score == 0 else ("mild" if score == 1 else ("moderate" if score == 2 else "severe"))
            }
            
            if score >= 2:
                high_scoring_parameters.append({
                    "parameter": param,
                    "description": self.PARAMETER_DESCRIPTIONS[param],
                    "score": score
                })
        
        return {
            "individual_scores": breakdown,
            "high_scoring_parameters": high_scoring_parameters,
            "total_possible_score": total_possible,
            "percentage_of_maximum": round((sum(parameters[p] for p in self.WAT1_PARAMETERS) / total_possible) * 100, 1)
        }
    
    def _assess_severity(self, score: int) -> Dict[str, Any]:
        """Assesses overall withdrawal severity based on score"""
        
        if score < self.INTERVENTION_THRESHOLD_MILD:
            severity = "minimal"
            urgency = "routine"
            description = "No significant withdrawal symptoms"
        elif score < self.INTERVENTION_THRESHOLD_MODERATE:
            severity = "mild_to_moderate"
            urgency = "prompt"
            description = "Withdrawal symptoms requiring intervention"
        else:
            severity = "moderate_to_severe"
            urgency = "urgent"
            description = "Significant withdrawal requiring immediate attention"
        
        return {
            "severity": severity,
            "urgency": urgency,
            "description": description,
            "score": score,
            "max_possible": self.MAX_SCORE,
            "intervention_threshold": score >= self.INTERVENTION_THRESHOLD_MILD
        }
    
    def _get_intervention_recommendations(self, score: int, post_menstrual_age_weeks: int) -> list:
        """Generates intervention recommendations based on score and age"""
        
        recommendations = []
        
        if score < self.INTERVENTION_THRESHOLD_MILD:
            recommendations.extend([
                "Continue current supportive care",
                "Monitor for symptom progression",
                "Implement comfort measures",
                "Maintain environmental modifications"
            ])
        elif score < self.INTERVENTION_THRESHOLD_MODERATE:
            recommendations.extend([
                "Consider pharmacological intervention",
                "Initiate or adjust withdrawal protocol",
                "Increase monitoring frequency",
                "Enhance comfort measures",
                "Consider dose adjustments of weaning medications"
            ])
        else:
            recommendations.extend([
                "Immediate pharmacological intervention required",
                "Urgent physician notification",
                "Consider ICU-level monitoring",
                "Comprehensive withdrawal protocol implementation",
                "Consider specialist consultation"
            ])
        
        # Age-specific recommendations
        if post_menstrual_age_weeks < self.AGE_THRESHOLDS["preterm"]:
            recommendations.append("Use preterm-specific dosing guidelines")
        elif post_menstrual_age_weeks > 104:  # >2 years
            recommendations.append("Consider age-appropriate behavioral interventions")
        
        return recommendations
    
    def _get_monitoring_recommendations(self, score: int) -> list:
        """Generates monitoring recommendations based on severity"""
        
        if score < self.INTERVENTION_THRESHOLD_MILD:
            return [
                "Assess WAT-1 every 8-12 hours",
                "Monitor vital signs every 4 hours",
                "Document feeding tolerance",
                "Observe for symptom changes"
            ]
        elif score < self.INTERVENTION_THRESHOLD_MODERATE:
            return [
                "Assess WAT-1 every 4-6 hours",
                "Monitor vital signs every 2 hours",
                "Continuous cardiorespiratory monitoring",
                "Frequent neurological assessments",
                "Document medication effectiveness"
            ]
        else:
            return [
                "Assess WAT-1 every 1-2 hours",
                "Continuous vital sign monitoring",
                "Continuous cardiorespiratory monitoring",
                "Frequent neurological assessments",
                "Consider arterial line for blood pressure monitoring",
                "Monitor for seizure activity"
            ]
    
    def _get_comfort_measures(self, post_menstrual_age_weeks: int, parameters: Dict[str, int]) -> list:
        """Generates age-appropriate comfort measures"""
        
        comfort_measures = [
            "Maintain quiet, dimly lit environment",
            "Minimize unnecessary stimulation",
            "Use soft bedding and positioning aids",
            "Encourage family presence and involvement"
        ]
        
        # Age-specific comfort measures
        if post_menstrual_age_weeks < 40:
            comfort_measures.extend([
                "Provide developmental positioning",
                "Use gentle tactile stimulation",
                "Consider pacifier for non-nutritive sucking"
            ])
        elif post_menstrual_age_weeks < 52:
            comfort_measures.extend([
                "Swaddling for comfort",
                "Gentle rocking or rhythmic movement",
                "Soft music or white noise"
            ])
        else:
            comfort_measures.extend([
                "Age-appropriate comfort objects",
                "Structured routine and predictability",
                "Distraction techniques during procedures"
            ])
        
        # Symptom-specific measures
        if parameters["fever"] >= 1:
            comfort_measures.append("Temperature management and cooling measures")
        
        if parameters["poor_feeding_vomiting"] >= 1:
            comfort_measures.append("Small, frequent feeds and feeding modifications")
        
        return comfort_measures
    
    def _get_medication_considerations(self, score: int, post_menstrual_age_weeks: int) -> list:
        """Generates medication-related considerations"""
        
        if score < self.INTERVENTION_THRESHOLD_MILD:
            return [
                "Pharmacological intervention not typically required",
                "Continue current weaning schedule if applicable",
                "Monitor for need to slow weaning process"
            ]
        
        medications = [
            "Consider methadone for opioid withdrawal",
            "Consider clonidine for sympathetic symptoms",
            "Lorazepam may be considered for benzodiazepine withdrawal",
            "Adjust doses based on age and weight"
        ]
        
        # Age-specific considerations
        if post_menstrual_age_weeks < 37:
            medications.extend([
                "Use preterm dosing guidelines",
                "Consider pharmacokinetic differences",
                "Monitor for medication accumulation"
            ])
        
        if score >= self.INTERVENTION_THRESHOLD_MODERATE:
            medications.extend([
                "Consider combination therapy for severe symptoms",
                "Monitor for medication interactions",
                "Frequent reassessment of medication effectiveness"
            ])
        
        return medications
    
    def _get_family_education_points(self, score: int, post_menstrual_age_weeks: int) -> list:
        """Generates family education recommendations"""
        
        education = [
            "Explain withdrawal as expected response to medication weaning",
            "Teach recognition of withdrawal symptoms",
            "Demonstrate comfort measures families can provide",
            "Explain importance of consistent assessment and monitoring"
        ]
        
        if score >= self.INTERVENTION_THRESHOLD_MILD:
            education.extend([
                "Explain medication treatment plan and goals",
                "Discuss timeline for symptom improvement",
                "Teach when to notify healthcare providers",
                "Provide information about withdrawal process"
            ])
        
        # Age-specific education
        if post_menstrual_age_weeks > 104:
            education.extend([
                "Age-appropriate explanation for child",
                "Involve child in comfort measures when possible",
                "Explain behavioral changes child may experience"
            ])
        
        return education


def calculate_wat_1_pediatric_withdrawal(post_menstrual_age_weeks, state_sleep_wake_cycle, tremor,
                                       increased_muscle_tone, excoriation, myoclonus_seizures,
                                       tachypnea, sweating, fever, frequent_yawning_sneezing,
                                       nasal_stuffiness, poor_feeding_vomiting) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_wat_1_pediatric_withdrawal pattern
    """
    calculator = Wat1PediatricWithdrawalCalculator()
    return calculator.calculate(
        post_menstrual_age_weeks, state_sleep_wake_cycle, tremor, increased_muscle_tone,
        excoriation, myoclonus_seizures, tachypnea, sweating, fever,
        frequent_yawning_sneezing, nasal_stuffiness, poor_feeding_vomiting
    )