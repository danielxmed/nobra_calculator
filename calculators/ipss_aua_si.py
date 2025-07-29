"""
International Prostate Symptom Score (IPSS)/American Urological Association Symptom Index (AUA-SI) Calculator

Measures severity of benign prostatic hyperplasia (BPH) symptoms using 7 standardized 
questions about urinary symptoms. Used to guide treatment decisions and monitor response 
to therapy in men with lower urinary tract symptoms.

References:
- Barry MJ, Fowler FJ Jr, O'Leary MP, et al. The American Urological Association 
  symptom index for benign prostatic hyperplasia. J Urol. 1992;148(5):1549-57.
- Cockett AT, Aso Y, Denis L, et al. World Health Organization Consensus Committee 
  recommendations concerning the diagnosis of BPH. Prog Urol. 1991;1(6):957-72.
"""

from typing import Dict, Any


class IpssAuaSiCalculator:
    """Calculator for International Prostate Symptom Score (IPSS)/AUA Symptom Index"""
    
    def __init__(self):
        # Score ranges for symptom severity classification
        self.MILD_MIN = 0
        self.MILD_MAX = 7
        self.MODERATE_MIN = 8
        self.MODERATE_MAX = 19
        self.SEVERE_MIN = 20
        self.SEVERE_MAX = 35
        
        # Maximum possible score
        self.MAX_SCORE = 35
        self.MIN_SCORE = 0
        
    def calculate(self, incomplete_emptying: int, frequency: int, intermittency: int,
                 urgency: int, weak_stream: int, straining: int, nocturia: int) -> Dict[str, Any]:
        """
        Calculates the IPSS/AUA-SI score from 7 urinary symptom questions
        
        Args:
            incomplete_emptying (int): Sensation of not emptying bladder (0-5)
            frequency (int): Urinating less than every two hours (0-5)
            intermittency (int): Stopping and starting during urination (0-5)
            urgency (int): Difficulty postponing urination (0-5)
            weak_stream (int): Weak urinary stream (0-5)
            straining (int): Straining to start urination (0-5)
            nocturia (int): Number of times getting up at night to urinate (0-5)
            
        Returns:
            Dict containing the total score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(incomplete_emptying, frequency, intermittency,
                            urgency, weak_stream, straining, nocturia)
        
        # Calculate total IPSS score
        total_score = self._calculate_ipss_score(
            incomplete_emptying, frequency, intermittency,
            urgency, weak_stream, straining, nocturia
        )
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, incomplete_emptying: int, frequency: int, intermittency: int,
                        urgency: int, weak_stream: int, straining: int, nocturia: int):
        """Validates all input parameters"""
        
        # List of all parameters for validation
        params = [
            ("incomplete_emptying", incomplete_emptying),
            ("frequency", frequency),
            ("intermittency", intermittency),
            ("urgency", urgency),
            ("weak_stream", weak_stream),
            ("straining", straining),
            ("nocturia", nocturia)
        ]
        
        for param_name, param_value in params:
            # Check if parameter is an integer
            if not isinstance(param_value, int):
                raise ValueError(f"{param_name} must be an integer")
            
            # Check if parameter is within valid range (0-5)
            if param_value < 0 or param_value > 5:
                raise ValueError(f"{param_name} must be between 0 and 5, got {param_value}")
    
    def _calculate_ipss_score(self, incomplete_emptying: int, frequency: int, intermittency: int,
                             urgency: int, weak_stream: int, straining: int, nocturia: int) -> int:
        """
        Calculates the total IPSS score by summing all 7 symptom questions
        
        Each question contributes 0-5 points to the total score.
        Total possible range: 0-35 points.
        """
        total_score = (
            incomplete_emptying +    # Incomplete emptying (0-5 points)
            frequency +             # Urinary frequency (0-5 points)
            intermittency +         # Intermittent stream (0-5 points)
            urgency +               # Urinary urgency (0-5 points)
            weak_stream +           # Weak stream (0-5 points)
            straining +             # Straining to urinate (0-5 points)
            nocturia                # Nocturia episodes (0-5 points)
        )
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines BPH symptom severity and clinical recommendations
        
        Args:
            score (int): IPSS total score (0-35 points)
            
        Returns:
            Dict with severity classification and treatment recommendations
        """
        
        if score <= self.MILD_MAX:
            return {
                "stage": "Mild",
                "description": "Mild BPH symptoms",
                "interpretation": "Mild benign prostatic hyperplasia symptoms. Patient may be managed with watchful waiting, lifestyle modifications, and regular monitoring. Medical treatment generally not required unless bothersome to patient."
            }
        elif score <= self.MODERATE_MAX:
            return {
                "stage": "Moderate",
                "description": "Moderate BPH symptoms",
                "interpretation": "Moderate benign prostatic hyperplasia symptoms. Consider medical treatment with alpha-blockers, 5-alpha reductase inhibitors, or combination therapy. Lifestyle modifications and regular follow-up recommended."
            }
        else:  # score >= SEVERE_MIN
            return {
                "stage": "Severe",
                "description": "Severe BPH symptoms",
                "interpretation": "Severe benign prostatic hyperplasia symptoms. Medical treatment strongly recommended. Consider surgical intervention if medical therapy fails or patient has complications such as recurrent UTIs, bladder stones, or renal insufficiency."
            }


def calculate_ipss_aua_si(incomplete_emptying: int, frequency: int, intermittency: int,
                         urgency: int, weak_stream: int, straining: int, nocturia: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates IPSS/AUA-SI score for BPH symptom severity assessment.
    """
    calculator = IpssAuaSiCalculator()
    return calculator.calculate(incomplete_emptying, frequency, intermittency,
                              urgency, weak_stream, straining, nocturia)