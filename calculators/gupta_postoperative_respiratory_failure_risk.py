"""
Gupta Postoperative Respiratory Failure Risk Calculator

The Gupta Postoperative Respiratory Failure Risk calculator predicts the risk of 
mechanical ventilation for >48 hours after surgery or unplanned intubation within 
30 days of surgery. This validated tool was developed using the American College of 
Surgeons' National Surgical Quality Improvement Program (ACS NSQIP) data and 
demonstrates excellent predictive accuracy.

The calculator helps clinicians identify patients at increased risk of postoperative 
respiratory failure, enabling implementation of targeted prevention strategies, 
appropriate level of care planning, and informed consent discussions.

Clinical Applications:
- Preoperative risk stratification for respiratory failure prevention
- Patient counseling and informed consent discussions
- Decision-making for ICU admission and enhanced monitoring
- Identification of patients requiring pulmonology consultation
- Postoperative care planning and resource allocation

References (Vancouver style):
1. Gupta H, Gupta PK, Fang X, et al. Development and validation of a risk calculator 
   predicting postoperative respiratory failure. Chest. 2011;140(5):1207-1215. 
   doi: 10.1378/chest.11-0466
2. American College of Surgeons National Surgical Quality Improvement Program. 
   ACS NSQIP Risk Calculator. https://riskcalculator.facs.org/
3. Canet J, Gallart L, Gomar C, et al. Prediction of postoperative pulmonary 
   complications in a population-based surgical cohort. Anesthesiology. 
   2010;113(6):1338-1350.
"""

import math
from typing import Dict, Any


