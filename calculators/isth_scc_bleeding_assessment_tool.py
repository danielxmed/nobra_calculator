"""
ISTH-SCC Bleeding Assessment Tool Calculator

Assesses bleeding symptoms in patients with inherited bleeding disorders using the standardized 
questionnaire developed by the International Society on Thrombosis and Haemostasis (ISTH) 
Scientific and Standardization Committee (SSC).

References:
1. Rodeghiero F, Tosetto A, Abshire T, Arnold DM, Coller B, James P, Neunert C, Lillicrap D. ISTH/SSC bleeding assessment tool: a standardized questionnaire and a proposal for a new bleeding score for inherited bleeding disorders. J Thromb Haemost. 2010 Sep;8(9):2063-5.
2. Elbatarny M, Mollah S, Grabell J, et al. Normal range of bleeding scores for the ISTH-BAT: adult and pediatric data from the merging project. Haemophilia. 2014 Nov;20(6):831-5.
3. Deforest M, Grabell J, Albert S, et al. Generation and optimization of the self-administered bleeding assessment tool and its validation as a screening test for von Willebrand disease. Haemophilia. 2015 May;21(3):e132-9.
"""

from typing import Dict, Any


class IsthSccBleedingAssessmentToolCalculator:
    """Calculator for ISTH-SCC Bleeding Assessment Tool"""
    
    def __init__(self):
        # CNS bleeding special scoring
        self.CNS_BLEEDING_SCORES = {
            "never": 0,
            "subdural": 3,
            "intracerebral": 4
        }
        
        # Interpretation thresholds by demographic
        self.THRESHOLDS = {
            "child": {"typical_max": 2, "atypical_min": 3},
            "adult_male": {"typical_max": 3, "atypical_min": 4},
            "adult_female": {"typical_max": 5, "atypical_min": 6}
        }
    
    def calculate(self, epistaxis: int, cutaneous_bleeding: int, minor_wounds: int, 
                 oral_cavity: int, gi_bleeding: int, hematuria: int, tooth_extraction: int,
                 surgery: int, menorrhagia: int, postpartum_hemorrhage: int, 
                 muscle_hematomas: int, hemarthrosis: int, cns_bleeding: str, 
                 other_bleeding: int, age_group: str, gender: str) -> Dict[str, Any]:
        """
        Calculates the ISTH-SCC Bleeding Assessment score
        
        Args:
            epistaxis (int): Nosebleed score (0-4)
            cutaneous_bleeding (int): Skin bleeding score (0-4)
            minor_wounds (int): Minor wound bleeding score (0-4)
            oral_cavity (int): Oral cavity bleeding score (0-4)
            gi_bleeding (int): GI bleeding score (0-4)
            hematuria (int): Blood in urine score (0-4)
            tooth_extraction (int): Tooth extraction bleeding score (0-4)
            surgery (int): Surgical bleeding score (0-4)
            menorrhagia (int): Heavy menstrual bleeding score (0-4)
            postpartum_hemorrhage (int): Postpartum bleeding score (0-4)
            muscle_hematomas (int): Muscle bleeding score (0-4)
            hemarthrosis (int): Joint bleeding score (0-4)
            cns_bleeding (str): CNS bleeding category (never/subdural/intracerebral)
            other_bleeding (int): Other bleeding score (0-4)
            age_group (str): Age group (child/adult_male/adult_female)
            gender (str): Gender (male/female)
            
        Returns:
            Dict with the bleeding score and interpretation
        """
        
        # Validations
        self._validate_inputs(epistaxis, cutaneous_bleeding, minor_wounds, oral_cavity, 
                            gi_bleeding, hematuria, tooth_extraction, surgery, menorrhagia, 
                            postpartum_hemorrhage, muscle_hematomas, hemarthrosis, 
                            cns_bleeding, other_bleeding, age_group, gender)
        
        # Calculate total score
        total_score = self._calculate_total_score(
            epistaxis, cutaneous_bleeding, minor_wounds, oral_cavity, gi_bleeding, 
            hematuria, tooth_extraction, surgery, menorrhagia, postpartum_hemorrhage, 
            muscle_hematomas, hemarthrosis, cns_bleeding, other_bleeding
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, age_group, gender)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, epistaxis: int, cutaneous_bleeding: int, minor_wounds: int, 
                        oral_cavity: int, gi_bleeding: int, hematuria: int, tooth_extraction: int,
                        surgery: int, menorrhagia: int, postpartum_hemorrhage: int, 
                        muscle_hematomas: int, hemarthrosis: int, cns_bleeding: str, 
                        other_bleeding: int, age_group: str, gender: str):
        """Validates input parameters"""
        
        # Validate integer scores (0-4)
        integer_params = [
            ("epistaxis", epistaxis), ("cutaneous_bleeding", cutaneous_bleeding),
            ("minor_wounds", minor_wounds), ("oral_cavity", oral_cavity),
            ("gi_bleeding", gi_bleeding), ("hematuria", hematuria),
            ("tooth_extraction", tooth_extraction), ("surgery", surgery),
            ("menorrhagia", menorrhagia), ("postpartum_hemorrhage", postpartum_hemorrhage),
            ("muscle_hematomas", muscle_hematomas), ("hemarthrosis", hemarthrosis),
            ("other_bleeding", other_bleeding)
        ]
        
        for param_name, param_value in integer_params:
            if not isinstance(param_value, int) or param_value < 0 or param_value > 4:
                raise ValueError(f"{param_name} must be an integer between 0 and 4")
        
        # Validate CNS bleeding
        if cns_bleeding not in self.CNS_BLEEDING_SCORES:
            raise ValueError(f"cns_bleeding must be one of: {list(self.CNS_BLEEDING_SCORES.keys())}")
        
        # Validate age group
        if age_group not in self.THRESHOLDS:
            raise ValueError(f"age_group must be one of: {list(self.THRESHOLDS.keys())}")
        
        # Validate gender
        if gender not in ["male", "female"]:
            raise ValueError("gender must be either 'male' or 'female'")
    
    def _calculate_total_score(self, epistaxis: int, cutaneous_bleeding: int, minor_wounds: int, 
                             oral_cavity: int, gi_bleeding: int, hematuria: int, tooth_extraction: int,
                             surgery: int, menorrhagia: int, postpartum_hemorrhage: int, 
                             muscle_hematomas: int, hemarthrosis: int, cns_bleeding: str, 
                             other_bleeding: int) -> int:
        """
        Calculates the total ISTH-SCC bleeding assessment score
        
        Returns:
            int: Total score (0-55 points maximum)
        """
        
        # Sum all regular bleeding scores (0-4 each)
        regular_scores = (
            epistaxis + cutaneous_bleeding + minor_wounds + oral_cavity + gi_bleeding + 
            hematuria + tooth_extraction + surgery + menorrhagia + postpartum_hemorrhage + 
            muscle_hematomas + hemarthrosis + other_bleeding
        )
        
        # Add CNS bleeding score (special scoring: 0/3/4)
        cns_score = self.CNS_BLEEDING_SCORES[cns_bleeding]
        
        total_score = regular_scores + cns_score
        
        return total_score
    
    def _get_interpretation(self, total_score: int, age_group: str, gender: str) -> Dict[str, str]:
        """
        Gets clinical interpretation based on total score and demographics
        
        Args:
            total_score (int): Total bleeding assessment score
            age_group (str): Age group for interpretation
            gender (str): Gender for additional context
            
        Returns:
            Dict with interpretation details
        """
        
        threshold_info = self.THRESHOLDS[age_group]
        typical_max = threshold_info["typical_max"]
        atypical_min = threshold_info["atypical_min"]
        
        if total_score <= typical_max:
            # Typical bleeding pattern
            if age_group == "child":
                return {
                    "stage": "Child - Typical",
                    "description": "Typical bleeding pattern for children",
                    "interpretation": f"Score {total_score} points for children <18 years: Typical bleeding pattern. Low likelihood of inherited bleeding disorder. This score falls within the normal range for pediatric patients. Consider clinical context including family history of bleeding disorders. No immediate hematologic evaluation required unless strong clinical suspicion based on severity of individual bleeding episodes or positive family history."
                }
            elif age_group == "adult_male":
                return {
                    "stage": "Adult Male - Typical",
                    "description": "Typical bleeding pattern for adult males",
                    "interpretation": f"Score {total_score} points for adult males: Typical bleeding pattern. Low likelihood of inherited bleeding disorder. This score falls within the normal range for adult males. Consider clinical context including family history and severity of individual bleeding episodes. Routine hematologic screening is not indicated unless there are specific clinical concerns or positive family history."
                }
            else:  # adult_female
                return {
                    "stage": "Adult Female - Typical",
                    "description": "Typical bleeding pattern for adult females",
                    "interpretation": f"Score {total_score} points for adult females: Typical bleeding pattern. Low likelihood of inherited bleeding disorder. This score falls within the normal range for adult females, accounting for menstrual and reproductive bleeding. Consider clinical context including family history and severity of bleeding episodes. Routine hematologic evaluation is not indicated unless specific clinical concerns arise."
                }
        else:
            # Atypical bleeding pattern
            if age_group == "child":
                return {
                    "stage": "Child - Atypical",
                    "description": "Atypical bleeding pattern for children",
                    "interpretation": f"Score {total_score} points for children <18 years: Atypical bleeding pattern. Increased likelihood of inherited bleeding disorder. This score exceeds the typical range for pediatric patients (≥{atypical_min} points). Recommend hematologic evaluation including complete blood count with platelet count, PT/PTT, and consideration for von Willebrand disease studies and platelet function testing. Obtain detailed family history and assess individual bleeding episode severity."
                }
            elif age_group == "adult_male":
                return {
                    "stage": "Adult Male - Atypical",
                    "description": "Atypical bleeding pattern for adult males",
                    "interpretation": f"Score {total_score} points for adult males: Atypical bleeding pattern. Increased likelihood of inherited bleeding disorder. This score exceeds the typical range for adult males (≥{atypical_min} points). Recommend comprehensive hematologic evaluation including complete blood count, coagulation studies (PT/PTT), von Willebrand disease panel, and platelet function studies. Consider factor deficiencies and inherited platelet disorders based on bleeding pattern."
                }
            else:  # adult_female
                return {
                    "stage": "Adult Female - Atypical",
                    "description": "Atypical bleeding pattern for adult females",
                    "interpretation": f"Score {total_score} points for adult females: Atypical bleeding pattern. Increased likelihood of inherited bleeding disorder. This score exceeds the typical range for adult females (≥{atypical_min} points). Recommend hematologic evaluation including von Willebrand disease studies and platelet function testing, particularly given the higher prevalence of bleeding disorders in women with menorrhagia. Consider comprehensive coagulation panel and detailed gynecologic history."
                }


def calculate_isth_scc_bleeding_assessment_tool(epistaxis: int, cutaneous_bleeding: int, minor_wounds: int, 
                                               oral_cavity: int, gi_bleeding: int, hematuria: int, 
                                               tooth_extraction: int, surgery: int, menorrhagia: int, 
                                               postpartum_hemorrhage: int, muscle_hematomas: int, 
                                               hemarthrosis: int, cns_bleeding: str, other_bleeding: int, 
                                               age_group: str, gender: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_isth_scc_bleeding_assessment_tool pattern
    """
    calculator = IsthSccBleedingAssessmentToolCalculator()
    return calculator.calculate(epistaxis, cutaneous_bleeding, minor_wounds, oral_cavity, 
                               gi_bleeding, hematuria, tooth_extraction, surgery, menorrhagia, 
                               postpartum_hemorrhage, muscle_hematomas, hemarthrosis, 
                               cns_bleeding, other_bleeding, age_group, gender)