"""
VIRSTA Score for Infective Endocarditis Risk Assessment Calculator

Clinical decision tool for risk-stratifying suspected infective endocarditis cases.

References:
1. Sunnerhagen T, Törnell A, Vikbrant M, et al. VIRSTA score: prediction of infective 
   endocarditis and mortality in Staphylococcus aureus bacteremia; a cohort study. 
   Clin Microbiol Infect. 2019;25(4):480-486. doi: 10.1016/j.cmi.2018.06.021
2. Palraj BR, Baddour LM, Hess EP, et al. Predicting risk of endocarditis using a 
   clinical tool (PREDICT): scoring system to guide use of echocardiography in the 
   setting of Staphylococcus aureus bacteremia. Clin Infect Dis. 2015;61(1):18-28.
"""

from typing import Dict, Any


class VirstaScoreCalculator:
    """Calculator for VIRSTA Score for Infective Endocarditis Risk Assessment"""
    
    def __init__(self):
        # VIRSTA Score criteria and their point values
        self.CRITERIA_POINTS = {
            "valve_disease_or_prosthetic_valve": 5,
            "injection_drug_use": 5,
            "vascular_phenomena": 4,
            "immunologic_phenomena": 3,
            "systemic_emboli": 3,
            "temperature_over_38c": 2,
            "age_over_60": 2,
            "wbc_over_11000": 1,
            "central_venous_catheter": 1,
            "staph_aureus_bacteremia": 1
        }
    
    def calculate(self, valve_disease_or_prosthetic_valve: str, injection_drug_use: str,
                 vascular_phenomena: str, immunologic_phenomena: str, systemic_emboli: str,
                 temperature_over_38c: str, age_over_60: str, wbc_over_11000: str,
                 central_venous_catheter: str, staph_aureus_bacteremia: str) -> Dict[str, Any]:
        """
        Calculates the VIRSTA Score for infective endocarditis risk assessment
        
        Args:
            valve_disease_or_prosthetic_valve (str): Known valve disease or prosthetic valve ("yes"/"no")
            injection_drug_use (str): History of injection drug use ("yes"/"no")
            vascular_phenomena (str): Presence of vascular phenomena ("yes"/"no")
            immunologic_phenomena (str): Presence of immunologic phenomena ("yes"/"no")
            systemic_emboli (str): Evidence of systemic arterial emboli ("yes"/"no")
            temperature_over_38c (str): Fever >38°C ("yes"/"no")
            age_over_60 (str): Age >60 years ("yes"/"no")
            wbc_over_11000 (str): WBC >11,000/μL ("yes"/"no")
            central_venous_catheter (str): Presence of central venous catheter ("yes"/"no")
            staph_aureus_bacteremia (str): Staphylococcus aureus bacteremia ("yes"/"no")
            
        Returns:
            Dict with the VIRSTA score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            valve_disease_or_prosthetic_valve, injection_drug_use, vascular_phenomena,
            immunologic_phenomena, systemic_emboli, temperature_over_38c, age_over_60,
            wbc_over_11000, central_venous_catheter, staph_aureus_bacteremia
        )
        
        # Calculate score
        parameters = {
            "valve_disease_or_prosthetic_valve": valve_disease_or_prosthetic_valve,
            "injection_drug_use": injection_drug_use,
            "vascular_phenomena": vascular_phenomena,
            "immunologic_phenomena": immunologic_phenomena,
            "systemic_emboli": systemic_emboli,
            "temperature_over_38c": temperature_over_38c,
            "age_over_60": age_over_60,
            "wbc_over_11000": wbc_over_11000,
            "central_venous_catheter": central_venous_catheter,
            "staph_aureus_bacteremia": staph_aureus_bacteremia
        }
        
        total_score = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Generate component breakdown
        component_breakdown = self._generate_component_breakdown(parameters, total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"],
            "component_breakdown": component_breakdown
        }
    
    def _validate_inputs(self, *args):
        """Validates all input parameters"""
        
        valid_responses = ["yes", "no"]
        
        for i, arg in enumerate(args):
            if not isinstance(arg, str):
                raise ValueError(f"Parameter {i+1} must be a string")
            
            if arg.lower() not in valid_responses:
                raise ValueError(f"Parameter {i+1} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, parameters: Dict[str, str]) -> int:
        """
        Calculates the total VIRSTA score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            
        Returns:
            int: Total VIRSTA score
        """
        
        total_score = 0
        
        for parameter, value in parameters.items():
            if value.lower() == "yes":
                total_score += self.CRITERIA_POINTS[parameter]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the VIRSTA score
        
        Args:
            score (int): Calculated VIRSTA score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 1:
            return {
                "stage": "Very Low Risk",
                "stage_description": "Very low probability of infective endocarditis",
                "interpretation": f"VIRSTA score of {score} indicates very low risk for infective endocarditis "
                               f"(negative predictive value >99%). Echocardiography may be deferred in these patients "
                               f"unless clinical suspicion remains high based on other factors. Consider alternative "
                               f"diagnoses and outpatient management with close follow-up. The very low score suggests "
                               f"that resources may be better allocated to other diagnostic considerations."
            }
        else:
            return {
                "stage": "Higher Risk",
                "stage_description": "Increased probability of infective endocarditis",
                "interpretation": f"VIRSTA score of {score} indicates increased risk for infective endocarditis. "
                               f"Echocardiography is recommended for further evaluation. Consider transesophageal "
                               f"echocardiography if transthoracic echocardiography is negative and clinical suspicion "
                               f"remains high. Initiate appropriate antimicrobial therapy based on blood culture results "
                               f"and monitor closely for complications including embolic events, heart failure, and "
                               f"abscess formation."
            }
    
    def _generate_component_breakdown(self, parameters: Dict[str, str], total_score: int) -> Dict[str, Any]:
        """
        Generates detailed component breakdown of the VIRSTA score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            total_score (int): Total calculated score
            
        Returns:
            Dict with component breakdown
        """
        
        component_scores = {}
        positive_criteria = []
        
        for parameter, value in parameters.items():
            points = self.CRITERIA_POINTS[parameter] if value.lower() == "yes" else 0
            component_scores[parameter] = {
                "present": value.lower() == "yes",
                "points": points
            }
            
            if value.lower() == "yes":
                positive_criteria.append({
                    "criterion": parameter.replace("_", " ").title(),
                    "points": self.CRITERIA_POINTS[parameter]
                })
        
        return {
            "total_score": total_score,
            "positive_criteria_count": len(positive_criteria),
            "positive_criteria": positive_criteria,
            "component_scores": component_scores,
            "high_value_criteria": [
                criteria for criteria in positive_criteria 
                if criteria["points"] >= 4
            ],
            "scoring_notes": [
                "Score ≤1 has negative predictive value >99% for ruling out infective endocarditis",
                "Originally developed and validated in Staphylococcus aureus bacteremia patients",
                "Should be used in conjunction with clinical judgment"
            ]
        }


def calculate_virsta_score(valve_disease_or_prosthetic_valve, injection_drug_use,
                          vascular_phenomena, immunologic_phenomena, systemic_emboli,
                          temperature_over_38c, age_over_60, wbc_over_11000,
                          central_venous_catheter, staph_aureus_bacteremia) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_virsta_score pattern
    """
    calculator = VirstaScoreCalculator()
    return calculator.calculate(
        valve_disease_or_prosthetic_valve, injection_drug_use, vascular_phenomena,
        immunologic_phenomena, systemic_emboli, temperature_over_38c, age_over_60,
        wbc_over_11000, central_venous_catheter, staph_aureus_bacteremia
    )