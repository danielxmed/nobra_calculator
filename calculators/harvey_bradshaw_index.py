"""
Harvey-Bradshaw Index (HBI) for Crohn's Disease Calculator

Stratifies severity of Crohn's disease using only clinical parameters.
A simplified version of the CDAI that correlates 93% with CDAI but doesn't require labs.

References:
1. Harvey RF, Bradshaw JM. Lancet. 1980;1(8167):514.
2. Peyrin-Biroulet L, et al. Clin Gastroenterol Hepatol. 2016;14(3):348-354.
"""

from typing import Dict, Any, List


class HarveyBradshawIndexCalculator:
    """Calculator for Harvey-Bradshaw Index (HBI) for Crohn's Disease"""
    
    def __init__(self):
        # Complication options that count as 1 point each
        self.VALID_COMPLICATIONS = [
            "none",
            "arthralgia",
            "uveitis",
            "erythema_nodosum",
            "aphthous_ulcers",
            "pyoderma_gangrenosum",
            "anal_fissures",
            "new_fistula",
            "abscess"
        ]
    
    def calculate(self, general_wellbeing: int, abdominal_pain: int, 
                  liquid_stools: int, abdominal_mass: int, 
                  complications: List[str]) -> Dict[str, Any]:
        """
        Calculates the HBI score using the provided parameters
        
        Args:
            general_wellbeing (int): General well-being (0-4)
            abdominal_pain (int): Abdominal pain severity (0-3)
            liquid_stools (int): Number of liquid/soft stools per day
            abdominal_mass (int): Abdominal mass on exam (0-3)
            complications (List[str]): List of extra-intestinal manifestations
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(general_wellbeing, abdominal_pain, liquid_stools,
                            abdominal_mass, complications)
        
        # Calculate HBI score
        score = 0
        
        # Add scores from each domain
        score += general_wellbeing  # 0-4 points
        score += abdominal_pain     # 0-3 points
        score += liquid_stools      # 1 point per stool
        score += abdominal_mass     # 0-3 points
        
        # Add complications (1 point each, excluding "none")
        complication_count = len([c for c in complications if c != "none"])
        score += complication_count
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, general_wellbeing: int, abdominal_pain: int,
                        liquid_stools: int, abdominal_mass: int,
                        complications: List[str]):
        """Validates input parameters"""
        
        # Validate general wellbeing (0-4)
        if not isinstance(general_wellbeing, int) or general_wellbeing < 0 or general_wellbeing > 4:
            raise ValueError("General wellbeing must be an integer between 0 and 4")
        
        # Validate abdominal pain (0-3)
        if not isinstance(abdominal_pain, int) or abdominal_pain < 0 or abdominal_pain > 3:
            raise ValueError("Abdominal pain must be an integer between 0 and 3")
        
        # Validate liquid stools (0-50, reasonable upper limit)
        if not isinstance(liquid_stools, int) or liquid_stools < 0 or liquid_stools > 50:
            raise ValueError("Number of liquid stools must be an integer between 0 and 50")
        
        # Validate abdominal mass (0-3)
        if not isinstance(abdominal_mass, int) or abdominal_mass < 0 or abdominal_mass > 3:
            raise ValueError("Abdominal mass must be an integer between 0 and 3")
        
        # Validate complications
        if not isinstance(complications, list):
            raise ValueError("Complications must be a list")
        
        for comp in complications:
            if comp not in self.VALID_COMPLICATIONS:
                raise ValueError(f"Invalid complication: {comp}. Must be one of: {', '.join(self.VALID_COMPLICATIONS)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the HBI score
        
        Args:
            score (int): Calculated HBI score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 5:
            return {
                "stage": "Remission",
                "description": "Disease in remission",
                "interpretation": (
                    "Patient's Crohn's disease is in remission. The score indicates minimal or no "
                    "disease activity. Continue current maintenance therapy and routine monitoring."
                )
            }
        elif score <= 7:
            return {
                "stage": "Mild Disease",
                "description": "Mild disease activity",
                "interpretation": (
                    "Patient has mild Crohn's disease activity. Consider optimization of current "
                    "therapy or initiation of treatment if not already on therapy. Close monitoring "
                    "is recommended."
                )
            }
        elif score <= 16:
            return {
                "stage": "Moderate Disease",
                "description": "Moderate disease activity",
                "interpretation": (
                    "Patient has moderate Crohn's disease activity. Treatment escalation is typically "
                    "warranted. Consider systemic corticosteroids, immunomodulators, or biologic "
                    "therapy depending on current treatment status."
                )
            }
        else:  # score > 16
            return {
                "stage": "Severe Disease",
                "description": "Severe disease activity",
                "interpretation": (
                    "Patient has severe Crohn's disease activity. Urgent treatment intensification "
                    "is needed. Consider hospitalization, intravenous corticosteroids, and/or rapid "
                    "initiation of biologic therapy. Evaluate for complications."
                )
            }


def calculate_harvey_bradshaw_index(general_wellbeing: int, abdominal_pain: int,
                                   liquid_stools: int, abdominal_mass: int,
                                   complications: List[str]) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HarveyBradshawIndexCalculator()
    return calculator.calculate(general_wellbeing, abdominal_pain, liquid_stools,
                              abdominal_mass, complications)