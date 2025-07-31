"""
Gleason Score for Prostate Cancer Calculator

The Gleason Score is a histologic grading system for prostate cancer based on 
microscopic tumor architecture patterns. Developed by Dr. Donald Gleason in the 1960s 
and modified in 2014 by the International Society of Urological Pathology (ISUP), 
it uses primary and secondary tumor patterns to predict prognosis and guide treatment 
decisions. The score combines the two most prevalent architectural patterns found in 
the tumor specimen and ranges from 6-10.

References (Vancouver style):
1. Gleason DF, Mellinger GT. Prediction of prognosis for prostatic adenocarcinoma by 
   combined histological grading and clinical staging. J Urol. 1974;111(1):58-64.
2. Epstein JI, Egevad L, Amin MB, et al. The 2014 International Society of Urological 
   Pathology (ISUP) Consensus Conference on Gleason Grading of Prostatic Carcinoma: 
   Definition of Grading Patterns and Proposal for a New Grading System. Am J Surg 
   Pathol. 2016;40(2):244-252. doi: 10.1097/PAS.0000000000000530.
3. Pierorazio PM, Walsh PC, Partin AW, Epstein JI. Prognostic Gleason grade grouping: 
   data based on the modified Gleason scoring system. BJU Int. 2013;111(5):753-760. 
   doi: 10.1111/j.1464-410X.2012.11611.x.
4. D'Amico AV, Whittington R, Malkowicz SB, et al. Biochemical outcome after radical 
   prostatectomy, external beam radiation therapy, or interstitial radiation therapy 
   for clinically localized prostate cancer. JAMA. 1998;280(11):969-974. 
   doi: 10.1001/jama.280.11.969.
"""

from typing import Dict, Any


