"""
IMDC (International Metastatic RCC Database Consortium) Risk Model Calculator

Predicts survival in patients with metastatic renal cell carcinoma treated with systemic therapy.
Originally developed by Heng et al. in 2009 and refined in 2013.

References (Vancouver style):
1. Heng DY, Xie W, Regan MM, Warren MA, Golshayan AR, Sahi C, et al. Prognostic factors for 
   overall survival in patients with metastatic renal cell carcinoma treated with vascular 
   endothelial growth factor-targeted agents: results from a large, multicenter study. 
   J Clin Oncol. 2009 Dec 1;27(34):5794-9. doi: 10.1200/JCO.2008.21.4809

2. Heng DY, Xie W, Regan MM, Harshman LC, Bjarnason GA, Vaishampayan UN, et al. External 
   validation and comparison with other models of the International Metastatic Renal-Cell 
   Carcinoma Database Consortium prognostic model: a population-based study. Lancet Oncol. 
   2013 Feb;14(2):141-8. doi: 10.1016/S1470-2045(12)70559-4

3. Motzer RJ, Tannir NM, McDermott DF, Arén Frontera O, Melichar B, Choueiri TK, et al. 
   Nivolumab plus Ipilimumab versus Sunitinib in Advanced Renal-Cell Carcinoma. N Engl J Med. 
   2018 Apr 5;378(14):1277-1290. doi: 10.1056/NEJMoa1712126
"""

from typing import Dict, Any


