"""
Rule of 7s for Lyme Meningitis Calculator

Distinguishes Lyme meningitis from aseptic meningitis in pediatric patients 
(ages 2-18) in Lyme endemic areas. This validated clinical prediction rule 
identifies children at low risk for Lyme meningitis.

References (Vancouver style):
1. Avery RA, Frank G, Glutting JJ, Eppes SC. Prediction of Lyme meningitis in 
   children from a Lyme disease-endemic region: a logistic-regression model using 
   history, physical, and laboratory findings. Pediatrics. 2006 Aug;118(2):e477-81. 
   doi: 10.1542/peds.2005-3043.
2. Garro AC, Rutman M, Simonsen K, Jaeger JL, Chapin K, Lockhart G. Prospective 
   validation of a clinical prediction model for Lyme meningitis in children. 
   Pediatrics. 2009 May;123(5):e829-34. doi: 10.1542/peds.2008-2048.
3. Cohn KA, Thompson AD, Shah SS, Hines EM, Lyons TW, Welsh EJ, Levas MN, 
   Lewander WJ, Bennett NJ, Nigrovic LE. Validation of a Clinical Prediction Rule 
   to Distinguish Lyme Meningitis From Aseptic Meningitis. Pediatrics. 
   2012 Jan;129(1):e46-53. doi: 10.1542/peds.2011-1215.
"""

from typing import Dict, Any