class GleasonScoreProstateCalculator:
    """Calculator for Gleason Score for Prostate Cancer"""
    
    def __init__(self):
        # Grade pattern descriptions
        self.GRADE_DESCRIPTIONS = {
            3: "Well-formed glands with minimal architectural distortion",
            4: "Fused glands, ill-defined glands, or cribriform pattern", 
            5: "No glandular formation, solid sheets, or comedonecrosis"
        }
        
        # Grade Group mappings (ISUP 2014)
        self.GRADE_GROUPS = {
            6: {"group": 1, "description": "Grade Group 1 (≤6)"},
            7: {"group": "2_or_3", "description": "Grade Group 2 (3+4) or 3 (4+3)"},
            8: {"group": 4, "description": "Grade Group 4 (8)"},
            9: {"group": 5, "description": "Grade Group 5 (9-10)"},
            10: {"group": 5, "description": "Grade Group 5 (9-10)"}
        }
    
    def calculate(self, primary_grade: int, secondary_grade: int) -> Dict[str, Any]:
        """
        Calculates Gleason Score for prostate cancer prognosis
        
        Args:
            primary_grade (int): Primary Gleason grade (3-5, most prevalent pattern >50%)
            secondary_grade (int): Secondary Gleason grade (3-5, second most common ≥5%)
            
        Returns:
            Dict with the Gleason score, grade group, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(primary_grade, secondary_grade)
        
        # Calculate total score
        total_score = primary_grade + secondary_grade
        
        # Determine grade group based on score and pattern
        grade_group = self._determine_grade_group(primary_grade, secondary_grade, total_score)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(primary_grade, secondary_grade, total_score, grade_group)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, primary_grade: int, secondary_grade: int):
        """Validates input parameters"""
        
        if not isinstance(primary_grade, int) or primary_grade not in [3, 4, 5]:
            raise ValueError("Primary grade must be 3, 4, or 5 (grades 1-2 represent benign tissue)")
        
        if not isinstance(secondary_grade, int) or secondary_grade not in [3, 4, 5]:
            raise ValueError("Secondary grade must be 3, 4, or 5 (grades 1-2 represent benign tissue)")
    
    def _determine_grade_group(self, primary_grade: int, secondary_grade: int, total_score: int) -> Dict[str, Any]:
        """
        Determines ISUP Grade Group based on Gleason score and pattern
        
        Args:
            primary_grade (int): Primary pattern grade
            secondary_grade (int): Secondary pattern grade  
            total_score (int): Total Gleason score
            
        Returns:
            Dict with grade group number and description
        """
        
        if total_score == 6:
            return {"number": 1, "description": "Grade Group 1", "pattern": f"{primary_grade}+{secondary_grade}"}
        elif total_score == 7:
            if primary_grade == 3 and secondary_grade == 4:
                return {"number": 2, "description": "Grade Group 2", "pattern": "3+4"}
            elif primary_grade == 4 and secondary_grade == 3:
                return {"number": 3, "description": "Grade Group 3", "pattern": "4+3"}
            else:
                # Other combinations that sum to 7 (rare, like 5+2 but we only allow 3-5)
                return {"number": 3, "description": "Grade Group 3", "pattern": f"{primary_grade}+{secondary_grade}"}
        elif total_score == 8:
            return {"number": 4, "description": "Grade Group 4", "pattern": f"{primary_grade}+{secondary_grade}"}
        elif total_score >= 9:
            return {"number": 5, "description": "Grade Group 5", "pattern": f"{primary_grade}+{secondary_grade}"}
        else:
            # Should not reach here with current validation
            return {"number": 1, "description": "Grade Group 1", "pattern": f"{primary_grade}+{secondary_grade}"}
    
    def _get_interpretation(self, primary_grade: int, secondary_grade: int, 
                          total_score: int, grade_group: Dict[str, Any]) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Gleason score and grade group
        
        Returns:
            Dict with interpretation details
        """
        
        # Pattern-specific details
        primary_desc = self.GRADE_DESCRIPTIONS[primary_grade]
        secondary_desc = self.GRADE_DESCRIPTIONS[secondary_grade]
        pattern_summary = f"Primary pattern {primary_grade} ({primary_desc}); Secondary pattern {secondary_grade} ({secondary_desc})"
        
        # Score and grade group summary
        score_summary = f"Gleason Score: {primary_grade}+{secondary_grade}={total_score}. {grade_group['description']} ({grade_group['pattern']}). {pattern_summary}."
        
        # Clinical interpretation based on total score
        if total_score == 6:
            return {
                "stage": "Low-Grade Cancer (Grade Group 1)",
                "description": "Well-differentiated, favorable prognosis",
                "interpretation": (
                    f"{score_summary} Low-grade prostate cancer with excellent prognosis. "
                    f"Tumor grows slowly and is less likely to spread or metastasize. "
                    f"10-year cancer-specific survival exceeds 95%. Often managed with active "
                    f"surveillance, especially in older patients (>70 years) or those with "
                    f"limited life expectancy (<10 years). Treatment options include: active "
                    f"surveillance with regular PSA monitoring, radical prostatectomy, or "
                    f"radiation therapy. Decision should consider patient age, comorbidities, "
                    f"PSA levels, clinical stage, and patient preferences. Regular monitoring "
                    f"with PSA, DRE, and repeat biopsies if on surveillance."
                )
            }
        elif total_score == 7:
            if primary_grade == 3 and secondary_grade == 4:
                prognosis_detail = (
                    f"Grade Group 2 (3+4=7) has more favorable prognosis than Grade Group 3 "
                    f"(4+3=7) due to predominant well-differentiated pattern. "
                )
            else:
                prognosis_detail = (
                    f"Grade Group 3 (4+3=7) has less favorable prognosis than Grade Group 2 "
                    f"(3+4=7) due to predominant poorly-differentiated pattern. "
                )
            
            return {
                "stage": "Intermediate-Grade Cancer (Grade Group 2-3)",
                "description": "Moderately differentiated, intermediate prognosis",
                "interpretation": (
                    f"{score_summary} Intermediate-grade prostate cancer with moderate "
                    f"aggressiveness and metastatic potential. {prognosis_detail}"
                    f"10-year cancer-specific survival ranges 85-95%. Typically requires "
                    f"definitive treatment with curative intent. Treatment options include: "
                    f"radical prostatectomy, external beam radiation therapy (EBRT), "
                    f"brachytherapy, or combination therapies. May benefit from adjuvant "
                    f"hormone therapy depending on risk factors. Consider genetic testing "
                    f"and multidisciplinary consultation. Regular PSA monitoring and "
                    f"imaging surveillance post-treatment essential."
                )
            }
        elif total_score == 8:
            return {
                "stage": "High-Grade Cancer (Grade Group 4)",
                "description": "Poorly differentiated, unfavorable prognosis",
                "interpretation": (
                    f"{score_summary} High-grade prostate cancer with aggressive behavior "
                    f"and significant metastatic potential. 10-year cancer-specific survival "
                    f"ranges 60-80%. Requires aggressive multimodal treatment approach. "
                    f"Treatment typically includes: radical prostatectomy with extended "
                    f"lymph node dissection, high-dose radiation therapy with androgen "
                    f"deprivation therapy (ADT), or combination treatments. Consider "
                    f"neoadjuvant/adjuvant hormone therapy for 18-36 months. Advanced "
                    f"imaging (MRI, bone scan, CT) for staging. Genetic counseling and "
                    f"testing recommended. Close monitoring for biochemical recurrence "
                    f"and distant metastases required. Multidisciplinary oncology team "
                    f"management essential."
                )
            }
        else:  # total_score >= 9
            return {
                "stage": "Very High-Grade Cancer (Grade Group 5)",
                "description": "Very poorly differentiated, very unfavorable prognosis",
                "interpretation": (
                    f"{score_summary} Very high-grade prostate cancer with very aggressive "
                    f"behavior and high likelihood of metastasis. Poor prognosis with "
                    f"10-year cancer-specific survival 40-60%. Requires immediate aggressive "
                    f"multimodal treatment. Treatment includes: radical prostatectomy with "
                    f"extended lymph node dissection (if localized), high-dose radiation "
                    f"with long-term ADT (2-3 years), or systemic therapy for metastatic "
                    f"disease. Consider docetaxel chemotherapy, abiraterone, or enzalutamide. "
                    f"Advanced imaging and staging essential (CT, bone scan, PSMA PET if "
                    f"available). Genetic counseling and testing strongly recommended. "
                    f"Consider clinical trial enrollment. Multidisciplinary team management "
                    f"with medical oncology, radiation oncology, and urology required. "
                    f"Palliative care consultation for symptom management and quality of life."
                )
            }


def calculate_gleason_score_prostate(primary_grade: int, secondary_grade: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gleason_score_prostate pattern
    """
    calculator = GleasonScoreProstateCalculator()
    return calculator.calculate(primary_grade, secondary_grade)