"""
Manchester Score for Prognosis in Small Cell Lung Cancer Calculator

Predicts 2-year survival in patients with small cell lung cancer (SCLC) using six clinical
and laboratory parameters. Stratifies patients into three prognostic groups.

References:
1. Cerny T, Blair V, Anderson H, Bramwell V, Thatcher N. Pretreatment prognostic factors 
   and scoring system in 407 small-cell lung cancer patients. Int J Cancer. 1987 Jul 15;40(1):1-7. 
   doi: 10.1002/ijc.2910400102.
2. Paesmans M, Sculier JP, Libert P, Bureau G, Dabouis G, Thiriaux J, et al. Prognostic 
   factors for survival in advanced non-small-cell lung cancer: univariate and multivariate 
   analyses including recursive partitioning and amalgamation algorithms in 1,052 patients. 
   J Clin Oncol. 1995 May;13(5):1221-30. doi: 10.1200/JCO.1995.13.5.1221.
"""

from typing import Dict, Any


class ManchesterScorePrognosisSclcCalculator:
    """Calculator for Manchester Score for Prognosis in Small Cell Lung Cancer"""
    
    def __init__(self):
        # Thresholds for scoring
        self.SODIUM_THRESHOLD = 132.0  # mmol/L
        self.BICARBONATE_THRESHOLD = 24.0  # mmol/L
        self.KPS_THRESHOLD = 50  # Karnofsky Performance Status
        
        # Valid options
        self.VALID_LDH_LEVELS = ["normal", "elevated"]
        self.VALID_ALP_LEVELS = ["normal", "1.1_to_1.5_times_normal", "greater_than_1.5_times_normal"]
        self.VALID_DISEASE_STAGES = ["limited", "extensive"]
    
    def calculate(self, serum_ldh: str, serum_sodium: float, serum_alkaline_phosphatase: str, 
                  serum_bicarbonate: float, disease_stage: str, karnofsky_performance_status: int) -> Dict[str, Any]:
        """
        Calculates the Manchester Score for SCLC prognosis using the provided parameters
        
        Args:
            serum_ldh (str): LDH level ("normal" or "elevated")
            serum_sodium (float): Serum sodium in mmol/L
            serum_alkaline_phosphatase (str): ALP level relative to normal
            serum_bicarbonate (float): Serum bicarbonate in mmol/L
            disease_stage (str): Disease stage ("limited" or "extensive")
            karnofsky_performance_status (int): KPS score (0-100)
            
        Returns:
            Dict with the result, component scores, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(serum_ldh, serum_sodium, serum_alkaline_phosphatase, 
                             serum_bicarbonate, disease_stage, karnofsky_performance_status)
        
        # Calculate individual component scores
        ldh_score = self._calculate_ldh_score(serum_ldh)
        sodium_score = self._calculate_sodium_score(serum_sodium)
        alp_score = self._calculate_alp_score(serum_alkaline_phosphatase)
        bicarbonate_score = self._calculate_bicarbonate_score(serum_bicarbonate)
        stage_score = self._calculate_stage_score(disease_stage)
        kps_score = self._calculate_kps_score(karnofsky_performance_status)
        
        # Calculate total Manchester Score
        total_score = ldh_score + sodium_score + alp_score + bicarbonate_score + stage_score + kps_score
        
        # Get interpretation and prognosis
        interpretation_data = self._get_interpretation(total_score)
        
        # Get detailed survival data
        survival_data = self._get_survival_data(total_score)
        
        return {
            "result": {
                "total_score": total_score,
                "ldh_score": ldh_score,
                "sodium_score": sodium_score,
                "alp_score": alp_score,
                "bicarbonate_score": bicarbonate_score,
                "stage_score": stage_score,
                "kps_score": kps_score,
                "ldh_category": f"LDH {serum_ldh}",
                "sodium_category": f"Sodium {'<132' if serum_sodium < self.SODIUM_THRESHOLD else '≥132'} mmol/L: {serum_sodium}",
                "alp_category": f"Alkaline phosphatase {serum_alkaline_phosphatase.replace('_', ' ')}",
                "bicarbonate_category": f"Bicarbonate {'<24' if serum_bicarbonate < self.BICARBONATE_THRESHOLD else '≥24'} mmol/L: {serum_bicarbonate}",
                "stage_category": f"Disease stage: {disease_stage}",
                "kps_category": f"Karnofsky Performance Status {'≤50' if karnofsky_performance_status <= self.KPS_THRESHOLD else '>50'}: {karnofsky_performance_status}",
                "survival_data": survival_data
            },
            "unit": "points",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, serum_ldh: str, serum_sodium: float, serum_alkaline_phosphatase: str,
                        serum_bicarbonate: float, disease_stage: str, karnofsky_performance_status: int):
        """Validates input parameters"""
        
        # Validate LDH level
        if not isinstance(serum_ldh, str):
            raise ValueError("Serum LDH level must be a string")
        
        if serum_ldh.lower() not in [level.lower() for level in self.VALID_LDH_LEVELS]:
            raise ValueError(f"LDH level must be one of: {', '.join(self.VALID_LDH_LEVELS)}")
        
        # Validate sodium
        if not isinstance(serum_sodium, (int, float)):
            raise ValueError("Serum sodium must be a number")
        
        if serum_sodium < 110.0 or serum_sodium > 160.0:
            raise ValueError("Serum sodium must be between 110.0 and 160.0 mmol/L")
        
        # Validate alkaline phosphatase
        if not isinstance(serum_alkaline_phosphatase, str):
            raise ValueError("Serum alkaline phosphatase level must be a string")
        
        if serum_alkaline_phosphatase not in self.VALID_ALP_LEVELS:
            raise ValueError(f"ALP level must be one of: {', '.join(self.VALID_ALP_LEVELS)}")
        
        # Validate bicarbonate
        if not isinstance(serum_bicarbonate, (int, float)):
            raise ValueError("Serum bicarbonate must be a number")
        
        if serum_bicarbonate < 10.0 or serum_bicarbonate > 40.0:
            raise ValueError("Serum bicarbonate must be between 10.0 and 40.0 mmol/L")
        
        # Validate disease stage
        if not isinstance(disease_stage, str):
            raise ValueError("Disease stage must be a string")
        
        if disease_stage.lower() not in [stage.lower() for stage in self.VALID_DISEASE_STAGES]:
            raise ValueError(f"Disease stage must be one of: {', '.join(self.VALID_DISEASE_STAGES)}")
        
        # Validate Karnofsky Performance Status
        if not isinstance(karnofsky_performance_status, int):
            raise ValueError("Karnofsky Performance Status must be an integer")
        
        if karnofsky_performance_status < 0 or karnofsky_performance_status > 100:
            raise ValueError("Karnofsky Performance Status must be between 0 and 100")
    
    def _calculate_ldh_score(self, serum_ldh: str) -> int:
        """Calculates score based on LDH level"""
        return 1 if serum_ldh.lower() == "elevated" else 0
    
    def _calculate_sodium_score(self, serum_sodium: float) -> int:
        """Calculates score based on sodium level"""
        return 1 if serum_sodium < self.SODIUM_THRESHOLD else 0
    
    def _calculate_alp_score(self, serum_alkaline_phosphatase: str) -> int:
        """Calculates score based on alkaline phosphatase level"""
        return 1 if serum_alkaline_phosphatase == "greater_than_1.5_times_normal" else 0
    
    def _calculate_bicarbonate_score(self, serum_bicarbonate: float) -> int:
        """Calculates score based on bicarbonate level"""
        return 1 if serum_bicarbonate < self.BICARBONATE_THRESHOLD else 0
    
    def _calculate_stage_score(self, disease_stage: str) -> int:
        """Calculates score based on disease stage"""
        return 1 if disease_stage.lower() == "extensive" else 0
    
    def _calculate_kps_score(self, karnofsky_performance_status: int) -> int:
        """Calculates score based on Karnofsky Performance Status"""
        return 1 if karnofsky_performance_status <= self.KPS_THRESHOLD else 0
    
    def _get_survival_data(self, total_score: int) -> Dict[str, str]:
        """
        Returns survival data based on Manchester Score
        
        Args:
            total_score (int): Total Manchester Score
            
        Returns:
            Dict with survival rates and prognostic information
        """
        
        if total_score <= 1:  # Good prognosis
            return {
                "two_year_survival": "16.2%",
                "prognostic_group": "Good",
                "contains_long_term_survivors": "Yes",
                "treatment_approach": "Curative intent"
            }
        elif total_score <= 3:  # Medium prognosis
            return {
                "two_year_survival": "2.5%",
                "prognostic_group": "Medium",
                "contains_long_term_survivors": "Rare",
                "treatment_approach": "Standard with monitoring"
            }
        else:  # Poor prognosis (4-6 points)
            return {
                "two_year_survival": "0%",
                "prognostic_group": "Poor",
                "contains_long_term_survivors": "No",
                "treatment_approach": "Palliative focus"
            }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the prognostic group and interpretation based on the total score
        
        Args:
            total_score (int): Total Manchester Score
            
        Returns:
            Dict with prognostic group and clinical interpretation
        """
        
        if total_score <= 1:  # Good prognosis (0-1 points)
            return {
                "stage": "Good Prognosis",
                "description": "Good prognostic group with best survival outcomes",
                "interpretation": (
                    "Good prognosis with 16.2% two-year survival rate. This prognostic group contains "
                    "all long-term survivors identified in the original Manchester study cohort. "
                    "Consider standard chemotherapy regimens with curative intent. Patients in this "
                    "group are suitable candidates for aggressive treatment approaches including "
                    "concurrent chemoradiotherapy for limited stage disease. Treatment decisions "
                    "should focus on achieving maximum therapeutic benefit while maintaining "
                    "acceptable quality of life. Regular monitoring for treatment response and "
                    "toxicity is recommended."
                )
            }
        elif total_score <= 3:  # Medium prognosis (2-3 points)
            return {
                "stage": "Medium Prognosis",
                "description": "Intermediate prognostic group with moderate survival outcomes",
                "interpretation": (
                    "Medium prognosis with 2.5% two-year survival rate. Consider standard treatment "
                    "protocols with careful monitoring for treatment tolerance and response. Balance "
                    "treatment intensity with quality of life considerations, as cure rates are low. "
                    "May benefit from supportive care measures alongside chemotherapy. Treatment "
                    "decisions should involve thorough discussion with patient and family regarding "
                    "goals of care, potential benefits, and expected outcomes. Consider palliative "
                    "care consultation early in the treatment course."
                )
            }
        else:  # Poor prognosis (4-6 points)
            return {
                "stage": "Poor Prognosis",
                "description": "Poor prognostic group with worst survival outcomes",
                "interpretation": (
                    "Poor prognosis with 0% two-year survival rate in the original study cohort. "
                    "No patients in this prognostic group survived longer than one year. Consider "
                    "palliative care approach with primary emphasis on symptom management and "
                    "quality of life optimization. Treatment decisions should focus on palliation "
                    "rather than cure. Early palliative care referral is strongly recommended. "
                    "Any chemotherapy should be given with palliative intent, and treatment "
                    "should be discontinued if no benefit or unacceptable toxicity occurs."
                )
            }


def calculate_manchester_score_prognosis_sclc(serum_ldh: str, serum_sodium: float, 
                                            serum_alkaline_phosphatase: str, serum_bicarbonate: float,
                                            disease_stage: str, karnofsky_performance_status: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ManchesterScorePrognosisSclcCalculator()
    return calculator.calculate(serum_ldh, serum_sodium, serum_alkaline_phosphatase, 
                               serum_bicarbonate, disease_stage, karnofsky_performance_status)