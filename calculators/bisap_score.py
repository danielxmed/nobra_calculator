"""
BISAP Score for Pancreatitis Mortality Calculator

Predicts mortality risk in pancreatitis with fewer variables than Ranson's.

References (Vancouver style):
1. Wu BU, Johannes RS, Sun X, Tabak Y, Conwell DL, Banks PA. The early prediction of 
   mortality in acute pancreatitis: a large population-based study. Gut. 2008 Dec;57(12):1698-703.
2. Singh VK, Wu BU, Bollen TL, Repas K, Maurer R, Johannes RS, et al. A prospective 
   evaluation of the bedside index for severity in acute pancreatitis score in assessing 
   mortality and intermediate markers of severity in acute pancreatitis. Am J Gastroenterol. 
   2009 Apr;104(4):966-71.
3. Gao W, Yang HX, Ma CE. The Value of BISAP Score for Predicting Mortality and Severity 
   in Acute Pancreatitis: A Systematic Review and Meta-Analysis. PLoS One. 2015 Jun 22;10(6):e0130412.
"""

from typing import Dict, Any


class BisapScoreCalculator:
    """Calculator for BISAP Score for Pancreatitis Mortality"""
    
    def __init__(self):
        # BISAP criteria descriptions
        self.criteria_descriptions = {
            "B": "Blood Urea Nitrogen (BUN) > 25 mg/dL",
            "I": "Impaired mental status or GCS < 15",
            "S": "≥2 SIRS criteria",
            "A": "Age > 60 years", 
            "P": "Pleural effusion on imaging"
        }
        
        # SIRS criteria definition
        self.sirs_definition = (
            "SIRS criteria (≥2 required): pulse >90 bpm, respirations >20/min or "
            "PaCO2 <32 mmHg, temperature >38°C or <36°C, WBC >12,000 or <4,000 cells/mm³ "
            "or >10% bands"
        )
    
    def calculate(self, bun_elevated: str, impaired_mental_status: str, 
                  sirs_criteria: str, age_over_60: str, pleural_effusion: str) -> Dict[str, Any]:
        """
        Calculates the BISAP score
        
        Args:
            bun_elevated: BUN > 25 mg/dL ("yes"/"no")
            impaired_mental_status: Impaired mental status or GCS < 15 ("yes"/"no")
            sirs_criteria: ≥2 SIRS criteria present ("yes"/"no")
            age_over_60: Age > 60 years ("yes"/"no")
            pleural_effusion: Pleural effusion on imaging ("yes"/"no")
            
        Returns:
            Dict with BISAP score and interpretation
        """
        
        # Calculate score by summing positive criteria
        score = 0
        positive_criteria = []
        
        if bun_elevated == "yes":
            score += 1
            positive_criteria.append("B - Elevated BUN (>25 mg/dL)")
        
        if impaired_mental_status == "yes":
            score += 1
            positive_criteria.append("I - Impaired mental status (GCS <15)")
        
        if sirs_criteria == "yes":
            score += 1
            positive_criteria.append("S - SIRS criteria (≥2 present)")
        
        if age_over_60 == "yes":
            score += 1
            positive_criteria.append("A - Age >60 years")
        
        if pleural_effusion == "yes":
            score += 1
            positive_criteria.append("P - Pleural effusion present")
        
        # Generate interpretation
        interpretation = self._generate_interpretation(score, positive_criteria)
        
        # Get severity classification
        severity = self._get_severity_classification(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation,
            "stage": severity["stage"],
            "stage_description": severity["description"]
        }
    
    def _get_severity_classification(self, score: int) -> Dict[str, str]:
        """Gets severity classification based on score"""
        
        if score <= 2:
            return {
                "stage": "Low Risk",
                "description": "Mild acute pancreatitis with low mortality risk (<2%)"
            }
        else:  # score >= 3
            return {
                "stage": "High Risk", 
                "description": "Severe acute pancreatitis with high mortality risk (15-20%)"
            }
    
    def _generate_interpretation(self, score: int, positive_criteria: list) -> str:
        """Generates detailed interpretation of the BISAP score"""
        
        interpretation_parts = []
        
        # Score and risk level
        if score <= 2:
            interpretation_parts.append(
                f"BISAP score: {score}/5 points. Low risk for mortality (<2% mortality rate). "
                "This suggests mild acute pancreatitis."
            )
        else:
            interpretation_parts.append(
                f"BISAP score: {score}/5 points. High risk for mortality (15-20% mortality rate). "
                "This suggests severe acute pancreatitis requiring intensive monitoring and management."
            )
        
        # Present criteria
        if positive_criteria:
            interpretation_parts.append(
                f"Positive criteria: {', '.join(positive_criteria)}."
            )
        else:
            interpretation_parts.append("No BISAP criteria are positive.")
        
        # Clinical recommendations based on score
        if score <= 2:
            interpretation_parts.append(
                "Management: Standard supportive care with fluid resuscitation, pain control, "
                "and nutritional support. Monitor for complications."
            )
        else:
            interpretation_parts.append(
                "Management: Consider ICU admission or close monitoring. Aggressive fluid "
                "resuscitation, organ support as needed, early nutritional support, and "
                "monitoring for complications including organ failure and pancreatic necrosis."
            )
        
        # Additional clinical pearls
        interpretation_parts.append(
            "Note: BISAP score should be used in conjunction with clinical judgment. "
            "The score has 56% sensitivity and 91% specificity for mortality prediction at cutoff ≥3."
        )
        
        return " ".join(interpretation_parts)


def calculate_bisap_score(bun_elevated: str, impaired_mental_status: str, 
                         sirs_criteria: str, age_over_60: str, 
                         pleural_effusion: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BisapScoreCalculator()
    return calculator.calculate(
        bun_elevated, impaired_mental_status, sirs_criteria, 
        age_over_60, pleural_effusion
    )