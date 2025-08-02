"""
Multiple Myeloma International Staging System (ISS) Calculator

Prognosticates severity of multiple myeloma based on routinely obtained lab values
including serum β2 microglobulin and albumin levels.

References:
1. Greipp PR, et al. J Clin Oncol. 2005;23(15):3412-20.
2. Durie BG, et al. Cancer. 1975;36(3):842-54.
3. Palumbo A, et al. J Clin Oncol. 2015;33(26):2863-9.
"""

from typing import Dict, Any


class MultipleMyelomaIssCalculator:
    """Calculator for Multiple Myeloma International Staging System (ISS)"""
    
    def __init__(self):
        # ISS staging thresholds
        self.BETA2_MICROGLOBULIN_STAGE_I_THRESHOLD = 3.5  # mg/L
        self.BETA2_MICROGLOBULIN_STAGE_III_THRESHOLD = 5.5  # mg/L
        self.ALBUMIN_THRESHOLD = 3.5  # g/dL
        
        # Median overall survival data (months)
        self.SURVIVAL_DATA = {
            "Stage I": 62,
            "Stage II": 44,
            "Stage III": 29
        }
    
    def calculate(self, serum_beta2_microglobulin: float, serum_albumin: float) -> Dict[str, Any]:
        """
        Calculates the ISS stage for multiple myeloma
        
        Args:
            serum_beta2_microglobulin (float): Serum β2 microglobulin level in mg/L
            serum_albumin (float): Serum albumin level in g/dL
            
        Returns:
            Dict with ISS stage and prognostic interpretation
        """
        
        # Validate inputs
        self._validate_inputs(serum_beta2_microglobulin, serum_albumin)
        
        # Determine ISS stage
        stage = self._determine_stage(serum_beta2_microglobulin, serum_albumin)
        
        # Get interpretation
        interpretation = self._get_interpretation(stage, serum_beta2_microglobulin, serum_albumin)
        
        return {
            "result": stage,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, serum_beta2_microglobulin: float, serum_albumin: float):
        """Validates input parameters"""
        
        if not isinstance(serum_beta2_microglobulin, (int, float)):
            raise ValueError("Serum β2 microglobulin must be a number")
        
        if not isinstance(serum_albumin, (int, float)):
            raise ValueError("Serum albumin must be a number")
        
        if serum_beta2_microglobulin < 0.1 or serum_beta2_microglobulin > 50.0:
            raise ValueError("Serum β2 microglobulin must be between 0.1 and 50.0 mg/L")
        
        if serum_albumin < 1.0 or serum_albumin > 6.0:
            raise ValueError("Serum albumin must be between 1.0 and 6.0 g/dL")
    
    def _determine_stage(self, serum_beta2_microglobulin: float, serum_albumin: float) -> str:
        """Determines ISS stage based on lab values"""
        
        # Stage I: β2 microglobulin <3.5 mg/L AND albumin ≥3.5 g/dL
        if (serum_beta2_microglobulin < self.BETA2_MICROGLOBULIN_STAGE_I_THRESHOLD and 
            serum_albumin >= self.ALBUMIN_THRESHOLD):
            return "Stage I"
        
        # Stage III: β2 microglobulin ≥5.5 mg/L (regardless of albumin)
        elif serum_beta2_microglobulin >= self.BETA2_MICROGLOBULIN_STAGE_III_THRESHOLD:
            return "Stage III"
        
        # Stage II: Everything else
        # Either: (β2 microglobulin <3.5 mg/L AND albumin <3.5 g/dL) 
        # OR: (β2 microglobulin 3.5-5.4 mg/L regardless of albumin)
        else:
            return "Stage II"
    
    def _get_interpretation(self, stage: str, serum_beta2_microglobulin: float, 
                          serum_albumin: float) -> Dict[str, str]:
        """
        Provides prognostic interpretation based on ISS stage
        
        Args:
            stage (str): ISS stage
            serum_beta2_microglobulin (float): β2 microglobulin level
            serum_albumin (float): Albumin level
            
        Returns:
            Dict with interpretation details
        """
        
        median_survival = self.SURVIVAL_DATA[stage]
        
        if stage == "Stage I":
            return {
                "stage": "Stage I",
                "description": "Best prognosis",
                "interpretation": (
                    f"ISS Stage I Multiple Myeloma: β2 microglobulin {serum_beta2_microglobulin} mg/L (<3.5) "
                    f"and albumin {serum_albumin} g/dL (≥3.5). "
                    f"PROGNOSIS: Best prognostic group with median overall survival of {median_survival} months. "
                    f"CLINICAL SIGNIFICANCE: Patients in this stage have the lowest tumor burden and best "
                    f"nutritional status. They typically respond well to standard treatment regimens and have "
                    f"the longest expected survival. "
                    f"MANAGEMENT RECOMMENDATIONS: Standard induction therapy appropriate for transplant-eligible "
                    f"or transplant-ineligible patients based on age and comorbidities. Consider autologous "
                    f"stem cell transplant if eligible. Regular monitoring for disease progression and treatment "
                    f"response. "
                    f"FOLLOW-UP: Monitor β2 microglobulin and albumin levels along with other myeloma markers "
                    f"(M-protein, free light chains) every 3-6 months during treatment and follow-up."
                )
            }
        
        elif stage == "Stage II":
            return {
                "stage": "Stage II",
                "description": "Intermediate prognosis",
                "interpretation": (
                    f"ISS Stage II Multiple Myeloma: Either β2 microglobulin {serum_beta2_microglobulin} mg/L "
                    f"(<3.5) with albumin {serum_albumin} g/dL (<3.5), OR β2 microglobulin 3.5-5.4 mg/L "
                    f"(regardless of albumin level). "
                    f"PROGNOSIS: Intermediate prognostic group with median overall survival of {median_survival} months. "
                    f"CLINICAL SIGNIFICANCE: Patients have moderate tumor burden or compromised nutritional status. "
                    f"Disease characteristics fall between Stage I and Stage III in terms of expected outcomes. "
                    f"MANAGEMENT RECOMMENDATIONS: Standard induction therapy with close monitoring for treatment "
                    f"response and toxicity. Autologous stem cell transplant should be considered if patient is "
                    f"eligible. May benefit from more intensive supportive care if albumin is low. Nutritional "
                    f"assessment and optimization may be beneficial. "
                    f"FOLLOW-UP: Close monitoring every 2-3 months during active treatment. Watch for progression "
                    f"to higher stage or development of complications."
                )
            }
        
        else:  # Stage III
            return {
                "stage": "Stage III",
                "description": "Poorest prognosis",
                "interpretation": (
                    f"ISS Stage III Multiple Myeloma: β2 microglobulin {serum_beta2_microglobulin} mg/L (≥5.5) "
                    f"regardless of albumin level ({serum_albumin} g/dL). "
                    f"PROGNOSIS: Poorest prognostic group with median overall survival of {median_survival} months. "
                    f"CLINICAL SIGNIFICANCE: Highest tumor burden and/or compromised kidney function. These patients "
                    f"have the most aggressive disease course and shortest expected survival. "
                    f"MANAGEMENT RECOMMENDATIONS: Aggressive induction therapy if patient can tolerate. Consider "
                    f"novel agent combinations and clinical trial enrollment. Autologous stem cell transplant "
                    f"if eligible, though benefit may be limited. Intensive supportive care including management "
                    f"of kidney dysfunction, bone disease, and other complications. Early palliative care "
                    f"consultation may be appropriate. "
                    f"FOLLOW-UP: Very close monitoring every 1-2 months. Monitor kidney function closely as "
                    f"elevated β2 microglobulin may reflect renal impairment. Consider more frequent imaging "
                    f"for bone disease surveillance."
                )
            }


def calculate_multiple_myeloma_iss(serum_beta2_microglobulin: float, 
                                   serum_albumin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MultipleMyelomaIssCalculator()
    return calculator.calculate(serum_beta2_microglobulin, serum_albumin)