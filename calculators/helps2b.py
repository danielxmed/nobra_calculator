"""
2HELPS2B Score Calculator

Estimates seizure risk in acutely ill patients undergoing continuous EEG.
Developed by Struck et al. (2017) to optimize neurological monitoring duration.
"""

from typing import Dict, Any


class Helps2bCalculator:
    """Calculator for 2HELPS2B Score"""
    
    def calculate(self, seizure_history: str, epileptiform_discharges: str, 
                 lateralized_periodic_discharges: str, bilateral_independent_periodic_discharges: str,
                 brief_potentially_ictal_rhythmic_discharges: str, burst_suppression: str) -> Dict[str, Any]:
        """
        Calculates the 2HELPS2B Score
        
        Args:
            seizure_history: History of seizures ("yes" or "no")
            epileptiform_discharges: Epileptiform discharges ("present" or "absent")
            lateralized_periodic_discharges: Lateralized periodic discharges ("present" or "absent")
            bilateral_independent_periodic_discharges: Bilateral independent periodic discharges ("present" or "absent")
            brief_potentially_ictal_rhythmic_discharges: Brief potentially ictal rhythmic discharges ("present" or "absent")
            burst_suppression: Burst-suppression pattern ("present" or "absent")
            
        Returns:
            Dict with result and interpretation
        """
        
        # Validations
        self._validate_inputs(seizure_history, epileptiform_discharges, lateralized_periodic_discharges,
                            bilateral_independent_periodic_discharges, brief_potentially_ictal_rhythmic_discharges,
                            burst_suppression)
        
        # Calculate score
        score = self._calculate_score(seizure_history, epileptiform_discharges, lateralized_periodic_discharges,
                                    bilateral_independent_periodic_discharges, brief_potentially_ictal_rhythmic_discharges,
                                    burst_suppression)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, seizure_history, epileptiform_discharges, lateralized_periodic_discharges,
                        bilateral_independent_periodic_discharges, brief_potentially_ictal_rhythmic_discharges,
                        burst_suppression):
        """Validates input parameters"""
        
        valid_binary_options = ["yes", "no", "present", "absent"]
        
        if seizure_history not in ["yes", "no"]:
            raise ValueError("Seizure history must be 'yes' or 'no'")
        
        if epileptiform_discharges not in ["present", "absent"]:
            raise ValueError("Epileptiform discharges must be 'present' or 'absent'")
        
        if lateralized_periodic_discharges not in ["present", "absent"]:
            raise ValueError("Lateralized periodic discharges must be 'present' or 'absent'")
        
        if bilateral_independent_periodic_discharges not in ["present", "absent"]:
            raise ValueError("Bilateral independent periodic discharges must be 'present' or 'absent'")
        
        if brief_potentially_ictal_rhythmic_discharges not in ["present", "absent"]:
            raise ValueError("Brief potentially ictal rhythmic discharges must be 'present' or 'absent'")
        
        if burst_suppression not in ["present", "absent"]:
            raise ValueError("Burst-suppression pattern must be 'present' or 'absent'")
    
    def _calculate_score(self, seizure_history, epileptiform_discharges, lateralized_periodic_discharges,
                        bilateral_independent_periodic_discharges, brief_potentially_ictal_rhythmic_discharges,
                        burst_suppression):
        """Calculates the 2HELPS2B Score"""
        
        score = 0
        
        # Seizure history (1 point if present)
        if seizure_history == "yes":
            score += 1
        
        # Epileptiform discharges (1 point if present)
        if epileptiform_discharges == "present":
            score += 1
        
        # Lateralized periodic discharges - LPDs (1 point if present)
        if lateralized_periodic_discharges == "present":
            score += 1
        
        # Bilateral independent periodic discharges - BIPDs (1 point if present)
        if bilateral_independent_periodic_discharges == "present":
            score += 1
        
        # Brief potentially ictal rhythmic discharges - BIRDs (1 point if present)
        if brief_potentially_ictal_rhythmic_discharges == "present":
            score += 1
        
        # Burst-suppression pattern (1 point if present)
        if burst_suppression == "present":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated score (0-6)
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Very low seizure risk",
                "interpretation": "Seizure risk in 72h: 5%. Only 1-hour screening EEG recommended. Additional monitoring generally not necessary."
            }
        elif score == 1:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate seizure risk",
                "interpretation": "Seizure risk in 72h: 12%. 12-hour cEEG monitoring recommended to detect non-obvious seizures."
            }
        elif score == 2:
            return {
                "stage": "High Risk",
                "description": "High seizure risk",
                "interpretation": "Seizure risk in 72h: 27%. At least 24-hour cEEG monitoring recommended. Intensive neurological vigilance necessary."
            }
        elif score == 3:
            return {
                "stage": "Very High Risk",
                "description": "Very high seizure risk",
                "interpretation": "Seizure risk in 72h: 50%. Prolonged continuous monitoring (≥24h) highly recommended. Consider prophylactic anticonvulsant treatment."
            }
        elif score == 4:
            return {
                "stage": "Extreme Risk",
                "description": "Extremely high seizure risk",
                "interpretation": "Seizure risk in 72h: 73%. Mandatory prolonged continuous monitoring. Anticonvulsant treatment should be considered. Intensive neurological care."
            }
        elif score == 5:
            return {
                "stage": "Critical Risk",
                "description": "Critical seizure risk",
                "interpretation": "Seizure risk in 72h: 88%. Continuous monitoring in neurological ICU. Anticonvulsant treatment frequently indicated. Reserved prognosis."
            }
        else:  # score == 6
            return {
                "stage": "Maximum Risk",
                "description": "Maximum seizure risk",
                "interpretation": "Seizure risk in 72h: >95%. Mandatory continuous monitoring in ICU. Urgent anticonvulsant treatment and neuroprotective measures. Severe prognosis."
            }


def calculate_helps2b(seizure_history: str, epileptiform_discharges: str, 
                     lateralized_periodic_discharges: str, bilateral_independent_periodic_discharges: str,
                     brief_potentially_ictal_rhythmic_discharges: str, burst_suppression: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    """
    calculator = Helps2bCalculator()
    return calculator.calculate(seizure_history, epileptiform_discharges, lateralized_periodic_discharges,
                              bilateral_independent_periodic_discharges, brief_potentially_ictal_rhythmic_discharges,
                              burst_suppression)
