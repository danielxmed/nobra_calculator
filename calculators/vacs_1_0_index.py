"""
Veterans Aging Cohort Study (VACS) 1.0 Index Calculator

Estimates 5-year all-cause mortality risk in patients with HIV and/or HCV by integrating 
HIV-specific biomarkers with general health indicators.

References:
1. Justice AC, McGinnis KA, Skanderson M, et al. Towards a combined prognostic index for 
   survival in HIV infection: the role of 'non-HIV' biomarkers. HIV Med. 2010;11(2):143-151.
2. Tate JP, Justice AC, Hughes MD, et al. An internationally generalizable risk index for 
   mortality prediction in HIV-infected adults. AIDS. 2013;27(4):563-572.
3. Justice AC, Dombrowski E, Conigliaro J, et al. Veterans Aging Cohort Study (VACS): 
   Overview and description. Med Care. 2006;44(8 Suppl 2):S13-24.
"""

from typing import Dict, Any


class Vacs10IndexCalculator:
    """Calculator for Veterans Aging Cohort Study (VACS) 1.0 Index"""
    
    def __init__(self):
        # VACS 1.0 Index scoring system
        self.AGE_POINTS = {
            (0, 49): 0,       # <50 years
            (50, 64): 12,     # 50-64 years
            (65, 150): 27     # ≥65 years
        }
        
        self.CD4_POINTS = {
            (500, 5000): 0,    # ≥500 cells/mm³
            (350, 499): 6,     # 350-499 cells/mm³
            (200, 349): 6,     # 200-349 cells/mm³
            (100, 199): 10,    # 100-199 cells/mm³
            (50, 99): 28,      # 50-99 cells/mm³
            (0, 49): 29        # <50 cells/mm³
        }
        
        self.HIV_RNA_POINTS = {
            (0, 499): 0,           # <500 copies/mL
            (500, 99999): 7,       # 500-99,999 copies/mL
            (100000, 10000000): 14 # ≥100,000 copies/mL
        }
        
        self.HEMOGLOBIN_POINTS = {
            (14.0, 25.0): 0,      # ≥14 g/dL
            (12.0, 13.9): 10,     # 12-13.9 g/dL
            (10.0, 11.9): 22,     # 10-11.9 g/dL
            (0.0, 9.9): 38        # <10 g/dL
        }
        
        self.FIB4_POINTS = {
            (0.0, 1.44): 0,       # <1.45
            (1.45, 3.25): 6,      # 1.45-3.25
            (3.26, 50.0): 25      # >3.25
        }
        
        self.EGFR_POINTS = {
            (60.0, 200.0): 0,     # ≥60 mL/min
            (45.0, 59.9): 6,      # 45-59.9 mL/min
            (30.0, 44.9): 8,      # 30-44.9 mL/min
            (0.0, 29.9): 26       # <30 mL/min
        }
        
        self.HCV_POINTS = {
            "no": 0,
            "yes": 5
        }
    
    def calculate(self, age: int, cd4_count: int, hiv_rna_copies_ml: int, 
                 hemoglobin_g_dl: float, fib4_index: float, egfr_ml_min: float,
                 hepatitis_c_coinfection: str) -> Dict[str, Any]:
        """
        Calculates the VACS 1.0 Index score
        
        Args:
            age (int): Patient's age in years
            cd4_count (int): CD4+ T cell count (cells/mm³)
            hiv_rna_copies_ml (int): HIV-1 RNA viral load (copies/mL)
            hemoglobin_g_dl (float): Hemoglobin level (g/dL)
            fib4_index (float): FIB-4 Index for liver fibrosis
            egfr_ml_min (float): Estimated glomerular filtration rate (mL/min/1.73m²)
            hepatitis_c_coinfection (str): HCV co-infection status ("yes"/"no")
            
        Returns:
            Dict with VACS score, risk assessment, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, cd4_count, hiv_rna_copies_ml, hemoglobin_g_dl, 
                            fib4_index, egfr_ml_min, hepatitis_c_coinfection)
        
        # Calculate component scores
        age_points = self._get_points_from_range(age, self.AGE_POINTS)
        cd4_points = self._get_points_from_range(cd4_count, self.CD4_POINTS)
        hiv_rna_points = self._get_points_from_range(hiv_rna_copies_ml, self.HIV_RNA_POINTS)
        hemoglobin_points = self._get_points_from_range(hemoglobin_g_dl, self.HEMOGLOBIN_POINTS)
        fib4_points = self._get_points_from_range(fib4_index, self.FIB4_POINTS)
        egfr_points = self._get_points_from_range(egfr_ml_min, self.EGFR_POINTS)
        hcv_points = self.HCV_POINTS[hepatitis_c_coinfection.lower()]
        
        # Calculate total VACS score
        vacs_score = (age_points + cd4_points + hiv_rna_points + hemoglobin_points + 
                     fib4_points + egfr_points + hcv_points)
        
        # Get interpretation
        interpretation = self._get_interpretation(vacs_score)
        
        # Create component breakdown
        component_breakdown = {
            "age_points": age_points,
            "cd4_points": cd4_points,
            "hiv_rna_points": hiv_rna_points,
            "hemoglobin_points": hemoglobin_points,
            "fib4_points": fib4_points,
            "egfr_points": egfr_points,
            "hcv_points": hcv_points
        }
        
        return {
            "result": vacs_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_breakdown": component_breakdown
        }
    
    def _validate_inputs(self, age: int, cd4_count: int, hiv_rna_copies_ml: int, 
                        hemoglobin_g_dl: float, fib4_index: float, egfr_ml_min: float,
                        hepatitis_c_coinfection: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(cd4_count, int) or cd4_count < 0 or cd4_count > 5000:
            raise ValueError("CD4 count must be an integer between 0 and 5000 cells/mm³")
        
        if not isinstance(hiv_rna_copies_ml, int) or hiv_rna_copies_ml < 0 or hiv_rna_copies_ml > 10000000:
            raise ValueError("HIV RNA must be an integer between 0 and 10,000,000 copies/mL")
        
        if not isinstance(hemoglobin_g_dl, (int, float)) or hemoglobin_g_dl < 3.0 or hemoglobin_g_dl > 25.0:
            raise ValueError("Hemoglobin must be between 3.0 and 25.0 g/dL")
        
        if not isinstance(fib4_index, (int, float)) or fib4_index < 0.0 or fib4_index > 50.0:
            raise ValueError("FIB-4 Index must be between 0.0 and 50.0")
        
        if not isinstance(egfr_ml_min, (int, float)) or egfr_ml_min < 0.0 or egfr_ml_min > 200.0:
            raise ValueError("eGFR must be between 0.0 and 200.0 mL/min/1.73m²")
        
        if hepatitis_c_coinfection.lower() not in ["yes", "no"]:
            raise ValueError("Hepatitis C co-infection must be 'yes' or 'no'")
    
    def _get_points_from_range(self, value: float, points_dict: Dict) -> int:
        """Gets points for a value based on range definitions"""
        
        for (min_val, max_val), points in points_dict.items():
            if min_val <= value <= max_val:
                return points
        
        # This should not happen with proper validation
        raise ValueError(f"Value {value} does not fall within any defined range")
    
    def _get_interpretation(self, vacs_score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on VACS score
        
        Args:
            vacs_score (int): Calculated VACS 1.0 Index score
            
        Returns:
            Dict with interpretation details
        """
        
        if vacs_score <= 20:
            return {
                "stage": "Low Risk",
                "description": "Low 5-year mortality risk",
                "interpretation": f"VACS 1.0 Index score of {vacs_score} indicates low 5-year mortality risk. "
                               f"Continue regular HIV care and monitoring. Focus on maintaining HIV suppression, "
                               f"adherence to antiretroviral therapy, and routine comorbidity screening. "
                               f"Standard follow-up intervals are appropriate."
            }
        elif vacs_score <= 40:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate 5-year mortality risk",
                "interpretation": f"VACS 1.0 Index score of {vacs_score} indicates moderate 5-year mortality risk. "
                               f"Enhanced monitoring recommended. Address modifiable risk factors including "
                               f"liver disease (FIB-4 optimization), kidney function preservation, and anemia management. "
                               f"Consider more frequent clinical evaluations and specialist consultations as needed."
            }
        elif vacs_score <= 60:
            return {
                "stage": "High Risk",
                "description": "High 5-year mortality risk",
                "interpretation": f"VACS 1.0 Index score of {vacs_score} indicates high 5-year mortality risk. "
                               f"Intensive management recommended. Prioritize aggressive treatment of liver disease, "
                               f"kidney dysfunction, and severe anemia. Consider hepatology, nephrology, and "
                               f"hematology referrals. Implement comprehensive care coordination and frequent monitoring."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high 5-year mortality risk",
                "interpretation": f"VACS 1.0 Index score of {vacs_score} indicates very high 5-year mortality risk. "
                               f"Urgent comprehensive management required. Immediate attention to life-threatening "
                               f"comorbidities including end-stage liver disease, kidney failure, and severe anemia. "
                               f"Consider multidisciplinary care team, aggressive interventions, and discussion of "
                               f"goals of care including palliative care options alongside curative treatments."
            }


def calculate_vacs_1_0_index(age: int, cd4_count: int, hiv_rna_copies_ml: int, 
                           hemoglobin_g_dl: float, fib4_index: float, egfr_ml_min: float,
                           hepatitis_c_coinfection: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_vacs_1_0_index pattern
    """
    calculator = Vacs10IndexCalculator()
    return calculator.calculate(age, cd4_count, hiv_rna_copies_ml, hemoglobin_g_dl, 
                              fib4_index, egfr_ml_min, hepatitis_c_coinfection)