"""
Indications for Paxlovid Calculator

Aids in determining if Paxlovid (nirmatrelvir boosted with ritonavir) is appropriate 
therapy in an adult COVID-19 positive patient. Evaluates eligibility based on FDA 
guidelines including age, weight, symptom duration, disease severity, kidney function, 
high-risk conditions, and potential contraindications.

References (Vancouver style):
1. U.S. Food and Drug Administration. Fact Sheet for Healthcare Providers: Emergency 
   Use Authorization for Paxlovid. Updated May 2023.
2. Hammond J, Leister-Tebbe H, Gardner A, et al. Oral nirmatrelvir for high-risk, 
   nonhospitalized adults with Covid-19. N Engl J Med. 2022;386(15):1397-1408. 
   doi: 10.1056/NEJMoa2118542.
3. Centers for Disease Control and Prevention. Clinical Care Guidance: Oral Antiviral 
   Treatment for COVID-19. Updated 2023.
4. NIH COVID-19 Treatment Guidelines Panel. Ritonavir-Boosted Nirmatrelvir (Paxlovid). 
   Updated 2023.
"""

from typing import Dict, Any


class IndicationsForPaxlovidCalculator:
    """Calculator for Paxlovid eligibility determination"""
    
    def __init__(self):
        # Basic eligibility criteria (all must be met)
        self.basic_criteria = [
            "age_over_12",
            "weight_over_40kg", 
            "mild_moderate_covid",
            "symptom_onset_5_days",
            "egfr_over_30",
            "no_severe_hepatic_impairment"
        ]
        
        # High-risk conditions (at least one must be present)
        self.high_risk_factors = [
            "age_over_50",
            "diabetes",
            "heart_disease",
            "lung_disease",
            "obesity",
            "immunocompromised",
            "pregnancy",
            "unvaccinated_or_not_current",
            "other_high_risk_condition"
        ]
        
        # Contraindications
        self.contraindications = [
            "significant_drug_interactions"
        ]
    
    def calculate(self, age_over_12: str, weight_over_40kg: str, mild_moderate_covid: str,
                 symptom_onset_5_days: str, egfr_over_30: str, no_severe_hepatic_impairment: str,
                 age_over_50: str, diabetes: str, heart_disease: str, lung_disease: str,
                 obesity: str, immunocompromised: str, pregnancy: str, 
                 unvaccinated_or_not_current: str, other_high_risk_condition: str,
                 significant_drug_interactions: str) -> Dict[str, Any]:
        """
        Calculates Paxlovid eligibility and dosing recommendation
        
        Args:
            age_over_12 (str): Patient age >12 years
            weight_over_40kg (str): Patient weight >40 kg (88 lbs)
            mild_moderate_covid (str): Mild to moderate COVID-19 severity
            symptom_onset_5_days (str): Symptom onset ≤5 days
            egfr_over_30 (str): eGFR >30 mL/min/1.73m²
            no_severe_hepatic_impairment (str): No severe hepatic impairment
            age_over_50 (str): Age >50 years
            diabetes (str): Diabetes mellitus
            heart_disease (str): Cardiovascular disease
            lung_disease (str): Chronic lung disease
            obesity (str): Obesity (BMI ≥30)
            immunocompromised (str): Immunocompromised state
            pregnancy (str): Current pregnancy
            unvaccinated_or_not_current (str): Unvaccinated/not up to date
            other_high_risk_condition (str): Other CDC high-risk conditions
            significant_drug_interactions (str): Significant drug interactions
            
        Returns:
            Dict with the recommendation and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_over_12, weight_over_40kg, mild_moderate_covid, symptom_onset_5_days,
            egfr_over_30, no_severe_hepatic_impairment, age_over_50, diabetes,
            heart_disease, lung_disease, obesity, immunocompromised, pregnancy,
            unvaccinated_or_not_current, other_high_risk_condition, significant_drug_interactions
        )
        
        # Collect parameters
        parameters = {
            "age_over_12": age_over_12,
            "weight_over_40kg": weight_over_40kg,
            "mild_moderate_covid": mild_moderate_covid,
            "symptom_onset_5_days": symptom_onset_5_days,
            "egfr_over_30": egfr_over_30,
            "no_severe_hepatic_impairment": no_severe_hepatic_impairment,
            "age_over_50": age_over_50,
            "diabetes": diabetes,
            "heart_disease": heart_disease,
            "lung_disease": lung_disease,
            "obesity": obesity,
            "immunocompromised": immunocompromised,
            "pregnancy": pregnancy,
            "unvaccinated_or_not_current": unvaccinated_or_not_current,
            "other_high_risk_condition": other_high_risk_condition,
            "significant_drug_interactions": significant_drug_interactions
        }
        
        # Calculate eligibility
        recommendation = self._calculate_eligibility(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(recommendation)
        
        return {
            "result": recommendation["recommendation"],
            "unit": "recommendation",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        # All parameters should be "no" or "yes"
        valid_options = ["no", "yes"]
        parameter_names = [
            "age_over_12", "weight_over_40kg", "mild_moderate_covid", "symptom_onset_5_days",
            "egfr_over_30", "no_severe_hepatic_impairment", "age_over_50", "diabetes",
            "heart_disease", "lung_disease", "obesity", "immunocompromised", "pregnancy",
            "unvaccinated_or_not_current", "other_high_risk_condition", "significant_drug_interactions"
        ]
        
        for i, value in enumerate(args):
            if value not in valid_options:
                raise ValueError(f"{parameter_names[i]} must be 'no' or 'yes'")
    
    def _calculate_eligibility(self, parameters: Dict[str, str]) -> Dict[str, Any]:
        """
        Calculates Paxlovid eligibility based on FDA criteria
        
        Eligibility Algorithm:
        1. Check basic criteria (all must be met)
        2. Check for contraindications
        3. Check for high-risk factors (at least one required)
        4. Determine dosing based on renal function
        """
        
        # Check basic criteria
        basic_criteria_met = all(parameters[criterion] == "yes" for criterion in self.basic_criteria)
        
        if not basic_criteria_met:
            # Identify which basic criteria failed
            failed_criteria = [criterion for criterion in self.basic_criteria if parameters[criterion] == "no"]
            return {
                "recommendation": "Not Indicated",
                "reason": f"Failed basic criteria: {', '.join(failed_criteria)}",
                "code": 0
            }
        
        # Check for contraindications
        has_contraindications = any(parameters[contraindication] == "yes" for contraindication in self.contraindications)
        
        if has_contraindications:
            return {
                "recommendation": "Contraindicated",
                "reason": "Significant drug interactions present",
                "code": 1
            }
        
        # Check for high-risk factors
        has_high_risk = any(parameters[risk_factor] == "yes" for risk_factor in self.high_risk_factors)
        
        if not has_high_risk:
            return {
                "recommendation": "Not Indicated", 
                "reason": "No high-risk factors present",
                "code": 0
            }
        
        # Patient is eligible - determine dosing based on renal function
        # Note: We infer renal function from the egfr_over_30 parameter
        # In a real implementation, you might want separate eGFR ranges
        
        # For this implementation, we'll assume:
        # - If eGFR >30, we check if it's likely >60 (standard dose) vs 30-60 (reduced dose)
        # - Since we only have egfr_over_30, we'll default to standard dose
        # - In practice, you'd want separate parameters for eGFR ranges
        
        return {
            "recommendation": "Standard Dose",
            "reason": "Eligible for Paxlovid therapy",
            "code": 2
        }
    
    def _get_interpretation(self, recommendation: Dict[str, Any]) -> Dict[str, str]:
        """
        Provides clinical interpretation based on eligibility assessment
        
        Args:
            recommendation (Dict): Recommendation result with code
            
        Returns:
            Dict with interpretation details
        """
        
        code = recommendation["code"]
        
        if code == 0:  # Not Indicated
            return {
                "stage": "Not Indicated",
                "description": "Paxlovid not recommended",
                "interpretation": "Patient does not meet eligibility criteria for Paxlovid therapy. Consider alternative treatments or supportive care as appropriate."
            }
        elif code == 1:  # Contraindicated
            return {
                "stage": "Contraindicated", 
                "description": "Paxlovid contraindicated",
                "interpretation": "Paxlovid is contraindicated due to significant drug interactions, severe renal impairment, or other safety concerns. Do not prescribe."
            }
        elif code == 2:  # Standard Dose
            return {
                "stage": "Standard Dose",
                "description": "Paxlovid indicated - standard dose",
                "interpretation": "Patient eligible for Paxlovid. Prescribe standard dose: nirmatrelvir 300mg + ritonavir 100mg twice daily for 5 days. Start within 5 days of symptom onset."
            }
        elif code == 3:  # Reduced Dose
            return {
                "stage": "Reduced Dose",
                "description": "Paxlovid indicated - reduced dose", 
                "interpretation": "Patient eligible for Paxlovid with dose adjustment for moderate renal impairment (eGFR 30-60). Prescribe reduced dose: nirmatrelvir 150mg + ritonavir 100mg twice daily for 5 days."
            }
        else:
            return {
                "stage": "Error",
                "description": "Unknown recommendation code",
                "interpretation": "Unable to determine recommendation. Please review criteria and try again."
            }


def calculate_indications_for_paxlovid(age_over_12: str, weight_over_40kg: str, 
                                     mild_moderate_covid: str, symptom_onset_5_days: str,
                                     egfr_over_30: str, no_severe_hepatic_impairment: str,
                                     age_over_50: str, diabetes: str, heart_disease: str,
                                     lung_disease: str, obesity: str, immunocompromised: str,
                                     pregnancy: str, unvaccinated_or_not_current: str,
                                     other_high_risk_condition: str, 
                                     significant_drug_interactions: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = IndicationsForPaxlovidCalculator()
    return calculator.calculate(
        age_over_12, weight_over_40kg, mild_moderate_covid, symptom_onset_5_days,
        egfr_over_30, no_severe_hepatic_impairment, age_over_50, diabetes,
        heart_disease, lung_disease, obesity, immunocompromised, pregnancy,
        unvaccinated_or_not_current, other_high_risk_condition, significant_drug_interactions
    )