"""
CHIP (CT in Head Injury Patients) Prediction Rule Calculator

Predicts need for CT imaging in patients with minor head trauma to detect 
potential intracranial injuries.

References:
1. Smits M, Dippel DW, Steyerberg EW, de Haan GG, Dekker HM, Vos PE, et al. 
   Predicting intracranial traumatic findings on computed tomography in patients 
   with minor head injury: the CHIP prediction rule. Ann Intern Med. 2007 Mar 
   6;146(6):397-405.
2. Smits M, Dippel DW, de Haan GG, Dekker HM, Vos PE, Kool DR, et al. External 
   validation of the Canadian CT Head Rule and the New Orleans Criteria for CT 
   scanning in patients with minor head injury. JAMA. 2005 Sep 28;294(12):1519-25.
3. van den Brand CL, Rambach AH, Postma K, et al. Update of the CHIP (CT in Head 
   Injury Patients) decision rule for patients with minor head injury based on a 
   multicenter consecutive case series. Emerg Med J. 2022 Dec;39(12):897-902.
"""

from typing import Dict, Any


class ChipPredictionRuleCalculator:
    """Calculator for CHIP (CT in Head Injury Patients) Prediction Rule"""
    
    def __init__(self):
        # Major criteria - any one present indicates CT recommended
        self.major_criteria = [
            "pedestrian_cyclist_vehicle",
            "ejected_from_vehicle", 
            "vomiting",
            "amnesia_4_hours_or_more",
            "clinical_skull_fracture",
            "gcs_less_than_15",
            "gcs_deterioration_2_points",
            "anticoagulant_use",
            "post_traumatic_seizure",
            "age_60_or_older"
        ]
        
        # Minor criteria - two or more present indicate CT recommended
        self.minor_criteria = [
            "fall_from_elevation",
            "anterograde_amnesia",
            "amnesia_2_to_4_hours",
            "skull_contusion",
            "neurologic_deficit",
            "loss_of_consciousness",
            "gcs_deterioration_1_point",
            "age_40_to_60"
        ]
        
        # Criteria descriptions for reporting
        self.criteria_descriptions = {
            "pedestrian_cyclist_vehicle": "Pedestrian or cyclist struck by vehicle",
            "ejected_from_vehicle": "Patient ejected from vehicle during accident",
            "vomiting": "Post-traumatic vomiting",
            "amnesia_4_hours_or_more": "Post-traumatic amnesia ≥4 hours",
            "clinical_skull_fracture": "Clinical signs of skull fracture",
            "gcs_less_than_15": "Glasgow Coma Scale <15",
            "gcs_deterioration_2_points": "GCS deterioration ≥2 points",
            "anticoagulant_use": "Current anticoagulant medication use",
            "post_traumatic_seizure": "Post-traumatic seizure",
            "age_60_or_older": "Age ≥60 years",
            "fall_from_elevation": "Fall from any elevation",
            "anterograde_amnesia": "Persistent anterograde amnesia",
            "amnesia_2_to_4_hours": "Post-traumatic amnesia 2 to <4 hours",
            "skull_contusion": "Skull contusion present",
            "neurologic_deficit": "Neurologic deficit present",
            "loss_of_consciousness": "Loss of consciousness",
            "gcs_deterioration_1_point": "GCS deterioration of 1 point",
            "age_40_to_60": "Age 40-60 years"
        }
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates CHIP prediction rule recommendation based on clinical criteria
        
        Args:
            **kwargs: All CHIP criteria parameters (yes/no for each)
            
        Returns:
            Dict with CT recommendation and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(kwargs)
        
        # Count major and minor criteria present
        major_criteria_present = []
        minor_criteria_present = []
        
        for criterion in self.major_criteria:
            if kwargs.get(criterion) == "yes":
                major_criteria_present.append(criterion)
        
        for criterion in self.minor_criteria:
            if kwargs.get(criterion) == "yes":
                minor_criteria_present.append(criterion)
        
        # Determine recommendation based on criteria
        recommendation_assessment = self._get_recommendation_assessment(
            major_criteria_present, minor_criteria_present
        )
        
        # Get detailed assessment breakdown
        assessment_breakdown = self._get_assessment_breakdown(
            major_criteria_present, minor_criteria_present, kwargs
        )
        
        return {
            "result": {
                "recommendation": recommendation_assessment["recommendation"],
                "risk_level": recommendation_assessment["risk_level"],
                "major_criteria_count": len(major_criteria_present),
                "minor_criteria_count": len(minor_criteria_present),
                "major_criteria_present": [self.criteria_descriptions[c] for c in major_criteria_present],
                "minor_criteria_present": [self.criteria_descriptions[c] for c in minor_criteria_present],
                "clinical_rationale": recommendation_assessment["rationale"],
                "assessment_breakdown": assessment_breakdown
            },
            "unit": "",
            "interpretation": recommendation_assessment["interpretation"],
            "stage": recommendation_assessment["recommendation"],
            "stage_description": recommendation_assessment["description"]
        }
    
    def _validate_inputs(self, kwargs):
        """Validates input parameters"""
        
        all_criteria = self.major_criteria + self.minor_criteria
        
        # Check that all required parameters are present
        for criterion in all_criteria:
            if criterion not in kwargs:
                raise ValueError(f"Missing required parameter: {criterion}")
            
            if kwargs[criterion] not in ["yes", "no"]:
                raise ValueError(f"{criterion} must be 'yes' or 'no'")
    
    def _get_recommendation_assessment(self, major_present, minor_present) -> Dict[str, Any]:
        """
        Determines CT recommendation based on CHIP criteria
        
        Args:
            major_present: List of major criteria present
            minor_present: List of minor criteria present
            
        Returns:
            Dict with recommendation and clinical guidance
        """
        
        major_count = len(major_present)
        minor_count = len(minor_present)
        
        if major_count > 0:
            # Any major criterion present = CT recommended
            recommendation = "CT Recommended"
            risk_level = "High Risk"
            description = "High risk for intracranial injury"
            rationale = f"One or more major criteria present ({major_count} major criteria met)"
            interpretation = f"CHIP Rule: CT RECOMMENDED. {major_count} major criterion(s) present indicating high risk for intracranial traumatic findings. Proceed with CT imaging to evaluate for potential neurosurgical lesions."
            
        elif minor_count >= 2:
            # Two or more minor criteria = CT recommended
            recommendation = "CT Recommended"
            risk_level = "Moderate to High Risk"
            description = "Moderate to high risk for intracranial injury"
            rationale = f"Two or more minor criteria present ({minor_count} minor criteria met)"
            interpretation = f"CHIP Rule: CT RECOMMENDED. {minor_count} minor criteria present indicating moderate to high risk for intracranial traumatic findings. Proceed with CT imaging for evaluation."
            
        elif minor_count == 1:
            # One minor criterion = clinical judgment
            recommendation = "Clinical Judgment"
            risk_level = "Low to Moderate Risk"
            description = "Low to moderate risk for intracranial injury"
            rationale = f"One minor criterion present ({minor_count} minor criteria met)"
            interpretation = f"CHIP Rule: CLINICAL JUDGMENT REQUIRED. {minor_count} minor criterion present. Consider CT imaging based on clinical assessment, patient factors, and physician judgment."
            
        else:
            # No criteria met = CT not indicated
            recommendation = "CT Not Indicated"
            risk_level = "Low Risk"
            description = "Low risk for intracranial injury"
            rationale = "No major or minor criteria present"
            interpretation = "CHIP Rule: CT NOT INDICATED. No major or minor criteria met indicating low risk for intracranial traumatic findings. Continue clinical observation and provide appropriate discharge instructions."
        
        return {
            "recommendation": recommendation,
            "risk_level": risk_level,
            "description": description,
            "rationale": rationale,
            "interpretation": interpretation
        }
    
    def _get_assessment_breakdown(self, major_present, minor_present, all_criteria):
        """Provides detailed assessment breakdown"""
        
        breakdown = {
            "criteria_analysis": {
                "major_criteria": {
                    "definition": "Any one major criterion present indicates CT recommended",
                    "count_present": len(major_present),
                    "criteria_met": [self.criteria_descriptions[c] for c in major_present],
                    "all_major_criteria": [self.criteria_descriptions[c] for c in self.major_criteria]
                },
                "minor_criteria": {
                    "definition": "Two or more minor criteria present indicate CT recommended",
                    "count_present": len(minor_present),
                    "criteria_met": [self.criteria_descriptions[c] for c in minor_present],
                    "all_minor_criteria": [self.criteria_descriptions[c] for c in self.minor_criteria]
                }
            },
            "decision_logic": {
                "ct_recommended_conditions": [
                    "Any one major criterion present",
                    "Two or more minor criteria present"
                ],
                "clinical_judgment_condition": "Exactly one minor criterion present",
                "ct_not_indicated_condition": "No major or minor criteria present"
            },
            "clinical_context": {
                "target_population": "Patients ≥16 years with minor head injury (GCS 13-15)",
                "timing": "Within 24 hours of blunt head trauma",
                "validation": "100% sensitivity for neurosurgical interventions in original study",
                "specificity": "23-30% specificity in original validation",
                "limitations": "Not validated for pediatric populations"
            },
            "evidence_base": {
                "original_study": "Smits et al. 2007 - Dutch multicenter study",
                "validation": "External validation in multiple studies",
                "performance": "High sensitivity for clinically important findings",
                "update": "Updated model published in 2022 with similar performance"
            }
        }
        
        return breakdown


