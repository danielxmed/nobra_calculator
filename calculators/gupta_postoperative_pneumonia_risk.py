"""
Gupta Postoperative Pneumonia Risk Calculator

The Gupta Postoperative Pneumonia Risk calculator predicts the risk of pneumonia 
after surgery based on seven validated preoperative risk factors. This tool was 
developed using the American College of Surgeons' National Surgical Quality 
Improvement Program (ACS NSQIP) data and demonstrates excellent predictive accuracy.

The calculator helps clinicians identify patients at increased risk of postoperative 
pneumonia, enabling implementation of targeted prevention strategies and informed 
consent discussions.

Clinical Applications:
- Preoperative risk stratification for pneumonia prevention
- Patient counseling and informed consent discussions
- Decision-making for enhanced pulmonary care protocols
- Identification of patients requiring pulmonology consultation
- Postoperative care planning and resource allocation

References (Vancouver style):
1. Gupta H, Gupta PK, Fang X, et al. Development and validation of a risk calculator 
   for predicting postoperative pneumonia. Mayo Clin Proc. 2013;88(11):1241-1249. 
   doi: 10.1016/j.mayocp.2013.06.027
2. American College of Surgeons National Surgical Quality Improvement Program. 
   ACS NSQIP Risk Calculator. https://riskcalculator.facs.org/
3. Smetana GW, Lawrence VA, Cornell JE. American College of Physicians. Preoperative 
   pulmonary risk stratification for noncardiothoracic surgery: systematic review for 
   the American College of Physicians. Ann Intern Med. 2006;144(8):581-595.
"""

import math
from typing import Dict, Any


