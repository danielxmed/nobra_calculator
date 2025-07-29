"""
Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS) Calculator

Provides diagnostic criteria for acute respiratory distress syndrome (ARDS) and classifies 
severity based on oxygenation according to the 2012 Berlin Definition.

References (Vancouver style):
1. Ranieri VM, Rubenfeld GD, Thompson BT, Ferguson ND, Caldwell E, Fan E, et al; 
   ARDS Definition Task Force. Acute respiratory distress syndrome: the Berlin Definition. 
   JAMA. 2012 Jun 20;307(23):2526-33.
2. Fan E, Brodie D, Slutsky AS. Acute Respiratory Distress Syndrome: Advances in 
   Diagnosis and Treatment. JAMA. 2018 Feb 20;319(7):698-710.
3. Matthay MA, Zemans RL, Zimmerman GA, Arabi YM, Beitler JR, Mercat A, et al. 
   Acute respiratory distress syndrome. Nat Rev Dis Primers. 2019 Mar 14;5(1):18.
"""

from typing import Dict, Any


class BerlinCriteriaArdsCalculator:
    """Calculator for Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS)"""
    
    def __init__(self):
        # ARDS severity thresholds based on PaO2/FiO2 ratio
        self.MILD_ARDS_MIN = 200
        self.MILD_ARDS_MAX = 300
        self.MODERATE_ARDS_MIN = 100
        self.MODERATE_ARDS_MAX = 200
        self.SEVERE_ARDS_MAX = 100
    
    def calculate(self, timing_within_one_week: str, bilateral_opacities: str, 
                 not_cardiac_failure: str, ards_risk_factor: str, 
                 pao2_fio2_ratio: float, peep_at_least_5: str) -> Dict[str, Any]:
        """
        Calculates ARDS diagnosis and severity classification using Berlin Criteria
        
        Args:
            timing_within_one_week (str): Acute onset within 1 week ("yes" or "no")
            bilateral_opacities (str): Bilateral opacities on chest imaging ("yes" or "no")
            not_cardiac_failure (str): Not explained by cardiac failure ("yes" or "no")
            ards_risk_factor (str): Presence of ARDS risk factor ("yes" or "no")
            pao2_fio2_ratio (float): PaO2/FiO2 ratio in mmHg with PEEP ≥5 cm H2O
            peep_at_least_5 (str): PEEP or CPAP ≥5 cm H2O ("yes" or "no")
            
        Returns:
            Dict with ARDS diagnosis, severity classification, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(timing_within_one_week, bilateral_opacities, 
                            not_cardiac_failure, ards_risk_factor, 
                            pao2_fio2_ratio, peep_at_least_5)
        
        # Check if all Berlin criteria are met
        meets_all_criteria = self._check_all_criteria(
            timing_within_one_week, bilateral_opacities, 
            not_cardiac_failure, ards_risk_factor, peep_at_least_5
        )
        
        if not meets_all_criteria:
            return {
                "result": "No ARDS",
                "unit": "classification",
                "interpretation": "Patient does not meet all required criteria for ARDS diagnosis. Review alternative diagnoses for acute respiratory failure.",
                "stage": "No ARDS",
                "stage_description": "Does not meet Berlin criteria for ARDS"
            }
        
        # Determine ARDS severity based on PaO2/FiO2 ratio
        severity_classification = self._classify_severity(pao2_fio2_ratio)
        interpretation = self._get_interpretation(severity_classification)
        
        return {
            "result": severity_classification,
            "unit": "classification",
            "interpretation": interpretation["interpretation"],
            "stage": severity_classification,
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, timing_within_one_week, bilateral_opacities, 
                        not_cardiac_failure, ards_risk_factor, 
                        pao2_fio2_ratio, peep_at_least_5):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = [
            ("timing_within_one_week", timing_within_one_week),
            ("bilateral_opacities", bilateral_opacities),
            ("not_cardiac_failure", not_cardiac_failure),
            ("ards_risk_factor", ards_risk_factor),
            ("peep_at_least_5", peep_at_least_5)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate PaO2/FiO2 ratio
        if not isinstance(pao2_fio2_ratio, (int, float)):
            raise ValueError("pao2_fio2_ratio must be a number")
        
        if pao2_fio2_ratio < 50 or pao2_fio2_ratio > 500:
            raise ValueError("pao2_fio2_ratio must be between 50 and 500 mmHg")
    
    def _check_all_criteria(self, timing_within_one_week, bilateral_opacities, 
                           not_cardiac_failure, ards_risk_factor, peep_at_least_5):
        """
        Checks if all four Berlin criteria are met for ARDS diagnosis
        
        Returns:
            bool: True if all criteria are met, False otherwise
        """
        
        criteria = [
            timing_within_one_week == "yes",
            bilateral_opacities == "yes",
            not_cardiac_failure == "yes",
            ards_risk_factor == "yes",
            peep_at_least_5 == "yes"
        ]
        
        return all(criteria)
    
    def _classify_severity(self, pao2_fio2_ratio: float) -> str:
        """
        Classifies ARDS severity based on PaO2/FiO2 ratio
        
        Args:
            pao2_fio2_ratio (float): PaO2/FiO2 ratio in mmHg
            
        Returns:
            str: ARDS severity classification
        """
        
        if pao2_fio2_ratio <= self.SEVERE_ARDS_MAX:
            return "Severe ARDS"
        elif pao2_fio2_ratio <= self.MODERATE_ARDS_MAX:
            return "Moderate ARDS"
        elif pao2_fio2_ratio <= self.MILD_ARDS_MAX:
            return "Mild ARDS"
        else:
            # This shouldn't happen if all criteria are met, but handle edge case
            return "No ARDS"
    
    def _get_interpretation(self, severity: str) -> Dict[str, str]:
        """
        Provides clinical interpretation and management recommendations
        
        Args:
            severity (str): ARDS severity classification
            
        Returns:
            Dict with interpretation and description
        """
        
        interpretations = {
            "Mild ARDS": {
                "description": "PaO2/FiO2 >200 to ≤300 mmHg with PEEP ≥5 cm H2O",
                "interpretation": "Patient meets criteria for mild ARDS. Consider lung-protective ventilation strategies, conservative fluid management, and monitoring for progression."
            },
            "Moderate ARDS": {
                "description": "PaO2/FiO2 >100 to ≤200 mmHg with PEEP ≥5 cm H2O",
                "interpretation": "Patient meets criteria for moderate ARDS. Implement lung-protective ventilation, consider higher PEEP strategies, prone positioning, and close monitoring."
            },
            "Severe ARDS": {
                "description": "PaO2/FiO2 ≤100 mmHg with PEEP ≥5 cm H2O",
                "interpretation": "Patient meets criteria for severe ARDS. Implement aggressive lung-protective strategies, consider prone positioning, neuromuscular blockade, and potentially ECMO consultation."
            },
            "No ARDS": {
                "description": "Does not meet Berlin criteria for ARDS",
                "interpretation": "Patient does not meet all required criteria for ARDS diagnosis. Review alternative diagnoses for acute respiratory failure."
            }
        }
        
        return interpretations.get(severity, interpretations["No ARDS"])


def calculate_berlin_criteria_ards(timing_within_one_week: str, bilateral_opacities: str, 
                                 not_cardiac_failure: str, ards_risk_factor: str, 
                                 pao2_fio2_ratio: float, peep_at_least_5: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates ARDS diagnosis and severity classification using the 2012 Berlin Definition.
    All four criteria must be met for ARDS diagnosis: timing (≤7 days), bilateral opacities,
    exclusion of cardiac causes, and presence of risk factors. Severity is classified based
    on PaO2/FiO2 ratio measured with PEEP ≥5 cm H2O.
    """
    calculator = BerlinCriteriaArdsCalculator()
    return calculator.calculate(timing_within_one_week, bilateral_opacities, 
                               not_cardiac_failure, ards_risk_factor, 
                               pao2_fio2_ratio, peep_at_least_5)