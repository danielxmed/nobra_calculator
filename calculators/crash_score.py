"""
Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) Score Calculator

Predicts risk of severe chemotherapy toxicity in older cancer patients (≥70 years).
Assesses both hematologic (grade 4) and nonhematologic (grade 3/4) toxicities.

References:
1. Extermann M, et al. Predicting the risk of chemotherapy toxicity in older patients: 
   the Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) score. 
   Cancer. 2012;118(13):3377-86.
2. Extermann M, et al. Chemotoxicity recalibration in the common terminology criteria 
   for adverse events version 4.0 in older patients with cancer. 
   J Geriatr Oncol. 2013;4(4):353-8.
"""

from typing import Dict, Any


class CrashScoreCalculator:
    """Calculator for Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH)"""
    
    def __init__(self):
        # Define point values for hematologic toxicity parameters
        self.hematologic_points = {
            "diastolic_bp": {
                "lte_72": 0,   # ≤72 mmHg
                "gt_72": 1     # >72 mmHg
            },
            "iadl_score": {
                "26_to_29": 0,  # 26-29 (better function)
                "10_to_25": 1   # 10-25
            },
            "ldh": {
                "0_to_459": 0,  # 0-459 U/L
                "gt_459": 2     # >459 U/L
            },
            "chemo_risk_hematologic": {
                "0_to_0.44": 0,     # 0-0.44
                "0.45_to_0.57": 1,  # 0.45-0.57
                "gt_0.57": 2        # >0.57
            }
        }
        
        # Define point values for nonhematologic toxicity parameters
        self.nonhematologic_points = {
            "ecog_ps": {
                "0": 0,        # ECOG 0
                "1_to_2": 1,   # ECOG 1-2
                "3_to_4": 2    # ECOG 3-4
            },
            "mmse": {
                "30": 0,       # Perfect score
                "lt_30": 2     # <30
            },
            "mna": {
                "28_to_30": 0, # 28-30 (normal)
                "lt_28": 2     # <28
            },
            "chemo_risk_nonhematologic": {
                "0": 0,
                "1": 1,
                "2": 2
            }
        }
    
    def calculate(self, diastolic_bp: str, iadl_score: str, ldh: str,
                  chemo_risk_hematologic: str, ecog_ps: str, mmse: str,
                  mna: str, chemo_risk_nonhematologic: str) -> Dict[str, Any]:
        """
        Calculates the CRASH score
        
        Args:
            diastolic_bp: Diastolic blood pressure category
            iadl_score: IADL score category
            ldh: LDH level category
            chemo_risk_hematologic: Chemotherapy risk for hematologic toxicity
            ecog_ps: ECOG Performance Status
            mmse: Mini Mental State Examination score
            mna: Mini Nutritional Assessment score
            chemo_risk_nonhematologic: Chemotherapy risk for nonhematologic toxicity
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(diastolic_bp, iadl_score, ldh, chemo_risk_hematologic,
                            ecog_ps, mmse, mna, chemo_risk_nonhematologic)
        
        # Calculate hematologic subscore
        hematologic_score = (
            self.hematologic_points["diastolic_bp"][diastolic_bp] +
            self.hematologic_points["iadl_score"][iadl_score] +
            self.hematologic_points["ldh"][ldh] +
            self.hematologic_points["chemo_risk_hematologic"][chemo_risk_hematologic]
        )
        
        # Calculate nonhematologic subscore
        nonhematologic_score = (
            self.nonhematologic_points["ecog_ps"][ecog_ps] +
            self.nonhematologic_points["mmse"][mmse] +
            self.nonhematologic_points["mna"][mna] +
            self.nonhematologic_points["chemo_risk_nonhematologic"][chemo_risk_nonhematologic]
        )
        
        # Calculate combined score
        # Note: When combining scores, chemotherapy risk is counted only once
        # We use the maximum of the two chemotherapy risk scores
        chemo_risk_combined = max(
            self.hematologic_points["chemo_risk_hematologic"][chemo_risk_hematologic],
            self.nonhematologic_points["chemo_risk_nonhematologic"][chemo_risk_nonhematologic]
        )
        
        # Combined score excludes duplicate chemotherapy risk
        combined_score = (
            self.hematologic_points["diastolic_bp"][diastolic_bp] +
            self.hematologic_points["iadl_score"][iadl_score] +
            self.hematologic_points["ldh"][ldh] +
            self.nonhematologic_points["ecog_ps"][ecog_ps] +
            self.nonhematologic_points["mmse"][mmse] +
            self.nonhematologic_points["mna"][mna] +
            chemo_risk_combined
        )
        
        # Get interpretations
        hematologic_interpretation = self._get_hematologic_interpretation(hematologic_score)
        nonhematologic_interpretation = self._get_nonhematologic_interpretation(nonhematologic_score)
        combined_interpretation = self._get_combined_interpretation(combined_score)
        
        return {
            "result": {
                "combined_score": combined_score,
                "hematologic_score": hematologic_score,
                "nonhematologic_score": nonhematologic_score
            },
            "unit": "points",
            "interpretation": combined_interpretation["interpretation"],
            "stage": combined_interpretation["risk_category"],
            "stage_description": combined_interpretation["description"],
            "subscores": {
                "hematologic": {
                    "score": hematologic_score,
                    "risk": hematologic_interpretation["risk_category"],
                    "interpretation": hematologic_interpretation["interpretation"]
                },
                "nonhematologic": {
                    "score": nonhematologic_score,
                    "risk": nonhematologic_interpretation["risk_category"],
                    "interpretation": nonhematologic_interpretation["interpretation"]
                }
            }
        }
    
    def _validate_inputs(self, diastolic_bp: str, iadl_score: str, ldh: str,
                        chemo_risk_hematologic: str, ecog_ps: str, mmse: str,
                        mna: str, chemo_risk_nonhematologic: str):
        """Validates input parameters"""
        
        if diastolic_bp not in self.hematologic_points["diastolic_bp"]:
            raise ValueError(f"Invalid diastolic BP category: {diastolic_bp}")
        
        if iadl_score not in self.hematologic_points["iadl_score"]:
            raise ValueError(f"Invalid IADL score category: {iadl_score}")
        
        if ldh not in self.hematologic_points["ldh"]:
            raise ValueError(f"Invalid LDH category: {ldh}")
        
        if chemo_risk_hematologic not in self.hematologic_points["chemo_risk_hematologic"]:
            raise ValueError(f"Invalid hematologic chemotherapy risk: {chemo_risk_hematologic}")
        
        if ecog_ps not in self.nonhematologic_points["ecog_ps"]:
            raise ValueError(f"Invalid ECOG PS: {ecog_ps}")
        
        if mmse not in self.nonhematologic_points["mmse"]:
            raise ValueError(f"Invalid MMSE category: {mmse}")
        
        if mna not in self.nonhematologic_points["mna"]:
            raise ValueError(f"Invalid MNA category: {mna}")
        
        if chemo_risk_nonhematologic not in self.nonhematologic_points["chemo_risk_nonhematologic"]:
            raise ValueError(f"Invalid nonhematologic chemotherapy risk: {chemo_risk_nonhematologic}")
    
    def _get_hematologic_interpretation(self, score: int) -> Dict[str, str]:
        """Get hematologic toxicity risk interpretation"""
        
        if score <= 1:
            return {
                "risk_category": "Low",
                "interpretation": "Low risk (~7%) of grade 4 hematologic toxicity"
            }
        elif score <= 3:
            return {
                "risk_category": "Low-Intermediate",
                "interpretation": "Low-intermediate risk (~23%) of grade 4 hematologic toxicity"
            }
        elif score <= 5:
            return {
                "risk_category": "Intermediate-High",
                "interpretation": "Intermediate-high risk (~54%) of grade 4 hematologic toxicity"
            }
        else:
            return {
                "risk_category": "High",
                "interpretation": "High risk (~100%) of grade 4 hematologic toxicity"
            }
    
    def _get_nonhematologic_interpretation(self, score: int) -> Dict[str, str]:
        """Get nonhematologic toxicity risk interpretation"""
        
        if score <= 2:
            return {
                "risk_category": "Low",
                "interpretation": "Low risk (~33%) of grade 3/4 nonhematologic toxicity"
            }
        elif score <= 4:
            return {
                "risk_category": "Low-Intermediate",
                "interpretation": "Low-intermediate risk (~46%) of grade 3/4 nonhematologic toxicity"
            }
        elif score <= 6:
            return {
                "risk_category": "Intermediate-High",
                "interpretation": "Intermediate-high risk (~67%) of grade 3/4 nonhematologic toxicity"
            }
        else:
            return {
                "risk_category": "High",
                "interpretation": "High risk (~93%) of grade 3/4 nonhematologic toxicity"
            }
    
    def _get_combined_interpretation(self, score: int) -> Dict[str, str]:
        """Get combined CRASH score interpretation"""
        
        if score <= 3:
            return {
                "risk_category": "Low",
                "description": "Low risk",
                "interpretation": "Low risk for severe chemotherapy toxicity. Standard chemotherapy dosing may be appropriate with routine monitoring."
            }
        elif score <= 6:
            return {
                "risk_category": "Low-Intermediate",
                "description": "Low-intermediate risk",
                "interpretation": "Low-intermediate risk for severe chemotherapy toxicity. Consider close monitoring and early intervention strategies."
            }
        elif score <= 9:
            return {
                "risk_category": "Intermediate-High",
                "description": "Intermediate-high risk",
                "interpretation": "Intermediate-high risk for severe chemotherapy toxicity. Consider dose reduction, prophylactic measures, or alternative therapies."
            }
        else:
            return {
                "risk_category": "High",
                "description": "High risk",
                "interpretation": "High risk for severe chemotherapy toxicity. Strongly consider dose reduction, alternative less toxic regimens, or supportive care alone."
            }


def calculate_crash_score(diastolic_bp: str, iadl_score: str, ldh: str,
                         chemo_risk_hematologic: str, ecog_ps: str, mmse: str,
                         mna: str, chemo_risk_nonhematologic: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CrashScoreCalculator()
    return calculator.calculate(diastolic_bp, iadl_score, ldh, chemo_risk_hematologic,
                               ecog_ps, mmse, mna, chemo_risk_nonhematologic)