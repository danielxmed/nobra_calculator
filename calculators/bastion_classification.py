"""
Bastion Classification of Lower Limb Blast Injuries Calculator

Stratifies lower limb blast injuries to guide treatment.

References (Vancouver style):
1. Jacobs N, Rourke K, Rutherford J, Hicks A, Smith SR, Templeton P, et al. Lower limb injuries 
   caused by improvised explosive devices: Proposed 'Bastion Classification' and prospective 
   validation. Injury. 2014 Sep;45(9):1422-8.
2. Lundy JB, Hobbs CM. 'Bastion Classification': evolution of experience mandates caution when 
   considering using class as predictor for method of temporary vascular control. Injury. 2013 
   Nov;44(11):1671-2.
3. Scerbo MH, Mumm JP, Gates K, Love JD, Wade CE, Holcomb JB, et al. Safety and Appropriateness 
   of Tourniquets in 105 Civilians. Prehosp Emerg Care. 2016 Nov-Dec;20(6):712-722.
"""

from typing import Dict, Any


class BastionClassificationCalculator:
    """Calculator for Bastion Classification of Lower Limb Blast Injuries"""
    
    def __init__(self):
        # Class descriptions
        self.class_descriptions = {
            1: "Injury confined to foot",
            2: "Injury involving lower leg permitting effective below-knee tourniquet application",
            3: "Injury involving proximal lower leg or thigh, permitting effective above-knee tourniquet application",
            4: "Proximal thigh injury, preventing effective tourniquet application",
            5: "Any injury with buttock involvement"
        }
        
        # Management recommendations
        self.management_recommendations = {
            1: "Local hemorrhage control, consider foot salvage vs. amputation",
            2: "Below-knee tourniquet effective for hemorrhage control",
            3: "Above-knee tourniquet effective for hemorrhage control (most common pattern: 49%)",
            4: "Tourniquet application challenging, may require proximal vascular control",
            5: "Tourniquet ineffective, requires operative proximal vascular control"
        }
    
    def calculate(self, injury_class: int, segmental_injury: str, abdominal_injury: str,
                  genital_perineal_injury: str, pelvic_ring_injury: str, 
                  upper_limb_injury: str) -> Dict[str, Any]:
        """
        Calculates the Bastion Classification with applicable suffixes
        
        Args:
            injury_class: Anatomical level of injury (1-5)
            segmental_injury: Presence of potentially viable tissue distal to injury ("yes"/"no")
            abdominal_injury: Associated intraperitoneal abdominal injury ("yes"/"no")
            genital_perineal_injury: Associated genitalia and perineal injury ("yes"/"no")
            pelvic_ring_injury: Associated pelvic ring injury ("yes"/"no")
            upper_limb_injury: Associated upper limb injury ("yes"/"no")
            
        Returns:
            Dict with classification result and interpretation
        """
        
        # Validate injury class
        if injury_class not in range(1, 6):
            raise ValueError("Injury class must be between 1 and 5")
        
        # Build classification string
        classification = str(injury_class)
        
        # Add suffixes based on associated injuries
        suffixes = []
        suffix_descriptions = []
        
        if segmental_injury == "yes":
            suffixes.append("S")
            suffix_descriptions.append("Segmental injury present")
        
        if abdominal_injury == "yes":
            suffixes.append("A")
            suffix_descriptions.append("Associated intraperitoneal abdominal injury")
        
        if genital_perineal_injury == "yes":
            suffixes.append("B")
            suffix_descriptions.append("Associated genitalia and perineal injury")
        
        if pelvic_ring_injury == "yes":
            suffixes.append("C")
            suffix_descriptions.append("Associated pelvic ring injury")
        
        if upper_limb_injury == "yes":
            suffixes.append("D")
            suffix_descriptions.append("Associated upper limb injury")
        
        # Combine classification with suffixes
        if suffixes:
            classification += "-" + "".join(suffixes)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(
            injury_class, suffixes, suffix_descriptions
        )
        
        return {
            "result": classification,
            "unit": "classification",
            "interpretation": interpretation,
            "stage": f"Class {injury_class}",
            "stage_description": self.class_descriptions[injury_class]
        }
    
    def _generate_interpretation(self, injury_class: int, suffixes: list, 
                                suffix_descriptions: list) -> str:
        """Generates detailed interpretation of the classification"""
        
        interpretation_parts = []
        
        # Primary classification interpretation
        interpretation_parts.append(
            f"Bastion Class {injury_class}: {self.class_descriptions[injury_class]}. "
        )
        
        # Management recommendation
        interpretation_parts.append(
            f"Management: {self.management_recommendations[injury_class]} "
        )
        
        # Tourniquet effectiveness
        if injury_class <= 3:
            interpretation_parts.append(
                "Tourniquet application is effective for hemorrhage control. "
            )
        else:
            interpretation_parts.append(
                "Tourniquet application is challenging or ineffective; "
                "may require operative proximal vascular control. "
            )
        
        # Associated injuries if present
        if suffix_descriptions:
            interpretation_parts.append(
                f"Associated injuries: {', '.join(suffix_descriptions)}. "
            )
            
            # Special considerations for specific suffixes
            if "A" in suffixes:
                interpretation_parts.append(
                    "Consider damage control laparotomy. "
                )
            if "B" in suffixes:
                interpretation_parts.append(
                    "Urological/gynecological consultation recommended. "
                )
            if "C" in suffixes:
                interpretation_parts.append(
                    "Pelvic binder application and massive transfusion protocol may be needed. "
                )
        
        # General recommendations
        if injury_class >= 4:
            interpretation_parts.append(
                "High risk for massive hemorrhage; prepare for massive transfusion protocol. "
            )
        
        return "".join(interpretation_parts).strip()


def calculate_bastion_classification(injury_class: int, segmental_injury: str, 
                                   abdominal_injury: str, genital_perineal_injury: str,
                                   pelvic_ring_injury: str, upper_limb_injury: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BastionClassificationCalculator()
    return calculator.calculate(
        injury_class, segmental_injury, abdominal_injury,
        genital_perineal_injury, pelvic_ring_injury, upper_limb_injury
    )