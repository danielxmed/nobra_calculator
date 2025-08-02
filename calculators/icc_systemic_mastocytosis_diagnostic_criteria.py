"""
International Consensus Classification (ICC) Diagnostic Criteria for Systemic Mastocytosis Calculator

Diagnoses systemic mastocytosis according to the International Consensus Classification (ICC) 
criteria using morphological, immunophenotypic, and molecular parameters.

References (Vancouver style):
1. Leguit RJ, van der Linden MP, Jansen JH, Hebeda KM, Lam KH, Leenders WP, et al. The international 
   consensus classification of mastocytosis and related entities. Virchows Arch. 2023 Jan;482(1):99-112. 
   doi: 10.1007/s00428-022-03454-6.
2. Arber DA, Orazi A, Hasserjian RP, Borowitz MJ, Calvo KR, Kvasnicka HM, et al. International 
   Consensus Classification of Myeloid Neoplasms and Acute Leukemias: integrating morphologic, 
   clinical, and genomic data. Blood. 2022 Sep 15;140(11):1200-1228. doi: 10.1182/blood.2022015850.
3. Valent P, Akin C, Bonadonna P, Hartmann K, Alvarez-Twose I, Brockow K, et al. Updated Diagnostic 
   Criteria and Classification of Mast Cell Disorders: A Consensus Proposal. HemaSphere. 2021 Oct 29;5(11):e646. 
   doi: 10.1097/HS9.0000000000000646.
"""

from typing import Dict, Any


