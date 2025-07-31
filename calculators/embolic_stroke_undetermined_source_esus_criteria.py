"""
Embolic Stroke of Undetermined Source (ESUS) Criteria Calculator

Diagnostic criteria for identifying embolic stroke of undetermined source after 
comprehensive evaluation excluding other specific stroke etiologies.

References:
1. Hart RG, Diener HC, Coutts SB, Easton JD, Granger CB, O'Donnell MJ, et al. Embolic 
   strokes of undetermined source: the case for a new clinical construct. Lancet Neurol. 
   2014;13(4):429-38. doi: 10.1016/S1474-4422(13)70310-7.
2. Adams HP Jr, Bendixen BH, Kappelle LJ, Biller J, Love BB, Gordon DL, et al. 
   Classification of subtype of acute ischemic stroke. Definitions for use in a multicenter 
   clinical trial. TOAST. Trial of Org 10172 in Acute Stroke Treatment. Stroke. 1993;24(1):35-41.
"""

from typing import Dict, Any


class EmbolicStrokeUndeterminedSourceEsusCriteriaCalculator:
    """Calculator for Embolic Stroke of Undetermined Source (ESUS) Criteria"""
    
    def __init__(self):
        # ESUS diagnostic criteria requirements
        self.CLINICAL_CRITERIA = {
            'stroke_type_non_lacunar': {
                'description': 'Non-lacunar stroke detected by CT or MRI',
                'requirement': 'Yes'
            },
            'no_significant_atherosclerosis': {
                'description': 'Absence of ≥50% luminal stenosis in arteries supplying ischemic area',
                'requirement': 'Yes'
            },
            'no_major_cardioembolic_source': {
                'description': 'No major cardioembolic sources identified',
                'requirement': 'Yes'
            },
            'no_other_specific_cause': {
                'description': 'No other specific cause of stroke identified',
                'requirement': 'Yes'
            }
        }
        
        self.DIAGNOSTIC_EVALUATION_CRITERIA = {
            'adequate_cardiac_monitoring': {
                'description': 'Cardiac rhythm monitoring ≥24 hours with automated rhythm detection',
                'requirement': 'Yes'
            },
            'adequate_vascular_imaging': {
                'description': 'Adequate vascular imaging completed',
                'requirement': 'Yes'
            },
            'adequate_cardiac_imaging': {
                'description': 'Adequate cardiac imaging completed',
                'requirement': 'Yes'
            }
        }
    
    def calculate(self, stroke_type_non_lacunar: str, no_significant_atherosclerosis: str,
                  no_major_cardioembolic_source: str, no_other_specific_cause: str,
                  adequate_cardiac_monitoring: str, adequate_vascular_imaging: str,
                  adequate_cardiac_imaging: str) -> Dict[str, Any]:
        """
        Evaluates ESUS diagnostic criteria using the provided parameters
        
        Args:
            stroke_type_non_lacunar (str): Non-lacunar stroke on imaging
            no_significant_atherosclerosis (str): No ≥50% stenosis in relevant arteries
            no_major_cardioembolic_source (str): No major cardioembolic sources
            no_other_specific_cause (str): No other specific stroke causes
            adequate_cardiac_monitoring (str): ≥24h cardiac monitoring completed
            adequate_vascular_imaging (str): Adequate vascular imaging completed
            adequate_cardiac_imaging (str): Adequate cardiac imaging completed
            
        Returns:
            Dict with the diagnostic result and interpretation
        """
        
        # Map parameters for easier processing
        clinical_parameters = {
            'stroke_type_non_lacunar': stroke_type_non_lacunar,
            'no_significant_atherosclerosis': no_significant_atherosclerosis,
            'no_major_cardioembolic_source': no_major_cardioembolic_source,
            'no_other_specific_cause': no_other_specific_cause
        }
        
        diagnostic_parameters = {
            'adequate_cardiac_monitoring': adequate_cardiac_monitoring,
            'adequate_vascular_imaging': adequate_vascular_imaging,
            'adequate_cardiac_imaging': adequate_cardiac_imaging
        }
        
        all_parameters = {**clinical_parameters, **diagnostic_parameters}
        
        # Validate inputs
        self._validate_inputs(all_parameters)
        
        # Evaluate criteria
        diagnosis_result = self._evaluate_esus_criteria(clinical_parameters, diagnostic_parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_result, clinical_parameters, diagnostic_parameters)
        
        return {
            "result": diagnosis_result["diagnosis"],
            "unit": None,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            # Check if value is valid (Yes or No)
            if value not in ["Yes", "No"]:
                raise ValueError(f"Parameter '{param_name}' must be 'Yes' or 'No', got '{value}'")
    
    def _evaluate_esus_criteria(self, clinical_parameters: Dict[str, str], 
                               diagnostic_parameters: Dict[str, str]) -> Dict[str, Any]:
        """Evaluates ESUS diagnostic criteria"""
        
        # Check clinical criteria
        clinical_criteria_met = []
        clinical_criteria_failed = []
        
        for param_name, value in clinical_parameters.items():
            required_value = self.CLINICAL_CRITERIA[param_name]['requirement']
            if value == required_value:
                clinical_criteria_met.append(param_name)
            else:
                clinical_criteria_failed.append(param_name)
        
        # Check diagnostic evaluation completeness
        diagnostic_evaluation_complete = []
        diagnostic_evaluation_incomplete = []
        
        for param_name, value in diagnostic_parameters.items():
            required_value = self.DIAGNOSTIC_EVALUATION_CRITERIA[param_name]['requirement']
            if value == required_value:
                diagnostic_evaluation_complete.append(param_name)
            else:
                diagnostic_evaluation_incomplete.append(param_name)
        
        # Determine overall diagnosis
        all_clinical_criteria_met = len(clinical_criteria_failed) == 0
        adequate_evaluation_completed = len(diagnostic_evaluation_incomplete) == 0
        
        if not adequate_evaluation_completed:
            diagnosis = "Inadequate Evaluation"
        elif all_clinical_criteria_met:
            diagnosis = "ESUS Diagnosis Confirmed"
        else:
            diagnosis = "ESUS Diagnosis Not Met"
        
        return {
            "diagnosis": diagnosis,
            "clinical_criteria_met": clinical_criteria_met,
            "clinical_criteria_failed": clinical_criteria_failed,
            "diagnostic_evaluation_complete": diagnostic_evaluation_complete,
            "diagnostic_evaluation_incomplete": diagnostic_evaluation_incomplete,
            "all_clinical_criteria_met": all_clinical_criteria_met,
            "adequate_evaluation_completed": adequate_evaluation_completed
        }
    
    def _get_interpretation(self, diagnosis_result: Dict[str, Any], 
                           clinical_parameters: Dict[str, str],
                           diagnostic_parameters: Dict[str, str]) -> Dict[str, str]:
        """
        Determines the interpretation based on the diagnostic evaluation
        
        Args:
            diagnosis_result (Dict): Results of ESUS criteria evaluation
            clinical_parameters (Dict): Clinical criteria parameters
            diagnostic_parameters (Dict): Diagnostic evaluation parameters
            
        Returns:
            Dict with interpretation details
        """
        
        diagnosis = diagnosis_result["diagnosis"]
        
        # Base interpretations
        if diagnosis == "ESUS Diagnosis Confirmed":
            stage = "ESUS Diagnosis Confirmed"
            description = "Meets all ESUS criteria"
            base_interpretation = (
                "Patient meets all diagnostic criteria for Embolic Stroke of Undetermined Source (ESUS). "
                "This diagnosis applies when all four clinical criteria are satisfied AND adequate diagnostic "
                "evaluation has been completed. Consider anticoagulation strategies, extended cardiac monitoring, "
                "and targeted embolic source investigation. Patient may be eligible for ESUS-specific clinical "
                "trials and treatment protocols."
            )
        elif diagnosis == "Inadequate Evaluation":
            stage = "Inadequate Evaluation"
            description = "Insufficient diagnostic workup"
            base_interpretation = (
                "Diagnostic evaluation is inadequate to determine ESUS status. Complete the minimum required "
                "diagnostic evaluation including: ≥24-hour cardiac monitoring with automated rhythm detection, "
                "comprehensive vascular imaging of extracranial and intracranial arteries, and adequate cardiac "
                "imaging (TTE and/or TEE). Reassess ESUS criteria after completing appropriate diagnostic workup."
            )
        else:  # ESUS Diagnosis Not Met
            stage = "ESUS Diagnosis Not Met"
            description = "Does not meet ESUS criteria"
            base_interpretation = (
                "Patient does not meet diagnostic criteria for Embolic Stroke of Undetermined Source (ESUS). "
                "Either clinical criteria are not fulfilled or adequate diagnostic evaluation is incomplete. "
                "Complete recommended diagnostic evaluation and identify specific stroke etiology. Consider "
                "alternative stroke classifications such as large artery atherosclerosis, cardioembolic stroke, "
                "small vessel disease, or other determined etiology."
            )
        
        # Add specific details about failed criteria
        interpretation_text = base_interpretation
        
        if diagnosis_result["clinical_criteria_failed"]:
            failed_criteria = []
            for param_name in diagnosis_result["clinical_criteria_failed"]:
                criteria_description = self.CLINICAL_CRITERIA[param_name]['description']
                failed_criteria.append(criteria_description.lower())
            
            interpretation_text += f" Clinical criteria not met: {'; '.join(failed_criteria)}."
        
        if diagnosis_result["diagnostic_evaluation_incomplete"]:
            incomplete_evaluations = []
            for param_name in diagnosis_result["diagnostic_evaluation_incomplete"]:
                eval_description = self.DIAGNOSTIC_EVALUATION_CRITERIA[param_name]['description']
                incomplete_evaluations.append(eval_description.lower())
            
            interpretation_text += f" Incomplete diagnostic evaluations: {'; '.join(incomplete_evaluations)}."
        
        # Add clinical management guidance
        if diagnosis == "ESUS Diagnosis Confirmed":
            interpretation_text += (
                " Recommended next steps: Consider extended cardiac monitoring (>24-48 hours), "
                "evaluation for patent foramen ovale, assessment for hypercoagulable states, and "
                "discussion of anticoagulation vs antiplatelet therapy. Monitor for clinical trial "
                "eligibility and emerging treatment options."
            )
        elif diagnosis == "Inadequate Evaluation":
            interpretation_text += (
                " Priority actions: Complete missing diagnostic evaluations before determining stroke "
                "subtype. Ensure comprehensive vascular imaging includes both extracranial and intracranial "
                "circulation. Consider extended cardiac monitoring if initial monitoring was borderline adequate."
            )
        else:
            interpretation_text += (
                " Next steps: Identify specific stroke etiology based on positive findings. Apply appropriate "
                "TOAST classification. Initiate etiology-specific secondary prevention strategies. Consider "
                "additional targeted investigations based on clinical presentation and initial findings."
            )
        
        # Add general clinical considerations
        interpretation_text += (
            " Important considerations: ESUS diagnosis requires rigorous exclusion of other stroke etiologies. "
            "The classification may change with additional testing or emerging diagnostic techniques. "
            "Regular reassessment is recommended as new information becomes available."
        )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation_text
        }


def calculate_embolic_stroke_undetermined_source_esus_criteria(
    stroke_type_non_lacunar: str, no_significant_atherosclerosis: str,
    no_major_cardioembolic_source: str, no_other_specific_cause: str,
    adequate_cardiac_monitoring: str, adequate_vascular_imaging: str,
    adequate_cardiac_imaging: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_embolic_stroke_undetermined_source_esus_criteria pattern
    """
    calculator = EmbolicStrokeUndeterminedSourceEsusCriteriaCalculator()
    return calculator.calculate(
        stroke_type_non_lacunar, no_significant_atherosclerosis,
        no_major_cardioembolic_source, no_other_specific_cause,
        adequate_cardiac_monitoring, adequate_vascular_imaging,
        adequate_cardiac_imaging
    )