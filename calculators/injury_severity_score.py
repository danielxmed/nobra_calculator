"""
Injury Severity Score (ISS) Calculator

Standardizes traumatic injury severity based on worst injury from 6 body systems
using the Abbreviated Injury Scale (AIS). The ISS correlates with mortality, 
morbidity and hospitalization time after trauma.

References (Vancouver style):
1. Baker SP, O'Neill B, Haddon W Jr, Long WB. The injury severity score: a method 
   for describing patients with multiple injuries and evaluating emergency care. 
   J Trauma. 1974 Mar;14(3):187-96.
2. Beverland DE, Rutherford WH. An assessment of the validity of the injury severity 
   score when applied to gunshot wounds. Injury. 1983 Mar;14(5):471-5.
3. Copes WS, Champion HR, Sacco WJ, Lawnick MM, Keast SL, Bain LW. The Injury 
   Severity Score revisited. J Trauma. 1988 Jan;28(1):69-77.
"""

from typing import Dict, Any


class InjurySeverityScoreCalculator:
    """Calculator for Injury Severity Score (ISS)"""
    
    def __init__(self):
        # AIS scale definitions
        self.ais_definitions = {
            0: "No injury",
            1: "Minor",
            2: "Moderate", 
            3: "Serious",
            4: "Severe",
            5: "Critical",
            6: "Unsurvivable"
        }
        
        # Body region names
        self.body_regions = {
            "head_neck": "Head and neck",
            "face": "Face",
            "chest": "Chest", 
            "abdomen": "Abdomen",
            "extremity": "Extremity",
            "external": "External"
        }
    
    def calculate(self, head_neck_ais: int, face_ais: int, chest_ais: int,
                 abdomen_ais: int, extremity_ais: int, external_ais: int) -> Dict[str, Any]:
        """
        Calculates the Injury Severity Score (ISS)
        
        Args:
            head_neck_ais (int): Head and neck AIS score (0-6)
            face_ais (int): Face AIS score (0-6)
            chest_ais (int): Chest AIS score (0-6)
            abdomen_ais (int): Abdomen AIS score (0-6)
            extremity_ais (int): Extremity AIS score (0-6)
            external_ais (int): External AIS score (0-6)
            
        Returns:
            Dict with the ISS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(head_neck_ais, face_ais, chest_ais, 
                             abdomen_ais, extremity_ais, external_ais)
        
        # Calculate ISS
        iss_score = self._calculate_iss(head_neck_ais, face_ais, chest_ais,
                                       abdomen_ais, extremity_ais, external_ais)
        
        # Get interpretation
        interpretation = self._get_interpretation(iss_score)
        
        return {
            "result": iss_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, head_neck_ais: int, face_ais: int, chest_ais: int,
                        abdomen_ais: int, extremity_ais: int, external_ais: int):
        """Validates input parameters"""
        
        ais_scores = [
            ("head_neck_ais", head_neck_ais),
            ("face_ais", face_ais),
            ("chest_ais", chest_ais),
            ("abdomen_ais", abdomen_ais),
            ("extremity_ais", extremity_ais),
            ("external_ais", external_ais)
        ]
        
        for param_name, ais_score in ais_scores:
            # Check if integer
            if not isinstance(ais_score, int):
                raise ValueError(f"{param_name} must be an integer")
            
            # Check range
            if ais_score < 0 or ais_score > 6:
                raise ValueError(f"{param_name} must be between 0 and 6 (AIS scale)")
    
    def _calculate_iss(self, head_neck_ais: int, face_ais: int, chest_ais: int,
                      abdomen_ais: int, extremity_ais: int, external_ais: int) -> int:
        """
        Calculates the Injury Severity Score using ISS formula
        
        ISS Calculation Method:
        1. If any AIS score is 6 (unsurvivable), ISS = 75 automatically
        2. Otherwise, take the three highest AIS scores
        3. Square each of the three highest scores
        4. Sum the squared scores to get ISS
        
        Formula: ISS = A² + B² + C² (where A, B, C are the 3 highest AIS scores)
        Range: 0-75 points
        """
        
        # Collect all AIS scores
        all_ais_scores = [
            head_neck_ais, face_ais, chest_ais,
            abdomen_ais, extremity_ais, external_ais
        ]
        
        # Check for unsurvivable injury (AIS = 6)
        if 6 in all_ais_scores:
            return 75
        
        # Sort AIS scores in descending order to get the three highest
        sorted_ais_scores = sorted(all_ais_scores, reverse=True)
        
        # Take the three highest AIS scores
        top_three_ais = sorted_ais_scores[:3]
        
        # Calculate ISS by squaring and summing the top three scores
        iss_score = sum(score ** 2 for score in top_three_ais)
        
        return iss_score
    
    def _get_interpretation(self, iss_score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on ISS score
        
        Args:
            iss_score (int): Calculated ISS score (0-75)
            
        Returns:
            Dict with interpretation details
        """
        
        if iss_score <= 8:
            return {
                "stage": "Minor Trauma",
                "description": f"ISS {iss_score} points (0-8 points)",
                "interpretation": "Minor trauma. Low mortality risk. Standard trauma evaluation and management protocols apply."
            }
        elif iss_score <= 15:
            return {
                "stage": "Moderate Trauma",
                "description": f"ISS {iss_score} points (9-15 points)",
                "interpretation": "Moderate trauma. Increased morbidity risk. Consider trauma team activation and comprehensive evaluation."
            }
        elif iss_score <= 24:
            return {
                "stage": "Major Trauma",
                "description": f"ISS {iss_score} points (16-24 points)",
                "interpretation": "Major trauma. Significant mortality and morbidity risk. Trauma team activation indicated. Consider transfer to trauma center if not already at one."
            }
        elif iss_score <= 40:
            return {
                "stage": "Severe Trauma",
                "description": f"ISS {iss_score} points (25-40 points)",
                "interpretation": "Severe trauma. High mortality risk. Requires immediate trauma team response, aggressive resuscitation, and specialized trauma care."
            }
        else:  # iss_score > 40 (up to 75)
            return {
                "stage": "Critical Trauma",
                "description": f"ISS {iss_score} points (41-75 points)",
                "interpretation": "Critical trauma. Very high mortality risk. Requires immediate life-saving interventions, maximum trauma team response, and consideration of damage control strategies."
            }


def calculate_injury_severity_score(head_neck_ais: int, face_ais: int, chest_ais: int,
                                   abdomen_ais: int, extremity_ais: int, external_ais: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = InjurySeverityScoreCalculator()
    return calculator.calculate(head_neck_ais, face_ais, chest_ais,
                               abdomen_ais, extremity_ais, external_ais)