class IccSystemicMastocytosisDiagnosticCriteriaCalculator:
    """Calculator for ICC Diagnostic Criteria for Systemic Mastocytosis"""
    
    def __init__(self):
        pass
    
    def calculate(self, multifocal_mast_cell_infiltrates: str, atypical_mast_cell_morphology: str,
                  aberrant_mast_cell_markers: str, kit_mutation_detected: str,
                  elevated_serum_tryptase: str) -> Dict[str, Any]:
        """
        Diagnoses systemic mastocytosis using ICC criteria
        
        Args:
            multifocal_mast_cell_infiltrates (str): Multifocal dense infiltrates ≥15 mast cells ("present" or "absent")
            atypical_mast_cell_morphology (str): >25% spindle-shaped or atypical morphology ("yes" or "no")
            aberrant_mast_cell_markers (str): CD25, CD2, or CD30 expression ("yes" or "no")
            kit_mutation_detected (str): KIT D816V or activating mutation ("yes" or "no")
            elevated_serum_tryptase (str): Persistently >20 ng/mL ("yes" or "no")
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(multifocal_mast_cell_infiltrates, atypical_mast_cell_morphology,
                            aberrant_mast_cell_markers, kit_mutation_detected, elevated_serum_tryptase)
        
        # Evaluate major criterion
        major_criterion_met = self._evaluate_major_criterion(multifocal_mast_cell_infiltrates)
        
        # Count minor criteria
        minor_criteria_count = self._count_minor_criteria(
            atypical_mast_cell_morphology, aberrant_mast_cell_markers,
            kit_mutation_detected, elevated_serum_tryptase
        )
        
        # Determine diagnosis
        diagnosis_result = self._determine_diagnosis(major_criterion_met, minor_criteria_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_result)
        
        return {
            "result": diagnosis_result,
            "unit": None,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, multifocal_mast_cell_infiltrates: str, atypical_mast_cell_morphology: str,
                        aberrant_mast_cell_markers: str, kit_mutation_detected: str, elevated_serum_tryptase: str):
        """Validates input parameters"""
        
        valid_present_absent = ["present", "absent"]
        valid_yes_no = ["yes", "no"]
        
        # Validate major criterion
        if multifocal_mast_cell_infiltrates not in valid_present_absent:
            raise ValueError("Multifocal mast cell infiltrates must be 'present' or 'absent'")
        
        # Validate minor criteria
        if atypical_mast_cell_morphology not in valid_yes_no:
            raise ValueError("Atypical mast cell morphology must be 'yes' or 'no'")
        
        if aberrant_mast_cell_markers not in valid_yes_no:
            raise ValueError("Aberrant mast cell markers must be 'yes' or 'no'")
        
        if kit_mutation_detected not in valid_yes_no:
            raise ValueError("KIT mutation detected must be 'yes' or 'no'")
        
        if elevated_serum_tryptase not in valid_yes_no:
            raise ValueError("Elevated serum tryptase must be 'yes' or 'no'")
    
    def _evaluate_major_criterion(self, multifocal_mast_cell_infiltrates: str) -> bool:
        """Evaluates if the major criterion is met"""
        
        # Major criterion: Multifocal dense infiltrates of ≥15 mast cells in aggregates
        return multifocal_mast_cell_infiltrates == "present"
    
    def _count_minor_criteria(self, atypical_mast_cell_morphology: str, aberrant_mast_cell_markers: str,
                            kit_mutation_detected: str, elevated_serum_tryptase: str) -> int:
        """Counts the number of minor criteria present"""
        
        count = 0
        
        # Minor criterion 1: Atypical morphology (>25% spindle-shaped or immature)
        if atypical_mast_cell_morphology == "yes":
            count += 1
        
        # Minor criterion 2: Aberrant markers (CD25, CD2, CD30)
        if aberrant_mast_cell_markers == "yes":
            count += 1
        
        # Minor criterion 3: KIT mutation (D816V or other activating)
        if kit_mutation_detected == "yes":
            count += 1
        
        # Minor criterion 4: Elevated serum tryptase (>20 ng/mL)
        if elevated_serum_tryptase == "yes":
            count += 1
        
        return count
    
    def _determine_diagnosis(self, major_criterion_met: bool, minor_criteria_count: int) -> str:
        """Determines the diagnostic result"""
        
        # SM diagnosis: Major criterion OR ≥3 minor criteria
        if major_criterion_met or minor_criteria_count >= 3:
            return "Systemic Mastocytosis Diagnosed"
        else:
            return "Systemic Mastocytosis Not Diagnosed"
    
    def _get_interpretation(self, diagnosis_result: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the diagnostic result
        
        Args:
            diagnosis_result (str): Diagnostic result
            
        Returns:
            Dict with diagnostic interpretation and recommendations
        """
        
        if diagnosis_result == "Systemic Mastocytosis Diagnosed":
            return {
                "stage": "Systemic Mastocytosis Diagnosed",
                "description": "ICC Criteria Met",
                "interpretation": "Diagnosis of systemic mastocytosis established according to ICC criteria. Requires comprehensive staging evaluation including bone marrow biopsy, imaging studies, and laboratory assessment. Consider subtype classification (ISM, SSM, ASM, MCL, SM-AMN) based on additional clinical and laboratory findings. Evaluate for organ dysfunction and associated symptoms including mediator-related symptoms, organomegaly, cytopenias, and osteoporosis. Discuss treatment options including symptom management with antihistamines and mast cell stabilizers, cytoreductive therapy, or targeted therapies (KIT inhibitors) based on subtype and severity."
            }
        else:  # Not Diagnosed
            return {
                "stage": "Systemic Mastocytosis Not Diagnosed",
                "description": "ICC Criteria Not Met",
                "interpretation": "ICC diagnostic criteria for systemic mastocytosis not satisfied. Consider alternative diagnoses including cutaneous mastocytosis, mast cell activation syndrome, reactive mastocytosis, or other hematologic malignancies. Recommend comprehensive evaluation with additional testing as clinically indicated including repeat bone marrow biopsy with adequate sampling, immunohistochemical staining for tryptase and CD117, flow cytometry for aberrant markers, and molecular testing with high-sensitivity assays for KIT mutations. Consider consultation with hematopathology expertise for morphological review."
            }


def calculate_icc_systemic_mastocytosis_diagnostic_criteria(multifocal_mast_cell_infiltrates: str, atypical_mast_cell_morphology: str,
                                                          aberrant_mast_cell_markers: str, kit_mutation_detected: str,
                                                          elevated_serum_tryptase: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Diagnoses systemic mastocytosis using ICC criteria based on morphological, 
    immunophenotypic, and molecular parameters.
    
    Args:
        multifocal_mast_cell_infiltrates (str): Multifocal dense infiltrates
        atypical_mast_cell_morphology (str): Atypical mast cell morphology
        aberrant_mast_cell_markers (str): Aberrant immunophenotype
        kit_mutation_detected (str): KIT mutation presence
        elevated_serum_tryptase (str): Elevated tryptase level
        
    Returns:
        Dict with diagnostic result and clinical interpretation
    """
    calculator = IccSystemicMastocytosisDiagnosticCriteriaCalculator()
    return calculator.calculate(multifocal_mast_cell_infiltrates, atypical_mast_cell_morphology,
                              aberrant_mast_cell_markers, kit_mutation_detected, elevated_serum_tryptase)