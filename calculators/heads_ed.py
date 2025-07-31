"""
HEADS-ED Calculator

Screens for pediatric mental health needs in the emergency department.
Evaluates 7 domains to guide clinical decision-making and referral needs.

References:
- Cappelli M, et al. Pediatrics. 2012;130(2):e321-327.
- Cappelli M, et al. Pediatr Emerg Care. 2017;33(5):316-321.
"""

from typing import Dict, Any


class HeadsEdCalculator:
    """Calculator for HEADS-ED pediatric mental health screening tool"""
    
    def calculate(self, home: int, education: int, activities: int, 
                 drugs: int, suicidality: int, emotions: int, 
                 discharge: int) -> Dict[str, Any]:
        """
        Calculates the HEADS-ED score using the provided parameters
        
        Args:
            home (int): Home environment score (0-2)
            education (int): Education/employment score (0-2)
            activities (int): Activities & peers score (0-2)
            drugs (int): Drugs & alcohol score (0-2)
            suicidality (int): Suicidality score (0-2)
            emotions (int): Emotions/behaviors score (0-2)
            discharge (int): Discharge resources score (0-2)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(home, education, activities, drugs, 
                            suicidality, emotions, discharge)
        
        # Calculate total score
        result = home + education + activities + drugs + suicidality + emotions + discharge
        
        # Get interpretation
        interpretation = self._get_interpretation(result, suicidality)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "requires_consultation": interpretation["requires_consultation"],
            "suicidality_score": suicidality
        }
    
    def _validate_inputs(self, home: int, education: int, activities: int,
                        drugs: int, suicidality: int, emotions: int,
                        discharge: int):
        """Validates input parameters"""
        
        parameters = {
            "home": home,
            "education": education,
            "activities": activities,
            "drugs": drugs,
            "suicidality": suicidality,
            "emotions": emotions,
            "discharge": discharge
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name.capitalize()} must be an integer")
            
            if value < 0 or value > 2:
                raise ValueError(f"{param_name.capitalize()} must be between 0 and 2")
    
    def _get_interpretation(self, result: int, suicidality: int) -> Dict[str, Any]:
        """
        Determines the interpretation based on the result and suicidality score
        
        Args:
            result (int): Total HEADS-ED score
            suicidality (int): Suicidality subscore
            
        Returns:
            Dict with interpretation
        """
        
        # Check for high suicidality first (overrides total score)
        if suicidality == 2:
            return {
                "stage": "Immediate Risk",
                "description": "Suicide plan or gesture present",
                "interpretation": "Immediate psychiatric consultation required due to suicidality score of 2. Patient has suicide plan or gesture. Ensure patient safety, initiate appropriate monitoring, and arrange urgent psychiatric evaluation.",
                "requires_consultation": True
            }
        
        # Check total score
        if result >= 8:
            return {
                "stage": "High Risk",
                "description": "Significant mental health needs",
                "interpretation": "Referral for specialized mental health assessment is recommended. Total score ≥8 indicates significant mental health concerns requiring psychiatric consultation. Consider appropriate level of care based on clinical presentation and ensure adequate support resources are in place.",
                "requires_consultation": True
            }
        else:
            # Low risk but check if suicidality = 1
            if suicidality == 1:
                return {
                    "stage": "Moderate Risk",
                    "description": "Suicidal ideation present",
                    "interpretation": "Although total score is <8, presence of suicidal ideation requires careful assessment. Consider psychiatric consultation based on clinical judgment. Ensure safety planning and appropriate follow-up are arranged.",
                    "requires_consultation": False
                }
            else:
                return {
                    "stage": "Low Risk",
                    "description": "Low mental health needs",
                    "interpretation": "Consider community resources and routine follow-up. No immediate psychiatric consultation needed unless other concerning factors present. Provide education about available mental health resources and ensure appropriate outpatient follow-up is arranged.",
                    "requires_consultation": False
                }


def calculate_heads_ed(home: int, education: int, activities: int,
                      drugs: int, suicidality: int, emotions: int,
                      discharge: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_heads_ed pattern
    """
    calculator = HeadsEdCalculator()
    return calculator.calculate(home, education, activities, drugs,
                              suicidality, emotions, discharge)