"""
National Comprehensive Cancer Network International Prognostic Index (NCCN-IPI) Calculator

Predicts survival in patients with diffuse large B-cell lymphoma (DLBCL).
Enhanced prognostic index developed for the rituximab era.

References:
1. Zhou Z, et al. Blood. 2014;123(6):837-42.
2. Ruppert AS, et al. Blood. 2020;135(23):2041-2048.
"""

from typing import Dict, Any


class NccnIpiCalculator:
    """Calculator for NCCN-IPI score in DLBCL patients"""
    
    def __init__(self):
        # Age scoring thresholds
        self.AGE_THRESHOLDS = [
            (40, 0),   # ≤40 years: 0 points
            (60, 1),   # >40-60 years: 1 point
            (75, 2),   # >60-75 years: 2 points
            (120, 3)   # >75 years: 3 points
        ]
        
        # LDH ratio scoring thresholds
        self.LDH_THRESHOLDS = [
            (1.0, 0),  # Normal (≤1× ULN): 0 points
            (3.0, 1),  # >1-3× ULN: 1 point
            (999, 2)   # ≥3× ULN: 2 points
        ]
    
    def calculate(self, age: int, ldh_ratio: float, extranodal_sites: str,
                  ann_arbor_stage: str, ecog_performance_status: int) -> Dict[str, Any]:
        """
        Calculates the NCCN-IPI score
        
        Args:
            age: Patient age in years
            ldh_ratio: LDH ratio (patient's LDH / upper limit of normal)
            extranodal_sites: "yes" if extranodal disease in major organs, "no" otherwise
            ann_arbor_stage: Ann Arbor stage ("I", "II", "III", or "IV")
            ecog_performance_status: ECOG performance status (0-4)
            
        Returns:
            Dict with score, unit, interpretation, stage, and stage description
        """
        # Validate inputs
        self._validate_inputs(age, ldh_ratio, extranodal_sites, 
                            ann_arbor_stage, ecog_performance_status)
        
        # Calculate total score
        total_score = 0
        
        # Age scoring
        age_points = self._calculate_age_points(age)
        total_score += age_points
        
        # LDH scoring
        ldh_points = self._calculate_ldh_points(ldh_ratio)
        total_score += ldh_points
        
        # Extranodal sites (1 point if yes)
        if extranodal_sites.lower() == "yes":
            total_score += 1
        
        # Ann Arbor stage (1 point if III or IV)
        if ann_arbor_stage in ["III", "IV"]:
            total_score += 1
        
        # ECOG performance status (1 point if ≥2)
        if ecog_performance_status >= 2:
            total_score += 1
        
        # Get interpretation based on score
        interpretation_data = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"],
            "components": {
                "age_points": age_points,
                "ldh_points": ldh_points,
                "extranodal_sites": 1 if extranodal_sites.lower() == "yes" else 0,
                "ann_arbor_stage": 1 if ann_arbor_stage in ["III", "IV"] else 0,
                "ecog_status": 1 if ecog_performance_status >= 2 else 0
            }
        }
    
    def _validate_inputs(self, age: int, ldh_ratio: float, extranodal_sites: str,
                        ann_arbor_stage: str, ecog_performance_status: int):
        """Validates input parameters"""
        if not isinstance(age, (int, float)) or age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        if not isinstance(ldh_ratio, (int, float)) or ldh_ratio < 0.1 or ldh_ratio > 20:
            raise ValueError("LDH ratio must be between 0.1 and 20")
        
        if extranodal_sites.lower() not in ["yes", "no"]:
            raise ValueError("Extranodal sites must be 'yes' or 'no'")
        
        if ann_arbor_stage not in ["I", "II", "III", "IV"]:
            raise ValueError("Ann Arbor stage must be I, II, III, or IV")
        
        if not isinstance(ecog_performance_status, int) or ecog_performance_status < 0 or ecog_performance_status > 4:
            raise ValueError("ECOG performance status must be between 0 and 4")
    
    def _calculate_age_points(self, age: int) -> int:
        """Calculates points based on age"""
        for threshold, points in self.AGE_THRESHOLDS:
            if age <= threshold:
                return points
        return 3  # >75 years
    
    def _calculate_ldh_points(self, ldh_ratio: float) -> int:
        """Calculates points based on LDH ratio"""
        for threshold, points in self.LDH_THRESHOLDS:
            if ldh_ratio <= threshold:
                return points
        return 2  # ≥3× ULN
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines risk group and interpretation based on NCCN-IPI score
        
        Args:
            score: Total NCCN-IPI score (0-8)
            
        Returns:
            Dict with stage, description, and interpretation
        """
        if score <= 1:
            return {
                "stage": "Low",
                "description": "Low risk",
                "interpretation": (
                    "5-year overall survival: 96%. Excellent prognosis with standard "
                    "R-CHOP chemotherapy. Consider clinical trials for de-escalation "
                    "strategies."
                )
            }
        elif score <= 3:
            return {
                "stage": "Low-Intermediate",
                "description": "Low-intermediate risk",
                "interpretation": (
                    "5-year overall survival: 82%. Good prognosis with standard therapy. "
                    "Standard R-CHOP remains appropriate."
                )
            }
        elif score <= 5:
            return {
                "stage": "High-Intermediate",
                "description": "High-intermediate risk",
                "interpretation": (
                    "5-year overall survival: 64%. Moderate prognosis. Consider intensified "
                    "therapy or clinical trials for novel agents."
                )
            }
        else:  # score >= 6
            return {
                "stage": "High",
                "description": "High risk",
                "interpretation": (
                    "5-year overall survival: 33%. Poor prognosis with standard therapy. "
                    "Strong consideration for intensive therapy, autologous stem cell "
                    "transplant, or clinical trials."
                )
            }


def calculate_nccn_ipi(age: int, ldh_ratio: float, extranodal_sites: str,
                      ann_arbor_stage: str, ecog_performance_status: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_nccn_ipi pattern
    """
    calculator = NccnIpiCalculator()
    return calculator.calculate(age, ldh_ratio, extranodal_sites,
                               ann_arbor_stage, ecog_performance_status)