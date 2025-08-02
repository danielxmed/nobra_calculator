"""
PROMISE Score for Malignant Pleural Effusion Calculator

Predicts 3-month mortality in patients with malignant pleural effusion using 
clinical and biological parameters. This tool helps guide treatment decisions 
and prognostic discussions.

References:
1. Psallidas I, Kanellakis NI, Gerry S, Thakur N, Bamber J, Dipper A, et al. 
   Development and validation of response markers to predict survival and 
   pleurodesis success in patients with malignant pleural effusion (PROMISE): 
   a multicohort analysis. Lancet Oncol. 2018;19(7):930-939. 
   doi: 10.1016/S1470-2045(18)30294-8.
2. Yap E, Anderson B, Nair A, Vaska K, Ferland L, Penney B, et al. 
   The role of LENT and PROMISE scores in predicting survival in malignant 
   pleural effusion. Lung. 2022;200(4):459-465. 
   doi: 10.1007/s00408-022-00547-5.
"""

from typing import Dict, Any


class PromiseScoreMalignantPleuralEffusionCalculator:
    """Calculator for PROMISE Score for Malignant Pleural Effusion"""
    
    def __init__(self):
        # Scoring weights for each parameter
        self.PREVIOUS_CHEMOTHERAPY_POINTS = {"no": 0, "yes": 4}
        self.PREVIOUS_RADIOTHERAPY_POINTS = {"no": 0, "yes": 2}
        
        self.HEMOGLOBIN_POINTS = {
            "≥16": 0,
            "14_to_<16": 1,
            "12_to_<14": 2,
            "10_to_<12": 3,
            "<10": 4
        }
        
        self.WBC_COUNT_POINTS = {
            "<4": 0,
            "4_to_<6.3": 2,
            "6.3_to_<10": 4,
            "10_to_<15.8": 7,
            "≥15.8": 9
        }
        
        self.CRP_POINTS = {
            "<3": 0,
            "3_to_<10": 3,
            "10_to_<32": 5,
            "32_to_<100": 8,
            "≥100": 11
        }
        
        self.ECOG_STATUS_POINTS = {"0-1": 0, "2-4": 7}
        self.CANCER_TYPE_POINTS = {"mesothelioma": 0, "lung": 6, "other": 5}
        
        # Valid options for validation
        self.VALID_CHEMOTHERAPY = ["no", "yes"]
        self.VALID_RADIOTHERAPY = ["no", "yes"]
        self.VALID_HEMOGLOBIN = ["≥16", "14_to_<16", "12_to_<14", "10_to_<12", "<10"]
        self.VALID_WBC = ["<4", "4_to_<6.3", "6.3_to_<10", "10_to_<15.8", "≥15.8"]
        self.VALID_CRP = ["<3", "3_to_<10", "10_to_<32", "32_to_<100", "≥100"]
        self.VALID_ECOG = ["0-1", "2-4"]
        self.VALID_CANCER_TYPE = ["mesothelioma", "lung", "other"]
    
    def calculate(self, previous_chemotherapy: str, previous_radiotherapy: str, 
                  hemoglobin: str, wbc_count: str, crp: str, ecog_status: str, 
                  cancer_type: str) -> Dict[str, Any]:
        """
        Calculates the PROMISE Score for Malignant Pleural Effusion
        
        Args:
            previous_chemotherapy (str): Previous chemotherapy history ("no" or "yes")
            previous_radiotherapy (str): Previous radiotherapy history ("no" or "yes")
            hemoglobin (str): Hemoglobin level category
            wbc_count (str): White blood cell count category
            crp (str): C-reactive protein level category
            ecog_status (str): ECOG Performance Status ("0-1" or "2-4")
            cancer_type (str): Primary cancer type ("mesothelioma", "lung", or "other")
            
        Returns:
            Dict with the PROMISE score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(previous_chemotherapy, previous_radiotherapy, hemoglobin, 
                             wbc_count, crp, ecog_status, cancer_type)
        
        # Calculate individual component scores
        chemo_points = self.PREVIOUS_CHEMOTHERAPY_POINTS[previous_chemotherapy]
        radio_points = self.PREVIOUS_RADIOTHERAPY_POINTS[previous_radiotherapy]
        hgb_points = self.HEMOGLOBIN_POINTS[hemoglobin]
        wbc_points = self.WBC_COUNT_POINTS[wbc_count]
        crp_points = self.CRP_POINTS[crp]
        ecog_points = self.ECOG_STATUS_POINTS[ecog_status]
        cancer_points = self.CANCER_TYPE_POINTS[cancer_type]
        
        # Calculate total score
        total_score = (chemo_points + radio_points + hgb_points + 
                      wbc_points + crp_points + ecog_points + cancer_points)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, previous_chemotherapy: str, previous_radiotherapy: str, 
                        hemoglobin: str, wbc_count: str, crp: str, ecog_status: str, 
                        cancer_type: str):
        """Validates input parameters"""
        
        if previous_chemotherapy not in self.VALID_CHEMOTHERAPY:
            raise ValueError(f"Previous chemotherapy must be one of: {', '.join(self.VALID_CHEMOTHERAPY)}")
        
        if previous_radiotherapy not in self.VALID_RADIOTHERAPY:
            raise ValueError(f"Previous radiotherapy must be one of: {', '.join(self.VALID_RADIOTHERAPY)}")
        
        if hemoglobin not in self.VALID_HEMOGLOBIN:
            raise ValueError(f"Hemoglobin must be one of: {', '.join(self.VALID_HEMOGLOBIN)}")
        
        if wbc_count not in self.VALID_WBC:
            raise ValueError(f"WBC count must be one of: {', '.join(self.VALID_WBC)}")
        
        if crp not in self.VALID_CRP:
            raise ValueError(f"CRP must be one of: {', '.join(self.VALID_CRP)}")
        
        if ecog_status not in self.VALID_ECOG:
            raise ValueError(f"ECOG status must be one of: {', '.join(self.VALID_ECOG)}")
        
        if cancer_type not in self.VALID_CANCER_TYPE:
            raise ValueError(f"Cancer type must be one of: {', '.join(self.VALID_CANCER_TYPE)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the PROMISE score
        
        Args:
            score (int): Total PROMISE score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 20:
            return {
                "stage": "Low Risk",
                "description": "3-month mortality <25%",
                "interpretation": f"LOW MORTALITY RISK (PROMISE Score: {score}): Predicted 3-month mortality <25%. "
                                f"PROGNOSIS: Excellent short-term survival expected with good quality of life potential. "
                                f"MANAGEMENT: Consider aggressive treatment approaches including pleurodesis, indwelling "
                                f"pleural catheters, or thoracoscopic procedures. INTERVENTIONS: Patient is suitable "
                                f"candidate for invasive procedures with curative or long-term palliative intent. "
                                f"MONITORING: Regular follow-up with focus on symptom control and quality of life. "
                                f"COUNSELING: Reassuring prognosis allows for comprehensive treatment planning."
            }
        elif score <= 30:
            return {
                "stage": "Intermediate-Low Risk",
                "description": "3-month mortality 25-50%",
                "interpretation": f"INTERMEDIATE-LOW MORTALITY RISK (PROMISE Score: {score}): Predicted 3-month "
                                f"mortality 25-50%. PROGNOSIS: Moderate survival expectation requiring balanced "
                                f"treatment approach. MANAGEMENT: Treatment decisions should weigh benefits versus "
                                f"burdens based on individual patient factors and preferences. INTERVENTIONS: "
                                f"Consider pleurodesis or indwelling catheter based on performance status and "
                                f"treatment goals. MONITORING: Close follow-up with reassessment of clinical "
                                f"status and treatment response. COUNSELING: Balanced discussions about "
                                f"prognosis and treatment options."
            }
        elif score <= 40:
            return {
                "stage": "Intermediate-High Risk",
                "description": "3-month mortality 50-75%",
                "interpretation": f"INTERMEDIATE-HIGH MORTALITY RISK (PROMISE Score: {score}): Predicted 3-month "
                                f"mortality 50-75%. PROGNOSIS: Limited survival expectation requiring careful "
                                f"consideration of treatment intensity. MANAGEMENT: Focus on symptom control with "
                                f"selective use of invasive procedures. INTERVENTIONS: Consider less invasive options "
                                f"such as therapeutic thoracentesis or indwelling pleural catheter. Avoid high-risk "
                                f"procedures unless significant symptom benefit expected. MONITORING: Frequent "
                                f"reassessment with emphasis on comfort and functional status. COUNSELING: Realistic "
                                f"prognostic discussions with focus on quality of life goals."
            }
        else:  # score > 40
            return {
                "stage": "High Risk",
                "description": "3-month mortality >75%",
                "interpretation": f"HIGH MORTALITY RISK (PROMISE Score: {score}): Predicted 3-month mortality >75%. "
                                f"PROGNOSIS: Very limited survival expectation with poor functional status likely. "
                                f"MANAGEMENT: Primarily palliative care approach with comfort-focused interventions. "
                                f"INTERVENTIONS: Avoid invasive procedures unless absolutely necessary for symptom "
                                f"relief. Consider therapeutic thoracentesis only for severe dyspnea. Focus on "
                                f"pain control, dyspnea management, and psychosocial support. MONITORING: Symptom-based "
                                f"assessment with emphasis on comfort measures. COUNSELING: Compassionate prognostic "
                                f"discussions with transition to end-of-life care planning."
            }


def calculate_promise_score_malignant_pleural_effusion(previous_chemotherapy: str, 
                                                      previous_radiotherapy: str, 
                                                      hemoglobin: str, wbc_count: str, 
                                                      crp: str, ecog_status: str, 
                                                      cancer_type: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PromiseScoreMalignantPleuralEffusionCalculator()
    return calculator.calculate(previous_chemotherapy, previous_radiotherapy, hemoglobin, 
                               wbc_count, crp, ecog_status, cancer_type)