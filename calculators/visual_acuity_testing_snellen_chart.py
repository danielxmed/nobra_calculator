"""
Visual Acuity Testing (Snellen Chart) Calculator

Assesses binocular and monocular visual acuity using standardized Snellen optotypes.

References:
1. Snellen H. Probebuchstaben zur Bestimmung der Sehschärfe. Utrecht: Van de Weijer; 1862.
2. Elliott DB. The good (logMAR), the bad (Snellen) and the ugly (BCVA, number of 
   letters read) of visual acuity measurement. Ophthalmic Physiol Opt. 2016;36(4):355-358.
3. Bailey IL, Lovie JE. New design principles for visual acuity letter charts. 
   Am J Optom Physiol Opt. 1976;53(11):740-745.
"""

from typing import Dict, Any


class VisualAcuityTestingSnellenChartCalculator:
    """Calculator for Visual Acuity Testing (Snellen Chart)"""
    
    def __init__(self):
        # Mapping of Snellen chart lines to visual acuity values
        self.LINE_TO_ACUITY = {
            "line_1_20_200": "20/200",
            "line_2_20_160": "20/160", 
            "line_3_20_125": "20/125",
            "line_4_20_100": "20/100",
            "line_5_20_80": "20/80",
            "line_6_20_63": "20/63",
            "line_7_20_50": "20/50",
            "line_8_20_40": "20/40",
            "line_9_20_32": "20/32",
            "line_10_20_25": "20/25",
            "line_11_20_20": "20/20",
            "counting_fingers": "CF",
            "hand_motion": "HM",
            "light_perception": "LP",
            "no_light_perception": "NLP"
        }
        
        # Numerical conversion for comparison and severity assessment
        self.ACUITY_TO_DECIMAL = {
            "20/20": 1.0,
            "20/25": 0.8,
            "20/32": 0.625,
            "20/40": 0.5,
            "20/50": 0.4,
            "20/63": 0.317,
            "20/80": 0.25,
            "20/100": 0.2,
            "20/125": 0.16,
            "20/160": 0.125,
            "20/200": 0.1,
            "CF": 0.05,
            "HM": 0.025,
            "LP": 0.0125,
            "NLP": 0.0
        }
        
        # Distance conversion factors
        self.DISTANCE_FACTORS = {
            "20_feet": 1.0,      # Standard US distance
            "6_meters": 1.0,     # Standard metric distance (equivalent to 20 feet)
            "4_feet_mobile": 0.2  # Mobile device testing at 4 feet
        }
    
    def calculate(self, eye_tested: str, lowest_line_read: str, 
                 testing_distance: str, corrective_lenses: str) -> Dict[str, Any]:
        """
        Calculates visual acuity based on Snellen chart reading
        
        Args:
            eye_tested (str): Which eye was tested ("right_eye", "left_eye", "both_eyes")
            lowest_line_read (str): Smallest line read correctly on Snellen chart
            testing_distance (str): Distance at which test was performed
            corrective_lenses (str): Whether corrective lenses were worn during testing
            
        Returns:
            Dict with visual acuity result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(eye_tested, lowest_line_read, testing_distance, corrective_lenses)
        
        # Get base visual acuity
        visual_acuity = self.LINE_TO_ACUITY[lowest_line_read]
        
        # Adjust for testing distance if needed (primarily for mobile testing)
        adjusted_acuity = self._adjust_for_distance(visual_acuity, testing_distance)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(adjusted_acuity, eye_tested, corrective_lenses)
        
        # Generate detailed assessment
        detailed_assessment = self._generate_detailed_assessment(
            visual_acuity, adjusted_acuity, eye_tested, testing_distance, corrective_lenses
        )
        
        return {
            "result": adjusted_acuity,
            "unit": "fraction",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"],
            "detailed_assessment": detailed_assessment
        }
    
    def _validate_inputs(self, eye_tested: str, lowest_line_read: str, 
                        testing_distance: str, corrective_lenses: str):
        """Validates input parameters"""
        
        valid_eyes = ["right_eye", "left_eye", "both_eyes"]
        if eye_tested not in valid_eyes:
            raise ValueError(f"eye_tested must be one of: {valid_eyes}")
        
        if lowest_line_read not in self.LINE_TO_ACUITY:
            raise ValueError(f"lowest_line_read must be one of: {list(self.LINE_TO_ACUITY.keys())}")
        
        valid_distances = ["20_feet", "6_meters", "4_feet_mobile"]
        if testing_distance not in valid_distances:
            raise ValueError(f"testing_distance must be one of: {valid_distances}")
        
        valid_lenses = ["yes", "no", "unknown"]
        if corrective_lenses not in valid_lenses:
            raise ValueError(f"corrective_lenses must be one of: {valid_lenses}")
    
    def _adjust_for_distance(self, visual_acuity: str, testing_distance: str) -> str:
        """
        Adjusts visual acuity for non-standard testing distances
        
        Args:
            visual_acuity (str): Base visual acuity measurement
            testing_distance (str): Testing distance used
            
        Returns:
            str: Adjusted visual acuity
        """
        
        # For standard distances (20 feet/6 meters), no adjustment needed
        if testing_distance in ["20_feet", "6_meters"]:
            return visual_acuity
        
        # For mobile testing at 4 feet, note the limitation
        if testing_distance == "4_feet_mobile" and visual_acuity not in ["CF", "HM", "LP", "NLP"]:
            return f"{visual_acuity} (mobile)"
        
        return visual_acuity
    
    def _get_interpretation(self, visual_acuity: str, eye_tested: str, 
                          corrective_lenses: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on visual acuity
        
        Args:
            visual_acuity (str): Measured visual acuity
            eye_tested (str): Which eye was tested
            corrective_lenses (str): Corrective lens status
            
        Returns:
            Dict with interpretation details
        """
        
        # Remove mobile notation for classification
        clean_acuity = visual_acuity.replace(" (mobile)", "")
        
        # Get decimal equivalent for classification
        decimal_acuity = self.ACUITY_TO_DECIMAL.get(clean_acuity, 0.0)
        
        # Determine eye description
        eye_description = {
            "right_eye": "right eye",
            "left_eye": "left eye", 
            "both_eyes": "both eyes"
        }[eye_tested]
        
        # Determine correction status
        correction_status = {
            "yes": "with correction",
            "no": "without correction",
            "unknown": "correction status unknown"
        }[corrective_lenses]
        
        # Classify visual acuity
        if clean_acuity == "20/20":
            stage = "Normal"
            stage_description = "Normal visual acuity"
            base_interpretation = f"Visual acuity of 20/20 in the {eye_description} represents normal vision {correction_status}. "
            recommendations = "No immediate intervention needed unless other visual complaints are present. Continue routine eye care."
            
        elif decimal_acuity >= 0.5:  # 20/25 to 20/40
            stage = "Mild Impairment"
            stage_description = "Mild visual impairment"
            base_interpretation = f"Visual acuity of {clean_acuity} in the {eye_description} indicates mild visual impairment {correction_status}. "
            recommendations = "Ophthalmologic evaluation recommended to determine need for corrective lenses or rule out early eye disease."
            
        elif decimal_acuity >= 0.2:  # 20/50 to 20/100
            stage = "Moderate Impairment"
            stage_description = "Moderate visual impairment"
            base_interpretation = f"Visual acuity of {clean_acuity} in the {eye_description} represents moderate visual impairment {correction_status}. "
            recommendations = "Ophthalmologic evaluation indicated to determine underlying cause and appropriate treatment. This level of vision loss impacts daily activities."
            
        elif decimal_acuity >= 0.1:  # 20/125 to 20/200
            stage = "Severe Impairment"
            stage_description = "Severe visual impairment approaching legal blindness"
            base_interpretation = f"Visual acuity of {clean_acuity} in the {eye_description} represents severe visual impairment {correction_status}. "
            if clean_acuity == "20/200":
                base_interpretation += "This meets the criteria for legal blindness in the United States. "
            recommendations = "Urgent ophthalmologic evaluation required. Consider low vision rehabilitation services and visual aids."
            
        else:  # CF, HM, LP, NLP
            stage = "Profound Impairment"
            stage_description = "Profound visual impairment"
            acuity_descriptions = {
                "CF": "counting fingers",
                "HM": "hand motion",
                "LP": "light perception only",
                "NLP": "no light perception"
            }
            base_interpretation = f"Visual acuity of {acuity_descriptions.get(clean_acuity, clean_acuity)} in the {eye_description} represents profound visual impairment {correction_status}. "
            recommendations = "Immediate ophthalmologic evaluation required to determine if vision loss is reversible and identify any treatable causes."
        
        # Add mobile testing limitation if applicable
        if "(mobile)" in visual_acuity:
            mobile_note = " Note: This measurement was obtained using mobile device testing, which may be less accurate than standard chart testing."
            base_interpretation += mobile_note
        
        interpretation = base_interpretation + recommendations
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }
    
    def _generate_detailed_assessment(self, visual_acuity: str, adjusted_acuity: str,
                                     eye_tested: str, testing_distance: str, 
                                     corrective_lenses: str) -> Dict[str, Any]:
        """
        Generates detailed assessment information
        
        Returns:
            Dict with detailed assessment data
        """
        
        clean_acuity = adjusted_acuity.replace(" (mobile)", "")
        decimal_equivalent = self.ACUITY_TO_DECIMAL.get(clean_acuity, 0.0)
        
        # Determine testing method
        testing_method = {
            "20_feet": "Standard Snellen chart at 20 feet",
            "6_meters": "Standard Snellen chart at 6 meters", 
            "4_feet_mobile": "Mobile device testing at 4 feet"
        }[testing_distance]
        
        # Clinical significance
        clinical_significance = []
        
        if decimal_equivalent == 1.0:
            clinical_significance.append("Normal visual acuity for distance vision")
        elif decimal_equivalent >= 0.8:
            clinical_significance.append("Mild reduction in visual acuity")
        elif decimal_equivalent >= 0.5:
            clinical_significance.append("Moderate reduction affecting daily activities")
        elif decimal_equivalent >= 0.1:
            clinical_significance.append("Severe visual impairment requiring intervention")
        else:
            clinical_significance.append("Profound visual impairment requiring immediate evaluation")
        
        if corrective_lenses == "no" and decimal_equivalent < 1.0:
            clinical_significance.append("May benefit from corrective lenses")
        
        if "(mobile)" in adjusted_acuity:
            clinical_significance.append("Mobile testing limitation - confirmation with standard chart recommended")
        
        return {
            "measured_acuity": visual_acuity,
            "final_acuity": adjusted_acuity,
            "decimal_equivalent": decimal_equivalent,
            "eye_tested": eye_tested.replace("_", " ").title(),
            "testing_method": testing_method,
            "corrective_lenses_worn": corrective_lenses,
            "clinical_significance": clinical_significance,
            "legal_blindness_criteria": decimal_equivalent <= 0.1,
            "recommendations": self._get_follow_up_recommendations(decimal_equivalent, corrective_lenses)
        }
    
    def _get_follow_up_recommendations(self, decimal_acuity: float, 
                                     corrective_lenses: str) -> list:
        """
        Generates follow-up recommendations based on visual acuity
        
        Returns:
            List of clinical recommendations
        """
        
        recommendations = []
        
        if decimal_acuity == 1.0:
            recommendations.append("Continue routine eye examinations")
            if corrective_lenses == "unknown":
                recommendations.append("Confirm corrective lens status")
        elif decimal_acuity >= 0.8:
            recommendations.append("Ophthalmologic evaluation within 6 months")
            if corrective_lenses == "no":
                recommendations.append("Consider refractive evaluation")
        elif decimal_acuity >= 0.5:
            recommendations.append("Ophthalmologic evaluation within 3 months")
            recommendations.append("Assess for correctable causes")
        elif decimal_acuity >= 0.1:
            recommendations.append("Urgent ophthalmologic evaluation within 1-2 weeks")
            recommendations.append("Consider low vision services")
            recommendations.append("Assess safety for driving and daily activities")
        else:
            recommendations.append("Immediate ophthalmologic evaluation")
            recommendations.append("Emergency department if acute onset")
            recommendations.append("Low vision rehabilitation referral")
            recommendations.append("Assess for reversible causes")
        
        return recommendations


def calculate_visual_acuity_testing_snellen_chart(eye_tested, lowest_line_read, 
                                                 testing_distance, corrective_lenses) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_visual_acuity_testing_snellen_chart pattern
    """
    calculator = VisualAcuityTestingSnellenChartCalculator()
    return calculator.calculate(eye_tested, lowest_line_read, testing_distance, corrective_lenses)