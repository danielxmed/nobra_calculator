"""
GO-FAR (Good Outcome Following Attempted Resuscitation) Score Calculator

The GO-FAR score is an evidence-based tool developed to predict survival to discharge 
with good neurological outcome after in-hospital cardiac arrest. It uses 13 pre-arrest 
clinical variables to stratify patients into risk categories, enabling healthcare 
providers to have informed discussions with patients and families about resuscitation 
preferences and code status decisions.

The score helps identify patients who are unlikely to benefit from resuscitation 
attempts, supporting shared decision-making regarding do-not-attempt-resuscitation 
(DNAR) orders. It should be used as part of comprehensive clinical assessment, not 
as the sole determinant of resuscitation status.

References (Vancouver style):
1. Ebell MH, Jang W, Shen Y, Geocadin RG. Get With the Guidelines-Resuscitation 
   Investigators. Development and validation of the Good Outcome Following Attempted 
   Resuscitation (GO-FAR) score to predict neurologically intact survival after 
   in-hospital cardiopulmonary resuscitation. JAMA Intern Med. 2013;173(20):1872-8. 
   doi: 10.1001/jamainternmed.2013.10037.
2. Piscator E, Hedberg P, Göransson K, Djarv T. Prearrest prediction of survival with 
   good neurologic recovery among in-hospital cardiac arrest patients. Resuscitation. 
   2018;128:63-69. doi: 10.1016/j.resuscitation.2018.05.006.
3. Perman SM, Stanton E, Soar J, et al. Location of in-hospital cardiac arrest in the 
   United States—variability in event rate and outcomes. J Am Heart Assoc. 
   2016;5(10):e003638. doi: 10.1161/JAHA.116.003638.
"""

from typing import Dict, Any


