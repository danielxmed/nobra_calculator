"""
AUDIT-C for Alcohol Use Calculator

Identifies at-risk drinkers who may not be alcohol dependent using a brief 
3-question screening tool derived from the full AUDIT questionnaire.

References:
1. Bush K, et al. The AUDIT alcohol consumption questions (AUDIT-C). Arch Intern Med. 1998;158(16):1789-95.
2. Bradley KA, et al. AUDIT-C as a brief screen for alcohol misuse in primary care. Alcohol Clin Exp Res. 2007;31(7):1208-17.
3. Frank D, et al. Effectiveness of the AUDIT-C as a screening test. J Gen Intern Med. 2008;23(6):781-7.
"""

from typing import Dict, Any


class AuditCCalculator:
    """Calculator for AUDIT-C Alcohol Use Screening"""
    
    def __init__(self):
        # Scoring for each question
        self.frequency_scores = {
            "never": 0,
            "monthly_or_less": 1,
            "2_to_4_times_month": 2,
            "2_to_3_times_week": 3,
            "4_or_more_times_week": 4
        }
        
        self.typical_drinks_scores = {
            "1_or_2": 0,
            "3_or_4": 1,
            "5_or_6": 2,
            "7_to_9": 3,
            "10_or_more": 4
        }
        
        self.six_or_more_scores = {
            "never": 0,
            "less_than_monthly": 1,
            "monthly": 2,
            "weekly": 3,
            "daily_or_almost_daily": 4
        }
        
        # Cutoff scores
        self.MALE_CUTOFF = 4
        self.FEMALE_CUTOFF = 3
    
    def calculate(self, frequency: str, typical_drinks: str, six_or_more: str, sex: str) -> Dict[str, Any]:
        """
        Calculates AUDIT-C score based on three alcohol consumption questions
        
        Args:
            frequency (str): Frequency of alcohol consumption
            typical_drinks (str): Number of drinks on typical drinking day
            six_or_more (str): Frequency of heavy drinking (6+ drinks)
            sex (str): Patient's biological sex (male/female)
            
        Returns:
            Dict with score and interpretation
        """
        
        # Validations
        self._validate_inputs(frequency, typical_drinks, six_or_more, sex)
        
        # Calculate score
        score = self._calculate_score(frequency, typical_drinks, six_or_more)
        
        # Get interpretation based on sex
        interpretation = self._get_interpretation(score, sex)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, frequency: str, typical_drinks: str, six_or_more: str, sex: str):
        """Validates input parameters"""
        
        if frequency not in self.frequency_scores:
            raise ValueError(f"Invalid frequency value: {frequency}")
        
        if typical_drinks not in self.typical_drinks_scores:
            raise ValueError(f"Invalid typical_drinks value: {typical_drinks}")
        
        if six_or_more not in self.six_or_more_scores:
            raise ValueError(f"Invalid six_or_more value: {six_or_more}")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
    
    def _calculate_score(self, frequency: str, typical_drinks: str, six_or_more: str) -> int:
        """Calculates total AUDIT-C score"""
        
        score = (
            self.frequency_scores[frequency] +
            self.typical_drinks_scores[typical_drinks] +
            self.six_or_more_scores[six_or_more]
        )
        
        return score
    
    def _get_interpretation(self, score: int, sex: str) -> Dict[str, str]:
        """
        Determines interpretation based on score and sex
        
        Args:
            score (int): AUDIT-C score (0-12)
            sex (str): Patient's sex
            
        Returns:
            Dict with interpretation details
        """
        
        cutoff = self.MALE_CUTOFF if sex == "male" else self.FEMALE_CUTOFF
        
        if score < cutoff:
            return {
                "stage": "Low risk",
                "description": "Low risk drinking pattern",
                "interpretation": f"""AUDIT-C Score: {score} points

This score suggests a low risk drinking pattern. No specific intervention is indicated based on this screening alone.

Scoring interpretation:
• For {sex}s: Scores ≥{cutoff} suggest alcohol misuse
• Current score of {score} is below the threshold

General guidance:
• Continue to monitor alcohol consumption
• Maintain awareness of safe drinking limits
• One standard drink = 12 oz beer (5%), 5 oz wine (12%), or 1.5 oz spirits (40%)"""
            }
        else:
            severity = self._get_severity(score)
            return {
                "stage": f"At risk ({sex.capitalize()})",
                "description": f"Score suggests alcohol misuse ({severity} severity)",
                "interpretation": f"""AUDIT-C Score: {score} points

This score suggests alcohol misuse for {sex} patients (cutoff ≥{cutoff}).

Severity assessment:
• Score {score}: {severity} severity of alcohol misuse
• Higher scores correlate with greater severity

Recommended actions:
• Further assessment with full AUDIT questionnaire may be warranted
• Consider brief intervention or referral to treatment
• Assess for alcohol use disorder using DSM-5 criteria
• Evaluate for medical complications of alcohol use

Note: The AUDIT-C is a screening tool and should be followed by clinical assessment for diagnosis."""
            }
    
    def _get_severity(self, score: int) -> str:
        """Determines severity level based on score"""
        if score <= 5:
            return "Mild"
        elif score <= 8:
            return "Moderate"
        else:
            return "Severe"


def calculate_audit_c(frequency: str, typical_drinks: str, six_or_more: str, sex: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AuditCCalculator()
    return calculator.calculate(frequency, typical_drinks, six_or_more, sex)