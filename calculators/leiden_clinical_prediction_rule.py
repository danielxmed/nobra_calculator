"""
Leiden Clinical Prediction Rule for Undifferentiated Arthritis Calculator

Calculates the likelihood of progression from undifferentiated arthritis to rheumatoid arthritis
using clinical variables including age, sex, joint distribution, morning stiffness, joint counts,
inflammatory markers, and autoantibody status. Helps guide early treatment decisions with DMARDs.

References:
1. van der Helm-van Mil AHM, le Cessie S, van Dongen H, Breedveld FC, Toes REM, Huizinga TWJ. 
   A prediction rule for disease outcome in patients with recent-onset undifferentiated arthritis: 
   how to guide individual treatment decisions. Arthritis Rheum. 2007 Feb;56(2):433-40.
2. Kuriya B, Cheng CK, Chen HM, Bykerk VP. Validation of a prediction rule for development of 
   rheumatoid arthritis in patients with early undifferentiated arthritis. Ann Rheum Dis. 2009 Sep;68(9):1482-5.
"""

from typing import Dict, Any


class LeidenClinicalPredictionRuleCalculator:
    """Calculator for Leiden Clinical Prediction Rule for Undifferentiated Arthritis"""
    
    def __init__(self):
        """Initialize scoring thresholds and point values"""
        
        # Risk interpretation thresholds
        self.low_risk_threshold = 6.0
        self.high_risk_threshold = 8.0
        
        # Age coefficient
        self.age_coefficient = 0.02
        
        # Scoring points for categorical variables
        self.sex_points = {
            "male": 0,
            "female": 1
        }
        
        self.joint_distribution_points = {
            "other": 0,
            "small_hands_feet": 0.5,
            "upper_extremities_only": 1,
            "upper_and_lower_extremities": 1.5
        }
        
        self.symmetric_distribution_points = {
            "no": 0,
            "yes": 0.5
        }
        
        self.morning_stiffness_points = {
            "less_than_30_min": 0,
            "30_to_59_min": 0.5,
            "60_min_or_more": 1
        }
        
        self.rheumatoid_factor_points = {
            "negative": 0,
            "positive": 1
        }
        
        self.anti_ccp_points = {
            "negative": 0,
            "positive": 2
        }
    
    def calculate(self, age_years: int, sex: str, joint_distribution: str, 
                 symmetric_distribution: str, morning_stiffness_duration: str,
                 tender_joints_count: int, swollen_joints_count: int,
                 c_reactive_protein: float, rheumatoid_factor: str,
                 anti_ccp_antibodies: str) -> Dict[str, Any]:
        """
        Calculates the Leiden Clinical Prediction Rule score
        
        Args:
            age_years (int): Patient age in years
            sex (str): Patient sex ("male" or "female")
            joint_distribution (str): Distribution pattern of affected joints
            symmetric_distribution (str): Whether joint involvement is symmetric
            morning_stiffness_duration (str): Duration of morning stiffness
            tender_joints_count (int): Number of tender joints (0-68)
            swollen_joints_count (int): Number of swollen joints (0-66)
            c_reactive_protein (float): C-reactive protein level in mg/L
            rheumatoid_factor (str): Rheumatoid factor status
            anti_ccp_antibodies (str): Anti-CCP antibody status
            
        Returns:
            Dict with the calculated score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_years, sex, joint_distribution, symmetric_distribution,
            morning_stiffness_duration, tender_joints_count, swollen_joints_count,
            c_reactive_protein, rheumatoid_factor, anti_ccp_antibodies
        )
        
        # Calculate score components
        age_score = self._calculate_age_score(age_years)
        sex_score = self._calculate_sex_score(sex)
        joint_dist_score = self._calculate_joint_distribution_score(joint_distribution)
        symmetric_score = self._calculate_symmetric_distribution_score(symmetric_distribution)
        stiffness_score = self._calculate_morning_stiffness_score(morning_stiffness_duration)
        tender_joints_score = self._calculate_tender_joints_score(tender_joints_count)
        swollen_joints_score = self._calculate_swollen_joints_score(swollen_joints_count)
        crp_score = self._calculate_crp_score(c_reactive_protein)
        rf_score = self._calculate_rf_score(rheumatoid_factor)
        anti_ccp_score = self._calculate_anti_ccp_score(anti_ccp_antibodies)
        
        # Calculate total score
        total_score = (
            age_score + sex_score + joint_dist_score + symmetric_score +
            stiffness_score + tender_joints_score + swollen_joints_score +
            crp_score + rf_score + anti_ccp_score
        )
        
        # Round to one decimal place
        total_score = round(total_score, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Generate detailed interpretation
        detailed_interpretation = self._generate_detailed_interpretation(
            total_score, interpretation, age_years, sex, joint_distribution,
            symmetric_distribution, morning_stiffness_duration, tender_joints_count,
            swollen_joints_count, c_reactive_protein, rheumatoid_factor, anti_ccp_antibodies
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": detailed_interpretation,
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_years, sex, joint_distribution, symmetric_distribution,
                        morning_stiffness_duration, tender_joints_count, swollen_joints_count,
                        c_reactive_protein, rheumatoid_factor, anti_ccp_antibodies):
        """Validates input parameters"""
        
        if not isinstance(age_years, int) or age_years < 18 or age_years > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if sex not in self.sex_points:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if joint_distribution not in self.joint_distribution_points:
            raise ValueError("Joint distribution must be one of: other, small_hands_feet, upper_extremities_only, upper_and_lower_extremities")
        
        if symmetric_distribution not in self.symmetric_distribution_points:
            raise ValueError("Symmetric distribution must be 'yes' or 'no'")
        
        if morning_stiffness_duration not in self.morning_stiffness_points:
            raise ValueError("Morning stiffness duration must be one of: less_than_30_min, 30_to_59_min, 60_min_or_more")
        
        if not isinstance(tender_joints_count, int) or tender_joints_count < 0 or tender_joints_count > 68:
            raise ValueError("Tender joints count must be an integer between 0 and 68")
        
        if not isinstance(swollen_joints_count, int) or swollen_joints_count < 0 or swollen_joints_count > 66:
            raise ValueError("Swollen joints count must be an integer between 0 and 66")
        
        if not isinstance(c_reactive_protein, (int, float)) or c_reactive_protein < 0:
            raise ValueError("C-reactive protein must be a non-negative number")
        
        if rheumatoid_factor not in self.rheumatoid_factor_points:
            raise ValueError("Rheumatoid factor must be 'positive' or 'negative'")
        
        if anti_ccp_antibodies not in self.anti_ccp_points:
            raise ValueError("Anti-CCP antibodies must be 'positive' or 'negative'")
    
    def _calculate_age_score(self, age_years: int) -> float:
        """Calculates age component score"""
        return age_years * self.age_coefficient
    
    def _calculate_sex_score(self, sex: str) -> float:
        """Calculates sex component score"""
        return self.sex_points[sex]
    
    def _calculate_joint_distribution_score(self, joint_distribution: str) -> float:
        """Calculates joint distribution component score"""
        return self.joint_distribution_points[joint_distribution]
    
    def _calculate_symmetric_distribution_score(self, symmetric_distribution: str) -> float:
        """Calculates symmetric distribution component score"""
        return self.symmetric_distribution_points[symmetric_distribution]
    
    def _calculate_morning_stiffness_score(self, morning_stiffness_duration: str) -> float:
        """Calculates morning stiffness component score"""
        return self.morning_stiffness_points[morning_stiffness_duration]
    
    def _calculate_tender_joints_score(self, tender_joints_count: int) -> float:
        """Calculates tender joints component score"""
        if tender_joints_count < 4:
            return 0
        elif tender_joints_count <= 10:
            return 0.5
        else:  # tender_joints_count >= 11
            return 1
    
    def _calculate_swollen_joints_score(self, swollen_joints_count: int) -> float:
        """Calculates swollen joints component score"""
        if swollen_joints_count < 4:
            return 0
        elif swollen_joints_count <= 10:
            return 0.5
        else:  # swollen_joints_count >= 11
            return 1
    
    def _calculate_crp_score(self, c_reactive_protein: float) -> float:
        """Calculates C-reactive protein component score"""
        if c_reactive_protein < 5:
            return 0
        elif c_reactive_protein <= 50:
            return 0.5
        else:  # c_reactive_protein >= 51
            return 1.5
    
    def _calculate_rf_score(self, rheumatoid_factor: str) -> float:
        """Calculates rheumatoid factor component score"""
        return self.rheumatoid_factor_points[rheumatoid_factor]
    
    def _calculate_anti_ccp_score(self, anti_ccp_antibodies: str) -> float:
        """Calculates anti-CCP antibodies component score"""
        return self.anti_ccp_points[anti_ccp_antibodies]
    
    def _get_interpretation(self, total_score: float) -> Dict[str, str]:
        """
        Interprets the Leiden Clinical Prediction Rule score
        
        Args:
            total_score (float): Calculated total score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= self.low_risk_threshold:
            return {
                "stage": "Low Risk",
                "description": "Low risk of progression to rheumatoid arthritis",
                "risk_category": "Low"
            }
        elif total_score < self.high_risk_threshold:
            return {
                "stage": "Indeterminate Risk",
                "description": "Indeterminate risk of progression to rheumatoid arthritis",
                "risk_category": "Intermediate"
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk of progression to rheumatoid arthritis",
                "risk_category": "High"
            }
    
    def _generate_detailed_interpretation(self, total_score, interpretation, age_years, sex,
                                        joint_distribution, symmetric_distribution,
                                        morning_stiffness_duration, tender_joints_count,
                                        swollen_joints_count, c_reactive_protein,
                                        rheumatoid_factor, anti_ccp_antibodies) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Returns:
            str: Detailed clinical interpretation and recommendations
        """
        
        # Base interpretation
        base_interpretation = (
            f"Leiden Clinical Prediction Rule score: {total_score} points. "
            f"Risk category: {interpretation['stage']}. "
        )
        
        # Risk-specific recommendations
        if total_score <= self.low_risk_threshold:
            recommendations = (
                "Low likelihood of progression from undifferentiated arthritis to rheumatoid arthritis within one year. "
                "Conservative management with watchful waiting may be appropriate. Regular follow-up recommended "
                "to monitor for disease progression. Consider reassessment in 3-6 months or if symptoms worsen."
            )
        elif total_score < self.high_risk_threshold:
            recommendations = (
                "Intermediate likelihood of progression to rheumatoid arthritis. Clinical judgment and additional "
                "factors should guide treatment decisions. Consider close monitoring with serial assessments. "
                "Early intervention may be considered depending on patient characteristics, symptom severity, "
                "and clinical presentation. Rheumatology consultation recommended."
            )
        else:
            recommendations = (
                "High likelihood of progression from undifferentiated arthritis to rheumatoid arthritis within one year. "
                "Early initiation of disease-modifying antirheumatic drugs (DMARDs) should be strongly considered "
                "to prevent joint damage and disability. Urgent rheumatology consultation recommended for treatment planning."
            )
        
        # Key contributing factors
        risk_factors = []
        if age_years > 50:
            risk_factors.append("older age")
        if sex == "female":
            risk_factors.append("female sex")
        if joint_distribution in ["small_hands_feet", "upper_and_lower_extremities"]:
            risk_factors.append("typical joint distribution pattern")
        if symmetric_distribution == "yes":
            risk_factors.append("symmetric joint involvement")
        if morning_stiffness_duration == "60_min_or_more":
            risk_factors.append("prolonged morning stiffness")
        if tender_joints_count >= 11 or swollen_joints_count >= 11:
            risk_factors.append("multiple affected joints")
        if c_reactive_protein >= 5:
            risk_factors.append("elevated inflammatory markers")
        if rheumatoid_factor == "positive":
            risk_factors.append("positive rheumatoid factor")
        if anti_ccp_antibodies == "positive":
            risk_factors.append("positive anti-CCP antibodies")
        
        factor_summary = ""
        if risk_factors:
            factor_summary = f" Key contributing factors include: {', '.join(risk_factors)}."
        
        # Clinical context
        clinical_context = (
            " This prediction rule is designed for adults with recent-onset undifferentiated arthritis "
            "(symptom duration typically <6 months) to guide early treatment decisions. "
            "The tool should be used in conjunction with comprehensive clinical assessment and "
            "is not intended to replace rheumatological evaluation."
        )
        
        return base_interpretation + recommendations + factor_summary + clinical_context


def calculate_leiden_clinical_prediction_rule(age_years, sex, joint_distribution,
                                            symmetric_distribution, morning_stiffness_duration,
                                            tender_joints_count, swollen_joints_count,
                                            c_reactive_protein, rheumatoid_factor,
                                            anti_ccp_antibodies) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = LeidenClinicalPredictionRuleCalculator()
    return calculator.calculate(
        age_years, sex, joint_distribution, symmetric_distribution,
        morning_stiffness_duration, tender_joints_count, swollen_joints_count,
        c_reactive_protein, rheumatoid_factor, anti_ccp_antibodies
    )