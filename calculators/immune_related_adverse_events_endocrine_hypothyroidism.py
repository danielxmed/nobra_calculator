"""
Immune-Related Adverse Events for Endocrine Toxicities - Hypothyroidism Calculator

Grades severity of hypothyroidism secondary to immune checkpoint inhibitor therapy
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

3. Faje AT, Sullivan R, Lawrence D, Trombetta M, Fadden R, Klibanski A, et al. 
   Ipilimumab-induced hypophysitis: a detailed longitudinal analysis in a large 
   cohort of patients with metastatic melanoma. J Clin Endocrinol Metab. 
   2014 Nov;99(11):4078-85. doi: 10.1210/jc.2014-2306.

4. Barroso-Sousa R, Barry WT, Garrido-Castro AC, Hodi FS, Min Y, Krop IE, et al. 
   Incidence of Endocrine Dysfunction Following the Use of Different Immune 
   Checkpoint Inhibitor Regimens: A Systematic Review and Meta-analysis. 
   JAMA Oncol. 2018 Feb 1;4(2):173-182. doi: 10.1001/jamaoncol.2017.3064.
"""

from typing import Dict, Any


class ImmuneRelatedAdverseEventsEndocrineHypothyroidismCalculator:
    """Calculator for immune-related adverse events endocrine hypothyroidism grading"""
    
    def __init__(self):
        # TSH thresholds in mIU/L
        self.tsh_threshold_grade_2 = 10.0  # TSH >10 mIU/L for Grade 2
        
        # Normal TSH range is typically 0.4-4.0 mIU/L (varies by laboratory)
        self.normal_tsh_upper = 4.0
    
    def calculate(self, tsh_miu_l: float, symptom_severity: str, 
                  myxedema_signs: str) -> Dict[str, Any]:
        """
        Calculates the irAE grade for endocrine hypothyroidism
        
        Args:
            tsh_miu_l (float): TSH level in mIU/L
            symptom_severity (str): "asymptomatic", "moderate_able_adls", or "severe_unable_adls"
            myxedema_signs (str): "yes" or "no" for myxedema or life-threatening complications
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(tsh_miu_l, symptom_severity, myxedema_signs)
        
        # Determine grade based on clinical criteria
        grade = self._determine_grade(tsh_miu_l, symptom_severity, myxedema_signs)
        
        # Get interpretation
        interpretation = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["grade"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, tsh_miu_l: float, symptom_severity: str, myxedema_signs: str):
        """Validates input parameters"""
        
        # Validate TSH
        if not isinstance(tsh_miu_l, (int, float)):
            raise ValueError("tsh_miu_l must be a number")
        
        if tsh_miu_l < 0.01 or tsh_miu_l > 100.0:
            raise ValueError("tsh_miu_l must be between 0.01 and 100.0 mIU/L")
        
        # Validate symptom severity
        valid_symptoms = ["asymptomatic", "moderate_able_adls", "severe_unable_adls"]
        if symptom_severity not in valid_symptoms:
            raise ValueError(f"symptom_severity must be one of: {valid_symptoms}")
        
        # Validate myxedema signs
        if myxedema_signs not in ["yes", "no"]:
            raise ValueError("myxedema_signs must be 'yes' or 'no'")
    
    def _determine_grade(self, tsh_miu_l: float, symptom_severity: str, 
                        myxedema_signs: str) -> int:
        """Determines the irAE grade based on clinical criteria"""
        
        # Grade 4: Life-threatening - myxedema coma or life-threatening complications
        if myxedema_signs == "yes":
            return 4
        
        # Grade 3: Severe symptoms, unable to perform ADLs
        if symptom_severity == "severe_unable_adls":
            return 3
        
        # Grade 2: Moderate symptoms with ADL preservation OR TSH >10 mIU/L
        if symptom_severity == "moderate_able_adls" or tsh_miu_l > self.tsh_threshold_grade_2:
            return 2
        
        # Grade 1: Asymptomatic with TSH <10 mIU/L (but usually >4.0 mIU/L to be considered abnormal)
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
                "description": "Mild - Asymptomatic with TSH <10 mIU/L",
                "interpretation": (
                    "Continue immune checkpoint inhibitor (ICPi) with close monitoring. "
                    "Check TSH and free thyroxine every 4-6 weeks during ICPi therapy. "
                    "No thyroid hormone supplementation needed at this time. Monitor for "
                    "development of symptoms or TSH elevation."
                )
            },
            2: {
                "grade": "Grade 2",
                "description": "Moderate - Moderate symptoms, able to perform ADLs, TSH >10 mIU/L",
                "interpretation": (
                    "May hold ICPi until symptoms resolve. Consider endocrinology consultation "
                    "for thyroid hormone replacement therapy. Consider thyroid hormone "
                    "supplementation with levothyroxine. Monitor TSH every 6-8 weeks. "
                    "Use free thyroxine monitoring short-term if needed. Resume ICPi when "
                    "symptoms controlled."
                )
            },
            3: {
                "grade": "Grade 3",
                "description": "Severe - Severe symptoms, unable to perform ADLs",
                "interpretation": (
                    "Hold ICPi until symptoms resolve to grade ≤1. Urgent endocrinology "
                    "consultation required. Initiate thyroid hormone supplementation immediately. "
                    "Consider hospital admission if signs of myxedema or cardiovascular "
                    "complications. Monitor closely for myxedema coma risk. Reassess thyroid "
                    "function as in grade 2."
                )
            },
            4: {
                "grade": "Grade 4",
                "description": "Life-threatening - Myxedema coma or life-threatening consequences",
                "interpretation": (
                    "Hold ICPi until symptoms resolve to grade ≤1. Immediate hospitalization "
                    "required for myxedema coma management. Urgent endocrinology and critical "
                    "care consultation. IV thyroid hormone replacement (levothyroxine or "
                    "liothyronine). Supportive care for hypothermia, hypotension, hyponatremia. "
                    "Consider permanent ICPi discontinuation."
                )
            }
        }
        
        return interpretations.get(grade, interpretations[4])  # Default to Grade 4 if invalid


def calculate_immune_related_adverse_events_endocrine_hypothyroidism(
    tsh_miu_l: float, symptom_severity: str, myxedema_signs: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_immune_related_adverse_events_endocrine_hypothyroidism pattern
    """
    calculator = ImmuneRelatedAdverseEventsEndocrineHypothyroidismCalculator()
    return calculator.calculate(tsh_miu_l, symptom_severity, myxedema_signs)