class ImdcRiskModelCalculator:
    """Calculator for IMDC Risk Model for Metastatic Renal Cell Carcinoma"""
    
    def __init__(self):
        # Risk factor points (each factor = 1 point if present)
        self.risk_factors = {
            "time_to_systemic_therapy": {"less_than_1_year": 1, "1_year_or_more": 0},
            "karnofsky_performance_status": {"less_than_80": 1, "80_or_more": 0},
            "hemoglobin": {"below_normal": 1, "normal_or_above": 0},
            "corrected_calcium": {"above_normal": 1, "normal_or_below": 0},
            "neutrophils": {"above_normal": 1, "normal_or_below": 0},
            "platelets": {"above_normal": 1, "normal_or_below": 0}
        }
        
        # Survival data from validation studies
        self.survival_data = {
            "favorable": {
                "median_os_months": 43.2,
                "range": "0 risk factors"
            },
            "intermediate": {
                "median_os_months": 22.5,
                "range": "1-2 risk factors"
            },
            "poor": {
                "median_os_months": 7.8,
                "range": "3-6 risk factors"
            }
        }
    
    def calculate(self, time_to_systemic_therapy: str, karnofsky_performance_status: str,
                  hemoglobin: str, corrected_calcium: str, neutrophils: str, 
                  platelets: str) -> Dict[str, Any]:
        """
        Calculates the IMDC risk score using the provided parameters
        
        Args:
            time_to_systemic_therapy (str): "less_than_1_year" or "1_year_or_more"
            karnofsky_performance_status (str): "less_than_80" or "80_or_more"
            hemoglobin (str): "below_normal" or "normal_or_above"
            corrected_calcium (str): "above_normal" or "normal_or_below"
            neutrophils (str): "above_normal" or "normal_or_below"
            platelets (str): "above_normal" or "normal_or_below"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(time_to_systemic_therapy, karnofsky_performance_status,
                             hemoglobin, corrected_calcium, neutrophils, platelets)
        
        # Calculate total score (sum of risk factors)
        total_score = self._calculate_score(
            time_to_systemic_therapy, karnofsky_performance_status,
            hemoglobin, corrected_calcium, neutrophils, platelets
        )
        
        # Get risk category and interpretation
        risk_assessment = self._get_risk_category(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["category"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, time_to_systemic_therapy: str, karnofsky_performance_status: str,
                        hemoglobin: str, corrected_calcium: str, neutrophils: str, 
                        platelets: str):
        """Validates input parameters"""
        
        # Validate time_to_systemic_therapy
        if time_to_systemic_therapy not in ["less_than_1_year", "1_year_or_more"]:
            raise ValueError("time_to_systemic_therapy must be 'less_than_1_year' or '1_year_or_more'")
        
        # Validate karnofsky_performance_status
        if karnofsky_performance_status not in ["less_than_80", "80_or_more"]:
            raise ValueError("karnofsky_performance_status must be 'less_than_80' or '80_or_more'")
        
        # Validate hemoglobin
        if hemoglobin not in ["below_normal", "normal_or_above"]:
            raise ValueError("hemoglobin must be 'below_normal' or 'normal_or_above'")
        
        # Validate corrected_calcium
        if corrected_calcium not in ["above_normal", "normal_or_below"]:
            raise ValueError("corrected_calcium must be 'above_normal' or 'normal_or_below'")
        
        # Validate neutrophils
        if neutrophils not in ["above_normal", "normal_or_below"]:
            raise ValueError("neutrophils must be 'above_normal' or 'normal_or_below'")
        
        # Validate platelets
        if platelets not in ["above_normal", "normal_or_below"]:
            raise ValueError("platelets must be 'above_normal' or 'normal_or_below'")
    
    def _calculate_score(self, time_to_systemic_therapy: str, karnofsky_performance_status: str,
                        hemoglobin: str, corrected_calcium: str, neutrophils: str, 
                        platelets: str) -> int:
        """Calculates the total IMDC risk score"""
        
        score = 0
        
        # Add points for each risk factor present
        score += self.risk_factors["time_to_systemic_therapy"][time_to_systemic_therapy]
        score += self.risk_factors["karnofsky_performance_status"][karnofsky_performance_status]
        score += self.risk_factors["hemoglobin"][hemoglobin]
        score += self.risk_factors["corrected_calcium"][corrected_calcium]
        score += self.risk_factors["neutrophils"][neutrophils]
        score += self.risk_factors["platelets"][platelets]
        
        return score
    
    def _get_risk_category(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and clinical interpretation based on the score
        
        Args:
            score (int): IMDC risk score (0-6)
            
        Returns:
            Dict with risk category and interpretation
        """
        
        if score == 0:
            return {
                "category": "Favorable Risk",
                "description": "0 risk factors",
                "interpretation": (
                    "Favorable prognosis with median overall survival of 43.2 months. "
                    "Consider pazopanib or sunitinib as first-line therapy. "
                    "These patients may not derive additional benefit from combination "
                    "immunotherapy compared to VEGF-targeted therapy alone."
                )
            }
        elif 1 <= score <= 2:
            return {
                "category": "Intermediate Risk",
                "description": "1-2 risk factors",
                "interpretation": (
                    "Intermediate prognosis with median overall survival of 22.5 months. "
                    "Consider ipilimumab plus nivolumab or cabozantinib as first-line therapy. "
                    "These patients derive significant survival benefit from combination "
                    "immunotherapy compared to sunitinib monotherapy."
                )
            }
        else:  # score >= 3
            return {
                "category": "Poor Risk",
                "description": "3-6 risk factors",
                "interpretation": (
                    "Poor prognosis with median overall survival of 7.8 months. "
                    "Consider ipilimumab plus nivolumab or cabozantinib as first-line therapy. "
                    "These patients have the greatest survival benefit from combination "
                    "immunotherapy. Early palliative care consultation should be considered."
                )
            }


def calculate_imdc_risk_model(time_to_systemic_therapy: str, karnofsky_performance_status: str,
                             hemoglobin: str, corrected_calcium: str, neutrophils: str, 
                             platelets: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_imdc_risk_model pattern
    """
    calculator = ImdcRiskModelCalculator()
    return calculator.calculate(
        time_to_systemic_therapy, karnofsky_performance_status,
        hemoglobin, corrected_calcium, neutrophils, platelets
    )