class GuptaPostoperativeRespiratoryFailureRiskCalculator:
    """Calculator for Gupta Postoperative Respiratory Failure Risk"""
    
    def __init__(self):
        # Functional status points
        self.FUNCTIONAL_STATUS_POINTS = {
            "independent": 0.0,
            "partially_dependent": 0.7678,
            "totally_dependent": 1.4046
        }
        
        # ASA class points
        self.ASA_CLASS_POINTS = {
            "1": -3.5265,  # Normal healthy patient
            "2": -2.0008,  # Mild systemic disease
            "3": -0.6201,  # Severe systemic disease
            "4": 0.2441,   # Severe systemic disease threatening life
            "5": 0.0       # Moribund patient
        }
        
        # Sepsis status points
        self.SEPSIS_POINTS = {
            "none": -0.7840,        # No sepsis
            "sirs": 0.0,            # Preoperative SIRS (reference)
            "sepsis": 0.2752,       # Preoperative sepsis
            "septic_shock": 0.9035  # Preoperative septic shock
        }
        
        # Emergency case points
        self.EMERGENCY_POINTS = {
            "no": -0.5739,
            "yes": 0.0
        }
        
        # Procedure type points (from highest to lowest risk)
        self.PROCEDURE_TYPE_POINTS = {
            "aortic": 1.0781,
            "brain": 0.8086,
            "thoracic_non_cardiac": 0.7737,
            "cardiac": 0.6959,
            "foregut_hepatobiliary": 0.4949,
            "peripheral_vascular": 0.3646,
            "neck": 0.2701,
            "gallbladder_appendix_adrenals_spleen": 0.2135,
            "intestinal": 0.1964,
            "renal": 0.1460,
            "spine": 0.1139,
            "orthopedic_non_spine": 0.0654,
            "other_abdomen": 0.0481,
            "urology_non_renal": 0.0089,
            "hernia": 0.0,  # Reference category
            "gynecologic_oncology": -0.0234,
            "obstetric_gynecologic": -0.1456,
            "other_hematologic": -0.2341,
            "skin": -0.3678,
            "thyroid_parathyroid": -0.4927,
            "vein": -0.8934,
            "breast": -2.6462
        }
        
        # Base constant for logistic regression
        self.BASE_CONSTANT = -1.7397
        
        # Risk interpretation thresholds
        self.RISK_THRESHOLDS = [
            {"min": 0.0, "max": 1.0, "level": "Very Low Risk", "description": "Minimal respiratory failure risk"},
            {"min": 1.0, "max": 3.0, "level": "Low Risk", "description": "Low respiratory failure risk"},
            {"min": 3.0, "max": 8.0, "level": "Moderate Risk", "description": "Moderate respiratory failure risk"},
            {"min": 8.0, "max": 20.0, "level": "High Risk", "description": "High respiratory failure risk"},
            {"min": 20.0, "max": 100.0, "level": "Very High Risk", "description": "Very high respiratory failure risk"}
        ]
    
    def calculate(self, functional_status: str, asa_class: str, sepsis_status: str,
                 emergency_case: str, procedure_type: str) -> Dict[str, Any]:
        """
        Calculates Gupta Postoperative Respiratory Failure Risk
        
        Args:
            functional_status (str): Functional status (independent, partially_dependent, totally_dependent)
            asa_class (str): ASA Physical Status Classification (1-5)
            sepsis_status (str): Preoperative sepsis status (none, sirs, sepsis, septic_shock)
            emergency_case (str): Emergency surgical case (no, yes)
            procedure_type (str): Type of surgical procedure
            
        Returns:
            Dict with respiratory failure risk percentage and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(functional_status, asa_class, sepsis_status, 
                            emergency_case, procedure_type)
        
        # Calculate risk score components
        functional_points = self.FUNCTIONAL_STATUS_POINTS[functional_status]
        asa_points = self.ASA_CLASS_POINTS[asa_class]
        sepsis_points = self.SEPSIS_POINTS[sepsis_status]
        emergency_points = self.EMERGENCY_POINTS[emergency_case]
        procedure_points = self.PROCEDURE_TYPE_POINTS[procedure_type]
        
        # Calculate logistic regression score (x)
        x = (self.BASE_CONSTANT + functional_points + asa_points + 
             sepsis_points + emergency_points + procedure_points)
        
        # Calculate risk percentage using logistic function
        # Risk = e^x / (1 + e^x) * 100
        try:
            exp_x = math.exp(x)
            risk_percentage = (exp_x / (1 + exp_x)) * 100
        except OverflowError:
            # Handle overflow for very high scores
            risk_percentage = 100.0 if x > 0 else 0.0
        
        # Get risk interpretation
        interpretation = self._get_interpretation(risk_percentage, functional_status, asa_class,
                                                sepsis_status, emergency_case, procedure_type)
        
        return {
            "result": round(risk_percentage, 2),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["level"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, functional_status: str, asa_class: str, sepsis_status: str,
                        emergency_case: str, procedure_type: str):
        """Validates input parameters"""
        
        if functional_status not in self.FUNCTIONAL_STATUS_POINTS:
            raise ValueError(f"Functional status must be one of: {list(self.FUNCTIONAL_STATUS_POINTS.keys())}")
        
        if asa_class not in self.ASA_CLASS_POINTS:
            raise ValueError(f"ASA class must be one of: {list(self.ASA_CLASS_POINTS.keys())}")
        
        if sepsis_status not in self.SEPSIS_POINTS:
            raise ValueError(f"Sepsis status must be one of: {list(self.SEPSIS_POINTS.keys())}")
        
        if emergency_case not in self.EMERGENCY_POINTS:
            raise ValueError(f"Emergency case must be one of: {list(self.EMERGENCY_POINTS.keys())}")
        
        if procedure_type not in self.PROCEDURE_TYPE_POINTS:
            raise ValueError(f"Procedure type must be one of: {list(self.PROCEDURE_TYPE_POINTS.keys())}")
    
    def _get_interpretation(self, risk_percentage: float, functional_status: str, 
                          asa_class: str, sepsis_status: str, emergency_case: str,
                          procedure_type: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on respiratory failure risk percentage
        
        Returns:
            Dict with risk level, description, and clinical recommendations
        """
        
        # Find appropriate risk category
        risk_category = None
        for threshold in self.RISK_THRESHOLDS:
            if threshold["min"] <= risk_percentage < threshold["max"]:
                risk_category = threshold
                break
        
        # Handle edge case for maximum risk
        if risk_category is None and risk_percentage >= 20.0:
            risk_category = self.RISK_THRESHOLDS[-1]
        elif risk_category is None:
            risk_category = self.RISK_THRESHOLDS[0]
        
        # Build parameter summary
        functional_descriptions = {
            "independent": "functionally independent",
            "partially_dependent": "partially dependent",
            "totally_dependent": "totally dependent"
        }
        
        asa_descriptions = {
            "1": "ASA Class I (normal healthy)",
            "2": "ASA Class II (mild systemic disease)",
            "3": "ASA Class III (severe systemic disease)",
            "4": "ASA Class IV (severe systemic disease threatening life)",
            "5": "ASA Class V (moribund patient)"
        }
        
        sepsis_descriptions = {
            "none": "no sepsis",
            "sirs": "preoperative SIRS",
            "sepsis": "preoperative sepsis",
            "septic_shock": "preoperative septic shock"
        }
        
        emergency_desc = "emergency case" if emergency_case == "yes" else "elective case"
        procedure_desc = procedure_type.replace("_", " ")
        
        parameter_summary = (
            f"Patient characteristics: {functional_descriptions[functional_status]}, "
            f"{asa_descriptions[asa_class]}, {sepsis_descriptions[sepsis_status]}, "
            f"{emergency_desc}, undergoing {procedure_desc}. "
        )
        
        # Generate risk-specific recommendations
        if risk_percentage < 1.0:  # Very Low Risk
            recommendations = (
                "Very low risk of postoperative respiratory failure. Standard perioperative care "
                "and monitoring are appropriate. Continue routine respiratory care including early "
                "mobilization, adequate pain management, and standard postoperative protocols. "
                "No additional respiratory interventions typically required."
            )
        elif risk_percentage < 3.0:  # Low Risk
            recommendations = (
                "Low risk of postoperative respiratory failure. Standard care with attention to "
                "respiratory status and pain management. Ensure adequate pain control to facilitate "
                "deep breathing and coughing. Monitor for signs of respiratory complications and "
                "implement standard pulmonary hygiene measures."
            )
        elif risk_percentage < 8.0:  # Moderate Risk
            recommendations = (
                "Moderate risk of postoperative respiratory failure. Consider enhanced respiratory "
                "monitoring and pulmonary care protocols. Implement aggressive pulmonary hygiene, "
                "incentive spirometry, and consider respiratory therapy consultation. Monitor closely "
                "for early signs of respiratory compromise."
            )
        elif risk_percentage < 20.0:  # High Risk
            recommendations = (
                "High risk of postoperative respiratory failure. Implement intensive respiratory "
                "monitoring and consider ICU-level care. Strong consideration for pulmonology "
                "consultation, mechanical ventilation readiness, and enhanced postoperative "
                "surveillance. Consider preoperative optimization if elective case."
            )
        else:  # Very High Risk
            recommendations = (
                "Very high risk of postoperative respiratory failure. Consider postponing elective "
                "surgery for preoperative optimization. ICU-level monitoring and care required. "
                "Mechanical ventilation should be readily available. Multidisciplinary team approach "
                "with pulmonology, anesthesia, and critical care involvement essential."
            )
        
        # Add important clinical considerations
        clinical_considerations = (
            "Important considerations: This calculator predicts postoperative respiratory failure "
            "risk (mechanical ventilation >48 hours or unplanned intubation ≤30 days). Respiratory "
            "failure is associated with significantly increased 30-day mortality (25.62% vs 0.98%). "
            "Use in conjunction with clinical judgment for surgical decision-making and care planning. "
            "Consider individual patient factors such as pulmonary function tests, recent respiratory "
            "infections, and surgical urgency when making final management decisions."
        )
        
        # Build comprehensive interpretation
        interpretation = (
            f"{parameter_summary}Gupta Postoperative Respiratory Failure Risk: {risk_percentage:.2f}% "
            f"risk of respiratory failure requiring mechanical ventilation >48 hours or unplanned "
            f"intubation within 30 days. Risk Category: {risk_category['level']} "
            f"({risk_category['description']}). Clinical recommendations: {recommendations} "
            f"{clinical_considerations}"
        )
        
        return {
            "level": risk_category["level"],
            "description": risk_category["description"], 
            "interpretation": interpretation
        }


def calculate_gupta_postoperative_respiratory_failure_risk(functional_status: str, asa_class: str, 
                                                         sepsis_status: str, emergency_case: str, 
                                                         procedure_type: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gupta_postoperative_respiratory_failure_risk pattern
    """
    calculator = GuptaPostoperativeRespiratoryFailureRiskCalculator()
    return calculator.calculate(functional_status, asa_class, sepsis_status, 
                              emergency_case, procedure_type)