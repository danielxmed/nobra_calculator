"""
Swede Score Calculator

Predicts colposcopically high-grade lesions (HGL) on histology in cervical 
cancer screening. This standardized colposcopy scoring system evaluates five 
key characteristics to guide clinical decision-making and treatment planning 
for cervical intraepithelial neoplasia.

References (Vancouver style):
1. Strander B, Andersson-Ellström A, Milsom I, Rådberg T, Ryd W. Liquid-based 
   cytology versus conventional Papanicolaou smear in an organized screening 
   program : a prospective randomized study. Cancer. 2007 Dec 25;111(6):285-91. 
   doi: 10.1002/cncr.23100.
2. Bowring J, Strander B, Young M, Evans H, Walker P. The Swede score: evaluation 
   of a scoring system designed to improve the predictive value of colposcopy. 
   J Low Genit Tract Dis. 2010 Oct;14(4):301-5. doi: 10.1097/LGT.0b013e3181d77756.
"""

from typing import Dict, Any


class SwedeScoreCalculator:
    """Calculator for Swede Score colposcopy assessment"""
    
    def __init__(self):
        # Scoring tables for each parameter
        self.ACETO_UPTAKE_SCORES = {
            "None or transparent": 0,
            "Shady, milky": 1,
            "Distinct, opaque white": 2
        }
        
        self.MARGINS_SURFACE_SCORES = {
            "Diffuse": 0,
            "Sharp but irregular, jagged": 1,
            "Sharp and even, with surface level difference": 2
        }
        
        self.VESSELS_SCORES = {
            "Fine, regular": 0,
            "Absent": 1,
            "Coarse or atypical": 2
        }
        
        self.LESION_SIZE_SCORES = {
            "<5 mm": 0,
            "5-15 mm or 2 quadrants": 1,
            ">15 mm or 3-4 quadrants": 2
        }
        
        self.IODINE_STAINING_SCORES = {
            "Brown": 0,
            "Faintly or patchy yellow": 1,
            "Distinct yellow": 2
        }
        
        # Risk thresholds
        self.LOW_RISK_THRESHOLD = 4      # <5 = low risk
        self.INTERMEDIATE_RISK_THRESHOLD = 7  # 5-7 = intermediate risk
        # ≥8 = high risk (see and treat)
    
    def calculate(self, aceto_uptake: str, margins_surface: str, vessels: str,
                  lesion_size: str, iodine_staining: str) -> Dict[str, Any]:
        """
        Calculates the Swede Score for colposcopic assessment
        
        The Swede Score is a standardized colposcopy scoring system that 
        evaluates five key characteristics of cervical lesions to predict 
        the likelihood of high-grade cervical intraepithelial neoplasia (CIN). 
        This tool helps guide clinical decision-making regarding biopsy, 
        treatment, or surveillance strategies.
        
        Args:
            aceto_uptake (str): Acetowhite uptake after acetic acid application
            margins_surface (str): Characteristics of lesion margins and surface
            vessels (str): Vascular pattern observed during colposcopy
            lesion_size (str): Size of lesion or number of quadrants involved
            iodine_staining (str): Iodine staining pattern (Schiller's test)
            
        Returns:
            Dict with the calculated score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(aceto_uptake, margins_surface, vessels, lesion_size, iodine_staining)
        
        # Calculate individual component scores
        aceto_score = self._get_aceto_score(aceto_uptake)
        margins_score = self._get_margins_score(margins_surface)
        vessels_score = self._get_vessels_score(vessels)
        size_score = self._get_size_score(lesion_size)
        iodine_score = self._get_iodine_score(iodine_staining)
        
        # Calculate total score
        total_score = aceto_score + margins_score + vessels_score + size_score + iodine_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, aceto_uptake: str, margins_surface: str, vessels: str,
                        lesion_size: str, iodine_staining: str):
        """Validates input parameters for the Swede Score calculation"""
        
        # Aceto uptake validation
        if not isinstance(aceto_uptake, str):
            raise ValueError("Aceto uptake must be a string")
        
        if aceto_uptake not in self.ACETO_UPTAKE_SCORES:
            valid_options = list(self.ACETO_UPTAKE_SCORES.keys())
            raise ValueError(f"Aceto uptake must be one of: {valid_options}")
        
        # Margins/surface validation
        if not isinstance(margins_surface, str):
            raise ValueError("Margins/surface must be a string")
        
        if margins_surface not in self.MARGINS_SURFACE_SCORES:
            valid_options = list(self.MARGINS_SURFACE_SCORES.keys())
            raise ValueError(f"Margins/surface must be one of: {valid_options}")
        
        # Vessels validation
        if not isinstance(vessels, str):
            raise ValueError("Vessels must be a string")
        
        if vessels not in self.VESSELS_SCORES:
            valid_options = list(self.VESSELS_SCORES.keys())
            raise ValueError(f"Vessels must be one of: {valid_options}")
        
        # Lesion size validation
        if not isinstance(lesion_size, str):
            raise ValueError("Lesion size must be a string")
        
        if lesion_size not in self.LESION_SIZE_SCORES:
            valid_options = list(self.LESION_SIZE_SCORES.keys())
            raise ValueError(f"Lesion size must be one of: {valid_options}")
        
        # Iodine staining validation
        if not isinstance(iodine_staining, str):
            raise ValueError("Iodine staining must be a string")
        
        if iodine_staining not in self.IODINE_STAINING_SCORES:
            valid_options = list(self.IODINE_STAINING_SCORES.keys())
            raise ValueError(f"Iodine staining must be one of: {valid_options}")
    
    def _get_aceto_score(self, aceto_uptake: str) -> int:
        """Gets the score for acetowhite uptake"""
        return self.ACETO_UPTAKE_SCORES[aceto_uptake]
    
    def _get_margins_score(self, margins_surface: str) -> int:
        """Gets the score for margins and surface characteristics"""
        return self.MARGINS_SURFACE_SCORES[margins_surface]
    
    def _get_vessels_score(self, vessels: str) -> int:
        """Gets the score for vascular pattern"""
        return self.VESSELS_SCORES[vessels]
    
    def _get_size_score(self, lesion_size: str) -> int:
        """Gets the score for lesion size"""
        return self.LESION_SIZE_SCORES[lesion_size]
    
    def _get_iodine_score(self, iodine_staining: str) -> int:
        """Gets the score for iodine staining pattern"""
        return self.IODINE_STAINING_SCORES[iodine_staining]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the Swede Score
        
        Args:
            score (int): Total Swede Score (0-10)
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if score <= self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low suspicion for high-grade lesion",
                "interpretation": (
                    f"Swede Score of {score} indicates low risk for high-grade cervical "
                    f"lesion. Studies show that 97.3% of patients with scores <5 have "
                    f"normal or low-grade lesions. Consider routine follow-up with "
                    f"repeat cytology and HPV testing per guidelines, or targeted biopsy "
                    f"only if high clinical suspicion persists. This score has high "
                    f"negative predictive value for excluding high-grade disease, making "
                    f"conservative management appropriate in most cases."
                )
            }
        
        elif score <= self.INTERMEDIATE_RISK_THRESHOLD:
            return {
                "stage": "Intermediate Risk",
                "description": "Consider biopsy based on clinical suspicion",
                "interpretation": (
                    f"Swede Score of {score} indicates intermediate risk for high-grade "
                    f"cervical lesion. This score range requires careful clinical judgment "
                    f"and correlation with cytology, HPV testing, and patient risk factors. "
                    f"Consider colposcopy-directed biopsy for histopathological confirmation "
                    f"before treatment planning. Multiple biopsies may be needed to adequately "
                    f"sample suspicious areas. Close follow-up is essential regardless of "
                    f"biopsy results, as sampling may miss occult high-grade disease."
                )
            }
        
        else:  # score >= 8
            return {
                "stage": "High Risk",
                "description": "Concerning for high-grade lesion",
                "interpretation": (
                    f"Swede Score of {score} indicates high suspicion for high-grade "
                    f"cervical lesion. This score has 90-100% specificity for high-grade "
                    f"CIN and warrants immediate intervention. Consider excisional treatment "
                    f"(LEEP, cone biopsy) at the time of colposcopy using a 'see and treat' "
                    f"approach. This strategy reduces patient visits, prevents loss to "
                    f"follow-up, and provides both diagnostic and therapeutic benefits. "
                    f"Ensure adequate excision margins and send specimen for histopathological "
                    f"evaluation to confirm diagnosis and assess completeness of excision."
                )
            }


def calculate_swede_score(aceto_uptake: str, margins_surface: str, vessels: str,
                         lesion_size: str, iodine_staining: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the Swede Score for colposcopic assessment of cervical lesions.
    
    Args:
        aceto_uptake (str): Acetowhite uptake after acetic acid application
        margins_surface (str): Characteristics of lesion margins and surface
        vessels (str): Vascular pattern observed during colposcopy
        lesion_size (str): Size of lesion or number of quadrants involved
        iodine_staining (str): Iodine staining pattern (Schiller's test)
        
    Returns:
        Dict with calculated score and clinical interpretation
    """
    calculator = SwedeScoreCalculator()
    return calculator.calculate(aceto_uptake, margins_surface, vessels, lesion_size, iodine_staining)