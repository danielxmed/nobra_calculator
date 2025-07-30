"""
Diabetic Ketoacidosis Mortality Prediction Model (DKA MPM) Score Calculator

Predicts in-hospital mortality in patients with diabetic ketoacidosis using clinical 
and laboratory parameters assessed at presentation, 12 hours, and 24 hours.

References:
- Efstathiou SP, Tsiakou AG, Tsioulos DI, et al. Clin Endocrinol (Oxf). 2002;57(5):595-601.
- Kitabchi AE, Umpierrez GE, Miles JM, Fisher JN. Diabetes Care. 2009;32(7):1335-1343.
"""

from typing import Dict, Any, List


class DkaMpmScoreCalculator:
    """Calculator for DKA MPM Score"""
    
    def __init__(self):
        # Point values for each parameter
        self.SCORING_PARAMETERS = {
            "severe_comorbidities": {"yes": 6, "no": 0},
            "ph_less_than_7": {"yes": 4, "no": 0},
            "insulin_over_50_units": {"yes": 4, "no": 0},
            "glucose_over_300_at_12h": {"yes": 4, "no": 0},
            "depressed_mental_state_24h": {"yes": 4, "no": 0},
            "fever_24h": {"yes": 3, "no": 0}
        }
        
        # Risk interpretation thresholds
        self.RISK_LEVELS = {
            "low_risk": {
                "range": (0, 14),
                "label": "Low Risk",
                "description": "Low risk of in-hospital mortality",
                "mortality_rate": "0.86%",
                "recommendation": "Standard DKA management and monitoring protocols"
            },
            "high_risk": {
                "range": (15, 18),
                "label": "High Risk", 
                "description": "High risk of in-hospital mortality",
                "mortality_rate": "20.8%",
                "recommendation": "Enhanced monitoring and consideration for ICU admission"
            },
            "very_high_risk": {
                "range": (19, 25),
                "label": "Very High Risk",
                "description": "Very high risk of in-hospital mortality",
                "mortality_rate": "93.3%",
                "recommendation": "Immediate ICU admission and aggressive management"
            }
        }
        
        # Clinical recommendations by risk level
        self.CLINICAL_RECOMMENDATIONS = {
            "low_risk": [
                "Standard DKA management protocols",
                "Regular monitoring of vital signs and laboratory values",
                "Routine fluid and electrolyte replacement",
                "Monitor for improvement in acidosis and ketosis",
                "Consider general medical ward admission",
                "Standard frequency laboratory monitoring (q4-6h initially)"
            ],
            "high_risk": [
                "Enhanced monitoring and closer observation",
                "Consider intensive care unit admission",
                "More frequent laboratory monitoring (q2-4h)",
                "Aggressive fluid and electrolyte management",
                "Close monitoring of mental status and hemodynamics",
                "Early involvement of endocrinology consultation",
                "Consider central venous access for monitoring",
                "Vigilant monitoring for complications"
            ],
            "very_high_risk": [
                "Immediate intensive care unit admission required",
                "Aggressive resuscitation and specialized management",
                "Continuous monitoring of vital signs",
                "Frequent laboratory monitoring (q1-2h initially)",
                "Consider invasive hemodynamic monitoring",
                "Multidisciplinary team approach (ICU, endocrinology, nephrology)",
                "Early family discussions regarding prognosis",
                "Consider goals of care discussions",
                "Aggressive treatment of complications",
                "Close monitoring for organ failure"
            ]
        }
        
        # Assessment timing information
        self.ASSESSMENT_TIMING = {
            "presentation": ["severe_comorbidities", "ph_less_than_7"],
            "12_hours": ["insulin_over_50_units", "glucose_over_300_at_12h"],
            "24_hours": ["depressed_mental_state_24h", "fever_24h"]
        }
    
    def calculate(self, severe_comorbidities: str, ph_less_than_7: str, 
                 insulin_over_50_units: str, glucose_over_300_at_12h: str,
                 depressed_mental_state_24h: str, fever_24h: str) -> Dict[str, Any]:
        """
        Calculates the DKA MPM Score
        
        Args:
            severe_comorbidities (str): Presence of severe comorbidities (yes/no)
            ph_less_than_7 (str): pH < 7.0 at presentation (yes/no)
            insulin_over_50_units (str): >50 units insulin in 12h (yes/no)
            glucose_over_300_at_12h (str): Glucose >300 mg/dL at 12h (yes/no)
            depressed_mental_state_24h (str): Depressed mental state at 24h (yes/no)
            fever_24h (str): Fever at 24h (yes/no)
            
        Returns:
            Dict with the calculated score and interpretation
        """
        
        # Collect all parameters
        parameters = {
            "severe_comorbidities": severe_comorbidities,
            "ph_less_than_7": ph_less_than_7,
            "insulin_over_50_units": insulin_over_50_units,
            "glucose_over_300_at_12h": glucose_over_300_at_12h,
            "depressed_mental_state_24h": depressed_mental_state_24h,
            "fever_24h": fever_24h
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score = self._calculate_total_score(parameters)
        
        # Determine risk level
        risk_level = self._determine_risk_level(total_score)
        
        # Get detailed assessment
        detailed_assessment = self._get_detailed_assessment(total_score, risk_level, parameters)
        
        # Get clinical recommendations
        recommendations = self._get_recommendations(risk_level)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, risk_level)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation,
            "stage": self.RISK_LEVELS[risk_level]["label"],
            "stage_description": self.RISK_LEVELS[risk_level]["description"],
            "total_score": total_score,
            "risk_level": risk_level,
            "mortality_rate": self.RISK_LEVELS[risk_level]["mortality_rate"],
            "detailed_assessment": detailed_assessment,
            "recommendations": recommendations,
            "parameter_breakdown": self._get_parameter_breakdown(parameters),
            "timing_assessment": self._get_timing_assessment(parameters),
            "clinical_considerations": self._get_clinical_considerations(risk_level, total_score),
            "monitoring_guidance": self._get_monitoring_guidance(risk_level),
            "prognosis_counseling": self._get_prognosis_counseling(risk_level, total_score)
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"Parameter {param_name} must be a string")
            
            if value.lower() not in ["yes", "no"]:
                raise ValueError(f"Parameter {param_name} must be 'yes' or 'no', got: {value}")
    
    def _calculate_total_score(self, parameters: Dict[str, str]) -> int:
        """Calculates the total DKA MPM score"""
        
        total_score = 0
        
        for param_name, value in parameters.items():
            if param_name in self.SCORING_PARAMETERS:
                points = self.SCORING_PARAMETERS[param_name][value.lower()]
                total_score += points
        
        return total_score
    
    def _determine_risk_level(self, total_score: int) -> str:
        """Determines risk level based on total score"""
        
        for risk_level, info in self.RISK_LEVELS.items():
            min_score, max_score = info["range"]
            if min_score <= total_score <= max_score:
                return risk_level
        
        # Handle edge cases
        if total_score < 0:
            return "low_risk"
        else:
            return "very_high_risk"
    
    def _get_detailed_assessment(self, total_score: int, risk_level: str, parameters: Dict[str, str]) -> Dict[str, Any]:
        """Generate detailed clinical assessment"""
        
        assessment = {
            "total_score": total_score,
            "risk_category": self.RISK_LEVELS[risk_level]["label"],
            "mortality_risk": self.RISK_LEVELS[risk_level]["mortality_rate"],
            "clinical_significance": risk_level != "low_risk",
            "parameter_analysis": {},
            "risk_factors_present": [],
            "timing_breakdown": {},
            "clinical_alerts": []
        }
        
        # Analyze each parameter
        for param_name, value in parameters.items():
            points = self.SCORING_PARAMETERS[param_name][value.lower()]
            assessment["parameter_analysis"][param_name] = {
                "value": value,
                "points": points,
                "significant": points > 0
            }
            
            if points > 0:
                assessment["risk_factors_present"].append({
                    "factor": param_name,
                    "points": points,
                    "description": self._get_parameter_description(param_name)
                })
        
        # Timing breakdown
        for timing, params in self.ASSESSMENT_TIMING.items():
            timing_score = sum(self.SCORING_PARAMETERS[p][parameters[p].lower()] for p in params)
            assessment["timing_breakdown"][timing] = {
                "score": timing_score,
                "parameters": params,
                "significance": self._assess_timing_significance(timing, timing_score)
            }
        
        # Clinical alerts
        assessment["clinical_alerts"] = self._generate_clinical_alerts(risk_level, parameters)
        
        return assessment
    
    def _get_parameter_description(self, param_name: str) -> str:
        """Get description for parameter"""
        
        descriptions = {
            "severe_comorbidities": "Severe comorbidities (immunosuppression, MI, COPD, cirrhosis, CHF, stroke)",
            "ph_less_than_7": "Severe acidosis (pH < 7.0)",
            "insulin_over_50_units": "High insulin requirement (>50 units in 12h)",
            "glucose_over_300_at_12h": "Persistent hyperglycemia (>300 mg/dL at 12h)",
            "depressed_mental_state_24h": "Altered mental status at 24h",
            "fever_24h": "Fever at 24h (≥38°C/100.4°F)"
        }
        
        return descriptions.get(param_name, param_name)
    
    def _assess_timing_significance(self, timing: str, score: int) -> str:
        """Assess significance of timing-specific score"""
        
        if timing == "presentation":
            if score >= 6:
                return "High early risk - immediate intensive monitoring required"
            elif score >= 4:
                return "Moderate early risk - enhanced monitoring recommended"
            else:
                return "Low early risk"
        elif timing == "12_hours":
            if score >= 6:
                return "Poor early response - treatment intensification needed"
            elif score >= 4:
                return "Suboptimal early response - close monitoring"
            else:
                return "Good early response"
        elif timing == "24_hours":
            if score >= 4:
                return "Concerning late complications - aggressive intervention"
            elif score >= 3:
                return "Late complications present - enhanced monitoring"
            else:
                return "No late complications"
        
        return "Unknown significance"
    
    def _generate_clinical_alerts(self, risk_level: str, parameters: Dict[str, str]) -> List[str]:
        """Generate clinical alerts based on parameters"""
        
        alerts = []
        
        if parameters["severe_comorbidities"].lower() == "yes":
            alerts.append("Multiple comorbidities present - consider multidisciplinary approach")
        
        if parameters["ph_less_than_7"].lower() == "yes":
            alerts.append("Severe acidosis - aggressive bicarbonate consideration and ICU care")
        
        if parameters["insulin_over_50_units"].lower() == "yes":
            alerts.append("High insulin resistance - review insulin protocol and glucose management")
        
        if parameters["glucose_over_300_at_12h"].lower() == "yes":
            alerts.append("Persistent hyperglycemia - reassess insulin therapy effectiveness")
        
        if parameters["depressed_mental_state_24h"].lower() == "yes":
            alerts.append("Altered mental status at 24h - evaluate for complications or cerebral edema")
        
        if parameters["fever_24h"].lower() == "yes":
            alerts.append("Fever at 24h - investigate for infectious complications")
        
        if risk_level == "very_high_risk":
            alerts.append("CRITICAL: Very high mortality risk - immediate ICU care and family discussions")
        elif risk_level == "high_risk":
            alerts.append("HIGH RISK: Consider ICU admission and enhanced monitoring")
        
        return alerts
    
    def _get_recommendations(self, risk_level: str) -> Dict[str, List[str]]:
        """Get clinical recommendations"""
        
        return {
            "immediate_actions": self.CLINICAL_RECOMMENDATIONS[risk_level].copy(),
            "monitoring": self._get_monitoring_recommendations(risk_level),
            "treatment": self._get_treatment_recommendations(risk_level)
        }
    
    def _get_monitoring_recommendations(self, risk_level: str) -> List[str]:
        """Get monitoring recommendations"""
        
        if risk_level == "low_risk":
            return [
                "Vital signs every 4-6 hours",
                "Laboratory monitoring every 4-6 hours initially",
                "Blood glucose monitoring every 2-4 hours",
                "Neurological checks every 4-6 hours",
                "Fluid balance monitoring"
            ]
        elif risk_level == "high_risk":
            return [
                "Vital signs every 2-4 hours",
                "Laboratory monitoring every 2-4 hours",
                "Blood glucose monitoring every 1-2 hours",
                "Neurological checks every 2 hours",
                "Strict fluid balance monitoring",
                "Consider continuous cardiac monitoring"
            ]
        else:  # very_high_risk
            return [
                "Continuous vital sign monitoring",
                "Laboratory monitoring every 1-2 hours",
                "Blood glucose monitoring every hour",
                "Continuous neurological monitoring",
                "Strict fluid balance with hourly assessment",
                "Continuous cardiac monitoring",
                "Consider invasive hemodynamic monitoring"
            ]
    
    def _get_treatment_recommendations(self, risk_level: str) -> List[str]:
        """Get treatment recommendations"""
        
        if risk_level == "low_risk":
            return [
                "Standard DKA insulin protocol",
                "Standard fluid replacement protocol",
                "Electrolyte replacement as needed",
                "Monitor for improvement in acidosis"
            ]
        elif risk_level == "high_risk":
            return [
                "Intensive insulin protocol with frequent adjustments",
                "Aggressive fluid resuscitation with close monitoring",
                "Proactive electrolyte replacement",
                "Consider bicarbonate if pH < 7.0",
                "Early endocrinology consultation"
            ]
        else:  # very_high_risk
            return [
                "Aggressive insulin protocol with continuous monitoring",
                "Rapid fluid resuscitation with hemodynamic monitoring",
                "Aggressive electrolyte replacement",
                "Consider bicarbonate therapy for severe acidosis",
                "Immediate endocrinology consultation",
                "Consider dialysis for severe complications",
                "Multidisciplinary intensive care approach"
            ]
    
    def _get_timing_assessment(self, parameters: Dict[str, str]) -> Dict[str, Any]:
        """Get assessment of timing-specific parameters"""
        
        timing_assessment = {}
        
        for timing, params in self.ASSESSMENT_TIMING.items():
            timing_score = sum(self.SCORING_PARAMETERS[p][parameters[p].lower()] for p in params)
            timing_assessment[timing] = {
                "score": timing_score,
                "assessment": self._assess_timing_significance(timing, timing_score),
                "parameters": {p: {"value": parameters[p], "points": self.SCORING_PARAMETERS[p][parameters[p].lower()]} for p in params}
            }
        
        return timing_assessment
    
    def _get_parameter_breakdown(self, parameters: Dict[str, str]) -> Dict[str, Any]:
        """Get detailed breakdown of each parameter"""
        
        breakdown = {}
        
        for param_name, value in parameters.items():
            points = self.SCORING_PARAMETERS[param_name][value.lower()]
            breakdown[param_name] = {
                "value": value,
                "points": points,
                "description": self._get_parameter_description(param_name),
                "significant": points > 0,
                "timing": self._get_parameter_timing(param_name)
            }
        
        return breakdown
    
    def _get_parameter_timing(self, param_name: str) -> str:
        """Get timing for parameter assessment"""
        
        for timing, params in self.ASSESSMENT_TIMING.items():
            if param_name in params:
                return timing
        return "unknown"
    
    def _get_clinical_considerations(self, risk_level: str, total_score: int) -> Dict[str, Any]:
        """Get clinical considerations"""
        
        return {
            "admission_recommendation": self._get_admission_recommendation(risk_level),
            "monitoring_intensity": self._get_monitoring_intensity(risk_level),
            "family_communication": self._get_family_communication_guidance(risk_level),
            "quality_improvement": self._get_quality_improvement_considerations(risk_level),
            "limitations": [
                "Score not externally validated - use clinical judgment",
                "APACHE II may be superior mortality predictor",
                "Not intended as sole basis for clinical decisions",
                "Requires assessment at multiple time points"
            ]
        }
    
    def _get_admission_recommendation(self, risk_level: str) -> str:
        """Get admission recommendation"""
        
        recommendations = {
            "low_risk": "General medical ward admission typically appropriate",
            "high_risk": "Consider ICU admission or step-down unit with enhanced monitoring",
            "very_high_risk": "Immediate ICU admission required"
        }
        
        return recommendations[risk_level]
    
    def _get_monitoring_intensity(self, risk_level: str) -> str:
        """Get monitoring intensity recommendation"""
        
        intensities = {
            "low_risk": "Standard monitoring protocols",
            "high_risk": "Enhanced monitoring with increased frequency",
            "very_high_risk": "Intensive monitoring with continuous assessment"
        }
        
        return intensities[risk_level]
    
    def _get_family_communication_guidance(self, risk_level: str) -> str:
        """Get family communication guidance"""
        
        guidance = {
            "low_risk": "Reassure family about good prognosis with standard treatment",
            "high_risk": "Discuss elevated risk and need for enhanced monitoring",
            "very_high_risk": "Early honest discussion about high mortality risk and goals of care"
        }
        
        return guidance[risk_level]
    
    def _get_quality_improvement_considerations(self, risk_level: str) -> List[str]:
        """Get quality improvement considerations"""
        
        if risk_level == "very_high_risk":
            return [
                "Review DKA protocols for very high-risk patients",
                "Ensure rapid ICU access and specialist consultation",
                "Consider morbidity and mortality review if poor outcome",
                "Evaluate early recognition and intervention protocols"
            ]
        elif risk_level == "high_risk":
            return [
                "Review monitoring protocols for high-risk patients",
                "Ensure appropriate escalation pathways",
                "Consider enhanced nursing ratios"
            ]
        else:
            return [
                "Standard quality metrics monitoring",
                "Routine outcome tracking"
            ]
    
    def _get_monitoring_guidance(self, risk_level: str) -> Dict[str, Any]:
        """Get detailed monitoring guidance"""
        
        return {
            "frequency": self._get_monitoring_frequency(risk_level),
            "parameters": self._get_monitoring_parameters(risk_level),
            "escalation_criteria": self._get_escalation_criteria(risk_level),
            "duration": self._get_monitoring_duration(risk_level)
        }
    
    def _get_monitoring_frequency(self, risk_level: str) -> Dict[str, str]:
        """Get monitoring frequency by risk level"""
        
        frequencies = {
            "low_risk": {
                "vital_signs": "Every 4-6 hours",
                "laboratory": "Every 4-6 hours initially",
                "glucose": "Every 2-4 hours",
                "neurological": "Every 4-6 hours"
            },
            "high_risk": {
                "vital_signs": "Every 2-4 hours", 
                "laboratory": "Every 2-4 hours",
                "glucose": "Every 1-2 hours",
                "neurological": "Every 2 hours"
            },
            "very_high_risk": {
                "vital_signs": "Continuous monitoring",
                "laboratory": "Every 1-2 hours",
                "glucose": "Every hour",
                "neurological": "Continuous assessment"
            }
        }
        
        return frequencies[risk_level]
    
    def _get_monitoring_parameters(self, risk_level: str) -> List[str]:
        """Get monitoring parameters by risk level"""
        
        base_params = [
            "Blood glucose",
            "Serum electrolytes (Na, K, Cl, CO2)",
            "Arterial blood gas",
            "Serum ketones or urine ketones",
            "Vital signs (BP, HR, RR, temp)",
            "Mental status",
            "Fluid balance"
        ]
        
        if risk_level in ["high_risk", "very_high_risk"]:
            base_params.extend([
                "Serum lactate",
                "Cardiac monitoring",
                "Urine output hourly"
            ])
        
        if risk_level == "very_high_risk":
            base_params.extend([
                "Central venous pressure (if indicated)",
                "Arterial line monitoring (if indicated)",
                "Continuous neurological monitoring"
            ])
        
        return base_params
    
    def _get_escalation_criteria(self, risk_level: str) -> List[str]:
        """Get escalation criteria"""
        
        criteria = [
            "Worsening mental status",
            "Hemodynamic instability",
            "Worsening acidosis despite treatment",
            "Persistent severe hyperglycemia",
            "Development of complications"
        ]
        
        if risk_level == "low_risk":
            criteria.append("Any parameter suggesting higher risk category")
        
        return criteria
    
    def _get_monitoring_duration(self, risk_level: str) -> str:
        """Get monitoring duration recommendation"""
        
        durations = {
            "low_risk": "Until acidosis resolves and patient stable for 12-24 hours",
            "high_risk": "Until acidosis resolves and patient stable for 24-48 hours",
            "very_high_risk": "Extended monitoring until patient stable for 48-72 hours"
        }
        
        return durations[risk_level]
    
    def _get_prognosis_counseling(self, risk_level: str, total_score: int) -> Dict[str, Any]:
        """Get prognosis counseling guidance"""
        
        return {
            "mortality_discussion": self._get_mortality_discussion(risk_level),
            "prognostic_factors": self._get_prognostic_factors(risk_level),
            "goals_of_care": self._get_goals_of_care_discussion(risk_level),
            "family_preparation": self._get_family_preparation_guidance(risk_level)
        }
    
    def _get_mortality_discussion(self, risk_level: str) -> str:
        """Get mortality discussion guidance"""
        
        discussions = {
            "low_risk": "Excellent prognosis with appropriate treatment (>99% survival expected)",
            "high_risk": "Good prognosis but elevated risk (approximately 20% mortality risk)",
            "very_high_risk": "Guarded prognosis with very high mortality risk (>90% mortality risk)"
        }
        
        return discussions[risk_level]
    
    def _get_prognostic_factors(self, risk_level: str) -> List[str]:
        """Get prognostic factors to discuss"""
        
        if risk_level == "very_high_risk":
            return [
                "Presence of multiple comorbidities",
                "Severe acidosis at presentation",
                "Poor response to initial treatment",
                "Development of complications",
                "Need for intensive care support"
            ]
        elif risk_level == "high_risk":
            return [
                "Elevated risk factors present",
                "Need for enhanced monitoring",
                "Response to treatment will guide prognosis"
            ]
        else:
            return [
                "Favorable prognostic profile",
                "Expected good response to treatment"
            ]
    
    def _get_goals_of_care_discussion(self, risk_level: str) -> str:
        """Get goals of care discussion guidance"""
        
        discussions = {
            "low_risk": "Focus on recovery and diabetes management education",
            "high_risk": "Discuss treatment intensity and monitoring needs",
            "very_high_risk": "Early discussion about goals of care, comfort measures, and family wishes"
        }
        
        return discussions[risk_level]
    
    def _get_family_preparation_guidance(self, risk_level: str) -> str:
        """Get family preparation guidance"""
        
        guidance = {
            "low_risk": "Prepare family for standard recovery course",
            "high_risk": "Prepare family for potential complications and need for intensive monitoring",
            "very_high_risk": "Prepare family for serious illness, potential complications, and possible poor outcome"
        }
        
        return guidance[risk_level]
    
    def _get_interpretation(self, total_score: int, risk_level: str) -> str:
        """Get comprehensive interpretation"""
        
        risk_info = self.RISK_LEVELS[risk_level]
        
        base_interpretation = (f"DKA MPM Score of {total_score} points indicates {risk_info['label']} "
                             f"with {risk_info['mortality_rate']} in-hospital mortality risk. "
                             f"{risk_info['description']}.")
        
        # Add specific recommendations
        if risk_level == "very_high_risk":
            base_interpretation += (" Immediate ICU admission and aggressive management required. "
                                  "Early family discussions about prognosis are recommended.")
        elif risk_level == "high_risk":
            base_interpretation += (" Enhanced monitoring and consideration for ICU admission recommended. "
                                  "Close observation for complications is essential.")
        else:
            base_interpretation += (" Standard DKA management protocols are appropriate. "
                                  "Routine monitoring and care expected to be sufficient.")
        
        return base_interpretation


def calculate_dka_mpm_score(severe_comorbidities: str, ph_less_than_7: str,
                           insulin_over_50_units: str, glucose_over_300_at_12h: str,
                           depressed_mental_state_24h: str, fever_24h: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DkaMpmScoreCalculator()
    return calculator.calculate(
        severe_comorbidities, ph_less_than_7, insulin_over_50_units,
        glucose_over_300_at_12h, depressed_mental_state_24h, fever_24h
    )