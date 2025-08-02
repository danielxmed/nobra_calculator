"""
HINTS for Stroke in Acute Vestibular Syndrome Calculator

Differentiates between peripheral and central causes of acute vestibular syndrome.

References:
- Kattah JC, et al. Stroke. 2009;40(11):3504-10.
- Newman-Toker DE, et al. Acad Emerg Med. 2013;20(10):986-96.
- Kerber KA, et al. Neurology. 2015;85(21):1869-78.
"""

from typing import Dict, Any


class HintsCalculator:
    """Calculator for HINTS examination"""
    
    def __init__(self):
        # Central findings that indicate dangerous HINTS
        self.CENTRAL_HEAD_IMPULSE = ["normal", "not_testable"]
        self.CENTRAL_NYSTAGMUS = ["direction_changing", "not_testable"]
        self.CENTRAL_SKEW = ["present", "not_testable"]
        
        # Peripheral findings that indicate benign HINTS
        self.PERIPHERAL_HEAD_IMPULSE = "abnormal"
        self.PERIPHERAL_NYSTAGMUS = "direction_fixed"
        self.PERIPHERAL_SKEW = "absent"
    
    def calculate(self, head_impulse_test: str, nystagmus: str, 
                  test_of_skew: str) -> Dict[str, Any]:
        """
        Evaluates HINTS examination findings
        
        Args:
            head_impulse_test (str): "normal", "abnormal", or "not_testable"
            nystagmus (str): "direction_fixed", "direction_changing", or "not_testable"
            test_of_skew (str): "absent", "present", or "not_testable"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(head_impulse_test, nystagmus, test_of_skew)
        
        # Check for central findings
        central_findings = 0
        
        if head_impulse_test in self.CENTRAL_HEAD_IMPULSE:
            central_findings += 1
        
        if nystagmus in self.CENTRAL_NYSTAGMUS:
            central_findings += 1
        
        if test_of_skew in self.CENTRAL_SKEW:
            central_findings += 1
        
        # Determine if HINTS is benign or dangerous
        if central_findings > 0:
            result = "Dangerous HINTS"
            score = 1
        else:
            # All findings must be peripheral for benign HINTS
            if (head_impulse_test == self.PERIPHERAL_HEAD_IMPULSE and
                nystagmus == self.PERIPHERAL_NYSTAGMUS and
                test_of_skew == self.PERIPHERAL_SKEW):
                result = "Benign HINTS"
                score = 0
            else:
                result = "Dangerous HINTS"
                score = 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": result,
            "unit": "pattern",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, head_impulse_test: str, nystagmus: str, 
                        test_of_skew: str):
        """Validates input parameters"""
        
        valid_hit = ["normal", "abnormal", "not_testable"]
        valid_nystagmus = ["direction_fixed", "direction_changing", "not_testable"]
        valid_skew = ["absent", "present", "not_testable"]
        
        if head_impulse_test not in valid_hit:
            raise ValueError(f"Head impulse test must be one of {valid_hit}")
        
        if nystagmus not in valid_nystagmus:
            raise ValueError(f"Nystagmus must be one of {valid_nystagmus}")
        
        if test_of_skew not in valid_skew:
            raise ValueError(f"Test of skew must be one of {valid_skew}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): 0 for benign, 1 for dangerous
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Benign HINTS",
                "description": "Suggests peripheral cause",
                "interpretation": "Pattern consistent with peripheral vestibular disorder. "
                                "All three findings point to peripheral etiology: abnormal "
                                "head impulse test, direction-fixed horizontal nystagmus, "
                                "and absent skew deviation. Consider vestibular neuritis "
                                "or labyrinthitis."
            }
        else:
            return {
                "stage": "Dangerous HINTS",
                "description": "Suggests central cause",
                "interpretation": "Pattern concerning for central pathology, particularly "
                                "posterior circulation stroke. One or more findings suggest "
                                "central etiology. Strongly consider neuroimaging and stroke "
                                "workup. Note that early MRI (<48 hours) may be falsely "
                                "negative for posterior circulation strokes."
            }


def calculate_hints(head_impulse_test: str, nystagmus: str, 
                    test_of_skew: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HintsCalculator()
    return calculator.calculate(head_impulse_test, nystagmus, test_of_skew)