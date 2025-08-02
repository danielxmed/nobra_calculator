"""
Mantle Cell Lymphoma International Prognostic Index (MIPI) Calculator

Predicts survival in mantle cell lymphoma patients using age, performance status,
lactate dehydrogenase level, and white blood cell count. Optionally calculates
biological MIPI (MIPIb) when Ki-67 proliferation index is available.

References:
1. Hoster E, Dreyling M, Klapper W, Gisselbrecht C, van Hoof A, Kluin-Nelemans HC, et al. 
   A new prognostic index (MIPI) for patients with advanced-stage mantle cell lymphoma. 
   Blood. 2008 Jan 15;111(2):558-65. doi: 10.1182/blood-2007-06-095331.
2. Hoster E, Klapper W, Hermine O, Kluin-Nelemans HC, Walewski J, Trneny M, et al. 
   Confirmation of the mantle-cell lymphoma International Prognostic Index in randomized 
   trials of the European Mantle-Cell Lymphoma Network. J Clin Oncol. 2014 May 1;32(13):1338-46. 
   doi: 10.1200/JCO.2013.52.2466.
"""

import math
from typing import Dict, Any, Optional


class MantleCellLymphomaInternationalPrognosticIndexCalculator:
    """Calculator for Mantle Cell Lymphoma International Prognostic Index (MIPI)"""
    
    def __init__(self):
        # MIPI formula coefficients
        self.AGE_COEFFICIENT = 0.03535
        self.ECOG_COEFFICIENT = 0.6978  # Added when ECOG 2-4
        self.LDH_COEFFICIENT = 1.367
        self.WBC_COEFFICIENT = 0.9393
        self.KI67_COEFFICIENT = 0.02142  # For biological MIPI (MIPIb)
        
        # Risk thresholds for MIPI
        self.LOW_RISK_THRESHOLD = 5.7
        self.HIGH_RISK_THRESHOLD = 6.2
        
        # Risk thresholds for MIPIb (when Ki-67 available)
        self.MIPIB_LOW_RISK_THRESHOLD = 5.7
        self.MIPIB_HIGH_RISK_THRESHOLD = 6.5
        
        # Valid options
        self.VALID_ECOG_OPTIONS = ["0_to_1", "2_to_4"]
    
    def calculate(self, age: int, ecog_performance_status: str, serum_ldh: float,
                  ldh_upper_limit_normal: float, white_blood_cell_count: float,
                  ki67_index: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates MIPI score for mantle cell lymphoma prognosis
        
        Args:
            age (int): Patient age in years
            ecog_performance_status (str): ECOG Performance Status ("0_to_1" or "2_to_4")
            serum_ldh (float): Serum LDH level in U/L
            ldh_upper_limit_normal (float): Upper limit of normal for LDH in U/L
            white_blood_cell_count (float): WBC count in ×10³/μL
            ki67_index (Optional[float]): Ki-67 proliferation index percentage (0-100)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, ecog_performance_status, serum_ldh, 
                             ldh_upper_limit_normal, white_blood_cell_count, ki67_index)
        
        # Calculate MIPI score
        mipi_score = self._calculate_mipi_score(
            age, ecog_performance_status, serum_ldh, 
            ldh_upper_limit_normal, white_blood_cell_count
        )
        
        # Calculate MIPIb if Ki-67 provided
        mipib_score = None
        if ki67_index is not None:
            mipib_score = mipi_score + (self.KI67_COEFFICIENT * ki67_index)
        
        # Determine which score to use for interpretation (prefer MIPIb if available)
        primary_score = mipib_score if mipib_score is not None else mipi_score
        score_type = "MIPIb" if mipib_score is not None else "MIPI"
        
        # Get interpretation
        interpretation = self._get_interpretation(primary_score, score_type)
        
        # Prepare detailed results
        result_data = {
            "mipi_score": round(mipi_score, 3),
            "score_type": score_type,
            "score_components": {
                "age_component": round(self.AGE_COEFFICIENT * age, 3),
                "ecog_component": self.ECOG_COEFFICIENT if ecog_performance_status == "2_to_4" else 0,
                "ldh_component": round(self.LDH_COEFFICIENT * math.log10(serum_ldh / ldh_upper_limit_normal), 3),
                "wbc_component": round(self.WBC_COEFFICIENT * math.log10(white_blood_cell_count), 3)
            },
            "ldh_ratio": round(serum_ldh / ldh_upper_limit_normal, 2),
            "clinical_parameters": {
                "age_years": age,
                "ecog_status": ecog_performance_status.replace("_", "-"),
                "ldh_level": f"{serum_ldh} U/L",
                "ldh_uln": f"{ldh_upper_limit_normal} U/L",
                "wbc_count": f"{white_blood_cell_count} ×10³/μL"
            }
        }
        
        # Add MIPIb specific data if available
        if mipib_score is not None:
            result_data["mipib_score"] = round(mipib_score, 3)
            result_data["score_components"]["ki67_component"] = round(self.KI67_COEFFICIENT * ki67_index, 3)
            result_data["clinical_parameters"]["ki67_index"] = f"{ki67_index}%"
        
        return {
            "result": result_data,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, ecog_performance_status: str, serum_ldh: float,
                        ldh_upper_limit_normal: float, white_blood_cell_count: float,
                        ki67_index: Optional[float]):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18 or age > 100:
            raise ValueError("Age must be between 18 and 100 years")
        
        # Validate ECOG performance status
        if not isinstance(ecog_performance_status, str):
            raise ValueError("ECOG performance status must be a string")
        
        if ecog_performance_status not in self.VALID_ECOG_OPTIONS:
            raise ValueError(f"ECOG performance status must be one of {self.VALID_ECOG_OPTIONS}")
        
        # Validate serum LDH
        if not isinstance(serum_ldh, (int, float)):
            raise ValueError("Serum LDH must be a number")
        
        if serum_ldh <= 0 or serum_ldh > 10000:
            raise ValueError("Serum LDH must be between 1 and 10000 U/L")
        
        # Validate LDH upper limit normal
        if not isinstance(ldh_upper_limit_normal, (int, float)):
            raise ValueError("LDH upper limit normal must be a number")
        
        if ldh_upper_limit_normal <= 0 or ldh_upper_limit_normal > 400:
            raise ValueError("LDH upper limit normal must be between 1 and 400 U/L")
        
        # Validate WBC count
        if not isinstance(white_blood_cell_count, (int, float)):
            raise ValueError("White blood cell count must be a number")
        
        if white_blood_cell_count <= 0 or white_blood_cell_count > 500:
            raise ValueError("White blood cell count must be between 0.1 and 500 ×10³/μL")
        
        # Validate Ki-67 index if provided
        if ki67_index is not None:
            if not isinstance(ki67_index, (int, float)):
                raise ValueError("Ki-67 index must be a number")
            
            if ki67_index < 0 or ki67_index > 100:
                raise ValueError("Ki-67 index must be between 0 and 100%")
    
    def _calculate_mipi_score(self, age: int, ecog_performance_status: str, 
                             serum_ldh: float, ldh_upper_limit_normal: float,
                             white_blood_cell_count: float) -> float:
        """Calculates the MIPI score using the original formula"""
        
        # Age component
        age_component = self.AGE_COEFFICIENT * age
        
        # ECOG component (added only if ECOG 2-4)
        ecog_component = self.ECOG_COEFFICIENT if ecog_performance_status == "2_to_4" else 0
        
        # LDH component (logarithmic)
        ldh_ratio = serum_ldh / ldh_upper_limit_normal
        ldh_component = self.LDH_COEFFICIENT * math.log10(ldh_ratio)
        
        # WBC component (logarithmic)
        wbc_component = self.WBC_COEFFICIENT * math.log10(white_blood_cell_count)
        
        # Calculate total MIPI score
        mipi_score = age_component + ecog_component + ldh_component + wbc_component
        
        return mipi_score
    
    def _get_interpretation(self, score: float, score_type: str) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on score
        
        Args:
            score (float): MIPI or MIPIb score
            score_type (str): "MIPI" or "MIPIb"
            
        Returns:
            Dict with risk category and clinical interpretation
        """
        
        # Use appropriate thresholds based on score type
        if score_type == "MIPIb":
            low_threshold = self.MIPIB_LOW_RISK_THRESHOLD
            high_threshold = self.MIPIB_HIGH_RISK_THRESHOLD
        else:
            low_threshold = self.LOW_RISK_THRESHOLD
            high_threshold = self.HIGH_RISK_THRESHOLD
        
        if score < low_threshold:
            return {
                "stage": "Low Risk",
                "description": "Low risk for poor prognosis",
                "interpretation": (
                    f"{score_type} score of {score:.3f} indicates low risk group. "
                    f"These patients have a 5-year overall survival rate of approximately 60% "
                    f"with median survival not reached in original studies. Consider standard "
                    f"chemotherapy regimens such as R-CHOP or R-bendamustine. These patients "
                    f"may be candidates for less intensive treatment approaches or observation "
                    f"in selected cases. Regular monitoring and reassessment during treatment "
                    f"course remains important for treatment modifications."
                )
            }
        elif score < high_threshold:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate risk for poor prognosis",
                "interpretation": (
                    f"{score_type} score of {score:.3f} indicates intermediate risk group. "
                    f"These patients have a median survival of approximately 51 months "
                    f"{'(58 months for MIPIb)' if score_type == 'MIPIb' else ''}. "
                    f"Systemic treatment is typically required at diagnosis. Consider intensive "
                    f"chemotherapy regimens such as R-CHOP, R-bendamustine, or clinical trial "
                    f"participation. May benefit from consolidation with autologous stem cell "
                    f"transplantation in first remission. Risk-adapted treatment approach is "
                    f"recommended based on patient age, comorbidities, and treatment tolerance."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk for poor prognosis",
                "interpretation": (
                    f"{score_type} score of {score:.3f} indicates high risk group. "
                    f"These patients have a median survival of approximately 29 months "
                    f"{'(37 months for MIPIb)' if score_type == 'MIPIb' else ''}. "
                    f"Immediate intensive treatment is required. Consider aggressive "
                    f"chemotherapy regimens, clinical trial participation, or novel targeted "
                    f"therapies. Strong consideration for consolidation with autologous stem "
                    f"cell transplantation in first remission. May benefit from maintenance "
                    f"therapy or experimental approaches. Close monitoring and early intervention "
                    f"for disease progression is essential."
                )
            }


def calculate_mantle_cell_lymphoma_international_prognostic_index(
    age: int, ecog_performance_status: str, serum_ldh: float,
    ldh_upper_limit_normal: float, white_blood_cell_count: float,
    ki67_index: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MantleCellLymphomaInternationalPrognosticIndexCalculator()
    return calculator.calculate(age, ecog_performance_status, serum_ldh,
                               ldh_upper_limit_normal, white_blood_cell_count, ki67_index)