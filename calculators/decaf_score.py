"""
DECAF Score for Acute Exacerbation of COPD Calculator

Predicts in-hospital mortality in acute COPD exacerbation using five key clinical 
variables: Dyspnoea (extended MRC), Eosinopenia, Consolidation, Acidaemia, and 
atrial Fibrillation.

References:
- Steer J, et al. Thorax. 2012;67(11):970-976.
- Echevarria C, et al. Thorax. 2016;71(2):133-140.
- Zhou M, et al. BMJ Open. 2021;11(2):e044923.
"""

from typing import Dict, Any, Optional


class DecafScoreCalculator:
    """Calculator for DECAF Score for Acute Exacerbation of COPD"""
    
    def __init__(self):
        # DECAF score components and weights
        self.SCORE_COMPONENTS = {
            "dyspnea": {
                "not_too_dyspneic": 0,
                "too_dyspneic_independent": 1,
                "too_dyspneic_dependent": 2
            },
            "eosinopenia": {"yes": 1, "no": 0},
            "consolidation": {"yes": 1, "no": 0},
            "acidemia": {"yes": 1, "no": 0},
            "atrial_fibrillation": {"yes": 1, "no": 0}
        }
        
        # Risk categories and mortality data
        self.RISK_CATEGORIES = {
            "low": {
                "score_range": (0, 1),
                "label": "Low Risk",
                "description": "Low mortality risk",
                "mortality_range": "0-1.5%",
                "mortality_specific": {0: "0%", 1: "1.5%"},
                "recommendation": "Routine management",
                "disposition": "Standard ward care",
                "monitoring": "Routine monitoring"
            },
            "intermediate": {
                "score_range": (2, 2),
                "label": "Intermediate Risk", 
                "description": "Intermediate mortality risk",
                "mortality_range": "5.4%",
                "mortality_specific": {2: "5.4%"},
                "recommendation": "Use clinician judgment re: disposition",
                "disposition": "Consider higher level care",
                "monitoring": "Close monitoring"
            },
            "high": {
                "score_range": (3, 6),
                "label": "High Risk",
                "description": "High mortality risk",
                "mortality_range": "15.3-50%",
                "mortality_specific": {3: "15.3%", 4: "31%", 5: "40%", 6: "50%"},
                "recommendation": "Consider escalation of care vs. palliative care",
                "disposition": "HDU/ICU consideration",
                "monitoring": "Intensive monitoring"
            }
        }
        
        # Management recommendations by risk level
        self.MANAGEMENT_RECOMMENDATIONS = {
            "low": [
                "Standard ward-based care is appropriate",
                "Routine COPD exacerbation management protocol",
                "Standard bronchodilator and corticosteroid therapy",
                "Regular monitoring for clinical improvement",
                "Discharge planning and outpatient follow-up arrangement"
            ],
            "intermediate": [
                "Close clinical monitoring and frequent reassessment",
                "Consider higher level of nursing care or step-down unit",
                "Aggressive bronchodilator and anti-inflammatory therapy", 
                "Early assessment for respiratory failure and need for ventilation",
                "Consider early mobilization and respiratory therapy"
            ],
            "high": [
                "Strong consideration for HDU/ICU level care",
                "Intensive monitoring for respiratory failure",
                "Early assessment for non-invasive or invasive ventilation",
                "Aggressive medical management with close monitoring",
                "Palliative care consultation for goals of care discussion",
                "Consider early family meetings and advance directive discussions"
            ]
        }
    
    def calculate(self, emrcd_dyspnea: str, eosinopenia: str, consolidation: str,
                  acidemia: str, atrial_fibrillation: str, 
                  patient_age: Optional[int] = None, 
                  smoking_history: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates DECAF score for acute COPD exacerbation mortality prediction
        
        Args:
            emrcd_dyspnea (str): Extended MRC Dyspnea Scale assessment
            eosinopenia (str): Presence of eosinopenia (<0.05×10⁹/L)
            consolidation (str): Consolidation on chest X-ray
            acidemia (str): Arterial blood gas pH <7.30
            atrial_fibrillation (str): Atrial fibrillation on ECG or history
            patient_age (int, optional): Patient age for clinical context
            smoking_history (str, optional): Smoking history for validity check
            
        Returns:
            Dict with DECAF score, risk assessment, and management recommendations
        """
        
        # Validations
        self._validate_inputs(emrcd_dyspnea, eosinopenia, consolidation, 
                            acidemia, atrial_fibrillation, patient_age, smoking_history)
        
        # Calculate DECAF score
        decaf_score = self._calculate_decaf_score(emrcd_dyspnea, eosinopenia, 
                                                consolidation, acidemia, atrial_fibrillation)
        
        # Determine risk category
        risk_category = self._determine_risk_category(decaf_score)
        
        # Get risk details
        risk_details = self.RISK_CATEGORIES[risk_category]
        
        # Generate clinical assessment
        clinical_assessment = self._get_clinical_assessment(
            emrcd_dyspnea, eosinopenia, consolidation, acidemia, atrial_fibrillation,
            decaf_score, risk_category, patient_age, smoking_history)
        
        # Get management recommendations
        management_recommendations = self._get_management_recommendations(
            risk_category, decaf_score, patient_age)
        
        # Generate interpretation
        interpretation = self._get_interpretation(risk_category, decaf_score, risk_details)
        
        # Get mortality risk details
        mortality_details = self._get_mortality_details(decaf_score, risk_category)
        
        return {
            "result": decaf_score,
            "unit": "DECAF score",
            "interpretation": interpretation,
            "stage": risk_details["label"],
            "stage_description": risk_details["description"],
            "decaf_score": decaf_score,
            "risk_category": risk_category,
            "mortality_risk": mortality_details["risk"],
            "mortality_range": risk_details["mortality_range"],
            "recommendation": risk_details["recommendation"],
            "disposition": risk_details["disposition"],
            "monitoring_level": risk_details["monitoring"],
            "clinical_assessment": clinical_assessment,
            "management_recommendations": management_recommendations,
            "mortality_details": mortality_details,
            "score_components": self._get_score_breakdown(
                emrcd_dyspnea, eosinopenia, consolidation, acidemia, atrial_fibrillation),
            "clinical_guidance": self._get_clinical_guidance(risk_category, decaf_score),
            "follow_up_recommendations": self._get_follow_up_recommendations(risk_category)
        }
    
    def _validate_inputs(self, emrcd_dyspnea, eosinopenia, consolidation, 
                        acidemia, atrial_fibrillation, patient_age, smoking_history):
        """Validates input parameters"""
        
        # Validate dyspnea scale
        valid_dyspnea = ["not_too_dyspneic", "too_dyspneic_independent", "too_dyspneic_dependent"]
        if emrcd_dyspnea not in valid_dyspnea:
            raise ValueError(f"emrcd_dyspnea must be one of: {valid_dyspnea}")
        
        # Validate binary parameters
        binary_params = [eosinopenia, consolidation, acidemia, atrial_fibrillation]
        param_names = ["eosinopenia", "consolidation", "acidemia", "atrial_fibrillation"]
        
        for param, name in zip(binary_params, param_names):
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
        
        # Validate optional parameters
        if patient_age is not None:
            if not isinstance(patient_age, int) or not 35 <= patient_age <= 120:
                raise ValueError("Patient age must be an integer between 35 and 120 years")
        
        if smoking_history is not None:
            if smoking_history not in ["yes", "no", "unknown"]:
                raise ValueError("smoking_history must be 'yes', 'no', or 'unknown'")
    
    def _calculate_decaf_score(self, emrcd_dyspnea, eosinopenia, consolidation, 
                              acidemia, atrial_fibrillation):
        """Calculates the DECAF score using component weights"""
        
        score = 0
        
        # Dyspnea component (0-2 points)
        score += self.SCORE_COMPONENTS["dyspnea"][emrcd_dyspnea]
        
        # Binary components (0-1 point each)
        score += self.SCORE_COMPONENTS["eosinopenia"][eosinopenia]
        score += self.SCORE_COMPONENTS["consolidation"][consolidation]
        score += self.SCORE_COMPONENTS["acidemia"][acidemia]
        score += self.SCORE_COMPONENTS["atrial_fibrillation"][atrial_fibrillation]
        
        return score
    
    def _determine_risk_category(self, decaf_score):
        """Determines risk category based on DECAF score"""
        
        for category, details in self.RISK_CATEGORIES.items():
            score_min, score_max = details["score_range"]
            if score_min <= decaf_score <= score_max:
                return category
        
        # Handle edge case (should not occur with valid inputs)
        return "low" if decaf_score < 0 else "high"
    
    def _get_clinical_assessment(self, emrcd_dyspnea, eosinopenia, consolidation,
                                acidemia, atrial_fibrillation, decaf_score, risk_category,
                                patient_age, smoking_history):
        """Generate clinical assessment based on parameters"""
        
        assessment = {
            "decaf_score": decaf_score,
            "risk_category": risk_category,
            "score_components": [],
            "clinical_factors": [],
            "validity_criteria": [],
            "additional_considerations": []
        }
        
        # Document score components
        dyspnea_descriptions = {
            "not_too_dyspneic": "Not too dyspneic to leave house (0 points)",
            "too_dyspneic_independent": "Too dyspneic to leave house but independent with washing/dressing (1 point)",
            "too_dyspneic_dependent": "Too dyspneic to leave house and wash/dress (2 points)"
        }
        assessment["score_components"].append(dyspnea_descriptions[emrcd_dyspnea])
        
        assessment["score_components"].append(f"Eosinopenia (<0.05×10⁹/L): {eosinopenia} ({1 if eosinopenia == 'yes' else 0} point)")
        assessment["score_components"].append(f"Consolidation on chest X-ray: {consolidation} ({1 if consolidation == 'yes' else 0} point)")
        assessment["score_components"].append(f"Acidemia (pH <7.30): {acidemia} ({1 if acidemia == 'yes' else 0} point)")
        assessment["score_components"].append(f"Atrial fibrillation: {atrial_fibrillation} ({1 if atrial_fibrillation == 'yes' else 0} point)")
        
        # Clinical factors
        assessment["clinical_factors"] = [
            f"Acute COPD exacerbation requiring hospitalization",
            f"DECAF score of {decaf_score} indicates {risk_category} risk for in-hospital mortality",
            f"Risk-appropriate management and monitoring recommended"
        ]
        
        # Validity criteria
        if patient_age is not None:
            if patient_age >= 35:
                assessment["validity_criteria"].append(f"Age ≥35 years (age {patient_age}) - score validity met")
            else:
                assessment["validity_criteria"].append(f"Age <35 years (age {patient_age}) - score not validated for this age group")
        
        if smoking_history is not None:
            if smoking_history == "yes":
                assessment["validity_criteria"].append("≥10 pack-year smoking history assumed - score validity supported")
            elif smoking_history == "no":
                assessment["validity_criteria"].append("No significant smoking history - score validity may be limited")
            else:
                assessment["validity_criteria"].append("Smoking history unknown - consider verification for score validity")
        
        # Additional considerations
        if consolidation == "yes":
            assessment["additional_considerations"].append("Presence of consolidation suggests pneumonic process requiring antimicrobial therapy")
        
        if acidemia == "yes":
            assessment["additional_considerations"].append("Acidemia indicates respiratory failure - consider ventilatory support")
        
        if atrial_fibrillation == "yes":
            assessment["additional_considerations"].append("Atrial fibrillation may require rate control and anticoagulation consideration")
        
        if eosinopenia == "yes":
            assessment["additional_considerations"].append("Eosinopenia may indicate systemic inflammation and poor prognosis")
        
        return assessment
    
    def _get_management_recommendations(self, risk_category, decaf_score, patient_age):
        """Get management recommendations based on risk assessment"""
        
        base_recommendations = self.MANAGEMENT_RECOMMENDATIONS[risk_category].copy()
        specific_recommendations = []
        
        # Age-specific considerations
        if patient_age is not None:
            if patient_age >= 75:
                specific_recommendations.append("Advanced age requires careful assessment of goals of care and functional status")
            if patient_age >= 80 and risk_category == "high":
                specific_recommendations.append("Consider early palliative care consultation for comprehensive care planning")
        
        # Score-specific considerations
        if decaf_score >= 4:
            specific_recommendations.append("DECAF score ≥4 indicates very high mortality risk - consider immediate escalation")
        
        if decaf_score == 6:
            specific_recommendations.append("Maximum DECAF score - urgent consideration for intensive care or comfort measures")
        
        return {
            "primary_recommendations": base_recommendations,
            "specific_considerations": specific_recommendations,
            "monitoring_requirements": self._get_monitoring_requirements(risk_category),
            "escalation_criteria": self._get_escalation_criteria(risk_category)
        }
    
    def _get_monitoring_requirements(self, risk_category):
        """Get monitoring requirements based on risk category"""
        
        if risk_category == "low":
            return [
                "Standard nursing observations every 4-6 hours",
                "Daily chest X-ray if indicated",
                "Monitor response to bronchodilator therapy",
                "Assess for clinical improvement and discharge readiness"
            ]
        elif risk_category == "intermediate":
            return [
                "Enhanced nursing observations every 2-4 hours",
                "Frequent assessment of respiratory status",
                "Consider arterial blood gas monitoring",
                "Monitor for signs of respiratory failure",
                "Regular reassessment of DECAF components"
            ]
        else:  # high risk
            return [
                "Intensive monitoring with continuous assessment",
                "Frequent arterial blood gas monitoring",
                "Cardiac monitoring for arrhythmias",
                "Hourly respiratory assessment",
                "Consider HDU/ICU level monitoring",
                "Multidisciplinary team involvement"
            ]
    
    def _get_escalation_criteria(self, risk_category):
        """Get escalation criteria based on risk category"""
        
        return {
            "respiratory": [
                "Worsening dyspnea or respiratory distress",
                "Deteriorating arterial blood gases",
                "Need for non-invasive or invasive ventilation",
                "Respiratory rate >30 or <8 breaths per minute"
            ],
            "cardiovascular": [
                "Hemodynamic instability",
                "New or worsening arrhythmias",
                "Signs of right heart failure",
                "Hypotension requiring vasopressor support"
            ],
            "general": [
                "Altered mental status or confusion",
                "Failure to respond to standard therapy",
                "Development of complications",
                "Patient or family request for escalation"
            ]
        }
    
    def _get_mortality_details(self, decaf_score, risk_category):
        """Get specific mortality risk details"""
        
        risk_details = self.RISK_CATEGORIES[risk_category]
        
        if decaf_score in risk_details["mortality_specific"]:
            specific_risk = risk_details["mortality_specific"][decaf_score]
        else:
            specific_risk = risk_details["mortality_range"]
        
        return {
            "risk": specific_risk,
            "confidence": "High" if risk_category != "intermediate" else "Moderate",
            "basis": "Derived from prospective cohort studies with external validation",
            "time_frame": "In-hospital mortality risk",
            "comparison": self._get_risk_comparison(decaf_score)
        }
    
    def _get_risk_comparison(self, decaf_score):
        """Get risk comparison information"""
        
        if decaf_score <= 1:
            return "Very low risk - similar to general medical ward patients"
        elif decaf_score == 2:
            return "Moderate risk - 5-10 times higher than low-risk patients"
        elif decaf_score == 3:
            return "High risk - 10-15 times higher than low-risk patients"
        else:
            return "Very high risk - >20 times higher than low-risk patients"
    
    def _get_clinical_guidance(self, risk_category, decaf_score):
        """Get clinical guidance based on assessment"""
        
        guidance = {
            "disposition": "",
            "priority": "",
            "family_communication": "",
            "prognosis_discussion": ""
        }
        
        if risk_category == "low":
            guidance["disposition"] = "Standard ward care appropriate"
            guidance["priority"] = "Routine priority for medical management"
            guidance["family_communication"] = "Reassuring prognosis with standard care"
            guidance["prognosis_discussion"] = "Excellent prognosis with appropriate treatment"
        
        elif risk_category == "intermediate":
            guidance["disposition"] = "Consider higher level care or close monitoring"
            guidance["priority"] = "Moderate priority requiring frequent assessment"
            guidance["family_communication"] = "Guarded prognosis requiring close monitoring"
            guidance["prognosis_discussion"] = "Moderate risk requiring individualized care planning"
        
        else:  # high risk
            guidance["disposition"] = "Strong consideration for HDU/ICU care"
            guidance["priority"] = "High priority requiring immediate attention"
            guidance["family_communication"] = "Serious condition requiring family meeting"
            guidance["prognosis_discussion"] = "High mortality risk warranting goals of care discussion"
        
        return guidance
    
    def _get_follow_up_recommendations(self, risk_category):
        """Get follow-up recommendations based on risk category"""
        
        if risk_category == "low":
            return {
                "inpatient": "Daily assessment until discharge readiness",
                "discharge": "Standard COPD action plan and outpatient follow-up",
                "outpatient": "Pulmonology follow-up within 2-4 weeks"
            }
        elif risk_category == "intermediate":
            return {
                "inpatient": "Twice daily specialist review",
                "discharge": "Enhanced discharge planning with home monitoring",
                "outpatient": "Early pulmonology follow-up within 1-2 weeks"
            }
        else:  # high risk
            return {
                "inpatient": "Daily multidisciplinary team review",
                "discharge": "Comprehensive discharge planning with community support",
                "outpatient": "Urgent pulmonology follow-up within 1 week"
            }
    
    def _get_score_breakdown(self, emrcd_dyspnea, eosinopenia, consolidation, 
                           acidemia, atrial_fibrillation):
        """Get detailed breakdown of score components"""
        
        components = []
        
        dyspnea_points = self.SCORE_COMPONENTS["dyspnea"][emrcd_dyspnea]
        components.append({
            "component": "Extended MRC Dyspnea",
            "value": emrcd_dyspnea,
            "points": dyspnea_points,
            "description": f"Functional limitation due to dyspnea"
        })
        
        eosinopenia_points = self.SCORE_COMPONENTS["eosinopenia"][eosinopenia]
        components.append({
            "component": "Eosinopenia",
            "value": eosinopenia,
            "points": eosinopenia_points,
            "description": f"Eosinophils <0.05×10⁹/L"
        })
        
        consolidation_points = self.SCORE_COMPONENTS["consolidation"][consolidation]
        components.append({
            "component": "Consolidation",
            "value": consolidation,
            "points": consolidation_points,
            "description": f"Consolidation on chest X-ray"
        })
        
        acidemia_points = self.SCORE_COMPONENTS["acidemia"][acidemia]
        components.append({
            "component": "Acidemia",
            "value": acidemia,
            "points": acidemia_points,
            "description": f"Arterial pH <7.30"
        })
        
        af_points = self.SCORE_COMPONENTS["atrial_fibrillation"][atrial_fibrillation]
        components.append({
            "component": "Atrial Fibrillation",
            "value": atrial_fibrillation,
            "points": af_points,
            "description": f"Atrial fibrillation on ECG or history"
        })
        
        return components
    
    def _get_interpretation(self, risk_category, decaf_score, risk_details):
        """Get comprehensive interpretation of DECAF assessment"""
        
        base_interpretation = (f"DECAF score of {decaf_score} indicates {risk_details['label']} "
                             f"with {risk_details['mortality_range']} in-hospital mortality risk.")
        
        if risk_category == "low":
            return (f"{base_interpretation} Routine ward-based management is appropriate "
                   f"with standard COPD exacerbation care.")
        
        elif risk_category == "intermediate":
            return (f"{base_interpretation} Use clinical judgment regarding disposition "
                   f"and consider closer monitoring with frequent reassessment.")
        
        else:  # high risk
            return (f"{base_interpretation} Strong consideration for escalation of care "
                   f"(HDU/ICU) or palliative care discussions depending on goals of care.")


def calculate_decaf_score(emrcd_dyspnea: str, eosinopenia: str, consolidation: str,
                         acidemia: str, atrial_fibrillation: str,
                         patient_age: Optional[int] = None, 
                         smoking_history: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DecafScoreCalculator()
    return calculator.calculate(emrcd_dyspnea, eosinopenia, consolidation,
                              acidemia, atrial_fibrillation, patient_age, smoking_history)