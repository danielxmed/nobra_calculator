"""
Truelove and Witts Severity Index for Ulcerative Colitis Calculator

Stratifies severity of ulcerative colitis into mild, moderate, or severe categories
based on clinical and laboratory parameters.

References:
1. Truelove SC, Witts LJ. Cortisone in ulcerative colitis; final report on a therapeutic trial. 
   Br Med J. 1955;2(4947):1041-8. PMID: 13260656; PMCID: PMC2061071.
2. Danese S, Fiocchi C. Ulcerative colitis. N Engl J Med. 2011 Nov 3;365(18):1713-25.
"""

from typing import Dict, Any


class TrueloveWittsSeverityIndexCalculator:
    """Calculator for Truelove and Witts Severity Index for Ulcerative Colitis"""
    
    def __init__(self):
        # Define severity interpretations
        self.interpretations = {
            "mild": {
                "stage": "Mild",
                "description": "Mild ulcerative colitis",
                "interpretation": "Mild disease with minimal systemic symptoms. Can usually be managed with topical or oral aminosalicylates. Monitor closely for response to treatment."
            },
            "moderate": {
                "stage": "Moderate", 
                "description": "Moderate ulcerative colitis",
                "interpretation": "Moderate disease with some systemic symptoms. Consider oral corticosteroids or immunomodulators. May require hospitalization for monitoring and treatment optimization."
            },
            "severe": {
                "stage": "Severe",
                "description": "Severe ulcerative colitis", 
                "interpretation": "Severe disease with significant systemic symptoms. Requires immediate hospitalization and intensive medical therapy. Consider intravenous corticosteroids, biologics, or surgical consultation. Monitor for complications such as toxic megacolon or perforation."
            }
        }
    
    def calculate(self, bowel_movements: str, blood_in_stool: str, pyrexia: str, 
                 tachycardia: str, anemia: str, esr_elevated: str) -> Dict[str, Any]:
        """
        Calculates the Truelove and Witts Severity Index
        
        Args:
            bowel_movements (str): Number of bowel movements per day ("less_than_4", "4_to_5", "6_or_more")
            blood_in_stool (str): Presence of blood in stool ("none_or_small", "between_mild_severe", "visible_blood")
            pyrexia (str): Presence of fever ≥100.04°F (37.8°C) ("no", "yes")
            tachycardia (str): Pulse >90 bpm ("no", "yes")
            anemia (str): Hemoglobin ≤10.5 g/dL (105 g/L) ("no", "yes")
            esr_elevated (str): ESR >30 mm/hr ("no", "yes")
            
        Returns:
            Dict with the severity classification and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bowel_movements, blood_in_stool, pyrexia, tachycardia, anemia, esr_elevated)
        
        # Determine severity
        severity = self._calculate_severity(bowel_movements, blood_in_stool, pyrexia, tachycardia, anemia, esr_elevated)
        
        # Get interpretation
        interpretation = self.interpretations[severity]
        
        return {
            "result": severity,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bowel_movements: str, blood_in_stool: str, pyrexia: str, 
                        tachycardia: str, anemia: str, esr_elevated: str):
        """Validates input parameters"""
        
        valid_bowel_movements = ["less_than_4", "4_to_5", "6_or_more"]
        valid_blood_options = ["none_or_small", "between_mild_severe", "visible_blood"]
        valid_yes_no = ["no", "yes"]
        
        if bowel_movements not in valid_bowel_movements:
            raise ValueError(f"Bowel movements must be one of: {valid_bowel_movements}")
        
        if blood_in_stool not in valid_blood_options:
            raise ValueError(f"Blood in stool must be one of: {valid_blood_options}")
        
        if pyrexia not in valid_yes_no:
            raise ValueError(f"Pyrexia must be one of: {valid_yes_no}")
        
        if tachycardia not in valid_yes_no:
            raise ValueError(f"Tachycardia must be one of: {valid_yes_no}")
        
        if anemia not in valid_yes_no:
            raise ValueError(f"Anemia must be one of: {valid_yes_no}")
        
        if esr_elevated not in valid_yes_no:
            raise ValueError(f"ESR elevated must be one of: {valid_yes_no}")
    
    def _calculate_severity(self, bowel_movements: str, blood_in_stool: str, pyrexia: str, 
                           tachycardia: str, anemia: str, esr_elevated: str) -> str:
        """
        Determines severity based on Truelove and Witts criteria
        
        Logic:
        - Mild: All criteria for mild severity are met
        - Severe: ≥6 bowel movements AND ≥1 systemic feature (fever, tachycardia, anemia)
        - Moderate: Between mild and severe criteria
        """
        
        # Check if all criteria for mild are met
        is_mild = (
            bowel_movements == "less_than_4" and
            blood_in_stool == "none_or_small" and
            pyrexia == "no" and
            tachycardia == "no" and
            anemia == "no" and
            esr_elevated == "no"
        )
        
        if is_mild:
            return "mild"
        
        # Check for severe criteria
        # Severe requires ≥6 bowel movements AND at least one systemic feature
        has_frequent_bowel_movements = (bowel_movements == "6_or_more")
        has_systemic_features = (pyrexia == "yes" or tachycardia == "yes" or anemia == "yes")
        
        if has_frequent_bowel_movements and has_systemic_features:
            return "severe"
        
        # Everything else is moderate
        return "moderate"


def calculate_truelove_witts_severity_index(bowel_movements: str, blood_in_stool: str, pyrexia: str, 
                                           tachycardia: str, anemia: str, esr_elevated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TrueloveWittsSeverityIndexCalculator()
    return calculator.calculate(bowel_movements, blood_in_stool, pyrexia, tachycardia, anemia, esr_elevated)