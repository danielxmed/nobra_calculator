"""
Immune-Related Adverse Events for GI Toxicity - Hepatitis Calculator

Grades severity of hepatitis secondary to immune checkpoint inhibitor (ICPi) therapy 
based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria.

This calculator evaluates liver function tests (AST, ALT, total bilirubin) to determine 
the severity of immune-mediated hepatitis and provides evidence-based management 
recommendations for ICPi therapy decisions.

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
4. De Martin E, Michot JM, Papoular B, Champiat S, Mateus C, Lambotte O, et al. 
   Characterization of liver injury induced by cancer immunotherapy using immune 
   checkpoint inhibitors. J Hepatol. 2018 Jun;68(6):1181-1190. 
   doi: 10.1016/j.jhep.2018.01.033.
"""

from typing import Dict, Any


class ImmuneRelatedAdverseEventsGiHepatitisCalculator:
    """Calculator for Immune-Related Adverse Events for GI Toxicity - Hepatitis"""
    
    def __init__(self):
        # CTCAE v5.0 grading thresholds for transaminases and bilirubin
        self.grade_thresholds = {
            "grade_1": {
                "transaminase_min": 1.0,
                "transaminase_max": 3.0,
                "bilirubin_min": 1.0,
                "bilirubin_max": 1.5
            },
            "grade_2": {
                "transaminase_min": 3.0,
                "transaminase_max": 5.0,
                "bilirubin_min": 1.5,
                "bilirubin_max": 3.0
            },
            "grade_3": {
                "transaminase_min": 5.0,
                "transaminase_max": 20.0,
                "bilirubin_min": 3.0,
                "bilirubin_max": 10.0
            },
            "grade_4": {
                "transaminase_min": 20.0,
                "bilirubin_min": 10.0
            }
        }
    
    def calculate(self, ast_level: float, ast_uln: float, alt_level: float, 
                 alt_uln: float, total_bilirubin: float, bilirubin_uln: float,
                 hepatic_decompensation: str) -> Dict[str, Any]:
        """
        Calculates the CTCAE grade for immune-related hepatitis
        
        Args:
            ast_level (float): AST level in U/L
            ast_uln (float): Upper limit of normal for AST in U/L
            alt_level (float): ALT level in U/L
            alt_uln (float): Upper limit of normal for ALT in U/L
            total_bilirubin (float): Total bilirubin level in mg/dL
            bilirubin_uln (float): Upper limit of normal for bilirubin in mg/dL
            hepatic_decompensation (str): Presence of hepatic decompensation ("yes" or "no")
            
        Returns:
            Dict with the grade and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(ast_level, ast_uln, alt_level, alt_uln, 
                            total_bilirubin, bilirubin_uln, hepatic_decompensation)
        
        # Calculate fold increases over ULN
        ast_fold = ast_level / ast_uln
        alt_fold = alt_level / alt_uln
        bilirubin_fold = total_bilirubin / bilirubin_uln
        
        # Determine grade based on CTCAE criteria
        grade = self._calculate_grade(ast_fold, alt_fold, bilirubin_fold, hepatic_decompensation)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, ast_level: float, ast_uln: float, alt_level: float,
                        alt_uln: float, total_bilirubin: float, bilirubin_uln: float,
                        hepatic_decompensation: str):
        """Validates input parameters"""
        
        # Validate AST values
        if not isinstance(ast_level, (int, float)) or ast_level < 5 or ast_level > 5000:
            raise ValueError("AST level must be a number between 5 and 5000 U/L")
        
        if not isinstance(ast_uln, (int, float)) or ast_uln < 20 or ast_uln > 80:
            raise ValueError("AST ULN must be a number between 20 and 80 U/L")
        
        # Validate ALT values
        if not isinstance(alt_level, (int, float)) or alt_level < 5 or alt_level > 5000:
            raise ValueError("ALT level must be a number between 5 and 5000 U/L")
        
        if not isinstance(alt_uln, (int, float)) or alt_uln < 20 or alt_uln > 80:
            raise ValueError("ALT ULN must be a number between 20 and 80 U/L")
        
        # Validate bilirubin values
        if not isinstance(total_bilirubin, (int, float)) or total_bilirubin < 0.1 or total_bilirubin > 50.0:
            raise ValueError("Total bilirubin must be a number between 0.1 and 50.0 mg/dL")
        
        if not isinstance(bilirubin_uln, (int, float)) or bilirubin_uln < 0.8 or bilirubin_uln > 2.0:
            raise ValueError("Bilirubin ULN must be a number between 0.8 and 2.0 mg/dL")
        
        # Validate hepatic decompensation
        if hepatic_decompensation not in ["yes", "no"]:
            raise ValueError("Hepatic decompensation must be 'yes' or 'no'")
    
    def _calculate_grade(self, ast_fold: float, alt_fold: float, bilirubin_fold: float,
                        hepatic_decompensation: str) -> int:
        """
        Determines CTCAE grade based on transaminase and bilirubin fold increases
        
        CTCAE v5.0 grading criteria:
        - Grade 1: AST/ALT 1-3× ULN OR bilirubin 1-1.5× ULN
        - Grade 2: AST/ALT 3-5× ULN OR bilirubin 1.5-3× ULN  
        - Grade 3: AST/ALT 5-20× ULN OR bilirubin 3-10× ULN
        - Grade 4: AST/ALT >20× ULN OR bilirubin >10× ULN OR hepatic decompensation
        """
        
        # Grade 4: Life-threatening - hepatic decompensation overrides all other criteria
        if hepatic_decompensation == "yes":
            return 4
        
        # Get the maximum transaminase fold increase (AST or ALT)
        max_transaminase_fold = max(ast_fold, alt_fold)
        
        # Grade 4: AST/ALT >20× ULN OR bilirubin >10× ULN
        if (max_transaminase_fold > self.grade_thresholds["grade_4"]["transaminase_min"] or
            bilirubin_fold > self.grade_thresholds["grade_4"]["bilirubin_min"]):
            return 4
        
        # Grade 3: AST/ALT 5-20× ULN OR bilirubin 3-10× ULN
        if (max_transaminase_fold >= self.grade_thresholds["grade_3"]["transaminase_min"] or
            bilirubin_fold >= self.grade_thresholds["grade_3"]["bilirubin_min"]):
            return 3
        
        # Grade 2: AST/ALT 3-5× ULN OR bilirubin 1.5-3× ULN
        if (max_transaminase_fold >= self.grade_thresholds["grade_2"]["transaminase_min"] or
            bilirubin_fold >= self.grade_thresholds["grade_2"]["bilirubin_min"]):
            return 2
        
        # Grade 1: AST/ALT 1-3× ULN OR bilirubin 1-1.5× ULN
        if (max_transaminase_fold >= self.grade_thresholds["grade_1"]["transaminase_min"] or
            bilirubin_fold >= self.grade_thresholds["grade_1"]["bilirubin_min"]):
            return 1
        
        # If no criteria met, default to Grade 1 (minimal elevation)
        return 1
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Provides clinical interpretation and management recommendations based on grade
        
        Args:
            grade (int): CTCAE grade (1-4)
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        interpretations = {
            1: {
                "stage": "Grade 1",
                "description": "Mild - AST/ALT 1-3× ULN OR total bilirubin 1-1.5× ULN",
                "interpretation": "Continue ICPi with close monitoring. Repeat liver chemistries 1-2 times weekly. Rule out alternative causes of hepatitis (viral, drug-induced, autoimmune, alcohol). Monitor for progression to higher grades. Consider hepatology consultation if persistent or worsening."
            },
            2: {
                "stage": "Grade 2", 
                "description": "Moderate - AST/ALT 3-5× ULN OR total bilirubin 1.5-3× ULN",
                "interpretation": "Hold ICPi until symptoms improve to grade ≤1. Start corticosteroids (methylprednisolone 1 mg/kg/day or equivalent). Obtain hepatology consultation. Rule out infectious and autoimmune causes. Consider liver biopsy if diagnosis unclear. Monitor liver function tests closely. Resume ICPi when grade ≤1 and steroids tapered."
            },
            3: {
                "stage": "Grade 3",
                "description": "Severe - AST/ALT 5-20× ULN OR total bilirubin 3-10× ULN", 
                "interpretation": "Permanently discontinue ICPi. Start high-dose corticosteroids (methylprednisolone 2 mg/kg/day or equivalent). Immediate hepatology consultation required. Consider hospitalization for monitoring. Rule out drug-induced liver injury and autoimmune hepatitis. Consider liver biopsy. If no improvement in 3-5 days, add mycophenolate mofetil or other immunosuppressants. Monitor for hepatic decompensation."
            },
            4: {
                "stage": "Grade 4",
                "description": "Life-threatening - AST/ALT >20× ULN OR total bilirubin >10× ULN OR hepatic decompensation",
                "interpretation": "Permanently discontinue ICPi. Immediate hospitalization required. Start high-dose IV corticosteroids (methylprednisolone 2 mg/kg/day). Urgent hepatology and intensive care consultation. Consider liver transplant evaluation if fulminant hepatic failure. Rule out drug-induced liver injury. Monitor coagulation parameters closely. Consider plasmapheresis or other rescue therapies if refractory to steroids."
            }
        }
        
        return interpretations.get(grade, interpretations[1])


def calculate_immune_related_adverse_events_gi_hepatitis(ast_level: float, ast_uln: float, 
                                                       alt_level: float, alt_uln: float,
                                                       total_bilirubin: float, bilirubin_uln: float,
                                                       hepatic_decompensation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImmuneRelatedAdverseEventsGiHepatitisCalculator()
    return calculator.calculate(ast_level, ast_uln, alt_level, alt_uln, 
                              total_bilirubin, bilirubin_uln, hepatic_decompensation)