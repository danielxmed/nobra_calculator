"""
Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA) Calculator

The Gupta MICA risk calculator predicts the risk of myocardial infarction or cardiac 
arrest within 30 days after surgery. This validated tool uses five perioperative risk 
factors and provides superior predictive ability compared to previous cardiac risk 
assessment tools.

The calculator helps clinicians identify patients who may benefit from enhanced 
perioperative cardiac monitoring, preoperative optimization, or specialized care 
planning. It applies to both cardiac and non-cardiac surgical procedures.

Clinical Applications:
- Preoperative risk stratification and patient counseling
- Decision-making for enhanced perioperative monitoring
- Identification of patients requiring cardiology consultation
- Postoperative care planning and resource allocation
- Informed consent discussions with patients and families

References (Vancouver style):
1. Gupta PK, Gupta H, Sundaram A, et al. Development and validation of a risk calculator 
   for prediction of cardiac risk after surgery. Circulation. 2011;124(4):381-387. 
   doi: 10.1161/CIRCULATIONAHA.110.015701
2. Bilimoria KY, Liu Y, Paruch JL, et al. Development and evaluation of the universal 
   ACS NSQIP surgical risk calculator: a decision aid and informed consent tool for 
   patients and surgeons. J Am Coll Surg. 2013;217(5):833-842. 
   doi: 10.1016/j.jamcollsurg.2013.07.385
3. Ford MK, Beattie WS, Wijeysundera DN. Systematic review: prediction of perioperative 
   cardiac complications and mortality by the revised cardiac risk index. Ann Intern Med. 
   2010;152(1):26-35. doi: 10.7326/0003-4819-152-1-201001050-00007
"""

import math
from typing import Dict, Any


