"""
LENT Prognostic Score for Malignant Pleural Effusion Calculator

Predicts survival in patients with malignant pleural effusion using four clinical and 
laboratory parameters: pleural fluid LDH, ECOG performance status, neutrophil-to-lymphocyte 
ratio, and tumor type. Helps inform treatment decisions and prognosis discussions.

References:
1. Clive AO, Kahan BC, Hopwood BE, Bhatnagar R, Morley AJ, Zahan-Evans N, et al. 
   Predicting survival in malignant pleural effusion: development and validation of the 
   LENT prognostic score. Thorax. 2014 Dec;69(12):1098-104.
2. Psallidas I, Kanellakis NI, Gerry S, Theza A, Saba T, Tsim S, et al. Development and 
   validation of response markers to predict survival and pleurodesis success in patients 
   with malignant pleural effusion (PROMISE): a multicohort analysis. Lancet Oncol. 2018 Jul;19(7):930-939.
"""

from typing import Dict, Any


class LentPrognosticScoreCalculator:
    """Calculator for LENT Prognostic Score for Malignant Pleural Effusion"""
    
    def __init__(self):
        """Initialize scoring thresholds and survival outcomes"""
        
        # LDH threshold
        self.ldh_threshold = 1500  # U/L
        
        # Neutrophil-to-lymphocyte ratio threshold
        self.nlr_threshold = 9
        
        # ECOG performance status points
        self.ecog_points = {
            0: 0,  # Fully active
            1: 1,  # Restricted in strenuous activity
            2: 2,  # Ambulatory, >50% waking hours up
            3: 3,  # Limited self-care, >50% waking hours bed/chair
            4: 3   # Completely disabled, bed/chair bound
        }
        
        # Tumor type points
        self.tumor_points = {
            "mesothelioma_hematologic": 0,  # Mesothelioma or hematologic malignancy
            "breast_gynecologic_renal": 1,  # Breast, gynecologic, or renal cell carcinoma
            "lung_other": 2                 # Lung or any other cancer
        }
        
        # Risk thresholds
        self.low_risk_max = 1
        self.moderate_risk_max = 4
        
        # Median survival outcomes (days)
        self.survival_outcomes = {
            "low_risk": 319,      # ~10.5 months
            "moderate_risk": 130, # ~4.3 months
            "high_risk": 44       # ~1.5 months
        }
    
    def calculate(self, pleural_fluid_ldh: float, ecog_performance_status: int,
                 neutrophil_lymphocyte_ratio: float, tumor_type: str) -> Dict[str, Any]:
        """
        Calculates the LENT Prognostic Score
        
        Args:
            pleural_fluid_ldh (float): Pleural fluid LDH level in U/L
            ecog_performance_status (int): ECOG Performance Status (0-4)
            neutrophil_lymphocyte_ratio (float): Serum neutrophil-to-lymphocyte ratio
            tumor_type (str): Primary tumor type category
            
        Returns:
            Dict with the calculated score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            pleural_fluid_ldh, ecog_performance_status,
            neutrophil_lymphocyte_ratio, tumor_type
        )
        
        # Calculate individual component scores
        ldh_score = self._calculate_ldh_score(pleural_fluid_ldh)
        ecog_score = self._calculate_ecog_score(ecog_performance_status)
        nlr_score = self._calculate_nlr_score(neutrophil_lymphocyte_ratio)
        tumor_score = self._calculate_tumor_score(tumor_type)
        
        # Calculate total score
        total_score = ldh_score + ecog_score + nlr_score + tumor_score
        
        # Get risk interpretation
        risk_interpretation = self._get_risk_interpretation(total_score)
        
        # Generate comprehensive interpretation
        detailed_interpretation = self._generate_detailed_interpretation(
            total_score, risk_interpretation, pleural_fluid_ldh,
            ecog_performance_status, neutrophil_lymphocyte_ratio, tumor_type
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": detailed_interpretation,
            "stage": risk_interpretation["stage"],
            "stage_description": risk_interpretation["description"]
        }
    
    def _validate_inputs(self, pleural_fluid_ldh, ecog_performance_status,
                        neutrophil_lymphocyte_ratio, tumor_type):
        """Validates input parameters"""
        
        if not isinstance(pleural_fluid_ldh, (int, float)) or pleural_fluid_ldh < 0:
            raise ValueError("Pleural fluid LDH must be a non-negative number")
        
        if pleural_fluid_ldh > 10000:
            raise ValueError("Pleural fluid LDH value seems unusually high (>10,000 U/L)")
        
        if not isinstance(ecog_performance_status, int) or ecog_performance_status not in self.ecog_points:
            raise ValueError("ECOG Performance Status must be an integer between 0 and 4")
        
        if not isinstance(neutrophil_lymphocyte_ratio, (int, float)) or neutrophil_lymphocyte_ratio < 0:
            raise ValueError("Neutrophil-to-lymphocyte ratio must be a non-negative number")
        
        if neutrophil_lymphocyte_ratio > 100:
            raise ValueError("Neutrophil-to-lymphocyte ratio seems unusually high (>100)")
        
        if tumor_type not in self.tumor_points:
            raise ValueError("Tumor type must be one of: mesothelioma_hematologic, breast_gynecologic_renal, lung_other")
    
    def _calculate_ldh_score(self, pleural_fluid_ldh: float) -> int:
        """Calculates LDH component score"""
        return 1 if pleural_fluid_ldh >= self.ldh_threshold else 0
    
    def _calculate_ecog_score(self, ecog_performance_status: int) -> int:
        """Calculates ECOG performance status component score"""
        return self.ecog_points[ecog_performance_status]
    
    def _calculate_nlr_score(self, neutrophil_lymphocyte_ratio: float) -> int:
        """Calculates neutrophil-to-lymphocyte ratio component score"""
        return 1 if neutrophil_lymphocyte_ratio >= self.nlr_threshold else 0
    
    def _calculate_tumor_score(self, tumor_type: str) -> int:
        """Calculates tumor type component score"""
        return self.tumor_points[tumor_type]
    
    def _get_risk_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Interprets the LENT score according to risk categories
        
        Args:
            total_score (int): Calculated total score
            
        Returns:
            Dict with risk interpretation
        """
        
        if total_score <= self.low_risk_max:
            return {
                "stage": "Low Risk",
                "description": "Low risk of mortality",
                "risk_category": "Low",
                "median_survival_days": self.survival_outcomes["low_risk"],
                "median_survival_months": round(self.survival_outcomes["low_risk"] / 30.4, 1)
            }
        elif total_score <= self.moderate_risk_max:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of mortality",
                "risk_category": "Moderate",
                "median_survival_days": self.survival_outcomes["moderate_risk"],
                "median_survival_months": round(self.survival_outcomes["moderate_risk"] / 30.4, 1)
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk of mortality",
                "risk_category": "High",
                "median_survival_days": self.survival_outcomes["high_risk"],
                "median_survival_months": round(self.survival_outcomes["high_risk"] / 30.4, 1)
            }
    
    def _generate_detailed_interpretation(self, total_score, risk_interpretation,
                                        pleural_fluid_ldh, ecog_performance_status,
                                        neutrophil_lymphocyte_ratio, tumor_type) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Returns:
            str: Detailed clinical interpretation and recommendations
        """
        
        # Base interpretation
        base_interpretation = (
            f"LENT Prognostic Score: {total_score} points. "
            f"Risk category: {risk_interpretation['stage']}. "
            f"Median survival: {risk_interpretation['median_survival_days']} days "
            f"(approximately {risk_interpretation['median_survival_months']} months). "
        )
        
        # Risk-specific recommendations
        if risk_interpretation["risk_category"] == "Low":
            recommendations = (
                "Low risk group with relatively better prognosis. Patients in this group may benefit "
                "from more aggressive interventions such as pleurodesis or indwelling pleural catheters. "
                "Consider discussing treatment options that may improve quality of life and potentially "
                "extend survival. Regular oncology follow-up and symptom management are important."
            )
        elif risk_interpretation["risk_category"] == "Moderate":
            recommendations = (
                "Moderate risk group with intermediate prognosis. Treatment decisions should be "
                "individualized based on patient preferences, performance status, and goals of care. "
                "Consider palliative interventions to improve quality of life. Discussion about "
                "advance directives and care preferences is appropriate."
            )
        else:  # High risk
            recommendations = (
                "High risk group with limited survival expectancy. Focus should be on palliative care "
                "and comfort measures. Less invasive interventions may be most appropriate to minimize "
                "patient burden. Early palliative care consultation and discussions about end-of-life "
                "care preferences are strongly recommended."
            )
        
        # Contributing factors
        contributing_factors = []
        if pleural_fluid_ldh >= self.ldh_threshold:
            contributing_factors.append(f"elevated pleural fluid LDH ({pleural_fluid_ldh} U/L)")
        if ecog_performance_status >= 2:
            contributing_factors.append(f"impaired functional status (ECOG {ecog_performance_status})")
        if neutrophil_lymphocyte_ratio >= self.nlr_threshold:
            contributing_factors.append(f"elevated neutrophil-to-lymphocyte ratio ({neutrophil_lymphocyte_ratio})")
        
        # Tumor type description
        tumor_descriptions = {
            "mesothelioma_hematologic": "mesothelioma or hematologic malignancy",
            "breast_gynecologic_renal": "breast, gynecologic, or renal cell carcinoma",
            "lung_other": "lung cancer or other solid tumor"
        }
        tumor_description = tumor_descriptions.get(tumor_type, "unknown tumor type")
        
        factor_summary = ""
        if contributing_factors:
            factor_summary = f" Key prognostic factors include: {', '.join(contributing_factors)}, and {tumor_description}."
        else:
            factor_summary = f" Primary tumor type: {tumor_description}."
        
        # Clinical context
        clinical_context = (
            " The LENT score should be used in conjunction with clinical judgment and patient preferences "
            "to guide treatment decisions. It is particularly useful for identifying patients who might "
            "benefit from less invasive interventions and for facilitating discussions about prognosis "
            "and goals of care."
        )
        
        return base_interpretation + recommendations + factor_summary + clinical_context


def calculate_lent_prognostic_score(pleural_fluid_ldh, ecog_performance_status,
                                  neutrophil_lymphocyte_ratio, tumor_type) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = LentPrognosticScoreCalculator()
    return calculator.calculate(
        pleural_fluid_ldh, ecog_performance_status,
        neutrophil_lymphocyte_ratio, tumor_type
    )