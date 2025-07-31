"""
Ottawa Ankle Rule Calculator

Rules out clinically significant foot and ankle fractures to reduce use of x-ray imaging.
Provides separate criteria for ankle and foot x-rays.

References:
1. Stiell IG, et al. Ann Emerg Med. 1992;21(4):384-90.
2. Stiell IG, et al. JAMA. 1994;271(11):827-32.
3. Bachmann LM, et al. BMJ. 2003;326(7386):417.
4. Dowling S, et al. Acad Emerg Med. 2009;16(4):277-87.
"""

from typing import Dict, Any


class OttawaAnkleRuleCalculator:
    """Calculator for Ottawa Ankle Rule"""
    
    def calculate(self, 
                  malleolar_zone_pain: str,
                  lateral_malleolus_tenderness: str,
                  medial_malleolus_tenderness: str,
                  midfoot_zone_pain: str,
                  fifth_metatarsal_tenderness: str,
                  navicular_tenderness: str,
                  unable_to_bear_weight: str) -> Dict[str, Any]:
        """
        Calculates Ottawa Ankle Rule recommendations
        
        Args:
            malleolar_zone_pain (str): Pain in malleolar zone (yes/no)
            lateral_malleolus_tenderness (str): Tenderness at lateral malleolus (yes/no)
            medial_malleolus_tenderness (str): Tenderness at medial malleolus (yes/no)
            midfoot_zone_pain (str): Pain in midfoot zone (yes/no)
            fifth_metatarsal_tenderness (str): Tenderness at 5th metatarsal base (yes/no)
            navicular_tenderness (str): Tenderness at navicular bone (yes/no)
            unable_to_bear_weight (str): Unable to bear weight (yes/no)
            
        Returns:
            Dict with x-ray recommendations and interpretation
        """
        
        # Validations
        self._validate_inputs(
            malleolar_zone_pain, lateral_malleolus_tenderness,
            medial_malleolus_tenderness, midfoot_zone_pain,
            fifth_metatarsal_tenderness, navicular_tenderness,
            unable_to_bear_weight
        )
        
        # Determine if ankle x-ray is needed
        ankle_xray_needed = self._check_ankle_xray(
            malleolar_zone_pain,
            lateral_malleolus_tenderness,
            medial_malleolus_tenderness,
            unable_to_bear_weight
        )
        
        # Determine if foot x-ray is needed
        foot_xray_needed = self._check_foot_xray(
            midfoot_zone_pain,
            fifth_metatarsal_tenderness,
            navicular_tenderness,
            unable_to_bear_weight
        )
        
        # Get result and interpretation
        result_data = self._get_result(ankle_xray_needed, foot_xray_needed)
        
        return {
            "result": result_data["result"],
            "unit": "recommendation",
            "interpretation": result_data["interpretation"],
            "stage": result_data["stage"],
            "stage_description": result_data["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates all input parameters"""
        valid_options = ["yes", "no"]
        param_names = [
            "malleolar_zone_pain", "lateral_malleolus_tenderness",
            "medial_malleolus_tenderness", "midfoot_zone_pain",
            "fifth_metatarsal_tenderness", "navicular_tenderness",
            "unable_to_bear_weight"
        ]
        
        for i, value in enumerate(args):
            if value not in valid_options:
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no'")
    
    def _check_ankle_xray(self, malleolar_zone_pain: str,
                          lateral_malleolus_tenderness: str,
                          medial_malleolus_tenderness: str,
                          unable_to_bear_weight: str) -> bool:
        """Determines if ankle x-ray is needed"""
        
        # Ankle x-ray needed if malleolar pain AND any of the following
        if malleolar_zone_pain == "yes":
            if (lateral_malleolus_tenderness == "yes" or
                medial_malleolus_tenderness == "yes" or
                unable_to_bear_weight == "yes"):
                return True
        
        return False
    
    def _check_foot_xray(self, midfoot_zone_pain: str,
                         fifth_metatarsal_tenderness: str,
                         navicular_tenderness: str,
                         unable_to_bear_weight: str) -> bool:
        """Determines if foot x-ray is needed"""
        
        # Foot x-ray needed if midfoot pain AND any of the following
        if midfoot_zone_pain == "yes":
            if (fifth_metatarsal_tenderness == "yes" or
                navicular_tenderness == "yes" or
                unable_to_bear_weight == "yes"):
                return True
        
        return False
    
    def _get_result(self, ankle_xray_needed: bool, 
                    foot_xray_needed: bool) -> Dict[str, str]:
        """
        Determines the result and interpretation
        
        Args:
            ankle_xray_needed (bool): Whether ankle x-ray is indicated
            foot_xray_needed (bool): Whether foot x-ray is indicated
            
        Returns:
            Dict with result and interpretation
        """
        
        if ankle_xray_needed and foot_xray_needed:
            return {
                "result": "both_xrays",
                "stage": "Both x-rays indicated",
                "description": "Both ankle and foot x-ray series required",
                "interpretation": "Based on the Ottawa Ankle Rule, both ankle and foot x-ray series are indicated. The presence of criteria in both zones suggests possible fractures in both areas requiring comprehensive radiographic evaluation."
            }
        elif ankle_xray_needed:
            return {
                "result": "ankle_xray_only",
                "stage": "Ankle x-ray indicated",
                "description": "Ankle x-ray series required",
                "interpretation": "Based on the Ottawa Ankle Rule, an ankle x-ray series is indicated due to malleolar zone pain with either malleolar tenderness or inability to bear weight. This combination suggests possible ankle fracture requiring radiographic evaluation."
            }
        elif foot_xray_needed:
            return {
                "result": "foot_xray_only",
                "stage": "Foot x-ray indicated",
                "description": "Foot x-ray series required",
                "interpretation": "Based on the Ottawa Ankle Rule, a foot x-ray series is indicated due to midfoot zone pain with either 5th metatarsal/navicular tenderness or inability to bear weight. This combination suggests possible foot fracture requiring radiographic evaluation."
            }
        else:
            return {
                "result": "no_xray_needed",
                "stage": "No imaging required",
                "description": "No x-ray needed",
                "interpretation": "Based on the Ottawa Ankle Rule, no ankle or foot x-rays are required. The absence of all clinical criteria suggests a very low probability of clinically significant fracture. The rule has 98-100% sensitivity for detecting fractures."
            }


def calculate_ottawa_ankle_rule(malleolar_zone_pain: str,
                                lateral_malleolus_tenderness: str,
                                medial_malleolus_tenderness: str,
                                midfoot_zone_pain: str,
                                fifth_metatarsal_tenderness: str,
                                navicular_tenderness: str,
                                unable_to_bear_weight: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OttawaAnkleRuleCalculator()
    return calculator.calculate(
        malleolar_zone_pain, lateral_malleolus_tenderness,
        medial_malleolus_tenderness, midfoot_zone_pain,
        fifth_metatarsal_tenderness, navicular_tenderness,
        unable_to_bear_weight
    )