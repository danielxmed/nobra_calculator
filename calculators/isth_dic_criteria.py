"""
ISTH Criteria for Disseminated Intravascular Coagulation (DIC) Calculator

Diagnoses overt disseminated intravascular coagulation (DIC) based on laboratory parameters.
This scoring system was developed by the International Society on Thrombosis and Haemostasis (ISTH)
as a standardized approach to DIC diagnosis using readily available laboratory tests.

References:
1. Taylor FB Jr, Toh CH, Hoots WK, Wada H, Levi M; Scientific Subcommittee on Disseminated Intravascular Coagulation (DIC) of the International Society on Thrombosis and Haemostasis (ISTH). Towards definition, clinical and laboratory criteria, and a scoring system for disseminated intravascular coagulation. Thromb Haemost. 2001 Nov;86(5):1327-30.
2. Toh CH, Hoots WK; SSC on Disseminated Intravascular Coagulation of the ISTH. The scoring system of the Scientific and Standardisation Committee on Disseminated Intravascular Coagulation of the International Society on Thrombosis and Haemostasis: a 5-year overview. J Thromb Haemost. 2007 Mar;5(3):604-6.
3. Bakhtiari K, Meijers JC, de Jonge E, Levi M. Prospective validation of the International Society of Thrombosis and Haemostasis scoring system for disseminated intravascular coagulation. Crit Care Med. 2004 Dec;32(12):2416-21.
"""

from typing import Dict, Any


class IsthDicCriteriaCalculator:
    """Calculator for ISTH Criteria for Disseminated Intravascular Coagulation (DIC)"""
    
    def __init__(self):
        # Scoring values for each parameter
        self.PLATELET_SCORES = {
            "≥100": 0,
            "50-99": 1,
            "<50": 2
        }
        
        self.FIBRIN_MARKER_SCORES = {
            "no_increase": 0,
            "moderate_increase": 2,
            "severe_increase": 3
        }
        
        self.PT_PROLONGATION_SCORES = {
            "<3_seconds": 0,
            "3-5_seconds": 1,
            "≥6_seconds": 2
        }
        
        self.FIBRINOGEN_SCORES = {
            "≥1_g_L": 0,
            "<1_g_L": 1
        }
    
    def calculate(self, platelet_count: str, fibrin_marker: str, 
                 pt_prolongation: str, fibrinogen_level: str) -> Dict[str, Any]:
        """
        Calculates the ISTH DIC score
        
        Args:
            platelet_count (str): Platelet count category (≥100, 50-99, <50)
            fibrin_marker (str): Fibrin-related marker elevation level
            pt_prolongation (str): Prothrombin time prolongation category
            fibrinogen_level (str): Fibrinogen level category
            
        Returns:
            Dict with the DIC score and interpretation
        """
        
        # Validations
        self._validate_inputs(platelet_count, fibrin_marker, pt_prolongation, fibrinogen_level)
        
        # Calculate total score
        total_score = self._calculate_total_score(
            platelet_count, fibrin_marker, pt_prolongation, fibrinogen_level
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, platelet_count: str, fibrin_marker: str, 
                        pt_prolongation: str, fibrinogen_level: str):
        """Validates input parameters"""
        
        if platelet_count not in self.PLATELET_SCORES:
            raise ValueError(f"platelet_count must be one of: {list(self.PLATELET_SCORES.keys())}")
        
        if fibrin_marker not in self.FIBRIN_MARKER_SCORES:
            raise ValueError(f"fibrin_marker must be one of: {list(self.FIBRIN_MARKER_SCORES.keys())}")
        
        if pt_prolongation not in self.PT_PROLONGATION_SCORES:
            raise ValueError(f"pt_prolongation must be one of: {list(self.PT_PROLONGATION_SCORES.keys())}")
        
        if fibrinogen_level not in self.FIBRINOGEN_SCORES:
            raise ValueError(f"fibrinogen_level must be one of: {list(self.FIBRINOGEN_SCORES.keys())}")
    
    def _calculate_total_score(self, platelet_count: str, fibrin_marker: str, 
                             pt_prolongation: str, fibrinogen_level: str) -> int:
        """
        Calculates the total ISTH DIC score
        
        Args:
            platelet_count (str): Platelet count category
            fibrin_marker (str): Fibrin-related marker elevation
            pt_prolongation (str): PT prolongation category
            fibrinogen_level (str): Fibrinogen level category
            
        Returns:
            int: Total score (0-8 points)
        """
        
        total_score = (
            self.PLATELET_SCORES[platelet_count] +
            self.FIBRIN_MARKER_SCORES[fibrin_marker] +
            self.PT_PROLONGATION_SCORES[pt_prolongation] +
            self.FIBRINOGEN_SCORES[fibrinogen_level]
        )
        
        return total_score
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Gets clinical interpretation based on total score
        
        Args:
            total_score (int): Total ISTH DIC score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score >= 5:
            return {
                "stage": "Compatible with Overt DIC",
                "description": "Compatible with overt DIC",
                "interpretation": f"Score ≥5 points ({total_score} points): Compatible with overt DIC. Strong likelihood of overt disseminated intravascular coagulation based on ISTH criteria. This finding has 91-93% sensitivity and 97-98% specificity for overt DIC. Consider immediate treatment and management of underlying condition. Monitor closely with serial laboratory studies and address precipitating factors such as sepsis, malignancy, obstetric complications, or trauma."
            }
        else:
            return {
                "stage": "Not Suggestive",
                "description": "Not suggestive of overt DIC",
                "interpretation": f"Score <5 points ({total_score} points): Not suggestive of overt DIC. This score does not rule out disseminated intravascular coagulation but may indicate non-overt DIC or absence of DIC. Consider clinical context and reassessment if suspicion remains high or if the patient's clinical condition changes. Serial measurements may be more informative than a single assessment."
            }


def calculate_isth_dic_criteria(platelet_count: str, fibrin_marker: str, 
                               pt_prolongation: str, fibrinogen_level: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_isth_dic_criteria pattern
    """
    calculator = IsthDicCriteriaCalculator()
    return calculator.calculate(platelet_count, fibrin_marker, pt_prolongation, fibrinogen_level)