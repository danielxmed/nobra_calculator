"""
Khorana Risk Score for Venous Thromboembolism in Cancer Patients Calculator

Predicts VTE risk for cancer patients depending on cancer type and other factors.
This validated risk assessment tool helps identify cancer patients at high risk for 
venous thromboembolism who may benefit from thromboprophylaxis during chemotherapy.

References:
1. Khorana AA, Kuderer NM, Culakova E, Lyman GH, Francis CW. Development and 
   validation of a predictive model for chemotherapy-associated venous 
   thromboembolism. Blood. 2008;111(10):4902-7.
2. Ay C, Dunkler D, Marosi C, Chiriac AL, Vormittag R, Simanek R, et al. 
   Prediction of venous thromboembolism in cancer patients. Blood. 
   2010;116(24):5377-82.
3. Verso M, Agnelli G, Barni S, Gasparini G, LaBianca R. A modified Khorana 
   risk assessment score for venous thromboembolism in cancer patients 
   receiving chemotherapy: the Protecht score. Intern Emerg Med. 2012;7(3):291-2.
4. Mulder FI, Candeloro M, Kamphuisen PW, Di Nisio M, Bossuyt PM, Guman N, et al. 
   The Khorana score for prediction of venous thromboembolism in cancer patients: 
   a systematic review and meta-analysis. Haematologica. 2019;104(6):1277-1287.
"""

from typing import Dict, Any


class KhoranaRiskScoreCalculator:
    """Calculator for Khorana Risk Score for VTE in Cancer Patients"""
    
    def __init__(self):
        # Cancer risk categories and their scores
        self.cancer_scores = {
            "very_high_risk": 2,  # Stomach, pancreas
            "high_risk": 1,       # Lung, lymphoma, gynecologic, bladder, testicular
            "standard_risk": 0    # Other cancers
        }
        
        # Risk stratification thresholds
        self.risk_categories = {
            "low": 0,
            "intermediate_low": 1,
            "intermediate_high": 2,
            "high": 3
        }
    
    def calculate(self, cancer_type: str, platelet_count_elevated: str,
                 hemoglobin_low_or_epo: str, leukocyte_count_elevated: str,
                 bmi_elevated: str) -> Dict[str, Any]:
        """
        Calculates Khorana Risk Score for VTE in cancer patients
        
        Args:
            cancer_type (str): Cancer risk category (very_high_risk, high_risk, standard_risk)
            platelet_count_elevated (str): Pre-chemo platelet count ≥350×10⁹/L
            hemoglobin_low_or_epo (str): Hgb <10 g/dL or using RBC growth factors
            leukocyte_count_elevated (str): Pre-chemo leukocyte count >11×10⁹/L
            bmi_elevated (str): BMI ≥35 kg/m²
            
        Returns:
            Dict with the risk score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(cancer_type, platelet_count_elevated,
                            hemoglobin_low_or_epo, leukocyte_count_elevated,
                            bmi_elevated)
        
        # Calculate total score
        total_score = self._calculate_total_score(
            cancer_type, platelet_count_elevated, hemoglobin_low_or_epo,
            leukocyte_count_elevated, bmi_elevated
        )
        
        # Get risk category and interpretation
        risk_assessment = self._get_risk_assessment(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["stage_description"]
        }
    
    def _validate_inputs(self, cancer_type: str, platelet_count_elevated: str,
                        hemoglobin_low_or_epo: str, leukocyte_count_elevated: str,
                        bmi_elevated: str):
        """Validates input parameters"""
        
        if cancer_type not in self.cancer_scores:
            raise ValueError(f"Cancer type must be one of: {list(self.cancer_scores.keys())}")
        
        # Validate yes/no parameters
        yes_no_params = {
            "platelet_count_elevated": platelet_count_elevated,
            "hemoglobin_low_or_epo": hemoglobin_low_or_epo,
            "leukocyte_count_elevated": leukocyte_count_elevated,
            "bmi_elevated": bmi_elevated
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, cancer_type: str, platelet_count_elevated: str,
                              hemoglobin_low_or_epo: str, leukocyte_count_elevated: str,
                              bmi_elevated: str) -> int:
        """Calculates the total Khorana score"""
        
        total_score = 0
        
        # Cancer type score
        total_score += self.cancer_scores[cancer_type]
        
        # Add 1 point for each positive risk factor
        if platelet_count_elevated == "yes":
            total_score += 1
        
        if hemoglobin_low_or_epo == "yes":
            total_score += 1
        
        if leukocyte_count_elevated == "yes":
            total_score += 1
        
        if bmi_elevated == "yes":
            total_score += 1
        
        return total_score
    
    def _get_risk_assessment(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and clinical interpretation
        
        Args:
            score (int): Total Khorana score
            
        Returns:
            Dict with risk assessment details
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "stage_description": "Low risk of VTE",
                "interpretation": (
                    f"Low risk of VTE (Khorana score: {score}). The 6-month VTE incidence is "
                    "approximately 5.0% in low-risk patients. Routine thromboprophylaxis is "
                    "generally not recommended for low-risk patients. Standard preventive "
                    "measures should be employed including early mobilization, adequate "
                    "hydration, and VTE awareness education. Monitor for VTE symptoms and "
                    "reassess risk if clinical status changes."
                )
            }
        
        elif score == 1:
            return {
                "stage": "Intermediate-Low Risk",
                "stage_description": "Intermediate-low risk of VTE",
                "interpretation": (
                    f"Intermediate-low risk of VTE (Khorana score: {score}). The 6-month VTE "
                    "incidence is approximately 6.6% in intermediate-risk patients (scores 1-2). "
                    "Consider individual patient factors when deciding on thromboprophylaxis. "
                    "Some guidelines suggest considering prophylaxis for scores ≥2. Enhanced "
                    "monitoring for VTE symptoms is recommended. Reassess risk with changes "
                    "in clinical status or treatment regimen."
                )
            }
        
        elif score == 2:
            return {
                "stage": "Intermediate-High Risk",
                "stage_description": "Intermediate-high risk of VTE",
                "interpretation": (
                    f"Intermediate-high risk of VTE (Khorana score: {score}). The 6-month VTE "
                    "incidence is approximately 6.6% in intermediate-risk patients. Recent "
                    "evidence suggests the optimal high-risk cutoff may be ≥2 points rather "
                    "than ≥3. Consider thromboprophylaxis with LMWH, which can reduce VTE "
                    "risk by 64% in high-risk patients. Discuss risks and benefits with "
                    "patient, considering bleeding risk and other factors."
                )
            }
        
        else:  # score >= 3
            return {
                "stage": "High Risk",
                "stage_description": "High risk of VTE",
                "interpretation": (
                    f"High risk of VTE (Khorana score: {score}). The 6-month VTE incidence is "
                    "approximately 11.0% in high-risk patients (score ≥3). Thromboprophylaxis "
                    "with LMWH is recommended in the absence of contraindications. Studies show "
                    "LMWH can reduce VTE risk by 64% in high-risk patients without significantly "
                    "increasing major bleeding risk. Consider prophylactic anticoagulation "
                    "throughout the chemotherapy period. Monitor closely for both VTE and "
                    "bleeding complications."
                )
            }


def calculate_khorana_risk_score(cancer_type: str, platelet_count_elevated: str,
                                hemoglobin_low_or_epo: str, leukocyte_count_elevated: str,
                                bmi_elevated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_khorana_risk_score pattern
    """
    calculator = KhoranaRiskScoreCalculator()
    return calculator.calculate(cancer_type, platelet_count_elevated,
                               hemoglobin_low_or_epo, leukocyte_count_elevated,
                               bmi_elevated)