class GuptaPostoperativePneumoniaRiskCalculator:
    """Calculator for Gupta Postoperative Pneumonia Risk"""
    
    def __init__(self):
        # Age coefficient (points per year)
        self.AGE_COEFFICIENT = 0.0144
        
        # COPD points
        self.COPD_POINTS = {
            "no": -0.4553,
            "yes": 0.0
        }
        
        # Functional status points
        self.FUNCTIONAL_STATUS_POINTS = {
            "independent": 0.0,
            "partially_dependent": 0.7653,
            "totally_dependent": 0.9400
        }
        
        # ASA class points
        self.ASA_CLASS_POINTS = {
            "1": -3.0225,  # Normal healthy patient
            "2": -1.6057,  # Mild systemic disease
            "3": -0.4915,  # Severe systemic disease
            "4": 0.0123,   # Severe systemic disease threatening life
            "5": 0.0       # Moribund patient
        }
        
        # Sepsis status points
        self.SEPSIS_POINTS = {
            "none": -0.7641,        # No sepsis
            "sirs": 0.0,            # Preoperative SIRS
            "sepsis": -0.0842,      # Preoperative sepsis
            "septic_shock": 0.1048  # Preoperative septic shock
        }
        
        # Smoking points
        self.SMOKING_POINTS = {
            "no": -0.4306,
            "yes": 0.0
        }
        
        # Procedure type points (from highest to lowest risk)
        self.PROCEDURE_TYPE_POINTS = {
            "aortic": 0.7178,
            "brain": 0.6405,
            "cardiac": 0.4492,
            "thoracic_non_cardiac": 0.2806,
            "neck": 0.1633,
            "peripheral_vascular": 0.1382,
            "foregut_hepatobiliary": 0.1239,
            "gallbladder_appendix_adrenals_spleen": 0.0823,
            "intestinal": 0.0645,
            "orthopedic_non_spine": 0.0189,
            "renal": -0.0234,
            "spine": -0.0689,
            "urology_non_renal": -0.1347,
            "hernia": -0.1456,
            "obstetric_gynecologic": -0.1789,
            "skin": -0.3254,
            "thyroid_parathyroid": -0.5632,
            "vein": -0.8945,
            "breast": -2.3318
        }
        
        # Base constant for logistic regression
        self.BASE_CONSTANT = -2.8977
        
        # Risk interpretation thresholds
        self.RISK_THRESHOLDS = [
            {"min": 0.0, "max": 1.0, "level": "Very Low Risk", "description": "Minimal pneumonia risk"},
            {"min": 1.0, "max": 3.0, "level": "Low Risk", "description": "Low pneumonia risk"},
            {"min": 3.0, "max": 6.0, "level": "Moderate Risk", "description": "Moderate pneumonia risk"},
            {"min": 6.0, "max": 15.0, "level": "High Risk", "description": "High pneumonia risk"},
            {"min": 15.0, "max": 100.0, "level": "Very High Risk", "description": "Very high pneumonia risk"}
        ]
    
    def calculate(self, age: int, copd: str, functional_status: str, asa_class: str,
                 sepsis_status: str, smoking: str, procedure_type: str) -> Dict[str, Any]:
        """
        Calculates Gupta Postoperative Pneumonia Risk
        
        Args:
            age (int): Patient age in years
            copd (str): Presence of COPD (no, yes)
            functional_status (str): Functional status (independent, partially_dependent, totally_dependent)
            asa_class (str): ASA Physical Status Classification (1-5)
            sepsis_status (str): Preoperative sepsis status (none, sirs, sepsis, septic_shock)
            smoking (str): Smoking within last year (no, yes)
            procedure_type (str): Type of surgical procedure
            
        Returns:
            Dict with pneumonia risk percentage and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, copd, functional_status, asa_class, 
                            sepsis_status, smoking, procedure_type)
        
        # Calculate risk score components
        age_points = age * self.AGE_COEFFICIENT
        copd_points = self.COPD_POINTS[copd]
        functional_points = self.FUNCTIONAL_STATUS_POINTS[functional_status]
        asa_points = self.ASA_CLASS_POINTS[asa_class]
        sepsis_points = self.SEPSIS_POINTS[sepsis_status]
        smoking_points = self.SMOKING_POINTS[smoking]
        procedure_points = self.PROCEDURE_TYPE_POINTS[procedure_type]
        
        # Calculate logistic regression score (x)
        x = (self.BASE_CONSTANT + age_points + copd_points + functional_points + 
             asa_points + sepsis_points + smoking_points + procedure_points)
        
        # Calculate risk percentage using logistic function
        # Risk = e^x / (1 + e^x) * 100
        try:
            exp_x = math.exp(x)
            risk_percentage = (exp_x / (1 + exp_x)) * 100
        except OverflowError:
            # Handle overflow for very high scores
            risk_percentage = 100.0 if x > 0 else 0.0
        
        # Get risk interpretation
        interpretation = self._get_interpretation(risk_percentage, age, copd, functional_status,
                                                asa_class, sepsis_status, smoking, procedure_type)
        
        return {
            "result": round(risk_percentage, 2),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["level"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, copd: str, functional_status: str, 
                        asa_class: str, sepsis_status: str, smoking: str, procedure_type: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if copd not in self.COPD_POINTS:
            raise ValueError(f"COPD must be one of: {list(self.COPD_POINTS.keys())}")
        
        if functional_status not in self.FUNCTIONAL_STATUS_POINTS:
            raise ValueError(f"Functional status must be one of: {list(self.FUNCTIONAL_STATUS_POINTS.keys())}")
        
        if asa_class not in self.ASA_CLASS_POINTS:
            raise ValueError(f"ASA class must be one of: {list(self.ASA_CLASS_POINTS.keys())}")
        
        if sepsis_status not in self.SEPSIS_POINTS:
            raise ValueError(f"Sepsis status must be one of: {list(self.SEPSIS_POINTS.keys())}")
        
        if smoking not in self.SMOKING_POINTS:
            raise ValueError(f"Smoking must be one of: {list(self.SMOKING_POINTS.keys())}")
        
        if procedure_type not in self.PROCEDURE_TYPE_POINTS:
            raise ValueError(f"Procedure type must be one of: {list(self.PROCEDURE_TYPE_POINTS.keys())}")
    
    def _get_interpretation(self, risk_percentage: float, age: int, copd: str, 
                          functional_status: str, asa_class: str, sepsis_status: str,
                          smoking: str, procedure_type: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on pneumonia risk percentage
        
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
        if risk_category is None and risk_percentage >= 15.0:
            risk_category = self.RISK_THRESHOLDS[-1]
        elif risk_category is None:
            risk_category = self.RISK_THRESHOLDS[0]
        
        # Build parameter summary
        copd_desc = "COPD present" if copd == "yes" else "no COPD"
        
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
        
        smoking_desc = "current smoker" if smoking == "yes" else "non-smoker"
        procedure_desc = procedure_type.replace("_", " ")
        
        parameter_summary = (
            f"Patient characteristics: {age} years old, {copd_desc}, {functional_descriptions[functional_status]}, "
            f"{asa_descriptions[asa_class]}, {sepsis_descriptions[sepsis_status]}, {smoking_desc}, "
            f"undergoing {procedure_desc}. "
        )
        
        # Generate risk-specific recommendations
        if risk_percentage < 1.0:  # Very Low Risk
            recommendations = (
                "Very low risk of postoperative pneumonia. Standard perioperative care and monitoring "
                "are appropriate. Continue routine pulmonary hygiene measures, early mobilization, and "
                "standard pain management protocols. No additional pneumonia prevention interventions required."
            )
        elif risk_percentage < 3.0:  # Low Risk
            recommendations = (
                "Low risk of postoperative pneumonia. Standard care with attention to pulmonary hygiene "
                "and early mobilization. Consider incentive spirometry, deep breathing exercises, and "
                "adequate pain control to facilitate coughing and ambulation."
            )
        elif risk_percentage < 6.0:  # Moderate Risk
            recommendations = (
                "Moderate risk of postoperative pneumonia. Consider enhanced pulmonary care including "
                "chest physiotherapy, aggressive incentive spirometry, early mobilization protocols, "
                "and closer respiratory monitoring. Optimize pain management to facilitate pulmonary hygiene."
            )
        elif risk_percentage < 15.0:  # High Risk
            recommendations = (
                "High risk of postoperative pneumonia. Implement aggressive pneumonia prevention strategies "
                "including preoperative pulmonary rehabilitation if feasible, postoperative chest physiotherapy, "
                "respiratory therapy consultation, and consider pulmonology evaluation for high-risk patients."
            )
        else:  # Very High Risk
            recommendations = (
                "Very high risk of postoperative pneumonia. Consider postponing elective surgery for "
                "preoperative optimization including pulmonary rehabilitation, smoking cessation, treatment "
                "of respiratory infections. Implement intensive pneumonia prevention protocols and consider "
                "ICU-level monitoring postoperatively."
            )
        
        # Add important clinical considerations
        clinical_considerations = (
            "Important considerations: This calculator predicts postoperative pneumonia risk based on "
            "validated ACS NSQIP data. Pneumonia is associated with significantly increased 30-day mortality "
            "(17.0% vs 1.5%). Use in conjunction with clinical judgment for surgical decision-making and "
            "targeted prevention strategies. Consider individual patient factors such as recent respiratory "
            "infections, medication compliance, and surgical urgency when making final management decisions."
        )
        
        # Build comprehensive interpretation
        interpretation = (
            f"{parameter_summary}Gupta Postoperative Pneumonia Risk: {risk_percentage:.2f}% risk of "
            f"pneumonia within 30 days after surgery. Risk Category: {risk_category['level']} "
            f"({risk_category['description']}). Clinical recommendations: {recommendations} "
            f"{clinical_considerations}"
        )
        
        return {
            "level": risk_category["level"],
            "description": risk_category["description"], 
            "interpretation": interpretation
        }


def calculate_gupta_postoperative_pneumonia_risk(age: int, copd: str, functional_status: str, 
                                               asa_class: str, sepsis_status: str, smoking: str, 
                                               procedure_type: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gupta_postoperative_pneumonia_risk pattern
    """
    calculator = GuptaPostoperativePneumoniaRiskCalculator()
    return calculator.calculate(age, copd, functional_status, asa_class, 
                              sepsis_status, smoking, procedure_type)