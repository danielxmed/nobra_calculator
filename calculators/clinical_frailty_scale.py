"""
CSHA Clinical Frailty Scale (CFS) Calculator

Measures frailty to predict survival, mortality, need for institutional care, 
and other adverse outcomes in older adults aged 65 and over.

References:
- Rockwood K, Song X, MacKnight C, et al. CMAJ. 2005;173(5):489-495.
- Church S, Rogers E, Rockwood K, Theou O. BMC Geriatr. 2020;20(1):393.
- Clegg A, Young J, Iliffe S, Rikkert MO, Rockwood K. Lancet. 2013;381(9868):752-762.
"""

from typing import Dict, Any, Optional


class ClinicalFrailtyScaleCalculator:
    """Calculator for CSHA Clinical Frailty Scale (CFS)"""
    
    def __init__(self):
        # Frailty scale definitions
        self.FRAILTY_LEVELS = {
            1: {
                "label": "Very Fit",
                "description": "People who are robust, active, energetic, and motivated. These people commonly exercise regularly. They are among the fittest for their age.",
                "risk_level": "very_low",
                "mortality_risk": "very_low"
            },
            2: {
                "label": "Fit", 
                "description": "People who have no severe disease symptoms but are less fit than category 1. They exercise or are very active occasionally, e.g., seasonally.",
                "risk_level": "very_low",
                "mortality_risk": "very_low"
            },
            3: {
                "label": "Managing Well",
                "description": "People whose medical problems are well-controlled but are not regularly active beyond routine walking.",
                "risk_level": "low",
                "mortality_risk": "low"
            },
            4: {
                "label": "Living with Very Mild Frailty",
                "description": "Previously named 'Vulnerable'. While not dependent on others for daily help, symptoms often limit activities.",
                "risk_level": "mild",
                "mortality_risk": "low"
            },
            5: {
                "label": "Living with Mild Frailty",
                "description": "These people often have more evident slowing, and need help in high order instrumental activities of daily living (finances, transportation, heavy housework, medications). Typically, mild frailty progressively impairs shopping and walking outside alone, meal preparation, and housework.",
                "risk_level": "moderate",
                "mortality_risk": "moderate"
            },
            6: {
                "label": "Living with Moderate Frailty", 
                "description": "People need help with all outside activities and with keeping house. Inside, they often have problems with stairs and need help with bathing and might need minimal assistance (cuing, standby) with dressing.",
                "risk_level": "moderate",
                "mortality_risk": "moderate"
            },
            7: {
                "label": "Living with Severe Frailty",
                "description": "Completely dependent for personal care, from whatever cause (physical or cognitive). Even so, they seem stable and not at high risk of dying (within ~6 months).",
                "risk_level": "high",
                "mortality_risk": "high"
            },
            8: {
                "label": "Living with Very Severe Frailty",
                "description": "Completely dependent, approaching the end of life. Typically, they could not recover even from a minor illness.",
                "risk_level": "very_high",
                "mortality_risk": "very_high"
            },
            9: {
                "label": "Terminally Ill",
                "description": "Approaching the end of life. This category applies to people with a life expectancy of under 6 months, who are not otherwise evidently frail.",
                "risk_level": "very_high",
                "mortality_risk": "very_high"
            }
        }
        
        # Risk categories
        self.RISK_CATEGORIES = {
            "very_low": {"label": "Very Low Risk", "color": "green"},
            "low": {"label": "Low Risk", "color": "lightgreen"},
            "mild": {"label": "Mild Risk", "color": "yellow"},
            "moderate": {"label": "Moderate Risk", "color": "orange"},
            "high": {"label": "High Risk", "color": "red"},
            "very_high": {"label": "Very High Risk", "color": "darkred"}
        }
    
    def calculate(self, frailty_level: int, age: int, 
                  dementia_present: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates Clinical Frailty Scale assessment and risk stratification
        
        Args:
            frailty_level (int): CFS level from 1 (Very Fit) to 9 (Terminally Ill)
            age (int): Patient age in years (must be ≥65)
            dementia_present (str, optional): "yes", "no", or "unknown"
            
        Returns:
            Dict with frailty assessment, risk stratification, and recommendations
        """
        
        # Validations
        self._validate_inputs(frailty_level, age, dementia_present)
        
        # Get frailty level details
        frailty_details = self.FRAILTY_LEVELS[frailty_level]
        
        # Determine risk stratification
        risk_assessment = self._get_risk_assessment(frailty_level)
        
        # Get clinical recommendations
        recommendations = self._get_clinical_recommendations(frailty_level, age, dementia_present)
        
        # Get predictive outcomes
        outcomes = self._get_predictive_outcomes(frailty_level)
        
        return {
            "result": frailty_level,
            "unit": "CFS level",
            "interpretation": self._get_interpretation(frailty_level),
            "stage": frailty_details["label"],
            "stage_description": frailty_details["description"],
            "risk_assessment": risk_assessment,
            "clinical_recommendations": recommendations,
            "predictive_outcomes": outcomes,
            "frailty_category": self._get_frailty_category(frailty_level),
            "mortality_risk": frailty_details["mortality_risk"],
            "intervention_suitability": self._get_intervention_suitability(frailty_level),
            "care_planning": self._get_care_planning_guidance(frailty_level)
        }
    
    def _validate_inputs(self, frailty_level: int, age: int, dementia_present: Optional[str]):
        """Validates input parameters"""
        
        if not isinstance(frailty_level, int) or not 1 <= frailty_level <= 9:
            raise ValueError("Frailty level must be an integer between 1 and 9")
        
        if not isinstance(age, int) or age < 65:
            raise ValueError("Age must be 65 years or older (CFS is only validated for patients ≥65)")
        
        if age > 120:
            raise ValueError("Age must be 120 years or less")
        
        if dementia_present is not None and dementia_present not in ["yes", "no", "unknown"]:
            raise ValueError("Dementia present must be 'yes', 'no', or 'unknown'")
    
    def _get_risk_assessment(self, frailty_level: int) -> Dict[str, Any]:
        """Get comprehensive risk assessment based on frailty level"""
        
        frailty_details = self.FRAILTY_LEVELS[frailty_level]
        risk_level = frailty_details["risk_level"]
        
        # Risk percentages based on literature review
        risk_data = {
            "very_low": {"mortality_6_month": "<5%", "hospital_readmission": "<15%", "functional_decline": "<10%"},
            "low": {"mortality_6_month": "5-10%", "hospital_readmission": "15-25%", "functional_decline": "10-20%"},
            "mild": {"mortality_6_month": "10-15%", "hospital_readmission": "25-35%", "functional_decline": "20-30%"},
            "moderate": {"mortality_6_month": "15-25%", "hospital_readmission": "35-45%", "functional_decline": "30-50%"},
            "high": {"mortality_6_month": "25-40%", "hospital_readmission": "45-60%", "functional_decline": "50-70%"},
            "very_high": {"mortality_6_month": ">40%", "hospital_readmission": ">60%", "functional_decline": ">70%"}
        }
        
        return {
            "overall_risk": self.RISK_CATEGORIES[risk_level]["label"],
            "risk_color": self.RISK_CATEGORIES[risk_level]["color"],
            "mortality_6_month": risk_data[risk_level]["mortality_6_month"],
            "hospital_readmission": risk_data[risk_level]["hospital_readmission"],
            "functional_decline": risk_data[risk_level]["functional_decline"],
            "institutionalization_risk": self._get_institutionalization_risk(frailty_level)
        }
    
    def _get_institutionalization_risk(self, frailty_level: int) -> str:
        """Get risk of requiring institutional care"""
        
        if frailty_level <= 3:
            return "Very low risk of requiring institutional care"
        elif frailty_level == 4:
            return "Low risk of requiring institutional care"
        elif frailty_level in [5, 6]:
            return "Moderate to high risk of requiring institutional care"
        else:
            return "High risk or already requiring institutional care"
    
    def _get_clinical_recommendations(self, frailty_level: int, age: int, 
                                      dementia_present: Optional[str]) -> Dict[str, Any]:
        """Get clinical recommendations based on frailty assessment"""
        
        recommendations = []
        monitoring = []
        interventions = []
        
        if frailty_level <= 3:
            recommendations.extend([
                "Focus on maintaining current fitness and preventing decline",
                "Encourage regular physical activity and exercise",
                "Ensure adequate nutrition and hydration",
                "Annual comprehensive health assessment"
            ])
            monitoring.append("Annual frailty reassessment")
            interventions.extend(["Exercise programs", "Nutritional counseling", "Preventive care"])
            
        elif frailty_level == 4:
            recommendations.extend([
                "Close monitoring for early signs of decline",
                "Consider preventive interventions",
                "Optimize management of chronic conditions",
                "Fall prevention strategies"
            ])
            monitoring.append("6-monthly frailty reassessment")
            interventions.extend(["Comprehensive geriatric assessment", "Physical therapy", "Medication review"])
            
        elif frailty_level in [5, 6]:
            recommendations.extend([
                "Comprehensive geriatric assessment indicated",
                "Consider targeted interventions for identified deficits",
                "Coordinate care with geriatrics team",
                "Assess need for home support services"
            ])
            monitoring.append("3-6 monthly reassessment")
            interventions.extend(["Multidisciplinary care team", "Home care services", "Caregiver support"])
            
        else:  # 7, 8, 9
            recommendations.extend([
                "Focus on comfort and quality of life",
                "Consider palliative care consultation",
                "Assess appropriate care setting",
                "Support family and caregivers"
            ])
            monitoring.append("Frequent reassessment as clinically indicated")
            interventions.extend(["Palliative care", "End-of-life planning", "Symptom management"])
        
        # Dementia-specific considerations
        if dementia_present == "yes":
            recommendations.append("Consider dementia-specific care pathways")
            interventions.append("Cognitive support services")
        
        return {
            "primary_recommendations": recommendations,
            "monitoring_schedule": monitoring,
            "suggested_interventions": interventions,
            "care_setting": self._get_appropriate_care_setting(frailty_level)
        }
    
    def _get_appropriate_care_setting(self, frailty_level: int) -> str:
        """Determine appropriate care setting"""
        
        if frailty_level <= 4:
            return "Community-based care with outpatient follow-up"
        elif frailty_level in [5, 6]:
            return "Consider home care services or assisted living"
        else:
            return "May require skilled nursing or residential care"
    
    def _get_predictive_outcomes(self, frailty_level: int) -> Dict[str, Any]:
        """Get predictive outcomes based on frailty level"""
        
        # Based on literature review of CFS predictive validity
        if frailty_level <= 3:
            return {
                "hospital_length_of_stay": "Shorter than average",
                "icu_mortality": "Low risk",
                "surgical_outcomes": "Good candidate for surgery",
                "recovery_potential": "Excellent",
                "emergency_outcomes": "Low risk of adverse events"
            }
        elif frailty_level == 4:
            return {
                "hospital_length_of_stay": "Average",
                "icu_mortality": "Low to moderate risk",
                "surgical_outcomes": "Generally good candidate",
                "recovery_potential": "Good with support",
                "emergency_outcomes": "Moderate risk of adverse events"
            }
        elif frailty_level in [5, 6]:
            return {
                "hospital_length_of_stay": "Longer than average",
                "icu_mortality": "Moderate to high risk",
                "surgical_outcomes": "Consider risks vs benefits",
                "recovery_potential": "Limited, requires support",
                "emergency_outcomes": "High risk of adverse events"
            }
        else:
            return {
                "hospital_length_of_stay": "Prolonged",
                "icu_mortality": "Very high risk",
                "surgical_outcomes": "High-risk candidate",
                "recovery_potential": "Poor",
                "emergency_outcomes": "Very high risk of adverse events"
            }
    
    def _get_frailty_category(self, frailty_level: int) -> str:
        """Get general frailty category"""
        
        if frailty_level <= 3:
            return "Fit to Managing Well"
        elif frailty_level == 4:
            return "Very Mild Frailty"
        elif frailty_level in [5, 6]:
            return "Mild to Moderate Frailty"
        elif frailty_level in [7, 8]:
            return "Severe to Very Severe Frailty"
        else:
            return "Terminally Ill"
    
    def _get_intervention_suitability(self, frailty_level: int) -> Dict[str, str]:
        """Assess suitability for different interventions"""
        
        if frailty_level <= 3:
            return {
                "intensive_interventions": "Highly suitable",
                "surgical_procedures": "Good candidate",
                "rehabilitation": "Excellent potential",
                "clinical_trials": "Suitable candidate"
            }
        elif frailty_level == 4:
            return {
                "intensive_interventions": "Generally suitable with monitoring",
                "surgical_procedures": "Good candidate with precautions",
                "rehabilitation": "Good potential",
                "clinical_trials": "Consider on case-by-case basis"
            }
        elif frailty_level in [5, 6]:
            return {
                "intensive_interventions": "Carefully consider risks vs benefits",
                "surgical_procedures": "High-risk candidate",
                "rehabilitation": "Limited potential",
                "clinical_trials": "Generally not suitable"
            }
        else:
            return {
                "intensive_interventions": "Generally not suitable",
                "surgical_procedures": "Very high-risk candidate",
                "rehabilitation": "Poor potential",
                "clinical_trials": "Not suitable"
            }
    
    def _get_care_planning_guidance(self, frailty_level: int) -> Dict[str, Any]:
        """Get care planning guidance"""
        
        if frailty_level <= 3:
            return {
                "goals_of_care": "Maintain independence and prevent decline",
                "advance_directives": "Consider completing if not already done",
                "family_involvement": "Keep informed, support independence",
                "resource_needs": "Minimal, focus on prevention"
            }
        elif frailty_level == 4:
            return {
                "goals_of_care": "Prevent progression, optimize function",
                "advance_directives": "Important to complete",
                "family_involvement": "Involve in care planning",
                "resource_needs": "Preventive services, monitoring"
            }
        elif frailty_level in [5, 6]:
            return {
                "goals_of_care": "Optimize comfort and function, prevent complications",
                "advance_directives": "Essential to complete",
                "family_involvement": "Active involvement in care decisions",
                "resource_needs": "Home support, coordinated care"
            }
        else:
            return {
                "goals_of_care": "Comfort, quality of life, dignified care",
                "advance_directives": "Review and update regularly",
                "family_involvement": "Central to care planning",
                "resource_needs": "Palliative care, end-of-life support"
            }
    
    def _get_interpretation(self, frailty_level: int) -> str:
        """Get comprehensive interpretation of frailty assessment"""
        
        frailty_details = self.FRAILTY_LEVELS[frailty_level]
        
        if frailty_level <= 3:
            return (f"CFS level {frailty_level} ({frailty_details['label']}) indicates {frailty_details['description'].lower()} "
                   f"This represents low frailty risk with good prognosis for recovery and suitability for intensive interventions. "
                   f"Focus should be on maintaining current fitness level and preventing decline through regular activity and preventive care.")
        
        elif frailty_level == 4:
            return (f"CFS level {frailty_level} ({frailty_details['label']}) indicates {frailty_details['description'].lower()} "
                   f"This represents vulnerability to stressors with need for close monitoring. Patient may benefit from "
                   f"preventive interventions and comprehensive assessment while maintaining relative independence.")
        
        elif frailty_level in [5, 6]:
            return (f"CFS level {frailty_level} ({frailty_details['label']}) indicates {frailty_details['description'].lower()} "
                   f"This represents significant functional limitations requiring assistance with complex activities. "
                   f"Comprehensive geriatric assessment and targeted interventions are recommended.")
        
        else:  # 7, 8, 9
            return (f"CFS level {frailty_level} ({frailty_details['label']}) indicates {frailty_details['description'].lower()} "
                   f"This represents very high risk of adverse outcomes with focus needed on comfort, quality of life, "
                   f"and appropriate care setting. Consider palliative care consultation and end-of-life planning.")


def calculate_clinical_frailty_scale(frailty_level: int, age: int, 
                                   dementia_present: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ClinicalFrailtyScaleCalculator()
    return calculator.calculate(frailty_level, age, dementia_present)