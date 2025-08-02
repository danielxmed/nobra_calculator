"""
Multiple Myeloma Diagnostic Criteria (IMWG) Calculator

Diagnoses multiple myeloma according to the International Myeloma Working Group 
(IMWG) criteria, including traditional CRAB criteria and newer SLiM biomarkers.

References:
1. Rajkumar SV, et al. Lancet Oncol. 2014;15(12):e538-48.
2. Kumar S, et al. Lancet Oncol. 2016;17(8):e328-e346.
3. Palumbo A, et al. J Clin Oncol. 2015;33(26):2863-9.
"""

from typing import Dict, Any


class MultipleMyelomaDiagnosticCriteriaCalculator:
    """Calculator for Multiple Myeloma Diagnostic Criteria (IMWG)"""
    
    def __init__(self):
        # IMWG diagnostic criteria components
        self.CLONAL_CRITERIA = ["clonal_plasma_cells_bone_marrow", "biopsy_proven_plasmacytoma"]
        self.CRAB_CRITERIA = ["hypercalcemia", "renal_insufficiency", "anemia", "bone_lesions"]
        self.SLIM_CRITERIA = ["plasma_cells_60_percent", "light_chain_ratio", "focal_mri_lesions"]
    
    def calculate(self, clonal_plasma_cells_bone_marrow: str, biopsy_proven_plasmacytoma: str,
                  hypercalcemia: str, renal_insufficiency: str, anemia: str, bone_lesions: str,
                  plasma_cells_60_percent: str, light_chain_ratio: str, 
                  focal_mri_lesions: str) -> Dict[str, Any]:
        """
        Evaluates multiple myeloma diagnostic criteria according to IMWG
        
        Args:
            clonal_plasma_cells_bone_marrow (str): Clonal bone marrow plasma cells ≥10%
            biopsy_proven_plasmacytoma (str): Biopsy-proven bony or extramedullary plasmacytoma
            hypercalcemia (str): Serum calcium >1 mg/dL above normal or >11 mg/dL
            renal_insufficiency (str): Creatinine clearance <40 mL/min or serum creatinine >2 mg/dL
            anemia (str): Hemoglobin >2 g/dL below normal or <10 g/dL
            bone_lesions (str): ≥1 osteolytic lesion on imaging
            plasma_cells_60_percent (str): Clonal bone marrow plasma cells ≥60%
            light_chain_ratio (str): Involved:uninvolved serum free light chain ratio ≥100
            focal_mri_lesions (str): >1 focal lesion on MRI
            
        Returns:
            Dict with diagnostic assessment and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(clonal_plasma_cells_bone_marrow, biopsy_proven_plasmacytoma,
                             hypercalcemia, renal_insufficiency, anemia, bone_lesions,
                             plasma_cells_60_percent, light_chain_ratio, focal_mri_lesions)
        
        # Evaluate diagnostic criteria
        diagnosis_result = self._evaluate_criteria(
            clonal_plasma_cells_bone_marrow, biopsy_proven_plasmacytoma,
            hypercalcemia, renal_insufficiency, anemia, bone_lesions,
            plasma_cells_60_percent, light_chain_ratio, focal_mri_lesions
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_result)
        
        return {
            "result": diagnosis_result["diagnosis"],
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, clonal_plasma_cells_bone_marrow: str, biopsy_proven_plasmacytoma: str,
                        hypercalcemia: str, renal_insufficiency: str, anemia: str, bone_lesions: str,
                        plasma_cells_60_percent: str, light_chain_ratio: str, focal_mri_lesions: str):
        """Validates input parameters"""
        
        parameters = {
            "clonal_plasma_cells_bone_marrow": clonal_plasma_cells_bone_marrow,
            "biopsy_proven_plasmacytoma": biopsy_proven_plasmacytoma,
            "hypercalcemia": hypercalcemia,
            "renal_insufficiency": renal_insufficiency,
            "anemia": anemia,
            "bone_lesions": bone_lesions,
            "plasma_cells_60_percent": plasma_cells_60_percent,
            "light_chain_ratio": light_chain_ratio,
            "focal_mri_lesions": focal_mri_lesions
        }
        
        for param_name, param_value in parameters.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _evaluate_criteria(self, clonal_plasma_cells_bone_marrow: str, biopsy_proven_plasmacytoma: str,
                          hypercalcemia: str, renal_insufficiency: str, anemia: str, bone_lesions: str,
                          plasma_cells_60_percent: str, light_chain_ratio: str, 
                          focal_mri_lesions: str) -> Dict[str, Any]:
        """Evaluates IMWG diagnostic criteria"""
        
        # Step 1: Check clonal plasma cell criteria (at least one must be present)
        clonal_criteria_met = (
            clonal_plasma_cells_bone_marrow == "yes" or 
            biopsy_proven_plasmacytoma == "yes"
        )
        
        # Step 2: Check myeloma defining events (at least one must be present)
        # CRAB criteria (traditional end-organ damage)
        crab_criteria_met = (
            hypercalcemia == "yes" or
            renal_insufficiency == "yes" or
            anemia == "yes" or
            bone_lesions == "yes"
        )
        
        # SLiM criteria (biomarkers of malignancy - 2014 update)
        slim_criteria_met = (
            plasma_cells_60_percent == "yes" or
            light_chain_ratio == "yes" or
            focal_mri_lesions == "yes"
        )
        
        # Overall myeloma defining events
        myeloma_defining_events = crab_criteria_met or slim_criteria_met
        
        # Final diagnosis: Both criteria must be met
        diagnosis_met = clonal_criteria_met and myeloma_defining_events
        
        # Detailed breakdown for interpretation
        criteria_details = {
            "clonal_criteria_met": clonal_criteria_met,
            "myeloma_defining_events": myeloma_defining_events,
            "crab_criteria_met": crab_criteria_met,
            "slim_criteria_met": slim_criteria_met,
            "clonal_plasma_cells_bone_marrow": clonal_plasma_cells_bone_marrow == "yes",
            "biopsy_proven_plasmacytoma": biopsy_proven_plasmacytoma == "yes",
            "hypercalcemia": hypercalcemia == "yes",
            "renal_insufficiency": renal_insufficiency == "yes",
            "anemia": anemia == "yes",
            "bone_lesions": bone_lesions == "yes",
            "plasma_cells_60_percent": plasma_cells_60_percent == "yes",
            "light_chain_ratio": light_chain_ratio == "yes",
            "focal_mri_lesions": focal_mri_lesions == "yes"
        }
        
        return {
            "diagnosis": "Multiple Myeloma" if diagnosis_met else "Not Diagnostic",
            "criteria_details": criteria_details
        }
    
    def _get_interpretation(self, diagnosis_result: Dict[str, Any]) -> Dict[str, str]:
        """
        Provides diagnostic interpretation based on IMWG criteria
        
        Args:
            diagnosis_result (Dict): Diagnostic evaluation results
            
        Returns:
            Dict with interpretation details
        """
        
        details = diagnosis_result["criteria_details"]
        diagnosis = diagnosis_result["diagnosis"]
        
        if diagnosis == "Multiple Myeloma":
            # Build detailed interpretation
            positive_criteria = []
            
            # Clonal criteria
            if details["clonal_plasma_cells_bone_marrow"]:
                positive_criteria.append("clonal bone marrow plasma cells ≥10%")
            if details["biopsy_proven_plasmacytoma"]:
                positive_criteria.append("biopsy-proven plasmacytoma")
            
            # CRAB criteria
            crab_found = []
            if details["hypercalcemia"]:
                crab_found.append("hypercalcemia")
            if details["renal_insufficiency"]:
                crab_found.append("renal insufficiency")
            if details["anemia"]:
                crab_found.append("anemia")
            if details["bone_lesions"]:
                crab_found.append("bone lesions")
            
            # SLiM criteria
            slim_found = []
            if details["plasma_cells_60_percent"]:
                slim_found.append("≥60% clonal plasma cells")
            if details["light_chain_ratio"]:
                slim_found.append("serum free light chain ratio ≥100")
            if details["focal_mri_lesions"]:
                slim_found.append(">1 focal MRI lesion")
            
            interpretation_parts = [
                f"DIAGNOSIS: Multiple myeloma according to IMWG criteria.",
                f"CLONAL EVIDENCE: {', '.join(positive_criteria)}."
            ]
            
            if crab_found:
                interpretation_parts.append(f"CRAB CRITERIA: {', '.join(crab_found)}.")
            
            if slim_found:
                interpretation_parts.append(f"SLiM BIOMARKERS: {', '.join(slim_found)}.")
            
            interpretation_parts.extend([
                "NEXT STEPS: Proceed with staging (ISS/R-ISS), cytogenetic analysis, and treatment planning.",
                "Consider bone marrow biopsy if not already performed, serum protein electrophoresis,",
                "immunofixation, serum free light chains, LDH, beta-2 microglobulin, and albumin.",
                "Imaging studies including whole-body MRI or PET-CT may be indicated.",
                "Multidisciplinary hematologic consultation is recommended for treatment planning.",
                "The patient requires immediate oncologic evaluation and staging workup."
            ])
            
            return {
                "stage": "Multiple Myeloma",
                "description": "Criteria met for multiple myeloma",
                "interpretation": " ".join(interpretation_parts)
            }
        
        else:
            # Diagnosis not met
            missing_criteria = []
            
            if not details["clonal_criteria_met"]:
                missing_criteria.append("clonal plasma cell evidence (need ≥10% clonal bone marrow plasma cells OR biopsy-proven plasmacytoma)")
            
            if not details["myeloma_defining_events"]:
                missing_criteria.append("myeloma defining events (need ≥1 CRAB criterion OR ≥1 SLiM biomarker)")
            
            interpretation_parts = [
                f"DIAGNOSIS: Does not meet IMWG criteria for multiple myeloma.",
                f"MISSING CRITERIA: {'; '.join(missing_criteria)}."
            ]
            
            # Suggest further evaluation
            if details["clonal_plasma_cells_bone_marrow"] or details["biopsy_proven_plasmacytoma"]:
                interpretation_parts.append("Consider evaluation for MGUS (monoclonal gammopathy of undetermined significance) or smoldering multiple myeloma.")
            
            interpretation_parts.extend([
                "RECOMMENDATIONS: Continue monitoring with serial laboratory studies.",
                "Consider repeat bone marrow biopsy if clinically indicated.",
                "Monitor for progression with regular SPEP, immunofixation, and serum free light chains.",
                "Annual follow-up or sooner if symptoms develop.",
                "Patient counseling regarding the nature of plasma cell disorders and monitoring plan."
            ])
            
            return {
                "stage": "Not Diagnostic",
                "description": "Criteria not met for multiple myeloma",
                "interpretation": " ".join(interpretation_parts)
            }


def calculate_multiple_myeloma_diagnostic_criteria(clonal_plasma_cells_bone_marrow: str, 
                                                   biopsy_proven_plasmacytoma: str,
                                                   hypercalcemia: str, renal_insufficiency: str, 
                                                   anemia: str, bone_lesions: str,
                                                   plasma_cells_60_percent: str, 
                                                   light_chain_ratio: str, 
                                                   focal_mri_lesions: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MultipleMyelomaDiagnosticCriteriaCalculator()
    return calculator.calculate(clonal_plasma_cells_bone_marrow, biopsy_proven_plasmacytoma,
                               hypercalcemia, renal_insufficiency, anemia, bone_lesions,
                               plasma_cells_60_percent, light_chain_ratio, focal_mri_lesions)