"""
Edmonton Obesity Staging System (EOSS) Calculator

Stratifies the presence and severity of obesity-related health impairments across medical, 
functional, and psychological domains to guide treatment decisions and predict outcomes.

References:
1. Sharma AM, Kushner RF. A proposed clinical staging system for obesity. Int J Obes (Lond). 
   2009;33(3):289-95. doi: 10.1038/ijo.2009.2.
2. Padwal RS, Pajewski NM, Allison DB, Sharma AM. Using the Edmonton obesity staging system to 
   predict mortality in a population-representative cohort of people with overweight and obesity. 
   CMAJ. 2011;183(14):E1059-66. doi: 10.1503/cmaj.110387.
"""

from typing import Dict, Any


class EdmontonObesityStagingSystemCalculator:
    """Calculator for Edmonton Obesity Staging System (EOSS)"""
    
    def __init__(self):
        # EOSS domain definitions
        self.DOMAINS = {
            'obesity_risk_factors': {
                'name': 'Obesity-Related Medical Risk Factors',
                'stages': {
                    0: 'No risk factors present',
                    1: 'Subclinical risk factors (borderline hypertension, impaired fasting glucose, elevated liver enzymes, arthralgia)',
                    2: 'Established obesity-related chronic disease (hypertension, type 2 diabetes, sleep apnea, osteoarthritis, reflux disease, gallbladder disease, gout)',
                    3: 'End-organ damage (myocardial infarction, heart failure, diabetic complications, osteoarthritis requiring joint replacement, non-alcoholic steatohepatitis)',
                    4: 'Severe, potentially end-stage chronic disease (advanced heart failure, stroke, severe diabetic complications, severe osteoarthritis, cirrhosis)'
                }
            },
            'physical_symptoms': {
                'name': 'Physical Symptoms and Functional Limitations',
                'stages': {
                    0: 'No physical symptoms or functional limitations',
                    1: 'Mild physical symptoms or limitations with activities of daily living',
                    2: 'Moderate physical symptoms or limitations with activities of daily living',
                    3: 'Significant physical symptoms or limitations with activities of daily living',
                    4: 'Severe physical symptoms or limitations with activities of daily living'
                }
            },
            'psychological_symptoms': {
                'name': 'Psychological Symptoms and Mental Health Impact',
                'stages': {
                    0: 'No psychological symptoms or mental health impact',
                    1: 'Mild psychological symptoms or mental health impact',
                    2: 'Moderate psychological symptoms or mental health impact',
                    3: 'Significant psychological symptoms or mental health impact',
                    4: 'Severe psychological symptoms or mental health impact'
                }
            }
        }
        
        # EOSS stage interpretations
        self.STAGE_DEFINITIONS = {
            0: {
                'name': 'Stage 0',
                'description': 'No obesity-related health impairments',
                'severity': 'None',
                'management_focus': 'Prevention and lifestyle counseling'
            },
            1: {
                'name': 'Stage 1',
                'description': 'Mild obesity-related health impairments',
                'severity': 'Mild',
                'management_focus': 'Intensive lifestyle interventions and risk factor monitoring'
            },
            2: {
                'name': 'Stage 2',
                'description': 'Moderate obesity-related health impairments',
                'severity': 'Moderate',
                'management_focus': 'Comprehensive obesity treatment and comorbidity management'
            },
            3: {
                'name': 'Stage 3',
                'description': 'Severe obesity-related health impairments',
                'severity': 'Severe',
                'management_focus': 'Aggressive management and multidisciplinary care'
            },
            4: {
                'name': 'Stage 4',
                'description': 'End-stage obesity-related health impairments',
                'severity': 'End-stage',
                'management_focus': 'Most aggressive interventions and supportive care'
            }
        }
    
    def calculate(self, obesity_risk_factors: int, physical_symptoms: int, 
                  psychological_symptoms: int) -> Dict[str, Any]:
        """
        Calculates the EOSS stage using the provided parameters
        
        Args:
            obesity_risk_factors (int): Stage of obesity-related medical risk factors (0-4)
            physical_symptoms (int): Stage of physical symptoms and functional limitations (0-4)
            psychological_symptoms (int): Stage of psychological symptoms and mental health impact (0-4)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(obesity_risk_factors, physical_symptoms, psychological_symptoms)
        
        # Calculate EOSS stage (highest stage across all domains)
        eoss_stage = self._calculate_eoss_stage(obesity_risk_factors, physical_symptoms, psychological_symptoms)
        
        # Get interpretation
        interpretation = self._get_interpretation(eoss_stage, {
            'obesity_risk_factors': obesity_risk_factors,
            'physical_symptoms': physical_symptoms,
            'psychological_symptoms': psychological_symptoms
        })
        
        return {
            "result": eoss_stage,
            "unit": "stage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, obesity_risk_factors: int, physical_symptoms: int, psychological_symptoms: int):
        """Validates input parameters"""
        
        parameters = {
            'obesity_risk_factors': obesity_risk_factors,
            'physical_symptoms': physical_symptoms,
            'psychological_symptoms': psychological_symptoms
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"Parameter '{param_name}' must be an integer")
            
            if value < 0 or value > 4:
                raise ValueError(f"Parameter '{param_name}' must be between 0 and 4, got {value}")
    
    def _calculate_eoss_stage(self, obesity_risk_factors: int, physical_symptoms: int, 
                             psychological_symptoms: int) -> int:
        """Calculates the EOSS stage using the highest severity rule"""
        
        # EOSS stage is determined by the highest stage across all three domains
        eoss_stage = max(obesity_risk_factors, physical_symptoms, psychological_symptoms)
        
        return eoss_stage
    
    def _get_interpretation(self, eoss_stage: int, domain_scores: Dict[str, int]) -> Dict[str, str]:
        """
        Determines the interpretation based on the EOSS stage
        
        Args:
            eoss_stage (int): Calculated EOSS stage
            domain_scores (Dict): Individual domain scores for context
            
        Returns:
            Dict with interpretation
        """
        
        stage_info = self.STAGE_DEFINITIONS[eoss_stage]
        
        # Base interpretation
        if eoss_stage == 0:
            interpretation_text = (
                "No obesity-related health impairments present. Focus on lifestyle counseling for "
                "healthy eating, regular physical activity, and weight maintenance. Prevention "
                "strategies to avoid future obesity-related complications."
            )
        elif eoss_stage == 1:
            interpretation_text = (
                "Mild obesity-related health impairments. Investigate and monitor subclinical risk "
                "factors. Implement intensive lifestyle interventions including structured dietary "
                "counseling, exercise programs, and behavioral modification. Regular monitoring for "
                "progression of risk factors."
            )
        elif eoss_stage == 2:
            interpretation_text = (
                "Moderate obesity-related health impairments with established chronic disease. "
                "Initiate comprehensive obesity treatment including pharmacotherapy consideration if "
                "appropriate. Actively manage comorbidities and functional limitations. Consider "
                "referral to obesity specialist."
            )
        elif eoss_stage == 3:
            interpretation_text = (
                "Severe obesity-related health impairments with end-organ damage or significant "
                "functional impairment. Aggressive obesity management required including consideration "
                "of bariatric surgery if appropriate. Intensive management of comorbidities and "
                "psychological support. Multidisciplinary care team approach."
            )
        else:  # eoss_stage == 4
            interpretation_text = (
                "End-stage obesity-related health impairments with severe, potentially life-threatening "
                "conditions. Pursue most aggressive management options available including bariatric "
                "surgery evaluation. Palliative care considerations may be appropriate. Comprehensive "
                "support services and end-of-life planning discussions if indicated."
            )
        
        # Add domain-specific context
        domain_context = self._get_domain_context(domain_scores)
        if domain_context:
            interpretation_text += f" Domain assessment: {domain_context}"
        
        return {
            "stage": stage_info["name"],
            "description": stage_info["description"],
            "interpretation": interpretation_text
        }
    
    def _get_domain_context(self, domain_scores: Dict[str, int]) -> str:
        """Provides context about which domains are contributing to the stage"""
        
        domain_contributions = []
        
        for domain_name, score in domain_scores.items():
            if score > 0:
                domain_display_name = self.DOMAINS[domain_name]['name']
                domain_contributions.append(f"{domain_display_name} (Stage {score})")
        
        if domain_contributions:
            return "; ".join(domain_contributions) + "."
        else:
            return "All domains at Stage 0."


def calculate_edmonton_obesity_staging_system(obesity_risk_factors: int, physical_symptoms: int, 
                                            psychological_symptoms: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_edmonton_obesity_staging_system pattern
    """
    calculator = EdmontonObesityStagingSystemCalculator()
    return calculator.calculate(obesity_risk_factors, physical_symptoms, psychological_symptoms)