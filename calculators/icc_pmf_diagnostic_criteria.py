"""
International Consensus Classification (ICC) Diagnostic Criteria for Primary Myelofibrosis (PMF) Calculator

Diagnoses primary myelofibrosis according to the International Consensus Classification (ICC) 
criteria using morphological, genetic, and clinical parameters.

References (Vancouver style):
1. Arber DA, Orazi A, Hasserjian RP, Borowitz MJ, Calvo KR, Kvasnicka HM, et al. International 
   Consensus Classification of Myeloid Neoplasms and Acute Leukemias: integrating morphologic, 
   clinical, and genomic data. Blood. 2022 Sep 15;140(11):1200-1228. doi: 10.1182/blood.2022015850.
2. Tefferi A, Guglielmelli P, Larson DR, Finke C, Wassie EA, Pieri L, et al. Long-term survival 
   and blast transformation in molecularly annotated essential thrombocythemia, polycythemia vera, 
   and myelofibrosis. Blood. 2014 Oct 16;124(16):2507-13. doi: 10.1182/blood-2014-05-579136.
3. Barbui T, Thiele J, Gisslinger H, Kvasnicka HM, Vannucchi AM, Guglielmelli P, et al. The 2016 
   WHO classification and diagnostic criteria for myeloproliferative neoplasms: document summary 
   and in-depth discussion. Blood Cancer J. 2018 Feb 15;8(2):15. doi: 10.1038/s41408-018-0054-y.
"""

from typing import Dict, Any


class IccPmfDiagnosticCriteriaCalculator:
    """Calculator for ICC Diagnostic Criteria for Primary Myelofibrosis"""
    
    def __init__(self):
        pass
    
    def calculate(self, bone_marrow_megakaryocytic_proliferation: str, bone_marrow_fibrosis_grade: str,
                  genetic_mutation_present: str, reactive_fibrosis_excluded: str, other_mpn_excluded: str,
                  anemia_present: str, leukocytosis_present: str, splenomegaly_present: str,
                  elevated_ldh: str) -> Dict[str, Any]:
        """
        Diagnoses PMF using ICC criteria
        
        Args:
            bone_marrow_megakaryocytic_proliferation (str): Megakaryocytic proliferation present ("present" or "absent")
            bone_marrow_fibrosis_grade (str): Fibrosis grade ("grade_0_1" or "grade_2_3")
            genetic_mutation_present (str): JAK2/CALR/MPL or clonal marker ("yes" or "no")
            reactive_fibrosis_excluded (str): Reactive causes excluded ("yes" or "no")
            other_mpn_excluded (str): Other MPNs excluded ("yes" or "no")
            anemia_present (str): Non-comorbid anemia present ("yes" or "no")
            leukocytosis_present (str): Leukocytosis ≥11×10^9/L ("yes" or "no")
            splenomegaly_present (str): Palpable splenomegaly ("yes" or "no")
            elevated_ldh (str): LDH above reference range ("yes" or "no")
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bone_marrow_megakaryocytic_proliferation, bone_marrow_fibrosis_grade,
                            genetic_mutation_present, reactive_fibrosis_excluded, other_mpn_excluded,
                            anemia_present, leukocytosis_present, splenomegaly_present, elevated_ldh)
        
        # Evaluate major criteria
        major_criteria_met = self._evaluate_major_criteria(
            bone_marrow_megakaryocytic_proliferation, genetic_mutation_present,
            reactive_fibrosis_excluded, other_mpn_excluded
        )
        
        # Evaluate minor criteria
        minor_criteria_count = self._count_minor_criteria(
            anemia_present, leukocytosis_present, splenomegaly_present, elevated_ldh
        )
        
        # Determine diagnosis
        diagnosis_result = self._determine_diagnosis(
            major_criteria_met, minor_criteria_count, bone_marrow_fibrosis_grade
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_result)
        
        return {
            "result": diagnosis_result,
            "unit": None,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bone_marrow_megakaryocytic_proliferation: str, bone_marrow_fibrosis_grade: str,
                        genetic_mutation_present: str, reactive_fibrosis_excluded: str, other_mpn_excluded: str,
                        anemia_present: str, leukocytosis_present: str, splenomegaly_present: str, elevated_ldh: str):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_present_absent = ["present", "absent"]
        valid_fibrosis_grades = ["grade_0_1", "grade_2_3"]
        
        # Validate megakaryocytic proliferation
        if bone_marrow_megakaryocytic_proliferation not in valid_present_absent:
            raise ValueError("Bone marrow megakaryocytic proliferation must be 'present' or 'absent'")
        
        # Validate fibrosis grade
        if bone_marrow_fibrosis_grade not in valid_fibrosis_grades:
            raise ValueError("Bone marrow fibrosis grade must be 'grade_0_1' or 'grade_2_3'")
        
        # Validate genetic mutation
        if genetic_mutation_present not in valid_yes_no:
            raise ValueError("Genetic mutation present must be 'yes' or 'no'")
        
        # Validate reactive fibrosis excluded
        if reactive_fibrosis_excluded not in valid_yes_no:
            raise ValueError("Reactive fibrosis excluded must be 'yes' or 'no'")
        
        # Validate other MPN excluded
        if other_mpn_excluded not in valid_yes_no:
            raise ValueError("Other MPN excluded must be 'yes' or 'no'")
        
        # Validate minor criteria
        if anemia_present not in valid_yes_no:
            raise ValueError("Anemia present must be 'yes' or 'no'")
        
        if leukocytosis_present not in valid_yes_no:
            raise ValueError("Leukocytosis present must be 'yes' or 'no'")
        
        if splenomegaly_present not in valid_yes_no:
            raise ValueError("Splenomegaly present must be 'yes' or 'no'")
        
        if elevated_ldh not in valid_yes_no:
            raise ValueError("Elevated LDH must be 'yes' or 'no'")
    
    def _evaluate_major_criteria(self, bone_marrow_megakaryocytic_proliferation: str,
                               genetic_mutation_present: str, reactive_fibrosis_excluded: str,
                               other_mpn_excluded: str) -> bool:
        """Evaluates if all major criteria are met"""
        
        # Major criterion 1: Megakaryocytic proliferation present
        criterion_1 = bone_marrow_megakaryocytic_proliferation == "present"
        
        # Major criterion 2: Genetic clonality (JAK2/CALR/MPL or other clonal marker)
        criterion_2 = genetic_mutation_present == "yes"
        
        # Major criterion 3: Reactive fibrosis excluded AND other MPNs excluded
        criterion_3 = reactive_fibrosis_excluded == "yes" and other_mpn_excluded == "yes"
        
        # All major criteria must be met
        return criterion_1 and criterion_2 and criterion_3
    
    def _count_minor_criteria(self, anemia_present: str, leukocytosis_present: str,
                            splenomegaly_present: str, elevated_ldh: str) -> int:
        """Counts the number of minor criteria present"""
        
        count = 0
        
        if anemia_present == "yes":
            count += 1
        
        if leukocytosis_present == "yes":
            count += 1
        
        if splenomegaly_present == "yes":
            count += 1
        
        if elevated_ldh == "yes":
            count += 1
        
        return count
    
    def _determine_diagnosis(self, major_criteria_met: bool, minor_criteria_count: int,
                           bone_marrow_fibrosis_grade: str) -> str:
        """Determines the diagnostic result"""
        
        # PMF diagnosis requires all major criteria + at least 1 minor criterion
        if major_criteria_met and minor_criteria_count >= 1:
            # Determine stage based on fibrosis grade
            if bone_marrow_fibrosis_grade == "grade_0_1":
                return "Pre-PMF Diagnosed"
            else:  # grade_2_3
                return "Overt PMF Diagnosed"
        else:
            return "PMF Not Diagnosed"
    
    def _get_interpretation(self, diagnosis_result: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the diagnostic result
        
        Args:
            diagnosis_result (str): Diagnostic result
            
        Returns:
            Dict with diagnostic interpretation and recommendations
        """
        
        if diagnosis_result == "Pre-PMF Diagnosed":
            return {
                "stage": "Pre-PMF Diagnosed",
                "description": "Prefibrotic Primary Myelofibrosis",
                "interpretation": "Diagnosis of prefibrotic (early) primary myelofibrosis established. Early stage with megakaryocytic proliferation but minimal fibrosis (grade 0-1). Requires close hematologic monitoring and staging workup. Consider risk stratification with prognostic scoring systems (IPSS-R, GIPSS). Regular surveillance for disease progression to overt fibrotic stage. Discuss treatment options including observation, symptom management, or therapeutic intervention based on risk profile and symptoms."
            }
        elif diagnosis_result == "Overt PMF Diagnosed":
            return {
                "stage": "Overt PMF Diagnosed",
                "description": "Overt Fibrotic Primary Myelofibrosis",
                "interpretation": "Diagnosis of overt (fibrotic) primary myelofibrosis established. Advanced stage with significant bone marrow fibrosis (grade 2-3). Requires comprehensive staging evaluation and risk assessment. Consider prognostic scoring (DIPSS, DIPSS-Plus, MIPSS70). Evaluate for complications including cytopenias, extramedullary hematopoiesis, and constitutional symptoms. Discuss treatment options including JAK inhibitors, supportive care, or stem cell transplantation based on risk profile and patient factors."
            }
        else:  # PMF Not Diagnosed
            return {
                "stage": "PMF Not Diagnosed",
                "description": "Diagnostic Criteria Not Met",
                "interpretation": "Diagnostic criteria for primary myelofibrosis not satisfied. Consider alternative diagnoses including other myeloproliferative neoplasms, myelodysplastic syndromes, reactive bone marrow changes, or secondary myelofibrosis. Recommend comprehensive evaluation with additional testing as clinically indicated. Consider repeat bone marrow biopsy if clinical suspicion remains high. Ensure adequate genetic testing with high-sensitivity assays for JAK2, CALR, and MPL mutations."
            }