def calculate_chip_prediction_rule(
    pedestrian_cyclist_vehicle: str,
    ejected_from_vehicle: str,
    vomiting: str,
    amnesia_4_hours_or_more: str,
    clinical_skull_fracture: str,
    gcs_less_than_15: str,
    gcs_deterioration_2_points: str,
    anticoagulant_use: str,
    post_traumatic_seizure: str,
    age_60_or_older: str,
    fall_from_elevation: str,
    anterograde_amnesia: str,
    amnesia_2_to_4_hours: str,
    skull_contusion: str,
    neurologic_deficit: str,
    loss_of_consciousness: str,
    gcs_deterioration_1_point: str,
    age_40_to_60: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ChipPredictionRuleCalculator()
    return calculator.calculate(
        pedestrian_cyclist_vehicle=pedestrian_cyclist_vehicle,
        ejected_from_vehicle=ejected_from_vehicle,
        vomiting=vomiting,
        amnesia_4_hours_or_more=amnesia_4_hours_or_more,
        clinical_skull_fracture=clinical_skull_fracture,
        gcs_less_than_15=gcs_less_than_15,
        gcs_deterioration_2_points=gcs_deterioration_2_points,
        anticoagulant_use=anticoagulant_use,
        post_traumatic_seizure=post_traumatic_seizure,
        age_60_or_older=age_60_or_older,
        fall_from_elevation=fall_from_elevation,
        anterograde_amnesia=anterograde_amnesia,
        amnesia_2_to_4_hours=amnesia_2_to_4_hours,
        skull_contusion=skull_contusion,
        neurologic_deficit=neurologic_deficit,
        loss_of_consciousness=loss_of_consciousness,
        gcs_deterioration_1_point=gcs_deterioration_1_point,
        age_40_to_60=age_40_to_60
    )