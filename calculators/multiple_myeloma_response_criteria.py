"""
Multiple Myeloma Response Criteria (IMWG) Calculator

Evaluates disease response in multiple myeloma according to International Myeloma 
Working Group (IMWG) criteria including Complete Response, Partial Response, and 
Progressive Disease categories.

References:
1. Kumar S, et al. Lancet Oncol. 2016;17(8):e328-e346.
2. Durie BG, et al. Leukemia. 2006;20(9):1467-73.
3. Rajkumar SV, et al. Blood. 2011;117(18):4691-5.
"""

from typing import Dict, Any, Optional


class MultipleMyelomaResponseCriteriaCalculator:
    """Calculator for Multiple Myeloma Response Criteria (IMWG)"""
    
    def __init__(self):
        # Normal free light chain ratio range
        self.NORMAL_FLC_RATIO_MIN = 0.26
        self.NORMAL_FLC_RATIO_MAX = 1.65
        
        # Response category thresholds
        self.VGPR_M_PROTEIN_REDUCTION = 90  # %
        self.PR_M_PROTEIN_REDUCTION = 50    # %
        self.VGPR_URINE_M_PROTEIN_MAX = 100 # mg/24h
        self.PR_URINE_M_PROTEIN_MAX = 200   # mg/24h
        self.PR_PLASMACYTOMA_REDUCTION = 50 # %
        self.CR_PLASMA_CELLS_MAX = 5        # %
    
    def calculate(self, serum_immunofixation: str, urine_immunofixation: str,
                  bone_marrow_plasma_cells: float, soft_tissue_plasmacytomas: str,
                  free_light_chain_ratio: Optional[float] = None,
                  clonal_cells_bone_marrow: Optional[str] = None,
                  serum_m_protein_reduction: Optional[float] = None,
                  urine_m_protein_24h: Optional[float] = None,
                  serum_electrophoresis_detectable: Optional[str] = None,
                  plasmacytoma_reduction: Optional[float] = None) -> Dict[str, Any]:
        """
        Evaluates multiple myeloma response according to IMWG criteria
        
        Args:
            serum_immunofixation (str): Serum immunofixation result
            urine_immunofixation (str): Urine immunofixation result
            bone_marrow_plasma_cells (float): Percentage of plasma cells in bone marrow
            soft_tissue_plasmacytomas (str): Presence of soft tissue plasmacytomas
            free_light_chain_ratio (Optional[float]): Serum free light chain ratio
            clonal_cells_bone_marrow (Optional[str]): Clonal cells presence
            serum_m_protein_reduction (Optional[float]): Serum M protein reduction %
            urine_m_protein_24h (Optional[float]): 24-hour urine M protein level
            serum_electrophoresis_detectable (Optional[str]): M component detectable by electrophoresis
            plasmacytoma_reduction (Optional[float]): Plasmacytoma size reduction %
            
        Returns:
            Dict with response category and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(serum_immunofixation, urine_immunofixation, 
                             bone_marrow_plasma_cells, soft_tissue_plasmacytomas,
                             free_light_chain_ratio, clonal_cells_bone_marrow,
                             serum_m_protein_reduction, urine_m_protein_24h,
                             serum_electrophoresis_detectable, plasmacytoma_reduction)
        
        # Determine response category
        response_result = self._evaluate_response(
            serum_immunofixation, urine_immunofixation, bone_marrow_plasma_cells,
            soft_tissue_plasmacytomas, free_light_chain_ratio, clonal_cells_bone_marrow,
            serum_m_protein_reduction, urine_m_protein_24h, serum_electrophoresis_detectable,
            plasmacytoma_reduction
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(response_result)
        
        return {
            "result": response_result["category"],
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, serum_immunofixation: str, urine_immunofixation: str,
                        bone_marrow_plasma_cells: float, soft_tissue_plasmacytomas: str,
                        free_light_chain_ratio: Optional[float] = None,
                        clonal_cells_bone_marrow: Optional[str] = None,
                        serum_m_protein_reduction: Optional[float] = None,
                        urine_m_protein_24h: Optional[float] = None,
                        serum_electrophoresis_detectable: Optional[str] = None,
                        plasmacytoma_reduction: Optional[float] = None):
        """Validates input parameters"""
        
        if serum_immunofixation not in ["negative", "positive"]:
            raise ValueError("Serum immunofixation must be 'negative' or 'positive'")
        
        if urine_immunofixation not in ["negative", "positive"]:
            raise ValueError("Urine immunofixation must be 'negative' or 'positive'")
        
        if not isinstance(bone_marrow_plasma_cells, (int, float)) or bone_marrow_plasma_cells < 0 or bone_marrow_plasma_cells > 100:
            raise ValueError("Bone marrow plasma cells must be between 0 and 100%")
        
        if soft_tissue_plasmacytomas not in ["absent", "present"]:
            raise ValueError("Soft tissue plasmacytomas must be 'absent' or 'present'")
        
        if free_light_chain_ratio is not None:
            if not isinstance(free_light_chain_ratio, (int, float)) or free_light_chain_ratio <= 0:
                raise ValueError("Free light chain ratio must be a positive number")
        
        if clonal_cells_bone_marrow is not None and clonal_cells_bone_marrow not in ["absent", "present"]:
            raise ValueError("Clonal cells bone marrow must be 'absent' or 'present'")
        
        if serum_m_protein_reduction is not None:
            if not isinstance(serum_m_protein_reduction, (int, float)) or serum_m_protein_reduction < 0 or serum_m_protein_reduction > 100:
                raise ValueError("Serum M protein reduction must be between 0 and 100%")
        
        if urine_m_protein_24h is not None:
            if not isinstance(urine_m_protein_24h, (int, float)) or urine_m_protein_24h < 0:
                raise ValueError("Urine M protein 24h must be a non-negative number")
        
        if serum_electrophoresis_detectable is not None and serum_electrophoresis_detectable not in ["yes", "no"]:
            raise ValueError("Serum electrophoresis detectable must be 'yes' or 'no'")
        
        if plasmacytoma_reduction is not None:
            if not isinstance(plasmacytoma_reduction, (int, float)) or plasmacytoma_reduction < 0 or plasmacytoma_reduction > 100:
                raise ValueError("Plasmacytoma reduction must be between 0 and 100%")
    
    def _evaluate_response(self, serum_immunofixation: str, urine_immunofixation: str,
                          bone_marrow_plasma_cells: float, soft_tissue_plasmacytomas: str,
                          free_light_chain_ratio: Optional[float] = None,
                          clonal_cells_bone_marrow: Optional[str] = None,
                          serum_m_protein_reduction: Optional[float] = None,
                          urine_m_protein_24h: Optional[float] = None,
                          serum_electrophoresis_detectable: Optional[str] = None,
                          plasmacytoma_reduction: Optional[float] = None) -> Dict[str, Any]:
        """Evaluates response category based on IMWG criteria"""
        
        # Check for Complete Response criteria first
        cr_criteria = (
            serum_immunofixation == "negative" and
            urine_immunofixation == "negative" and
            bone_marrow_plasma_cells < self.CR_PLASMA_CELLS_MAX and
            soft_tissue_plasmacytomas == "absent"
        )
        
        if cr_criteria:
            # Check for Stringent Complete Response
            if (free_light_chain_ratio is not None and 
                clonal_cells_bone_marrow is not None and
                self.NORMAL_FLC_RATIO_MIN <= free_light_chain_ratio <= self.NORMAL_FLC_RATIO_MAX and
                clonal_cells_bone_marrow == "absent"):
                return {
                    "category": "Stringent Complete Response (sCR)",
                    "details": {
                        "meets_cr": True,
                        "normal_flc_ratio": True,
                        "no_clonal_cells": True
                    }
                }
            else:
                return {
                    "category": "Complete Response (CR)",
                    "details": {
                        "meets_cr": True,
                        "negative_immunofixation": True,
                        "low_plasma_cells": True,
                        "no_plasmacytomas": True
                    }
                }
        
        # Check for Very Good Partial Response (VGPR)
        vgpr_by_immunofixation = (
            serum_immunofixation == "positive" and
            urine_immunofixation == "positive" and
            serum_electrophoresis_detectable == "no"
        )
        
        vgpr_by_reduction = (
            serum_m_protein_reduction is not None and
            urine_m_protein_24h is not None and
            serum_m_protein_reduction >= self.VGPR_M_PROTEIN_REDUCTION and
            urine_m_protein_24h < self.VGPR_URINE_M_PROTEIN_MAX
        )
        
        if vgpr_by_immunofixation or vgpr_by_reduction:
            return {
                "category": "Very Good Partial Response (VGPR)",
                "details": {
                    "immunofixation_positive": vgpr_by_immunofixation,
                    "electrophoresis_negative": serum_electrophoresis_detectable == "no" if serum_electrophoresis_detectable else None,
                    "m_protein_reduction_90": vgpr_by_reduction,
                    "low_urine_m_protein": urine_m_protein_24h < self.VGPR_URINE_M_PROTEIN_MAX if urine_m_protein_24h else None
                }
            }
        
        # Check for Partial Response (PR)
        pr_serum = serum_m_protein_reduction is not None and serum_m_protein_reduction >= self.PR_M_PROTEIN_REDUCTION
        pr_urine = urine_m_protein_24h is not None and urine_m_protein_24h < self.PR_URINE_M_PROTEIN_MAX
        pr_plasmacytoma = (soft_tissue_plasmacytomas == "absent" or 
                          (plasmacytoma_reduction is not None and plasmacytoma_reduction >= self.PR_PLASMACYTOMA_REDUCTION))
        
        if pr_serum and (pr_urine or urine_m_protein_24h is None) and pr_plasmacytoma:
            return {
                "category": "Partial Response (PR)",
                "details": {
                    "serum_reduction_50": pr_serum,
                    "urine_criteria_met": pr_urine or urine_m_protein_24h is None,
                    "plasmacytoma_criteria_met": pr_plasmacytoma
                }
            }
        
        # If none of the above, determine between Stable Disease and Progressive Disease
        # For this implementation, we'll default to Stable Disease
        # Progressive Disease would require additional criteria like increases from baseline
        return {
            "category": "Stable Disease (SD)",
            "details": {
                "no_cr_criteria": not cr_criteria,
                "no_vgpr_criteria": not (vgpr_by_immunofixation or vgpr_by_reduction),
                "no_pr_criteria": not (pr_serum and pr_urine and pr_plasmacytoma)
            }
        }
    
    def _get_interpretation(self, response_result: Dict[str, Any]) -> Dict[str, str]:
        """
        Provides clinical interpretation based on response category
        
        Args:
            response_result (Dict): Response evaluation results
            
        Returns:
            Dict with interpretation details
        """
        
        category = response_result["category"]
        details = response_result["details"]
        
        if category == "Stringent Complete Response (sCR)":
            return {
                "stage": "Stringent Complete Response (sCR)",
                "description": "Best possible response",
                "interpretation": (
                    f"STRINGENT COMPLETE RESPONSE (sCR): The patient has achieved the highest level of response "
                    f"to multiple myeloma treatment. "
                    f"CRITERIA MET: Negative serum and urine immunofixation, <5% bone marrow plasma cells, "
                    f"absence of soft tissue plasmacytomas, normal free light chain ratio (0.26-1.65), and "
                    f"absence of clonal cells in bone marrow by immunohistochemistry/immunofluorescence. "
                    f"CLINICAL SIGNIFICANCE: This represents the deepest possible remission with undetectable "
                    f"disease by all available methods. Patients achieving sCR typically have the best "
                    f"long-term outcomes and lowest risk of relapse. "
                    f"MANAGEMENT: Continue current treatment regimen if on maintenance therapy. Monitor with "
                    f"regular laboratory assessments every 3-6 months. Consider minimal residual disease (MRD) "
                    f"testing if available. Discuss long-term prognosis and surveillance plan. "
                    f"FOLLOW-UP: Regular monitoring with serum protein electrophoresis, immunofixation, "
                    f"free light chains, and complete blood count. Imaging as clinically indicated."
                )
            }
        
        elif category == "Complete Response (CR)":
            return {
                "stage": "Complete Response (CR)",
                "description": "Complete response",
                "interpretation": (
                    f"COMPLETE RESPONSE (CR): The patient has achieved complete remission of multiple myeloma. "
                    f"CRITERIA MET: Negative serum and urine immunofixation, <5% bone marrow plasma cells, "
                    f"and disappearance of any soft tissue plasmacytomas. "
                    f"CLINICAL SIGNIFICANCE: This represents excellent response to treatment with no detectable "
                    f"M protein and minimal bone marrow involvement. Patients with CR have favorable outcomes "
                    f"and extended progression-free survival. "
                    f"MANAGEMENT: Continue current therapy if on treatment or consider maintenance therapy. "
                    f"Consider evaluation for stringent CR with free light chain ratio and bone marrow "
                    f"immunohistochemistry if not already performed. "
                    f"FOLLOW-UP: Regular monitoring every 3-6 months with laboratory studies. Continue "
                    f"surveillance for relapse with serum protein studies and clinical assessment."
                )
            }
        
        elif category == "Very Good Partial Response (VGPR)":
            return {
                "stage": "Very Good Partial Response (VGPR)",
                "description": "Very good partial response",
                "interpretation": (
                    f"VERY GOOD PARTIAL RESPONSE (VGPR): The patient has achieved very good partial remission. "
                    f"CRITERIA MET: Either M component detectable by immunofixation but not electrophoresis, "
                    f"OR ≥90% reduction in serum M component plus urine M component <100 mg per 24 hours. "
                    f"CLINICAL SIGNIFICANCE: This represents excellent response to treatment with minimal "
                    f"residual disease. VGPR is associated with good long-term outcomes and may progress "
                    f"to complete response with continued therapy. "
                    f"MANAGEMENT: Continue current treatment regimen. Consider intensification if appropriate "
                    f"to achieve complete response. Monitor for further improvement in response. "
                    f"FOLLOW-UP: Regular assessment every 2-3 months during active treatment. Monitor "
                    f"for progression to complete response or maintenance of current response level."
                )
            }
        
        elif category == "Partial Response (PR)":
            return {
                "stage": "Partial Response (PR)",
                "description": "Partial response",
                "interpretation": (
                    f"PARTIAL RESPONSE (PR): The patient has achieved significant but incomplete response. "
                    f"CRITERIA MET: ≥50% reduction of serum M protein, ≥90% reduction in 24-hour urinary "
                    f"M protein (or to <200 mg), and if present, ≥50% reduction in soft tissue plasmacytomas. "
                    f"CLINICAL SIGNIFICANCE: This represents meaningful response to treatment with substantial "
                    f"disease reduction. Patients with PR benefit from continued therapy and may achieve "
                    f"deeper responses with time. "
                    f"MANAGEMENT: Continue current treatment regimen with goal of achieving deeper response. "
                    f"Consider treatment intensification or alternative approaches if response plateaus. "
                    f"FOLLOW-UP: Regular monitoring every 2-3 months. Assess for improvement to VGPR or CR "
                    f"with continued therapy."
                )
            }
        
        elif category == "Stable Disease (SD)":
            return {
                "stage": "Stable Disease (SD)",
                "description": "Stable disease",
                "interpretation": (
                    f"STABLE DISEASE (SD): The patient has stable disease not meeting criteria for other "
                    f"response categories. "
                    f"CLINICAL SIGNIFICANCE: Disease is neither responding significantly nor progressing. "
                    f"This may represent disease control with current therapy or insufficient response "
                    f"requiring treatment modification. "
                    f"MANAGEMENT: Evaluate need for treatment change if this represents lack of response "
                    f"to initial therapy. Consider alternative treatment approaches or intensification. "
                    f"If on maintenance therapy, stable disease may be acceptable. "
                    f"FOLLOW-UP: Close monitoring every 1-2 months. Watch for signs of progression or "
                    f"late response to therapy."
                )
            }
        
        else:  # Progressive Disease
            return {
                "stage": "Progressive Disease (PD)",
                "description": "Disease progression",
                "interpretation": (
                    f"PROGRESSIVE DISEASE (PD): The patient has evidence of disease progression. "
                    f"CRITERIA: 25% increase from lowest response value in serum M component (≥0.5 g/100 mL "
                    f"increase), urine M component (≥200 mg per 24 hours increase), development of new bone "
                    f"lesions, or hypercalcemia (corrected serum calcium >11.5 mg/dL). "
                    f"CLINICAL SIGNIFICANCE: Disease has progressed and current therapy is no longer effective. "
                    f"Immediate treatment change is required. "
                    f"MANAGEMENT: Discontinue current therapy and initiate salvage treatment regimen. "
                    f"Consider clinical trial enrollment, novel agents, or combination therapy. Assess "
                    f"performance status and comorbidities for treatment planning. "
                    f"FOLLOW-UP: Immediate oncologic consultation and treatment planning. Close monitoring "
                    f"during transition to new therapy."
                )
            }


def calculate_multiple_myeloma_response_criteria(serum_immunofixation: str, 
                                                urine_immunofixation: str,
                                                bone_marrow_plasma_cells: float, 
                                                soft_tissue_plasmacytomas: str,
                                                free_light_chain_ratio: Optional[float] = None,
                                                clonal_cells_bone_marrow: Optional[str] = None,
                                                serum_m_protein_reduction: Optional[float] = None,
                                                urine_m_protein_24h: Optional[float] = None,
                                                serum_electrophoresis_detectable: Optional[str] = None,
                                                plasmacytoma_reduction: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MultipleMyelomaResponseCriteriaCalculator()
    return calculator.calculate(serum_immunofixation, urine_immunofixation,
                               bone_marrow_plasma_cells, soft_tissue_plasmacytomas,
                               free_light_chain_ratio, clonal_cells_bone_marrow,
                               serum_m_protein_reduction, urine_m_protein_24h,
                               serum_electrophoresis_detectable, plasmacytoma_reduction)