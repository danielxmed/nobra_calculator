"""
ASAS Criteria for Peripheral SpondyloArthritis (SpA) Calculator

Assessment of SpondyloArthritis International Society (ASAS) classification 
criteria for peripheral spondyloarthritis.

References (Vancouver style):
1. Rudwaleit M, van der Heijde D, Landewé R, Listing J, Akkoc N, Brandt J, et al. 
   The Assessment of SpondyloArthritis International Society classification criteria 
   for peripheral spondyloarthritis and for spondyloarthritis in general. 
   Ann Rheum Dis. 2011 Jan;70(1):25-31. doi: 10.1136/ard.2010.133645.
2. Sieper J, Rudwaleit M, Baraliakos X, Brandt J, Braun J, Burgos-Vargas R, et al. 
   The Assessment of SpondyloArthritis international Society (ASAS) handbook: 
   a guide to assess spondyloarthritis. Ann Rheum Dis. 2009;68 Suppl 2:ii1-44. 
   doi: 10.1136/ard.2008.104018.

The ASAS criteria for peripheral SpA classify patients with predominant peripheral 
manifestations. The criteria require an entry criterion (arthritis and/or enthesitis 
and/or dactylitis) plus additional SpA features.
"""

from typing import Dict, Any


class AsasPeripheralSpaCriteriaCalculator:
    """Calculator for ASAS Criteria for Peripheral SpondyloArthritis"""
    
    def __init__(self):
        # Group A features (need 1 or more)
        self.group_a_features = [
            'psoriasis',
            'inflammatory_bowel_disease', 
            'preceding_infection',
            'hla_b27',
            'uveitis_anterior',
            'sacroiliitis_imaging'
        ]
        
        # Group B features (need 2 or more)
        self.group_b_features = [
            'peripheral_arthritis',
            'enthesitis',
            'dactylitis',
            'inflammatory_back_pain_past',
            'family_history_spa'
        ]
    
    def calculate(self, peripheral_arthritis: str, enthesitis: str, dactylitis: str,
                 psoriasis: str, inflammatory_bowel_disease: str, preceding_infection: str,
                 hla_b27: str, uveitis_anterior: str, sacroiliitis_imaging: str,
                 inflammatory_back_pain_past: str, family_history_spa: str) -> Dict[str, Any]:
        """
        Calculates ASAS criteria for peripheral spondyloarthritis
        
        Args:
            peripheral_arthritis (str): Peripheral arthritis present
            enthesitis (str): Enthesitis present
            dactylitis (str): Dactylitis present
            psoriasis (str): Psoriasis present
            inflammatory_bowel_disease (str): IBD present
            preceding_infection (str): Preceding infection present
            hla_b27 (str): HLA-B27 positive
            uveitis_anterior (str): Anterior uveitis present
            sacroiliitis_imaging (str): Sacroiliitis on imaging
            inflammatory_back_pain_past (str): History of IBP
            family_history_spa (str): Family history of SpA
            
        Returns:
            Dict with classification result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            peripheral_arthritis, enthesitis, dactylitis, psoriasis,
            inflammatory_bowel_disease, preceding_infection, hla_b27,
            uveitis_anterior, sacroiliitis_imaging, inflammatory_back_pain_past,
            family_history_spa
        )
        
        # Check entry criterion
        entry_criterion_met = self._check_entry_criterion(
            peripheral_arthritis, enthesitis, dactylitis
        )
        
        if not entry_criterion_met:
            return {
                "result": "Peripheral SpA Criteria NOT Met",
                "unit": "",
                "interpretation": "Entry criterion not fulfilled. Patient must have arthritis and/or enthesitis and/or dactylitis to be classified as peripheral SpA.",
                "stage": "Entry criterion not met",
                "stage_description": "Does not meet basic entry requirements"
            }
        
        # Count Group A features
        group_a_count = self._count_group_a_features(
            psoriasis, inflammatory_bowel_disease, preceding_infection,
            hla_b27, uveitis_anterior, sacroiliitis_imaging
        )
        
        # Count Group B features  
        group_b_count = self._count_group_b_features(
            peripheral_arthritis, enthesitis, dactylitis,
            inflammatory_back_pain_past, family_history_spa
        )
        
        # Determine if criteria are met
        criteria_met = (group_a_count >= 1) or (group_b_count >= 2)
        
        if criteria_met:
            interpretation_details = self._get_positive_interpretation(
                group_a_count, group_b_count
            )
            return {
                "result": "Peripheral SpA Criteria Met",
                "unit": "",
                "interpretation": interpretation_details,
                "stage": "Criteria fulfilled",
                "stage_description": "Meets ASAS criteria for peripheral spondyloarthritis"
            }
        else:
            return {
                "result": "Peripheral SpA Criteria NOT Met",
                "unit": "",
                "interpretation": f"Entry criterion met but insufficient SpA features present. Group A features: {group_a_count}/6 (need ≥1), Group B features: {group_b_count}/5 (need ≥2). Patient needs either ≥1 Group A feature OR ≥2 Group B features.",
                "stage": "Insufficient features",
                "stage_description": "Entry criterion met but lacks required SpA features"
            }
    
    def _validate_inputs(self, *args):
        """Validates all input parameters"""
        for arg in args:
            if not isinstance(arg, str):
                raise ValueError("All parameters must be strings")
            if arg not in ["yes", "no"]:
                raise ValueError("All parameters must be 'yes' or 'no'")
    
    def _check_entry_criterion(self, peripheral_arthritis: str, enthesitis: str, 
                              dactylitis: str) -> bool:
        """
        Checks if entry criterion is met
        Entry criterion: arthritis and/or enthesitis and/or dactylitis
        """
        return (peripheral_arthritis == "yes" or 
                enthesitis == "yes" or 
                dactylitis == "yes")
    
    def _count_group_a_features(self, psoriasis: str, inflammatory_bowel_disease: str,
                               preceding_infection: str, hla_b27: str, uveitis_anterior: str,
                               sacroiliitis_imaging: str) -> int:
        """
        Counts Group A features present
        Group A: psoriasis, IBD, preceding infection, HLA-B27, uveitis, sacroiliitis
        """
        features = [
            psoriasis, inflammatory_bowel_disease, preceding_infection,
            hla_b27, uveitis_anterior, sacroiliitis_imaging
        ]
        return sum(1 for feature in features if feature == "yes")
    
    def _count_group_b_features(self, peripheral_arthritis: str, enthesitis: str,
                               dactylitis: str, inflammatory_back_pain_past: str,
                               family_history_spa: str) -> int:
        """
        Counts Group B features present
        Group B: arthritis, enthesitis, dactylitis, IBP past, family history SpA
        """
        features = [
            peripheral_arthritis, enthesitis, dactylitis,
            inflammatory_back_pain_past, family_history_spa
        ]
        return sum(1 for feature in features if feature == "yes")
    
    def _get_positive_interpretation(self, group_a_count: int, group_b_count: int) -> str:
        """
        Returns detailed interpretation for positive cases
        """
        interpretation = "Patient meets the ASAS classification criteria for peripheral spondyloarthritis. "
        interpretation += "Entry criterion (arthritis and/or enthesitis and/or dactylitis) is fulfilled. "
        
        if group_a_count >= 1 and group_b_count >= 2:
            interpretation += f"Both pathways satisfied: {group_a_count} Group A feature(s) (≥1 required) AND {group_b_count} Group B features (≥2 required)."
        elif group_a_count >= 1:
            interpretation += f"Group A pathway satisfied: {group_a_count} Group A feature(s) present (≥1 required). Group B features: {group_b_count}/5."
        else:
            interpretation += f"Group B pathway satisfied: {group_b_count} Group B features present (≥2 required). Group A features: {group_a_count}/6."
        
        interpretation += " Note: These are classification criteria for research purposes, not diagnostic criteria for clinical practice."
        
        return interpretation


def calculate_asas_peripheral_spa_criteria(peripheral_arthritis: str, enthesitis: str,
                                         dactylitis: str, psoriasis: str, 
                                         inflammatory_bowel_disease: str, preceding_infection: str,
                                         hla_b27: str, uveitis_anterior: str, 
                                         sacroiliitis_imaging: str, inflammatory_back_pain_past: str,
                                         family_history_spa: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AsasPeripheralSpaCriteriaCalculator()
    return calculator.calculate(
        peripheral_arthritis, enthesitis, dactylitis, psoriasis,
        inflammatory_bowel_disease, preceding_infection, hla_b27,
        uveitis_anterior, sacroiliitis_imaging, inflammatory_back_pain_past,
        family_history_spa
    )
