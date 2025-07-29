"""
Bacterial Meningitis Score for Children Calculator

Predicts likelihood of bacterial (versus aseptic) meningitis in children with CSF pleocytosis.
The score helps clinicians distinguish between bacterial and aseptic meningitis to support safe 
discharge decisions while maintaining appropriate caution for this serious condition.

References:
1. Nigrovic LE, Kuppermann N, Macias CG, et al. Clinical prediction rule for identifying 
   children with cerebrospinal fluid pleocytosis at very low risk of bacterial meningitis. 
   JAMA. 2007 Jan 3;297(1):52-60. doi: 10.1001/jama.297.1.52.
2. Nigrovic LE, Malley R, Kuppermann N. Meta-analysis of bacterial meningitis score validation 
   studies. Arch Dis Child. 2012 Sep;97(9):799-805. doi: 10.1136/archdischild-2012-301798.
"""

from typing import Dict, Any


class BacterialMeningitisScoreCalculator:
    """Calculator for Bacterial Meningitis Score for Children"""
    
    def __init__(self):
        # Threshold values for scoring
        self.CSF_ANC_THRESHOLD = 1000  # cells/µL
        self.CSF_PROTEIN_THRESHOLD = 80  # mg/dL
        self.PERIPHERAL_ANC_THRESHOLD = 10000  # cells/µL
    
    def calculate(self, csf_gram_stain: str, csf_anc: int, csf_protein: float, 
                  peripheral_blood_anc: int, seizure_at_presentation: str) -> Dict[str, Any]:
        """
        Calculates the Bacterial Meningitis Score using the provided parameters
        
        Args:
            csf_gram_stain (str): CSF Gram stain result ('negative' or 'positive')
            csf_anc (int): CSF absolute neutrophil count in cells/µL
            csf_protein (float): CSF protein level in mg/dL
            peripheral_blood_anc (int): Peripheral blood absolute neutrophil count in cells/µL
            seizure_at_presentation (str): Seizure at or prior to initial presentation ('yes' or 'no')
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(csf_gram_stain, csf_anc, csf_protein, 
                            peripheral_blood_anc, seizure_at_presentation)
        
        # Calculate score
        score = self._calculate_score(csf_gram_stain, csf_anc, csf_protein,
                                    peripheral_blood_anc, seizure_at_presentation)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, csf_gram_stain: str, csf_anc: int, csf_protein: float,
                        peripheral_blood_anc: int, seizure_at_presentation: str):
        """Validates input parameters"""
        
        # Validate CSF Gram stain
        if csf_gram_stain not in ["negative", "positive"]:
            raise ValueError("CSF Gram stain must be 'negative' or 'positive'")
        
        # Validate CSF ANC
        if not isinstance(csf_anc, (int, float)) or csf_anc < 0:
            raise ValueError("CSF ANC must be a non-negative number")
        if csf_anc > 50000:
            raise ValueError("CSF ANC value seems unusually high (>50,000 cells/µL)")
        
        # Validate CSF protein
        if not isinstance(csf_protein, (int, float)) or csf_protein < 0:
            raise ValueError("CSF protein must be a non-negative number")
        if csf_protein > 1000:
            raise ValueError("CSF protein value seems unusually high (>1000 mg/dL)")
        
        # Validate peripheral blood ANC
        if not isinstance(peripheral_blood_anc, (int, float)) or peripheral_blood_anc < 0:
            raise ValueError("Peripheral blood ANC must be a non-negative number")
        if peripheral_blood_anc > 100000:
            raise ValueError("Peripheral blood ANC value seems unusually high (>100,000 cells/µL)")
        
        # Validate seizure at presentation
        if seizure_at_presentation not in ["yes", "no"]:
            raise ValueError("Seizure at presentation must be 'yes' or 'no'")
    
    def _calculate_score(self, csf_gram_stain: str, csf_anc: int, csf_protein: float,
                        peripheral_blood_anc: int, seizure_at_presentation: str) -> int:
        """Implements the Bacterial Meningitis Score formula"""
        
        score = 0
        
        # Positive Gram stain (1 point)
        if csf_gram_stain == "positive":
            score += 1
        
        # CSF ANC ≥1,000 cells/µL (1 point)
        if csf_anc >= self.CSF_ANC_THRESHOLD:
            score += 1
        
        # CSF protein ≥80 mg/dL (1 point)
        if csf_protein >= self.CSF_PROTEIN_THRESHOLD:
            score += 1
        
        # Peripheral blood ANC ≥10,000 cells/µL (1 point)
        if peripheral_blood_anc >= self.PERIPHERAL_ANC_THRESHOLD:
            score += 1
        
        # Seizure at presentation (1 point)
        if seizure_at_presentation == "yes":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated Bacterial Meningitis Score
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "Very Low Risk",
                "description": "Very low risk of bacterial meningitis",
                "interpretation": (
                    "Score of 0 indicates very low risk of bacterial meningitis "
                    "(risk approximately 0.1%). Consider discharge with close follow-up. "
                    "Clinical judgment should always supersede the score. Consider single "
                    "dose of parenteral antibiotics (e.g., ceftriaxone) prior to discharge "
                    "while awaiting bacterial cultures."
                )
            }
        else:
            return {
                "stage": "Not Very Low Risk",
                "description": "Not very low risk of bacterial meningitis",
                "interpretation": (
                    f"Score of {score} indicates patient is not very low risk for bacterial "
                    f"meningitis. Admission for parenteral antibiotics and monitoring is "
                    f"recommended while awaiting CSF culture results. Higher scores correlate "
                    f"with increased likelihood of bacterial meningitis."
                )
            }


def calculate_bacterial_meningitis_score(csf_gram_stain: str, csf_anc: int, csf_protein: float,
                                        peripheral_blood_anc: int, seizure_at_presentation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BacterialMeningitisScoreCalculator()
    return calculator.calculate(csf_gram_stain, csf_anc, csf_protein, 
                              peripheral_blood_anc, seizure_at_presentation)