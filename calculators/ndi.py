"""
Neck Disability Index (NDI) Calculator

The NDI is a patient-reported outcome measure for neck pain and disability.
It consists of 10 domains, each scored 0-5, with a total score of 0-50.

References:
- Vernon H, Mior S. J Manipulative Physiol Ther. 1991;14(7):409-415.
- Vernon H. J Manipulative Physiol Ther. 2008;31(7):491-502.
"""

from typing import Dict, Any


class NdiCalculator:
    """Calculator for Neck Disability Index (NDI)"""
    
    def calculate(self, 
                  pain_intensity: int,
                  personal_care: int,
                  lifting: int,
                  reading: int,
                  headaches: int,
                  concentration: int,
                  work: int,
                  driving: int,
                  sleeping: int,
                  recreation: int) -> Dict[str, Any]:
        """
        Calculates the NDI score based on 10 functional domains
        
        Args:
            pain_intensity (int): Pain intensity score (0-5)
            personal_care (int): Personal care score (0-5)
            lifting (int): Lifting ability score (0-5)
            reading (int): Reading ability score (0-5)
            headaches (int): Headache score (0-5)
            concentration (int): Concentration score (0-5)
            work (int): Work capacity score (0-5)
            driving (int): Driving ability score (0-5)
            sleeping (int): Sleep quality score (0-5)
            recreation (int): Recreation activities score (0-5)
            
        Returns:
            Dict with NDI score and interpretation
        """
        
        # Validate all inputs
        domains = {
            'pain_intensity': pain_intensity,
            'personal_care': personal_care,
            'lifting': lifting,
            'reading': reading,
            'headaches': headaches,
            'concentration': concentration,
            'work': work,
            'driving': driving,
            'sleeping': sleeping,
            'recreation': recreation
        }
        
        for domain, value in domains.items():
            if not isinstance(value, int) or value < 0 or value > 5:
                raise ValueError(f"{domain} must be an integer between 0 and 5")
        
        # Calculate total NDI score
        ndi_score = sum(domains.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(ndi_score)
        
        return {
            "result": ndi_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the disability level based on NDI score
        
        Args:
            score (int): Total NDI score (0-50)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 4:
            return {
                "stage": "None",
                "description": "No disability",
                "interpretation": "The patient has no significant neck-related disability. They can perform all activities without pain interfering with daily life."
            }
        elif score <= 14:
            return {
                "stage": "Mild",
                "description": "Mild disability",
                "interpretation": "The patient has mild neck-related disability. Most activities of daily living are not significantly affected, though some discomfort may be present."
            }
        elif score <= 24:
            return {
                "stage": "Moderate",
                "description": "Moderate disability",
                "interpretation": "The patient has moderate neck-related disability. Pain and associated symptoms are having a significant impact on important activities of daily living."
            }
        elif score <= 34:
            return {
                "stage": "Severe",
                "description": "Severe disability",
                "interpretation": "The patient has severe neck-related disability. Major activities of daily living are affected, and the patient requires significant modifications to manage their condition."
            }
        else:
            return {
                "stage": "Complete",
                "description": "Complete disability",
                "interpretation": "The patient has complete neck-related disability. They are either bed-bound or have exaggerated symptoms. Careful evaluation is needed to rule out malingering or psychological overlay."
            }


def calculate_ndi(pain_intensity: int,
                  personal_care: int,
                  lifting: int,
                  reading: int,
                  headaches: int,
                  concentration: int,
                  work: int,
                  driving: int,
                  sleeping: int,
                  recreation: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NdiCalculator()
    return calculator.calculate(
        pain_intensity=pain_intensity,
        personal_care=personal_care,
        lifting=lifting,
        reading=reading,
        headaches=headaches,
        concentration=concentration,
        work=work,
        driving=driving,
        sleeping=sleeping,
        recreation=recreation
    )