"""
International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI) Calculator

Predicts overall and progression-free survival in diffuse large B-cell lymphoma (DLBCL) 
based on five independent risk factors. Provides both original IPI and revised R-IPI stratification.

References (Vancouver style):
1. A predictive model for aggressive non-Hodgkin's lymphoma. The International Non-Hodgkin's 
   Lymphoma Prognostic Factors Project. N Engl J Med. 1993 Sep 30;329(14):987-94. 
   doi: 10.1056/NEJM199309303291402.
2. The revised International Prognostic Index (R-IPI) is a better predictor of outcome than 
   the standard IPI for patients with diffuse large B-cell lymphoma treated with R-CHOP. 
   Blood. 2007 Mar 1;109(5):1857-61. doi: 10.1182/blood-2006-08-038257.
3. International prognostic indices in diffuse large B-cell lymphoma: a comparison of IPI, 
   R-IPI, and NCCN-IPI. Blood. 2020 Jun 11;135(23):2041-2048. 
   doi: 10.1182/blood.2019002729.
"""

from typing import Dict, Any


class DlbclIpiCalculator:
    """Calculator for International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI)"""
    
    def __init__(self):
        # Risk factor scoring weights - each factor contributes 1 point
        self.scoring_weights = {
            "age": {
                "60_or_younger": 0,
                "older_than_60": 1
            },
            "ldh_level": {
                "normal": 0,
                "elevated": 1
            },
            "ann_arbor_stage": {
                "stage_i_ii": 0,
                "stage_iii_iv": 1
            },
            "ecog_performance_status": {
                "0_1": 0,
                "2_or_higher": 1
            },
            "extranodal_sites": {
                "0_1_sites": 0,
                "more_than_1": 1
            }
        }
    
    def calculate(self, age: str, ldh_level: str, ann_arbor_stage: str, 
                  ecog_performance_status: str, extranodal_sites: str) -> Dict[str, Any]:
        """
        Calculates the IPI score using the provided parameters
        
        Args:
            age (str): Patient age category ("60_or_younger", "older_than_60")
            ldh_level (str): LDH level relative to ULN ("normal", "elevated")
            ann_arbor_stage (str): Disease stage ("stage_i_ii", "stage_iii_iv")
            ecog_performance_status (str): Performance status ("0_1", "2_or_higher")
            extranodal_sites (str): Number of extranodal sites ("0_1_sites", "more_than_1")
            
        Returns:
            Dict with the IPI score and interpretation for both IPI and R-IPI
        """
        
        # Validate inputs
        self._validate_inputs(age, ldh_level, ann_arbor_stage, ecog_performance_status, extranodal_sites)
        
        # Calculate total score
        total_score = self._calculate_total_score(age, ldh_level, ann_arbor_stage, 
                                                ecog_performance_status, extranodal_sites)
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, ldh_level: str, ann_arbor_stage: str, 
                        ecog_performance_status: str, extranodal_sites: str):
        """Validates input parameters"""
        
        # Validate age
        if age not in self.scoring_weights["age"]:
            raise ValueError(f"Age must be one of: {list(self.scoring_weights['age'].keys())}")
        
        # Validate LDH level
        if ldh_level not in self.scoring_weights["ldh_level"]:
            raise ValueError(f"LDH level must be one of: {list(self.scoring_weights['ldh_level'].keys())}")
        
        # Validate Ann Arbor stage
        if ann_arbor_stage not in self.scoring_weights["ann_arbor_stage"]:
            raise ValueError(f"Ann Arbor stage must be one of: {list(self.scoring_weights['ann_arbor_stage'].keys())}")
        
        # Validate ECOG performance status
        if ecog_performance_status not in self.scoring_weights["ecog_performance_status"]:
            raise ValueError(f"ECOG performance status must be one of: {list(self.scoring_weights['ecog_performance_status'].keys())}")
        
        # Validate extranodal sites
        if extranodal_sites not in self.scoring_weights["extranodal_sites"]:
            raise ValueError(f"Extranodal sites must be one of: {list(self.scoring_weights['extranodal_sites'].keys())}")
    
    def _calculate_total_score(self, age: str, ldh_level: str, ann_arbor_stage: str, 
                              ecog_performance_status: str, extranodal_sites: str) -> int:
        """Calculates the total IPI score"""
        
        total_score = 0
        total_score += self.scoring_weights["age"][age]
        total_score += self.scoring_weights["ldh_level"][ldh_level]
        total_score += self.scoring_weights["ann_arbor_stage"][ann_arbor_stage]
        total_score += self.scoring_weights["ecog_performance_status"][ecog_performance_status]
        total_score += self.scoring_weights["extranodal_sites"][extranodal_sites]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the IPI score
        
        Args:
            score (int): Calculated IPI score (0-5 points)
            
        Returns:
            Dict with risk stratification and clinical interpretation
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk (IPI) / Very Good (R-IPI)",
                "description": "Score 0-1 points",
                "interpretation": "Excellent prognosis. IPI Low Risk: 5-year OS ~73%. R-IPI Very Good: 4-year PFS 94%, OS 94%. Standard R-CHOP therapy appropriate. These patients have the best outcomes with conventional treatment and may be candidates for less intensive approaches in clinical trials."
            }
        elif score == 2:
            return {
                "stage": "Low-Intermediate Risk (IPI) / Good (R-IPI)",
                "description": "Score 2 points",
                "interpretation": "Good prognosis. IPI Low-Intermediate Risk: 5-year OS ~51%. R-IPI Good: Intermediate survival outcomes. Standard R-CHOP therapy recommended. Consider standard treatment approaches with close monitoring for response assessment."
            }
        elif score == 3:
            return {
                "stage": "High-Intermediate Risk (IPI) / Poor (R-IPI)",
                "description": "Score 3 points",
                "interpretation": "Intermediate prognosis. IPI High-Intermediate Risk: 5-year OS ~43%. R-IPI Poor: Lower survival expectations. Consider intensified treatment approaches, clinical trial enrollment, or novel therapeutic strategies. Close monitoring and aggressive supportive care recommended."
            }
        else:  # score >= 4
            return {
                "stage": "High Risk (IPI) / Poor (R-IPI)",
                "description": "Score 4-5 points",
                "interpretation": "Poor prognosis. IPI High Risk: 5-year OS ~26%. R-IPI Poor: Lowest survival expectations. Strong consideration for clinical trials, intensified regimens, or novel therapies. Consider CNS prophylaxis. Aggressive supportive care and close monitoring essential. May benefit from consolidative therapies."
            }


def calculate_dlbcl_ipi(age: str, ldh_level: str, ann_arbor_stage: str, 
                       ecog_performance_status: str, extranodal_sites: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the International Prognostic Index for DLBCL using five risk factors.
    Provides both original IPI (4 risk groups) and R-IPI (3 risk groups) stratification.
    
    Args:
        age (str): Patient age category
        ldh_level (str): LDH level relative to upper limit of normal
        ann_arbor_stage (str): Ann Arbor staging
        ecog_performance_status (str): ECOG performance status
        extranodal_sites (str): Number of extranodal disease sites
        
    Returns:
        Dict with IPI score and risk stratification
    """
    calculator = DlbclIpiCalculator()
    return calculator.calculate(age, ldh_level, ann_arbor_stage, ecog_performance_status, extranodal_sites)