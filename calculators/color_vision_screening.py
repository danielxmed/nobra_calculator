"""
Color Vision Screening (Ishihara Test) Calculator

Screens for red-green color blindness using the Ishihara pseudoisochromatic plates.
This abbreviated 14-plate version provides efficient screening while maintaining clinical accuracy.

References:
1. Ishihara S. Tests for Colour-Blindness. Tokyo: Kanehara Trading Inc; 1917.
2. Birch J. Worldwide prevalence of red-green color deficiency. J Opt Soc Am A Opt Image Sci Vis. 
   2012;29(3):313-20. doi: 10.1364/JOSAA.29.000313.
3. Dain SJ. Clinical colour vision tests. Clin Exp Optom. 2004;87(4-5):276-93. 
   doi: 10.1111/j.1444-0938.2004.tb05062.x.
4. Perera C, Chakrabarti R, Islam FM, Crowston J. The Eye Phone Study: reliability and 
   accuracy of assessing Neitz color vision with smartphone technology. Am J Ophthalmol. 
   2015;160(5):944-50.e1. doi: 10.1016/j.ajo.2015.08.014.
"""

from typing import Dict, Any


class ColorVisionScreeningCalculator:
    """Calculator for Color Vision Screening (Ishihara Test)"""
    
    def __init__(self):
        # Total plates in abbreviated screening test
        self.TOTAL_PLATES = 14
        
        # Threshold for color vision deficiency (more than 2 incorrect plates)
        self.DEFICIENCY_THRESHOLD = 2
        
        # Age threshold for reliability
        self.MIN_RELIABLE_AGE = 5
        
        # Test accuracy parameters
        self.test_performance = {
            "sensitivity": 0.92,  # 92% for red-green deficiencies
            "specificity": 1.00,  # 100% specificity
            "ppv_high_prevalence": 0.95,  # PPV in high-risk populations
            "npv_general": 0.99   # NPV in general population
        }
    
    def calculate(
        self,
        correct_plates_right_eye: int,
        correct_plates_left_eye: int,
        visual_acuity_adequate: str,
        patient_age: int
    ) -> Dict[str, Any]:
        """
        Evaluates color vision screening results using Ishihara test plates
        
        Args:
            correct_plates_right_eye: Number of plates correctly identified by right eye (0-14)
            correct_plates_left_eye: Number of plates correctly identified by left eye (0-14)
            visual_acuity_adequate: Visual acuity 20/100 or better (yes/no)
            patient_age: Patient age in years
            
        Returns:
            Dict with color vision assessment and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            correct_plates_right_eye, correct_plates_left_eye,
            visual_acuity_adequate, patient_age
        )
        
        # Calculate incorrect plates for each eye
        incorrect_right = self.TOTAL_PLATES - correct_plates_right_eye
        incorrect_left = self.TOTAL_PLATES - correct_plates_left_eye
        
        # Assess each eye independently
        right_eye_assessment = self._assess_eye_result(
            correct_plates_right_eye, incorrect_right, "Right"
        )
        left_eye_assessment = self._assess_eye_result(
            correct_plates_left_eye, incorrect_left, "Left"
        )
        
        # Overall assessment
        overall_assessment = self._get_overall_assessment(
            right_eye_assessment, left_eye_assessment
        )
        
        # Clinical recommendations
        recommendations = self._get_clinical_recommendations(
            overall_assessment, visual_acuity_adequate, patient_age
        )
        
        # Test limitations and warnings
        limitations = self._get_test_limitations(visual_acuity_adequate, patient_age)
        
        return {
            "result": {
                "right_eye": right_eye_assessment,
                "left_eye": left_eye_assessment,
                "overall_assessment": overall_assessment,
                "clinical_recommendations": recommendations,
                "test_performance": {
                    "sensitivity": f"{self.test_performance['sensitivity']*100:.0f}%",
                    "specificity": f"{self.test_performance['specificity']*100:.0f}%",
                    "applicable_deficiencies": "Red-green color vision defects (protanomaly, deuteranomaly)"
                },
                "test_limitations": limitations
            },
            "unit": "assessment",
            "interpretation": overall_assessment["interpretation"],
            "stage": overall_assessment["stage"],
            "stage_description": overall_assessment["description"]
        }
    
    def _validate_inputs(self, correct_right, correct_left, visual_acuity, age):
        """Validates input parameters"""
        
        # Validate plate counts
        if not isinstance(correct_right, int) or correct_right < 0 or correct_right > self.TOTAL_PLATES:
            raise ValueError(f"Right eye correct plates must be integer between 0 and {self.TOTAL_PLATES}")
        
        if not isinstance(correct_left, int) or correct_left < 0 or correct_left > self.TOTAL_PLATES:
            raise ValueError(f"Left eye correct plates must be integer between 0 and {self.TOTAL_PLATES}")
        
        # Validate visual acuity
        if visual_acuity not in ["yes", "no"]:
            raise ValueError("Visual acuity adequate must be 'yes' or 'no'")
        
        # Validate age
        if not isinstance(age, int) or age < 1 or age > 120:
            raise ValueError("Patient age must be integer between 1 and 120")
    
    def _assess_eye_result(self, correct_plates: int, incorrect_plates: int, eye_name: str) -> Dict[str, Any]:
        """Assesses color vision result for individual eye"""
        
        # Determine color vision status
        if incorrect_plates <= self.DEFICIENCY_THRESHOLD:
            if correct_plates >= 12:
                status = "Normal"
                risk_level = "Low"
                description = "Normal color vision"
                clinical_significance = "No color vision deficiency detected"
            else:
                status = "Borderline Normal"
                risk_level = "Low-Moderate"
                description = "Borderline normal color vision"
                clinical_significance = "Minimal errors may indicate mild deficiency or attention issues"
        elif incorrect_plates <= 6:
            status = "Possible Deficiency"
            risk_level = "Moderate"
            description = "Possible color vision deficiency"
            clinical_significance = "Moderate number of errors suggests possible color vision defect"
        else:
            status = "Likely Deficiency"
            risk_level = "High"
            description = "Color vision deficiency likely"
            clinical_significance = "Multiple errors strongly suggest red-green color vision deficiency"
        
        return {
            "eye": eye_name,
            "correct_plates": correct_plates,
            "incorrect_plates": incorrect_plates,
            "total_plates": self.TOTAL_PLATES,
            "accuracy_percentage": round((correct_plates / self.TOTAL_PLATES) * 100, 1),
            "status": status,
            "risk_level": risk_level,
            "description": description,
            "clinical_significance": clinical_significance
        }
    
    def _get_overall_assessment(self, right_assessment, left_assessment) -> Dict[str, str]:
        """Determines overall color vision assessment"""
        
        right_status = right_assessment["status"]
        left_status = left_assessment["status"]
        
        # Prioritize worst result
        deficiency_hierarchy = {
            "Likely Deficiency": 4,
            "Possible Deficiency": 3,
            "Borderline Normal": 2,
            "Normal": 1
        }
        
        worst_status = max([right_status, left_status], 
                          key=lambda x: deficiency_hierarchy[x])
        
        if worst_status == "Normal" and right_status == "Normal" and left_status == "Normal":
            stage = "Normal"
            description = "Normal color vision both eyes"
            interpretation = "Both eyes demonstrate normal color vision (>12/14 plates correct with ≤2 errors). No further color vision testing indicated unless clinical suspicion remains high."
            recommendation = "No additional color vision testing needed"
            
        elif worst_status in ["Normal", "Borderline Normal"]:
            stage = "Normal"
            description = "Normal color vision"
            interpretation = "Overall normal color vision with minimal errors. Results suggest intact red-green color discrimination ability."
            recommendation = "Consider repeat testing if clinical concerns persist"
            
        elif worst_status == "Possible Deficiency":
            stage = "Possible Deficiency"
            description = "Possible color vision deficiency"
            interpretation = "Moderate number of errors suggests possible color vision deficiency. May indicate mild red-green color discrimination difficulties."
            recommendation = "Consider ophthalmology referral for comprehensive color vision evaluation"
            
        else:  # Likely Deficiency
            stage = "Color Vision Deficiency"
            description = "Color vision deficiency likely"
            interpretation = "Multiple errors strongly suggest red-green color vision deficiency (protanomaly or deuteranomaly). Formal ophthalmologic evaluation recommended."
            recommendation = "Ophthalmology referral recommended for definitive diagnosis and management"
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "recommendation": recommendation,
            "bilateral_status": f"Right: {right_status}, Left: {left_status}"
        }
    
    def _get_clinical_recommendations(self, overall_assessment, visual_acuity, age) -> Dict[str, Any]:
        """Generates clinical recommendations based on results"""
        
        recommendations = {
            "primary_recommendation": overall_assessment["recommendation"],
            "follow_up_actions": [],
            "patient_counseling": [],
            "occupational_considerations": []
        }
        
        # Stage-specific recommendations
        if overall_assessment["stage"] == "Normal":
            recommendations["follow_up_actions"].append("Routine eye care as appropriate for age")
            recommendations["patient_counseling"].append("Normal color vision confirmed")
            
        elif overall_assessment["stage"] == "Possible Deficiency":
            recommendations["follow_up_actions"].extend([
                "Consider repeat Ishihara testing in 6-12 months",
                "Ophthalmology consultation if concerns persist"
            ])
            recommendations["patient_counseling"].extend([
                "Possible mild color vision difficulties detected",
                "Most daily activities should not be significantly affected"
            ])
            recommendations["occupational_considerations"].append(
                "May have limitations in color-critical occupations"
            )
            
        else:  # Color Vision Deficiency
            recommendations["follow_up_actions"].extend([
                "Ophthalmology referral for comprehensive color vision assessment",
                "Formal color vision testing (Farnsworth-Munsell 100 Hue test)",
                "Genetic counseling if family planning considerations"
            ])
            recommendations["patient_counseling"].extend([
                "Color vision deficiency likely present",
                "Condition is typically congenital and stable",
                "Adaptive strategies can help with daily activities",
                "Does not affect overall eye health or visual acuity"
            ])
            recommendations["occupational_considerations"].extend([
                "Limitations in color-critical occupations (pilots, electricians, some medical fields)",
                "Career counseling may be beneficial",
                "Reasonable accommodations often available"
            ])
        
        # Age-specific considerations
        if age < self.MIN_RELIABLE_AGE:
            recommendations["follow_up_actions"].append(
                "Repeat testing when child reaches 5-6 years of age"
            )
            recommendations["patient_counseling"].append(
                "Test may be less reliable in very young children"
            )
        
        # Visual acuity considerations
        if visual_acuity == "no":
            recommendations["follow_up_actions"].append(
                "Address visual acuity issues before repeat color vision testing"
            )
            recommendations["patient_counseling"].append(
                "Poor visual acuity may affect color vision test accuracy"
            )
        
        return recommendations
    
    def _get_test_limitations(self, visual_acuity, age) -> Dict[str, Any]:
        """Identifies test limitations and warnings"""
        
        limitations = {
            "general_limitations": [
                "Screening test only - not definitive diagnosis",
                "Primarily detects red-green color deficiencies",
                "Does not reliably detect blue-yellow (tritanomaly) defects",
                "Results may vary with lighting conditions and display calibration"
            ],
            "patient_specific_warnings": [],
            "test_reliability": "High"
        }
        
        # Age-related limitations
        if age < self.MIN_RELIABLE_AGE:
            limitations["patient_specific_warnings"].extend([
                "Test less reliable in children under 5 years",
                "Attention span and comprehension may affect results",
                "Consider repeat testing at older age"
            ])
            limitations["test_reliability"] = "Reduced"
        
        # Visual acuity limitations
        if visual_acuity == "no":
            limitations["patient_specific_warnings"].extend([
                "Test accuracy reduced with visual acuity below 20/100",
                "Refractive errors should be corrected before testing",
                "Consider formal ophthalmologic evaluation"
            ])
            limitations["test_reliability"] = "Reduced"
        
        return limitations


def calculate_color_vision_screening(
    correct_plates_right_eye: int,
    correct_plates_left_eye: int,
    visual_acuity_adequate: str,
    patient_age: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ColorVisionScreeningCalculator()
    return calculator.calculate(
        correct_plates_right_eye=correct_plates_right_eye,
        correct_plates_left_eye=correct_plates_left_eye,
        visual_acuity_adequate=visual_acuity_adequate,
        patient_age=patient_age
    )