class GuptaMicaCalculator:
    """Calculator for Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest"""
    
    def __init__(self):
        # Age coefficient (points per year)
        self.AGE_COEFFICIENT = 0.02
        
        # Functional status points
        self.FUNCTIONAL_STATUS_POINTS = {
            "independent": 0.0,
            "partially_dependent": 0.65,
            "totally_dependent": 1.03
        }
        
        # ASA class points
        self.ASA_CLASS_POINTS = {
            "1": -5.17,  # Normal healthy patient
            "2": -3.29,  # Mild systemic disease
            "3": -1.92,  # Severe systemic disease
            "4": -0.95,  # Severe systemic disease threatening life
            "5": 0.0     # Moribund patient
        }
        
        # Creatinine status points
        self.CREATININE_POINTS = {
            "normal": 0.0,      # ≤1.5 mg/dL
            "elevated": 0.61,   # >1.5 mg/dL
            "unknown": -0.10
        }
        
        # Surgery type points (from highest to lowest risk)
        self.SURGERY_TYPE_POINTS = {
            "aortic": 1.60,
            "brain": 1.40,
            "cardiac": 1.01,
            "foregut_hepatobiliary": 0.82,
            "gallbladder_appendix_adrenals_spleen": 0.67,
            "intestinal": 0.58,
            "neck": 0.40,
            "obstetric_gynecologic": 0.28,
            "orthopedic_non_spine": 0.20,
            "peripheral_vascular": 0.16,
            "skin": 0.12,
            "spine": 0.10,
            "thoracic_non_cardiac": 0.06,
            "urology_non_renal": 0.04,
            "renal": 0.02,
            "hernia": 0.0,
            "thyroid_parathyroid": -0.32,
            "breast": -1.61,
            "eye": -1.05,
            "vein": -1.09
        }
        
        # Base constant for logistic regression
        self.BASE_CONSTANT = -5.25
        
        # Risk interpretation thresholds
        self.RISK_THRESHOLDS = [
            {"min": 0.0, "max": 0.5, "level": "Very Low Risk", "description": "Minimal perioperative cardiac risk"},
            {"min": 0.5, "max": 1.0, "level": "Low Risk", "description": "Low perioperative cardiac risk"},
            {"min": 1.0, "max": 2.0, "level": "Moderate Risk", "description": "Moderate perioperative cardiac risk"},
            {"min": 2.0, "max": 5.0, "level": "High Risk", "description": "High perioperative cardiac risk"},
            {"min": 5.0, "max": 100.0, "level": "Very High Risk", "description": "Very high perioperative cardiac risk"}
        ]
    
    def calculate(self, age: int, functional_status: str, asa_class: str,
                 creatinine_status: str, surgery_type: str) -> Dict[str, Any]:
        """
        Calculates Gupta MICA risk score
        
        Args:
            age (int): Patient age in years
            functional_status (str): Functional status (independent, partially_dependent, totally_dependent)
            asa_class (str): ASA Physical Status Classification (1-5)
            creatinine_status (str): Creatinine level status (normal, elevated, unknown)
            surgery_type (str): Type of surgical procedure
            
        Returns:
            Dict with risk percentage and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, functional_status, asa_class, creatinine_status, surgery_type)
        
        # Calculate risk score components
        age_points = age * self.AGE_COEFFICIENT
        functional_points = self.FUNCTIONAL_STATUS_POINTS[functional_status]
        asa_points = self.ASA_CLASS_POINTS[asa_class]
        creatinine_points = self.CREATININE_POINTS[creatinine_status]
        surgery_points = self.SURGERY_TYPE_POINTS[surgery_type]
        
        # Calculate logistic regression score (x)
        x = (self.BASE_CONSTANT + age_points + functional_points + 
             asa_points + creatinine_points + surgery_points)
        
        # Calculate risk percentage using logistic function
        # Risk = e^x / (1 + e^x) * 100
        try:
            exp_x = math.exp(x)
            risk_percentage = (exp_x / (1 + exp_x)) * 100
        except OverflowError:
            # Handle overflow for very high scores
            risk_percentage = 100.0 if x > 0 else 0.0
        
        # Get risk interpretation
        interpretation = self._get_interpretation(risk_percentage, age, functional_status,
                                                asa_class, creatinine_status, surgery_type)
        
        return {
            "result": round(risk_percentage, 2),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["level"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, functional_status: str, asa_class: str,
                        creatinine_status: str, surgery_type: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if functional_status not in self.FUNCTIONAL_STATUS_POINTS:
            raise ValueError(f"Functional status must be one of: {list(self.FUNCTIONAL_STATUS_POINTS.keys())}")
        
        if asa_class not in self.ASA_CLASS_POINTS:
            raise ValueError(f"ASA class must be one of: {list(self.ASA_CLASS_POINTS.keys())}")
        
        if creatinine_status not in self.CREATININE_POINTS:
            raise ValueError(f"Creatinine status must be one of: {list(self.CREATININE_POINTS.keys())}")
        
        if surgery_type not in self.SURGERY_TYPE_POINTS:
            raise ValueError(f"Surgery type must be one of: {list(self.SURGERY_TYPE_POINTS.keys())}")
    
    def _get_interpretation(self, risk_percentage: float, age: int, functional_status: str,
                          asa_class: str, creatinine_status: str, surgery_type: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on risk percentage
        
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
        if risk_category is None and risk_percentage >= 5.0:
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
            "1": "ASA Class I (normal healthy patient)",
            "2": "ASA Class II (mild systemic disease)",
            "3": "ASA Class III (severe systemic disease)",
            "4": "ASA Class IV (severe systemic disease threatening life)",
            "5": "ASA Class V (moribund patient)"
        }
        
        creatinine_descriptions = {
            "normal": "normal creatinine (≤1.5 mg/dL)",
            "elevated": "elevated creatinine (>1.5 mg/dL)",
            "unknown": "unknown creatinine status"
        }
        
        surgery_descriptions = {
            "aortic": "aortic surgery",
            "brain": "brain surgery",
            "cardiac": "cardiac surgery",
            "breast": "breast surgery",
            "hernia": "hernia repair",
            "vein": "vein surgery"
        }
        
        surgery_desc = surgery_descriptions.get(surgery_type, surgery_type.replace("_", " "))
        
        parameter_summary = (
            f"Patient characteristics: {age} years old, {functional_descriptions[functional_status]}, "
            f"{asa_descriptions[asa_class]}, {creatinine_descriptions[creatinine_status]}, "
            f"undergoing {surgery_desc}. "
        )
        
        # Generate risk-specific recommendations
        if risk_percentage < 0.5:  # Very Low Risk
            recommendations = (
                "Very low perioperative cardiac risk. Standard perioperative monitoring and "
                "routine postoperative care protocols are appropriate. No additional cardiac "
                "interventions typically required. Continue standard perioperative medications "
                "as clinically indicated."
            )
        elif risk_percentage < 1.0:  # Low Risk
            recommendations = (
                "Low perioperative cardiac risk. Standard monitoring with attention to cardiac "
                "symptoms is recommended. Consider basic cardiac precautions and continue home "
                "cardiac medications unless contraindicated. Monitor for signs of myocardial "
                "ischemia postoperatively."
            )
        elif risk_percentage < 2.0:  # Moderate Risk
            recommendations = (
                "Moderate perioperative cardiac risk requiring enhanced monitoring. Consider "
                "cardiac telemetry monitoring, serial troponin measurements, and cardiology "
                "consultation for high-risk procedures. Optimize medical management of "
                "cardiovascular risk factors preoperatively."
            )
        elif risk_percentage < 5.0:  # High Risk
            recommendations = (
                "High perioperative cardiac risk requiring intensive monitoring and cardiac "
                "optimization. Strongly consider preoperative cardiology evaluation, continuous "
                "cardiac monitoring, postoperative ICU care, and serial cardiac biomarkers. "
                "Optimize beta-blockers, statins, and other cardioprotective medications."
            )
        else:  # Very High Risk
            recommendations = (
                "Very high perioperative cardiac risk requiring comprehensive cardiac evaluation "
                "and optimization. Consider postponing elective surgery for cardiac optimization, "
                "preoperative stress testing, echocardiography, and multidisciplinary team "
                "approach. May require invasive cardiac monitoring and ICU-level care."
            )
        
        # Add important clinical considerations
        clinical_considerations = (
            "Important considerations: This calculator predicts 30-day perioperative myocardial "
            "infarction or cardiac arrest risk based on validated risk factors. Should be used "
            "in conjunction with clinical judgment and comprehensive patient assessment. Consider "
            "individual patient factors not captured in the model, such as coronary artery disease, "
            "medication compliance, and surgical urgency when making final management decisions."
        )
        
        # Build comprehensive interpretation
        interpretation = (
            f"{parameter_summary}Gupta MICA Risk: {risk_percentage:.2f}% risk of perioperative "
            f"cardiac events within 30 days. Risk Category: {risk_category['level']} "
            f"({risk_category['description']}). Clinical recommendations: {recommendations} "
            f"{clinical_considerations}"
        )
        
        return {
            "level": risk_category["level"],
            "description": risk_category["description"],
            "interpretation": interpretation
        }


def calculate_gupta_mica(age: int, functional_status: str, asa_class: str,
                        creatinine_status: str, surgery_type: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gupta_mica pattern
    """
    calculator = GuptaMicaCalculator()
    return calculator.calculate(age, functional_status, asa_class, creatinine_status, surgery_type)