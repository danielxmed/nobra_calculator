"""
Barcelona-Clinic Liver Cancer (BCLC) Staging Calculator

Determines disease progression and appropriate treatment course for HCC patients
based on tumor characteristics, liver function, and performance status.

References:
1. Reig M, et al. BCLC strategy for prognosis prediction and treatment recommendation: 
   The 2022 update. J Hepatol. 2022 Mar;76(3):681-693.
2. Llovet JM, et al. Prognosis of hepatocellular carcinoma: the BCLC staging 
   classification. Semin Liver Dis. 1999;19(3):329-38.
"""

from typing import Dict, Any


class BclcStagingCalculator:
    """Calculator for Barcelona-Clinic Liver Cancer (BCLC) Staging Classification"""
    
    def __init__(self):
        self.stage_definitions = {
            "0": {
                "name": "Very Early Stage",
                "treatment": "Ablation (preferred), resection or transplantation",
                "prognosis": "5-year survival >70%"
            },
            "A": {
                "name": "Early Stage", 
                "treatment": "Resection, transplantation, or ablation depending on portal pressure and bilirubin",
                "prognosis": "5-year survival 50-70%"
            },
            "B": {
                "name": "Intermediate Stage",
                "treatment": "Transarterial chemoembolization (TACE)",
                "prognosis": "Median survival 20-26 months"
            },
            "C": {
                "name": "Advanced Stage",
                "treatment": "Systemic therapy (atezolizumab + bevacizumab, sorafenib, lenvatinib)",
                "prognosis": "Median survival 6-11 months"
            },
            "D": {
                "name": "Terminal Stage",
                "treatment": "Best supportive care",
                "prognosis": "Median survival <3 months"
            }
        }
    
    def calculate(self, performance_status: int, child_pugh_class: str, 
                  tumor_size: float, number_of_nodules: int,
                  portal_invasion: str, extrahepatic_spread: str) -> Dict[str, Any]:
        """
        Calculates BCLC stage based on patient parameters
        
        Args:
            performance_status (int): ECOG Performance Status (0-4)
            child_pugh_class (str): Child-Pugh class (A, B, or C)
            tumor_size (float): Size of largest tumor in cm
            number_of_nodules (int): Number of tumor nodules
            portal_invasion (str): Presence of portal vein invasion ("yes" or "no")
            extrahepatic_spread (str): Presence of extrahepatic spread ("yes" or "no")
            
        Returns:
            Dict with BCLC stage and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(performance_status, child_pugh_class, tumor_size,
                            number_of_nodules, portal_invasion, extrahepatic_spread)
        
        # Determine BCLC stage
        stage = self._determine_stage(performance_status, child_pugh_class,
                                    tumor_size, number_of_nodules,
                                    portal_invasion, extrahepatic_spread)
        
        # Get stage details
        stage_info = self.stage_definitions[stage]
        
        return {
            "result": stage,
            "unit": "",
            "interpretation": f"BCLC Stage {stage} - {stage_info['name']}. " + 
                            f"Treatment recommendation: {stage_info['treatment']}. " +
                            f"Prognosis: {stage_info['prognosis']}",
            "stage": f"Stage {stage}",
            "stage_description": stage_info['name']
        }
    
    def _validate_inputs(self, performance_status: int, child_pugh_class: str,
                        tumor_size: float, number_of_nodules: int,
                        portal_invasion: str, extrahepatic_spread: str):
        """Validates input parameters"""
        
        if not isinstance(performance_status, int) or performance_status < 0 or performance_status > 4:
            raise ValueError("Performance status must be an integer between 0 and 4")
        
        if child_pugh_class not in ["A", "B", "C"]:
            raise ValueError("Child-Pugh class must be A, B, or C")
        
        if not isinstance(tumor_size, (int, float)) or tumor_size < 0:
            raise ValueError("Tumor size must be a non-negative number")
        
        if not isinstance(number_of_nodules, int) or number_of_nodules < 0:
            raise ValueError("Number of nodules must be a non-negative integer")
        
        if portal_invasion not in ["yes", "no"]:
            raise ValueError("Portal invasion must be 'yes' or 'no'")
        
        if extrahepatic_spread not in ["yes", "no"]:
            raise ValueError("Extrahepatic spread must be 'yes' or 'no'")
    
    def _determine_stage(self, performance_status: int, child_pugh_class: str,
                        tumor_size: float, number_of_nodules: int,
                        portal_invasion: str, extrahepatic_spread: str) -> str:
        """
        Determines BCLC stage based on criteria
        
        Stage D (Terminal): PS >2 OR Child-Pugh C
        Stage C (Advanced): Portal invasion OR extrahepatic spread AND PS 1-2 AND Child-Pugh A-B
        Stage B (Intermediate): Multinodular (>3 nodules or any nodule >3cm) AND PS 0 AND Child-Pugh A-B
        Stage A (Early): Single nodule OR up to 3 nodules ≤3cm AND PS 0 AND Child-Pugh A-B
        Stage 0 (Very Early): Single nodule <2cm AND PS 0 AND Child-Pugh A
        """
        
        # Stage D: Terminal stage
        if performance_status > 2 or child_pugh_class == "C":
            return "D"
        
        # Stage C: Advanced stage
        if (portal_invasion == "yes" or extrahepatic_spread == "yes") and performance_status <= 2:
            return "C"
        
        # Only PS 0 and Child-Pugh A-B from here
        if performance_status != 0:
            # PS 1-2 without portal invasion or extrahepatic spread
            return "C"
        
        # Stage 0: Very early stage
        if (number_of_nodules == 1 and tumor_size < 2 and 
            child_pugh_class == "A" and portal_invasion == "no" and 
            extrahepatic_spread == "no"):
            return "0"
        
        # Stage A: Early stage
        if (((number_of_nodules == 1 and tumor_size <= 5) or 
             (number_of_nodules <= 3 and tumor_size <= 3)) and
            portal_invasion == "no" and extrahepatic_spread == "no"):
            return "A"
        
        # Stage B: Intermediate stage (multinodular or large tumors)
        return "B"


def calculate_bclc_staging(performance_status: int, child_pugh_class: str,
                          tumor_size: float, number_of_nodules: int,
                          portal_invasion: str, extrahepatic_spread: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BclcStagingCalculator()
    return calculator.calculate(performance_status, child_pugh_class,
                              tumor_size, number_of_nodules,
                              portal_invasion, extrahepatic_spread)