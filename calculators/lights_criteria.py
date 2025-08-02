"""
Light's Criteria for Exudative Effusions Calculator

Determines if pleural fluid is exudative or transudative by comparing pleural 
fluid and serum protein and lactate dehydrogenase (LDH) levels.

References:
1. Light RW, Macgregor MI, Luchsinger PC, Ball WC Jr. Pleural effusions: the 
   diagnostic separation of transudates and exudates. Ann Intern Med. 1972 
   Oct;77(4):507-13. doi: 10.7326/0003-4819-77-4-507.
2. Heffner JE, Brown LK, Barbieri C, DeLeo JM. Pleural fluid chemical analysis 
   in parapneumonic effusions. A meta-analysis. Am J Respir Crit Care Med. 1995 
   Jun;151(6):1700-8.
"""

from typing import Dict, Any, Optional


class LightsCriteriaCalculator:
    """Calculator for Light's Criteria for Exudative Effusions"""
    
    def __init__(self):
        # Default upper limit of normal for serum LDH (U/L)
        self.DEFAULT_LDH_UPPER_NORMAL = 222.0
        
        # Threshold values for Light's criteria
        self.PROTEIN_RATIO_THRESHOLD = 0.5
        self.LDH_RATIO_THRESHOLD = 0.6
        self.LDH_FRACTION_THRESHOLD = 2.0 / 3.0  # Two-thirds
    
    def calculate(
        self,
        serum_protein: float,
        pleural_fluid_protein: float,
        serum_ldh: float,
        pleural_fluid_ldh: float,
        serum_ldh_upper_normal: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates Light's Criteria to determine if pleural effusion is exudative or transudative
        
        Args:
            serum_protein (float): Total serum protein level in g/dL
            pleural_fluid_protein (float): Pleural fluid protein level in g/dL
            serum_ldh (float): Serum lactate dehydrogenase level in U/L
            pleural_fluid_ldh (float): Pleural fluid lactate dehydrogenase level in U/L
            serum_ldh_upper_normal (float, optional): Upper limit of normal for serum LDH in U/L
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            serum_protein, pleural_fluid_protein, serum_ldh, 
            pleural_fluid_ldh, serum_ldh_upper_normal
        )
        
        # Use default if upper normal not provided
        if serum_ldh_upper_normal is None:
            serum_ldh_upper_normal = self.DEFAULT_LDH_UPPER_NORMAL
        
        # Calculate the three Light's criteria
        criteria_results = self._evaluate_criteria(
            serum_protein, pleural_fluid_protein, serum_ldh, 
            pleural_fluid_ldh, serum_ldh_upper_normal
        )
        
        # Determine if exudate (any criteria met) or transudate (no criteria met)
        criteria_met = sum(criteria_results.values())
        is_exudate = criteria_met > 0
        
        # Get interpretation
        interpretation = self._get_interpretation(
            is_exudate, criteria_results, criteria_met,
            serum_protein, pleural_fluid_protein, serum_ldh, 
            pleural_fluid_ldh, serum_ldh_upper_normal
        )
        
        return {
            "result": criteria_met,
            "unit": "criteria",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(
        self, serum_protein, pleural_fluid_protein, serum_ldh, 
        pleural_fluid_ldh, serum_ldh_upper_normal
    ):
        """Validates input parameters"""
        
        if not isinstance(serum_protein, (int, float)) or serum_protein <= 0:
            raise ValueError("Serum protein must be a positive number")
        
        if serum_protein < 1.0 or serum_protein > 15.0:
            raise ValueError("Serum protein must be between 1.0 and 15.0 g/dL")
        
        if not isinstance(pleural_fluid_protein, (int, float)) or pleural_fluid_protein < 0:
            raise ValueError("Pleural fluid protein must be a non-negative number")
        
        if pleural_fluid_protein < 0.1 or pleural_fluid_protein > 10.0:
            raise ValueError("Pleural fluid protein must be between 0.1 and 10.0 g/dL")
        
        if not isinstance(serum_ldh, (int, float)) or serum_ldh <= 0:
            raise ValueError("Serum LDH must be a positive number")
        
        if serum_ldh < 50.0 or serum_ldh > 2000.0:
            raise ValueError("Serum LDH must be between 50 and 2000 U/L")
        
        if not isinstance(pleural_fluid_ldh, (int, float)) or pleural_fluid_ldh < 0:
            raise ValueError("Pleural fluid LDH must be a non-negative number")
        
        if pleural_fluid_ldh < 10.0 or pleural_fluid_ldh > 5000.0:
            raise ValueError("Pleural fluid LDH must be between 10 and 5000 U/L")
        
        if serum_ldh_upper_normal is not None:
            if not isinstance(serum_ldh_upper_normal, (int, float)) or serum_ldh_upper_normal <= 0:
                raise ValueError("Serum LDH upper normal must be a positive number")
            
            if serum_ldh_upper_normal < 100.0 or serum_ldh_upper_normal > 500.0:
                raise ValueError("Serum LDH upper normal must be between 100 and 500 U/L")
    
    def _evaluate_criteria(
        self, serum_protein, pleural_fluid_protein, serum_ldh, 
        pleural_fluid_ldh, serum_ldh_upper_normal
    ) -> Dict[str, bool]:
        """
        Evaluates the three Light's criteria
        
        Returns:
            Dict with results for each criterion
        """
        
        # Criterion 1: Pleural fluid protein / Serum protein > 0.5
        protein_ratio = pleural_fluid_protein / serum_protein
        criterion_1 = protein_ratio > self.PROTEIN_RATIO_THRESHOLD
        
        # Criterion 2: Pleural fluid LDH / Serum LDH > 0.6
        ldh_ratio = pleural_fluid_ldh / serum_ldh
        criterion_2 = ldh_ratio > self.LDH_RATIO_THRESHOLD
        
        # Criterion 3: Pleural fluid LDH > 2/3 * Upper limit normal serum LDH
        ldh_threshold = self.LDH_FRACTION_THRESHOLD * serum_ldh_upper_normal
        criterion_3 = pleural_fluid_ldh > ldh_threshold
        
        return {
            "protein_ratio": criterion_1,
            "ldh_ratio": criterion_2,
            "ldh_absolute": criterion_3
        }
    
    def _get_interpretation(
        self, is_exudate, criteria_results, criteria_met,
        serum_protein, pleural_fluid_protein, serum_ldh, 
        pleural_fluid_ldh, serum_ldh_upper_normal
    ) -> Dict[str, str]:
        """
        Determines the interpretation based on criteria results
        
        Returns:
            Dict with interpretation details
        """
        
        # Calculate ratios and values for detailed reporting
        protein_ratio = pleural_fluid_protein / serum_protein
        ldh_ratio = pleural_fluid_ldh / serum_ldh
        ldh_threshold = (2.0 / 3.0) * serum_ldh_upper_normal
        
        # Build detailed criteria analysis
        criteria_details = []
        if criteria_results["protein_ratio"]:
            criteria_details.append(f"protein ratio {protein_ratio:.2f} > 0.5")
        if criteria_results["ldh_ratio"]:
            criteria_details.append(f"LDH ratio {ldh_ratio:.2f} > 0.6")
        if criteria_results["ldh_absolute"]:
            criteria_details.append(f"pleural LDH {pleural_fluid_ldh:.0f} > {ldh_threshold:.0f} U/L")
        
        if is_exudate:
            criteria_text = ", ".join(criteria_details)
            return {
                "stage": "Exudate",
                "stage_description": "Exudative effusion",
                "interpretation": f"Light's Criteria: {criteria_met} of 3 criteria met. "
                                f"Classification: Exudative effusion. Criteria met: {criteria_text}. "
                                f"This indicates an inflammatory process requiring further diagnostic workup. "
                                f"Common causes include pneumonia, malignancy, tuberculosis, pulmonary embolism, "
                                f"autoimmune conditions, or other inflammatory processes. Recommend thoracentesis "
                                f"for additional pleural fluid analysis including cytology, microbiology, and "
                                f"specific markers as clinically indicated. Light's criteria have 98% sensitivity "
                                f"for identifying exudates, making this a reliable classification for guiding "
                                f"further evaluation and management."
            }
        else:
            return {
                "stage": "Transudate",
                "stage_description": "Transudative effusion",
                "interpretation": f"Light's Criteria: 0 of 3 criteria met. "
                                f"Classification: Transudative effusion. "
                                f"Protein ratio: {protein_ratio:.2f} (≤0.5), "
                                f"LDH ratio: {ldh_ratio:.2f} (≤0.6), "
                                f"pleural LDH: {pleural_fluid_ldh:.0f} U/L (≤{ldh_threshold:.0f} U/L). "
                                f"This suggests a non-inflammatory process, most commonly due to altered "
                                f"hydrostatic or oncotic pressures. Common causes include congestive heart "
                                f"failure, cirrhosis, nephrotic syndrome, or hypoalbuminemia. Treatment should "
                                f"focus on the underlying condition rather than the effusion itself. Consider "
                                f"possibility of 'pseudoexudate' if patient has been on diuretics or clinical "
                                f"presentation suggests heart failure despite exudative criteria."
            }


def calculate_lights_criteria(
    serum_protein: float,
    pleural_fluid_protein: float,
    serum_ldh: float,
    pleural_fluid_ldh: float,
    serum_ldh_upper_normal: Optional[float] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_lights_criteria pattern
    """
    calculator = LightsCriteriaCalculator()
    return calculator.calculate(
        serum_protein, pleural_fluid_protein, serum_ldh, 
        pleural_fluid_ldh, serum_ldh_upper_normal
    )