class RuleOf7sLymeMeningitisCalculator:
    """Calculator for Rule of 7s for Lyme Meningitis prediction"""
    
    def __init__(self):
        # Scoring thresholds based on validation studies
        self.HEADACHE_THRESHOLD = 7      # ≥7 days of headache = 1 point
        self.CSF_MONONUCLEAR_THRESHOLD = 70.0  # ≥70% mononuclear cells = 1 point
        
        # Performance characteristics from validation studies
        self.SENSITIVITY = 0.96          # 96% sensitivity (95% CI: 90-99%)
        self.SPECIFICITY = 0.41          # 41% specificity (95% CI: 36-47%)
        self.NPV_LOW_RISK = 1.0          # 100% NPV for <10% probability
        self.PPV_HIGH_RISK = 1.0         # 100% PPV for >50% probability
        
        # Risk probabilities
        self.LOW_RISK_PROBABILITY = 0.10  # <10% probability with score 0
        self.HIGH_RISK_PROBABILITY = 0.50 # >50% probability with score ≥1
    
    def calculate(self, headache_days: int, csf_mononuclear_percentage: float, 
                  cranial_nerve_palsy: str) -> Dict[str, Any]:
        """
        Calculates the Rule of 7s score for Lyme meningitis prediction
        
        The Rule of 7s identifies children at low risk for Lyme meningitis when
        ALL three criteria are met (score = 0): <7 days headache, <70% CSF 
        mononuclear cells, and no cranial nerve palsy.
        
        Args:
            headache_days (int): Number of days of headache symptoms (1-30)
            csf_mononuclear_percentage (float): Percentage of mononuclear cells in CSF (0-100%)
            cranial_nerve_palsy (str): Presence of cranial nerve palsy ("present" or "absent")
            
        Returns:
            Dict with the Rule of 7s score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(headache_days, csf_mononuclear_percentage, cranial_nerve_palsy)
        
        # Calculate Rule of 7s score
        score = self._calculate_score(headache_days, csf_mononuclear_percentage, cranial_nerve_palsy)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(score, headache_days, 
                                                csf_mononuclear_percentage, cranial_nerve_palsy)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, headache_days: int, csf_mononuclear_percentage: float, 
                        cranial_nerve_palsy: str):
        """Validates input parameters for Rule of 7s calculation"""
        
        # Headache days validation
        if not isinstance(headache_days, int):
            raise ValueError("Headache days must be an integer")
        
        if headache_days < 1 or headache_days > 30:
            raise ValueError("Headache days must be between 1 and 30 days")
        
        # CSF mononuclear percentage validation
        if not isinstance(csf_mononuclear_percentage, (int, float)):
            raise ValueError("CSF mononuclear percentage must be a number")
        
        if csf_mononuclear_percentage < 0 or csf_mononuclear_percentage > 100:
            raise ValueError("CSF mononuclear percentage must be between 0% and 100%")
        
        # Cranial nerve palsy validation
        if not isinstance(cranial_nerve_palsy, str):
            raise ValueError("Cranial nerve palsy must be a string")
        
        if cranial_nerve_palsy.lower() not in ["present", "absent"]:
            raise ValueError("Cranial nerve palsy must be 'present' or 'absent'")
        
        # Clinical validity checks
        if csf_mononuclear_percentage < 10:
            raise ValueError("Clinical concern: Very low mononuclear percentage - verify CSF analysis accuracy")
        
        if headache_days > 14:
            raise ValueError("Clinical concern: Prolonged headache duration may suggest alternative diagnosis")
    
    def _calculate_score(self, headache_days: int, csf_mononuclear_percentage: float, 
                        cranial_nerve_palsy: str) -> int:
        """
        Calculates the Rule of 7s score based on three criteria
        
        Scoring criteria:
        1. ≥7 days of headache = 1 point
        2. ≥70% CSF mononuclear cells = 1 point  
        3. Presence of cranial nerve palsy = 1 point
        
        Args:
            headache_days (int): Days of headache symptoms
            csf_mononuclear_percentage (float): CSF mononuclear cell percentage
            cranial_nerve_palsy (str): Cranial nerve palsy status
            
        Returns:
            int: Rule of 7s score (0-3 points)
        """
        
        score = 0
        
        # Criterion 1: ≥7 days of headache
        if headache_days >= self.HEADACHE_THRESHOLD:
            score += 1
        
        # Criterion 2: ≥70% CSF mononuclear cells
        if csf_mononuclear_percentage >= self.CSF_MONONUCLEAR_THRESHOLD:
            score += 1
        
        # Criterion 3: Presence of cranial nerve palsy
        if cranial_nerve_palsy.lower() == "present":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int, headache_days: int, 
                          csf_mononuclear_percentage: float, cranial_nerve_palsy: str) -> Dict[str, str]:
        """
        Provides detailed clinical interpretation based on Rule of 7s score
        
        Args:
            score (int): Calculated Rule of 7s score
            headache_days (int): Days of headache for context
            csf_mononuclear_percentage (float): CSF mononuclear percentage for context
            cranial_nerve_palsy (str): Cranial nerve palsy status for context
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        # Create detailed clinical context
        clinical_context = (
            f"Clinical parameters: {headache_days} days of headache, "
            f"{csf_mononuclear_percentage:.1f}% CSF mononuclear cells, "
            f"cranial nerve palsy {cranial_nerve_palsy.lower()}"
        )
        
        if score == 0:
            return {
                "stage": "Low Risk for Lyme Meningitis",
                "description": "Outpatient management appropriate",
                "interpretation": (
                    f"Low risk for Lyme meningitis (<10% probability). Patient meets all three "
                    f"'Rule of 7s' criteria for low risk: <7 days of headache, <70% CSF mononuclear "
                    f"cells, and no cranial nerve palsy. {clinical_context}. These children can be "
                    f"safely managed as outpatients while awaiting Lyme serology results. Consider "
                    f"discharge home with close outpatient follow-up, symptomatic treatment, and "
                    f"clear return precautions. Avoid unnecessary hospitalization and empirical "
                    f"parenteral antibiotics. Ensure proper follow-up within 24-48 hours and clear "
                    f"instructions for return if symptoms worsen."
                )
            }
        
        else:  # score 1-3
            risk_factors = []
            if headache_days >= self.HEADACHE_THRESHOLD:
                risk_factors.append(f"prolonged headache (≥{self.HEADACHE_THRESHOLD} days)")
            if csf_mononuclear_percentage >= self.CSF_MONONUCLEAR_THRESHOLD:
                risk_factors.append(f"high CSF mononuclear percentage (≥{self.CSF_MONONUCLEAR_THRESHOLD}%)")
            if cranial_nerve_palsy.lower() == "present":
                risk_factors.append("cranial nerve palsy present")
            
            risk_factors_text = ", ".join(risk_factors)
            
            return {
                "stage": "Not Low Risk for Lyme Meningitis",
                "description": "Consider inpatient management and empirical treatment",
                "interpretation": (
                    f"Not low risk for Lyme meningitis - higher probability of Lyme meningitis "
                    f"cannot be excluded (Rule of 7s score: {score}/3 points). Patient does not "
                    f"meet all criteria for low risk classification by the Rule of 7s. "
                    f"{clinical_context}. Risk factors present: {risk_factors_text}. Consider "
                    f"inpatient management with empirical antibiotic treatment for Lyme meningitis "
                    f"while awaiting confirmatory serology results. Initiate appropriate antibiotics "
                    f"(ceftriaxone) if clinical suspicion is high. Monitor closely for neurologic "
                    f"complications and clinical deterioration. Obtain comprehensive Lyme serology "
                    f"testing and consider additional diagnostic evaluation as clinically indicated."
                )
            }


def calculate_rule_of_7s_lyme_meningitis(headache_days: int, csf_mononuclear_percentage: float, 
                                       cranial_nerve_palsy: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates Rule of 7s score for distinguishing Lyme meningitis from aseptic meningitis.
    
    Args:
        headache_days (int): Number of days of headache symptoms
        csf_mononuclear_percentage (float): Percentage of mononuclear cells in CSF
        cranial_nerve_palsy (str): Presence of cranial nerve palsy ("present" or "absent")
        
    Returns:
        Dict with Rule of 7s score and clinical interpretation
    """
    calculator = RuleOf7sLymeMeningitisCalculator()
    return calculator.calculate(headache_days, csf_mononuclear_percentage, cranial_nerve_palsy)