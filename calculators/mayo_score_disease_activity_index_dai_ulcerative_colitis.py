"""
Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis Calculator

Assesses severity of ulcerative colitis using four clinical and endoscopic parameters.
Originally developed in 1987 to standardize assessment of ulcerative colitis activity 
and treatment response in clinical trials and practice.

References (Vancouver style):
1. Schroeder KW, Tremaine WJ, Ilstrup DM. Coated oral 5-aminosalicylic acid therapy 
   for mildly to moderately active ulcerative colitis. A randomized study. N Engl J Med. 
   1987 Dec 24;317(26):1625-9. doi: 10.1056/NEJM198712243172603.
2. D'Haens G, Sandborn WJ, Feagan BG, Geboes K, Hanauer SB, Irvine EJ, et al. 
   A review of activity indices and efficacy end points for clinical trials of medical 
   therapy in adults with ulcerative colitis. Gastroenterology. 2007 Feb;132(2):763-86. 
   doi: 10.1053/j.gastro.2006.12.038.
"""

from typing import Dict, Any


class MayoScoreDiseaseActivityIndexDaiUlcerativeColitisCalculator:
    """Calculator for Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis"""
    
    def __init__(self):
        # Scoring system for each parameter (0-3 points each)
        self.STOOL_FREQUENCY_SCORES = {
            "normal": 0,
            "1_2_more_than_normal": 1,
            "3_4_more_than_normal": 2,
            "more_than_4_more_than_normal": 3
        }
        
        self.RECTAL_BLEEDING_SCORES = {
            "none": 0,
            "visible_blood_less_than_half_time": 1,
            "visible_blood_half_time_or_more": 2,
            "passing_blood_alone": 3
        }
        
        self.MUCOSAL_APPEARANCE_SCORES = {
            "normal_inactive": 0,
            "mild_disease": 1,
            "moderate_disease": 2,
            "severe_disease": 3
        }
        
        self.PHYSICIAN_GLOBAL_ASSESSMENT_SCORES = {
            "normal": 0,
            "mild": 1,
            "moderate": 2,
            "severe": 3
        }
    
    def calculate(self, stool_frequency: str, rectal_bleeding: str, 
                 mucosal_appearance: str, physician_global_assessment: str) -> Dict[str, Any]:
        """
        Calculates the Mayo DAI score using the provided parameters
        
        Args:
            stool_frequency (str): Increase in stool frequency compared to normal
            rectal_bleeding (str): Presence and severity of rectal bleeding
            mucosal_appearance (str): Endoscopic findings of mucosal inflammation
            physician_global_assessment (str): Physician's overall clinical assessment
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(stool_frequency, rectal_bleeding, mucosal_appearance, physician_global_assessment)
        
        # Calculate individual component scores
        scores = self._calculate_component_scores(
            stool_frequency, rectal_bleeding, mucosal_appearance, physician_global_assessment
        )
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": scores
        }
    
    def _validate_inputs(self, stool_frequency: str, rectal_bleeding: str, 
                        mucosal_appearance: str, physician_global_assessment: str):
        """Validates input parameters"""
        
        if stool_frequency not in self.STOOL_FREQUENCY_SCORES:
            valid_options = list(self.STOOL_FREQUENCY_SCORES.keys())
            raise ValueError(f"Invalid stool_frequency. Must be one of: {valid_options}")
        
        if rectal_bleeding not in self.RECTAL_BLEEDING_SCORES:
            valid_options = list(self.RECTAL_BLEEDING_SCORES.keys())
            raise ValueError(f"Invalid rectal_bleeding. Must be one of: {valid_options}")
        
        if mucosal_appearance not in self.MUCOSAL_APPEARANCE_SCORES:
            valid_options = list(self.MUCOSAL_APPEARANCE_SCORES.keys())
            raise ValueError(f"Invalid mucosal_appearance. Must be one of: {valid_options}")
        
        if physician_global_assessment not in self.PHYSICIAN_GLOBAL_ASSESSMENT_SCORES:
            valid_options = list(self.PHYSICIAN_GLOBAL_ASSESSMENT_SCORES.keys())
            raise ValueError(f"Invalid physician_global_assessment. Must be one of: {valid_options}")
    
    def _calculate_component_scores(self, stool_frequency: str, rectal_bleeding: str,
                                  mucosal_appearance: str, physician_global_assessment: str) -> Dict[str, int]:
        """Calculates individual component scores"""
        
        return {
            "stool_frequency": self.STOOL_FREQUENCY_SCORES[stool_frequency],
            "rectal_bleeding": self.RECTAL_BLEEDING_SCORES[rectal_bleeding],
            "mucosal_appearance": self.MUCOSAL_APPEARANCE_SCORES[mucosal_appearance],
            "physician_global_assessment": self.PHYSICIAN_GLOBAL_ASSESSMENT_SCORES[physician_global_assessment]
        }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Mayo DAI total score (0-12)
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= 2:
            return {
                "stage": "Remission",
                "description": "Disease remission",
                "interpretation": "Mayo DAI score 0-2 indicates clinical remission of ulcerative colitis. "
                               "Patients in remission have minimal or no symptoms, absent or minimal bleeding, "
                               "normal or near-normal endoscopic appearance, and overall clinical well-being. "
                               "This represents the therapeutic goal for most patients and suggests effective "
                               "disease control with current treatment regimen."
            }
        elif 3 <= total_score <= 5:
            return {
                "stage": "Mild Disease",
                "description": "Mildly active disease",
                "interpretation": "Mayo DAI score 3-5 indicates mildly active ulcerative colitis. "
                               "Patients have mild symptoms with some increase in stool frequency, "
                               "intermittent bleeding, mild endoscopic changes with erythema and decreased "
                               "vascular pattern. Treatment adjustment may be considered to achieve remission, "
                               "with focus on optimizing current therapy or adding topical treatments."
            }
        elif 6 <= total_score <= 10:
            return {
                "stage": "Moderate Disease",
                "description": "Moderately active disease",
                "interpretation": "Mayo DAI score 6-10 indicates moderately active ulcerative colitis. "
                               "Patients experience moderate symptoms with increased stool frequency, "
                               "regular bleeding, moderate endoscopic inflammation with marked erythema "
                               "and absent vascular pattern. Requires more intensive treatment including "
                               "systemic immunosuppression, biologics, or hospitalization for severe cases."
            }
        else:  # 11-12
            return {
                "stage": "Severe Disease",
                "description": "Severely active disease",
                "interpretation": "Mayo DAI score 11-12 indicates severely active ulcerative colitis. "
                               "Patients have severe symptoms with frequent bloody stools, severe endoscopic "
                               "findings with spontaneous bleeding and ulceration. Requires immediate aggressive "
                               "treatment, hospitalization, intravenous corticosteroids, rescue therapy with "
                               "infliximab or cyclosporine, and consideration for colectomy if medical therapy fails."
            }


def calculate_mayo_score_disease_activity_index_dai_ulcerative_colitis(
    stool_frequency: str, rectal_bleeding: str, mucosal_appearance: str, 
    physician_global_assessment: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MayoScoreDiseaseActivityIndexDaiUlcerativeColitisCalculator()
    return calculator.calculate(stool_frequency, rectal_bleeding, mucosal_appearance, physician_global_assessment)