"""
Modified Mallampati Classification Calculator

Stratifies predicted difficulty of endotracheal intubation based on anatomical 
features visible during oral examination. The modified version includes Class IV 
added by Samsoon and Young in 1987 to the original 3-class system by Mallampati.

References:
1. Mallampati SR, et al. Can Anaesth Soc J. 1985;32(4):429-34.
2. Samsoon GL, Young JR. Anaesthesia. 1987;42(5):487-90.
3. Lee A, et al. Anesth Analg. 2006;102(6):1867-78.
"""

from typing import Dict, Any


class ModifiedMallampatiClassificationCalculator:
    """Calculator for Modified Mallampati Classification"""
    
    def __init__(self):
        # Class mappings
        self.CLASS_VALUES = {
            "class_1": 1,
            "class_2": 2,
            "class_3": 3,
            "class_4": 4
        }
        
        # Structure descriptions
        self.CLASS_DESCRIPTIONS = {
            "class_1": "Faucial pillars, soft palate, and uvula visualized",
            "class_2": "Faucial pillars and soft palate visualized, uvula masked",
            "class_3": "Only soft palate visualized",
            "class_4": "Only hard palate visualized"
        }
    
    def calculate(self, visible_structures: str) -> Dict[str, Any]:
        """
        Determines the Modified Mallampati class for airway assessment
        
        Args:
            visible_structures (str): Anatomical structures visible during examination
            
        Returns:
            Dict with Mallampati class and intubation difficulty prediction
        """
        
        # Validate inputs
        self._validate_inputs(visible_structures)
        
        # Get class value
        class_value = self.CLASS_VALUES[visible_structures]
        
        # Get interpretation
        interpretation = self._get_interpretation(visible_structures, class_value)
        
        return {
            "result": class_value,
            "unit": "class",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, visible_structures: str):
        """Validates input parameters"""
        
        if visible_structures not in self.CLASS_VALUES:
            valid_classes = ", ".join(self.CLASS_VALUES.keys())
            raise ValueError(f"visible_structures must be one of: {valid_classes}")
    
    def _get_interpretation(self, visible_structures: str, class_value: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Mallampati class
        
        Args:
            visible_structures: Structure visibility identifier
            class_value: Numeric class value
            
        Returns:
            Dict with interpretation details
        """
        
        class_interpretations = {
            "class_1": {
                "stage": "Class I",
                "description": "Easy intubation predicted",
                "interpretation": (f"Modified Mallampati Class {class_value}: Faucial pillars, soft palate, "
                                f"and uvula are all visualized. This indicates a favorable airway anatomy "
                                f"with low risk of difficult intubation. Standard direct laryngoscopy "
                                f"should be successful. No special airway preparation typically required. "
                                f"Sensitivity for easy intubation is high in this class.")
            },
            "class_2": {
                "stage": "Class II",
                "description": "Mild difficulty possible",
                "interpretation": (f"Modified Mallampati Class {class_value}: Faucial pillars and soft palate "
                                f"are visualized, but the uvula is masked by the tongue base. This suggests "
                                f"mildly increased intubation difficulty compared to Class I. Standard "
                                f"laryngoscopy should still be successful in most cases, but consider having "
                                f"backup airway devices available. Slight increase in laryngoscopy grade possible.")
            },
            "class_3": {
                "stage": "Class III",
                "description": "Moderate difficulty likely",
                "interpretation": (f"Modified Mallampati Class {class_value}: Only the soft palate is visualized, "
                                f"with faucial pillars and uvula obscured by the tongue. This predicts "
                                f"moderately difficult intubation with increased risk of poor laryngoscopic "
                                f"view. Consider alternative intubation strategies such as video laryngoscopy, "
                                f"use of stylet or bougie, or preparation for fiber-optic intubation. "
                                f"Have rescue airway devices readily available.")
            },
            "class_4": {
                "stage": "Class IV",
                "description": "Severe difficulty expected",
                "interpretation": (f"Modified Mallampati Class {class_value}: Soft palate is not visualized, "
                                f"with only the hard palate visible. This indicates high risk of difficult "
                                f"intubation with likely poor or impossible laryngoscopic view. Strongly "
                                f"consider awake fiber-optic intubation, video laryngoscopy with experienced "
                                f"operator, or alternative airway management techniques. Prepare for potential "
                                f"surgical airway. Consider involving anesthesiology or airway specialist.")
            }
        }
        
        return class_interpretations.get(visible_structures, {
            "stage": f"Class {class_value}",
            "description": "Unknown class",
            "interpretation": f"Unknown Modified Mallampati class: {class_value}"
        })


def calculate_modified_mallampati_classification(visible_structures: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedMallampatiClassificationCalculator()
    return calculator.calculate(visible_structures)