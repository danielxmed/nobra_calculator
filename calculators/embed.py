"""
Emergency Department-Initiated Buprenorphine for Opioid Use Disorder (EMBED) Calculator

Assesses OUD using DSM-5 criteria, evaluates withdrawal severity with COWS scale,
and determines readiness for ED-initiated buprenorphine treatment.

References:
1. D'Onofrio G, Chawarski MC, O'Connor PG, Pantalon MV, Busch SH, Owens PH, et al. 
   Emergency department-initiated buprenorphine for opioid dependence with continuation 
   in primary care: outcomes during and after intervention. J Gen Intern Med. 
   2017 Jun;32(6):660-666.
2. American Psychiatric Association. Diagnostic and statistical manual of mental 
   disorders (5th ed.). Arlington, VA: American Psychiatric Publishing; 2013.
3. Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). J Psychoactive 
   Drugs. 2003 Apr-Jun;35(2):253-9.
"""

from typing import Dict, Any


class EmbedCalculator:
    """Calculator for Emergency Department-Initiated Buprenorphine (EMBED) Assessment"""
    
    def __init__(self):
        """Initialize calculator"""
        pass
    
    def calculate(self, opioid_larger_amounts: str, unsuccessful_cut_down: str,
                 time_obtaining_using: str, craving_desire: str, failure_obligations: str,
                 continued_despite_problems: str, activities_given_up: str,
                 hazardous_situations: str, physical_psychological_problems: str,
                 tolerance: str, withdrawal: str, cows_score: int,
                 treatment_readiness: str, pregnancy_status: str,
                 buprenorphine_waiver: str) -> Dict[str, Any]:
        """
        Calculates EMBED assessment for ED-initiated buprenorphine candidacy
        
        Args:
            DSM-5 OUD criteria (11 parameters): All yes/no strings
            cows_score (int): Clinical Opiate Withdrawal Scale score (0-48)
            treatment_readiness (str): Patient readiness (ready/not_ready)
            pregnancy_status (str): Pregnancy status (yes/no)
            buprenorphine_waiver (str): Provider waiver status (yes/no)
            
        Returns:
            Dict with assessment result and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(opioid_larger_amounts, unsuccessful_cut_down,
                            time_obtaining_using, craving_desire, failure_obligations,
                            continued_despite_problems, activities_given_up,
                            hazardous_situations, physical_psychological_problems,
                            tolerance, withdrawal, cows_score, treatment_readiness,
                            pregnancy_status, buprenorphine_waiver)
        
        # Calculate DSM-5 OUD criteria count
        dsm5_score = self._calculate_dsm5_score(opioid_larger_amounts, unsuccessful_cut_down,
                                               time_obtaining_using, craving_desire,
                                               failure_obligations, continued_despite_problems,
                                               activities_given_up, hazardous_situations,
                                               physical_psychological_problems, tolerance,
                                               withdrawal)
        
        # Assess candidacy for buprenorphine
        result = self._assess_candidacy(dsm5_score, cows_score, treatment_readiness,
                                      pregnancy_status, buprenorphine_waiver)
        
        # Get interpretation
        interpretation = self._get_interpretation(result, dsm5_score, cows_score)
        
        return {
            "result": result,
            "unit": "recommendation",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, opioid_larger_amounts: str, unsuccessful_cut_down: str,
                        time_obtaining_using: str, craving_desire: str, failure_obligations: str,
                        continued_despite_problems: str, activities_given_up: str,
                        hazardous_situations: str, physical_psychological_problems: str,
                        tolerance: str, withdrawal: str, cows_score: int,
                        treatment_readiness: str, pregnancy_status: str,
                        buprenorphine_waiver: str):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_readiness = ["ready", "not_ready"]
        
        # Validate yes/no parameters
        yes_no_params = [
            ("opioid_larger_amounts", opioid_larger_amounts),
            ("unsuccessful_cut_down", unsuccessful_cut_down),
            ("time_obtaining_using", time_obtaining_using),
            ("craving_desire", craving_desire),
            ("failure_obligations", failure_obligations),
            ("continued_despite_problems", continued_despite_problems),
            ("activities_given_up", activities_given_up),
            ("hazardous_situations", hazardous_situations),
            ("physical_psychological_problems", physical_psychological_problems),
            ("tolerance", tolerance),
            ("withdrawal", withdrawal),
            ("pregnancy_status", pregnancy_status),
            ("buprenorphine_waiver", buprenorphine_waiver)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in valid_yes_no:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate treatment readiness
        if treatment_readiness not in valid_readiness:
            raise ValueError("treatment_readiness must be 'ready' or 'not_ready'")
        
        # Validate COWS score
        if not isinstance(cows_score, int):
            raise ValueError("cows_score must be an integer")
        
        if cows_score < 0 or cows_score > 48:
            raise ValueError("cows_score must be between 0 and 48")
    
    def _calculate_dsm5_score(self, opioid_larger_amounts: str, unsuccessful_cut_down: str,
                             time_obtaining_using: str, craving_desire: str,
                             failure_obligations: str, continued_despite_problems: str,
                             activities_given_up: str, hazardous_situations: str,
                             physical_psychological_problems: str, tolerance: str,
                             withdrawal: str) -> int:
        """
        Calculates DSM-5 OUD criteria score
        
        Returns:
            int: Number of DSM-5 criteria met (0-11)
        """
        
        criteria = [
            opioid_larger_amounts == "yes",
            unsuccessful_cut_down == "yes",
            time_obtaining_using == "yes",
            craving_desire == "yes",
            failure_obligations == "yes",
            continued_despite_problems == "yes",
            activities_given_up == "yes",
            hazardous_situations == "yes",
            physical_psychological_problems == "yes",
            tolerance == "yes",
            withdrawal == "yes"
        ]
        
        return sum(criteria)
    
    def _assess_candidacy(self, dsm5_score: int, cows_score: int, treatment_readiness: str,
                         pregnancy_status: str, buprenorphine_waiver: str) -> str:
        """
        Assesses candidacy for ED-initiated buprenorphine
        
        Args:
            dsm5_score (int): Number of DSM-5 OUD criteria met
            cows_score (int): Clinical Opiate Withdrawal Scale score
            treatment_readiness (str): Patient readiness for treatment
            pregnancy_status (str): Pregnancy status
            buprenorphine_waiver (str): Provider waiver status
            
        Returns:
            str: Assessment result (not_candidate, candidate_home_induction, candidate_ed_induction)
        """
        
        # Must have OUD diagnosis (≥2 DSM-5 criteria)
        if dsm5_score < 2:
            return "not_candidate"
        
        # Must be ready for treatment
        if treatment_readiness != "ready":
            return "not_candidate"
        
        # Provider must have waiver/certification
        if buprenorphine_waiver != "yes":
            return "not_candidate"
        
        # Special consideration for pregnancy (requires specialized care)
        if pregnancy_status == "yes":
            return "not_candidate"  # Requires specialized consultation
        
        # Determine induction approach based on COWS score
        if cows_score > 12:
            return "candidate_ed_induction"
        else:
            return "candidate_home_induction"
    
    def _get_interpretation(self, result: str, dsm5_score: int, cows_score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on assessment result
        
        Args:
            result (str): Assessment result
            dsm5_score (int): DSM-5 criteria score
            cows_score (int): COWS score
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine OUD severity
        if dsm5_score >= 6:
            oud_severity = "Severe"
        elif dsm5_score >= 4:
            oud_severity = "Moderate"
        elif dsm5_score >= 2:
            oud_severity = "Mild"
        else:
            oud_severity = "No OUD"
        
        # Determine withdrawal severity
        if cows_score > 12:
            withdrawal_severity = "Moderate to Severe"
        elif cows_score >= 8:
            withdrawal_severity = "Mild to Moderate"
        else:
            withdrawal_severity = "None to Mild"
        
        if result == "not_candidate":
            return {
                "stage": "Not Candidate",
                "description": "Not candidate for ED-initiated buprenorphine",
                "interpretation": (
                    f"Patient does not meet criteria for ED-initiated buprenorphine treatment. "
                    f"OUD severity: {oud_severity} ({dsm5_score}/11 criteria). "
                    f"Withdrawal severity: {withdrawal_severity} (COWS: {cows_score}). "
                    f"Consider alternative treatment options, referral to addiction medicine, "
                    f"or reassessment when circumstances change."
                )
            }
        
        elif result == "candidate_home_induction":
            return {
                "stage": "Candidate - Home Induction",
                "description": "Candidate for home induction protocol",
                "interpretation": (
                    f"Patient meets criteria for buprenorphine treatment. "
                    f"OUD severity: {oud_severity} ({dsm5_score}/11 criteria). "
                    f"Withdrawal severity: {withdrawal_severity} (COWS: {cows_score}). "
                    f"COWS ≤12 indicates home induction protocol is appropriate. "
                    f"Provide patient education, prescription for home induction, "
                    f"clear instructions, and arrange follow-up care."
                )
            }
        
        else:  # candidate_ed_induction
            return {
                "stage": "Candidate - ED Induction",
                "description": "Candidate for emergency department induction",
                "interpretation": (
                    f"Patient meets all criteria for ED-initiated buprenorphine induction. "
                    f"OUD severity: {oud_severity} ({dsm5_score}/11 criteria). "
                    f"Withdrawal severity: {withdrawal_severity} (COWS: {cows_score}). "
                    f"COWS >12 indicates moderate to severe withdrawal suitable for "
                    f"immediate ED induction. Proceed with ED induction protocol, "
                    f"monitor for precipitated withdrawal, and arrange follow-up care."
                )
            }


def calculate_embed(opioid_larger_amounts: str, unsuccessful_cut_down: str,
                   time_obtaining_using: str, craving_desire: str, failure_obligations: str,
                   continued_despite_problems: str, activities_given_up: str,
                   hazardous_situations: str, physical_psychological_problems: str,
                   tolerance: str, withdrawal: str, cows_score: int,
                   treatment_readiness: str, pregnancy_status: str,
                   buprenorphine_waiver: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_embed pattern
    """
    calculator = EmbedCalculator()
    return calculator.calculate(opioid_larger_amounts, unsuccessful_cut_down,
                               time_obtaining_using, craving_desire, failure_obligations,
                               continued_despite_problems, activities_given_up,
                               hazardous_situations, physical_psychological_problems,
                               tolerance, withdrawal, cows_score, treatment_readiness,
                               pregnancy_status, buprenorphine_waiver)