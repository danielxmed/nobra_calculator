"""
Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block Calculator

Diagnoses acute myocardial infarction in patients with prior left bundle branch block
using improved ECG criteria with better sensitivity than the original Sgarbossa criteria.

References:
1. Smith SW, et al. Ann Emerg Med. 2012;60(6):766-76.
2. Sgarbossa EB, et al. N Engl J Med. 1996;334(8):481-7.
3. Aslanger EK, et al. Ann Noninvasive Electrocardiol. 2015;20(1):12-20.
"""

from typing import Dict, Any


class ModifiedSgarbossaCriteriaCalculator:
    """Calculator for Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block"""
    
    def __init__(self):
        # Criterion mappings
        self.CRITERION_MAPPING = {
            "present": True,
            "absent": False
        }
    
    def calculate(self, concordant_st_elevation: str, concordant_st_depression: str, 
                  discordant_st_elevation_ratio: str) -> Dict[str, Any]:
        """
        Evaluates Modified Sgarbossa criteria for acute MI in LBBB
        
        Args:
            concordant_st_elevation (str): Concordant ST elevation ≥1 mm in leads with positive QRS
            concordant_st_depression (str): Concordant ST depression ≥1 mm in V1-V3
            discordant_st_elevation_ratio (str): Discordant ST elevation with ST/S ratio ≥-0.25
            
        Returns:
            Dict with Modified Sgarbossa criteria result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(concordant_st_elevation, concordant_st_depression, 
                             discordant_st_elevation_ratio)
        
        # Convert criteria to boolean values
        criterion_1 = self.CRITERION_MAPPING[concordant_st_elevation]
        criterion_2 = self.CRITERION_MAPPING[concordant_st_depression]
        criterion_3 = self.CRITERION_MAPPING[discordant_st_elevation_ratio]
        
        # Calculate result
        criteria_met = [criterion_1, criterion_2, criterion_3]
        positive_criteria_count = sum(criteria_met)
        
        # Determine result
        is_positive = positive_criteria_count > 0
        
        # Get interpretation
        interpretation = self._get_interpretation(is_positive, criteria_met)
        
        return {
            "result": "Positive" if is_positive else "Negative",
            "unit": "interpretation",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, concordant_st_elevation: str, concordant_st_depression: str,
                        discordant_st_elevation_ratio: str):
        """Validates input parameters"""
        
        valid_options = list(self.CRITERION_MAPPING.keys())
        
        if concordant_st_elevation not in valid_options:
            raise ValueError(f"Concordant ST elevation must be one of: {valid_options}")
        
        if concordant_st_depression not in valid_options:
            raise ValueError(f"Concordant ST depression must be one of: {valid_options}")
        
        if discordant_st_elevation_ratio not in valid_options:
            raise ValueError(f"Discordant ST elevation ratio must be one of: {valid_options}")
    
    def _get_interpretation(self, is_positive: bool, criteria_met: list) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Modified Sgarbossa criteria
        
        Args:
            is_positive (bool): Whether any criteria are positive
            criteria_met (list): List of boolean values for each criterion
            
        Returns:
            Dict with interpretation details
        """
        
        # Create detailed criteria summary
        criteria_names = [
            "Concordant ST elevation ≥1 mm",
            "Concordant ST depression ≥1 mm in V1-V3", 
            "Discordant ST elevation with ST/S ratio ≥-0.25"
        ]
        
        positive_criteria = [name for name, met in zip(criteria_names, criteria_met) if met]
        
        if is_positive:
            positive_list = "; ".join(positive_criteria)
            return {
                "stage": "Positive",
                "description": "At least one criterion met",
                "interpretation": (f"Modified Sgarbossa criteria POSITIVE for acute myocardial infarction "
                                f"in the setting of left bundle branch block. Positive criteria: {positive_list}. "
                                f"This result indicates a high likelihood of acute ST-elevation myocardial "
                                f"infarction (STEMI) despite the presence of LBBB. The Modified Sgarbossa "
                                f"criteria have 80% sensitivity and 99% specificity for acute MI in LBBB. "
                                f"Immediate cardiology consultation and emergent cardiac catheterization should "
                                f"be considered. This finding should be interpreted in conjunction with clinical "
                                f"presentation, cardiac biomarkers, and other diagnostic modalities. The modified "
                                f"criteria improve upon the original Sgarbossa criteria by using the ST/S ratio "
                                f"instead of absolute ST elevation measurements, significantly improving sensitivity.")
            }
        else:
            return {
                "stage": "Negative", 
                "description": "No criteria met",
                "interpretation": (f"Modified Sgarbossa criteria NEGATIVE for acute myocardial infarction "
                                f"in the setting of left bundle branch block. None of the three criteria "
                                f"are met: 1) No concordant ST elevation ≥1 mm in leads with positive QRS "
                                f"complex; 2) No concordant ST depression ≥1 mm in leads V1-V3; 3) No "
                                f"discordant ST elevation with ST/S ratio ≥-0.25. While this reduces the "
                                f"likelihood of acute STEMI, it does not completely rule out myocardial "
                                f"infarction. Clinical correlation with symptoms, cardiac biomarkers, and "
                                f"serial ECGs remains essential. Consider other causes of chest pain and "
                                f"alternative diagnostic approaches if clinical suspicion remains high. "
                                f"The negative likelihood ratio is 0.1, meaning acute MI is significantly "
                                f"less likely but not completely excluded.")
            }


def calculate_modified_sgarbossa_criteria(concordant_st_elevation: str, concordant_st_depression: str,
                                        discordant_st_elevation_ratio: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedSgarbossaCriteriaCalculator()
    return calculator.calculate(concordant_st_elevation, concordant_st_depression, 
                               discordant_st_elevation_ratio)