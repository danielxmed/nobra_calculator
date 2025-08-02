"""
Immune-Related Adverse Events for GI Toxicity - Colitis Calculator

Grades severity of colitis secondary to immune checkpoint inhibitor therapy
and provides management recommendations based on CTCAE Version 5.0 criteria.

References (Vancouver style):
1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
   Management of Immune-Related Adverse Events in Patients Treated With Immune 
   Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
   Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
   doi: 10.1200/JCO.2017.77.6385.

2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
   NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
   Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
   doi: 10.6004/jnccn.2020.0012.

3. Wang DY, Salem JE, Cohen JV, Chandra S, Menzer C, Ye F, et al. Fatal Toxic 
   Effects Associated With Immune Checkpoint Inhibitors: A Systematic Review 
   and Meta-analysis. JAMA Oncol. 2018 Dec 1;4(12):1721-1728. 
   doi: 10.1001/jamaoncol.2018.3923.

4. Gupta A, De Felice KM, Loftus EV Jr, Khanna S. Systematic review: colitis 
   associated with anti-CTLA-4 therapy. Aliment Pharmacol Ther. 2015 Aug;42(4):406-17. 
   doi: 10.1111/apt.13281.
"""

from typing import Dict, Any


class ImmuneRelatedAdverseEventsGiColitisCalculator:
    """Calculator for immune-related adverse events GI colitis grading"""
    
    def __init__(self):
        # Stool frequency thresholds for grading
        self.stool_thresholds = {
            "grade_1_max": 3,   # <4 stools/day increase for Grade 1
            "grade_2_min": 4,   # 4-6 stools/day increase for Grade 2
            "grade_2_max": 6,
            "grade_3_min": 7    # ≥7 stools/day increase for Grade 3
        }
    
    def calculate(self, stool_increase_per_day: int, incontinence_present: str,
                  functional_impact: str, hospitalization_indicated: str) -> Dict[str, Any]:
        """
        Calculates the irAE grade for GI colitis
        
        Args:
            stool_increase_per_day (int): Increase in stools per day over baseline
            incontinence_present (str): "yes" or "no" for fecal incontinence
            functional_impact (str): "none_minimal", "moderate_limiting", "severe_limiting", or "life_threatening"
            hospitalization_indicated (str): "yes" or "no" for hospitalization indication
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(stool_increase_per_day, incontinence_present, 
                             functional_impact, hospitalization_indicated)
        
        # Determine grade based on clinical criteria
        grade = self._determine_grade(stool_increase_per_day, incontinence_present,
                                     functional_impact, hospitalization_indicated)
        
        # Get interpretation
        interpretation = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["grade"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, stool_increase_per_day: int, incontinence_present: str,
                        functional_impact: str, hospitalization_indicated: str):
        """Validates input parameters"""
        
        # Validate stool increase
        if not isinstance(stool_increase_per_day, int):
            raise ValueError("stool_increase_per_day must be an integer")
        
        if stool_increase_per_day < 0 or stool_increase_per_day > 20:
            raise ValueError("stool_increase_per_day must be between 0 and 20")
        
        # Validate incontinence
        if incontinence_present not in ["yes", "no"]:
            raise ValueError("incontinence_present must be 'yes' or 'no'")
        
        # Validate functional impact
        valid_impacts = ["none_minimal", "moderate_limiting", "severe_limiting", "life_threatening"]
        if functional_impact not in valid_impacts:
            raise ValueError(f"functional_impact must be one of: {valid_impacts}")
        
        # Validate hospitalization
        if hospitalization_indicated not in ["yes", "no"]:
            raise ValueError("hospitalization_indicated must be 'yes' or 'no'")
    
    def _determine_grade(self, stool_increase_per_day: int, incontinence_present: str,
                        functional_impact: str, hospitalization_indicated: str) -> int:
        """Determines the irAE grade based on clinical criteria"""
        
        # Grade 4: Life-threatening consequences
        if functional_impact == "life_threatening":
            return 4
        
        # Grade 3: ≥7 stools/day increase OR incontinence OR severe functional limitation OR hospitalization needed
        if (stool_increase_per_day >= self.stool_thresholds["grade_3_min"] or
            incontinence_present == "yes" or
            functional_impact == "severe_limiting" or
            hospitalization_indicated == "yes"):
            return 3
        
        # Grade 2: 4-6 stools/day increase OR moderate functional limitation
        if (stool_increase_per_day >= self.stool_thresholds["grade_2_min"] and 
            stool_increase_per_day <= self.stool_thresholds["grade_2_max"]) or \
           functional_impact == "moderate_limiting":
            return 2
        
        # Grade 1: <4 stools/day increase with minimal impact
        return 1
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Gets the clinical interpretation based on the grade
        
        Args:
            grade (int): irAE grade (1-4)
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            1: {
                "grade": "Grade 1",
                "description": "Mild - Increase of <4 stools per day over baseline",
                "interpretation": (
                    "Continue immune checkpoint inhibitor (ICPi) with close monitoring. "
                    "Monitor for dehydration and electrolyte imbalances. Recommend dietary "
                    "changes (avoid high-fiber foods, dairy, caffeine). Expedited patient "
                    "contact and follow-up. Consider supportive care with loperamide if needed. "
                    "Educate patient on symptom monitoring."
                )
            },
            2: {
                "grade": "Grade 2",
                "description": "Moderate - Increase of 4-6 stools per day over baseline",
                "interpretation": (
                    "Hold ICPi until symptoms improve to grade ≤1. Consider corticosteroids "
                    "(prednisone 1 mg/kg/day). Provide supportive care including loperamide, "
                    "hydration, electrolyte monitoring. Obtain gastroenterology consultation. "
                    "Consider endoscopy evaluation to assess mucosal inflammation. Monitor "
                    "for progression to higher grade. Resume ICPi when symptoms controlled."
                )
            },
            3: {
                "grade": "Grade 3",
                "description": "Severe - Increase of ≥7 stools per day, incontinence, limiting self-care",
                "interpretation": (
                    "Consider permanently discontinuing CTLA-4 agents. Administer corticosteroids "
                    "(prednisone 1-2 mg/kg/day). Consider hospitalization for severe symptoms "
                    "or complications. Urgent gastroenterology consultation required. Consider "
                    "IV corticosteroids or infliximab if steroid-refractory. Monitor for "
                    "complications (perforation, bleeding). Aggressive supportive care."
                )
            },
            4: {
                "grade": "Grade 4",
                "description": "Life-threatening - Life-threatening consequences, urgent intervention required",
                "interpretation": (
                    "Permanently discontinue ICPi treatment. Immediate hospitalization required. "
                    "High-dose IV corticosteroids (methylprednisolone 1-2 mg/kg/day). Consider "
                    "early infliximab treatment (5 mg/kg) if steroid-refractory within 3-5 days. "
                    "Urgent gastroenterology and surgical consultation. Monitor for perforation, "
                    "bleeding, sepsis. Intensive supportive care with fluid resuscitation."
                )
            }
        }
        
        return interpretations.get(grade, interpretations[4])  # Default to Grade 4 if invalid


def calculate_immune_related_adverse_events_gi_colitis(
    stool_increase_per_day: int, incontinence_present: str,
    functional_impact: str, hospitalization_indicated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_immune_related_adverse_events_gi_colitis pattern
    """
    calculator = ImmuneRelatedAdverseEventsGiColitisCalculator()
    return calculator.calculate(stool_increase_per_day, incontinence_present,
                               functional_impact, hospitalization_indicated)