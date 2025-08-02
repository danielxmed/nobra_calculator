"""
Trunk Impairment Scale Calculator

Quantifies disability after stroke; also validated in Parkinson's disease.
Assesses static sitting balance, dynamic sitting balance, and coordination
through 17 specific motor tasks.

References:
- Verheyden G, Nieuwboer A, Mertin J, Preger R, Kiekens C, De weerdt W. 
  The Trunk Impairment Scale: a new tool to measure motor impairment of the trunk after stroke. 
  Clin Rehabil. 2004;18(3):326-34.
- Verheyden G, Willems AM, Ooms L, Nieuwboer A. Validity of the trunk impairment scale 
  as a measure of trunk performance in people with Parkinson's disease. 
  Arch Phys Med Rehabil. 2007;88(10):1304-8.
"""

from typing import Dict, Any


class TrunkImpairmentScaleCalculator:
    """Calculator for Trunk Impairment Scale"""
    
    def __init__(self):
        # Point values for each category
        self.static_points = {
            "static_item_1": {"no": 0, "yes": 2},
            "static_item_2": {"falls_or_cannot_maintain": 0, "maintains_position": 2},
            "static_item_3": {
                "falls": 0,
                "cannot_cross_without_arm_support": 1,
                "crosses_with_displacement_or_assistance": 2,
                "crosses_without_displacement": 3
            }
        }
        
        self.dynamic_points = {
            "dynamic_item_1": {"falls_needs_support_or_no_touch": 0, "moves_actively_and_touches": 1},
            "dynamic_item_2": {"no_or_opposite_shortening": 0, "appropriate_shortening": 1},
            "dynamic_item_3": {"compensation_present": 0, "moves_without_compensation": 1},
            "dynamic_item_4": {"falls_needs_support_or_no_touch": 0, "moves_actively_and_touches": 1},
            "dynamic_item_5": {"no_or_opposite_shortening": 0, "appropriate_shortening": 1},
            "dynamic_item_6": {"compensation_present": 0, "moves_without_compensation": 1},
            "dynamic_item_7": {"no_or_opposite_shortening": 0, "appropriate_shortening": 1},
            "dynamic_item_8": {"compensation_present": 0, "moves_without_compensation": 1},
            "dynamic_item_9": {"no_or_opposite_shortening": 0, "appropriate_shortening": 1},
            "dynamic_item_10": {"compensation_present": 0, "moves_without_compensation": 1}
        }
        
        self.coordination_points = {
            "coordination_item_1": {
                "hemiplegic_not_moved_3x": 0,
                "asymmetrical_rotation": 1,
                "symmetrical_rotation": 2
            },
            "coordination_item_2": {"asymmetrical_rotation": 0, "symmetrical_rotation": 1},
            "coordination_item_3": {
                "hemiplegic_not_moved_3x": 0,
                "asymmetrical_rotation": 1,
                "symmetrical_rotation": 2
            },
            "coordination_item_4": {"asymmetrical_rotation": 0, "symmetrical_rotation": 1}
        }
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates the Trunk Impairment Scale score
        
        Args:
            **kwargs: All 17 assessment parameters
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(**kwargs)
        
        # Special rule: If static_item_1 is "no", total score is 0
        if kwargs.get("static_item_1") == "no":
            return {
                "result": 0,
                "unit": "points",
                "interpretation": "Patient cannot maintain the basic sitting position without support for 10 seconds. This indicates severe trunk impairment requiring intensive rehabilitation and support. Complete assessment cannot be performed due to inability to maintain starting position.",
                "stage": "Severe Impairment",
                "stage_description": "Unable to maintain starting position"
            }
        
        # Calculate scores for each category
        static_score = self._calculate_static_score(**kwargs)
        dynamic_score = self._calculate_dynamic_score(**kwargs)
        coordination_score = self._calculate_coordination_score(**kwargs)
        
        # Total score
        total_score = static_score + dynamic_score + coordination_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, **kwargs):
        """Validates input parameters"""
        
        # Check that all required parameters are present
        required_params = [
            "static_item_1", "static_item_2", "static_item_3",
            "dynamic_item_1", "dynamic_item_2", "dynamic_item_3", "dynamic_item_4",
            "dynamic_item_5", "dynamic_item_6", "dynamic_item_7", "dynamic_item_8",
            "dynamic_item_9", "dynamic_item_10",
            "coordination_item_1", "coordination_item_2", "coordination_item_3", "coordination_item_4"
        ]
        
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")
        
        # Validate static parameters
        for param, value in kwargs.items():
            if param.startswith("static_"):
                if param not in self.static_points or value not in self.static_points[param]:
                    raise ValueError(f"Invalid value '{value}' for parameter '{param}'")
            elif param.startswith("dynamic_"):
                if param not in self.dynamic_points or value not in self.dynamic_points[param]:
                    raise ValueError(f"Invalid value '{value}' for parameter '{param}'")
            elif param.startswith("coordination_"):
                if param not in self.coordination_points or value not in self.coordination_points[param]:
                    raise ValueError(f"Invalid value '{value}' for parameter '{param}'")
    
    def _calculate_static_score(self, **kwargs) -> int:
        """Calculates static sitting balance score (0-7 points)"""
        score = 0
        
        # Item 1: Basic sitting balance
        score += self.static_points["static_item_1"][kwargs["static_item_1"]]
        
        # Item 2: Therapist crosses legs
        score += self.static_points["static_item_2"][kwargs["static_item_2"]]
        
        # Item 3: Patient crosses legs
        score += self.static_points["static_item_3"][kwargs["static_item_3"]]
        
        return score
    
    def _calculate_dynamic_score(self, **kwargs) -> int:
        """Calculates dynamic sitting balance score (0-10 points)"""
        score = 0
        
        # Dynamic items with dependency rules
        
        # Items 1-3: Hemiplegic elbow movement
        item_1_score = self.dynamic_points["dynamic_item_1"][kwargs["dynamic_item_1"]]
        score += item_1_score
        
        if item_1_score == 0:
            # If item 1 fails, items 2 & 3 score 0
            pass
        else:
            # Item 2: Shortening/lengthening assessment
            item_2_score = self.dynamic_points["dynamic_item_2"][kwargs["dynamic_item_2"]]
            score += item_2_score
            
            if item_2_score == 0:
                # If item 2 fails, item 3 scores 0
                pass
            else:
                # Item 3: Compensation assessment
                score += self.dynamic_points["dynamic_item_3"][kwargs["dynamic_item_3"]]
        
        # Items 4-6: Unaffected elbow movement
        item_4_score = self.dynamic_points["dynamic_item_4"][kwargs["dynamic_item_4"]]
        score += item_4_score
        
        if item_4_score == 0:
            # If item 4 fails, items 5 & 6 score 0
            pass
        else:
            # Item 5: Shortening/lengthening assessment
            item_5_score = self.dynamic_points["dynamic_item_5"][kwargs["dynamic_item_5"]]
            score += item_5_score
            
            if item_5_score == 0:
                # If item 5 fails, item 6 scores 0
                pass
            else:
                # Item 6: Compensation assessment
                score += self.dynamic_points["dynamic_item_6"][kwargs["dynamic_item_6"]]
        
        # Items 7-8: Hemiplegic pelvis lift
        item_7_score = self.dynamic_points["dynamic_item_7"][kwargs["dynamic_item_7"]]
        score += item_7_score
        
        if item_7_score == 0:
            # If item 7 fails, item 8 scores 0
            pass
        else:
            # Item 8: Compensation assessment
            score += self.dynamic_points["dynamic_item_8"][kwargs["dynamic_item_8"]]
        
        # Items 9-10: Unaffected pelvis lift
        item_9_score = self.dynamic_points["dynamic_item_9"][kwargs["dynamic_item_9"]]
        score += item_9_score
        
        if item_9_score == 0:
            # If item 9 fails, item 10 scores 0
            pass
        else:
            # Item 10: Compensation assessment
            score += self.dynamic_points["dynamic_item_10"][kwargs["dynamic_item_10"]]
        
        return score
    
    def _calculate_coordination_score(self, **kwargs) -> int:
        """Calculates coordination score (0-6 points)"""
        score = 0
        
        # Items 1-2: Upper trunk rotation
        item_1_score = self.coordination_points["coordination_item_1"][kwargs["coordination_item_1"]]
        score += item_1_score
        
        if item_1_score == 0:
            # If item 1 fails (hemiplegic side not moved 3x), item 2 scores 0
            pass
        else:
            # Item 2: Repeat within 6 seconds
            score += self.coordination_points["coordination_item_2"][kwargs["coordination_item_2"]]
        
        # Items 3-4: Lower trunk rotation
        item_3_score = self.coordination_points["coordination_item_3"][kwargs["coordination_item_3"]]
        score += item_3_score
        
        if item_3_score == 0:
            # If item 3 fails (hemiplegic side not moved 3x), item 4 scores 0
            pass
        else:
            # Item 4: Repeat within 6 seconds
            score += self.coordination_points["coordination_item_4"][kwargs["coordination_item_4"]]
        
        return score
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Total calculated score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score == 0:
            return {
                "stage": "Severe Impairment",
                "description": "Unable to maintain starting position",
                "interpretation": "Patient cannot maintain the basic sitting position without support for 10 seconds. This indicates severe trunk impairment requiring intensive rehabilitation and support. Complete assessment cannot be performed due to inability to maintain starting position."
            }
        elif 1 <= total_score <= 7:
            return {
                "stage": "Severe Impairment",
                "description": "Severe trunk motor impairment",
                "interpretation": "Significant trunk motor impairment with limited static and dynamic sitting balance. Requires intensive rehabilitation focusing on basic trunk control and sitting balance. High risk for falls and functional limitations in daily activities."
            }
        elif 8 <= total_score <= 15:
            return {
                "stage": "Moderate Impairment",
                "description": "Moderate trunk motor impairment",
                "interpretation": "Moderate trunk impairment with some preserved sitting balance but difficulties with dynamic movements and coordination. May benefit from targeted trunk rehabilitation exercises. Some functional activities may be compromised."
            }
        elif 16 <= total_score <= 19:
            return {
                "stage": "Mild Impairment",
                "description": "Mild trunk motor impairment",
                "interpretation": "Mild trunk impairment with generally good sitting balance but some deficits in coordination or dynamic movements. Rehabilitation should focus on fine-tuning trunk control and coordination."
            }
        else:  # 20-23
            return {
                "stage": "Normal/Near Normal",
                "description": "Normal or near-normal trunk function",
                "interpretation": "Excellent trunk function with minimal or no impairment. Good sitting balance, dynamic control, and coordination. May require minimal intervention or maintenance therapy."
            }


def calculate_trunk_impairment_scale(**kwargs) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TrunkImpairmentScaleCalculator()
    return calculator.calculate(**kwargs)