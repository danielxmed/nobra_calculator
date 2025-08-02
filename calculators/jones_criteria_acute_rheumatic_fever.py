"""
Jones Criteria for Acute Rheumatic Fever Diagnosis

Diagnoses acute rheumatic fever based on major and minor criteria with evidence of 
antecedent group A streptococcal infection. The revised 2015 criteria account for 
population risk stratification and require either 2 major criteria OR 1 major and 
2 minor criteria, plus evidence of streptococcal infection.

References:
1. Gewitz MH, Baltimore RS, Tani LY, Sable CA, Shulman ST, Carapetis J, et al. Revision of the Jones Criteria for the diagnosis of acute rheumatic fever in the era of Doppler echocardiography: a scientific statement from the American Heart Association. Circulation. 2015;131(20):1806-18.
2. WHO Expert Consultation on Rheumatic Fever and Rheumatic Heart Disease. WHO technical report series; no. 923. Geneva: World Health Organization; 2004.
3. Carapetis JR, Beaton A, Cunningham MW, Guilherme L, Karthikeyan G, Mayosi BM, et al. Acute rheumatic fever and rheumatic heart disease. Nat Rev Dis Primers. 2016;2:15084.
"""

from typing import Dict, Any


class JonesCriteriaAcuteRheumaticFeverCalculator:
    """Calculator for Jones Criteria for Acute Rheumatic Fever Diagnosis"""
    
    def __init__(self):
        # Major criteria (same for both risk populations)
        self.MAJOR_CRITERIA = [
            "carditis",
            "arthritis", 
            "chorea",
            "erythema_marginatum",
            "subcutaneous_nodules"
        ]
        
        # Minor criteria (differ by population risk)
        self.MINOR_CRITERIA_LOW_RISK = [
            "fever",
            "arthralgia",  # Only for low-risk populations
            "elevated_acute_phase_reactants",
            "prolonged_pr_interval",
            "previous_rf_rhd"
        ]
        
        self.MINOR_CRITERIA_MODERATE_HIGH_RISK = [
            "fever",
            # arthralgia is NOT a minor criterion for moderate-high risk
            "elevated_acute_phase_reactants", 
            "prolonged_pr_interval",
            "previous_rf_rhd"
        ]
    
    def calculate(self, population_risk: str, strep_evidence: str, carditis: str, 
                 arthritis: str, chorea: str, erythema_marginatum: str, 
                 subcutaneous_nodules: str, fever: str, arthralgia: str,
                 elevated_acute_phase_reactants: str, prolonged_pr_interval: str,
                 previous_rf_rhd: str) -> Dict[str, Any]:
        """
        Determines acute rheumatic fever diagnosis using Jones criteria
        
        Args:
            population_risk (str): Risk category ('low_risk' or 'moderate_high_risk')
            strep_evidence (str): Evidence of antecedent strep infection ('yes' or 'no')
            carditis (str): Carditis present ('yes' or 'no')
            arthritis (str): Type of arthritis ('polyarthritis', 'monoarthritis_polyarthralgia', 'none')
            chorea (str): Chorea present ('yes' or 'no')
            erythema_marginatum (str): Erythema marginatum present ('yes' or 'no')
            subcutaneous_nodules (str): Subcutaneous nodules present ('yes' or 'no')
            fever (str): Fever present ('yes' or 'no')
            arthralgia (str): Arthralgia present ('yes' or 'no')
            elevated_acute_phase_reactants (str): Elevated ESR/CRP ('yes' or 'no')
            prolonged_pr_interval (str): Prolonged PR interval ('yes' or 'no')
            previous_rf_rhd (str): Previous RF/RHD ('yes' or 'no')
            
        Returns:
            Dict with the diagnosis and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(population_risk, strep_evidence, carditis, arthritis, chorea,
                             erythema_marginatum, subcutaneous_nodules, fever, arthralgia,
                             elevated_acute_phase_reactants, prolonged_pr_interval, previous_rf_rhd)
        
        # Check for streptococcal evidence first
        if strep_evidence == "no":
            diagnosis = self._get_no_strep_diagnosis()
        else:
            # Count major and minor criteria
            major_count = self._count_major_criteria(carditis, arthritis, chorea, 
                                                   erythema_marginatum, subcutaneous_nodules,
                                                   population_risk)
            minor_count = self._count_minor_criteria(fever, arthralgia, elevated_acute_phase_reactants,
                                                   prolonged_pr_interval, previous_rf_rhd, 
                                                   population_risk, carditis)
            
            # Apply Jones criteria logic
            diagnosis = self._determine_diagnosis(major_count, minor_count)
        
        return {
            "result": diagnosis["diagnosis"],
            "unit": "criteria",
            "interpretation": diagnosis["interpretation"],
            "stage": diagnosis["stage"],
            "stage_description": diagnosis["description"]
        }
    
    def _validate_inputs(self, population_risk, strep_evidence, carditis, arthritis, chorea,
                        erythema_marginatum, subcutaneous_nodules, fever, arthralgia,
                        elevated_acute_phase_reactants, prolonged_pr_interval, previous_rf_rhd):
        """Validates input parameters"""
        
        if population_risk not in ["low_risk", "moderate_high_risk"]:
            raise ValueError("population_risk must be 'low_risk' or 'moderate_high_risk'")
        
        yes_no_params = [strep_evidence, carditis, chorea, erythema_marginatum, 
                        subcutaneous_nodules, fever, arthralgia, elevated_acute_phase_reactants,
                        prolonged_pr_interval, previous_rf_rhd]
        
        for param in yes_no_params:
            if param not in ["yes", "no"]:
                raise ValueError("All yes/no parameters must be 'yes' or 'no'")
        
        if arthritis not in ["polyarthritis", "monoarthritis_polyarthralgia", "none"]:
            raise ValueError("arthritis must be 'polyarthritis', 'monoarthritis_polyarthralgia', or 'none'")
    
    def _count_major_criteria(self, carditis, arthritis, chorea, erythema_marginatum, 
                             subcutaneous_nodules, population_risk):
        """Counts major criteria present"""
        
        major_count = 0
        
        # Carditis
        if carditis == "yes":
            major_count += 1
        
        # Arthritis - depends on population risk
        if population_risk == "low_risk":
            # Only polyarthritis counts as major for low-risk
            if arthritis == "polyarthritis":
                major_count += 1
        else:  # moderate_high_risk
            # Both polyarthritis and monoarthritis/polyarthralgia count as major
            if arthritis in ["polyarthritis", "monoarthritis_polyarthralgia"]:
                major_count += 1
        
        # Other major criteria
        if chorea == "yes":
            major_count += 1
        if erythema_marginatum == "yes":
            major_count += 1
        if subcutaneous_nodules == "yes":
            major_count += 1
        
        return major_count
    
    def _count_minor_criteria(self, fever, arthralgia, elevated_acute_phase_reactants,
                             prolonged_pr_interval, previous_rf_rhd, population_risk, carditis):
        """Counts minor criteria present"""
        
        minor_count = 0
        
        # Fever
        if fever == "yes":
            minor_count += 1
        
        # Arthralgia - only for low-risk populations
        if population_risk == "low_risk" and arthralgia == "yes":
            minor_count += 1
        
        # Elevated acute phase reactants
        if elevated_acute_phase_reactants == "yes":
            minor_count += 1
        
        # Prolonged PR interval (unless carditis is major criterion)
        if prolonged_pr_interval == "yes" and carditis == "no":
            minor_count += 1
        
        # Previous RF/RHD
        if previous_rf_rhd == "yes":
            minor_count += 1
        
        return minor_count
    
    def _determine_diagnosis(self, major_count, minor_count):
        """Determines diagnosis based on criteria counts"""
        
        # Jones criteria: 2 major OR 1 major + 2 minor
        if major_count >= 2 or (major_count >= 1 and minor_count >= 2):
            return {
                "diagnosis": "Acute Rheumatic Fever Diagnosed",
                "stage": "Diagnosed",
                "description": "Meets Jones criteria for acute rheumatic fever",
                "interpretation": f"Patient meets the revised 2015 Jones criteria for acute rheumatic fever diagnosis with {major_count} major criteria and {minor_count} minor criteria. Requires evidence of streptococcal infection plus either 2 major criteria OR 1 major + 2 minor criteria. Immediate treatment with anti-inflammatory therapy and penicillin prophylaxis is recommended. Consider echocardiography for all patients."
            }
        else:
            return {
                "diagnosis": "Jones Criteria Not Met", 
                "stage": "Not Diagnosed",
                "description": "Does not meet criteria for acute rheumatic fever",
                "interpretation": f"Patient does not meet the revised 2015 Jones criteria for acute rheumatic fever with {major_count} major criteria and {minor_count} minor criteria. Consider alternative diagnoses such as post-infectious arthritis, viral myocarditis, or other inflammatory conditions. Monitor for development of additional criteria over time."
            }
    
    def _get_no_strep_diagnosis(self):
        """Returns diagnosis when no streptococcal evidence"""
        
        return {
            "diagnosis": "Insufficient Evidence - No Strep Infection",
            "stage": "Insufficient Evidence", 
            "description": "No evidence of antecedent streptococcal infection",
            "interpretation": "Jones criteria require evidence of antecedent group A streptococcal infection for diagnosis of acute rheumatic fever. Consider testing for streptococcal antibodies (ASO, anti-DNase B), throat culture, or history of recent streptococcal infection. Special consideration may be given for isolated chorea or insidious carditis even without meeting standard criteria."
        }


def calculate_jones_criteria_acute_rheumatic_fever(population_risk: str, strep_evidence: str, 
                                                  carditis: str, arthritis: str, chorea: str, 
                                                  erythema_marginatum: str, subcutaneous_nodules: str,
                                                  fever: str, arthralgia: str, 
                                                  elevated_acute_phase_reactants: str,
                                                  prolonged_pr_interval: str, 
                                                  previous_rf_rhd: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_jones_criteria_acute_rheumatic_fever pattern
    """
    calculator = JonesCriteriaAcuteRheumaticFeverCalculator()
    return calculator.calculate(population_risk, strep_evidence, carditis, arthritis, chorea,
                               erythema_marginatum, subcutaneous_nodules, fever, arthralgia,
                               elevated_acute_phase_reactants, prolonged_pr_interval, previous_rf_rhd)