def calculate_icc_pmf_diagnostic_criteria(bone_marrow_megakaryocytic_proliferation: str, bone_marrow_fibrosis_grade: str,
                                        genetic_mutation_present: str, reactive_fibrosis_excluded: str, other_mpn_excluded: str,
                                        anemia_present: str, leukocytosis_present: str, splenomegaly_present: str,
                                        elevated_ldh: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Diagnoses primary myelofibrosis using ICC criteria based on morphological, 
    genetic, and clinical parameters.
    
    Args:
        bone_marrow_megakaryocytic_proliferation (str): Megakaryocytic proliferation
        bone_marrow_fibrosis_grade (str): Bone marrow fibrosis grade
        genetic_mutation_present (str): Genetic clonality present
        reactive_fibrosis_excluded (str): Reactive causes excluded
        other_mpn_excluded (str): Other MPNs excluded
        anemia_present (str): Non-comorbid anemia
        leukocytosis_present (str): Leukocytosis ≥11×10^9/L
        splenomegaly_present (str): Palpable splenomegaly
        elevated_ldh (str): LDH above reference range
        
    Returns:
        Dict with diagnostic result and clinical interpretation
    """
    calculator = IccPmfDiagnosticCriteriaCalculator()
    return calculator.calculate(bone_marrow_megakaryocytic_proliferation, bone_marrow_fibrosis_grade,
                              genetic_mutation_present, reactive_fibrosis_excluded, other_mpn_excluded,
                              anemia_present, leukocytosis_present, splenomegaly_present, elevated_ldh)