class GoFarScoreCalculator:
    """Calculator for GO-FAR (Good Outcome Following Attempted Resuscitation) Score"""
    
    def __init__(self):
        # Age category point values
        self.AGE_POINTS = {
            "under_70": 0,
            "70_to_74": 2,
            "75_to_79": 5,
            "80_to_84": 6,
            "85_or_over": 11
        }
        
        # Individual variable point values
        self.VARIABLE_POINTS = {
            "neurologically_intact": -15,  # Only applied if "yes"
            "major_trauma": 10,
            "acute_stroke": 8,
            "metastatic_hematologic_cancer": 7,
            "septicemia": 7,
            "medical_noncardiac_diagnosis": 7,
            "hepatic_insufficiency": 6,
            "skilled_nursing_facility": 6,
            "hypotension_hypoperfusion": 5,
            "renal_insufficiency": 4,
            "respiratory_insufficiency": 4,
            "pneumonia": 1
        }
        
        # Survival probability ranges
        self.SURVIVAL_RANGES = {
            "above_average": {"min": -15, "max": -6, "probability": ">15%"},
            "average": {"min": -5, "max": 13, "probability": "3-15%"},
            "low": {"min": 14, "max": 23, "probability": "1-3%"},
            "very_low": {"min": 24, "max": 50, "probability": "<1%"}
        }
    
    def calculate(self, age_category: str, neurologically_intact: str, major_trauma: str,
                 acute_stroke: str, metastatic_hematologic_cancer: str, septicemia: str,
                 medical_noncardiac_diagnosis: str, hepatic_insufficiency: str,
                 skilled_nursing_facility: str, hypotension_hypoperfusion: str,
                 renal_insufficiency: str, respiratory_insufficiency: str,
                 pneumonia: str) -> Dict[str, Any]:
        """
        Calculates GO-FAR score from 13 clinical variables
        
        Args:
            age_category (str): Age category (under_70, 70_to_74, 75_to_79, 80_to_84, 85_or_over)
            neurologically_intact (str): Neurologically intact at admission (yes/no)
            major_trauma (str): Major trauma present (yes/no)
            acute_stroke (str): Acute stroke present (yes/no)
            metastatic_hematologic_cancer (str): Metastatic or hematologic cancer (yes/no)
            septicemia (str): Septicemia present (yes/no)
            medical_noncardiac_diagnosis (str): Medical non-cardiac diagnosis (yes/no)
            hepatic_insufficiency (str): Hepatic insufficiency present (yes/no)
            skilled_nursing_facility (str): Admitted from skilled nursing facility (yes/no)
            hypotension_hypoperfusion (str): Hypotension/hypoperfusion present (yes/no)
            renal_insufficiency (str): Renal insufficiency/dialysis (yes/no)
            respiratory_insufficiency (str): Respiratory insufficiency present (yes/no)
            pneumonia (str): Pneumonia present (yes/no)
            
        Returns:
            Dict with GO-FAR score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_category, neurologically_intact, major_trauma, acute_stroke,
            metastatic_hematologic_cancer, septicemia, medical_noncardiac_diagnosis,
            hepatic_insufficiency, skilled_nursing_facility, hypotension_hypoperfusion,
            renal_insufficiency, respiratory_insufficiency, pneumonia
        )
        
        # Calculate total score
        score = self._calculate_score(
            age_category, neurologically_intact, major_trauma, acute_stroke,
            metastatic_hematologic_cancer, septicemia, medical_noncardiac_diagnosis,
            hepatic_insufficiency, skilled_nursing_facility, hypotension_hypoperfusion,
            renal_insufficiency, respiratory_insufficiency, pneumonia
        )
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category: str, neurologically_intact: str, major_trauma: str,
                        acute_stroke: str, metastatic_hematologic_cancer: str, septicemia: str,
                        medical_noncardiac_diagnosis: str, hepatic_insufficiency: str,
                        skilled_nursing_facility: str, hypotension_hypoperfusion: str,
                        renal_insufficiency: str, respiratory_insufficiency: str,
                        pneumonia: str):
        """Validates input parameters"""
        
        # Validate age category
        if age_category not in self.AGE_POINTS:
            raise ValueError(f"Age category must be one of: {list(self.AGE_POINTS.keys())}")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("neurologically_intact", neurologically_intact),
            ("major_trauma", major_trauma),
            ("acute_stroke", acute_stroke),
            ("metastatic_hematologic_cancer", metastatic_hematologic_cancer),
            ("septicemia", septicemia),
            ("medical_noncardiac_diagnosis", medical_noncardiac_diagnosis),
            ("hepatic_insufficiency", hepatic_insufficiency),
            ("skilled_nursing_facility", skilled_nursing_facility),
            ("hypotension_hypoperfusion", hypotension_hypoperfusion),
            ("renal_insufficiency", renal_insufficiency),
            ("respiratory_insufficiency", respiratory_insufficiency),
            ("pneumonia", pneumonia)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_score(self, age_category: str, neurologically_intact: str, major_trauma: str,
                        acute_stroke: str, metastatic_hematologic_cancer: str, septicemia: str,
                        medical_noncardiac_diagnosis: str, hepatic_insufficiency: str,
                        skilled_nursing_facility: str, hypotension_hypoperfusion: str,
                        renal_insufficiency: str, respiratory_insufficiency: str,
                        pneumonia: str) -> int:
        """
        Calculates the total GO-FAR score
        
        Scoring system:
        - Age points: 0-11 based on age category
        - Neurologically intact: -15 points if yes, 0 if no
        - Other variables: positive points if yes, 0 if no
        """
        
        total_score = 0
        
        # Add age points
        total_score += self.AGE_POINTS[age_category]
        
        # Add points for positive findings
        variables_and_values = [
            ("neurologically_intact", neurologically_intact),
            ("major_trauma", major_trauma),
            ("acute_stroke", acute_stroke),
            ("metastatic_hematologic_cancer", metastatic_hematologic_cancer),
            ("septicemia", septicemia),
            ("medical_noncardiac_diagnosis", medical_noncardiac_diagnosis),
            ("hepatic_insufficiency", hepatic_insufficiency),
            ("skilled_nursing_facility", skilled_nursing_facility),
            ("hypotension_hypoperfusion", hypotension_hypoperfusion),
            ("renal_insufficiency", renal_insufficiency),
            ("respiratory_insufficiency", respiratory_insufficiency),
            ("pneumonia", pneumonia)
        ]
        
        for variable_name, variable_value in variables_and_values:
            if variable_value == "yes":
                total_score += self.VARIABLE_POINTS[variable_name]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on GO-FAR score
        
        Returns:
            Dict with survival category, probability, and clinical recommendations
        """
        
        # Determine survival category
        if self.SURVIVAL_RANGES["above_average"]["min"] <= score <= self.SURVIVAL_RANGES["above_average"]["max"]:
            category = "above_average"
            stage = "Above Average Survival"
            description = "Good prognosis"
            probability = self.SURVIVAL_RANGES["above_average"]["probability"]
            recommendations = (
                "Above average probability of survival with good neurological outcome. "
                "Resuscitation is generally appropriate and should be discussed with patient and family. "
                "Consider patient values and preferences in decision-making. Full resuscitation measures "
                "are typically warranted unless patient has expressed different preferences."
            )
        elif self.SURVIVAL_RANGES["average"]["min"] <= score <= self.SURVIVAL_RANGES["average"]["max"]:
            category = "average"
            stage = "Average Survival"
            description = "Intermediate prognosis"
            probability = self.SURVIVAL_RANGES["average"]["probability"]
            recommendations = (
                "Average probability of survival with good neurological outcome. "
                "Individualized decision-making is recommended based on patient values, preferences, "
                "and goals of care. Discuss benefits and risks of resuscitation with patient and family. "
                "Consider patient's quality of life expectations and advance directives."
            )
        elif self.SURVIVAL_RANGES["low"]["min"] <= score <= self.SURVIVAL_RANGES["low"]["max"]:
            category = "low"
            stage = "Low Survival"
            description = "Poor prognosis"
            probability = self.SURVIVAL_RANGES["low"]["probability"]
            recommendations = (
                "Low probability of survival with good neurological outcome. "
                "Consider discussing limitations of resuscitation with patient and family. "
                "Focus on comfort measures and quality of life. Explore patient's values "
                "and preferences regarding aggressive interventions. Consider palliative care consultation."
            )
        else:  # Very low survival (score >= 24)
            category = "very_low"
            stage = "Very Low Survival"
            description = "Very poor prognosis"
            probability = self.SURVIVAL_RANGES["very_low"]["probability"]
            recommendations = (
                "Very low probability of survival with good neurological outcome. "
                "Strong consideration for do-not-attempt-resuscitation (DNAR) order after "
                "appropriate discussion with patient and family. Focus on comfort care and "
                "symptom management. Consider palliative care consultation and transition "
                "to comfort-focused goals of care."
            )
        
        # Build comprehensive interpretation
        interpretation = (
            f"GO-FAR Score: {score} points. Survival probability category: {stage} ({probability}). "
            f"Clinical recommendations: {recommendations} "
            f"Important note: This score should be used as part of comprehensive clinical assessment "
            f"and shared decision-making, not as the sole determinant of resuscitation status. "
            f"Consider patient autonomy, cultural factors, and individual circumstances."
        )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }


def calculate_go_far_score(age_category: str, neurologically_intact: str, major_trauma: str,
                          acute_stroke: str, metastatic_hematologic_cancer: str, septicemia: str,
                          medical_noncardiac_diagnosis: str, hepatic_insufficiency: str,
                          skilled_nursing_facility: str, hypotension_hypoperfusion: str,
                          renal_insufficiency: str, respiratory_insufficiency: str,
                          pneumonia: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_go_far_score pattern
    """
    calculator = GoFarScoreCalculator()
    return calculator.calculate(
        age_category, neurologically_intact, major_trauma, acute_stroke,
        metastatic_hematologic_cancer, septicemia, medical_noncardiac_diagnosis,
        hepatic_insufficiency, skilled_nursing_facility, hypotension_hypoperfusion,
        renal_insufficiency, respiratory_insufficiency, pneumonia
    )