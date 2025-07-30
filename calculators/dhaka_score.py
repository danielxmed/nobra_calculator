"""
Dehydration: Assessing Kids Accurately (DHAKA) Score Calculator

Classifies dehydration severity in children under 5 years old with acute diarrhea 
using four clinical assessment parameters.

References:
- Chisti MJ, et al. Lancet Glob Health. 2015;3(4):e204-e211.
- Pietroni MAC, et al. Lancet Glob Health. 2016;4(10):e744-e751.
- Goldman RD, et al. Pediatrics. 2008;122(3):545-549.
"""

from typing import Dict, Any, Optional


class DhakaScoreCalculator:
    """Calculator for DHAKA Score for Pediatric Dehydration Assessment"""
    
    def __init__(self):
        # DHAKA score components and weights
        self.SCORE_COMPONENTS = {
            "general_appearance": {
                "normal": 0,
                "restless_irritable": 2,
                "lethargic_unconscious": 4
            },
            "respirations": {
                "normal": 0,
                "deep": 2
            },
            "skin_pinch": {
                "normal": 0,
                "slow": 2,
                "very_slow": 4
            },
            "tears": {
                "normal": 0,
                "decreased": 1,
                "absent": 2
            }
        }
        
        # Dehydration categories and clinical data
        self.DEHYDRATION_CATEGORIES = {
            "none": {
                "score_range": (0, 1),
                "label": "No Dehydration",
                "description": "Minimal or no fluid loss",
                "fluid_loss": "<3%",
                "management": "Encourage fluid intake, continue normal diet",
                "monitoring": "Routine monitoring",
                "disposition": "Outpatient management"
            },
            "some": {
                "score_range": (2, 3),
                "label": "Some Dehydration",
                "description": "Mild to moderate fluid loss",
                "fluid_loss": "3-9%",
                "management": "Supervised oral rehydration therapy",
                "monitoring": "Close monitoring",
                "disposition": "Outpatient with close follow-up"
            },
            "severe": {
                "score_range": (4, 10),
                "label": "Severe Dehydration",
                "description": "Significant fluid loss requiring immediate intervention",
                "fluid_loss": "≥10%",
                "management": "Immediate IV rehydration, potential hospitalization",
                "monitoring": "Intensive monitoring",
                "disposition": "Hospitalization required"
            }
        }
        
        # Management recommendations by dehydration level
        self.MANAGEMENT_RECOMMENDATIONS = {
            "none": [
                "Encourage continued fluid intake and breastfeeding",
                "Continue normal age-appropriate diet",
                "Provide zinc supplementation as recommended",
                "Monitor for signs of worsening dehydration",
                "Educate caregivers on warning signs",
                "Follow-up as needed based on clinical course"
            ],
            "some": [
                "Initiate supervised oral rehydration therapy (ORT)",
                "Administer ORS solution according to WHO/UNICEF recommendations",
                "Monitor response to therapy closely",
                "Continue breastfeeding and age-appropriate feeding",
                "Provide zinc supplementation",
                "Reassess hydration status frequently",
                "Consider admission if ORT fails or tolerance is poor"
            ],
            "severe": [
                "Immediate intravenous fluid resuscitation",
                "Rapid assessment and stabilization of vital signs",
                "Monitor for complications (shock, electrolyte imbalances)",
                "Hospitalization for close monitoring",
                "Transition to ORT once clinically stable",
                "Address underlying causes and complications",
                "Multidisciplinary care coordination"
            ]
        }
    
    def calculate(self, general_appearance: str, respirations: str, skin_pinch: str,
                  tears: str, child_age_months: Optional[int] = None,
                  diarrhea_duration: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates DHAKA score for pediatric dehydration assessment
        
        Args:
            general_appearance (str): Child's general appearance and consciousness level
            respirations (str): Respiratory pattern assessment
            skin_pinch (str): Skin elasticity test results
            tears (str): Tear production when child cries
            child_age_months (int, optional): Child age for validity assessment
            diarrhea_duration (int, optional): Duration of diarrhea for clinical context
            
        Returns:
            Dict with DHAKA score, dehydration classification, and management recommendations
        """
        
        # Validations
        self._validate_inputs(general_appearance, respirations, skin_pinch, tears,
                            child_age_months, diarrhea_duration)
        
        # Calculate DHAKA score
        dhaka_score = self._calculate_dhaka_score(general_appearance, respirations,
                                                skin_pinch, tears)
        
        # Determine dehydration category
        dehydration_category = self._determine_dehydration_category(dhaka_score)
        
        # Get category details
        category_details = self.DEHYDRATION_CATEGORIES[dehydration_category]
        
        # Generate clinical assessment
        clinical_assessment = self._get_clinical_assessment(
            general_appearance, respirations, skin_pinch, tears, dhaka_score,
            dehydration_category, child_age_months, diarrhea_duration)
        
        # Get management recommendations
        management_recommendations = self._get_management_recommendations(
            dehydration_category, dhaka_score, child_age_months)
        
        # Generate interpretation
        interpretation = self._get_interpretation(dehydration_category, dhaka_score, category_details)
        
        # Get rehydration details
        rehydration_details = self._get_rehydration_details(dehydration_category, child_age_months)
        
        return {
            "result": dhaka_score,
            "unit": "DHAKA score",
            "interpretation": interpretation,
            "stage": category_details["label"],
            "stage_description": category_details["description"],
            "dhaka_score": dhaka_score,
            "dehydration_category": dehydration_category,
            "fluid_loss": category_details["fluid_loss"],
            "management": category_details["management"],
            "monitoring_level": category_details["monitoring"],
            "disposition": category_details["disposition"],
            "clinical_assessment": clinical_assessment,
            "management_recommendations": management_recommendations,
            "rehydration_details": rehydration_details,
            "score_components": self._get_score_breakdown(
                general_appearance, respirations, skin_pinch, tears),
            "caregiver_education": self._get_caregiver_education(dehydration_category),
            "follow_up_recommendations": self._get_follow_up_recommendations(dehydration_category),
            "warning_signs": self._get_warning_signs()
        }
    
    def _validate_inputs(self, general_appearance, respirations, skin_pinch, tears,
                        child_age_months, diarrhea_duration):
        """Validates input parameters"""
        
        # Validate general appearance
        valid_appearance = ["normal", "restless_irritable", "lethargic_unconscious"]
        if general_appearance not in valid_appearance:
            raise ValueError(f"general_appearance must be one of: {valid_appearance}")
        
        # Validate respirations
        if respirations not in ["normal", "deep"]:
            raise ValueError("respirations must be 'normal' or 'deep'")
        
        # Validate skin pinch
        valid_skin_pinch = ["normal", "slow", "very_slow"]
        if skin_pinch not in valid_skin_pinch:
            raise ValueError(f"skin_pinch must be one of: {valid_skin_pinch}")
        
        # Validate tears
        valid_tears = ["normal", "decreased", "absent"]
        if tears not in valid_tears:
            raise ValueError(f"tears must be one of: {valid_tears}")
        
        # Validate optional parameters
        if child_age_months is not None:
            if not isinstance(child_age_months, int) or not 1 <= child_age_months <= 59:
                raise ValueError("Child age must be an integer between 1 and 59 months")
        
        if diarrhea_duration is not None:
            if not isinstance(diarrhea_duration, int) or not 1 <= diarrhea_duration <= 13:
                raise ValueError("Diarrhea duration must be an integer between 1 and 13 days")
    
    def _calculate_dhaka_score(self, general_appearance, respirations, skin_pinch, tears):
        """Calculates the DHAKA score using component weights"""
        
        score = 0
        
        # General appearance component (0-4 points)
        score += self.SCORE_COMPONENTS["general_appearance"][general_appearance]
        
        # Respirations component (0-2 points)
        score += self.SCORE_COMPONENTS["respirations"][respirations]
        
        # Skin pinch component (0-4 points)
        score += self.SCORE_COMPONENTS["skin_pinch"][skin_pinch]
        
        # Tears component (0-2 points)
        score += self.SCORE_COMPONENTS["tears"][tears]
        
        return score
    
    def _determine_dehydration_category(self, dhaka_score):
        """Determines dehydration category based on DHAKA score"""
        
        for category, details in self.DEHYDRATION_CATEGORIES.items():
            score_min, score_max = details["score_range"]
            if score_min <= dhaka_score <= score_max:
                return category
        
        # Handle edge case (should not occur with valid inputs)
        return "severe" if dhaka_score > 3 else "none"
    
    def _get_clinical_assessment(self, general_appearance, respirations, skin_pinch,
                                tears, dhaka_score, dehydration_category,
                                child_age_months, diarrhea_duration):
        """Generate clinical assessment based on parameters"""
        
        assessment = {
            "dhaka_score": dhaka_score,
            "dehydration_category": dehydration_category,
            "score_components": [],
            "clinical_factors": [],
            "validity_criteria": [],
            "risk_factors": []
        }
        
        # Document score components
        appearance_descriptions = {
            "normal": "Normal general appearance (0 points)",
            "restless_irritable": "Restless or irritable (2 points)",
            "lethargic_unconscious": "Lethargic or unconscious (4 points)"
        }
        assessment["score_components"].append(appearance_descriptions[general_appearance])
        
        respiration_descriptions = {
            "normal": "Normal respirations (0 points)",
            "deep": "Deep respirations (2 points)"
        }
        assessment["score_components"].append(respiration_descriptions[respirations])
        
        skin_descriptions = {
            "normal": "Normal skin pinch (0 points)",
            "slow": "Slow skin pinch return (2 points)",
            "very_slow": "Very slow skin pinch return (4 points)"
        }
        assessment["score_components"].append(skin_descriptions[skin_pinch])
        
        tear_descriptions = {
            "normal": "Normal tears when crying (0 points)",
            "decreased": "Decreased tears when crying (1 point)",
            "absent": "Absent tears when crying (2 points)"
        }
        assessment["score_components"].append(tear_descriptions[tears])
        
        # Clinical factors
        assessment["clinical_factors"] = [
            f"Child with acute diarrhea presenting with dehydration assessment",
            f"DHAKA score of {dhaka_score} indicates {dehydration_category} dehydration",
            f"Requires {self.DEHYDRATION_CATEGORIES[dehydration_category]['management'].lower()}"
        ]
        
        # Validity criteria
        if child_age_months is not None:
            if child_age_months < 60:
                assessment["validity_criteria"].append(f"Age {child_age_months} months (<60 months) - score validity met")
            else:
                assessment["validity_criteria"].append(f"Age {child_age_months} months (≥60 months) - score not validated for this age group")
        
        if diarrhea_duration is not None:
            if diarrhea_duration < 14:
                assessment["validity_criteria"].append(f"Diarrhea duration {diarrhea_duration} days (<14 days) - acute diarrhea criteria met")
            else:
                assessment["validity_criteria"].append(f"Diarrhea duration {diarrhea_duration} days (≥14 days) - chronic diarrhea, score may not apply")
        
        # Risk factors
        if general_appearance in ["restless_irritable", "lethargic_unconscious"]:
            assessment["risk_factors"].append("Altered mental status indicates significant dehydration")
        
        if respirations == "deep":
            assessment["risk_factors"].append("Deep respirations suggest metabolic acidosis")
        
        if skin_pinch in ["slow", "very_slow"]:
            assessment["risk_factors"].append("Poor skin elasticity indicates volume depletion")
        
        if tears in ["decreased", "absent"]:
            assessment["risk_factors"].append("Reduced tear production indicates dehydration")
        
        return assessment
    
    def _get_management_recommendations(self, dehydration_category, dhaka_score, child_age_months):
        """Get management recommendations based on dehydration assessment"""
        
        base_recommendations = self.MANAGEMENT_RECOMMENDATIONS[dehydration_category].copy()
        specific_recommendations = []
        
        # Age-specific considerations
        if child_age_months is not None:
            if child_age_months < 6:
                specific_recommendations.append("Infant <6 months - breastfeeding strongly encouraged")
                specific_recommendations.append("Consider lower threshold for admission due to higher risk")
            elif child_age_months < 12:
                specific_recommendations.append("Infant <12 months - close monitoring for rapid deterioration")
            elif child_age_months < 24:
                specific_recommendations.append("Toddler - may require modified approach for cooperation with ORT")
        
        # Score-specific considerations
        if dhaka_score >= 6:
            specific_recommendations.append("High DHAKA score indicates very severe dehydration - urgent intervention needed")
        
        if dehydration_category == "severe":
            specific_recommendations.append("Consider ICU admission if shock or complications present")
            specific_recommendations.append("Rapid sequence rehydration with careful monitoring")
        
        return {
            "primary_recommendations": base_recommendations,
            "specific_considerations": specific_recommendations,
            "fluid_therapy": self._get_fluid_therapy_guidance(dehydration_category, child_age_months),
            "monitoring_requirements": self._get_monitoring_requirements(dehydration_category)
        }
    
    def _get_fluid_therapy_guidance(self, dehydration_category, child_age_months):
        """Get fluid therapy guidance based on dehydration level"""
        
        if dehydration_category == "none":
            return {
                "route": "Oral",
                "solution": "Continue normal fluids and breast milk",
                "rate": "As tolerated",
                "duration": "Until clinically improved",
                "monitoring": "Routine observation"
            }
        elif dehydration_category == "some":
            return {
                "route": "Oral rehydration therapy",
                "solution": "WHO/UNICEF ORS solution",
                "rate": "75 mL/kg over 4 hours if <2 years, 50 mL/kg if ≥2 years",
                "duration": "4-6 hours with reassessment",
                "monitoring": "Hourly assessment for first 4 hours"
            }
        else:  # severe
            return {
                "route": "Intravenous",
                "solution": "Lactated Ringer's or Normal Saline",
                "rate": "20 mL/kg bolus, then 100 mL/kg over 6 hours",
                "duration": "Until hemodynamically stable, then transition to ORT",
                "monitoring": "Continuous monitoring with frequent vital signs"
            }
    
    def _get_monitoring_requirements(self, dehydration_category):
        """Get monitoring requirements based on dehydration level"""
        
        if dehydration_category == "none":
            return [
                "Monitor for worsening symptoms",
                "Assess fluid intake and output",
                "Watch for signs of deterioration",
                "Follow-up in 24-48 hours"
            ]
        elif dehydration_category == "some":
            return [
                "Assess hydration status every 1-2 hours",
                "Monitor tolerance of oral rehydration",
                "Watch for signs of improvement or deterioration",
                "Reassess DHAKA score after 4 hours of therapy",
                "Monitor urine output and frequency"
            ]
        else:  # severe
            return [
                "Continuous monitoring of vital signs",
                "Frequent assessment of perfusion and mental status",
                "Hourly urine output measurement",
                "Monitor for fluid overload and electrolyte imbalances",
                "Serial assessment of hydration parameters",
                "Consider central venous access if difficult IV access"
            ]
    
    def _get_rehydration_details(self, dehydration_category, child_age_months):
        """Get specific rehydration details"""
        
        details = {
            "urgency": "",
            "setting": "",
            "expected_duration": "",
            "success_indicators": [],
            "failure_indicators": []
        }
        
        if dehydration_category == "none":
            details["urgency"] = "Non-urgent"
            details["setting"] = "Home or outpatient"
            details["expected_duration"] = "24-48 hours"
            details["success_indicators"] = [
                "Maintained normal activity level",
                "Good fluid intake",
                "Normal urination pattern"
            ]
            details["failure_indicators"] = [
                "Decreased fluid intake",
                "Worsening lethargy",
                "Decreased urination"
            ]
        
        elif dehydration_category == "some":
            details["urgency"] = "Moderate urgency"
            details["setting"] = "Outpatient with close supervision"
            details["expected_duration"] = "4-6 hours"
            details["success_indicators"] = [
                "Improved alertness and activity",
                "Good tolerance of ORS",
                "Improved skin elasticity",
                "Increased urination"
            ]
            details["failure_indicators"] = [
                "Poor tolerance of ORS",
                "Persistent lethargy",
                "Worsening dehydration signs",
                "Inability to keep fluids down"
            ]
        
        else:  # severe
            details["urgency"] = "Emergency"
            details["setting"] = "Emergency department or hospital"
            details["expected_duration"] = "6-24 hours"
            details["success_indicators"] = [
                "Improved perfusion and mental status",
                "Stabilized vital signs",
                "Improved urine output",
                "Ability to transition to oral intake"
            ]
            details["failure_indicators"] = [
                "Persistent shock",
                "Worsening mental status",
                "Electrolyte abnormalities",
                "Complications of rapid rehydration"
            ]
        
        return details
    
    def _get_caregiver_education(self, dehydration_category):
        """Get caregiver education points"""
        
        general_education = [
            "Continue breastfeeding throughout illness if applicable",
            "Offer fluids frequently in small amounts",
            "Watch for signs of worsening dehydration",
            "Seek medical attention if child becomes more lethargic",
            "Complete zinc supplementation course as prescribed"
        ]
        
        if dehydration_category == "none":
            specific_education = [
                "Child has minimal dehydration and can be managed at home",
                "Continue normal feeding and encourage extra fluids",
                "Monitor for any worsening of condition",
                "Return for follow-up if symptoms persist or worsen"
            ]
        elif dehydration_category == "some":
            specific_education = [
                "Child needs oral rehydration therapy",
                "Give ORS solution frequently in small amounts",
                "Continue feeding once vomiting stops",
                "Watch closely for improvement over next few hours",
                "Return immediately if unable to keep fluids down"
            ]
        else:  # severe
            specific_education = [
                "Child has severe dehydration requiring immediate medical care",
                "Hospital treatment is necessary",
                "IV fluids will be needed initially",
                "Close monitoring is required until stable",
                "Follow all medical team instructions carefully"
            ]
        
        return general_education + specific_education
    
    def _get_follow_up_recommendations(self, dehydration_category):
        """Get follow-up recommendations based on dehydration level"""
        
        if dehydration_category == "none":
            return {
                "timing": "24-48 hours if symptoms persist",
                "location": "Primary care or return visit as needed",
                "monitoring": "Home monitoring by caregivers",
                "red_flags": "Persistent vomiting, lethargy, decreased urination"
            }
        elif dehydration_category == "some":
            return {
                "timing": "4-6 hours for reassessment, then daily until resolved",
                "location": "Healthcare facility for initial reassessment",
                "monitoring": "Close outpatient monitoring",
                "red_flags": "Inability to tolerate ORS, worsening lethargy, signs of severe dehydration"
            }
        else:  # severe
            return {
                "timing": "Continuous until stable, then daily monitoring",
                "location": "Hospital until stable, then outpatient follow-up",
                "monitoring": "Inpatient monitoring until clinical improvement",
                "red_flags": "Any signs of clinical deterioration or complications"
            }
    
    def _get_warning_signs(self):
        """Get universal warning signs for caregivers"""
        
        return [
            "Child becomes increasingly lethargic or difficult to wake",
            "Persistent vomiting preventing fluid intake",
            "Blood in vomit or stool",
            "High fever (>39°C/102.2°F)",
            "Significant decrease or absence of urination",
            "Worsening of any dehydration signs",
            "Child appears severely ill or distressed",
            "Convulsions or loss of consciousness"
        ]
    
    def _get_score_breakdown(self, general_appearance, respirations, skin_pinch, tears):
        """Get detailed breakdown of score components"""
        
        components = []
        
        appearance_points = self.SCORE_COMPONENTS["general_appearance"][general_appearance]
        components.append({
            "component": "General Appearance",
            "value": general_appearance,
            "points": appearance_points,
            "description": "Child's level of consciousness and activity"
        })
        
        respiration_points = self.SCORE_COMPONENTS["respirations"][respirations]
        components.append({
            "component": "Respirations",
            "value": respirations,
            "points": respiration_points,
            "description": "Respiratory pattern and effort"
        })
        
        skin_points = self.SCORE_COMPONENTS["skin_pinch"][skin_pinch]
        components.append({
            "component": "Skin Pinch",
            "value": skin_pinch,
            "points": skin_points,
            "description": "Skin elasticity and turgor"
        })
        
        tear_points = self.SCORE_COMPONENTS["tears"][tears]
        components.append({
            "component": "Tears",
            "value": tears,
            "points": tear_points,
            "description": "Tear production when crying"
        })
        
        return components
    
    def _get_interpretation(self, dehydration_category, dhaka_score, category_details):
        """Get comprehensive interpretation of DHAKA assessment"""
        
        base_interpretation = (f"DHAKA score of {dhaka_score} indicates {category_details['label']} "
                             f"with {category_details['fluid_loss']} estimated fluid loss.")
        
        if dehydration_category == "none":
            return (f"{base_interpretation} Child has minimal dehydration and can be managed "
                   f"with continued fluid intake and normal diet. Monitor for any worsening.")
        
        elif dehydration_category == "some":
            return (f"{base_interpretation} Child requires supervised oral rehydration therapy "
                   f"with close monitoring for response to treatment and possible deterioration.")
        
        else:  # severe
            return (f"{base_interpretation} Child has severe dehydration requiring immediate "
                   f"intravenous rehydration and hospitalization for intensive monitoring.")


def calculate_dhaka_score(general_appearance: str, respirations: str, skin_pinch: str,
                         tears: str, child_age_months: Optional[int] = None,
                         diarrhea_duration: Optional[int] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DhakaScoreCalculator()
    return calculator.calculate(general_appearance, respirations, skin_pinch, tears,
                              child_age_months, diarrhea_duration)