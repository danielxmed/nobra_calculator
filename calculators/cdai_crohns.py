"""
Crohn's Disease Activity Index (CDAI) Calculator

Quantifies disease activity in Crohn's disease patients using clinical symptoms 
and laboratory findings over a 7-day period.

References:
- Best WR, Becktel JM, Singleton JW, Kern F Jr. Gastroenterology. 1976;70(3):439-444.
- Sandborn WJ, Feagan BG, Hanauer SB, et al. Gastroenterology. 2002;122(2):512-530.
"""

from typing import Dict, Any, List


class CdaiCrohnsCalculator:
    """Calculator for Crohn's Disease Activity Index (CDAI)"""
    
    def __init__(self):
        # Multipliers for each component
        self.LIQUID_STOOLS_MULTIPLIER = 2
        self.ABDOMINAL_PAIN_MULTIPLIER = 5
        self.GENERAL_WELLBEING_MULTIPLIER = 7
        self.EXTRAINTESTINAL_MULTIPLIER = 20
        self.ANTIDIARRHEAL_MULTIPLIER = 30
        self.ABDOMINAL_MASS_MULTIPLIER = 10
        self.HEMATOCRIT_MULTIPLIER = 6
        self.WEIGHT_MULTIPLIER = 1
        
        # Expected hematocrit values
        self.EXPECTED_HEMATOCRIT_MALE = 47.0
        self.EXPECTED_HEMATOCRIT_FEMALE = 42.0
        
        # Scoring dictionaries
        self.ABDOMINAL_PAIN_SCORES = {
            "none": 0,
            "mild": 1,
            "moderate": 2,
            "severe": 3
        }
        
        self.GENERAL_WELLBEING_SCORES = {
            "generally_well": 0,
            "slightly_under_par": 1,
            "poor": 2,
            "very_poor": 3,
            "terrible": 4
        }
        
        self.ABDOMINAL_MASS_SCORES = {
            "none": 0,
            "questionable": 2,
            "definite": 5
        }
    
    def calculate(self, liquid_stools_week: int, abdominal_pain_score: str, 
                  general_wellbeing_score: str, arthritis_arthralgias: str,
                  iritis_uveitis: str, erythema_nodosum: str, 
                  anal_fissure_fistula: str, other_fistulas: str, fever: str,
                  antidiarrheal_use: str, abdominal_mass: str, patient_sex: str,
                  observed_hematocrit: float, current_weight: float, 
                  ideal_weight: float) -> Dict[str, Any]:
        """
        Calculates the CDAI score using clinical parameters and laboratory values
        
        Args:
            liquid_stools_week (int): Number of liquid stools in past 7 days
            abdominal_pain_score (str): Average daily abdominal pain rating
            general_wellbeing_score (str): Average daily general well-being rating
            arthritis_arthralgias (str): Presence of arthritis/arthralgias
            iritis_uveitis (str): Presence of iritis/uveitis
            erythema_nodosum (str): Presence of erythema nodosum
            anal_fissure_fistula (str): Presence of anal fissure/fistula
            other_fistulas (str): Presence of other fistulas
            fever (str): Fever >37.8°C in past 7 days
            antidiarrheal_use (str): Use of antidiarrheal medications
            abdominal_mass (str): Presence of abdominal mass
            patient_sex (str): Patient biological sex
            observed_hematocrit (float): Current hematocrit percentage
            current_weight (float): Current weight in kg
            ideal_weight (float): Ideal weight in kg
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(liquid_stools_week, abdominal_pain_score, 
                            general_wellbeing_score, arthritis_arthralgias,
                            iritis_uveitis, erythema_nodosum, anal_fissure_fistula,
                            other_fistulas, fever, antidiarrheal_use, abdominal_mass,
                            patient_sex, observed_hematocrit, current_weight, ideal_weight)
        
        # Calculate each component
        component_scores = self._calculate_components(
            liquid_stools_week, abdominal_pain_score, general_wellbeing_score,
            arthritis_arthralgias, iritis_uveitis, erythema_nodosum,
            anal_fissure_fistula, other_fistulas, fever, antidiarrheal_use,
            abdominal_mass, patient_sex, observed_hematocrit, current_weight, ideal_weight
        )
        
        # Calculate total CDAI score
        total_score = sum(component_scores.values())
        total_score = int(round(total_score))
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_breakdown": self._format_component_breakdown(component_scores),
            "clinical_significance": self._get_clinical_significance(total_score),
            "calculation_details": self._get_calculation_details(component_scores)
        }
    
    def _validate_inputs(self, liquid_stools_week: int, abdominal_pain_score: str,
                        general_wellbeing_score: str, arthritis_arthralgias: str,
                        iritis_uveitis: str, erythema_nodosum: str, 
                        anal_fissure_fistula: str, other_fistulas: str, fever: str,
                        antidiarrheal_use: str, abdominal_mass: str, patient_sex: str,
                        observed_hematocrit: float, current_weight: float, 
                        ideal_weight: float):
        """Validates input parameters"""
        
        if not isinstance(liquid_stools_week, int) or liquid_stools_week < 0 or liquid_stools_week > 200:
            raise ValueError("Liquid stools count must be between 0 and 200")
        
        if abdominal_pain_score not in self.ABDOMINAL_PAIN_SCORES:
            valid_options = list(self.ABDOMINAL_PAIN_SCORES.keys())
            raise ValueError(f"Invalid abdominal pain score. Must be one of: {valid_options}")
        
        if general_wellbeing_score not in self.GENERAL_WELLBEING_SCORES:
            valid_options = list(self.GENERAL_WELLBEING_SCORES.keys())
            raise ValueError(f"Invalid general well-being score. Must be one of: {valid_options}")
        
        yes_no_fields = [
            arthritis_arthralgias, iritis_uveitis, erythema_nodosum,
            anal_fissure_fistula, other_fistulas, fever, antidiarrheal_use
        ]
        
        for field in yes_no_fields:
            if field not in ["yes", "no"]:
                raise ValueError("All extraintestinal complications and antidiarrheal use must be 'yes' or 'no'")
        
        if abdominal_mass not in self.ABDOMINAL_MASS_SCORES:
            valid_options = list(self.ABDOMINAL_MASS_SCORES.keys())
            raise ValueError(f"Invalid abdominal mass. Must be one of: {valid_options}")
        
        if patient_sex not in ["male", "female"]:
            raise ValueError("Patient sex must be 'male' or 'female'")
        
        if not 10.0 <= observed_hematocrit <= 60.0:
            raise ValueError("Observed hematocrit must be between 10.0 and 60.0%")
        
        if not 30.0 <= current_weight <= 300.0:
            raise ValueError("Current weight must be between 30.0 and 300.0 kg")
        
        if not 30.0 <= ideal_weight <= 300.0:
            raise ValueError("Ideal weight must be between 30.0 and 300.0 kg")
    
    def _calculate_components(self, liquid_stools_week: int, abdominal_pain_score: str,
                            general_wellbeing_score: str, arthritis_arthralgias: str,
                            iritis_uveitis: str, erythema_nodosum: str,
                            anal_fissure_fistula: str, other_fistulas: str, fever: str,
                            antidiarrheal_use: str, abdominal_mass: str, patient_sex: str,
                            observed_hematocrit: float, current_weight: float, 
                            ideal_weight: float) -> Dict[str, float]:
        """Calculate individual component scores"""
        
        # Component 1: Liquid stools
        liquid_stools_score = liquid_stools_week * self.LIQUID_STOOLS_MULTIPLIER
        
        # Component 2: Abdominal pain
        pain_score = self.ABDOMINAL_PAIN_SCORES[abdominal_pain_score]
        abdominal_pain_score_total = pain_score * self.ABDOMINAL_PAIN_MULTIPLIER
        
        # Component 3: General well-being
        wellbeing_score = self.GENERAL_WELLBEING_SCORES[general_wellbeing_score]
        general_wellbeing_score_total = wellbeing_score * self.GENERAL_WELLBEING_MULTIPLIER
        
        # Component 4: Extraintestinal complications (count present complications)
        extraintestinal_count = 0
        complications = [
            arthritis_arthralgias, iritis_uveitis, erythema_nodosum,
            anal_fissure_fistula, other_fistulas, fever
        ]
        extraintestinal_count = sum(1 for comp in complications if comp == "yes")
        extraintestinal_score = extraintestinal_count * self.EXTRAINTESTINAL_MULTIPLIER
        
        # Component 5: Antidiarrheal use
        antidiarrheal_score = (1 if antidiarrheal_use == "yes" else 0) * self.ANTIDIARRHEAL_MULTIPLIER
        
        # Component 6: Abdominal mass
        mass_score = self.ABDOMINAL_MASS_SCORES[abdominal_mass]
        abdominal_mass_score_total = mass_score * self.ABDOMINAL_MASS_MULTIPLIER
        
        # Component 7: Hematocrit deficit
        expected_hematocrit = (self.EXPECTED_HEMATOCRIT_MALE if patient_sex == "male" 
                              else self.EXPECTED_HEMATOCRIT_FEMALE)
        hematocrit_deficit = max(0, expected_hematocrit - observed_hematocrit)
        hematocrit_score = hematocrit_deficit * self.HEMATOCRIT_MULTIPLIER
        
        # Component 8: Weight deficit
        weight_deficit_percentage = max(0, (ideal_weight - current_weight) / ideal_weight * 100)
        weight_score = weight_deficit_percentage * self.WEIGHT_MULTIPLIER
        
        return {
            "liquid_stools": liquid_stools_score,
            "abdominal_pain": abdominal_pain_score_total,
            "general_wellbeing": general_wellbeing_score_total,
            "extraintestinal": extraintestinal_score,
            "antidiarrheal": antidiarrheal_score,
            "abdominal_mass": abdominal_mass_score_total,
            "hematocrit": hematocrit_score,
            "weight": weight_score
        }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the total score
        
        Args:
            total_score (int): Total CDAI score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score < 150:
            return {
                "stage": "Remission",
                "description": "Clinical remission",
                "interpretation": (f"CDAI score of {total_score} indicates clinical remission. "
                                 "Patients in this range are typically rated as 'very well' by physicians. "
                                 "Continue current maintenance therapy and monitor regularly.")
            }
        elif total_score < 220:
            return {
                "stage": "Mild Disease",
                "description": "Mild disease activity",
                "interpretation": (f"CDAI score of {total_score} indicates mild disease activity. "
                                 "Consider optimization of current therapy or step-up treatment. "
                                 "Monitor closely and reassess in 2-4 weeks.")
            }
        elif total_score < 300:
            return {
                "stage": "Moderate Disease",
                "description": "Moderate disease activity",
                "interpretation": (f"CDAI score of {total_score} indicates moderate disease activity. "
                                 "Consider corticosteroids, immunomodulators, or biologic therapy. "
                                 "Reassess in 2-4 weeks.")
            }
        elif total_score <= 450:
            return {
                "stage": "Severe Disease",
                "description": "Severe disease activity",
                "interpretation": (f"CDAI score of {total_score} indicates severe disease activity. "
                                 "Consider hospitalization, corticosteroids, immunosuppressants, or "
                                 "biologic therapy. Close monitoring required.")
            }
        else:  # > 450
            return {
                "stage": "Very Severe Disease",
                "description": "Very severe disease activity",
                "interpretation": (f"CDAI score of {total_score} indicates very severe disease activity. "
                                 "Consider hospitalization, intensive medical therapy, or surgical "
                                 "intervention. Immediate specialist consultation recommended.")
            }
    
    def _format_component_breakdown(self, component_scores: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Format component breakdown for response"""
        
        return {
            "liquid_stools": {
                "score": round(component_scores["liquid_stools"], 1),
                "description": "Number of liquid stools × 2",
                "multiplier": self.LIQUID_STOOLS_MULTIPLIER
            },
            "abdominal_pain": {
                "score": round(component_scores["abdominal_pain"], 1),
                "description": "Abdominal pain rating × 5",
                "multiplier": self.ABDOMINAL_PAIN_MULTIPLIER
            },
            "general_wellbeing": {
                "score": round(component_scores["general_wellbeing"], 1),
                "description": "General well-being rating × 7",
                "multiplier": self.GENERAL_WELLBEING_MULTIPLIER
            },
            "extraintestinal": {
                "score": round(component_scores["extraintestinal"], 1),
                "description": "Number of extraintestinal complications × 20",
                "multiplier": self.EXTRAINTESTINAL_MULTIPLIER
            },
            "antidiarrheal": {
                "score": round(component_scores["antidiarrheal"], 1),
                "description": "Antidiarrheal drug use × 30",
                "multiplier": self.ANTIDIARRHEAL_MULTIPLIER
            },
            "abdominal_mass": {
                "score": round(component_scores["abdominal_mass"], 1),
                "description": "Abdominal mass presence × 10",
                "multiplier": self.ABDOMINAL_MASS_MULTIPLIER
            },
            "hematocrit": {
                "score": round(component_scores["hematocrit"], 1),
                "description": "Hematocrit deficit × 6",
                "multiplier": self.HEMATOCRIT_MULTIPLIER
            },
            "weight": {
                "score": round(component_scores["weight"], 1),
                "description": "Weight deficit percentage × 1",
                "multiplier": self.WEIGHT_MULTIPLIER
            }
        }
    
    def _get_clinical_significance(self, total_score: int) -> Dict[str, Any]:
        """Get clinical significance and treatment response criteria"""
        
        return {
            "treatment_response_criteria": {
                "significant_response": "≥70 point decrease from baseline",
                "major_response": "≥100 point decrease from baseline",
                "remission_threshold": "<150 points"
            },
            "clinical_trial_usage": "Primary endpoint in most Crohn's disease clinical trials",
            "monitoring_frequency": self._get_monitoring_frequency(total_score),
            "treatment_considerations": self._get_treatment_considerations(total_score)
        }
    
    def _get_monitoring_frequency(self, total_score: int) -> str:
        """Get recommended monitoring frequency based on score"""
        
        if total_score < 150:
            return "Every 3-6 months or as clinically indicated"
        elif total_score < 220:
            return "Every 2-4 weeks until improvement"
        elif total_score < 300:
            return "Every 1-2 weeks with close monitoring"
        else:
            return "Weekly or more frequently, consider hospitalization"
    
    def _get_treatment_considerations(self, total_score: int) -> List[str]:
        """Get treatment considerations based on score"""
        
        if total_score < 150:
            return [
                "Continue current maintenance therapy",
                "Monitor for disease recurrence",
                "Focus on quality of life and nutrition"
            ]
        elif total_score < 220:
            return [
                "Optimize current medications",
                "Consider dose escalation",
                "Evaluate adherence and absorption"
            ]
        elif total_score < 300:
            return [
                "Consider corticosteroids for rapid symptom control",
                "Initiate or optimize immunomodulators",
                "Consider biologic therapy",
                "Nutritional assessment and support"
            ]
        else:
            return [
                "Consider hospitalization",
                "Intensive medical therapy",
                "Evaluate for complications",
                "Consider surgical consultation",
                "Nutritional support and monitoring"
            ]
    
    def _get_calculation_details(self, component_scores: Dict[str, float]) -> Dict[str, Any]:
        """Get detailed calculation information"""
        
        return {
            "formula": "CDAI = (Liquid stools × 2) + (Pain × 5) + (Well-being × 7) + (Complications × 20) + (Antidiarrheal × 30) + (Mass × 10) + (Hematocrit deficit × 6) + (Weight deficit × 1)",
            "total_possible_range": "0 to ~600 points",
            "assessment_period": "Based on 7-day patient diary",
            "original_study": "National Cooperative Crohn's Disease Study (1976)",
            "validation_studies": "Multiple validation studies confirm reliability and validity"
        }


def calculate_cdai_crohns(liquid_stools_week: int, abdominal_pain_score: str,
                         general_wellbeing_score: str, arthritis_arthralgias: str,
                         iritis_uveitis: str, erythema_nodosum: str,
                         anal_fissure_fistula: str, other_fistulas: str, fever: str,
                         antidiarrheal_use: str, abdominal_mass: str, patient_sex: str,
                         observed_hematocrit: float, current_weight: float,
                         ideal_weight: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CdaiCrohnsCalculator()
    return calculator.calculate(liquid_stools_week, abdominal_pain_score,
                              general_wellbeing_score, arthritis_arthralgias,
                              iritis_uveitis, erythema_nodosum, anal_fissure_fistula,
                              other_fistulas, fever, antidiarrheal_use, abdominal_mass,
                              patient_sex, observed_hematocrit, current_weight, ideal_weight)