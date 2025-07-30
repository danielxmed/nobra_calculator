"""
Centor Score (Modified/McIsaac) for Strep Pharyngitis Calculator

Estimates likelihood that pharyngitis is streptococcal and suggests management course.
Modified version includes age adjustment for improved accuracy.

References:
1. Centor RM, Witherspoon JM, Dalton HP, Brody CE, Link K. The diagnosis of strep throat 
   in adults in the emergency room. Med Decis Making. 1981;1(3):239-46. 
   doi: 10.1177/0272989X8100100304.
2. McIsaac WJ, White D, Tannenbaum D, Low DE. A clinical score to reduce unnecessary 
   antibiotic use in patients with sore throat. CMAJ. 1998 Jan 13;158(1):75-83.
3. McIsaac WJ, Kellner JD, Aufricht P, Vanjaka A, Low DE. Empirical validation of 
   guidelines for the management of pharyngitis in children and adults. JAMA. 2004 
   Apr 7;291(13):1587-95. doi: 10.1001/jama.291.13.1587.
"""

from typing import Dict, Any


class CentorScoreCalculator:
    """Calculator for Centor Score (Modified/McIsaac) for Strep Pharyngitis"""
    
    def __init__(self):
        # Probability ranges for GAS infection based on score
        self.probability_ranges = {
            (-1, 0, 1): {"min": 1, "max": 10, "description": "Low probability (1-10%)"},
            (2,): {"min": 11, "max": 17, "description": "Moderate probability (11-17%)"},
            (3,): {"min": 28, "max": 35, "description": "Moderate probability (28-35%)"},
            (4, 5): {"min": 51, "max": 53, "description": "High probability (51-53%)"}
        }
    
    def calculate(
        self,
        tonsillar_exudate: str,
        tender_cervical_nodes: str,
        history_of_fever: str,
        absence_of_cough: str,
        age_years: int
    ) -> Dict[str, Any]:
        """
        Calculates Modified Centor Score for streptococcal pharyngitis probability
        
        Args:
            tonsillar_exudate: Presence of tonsillar swelling or exudate
            tender_cervical_nodes: Swollen, tender anterior cervical lymph nodes
            history_of_fever: History of fever (>38°C or 100.4°F)
            absence_of_cough: Absence of cough
            age_years: Patient age in years
            
        Returns:
            Dict with Centor score, probability assessment, and management recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            tonsillar_exudate, tender_cervical_nodes, history_of_fever,
            absence_of_cough, age_years
        )
        
        # Calculate base score from clinical criteria
        base_score = self._calculate_clinical_score(
            tonsillar_exudate, tender_cervical_nodes, history_of_fever, absence_of_cough
        )
        
        # Apply age adjustment
        age_adjustment = self._get_age_adjustment(age_years)
        
        # Calculate total score
        total_score = base_score + age_adjustment
        
        # Get probability assessment
        probability = self._get_probability_assessment(total_score)
        
        # Get management recommendations
        management = self._get_management_recommendations(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            tonsillar_exudate, tender_cervical_nodes, history_of_fever,
            absence_of_cough, age_years, age_adjustment
        )
        
        return {
            "result": {
                "total_score": total_score,
                "gas_probability_percent": probability["probability_range"],
                "risk_level": management["risk_level"],
                "management_recommendation": management["recommendation"],
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": management["interpretation"],
            "stage": management["stage"],
            "stage_description": management["description"]
        }
    
    def _validate_inputs(self, tonsillar, nodes, fever, cough, age):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        
        if tonsillar not in valid_yes_no:
            raise ValueError("Tonsillar exudate must be 'yes' or 'no'")
        
        if nodes not in valid_yes_no:
            raise ValueError("Tender cervical nodes must be 'yes' or 'no'")
        
        if fever not in valid_yes_no:
            raise ValueError("History of fever must be 'yes' or 'no'")
        
        if cough not in valid_yes_no:
            raise ValueError("Absence of cough must be 'yes' or 'no'")
        
        if not isinstance(age, int) or not (3 <= age <= 120):
            raise ValueError("Age must be an integer between 3-120 years")
    
    def _calculate_clinical_score(self, tonsillar, nodes, fever, cough):
        """Calculates score from clinical criteria (1 point each)"""
        
        score = 0
        
        if tonsillar == "yes":
            score += 1
        
        if nodes == "yes":
            score += 1
        
        if fever == "yes":
            score += 1
        
        if cough == "yes":
            score += 1
        
        return score
    
    def _get_age_adjustment(self, age: int) -> int:
        """Gets age adjustment for modified Centor score"""
        
        if 3 <= age <= 14:
            return 1  # Higher risk of streptococcal infection in children
        elif 15 <= age <= 44:
            return 0  # Baseline risk
        else:  # age >= 45
            return -1  # Lower risk of streptococcal infection in older adults
    
    def _get_probability_assessment(self, score: int) -> Dict[str, Any]:
        """Gets probability assessment based on total score"""
        
        for score_range, prob_data in self.probability_ranges.items():
            if score in score_range:
                return {
                    "probability_range": f"{prob_data['min']}-{prob_data['max']}%",
                    "description": prob_data["description"]
                }
        
        # Default for edge cases
        return {
            "probability_range": "Unknown",
            "description": "Score outside validated range"
        }
    
    def _get_management_recommendations(self, score: int) -> Dict[str, str]:
        """Gets management recommendations based on score"""
        
        if score <= 1:
            return {
                "risk_level": "Low Risk",
                "stage": "Low Risk",
                "description": "Low probability of streptococcal infection",
                "recommendation": "No testing or antibiotics recommended",
                "interpretation": f"Centor Score {score}: Low probability of Group A Streptococcus (1-10%). No testing or antibiotics recommended. Provide symptomatic treatment only. Consider viral etiology and supportive care including analgesics, throat lozenges, and adequate hydration."
            }
        elif 2 <= score <= 3:
            return {
                "risk_level": "Moderate Risk",
                "stage": "Moderate Risk", 
                "description": "Moderate probability of streptococcal infection",
                "recommendation": "RADT and/or throat culture recommended",
                "interpretation": f"Centor Score {score}: Moderate probability of Group A Streptococcus (11-35%). Rapid antigen detection test (RADT) and/or throat culture recommended. Prescribe antibiotics only if test results are positive. Avoid empiric antibiotic treatment."
            }
        else:  # score >= 4
            return {
                "risk_level": "High Risk",
                "stage": "High Risk",
                "description": "High probability of streptococcal infection",
                "recommendation": "Consider empiric treatment or testing",
                "interpretation": f"Centor Score {score}: High probability of Group A Streptococcus (51-53%). Strong consideration for empiric antibiotic treatment or immediate testing with RADT/culture. High likelihood of bacterial infection requiring antibiotic therapy."
            }
    
    def _get_scoring_breakdown(self, tonsillar, nodes, fever, cough, age, age_adj):
        """Provides detailed scoring breakdown"""
        
        breakdown = {
            "clinical_criteria": {
                "tonsillar_exudate": {
                    "present": tonsillar == "yes",
                    "points": 1 if tonsillar == "yes" else 0,
                    "description": "Tonsillar swelling or exudate"
                },
                "tender_cervical_nodes": {
                    "present": nodes == "yes",
                    "points": 1 if nodes == "yes" else 0,
                    "description": "Swollen, tender anterior cervical lymph nodes"
                },
                "history_of_fever": {
                    "present": fever == "yes",
                    "points": 1 if fever == "yes" else 0,
                    "description": "History of fever (>38°C or 100.4°F)"
                },
                "absence_of_cough": {
                    "present": cough == "yes",
                    "points": 1 if cough == "yes" else 0,
                    "description": "Absence of cough"
                }
            },
            "age_adjustment": {
                "age_years": age,
                "age_category": self._get_age_category(age),
                "points": age_adj,
                "description": "Age-based risk adjustment"
            }
        }
        
        return breakdown
    
    def _get_age_category(self, age: int) -> str:
        """Gets age category description"""
        
        if 3 <= age <= 14:
            return "3-14 years (increased risk)"
        elif 15 <= age <= 44:
            return "15-44 years (baseline risk)"
        else:
            return "≥45 years (decreased risk)"


def calculate_centor_score(
    tonsillar_exudate: str,
    tender_cervical_nodes: str,
    history_of_fever: str,
    absence_of_cough: str,
    age_years: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CentorScoreCalculator()
    return calculator.calculate(
        tonsillar_exudate=tonsillar_exudate,
        tender_cervical_nodes=tender_cervical_nodes,
        history_of_fever=history_of_fever,
        absence_of_cough=absence_of_cough,
        age_years=age_years
    )