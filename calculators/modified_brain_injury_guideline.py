"""
Modified Brain Injury Guideline (mBIG) Calculator

Defines management of traumatic brain injury by stratifying patients into 
three categories based on clinical and radiographic factors.

References:
1. Joseph B, et al. J Trauma Acute Care Surg. 2014;77(4):597-605.
2. Hartwell EA, et al. J Trauma Acute Care Surg. 2022;92(4):e92-e98.
"""

from typing import Dict, Any


class ModifiedBrainInjuryGuidelineCalculator:
    """Calculator for Modified Brain Injury Guideline (mBIG)"""
    
    def __init__(self):
        # mBIG 3 criteria (highest severity)
        self.MBIG_3_CRITERIA = [
            'anticoagulation_antiplatelet',
            'epidural_hematoma',
            'intraventricular_hemorrhage',
            'displaced_skull_fracture'
        ]
        
        # mBIG 2 criteria (intermediate severity)
        self.MBIG_2_CRITERIA = [
            'blood_alcohol_over_80',
            'nondisplaced_skull_fracture'
        ]
    
    def calculate(self, anticoagulation_antiplatelet: str, epidural_hematoma: str,
                  intraventricular_hemorrhage: str, displaced_skull_fracture: str,
                  subdural_hematoma_size: str, intraparenchymal_hemorrhage_size: str,
                  subarachnoid_hemorrhage_extent: str, blood_alcohol_level: str,
                  nondisplaced_skull_fracture: str) -> Dict[str, Any]:
        """
        Calculates the Modified Brain Injury Guideline (mBIG) classification
        
        Args:
            anticoagulation_antiplatelet (str): Anticoagulation/antiplatelet medication use
            epidural_hematoma (str): Presence of epidural hematoma
            intraventricular_hemorrhage (str): Presence of intraventricular hemorrhage
            displaced_skull_fracture (str): Presence of displaced skull fracture
            subdural_hematoma_size (str): Size category of subdural hematoma
            intraparenchymal_hemorrhage_size (str): Size/number of intraparenchymal hemorrhages
            subarachnoid_hemorrhage_extent (str): Extent of subarachnoid hemorrhage
            blood_alcohol_level (str): Blood alcohol level category
            nondisplaced_skull_fracture (str): Presence of nondisplaced skull fracture
            
        Returns:
            Dict with mBIG classification and management recommendations
        """
        
        # Validate inputs
        self._validate_inputs(anticoagulation_antiplatelet, epidural_hematoma,
                            intraventricular_hemorrhage, displaced_skull_fracture,
                            subdural_hematoma_size, intraparenchymal_hemorrhage_size,
                            subarachnoid_hemorrhage_extent, blood_alcohol_level,
                            nondisplaced_skull_fracture)
        
        # Check for mBIG 3 criteria (highest priority)
        if self._has_mbig_3_criteria(anticoagulation_antiplatelet, epidural_hematoma,
                                   intraventricular_hemorrhage, displaced_skull_fracture,
                                   subdural_hematoma_size, intraparenchymal_hemorrhage_size,
                                   subarachnoid_hemorrhage_extent):
            category = 3
        
        # Check for mBIG 2 criteria (intermediate priority)
        elif self._has_mbig_2_criteria(blood_alcohol_level, nondisplaced_skull_fracture,
                                     subdural_hematoma_size, intraparenchymal_hemorrhage_size,
                                     subarachnoid_hemorrhage_extent):
            category = 2
        
        # Default to mBIG 1 (lowest severity)
        else:
            category = 1
        
        # Get interpretation
        interpretation = self._get_interpretation(category)
        
        return {
            "result": category,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, anticoagulation_antiplatelet: str, epidural_hematoma: str,
                        intraventricular_hemorrhage: str, displaced_skull_fracture: str,
                        subdural_hematoma_size: str, intraparenchymal_hemorrhage_size: str,
                        subarachnoid_hemorrhage_extent: str, blood_alcohol_level: str,
                        nondisplaced_skull_fracture: str):
        """Validates input parameters"""
        
        # Valid options for yes/no parameters
        yes_no_options = ["yes", "no"]
        
        # Validate yes/no parameters
        if anticoagulation_antiplatelet not in yes_no_options:
            raise ValueError("anticoagulation_antiplatelet must be 'yes' or 'no'")
        if epidural_hematoma not in yes_no_options:
            raise ValueError("epidural_hematoma must be 'yes' or 'no'")
        if intraventricular_hemorrhage not in yes_no_options:
            raise ValueError("intraventricular_hemorrhage must be 'yes' or 'no'")
        if displaced_skull_fracture not in yes_no_options:
            raise ValueError("displaced_skull_fracture must be 'yes' or 'no'")
        if nondisplaced_skull_fracture not in yes_no_options:
            raise ValueError("nondisplaced_skull_fracture must be 'yes' or 'no'")
        
        # Validate subdural hematoma size
        valid_sdh_sizes = ["none", "4mm_or_less", "4_to_8mm", "8mm_or_more"]
        if subdural_hematoma_size not in valid_sdh_sizes:
            raise ValueError(f"subdural_hematoma_size must be one of: {', '.join(valid_sdh_sizes)}")
        
        # Validate intraparenchymal hemorrhage size
        valid_iph_sizes = ["none", "4mm_or_less_single", "4_to_8mm_single", "8mm_or_more_or_multiple"]
        if intraparenchymal_hemorrhage_size not in valid_iph_sizes:
            raise ValueError(f"intraparenchymal_hemorrhage_size must be one of: {', '.join(valid_iph_sizes)}")
        
        # Validate subarachnoid hemorrhage extent
        valid_sah_extents = ["none", "limited_1_3mm", "1_hemisphere_over_3_sulci_1_3mm", "bihemispheric_or_over_3mm"]
        if subarachnoid_hemorrhage_extent not in valid_sah_extents:
            raise ValueError(f"subarachnoid_hemorrhage_extent must be one of: {', '.join(valid_sah_extents)}")
        
        # Validate blood alcohol level
        valid_alcohol_levels = ["unknown_or_under_80", "over_80_mg_dl"]
        if blood_alcohol_level not in valid_alcohol_levels:
            raise ValueError(f"blood_alcohol_level must be one of: {', '.join(valid_alcohol_levels)}")
    
    def _has_mbig_3_criteria(self, anticoagulation_antiplatelet: str, epidural_hematoma: str,
                           intraventricular_hemorrhage: str, displaced_skull_fracture: str,
                           subdural_hematoma_size: str, intraparenchymal_hemorrhage_size: str,
                           subarachnoid_hemorrhage_extent: str) -> bool:
        """Check if patient meets any mBIG 3 criteria"""
        
        # Direct mBIG 3 criteria
        if anticoagulation_antiplatelet == "yes":
            return True
        if epidural_hematoma == "yes":
            return True
        if intraventricular_hemorrhage == "yes":
            return True
        if displaced_skull_fracture == "yes":
            return True
        
        # Size-based mBIG 3 criteria
        if subdural_hematoma_size == "8mm_or_more":
            return True
        if intraparenchymal_hemorrhage_size == "8mm_or_more_or_multiple":
            return True
        if subarachnoid_hemorrhage_extent == "bihemispheric_or_over_3mm":
            return True
        
        return False
    
    def _has_mbig_2_criteria(self, blood_alcohol_level: str, nondisplaced_skull_fracture: str,
                           subdural_hematoma_size: str, intraparenchymal_hemorrhage_size: str,
                           subarachnoid_hemorrhage_extent: str) -> bool:
        """Check if patient meets any mBIG 2 criteria"""
        
        # Direct mBIG 2 criteria
        if blood_alcohol_level == "over_80_mg_dl":
            return True
        if nondisplaced_skull_fracture == "yes":
            return True
        
        # Size-based mBIG 2 criteria
        if subdural_hematoma_size == "4_to_8mm":
            return True
        if intraparenchymal_hemorrhage_size == "4_to_8mm_single":
            return True
        if subarachnoid_hemorrhage_extent == "1_hemisphere_over_3_sulci_1_3mm":
            return True
        
        return False
    
    def _get_interpretation(self, category: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mBIG category
        
        Args:
            category: mBIG category (1, 2, or 3)
            
        Returns:
            Dict with interpretation details
        """
        
        if category == 1:
            return {
                "stage": "mBIG 1",
                "description": "Lowest severity - No admission required",
                "interpretation": ("mBIG 1 classification indicates lowest severity traumatic brain injury. "
                                "Management: 6-hour ED observation with Q2 neurological assessments. "
                                "No repeat head CT required, no neurosurgery consultation needed. "
                                "Patient can be safely discharged when GCS returns to 15. "
                                "This approach has been validated to be safe and significantly reduces "
                                "resource utilization.")
            }
        elif category == 2:
            return {
                "stage": "mBIG 2",
                "description": "Intermediate severity - Hospital admission",
                "interpretation": ("mBIG 2 classification indicates intermediate severity traumatic brain injury. "
                                "Management: Hospital admission to general medical floor for 24-48 hours. "
                                "Q2 neurological assessments required. No repeat head CT needed, "
                                "no neurosurgery consultation required. Discharge when GCS returns to 15. "
                                "This category balances safety with resource conservation.")
            }
        else:  # category == 3
            return {
                "stage": "mBIG 3",
                "description": "Highest severity - Standard of care",
                "interpretation": ("mBIG 3 classification indicates highest severity traumatic brain injury. "
                                "Management: Continue with standard of care at your institution. "
                                "Requires neurosurgical consultation and intensive monitoring. "
                                "These patients have significant intracranial pathology requiring "
                                "full neurosurgical evaluation and management.")
            }


def calculate_modified_brain_injury_guideline(anticoagulation_antiplatelet: str,
                                           epidural_hematoma: str,
                                           intraventricular_hemorrhage: str,
                                           displaced_skull_fracture: str,
                                           subdural_hematoma_size: str,
                                           intraparenchymal_hemorrhage_size: str,
                                           subarachnoid_hemorrhage_extent: str,
                                           blood_alcohol_level: str,
                                           nondisplaced_skull_fracture: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedBrainInjuryGuidelineCalculator()
    return calculator.calculate(anticoagulation_antiplatelet, epidural_hematoma,
                              intraventricular_hemorrhage, displaced_skull_fracture,
                              subdural_hematoma_size, intraparenchymal_hemorrhage_size,
                              subarachnoid_hemorrhage_extent, blood_alcohol_level,
                              nondisplaced_skull_fracture)