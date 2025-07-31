"""
Donor Lymphocyte Infusion (DLI) Volume Calculator

Estimates total blood volume to process by apheresis to produce appropriate DLI dosage.

References:
1. Wingard JR, Hsu J, Hiemenz JW. Hematopoietic Stem Cell Transplantation: A Handbook 
   for Clinicians. 2nd ed. Bethesda, MD: AABB Press; 2010.
2. Schmitz N, Dreger P, Suttorp M, et al. Primary transplantation of allogeneic peripheral 
   blood progenitor cells mobilized by filgrastim. Blood. 1995 Mar 1;85(5):1666-72.
"""

from typing import Dict, Any


class DliVolumeCalculator:
    """Calculator for Donor Lymphocyte Infusion (DLI) Volume"""
    
    def __init__(self):
        # Conversion factor for cells per microliter to cells per milliliter
        self.CELLS_PER_ML_CONVERSION = 1000
    
    def calculate(self, recipient_weight: float, cd3_infusion_dose: float,
                  number_of_infusions: int, collection_efficiency: float,
                  donor_wbc_count: float, donor_total_lymphocytes: float,
                  donor_cd3_lymphocytes: float) -> Dict[str, Any]:
        """
        Calculates the blood volume needed for DLI collection
        
        Args:
            recipient_weight (float): Recipient weight in kg
            cd3_infusion_dose (float): CD3+ infusion dose (× 10⁶ cells/kg)
            number_of_infusions (int): Number of planned infusions
            collection_efficiency (float): Collection efficiency as percentage
            donor_wbc_count (float): Donor WBC count (× 10³/μL)
            donor_total_lymphocytes (float): Donor total lymphocytes as % of WBC
            donor_cd3_lymphocytes (float): Donor CD3+ lymphocytes as % of lymphocytes
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(recipient_weight, cd3_infusion_dose, number_of_infusions,
                             collection_efficiency, donor_wbc_count, donor_total_lymphocytes,
                             donor_cd3_lymphocytes)
        
        # Calculate using the DLI volume formula:
        # 1. Calculate absolute CD3+ lymphocyte count in donor blood
        # 2. Calculate total CD3+ cells needed
        # 3. Calculate total blood volume needed
        
        # Step 1: Calculate absolute CD3+ lymphocyte count (× 10³ cells/μL)
        # donor_wbc_count is already in × 10³/μL units
        # So absolute count = donor_wbc_count × % lymphocytes × % CD3+ 
        # Result will be in × 10³ cells/μL
        absolute_cd3_count_thousands = (donor_wbc_count * 
                                       (donor_total_lymphocytes / 100) * 
                                       (donor_cd3_lymphocytes / 100))
        
        # Step 2: Total CD3+ cells needed (× 10⁶ cells)
        # = recipient weight × CD3+ dose × number of infusions  
        total_cd3_needed_millions = recipient_weight * cd3_infusion_dose * number_of_infusions
        
        # Step 3: Calculate blood volume needed in mL
        # Convert units properly:
        # - absolute_cd3_count_thousands × 10³ = actual cells per μL
        # - total_cd3_needed_millions × 10⁶ = actual cells needed
        # - collection_efficiency is in percentage
        
        # CD3+ cells collected per μL = absolute_cd3_count_thousands × 10³ × (collection_efficiency / 100)
        cd3_cells_collected_per_ul = absolute_cd3_count_thousands * 1000 * (collection_efficiency / 100)
        
        # Total actual cells needed = total_cd3_needed_millions × 10⁶
        total_cells_needed = total_cd3_needed_millions * 1000000
        
        # Blood volume in μL = total_cells_needed / cd3_cells_collected_per_ul
        blood_volume_ul = total_cells_needed / cd3_cells_collected_per_ul
        
        # Convert to mL
        blood_volume_needed = blood_volume_ul / 1000
        
        # Round to nearest mL
        blood_volume_needed = round(blood_volume_needed)
        
        # Get interpretation
        interpretation = self._get_interpretation(blood_volume_needed)
        
        return {
            "result": blood_volume_needed,
            "unit": "mL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, recipient_weight: float, cd3_infusion_dose: float,
                        number_of_infusions: int, collection_efficiency: float,
                        donor_wbc_count: float, donor_total_lymphocytes: float,
                        donor_cd3_lymphocytes: float):
        """Validates input parameters"""
        
        # Validate recipient weight
        if not isinstance(recipient_weight, (int, float)):
            raise ValueError("recipient_weight must be a number")
        if recipient_weight < 1 or recipient_weight > 300:
            raise ValueError("recipient_weight must be between 1 and 300 kg")
        
        # Validate CD3+ infusion dose
        if not isinstance(cd3_infusion_dose, (int, float)):
            raise ValueError("cd3_infusion_dose must be a number")
        if cd3_infusion_dose < 0.1 or cd3_infusion_dose > 1000:
            raise ValueError("cd3_infusion_dose must be between 0.1 and 1000 × 10⁶ cells/kg")
        
        # Validate number of infusions
        if not isinstance(number_of_infusions, int):
            raise ValueError("number_of_infusions must be an integer")
        if number_of_infusions < 1 or number_of_infusions > 10:
            raise ValueError("number_of_infusions must be between 1 and 10")
        
        # Validate collection efficiency
        if not isinstance(collection_efficiency, (int, float)):
            raise ValueError("collection_efficiency must be a number")
        if collection_efficiency < 10 or collection_efficiency > 90:
            raise ValueError("collection_efficiency must be between 10 and 90 percent")
        
        # Validate donor WBC count
        if not isinstance(donor_wbc_count, (int, float)):
            raise ValueError("donor_wbc_count must be a number")
        if donor_wbc_count < 1 or donor_wbc_count > 50:
            raise ValueError("donor_wbc_count must be between 1 and 50 × 10³/μL")
        
        # Validate donor total lymphocytes
        if not isinstance(donor_total_lymphocytes, (int, float)):
            raise ValueError("donor_total_lymphocytes must be a number")
        if donor_total_lymphocytes < 5 or donor_total_lymphocytes > 80:
            raise ValueError("donor_total_lymphocytes must be between 5 and 80 percent")
        
        # Validate donor CD3+ lymphocytes
        if not isinstance(donor_cd3_lymphocytes, (int, float)):
            raise ValueError("donor_cd3_lymphocytes must be a number")
        if donor_cd3_lymphocytes < 30 or donor_cd3_lymphocytes > 90:
            raise ValueError("donor_cd3_lymphocytes must be between 30 and 90 percent")
    
    def _get_interpretation(self, volume: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the blood volume needed
        
        Args:
            volume (float): Blood volume needed in mL
            
        Returns:
            Dict with interpretation
        """
        
        if volume < 2000:
            return {
                "stage": "Low volume",
                "description": "Small apheresis procedure",
                "interpretation": "Low blood volume requirement. Short apheresis procedure expected. Monitor donor comfort and fluid balance."
            }
        elif volume < 5000:
            return {
                "stage": "Moderate volume",
                "description": "Standard apheresis procedure",
                "interpretation": "Moderate blood volume requirement. Standard apheresis procedure. Ensure adequate donor hydration and monitor vital signs."
            }
        elif volume < 10000:
            return {
                "stage": "High volume",
                "description": "Extended apheresis procedure",
                "interpretation": "High blood volume requirement. Extended apheresis procedure. Consider splitting into multiple sessions. Close monitoring of donor required."
            }
        else:  # volume >= 10000
            return {
                "stage": "Very high volume",
                "description": "Multiple session requirement",
                "interpretation": "Very high blood volume requirement. Strongly consider multiple apheresis sessions to ensure donor safety. Careful donor selection and monitoring essential."
            }


def calculate_dli_volume(recipient_weight: float, cd3_infusion_dose: float,
                        number_of_infusions: int, collection_efficiency: float,
                        donor_wbc_count: float, donor_total_lymphocytes: float,
                        donor_cd3_lymphocytes: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DliVolumeCalculator()
    return calculator.calculate(recipient_weight, cd3_infusion_dose, number_of_infusions,
                               collection_efficiency, donor_wbc_count, donor_total_lymphocytes,
                               donor_cd3_lymphocytes)