"""
Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria Calculator

The GELF Criteria determines if immediate therapy for follicular lymphoma is needed by 
identifying high tumor burden patients who require treatment rather than active surveillance 
(watch and wait). This scoring system was developed to standardize treatment decisions and 
harmonize clinical trial populations in follicular lymphoma.

The criteria help clinicians distinguish between patients who can safely undergo active 
surveillance versus those who require immediate therapeutic intervention based on disease 
burden and clinical presentation.

Clinical Applications:
- Treatment decision-making in newly diagnosed follicular lymphoma
- Distinguishing between active surveillance vs. immediate therapy candidates
- Standardizing clinical trial enrollment criteria
- Risk stratification for treatment planning
- Monitoring patients during active surveillance

References (Vancouver style):
1. Brice P, Bastion Y, Lepage E, et al. Comparison in low-tumor-burden follicular 
   lymphomas between an initial no-treatment policy, prednimustine, or interferon alfa: 
   a randomized study from the Groupe d'Etude des Lymphomes Folliculaires. J Clin Oncol. 
   1997;15(3):1110-1117. doi: 10.1200/JCO.1997.15.3.1110
2. Solal-Céligny P, Roy P, Colombat P, et al. Follicular lymphoma international prognostic 
   index. Blood. 2004;104(5):1258-1265. doi: 10.1182/blood-2003-12-4434
3. Ardeshna KM, Smith P, Norton A, et al. Long-term effect of a watch and wait policy 
   versus immediate systemic treatment for asymptomatic advanced-stage non-Hodgkin lymphoma: 
   a randomised controlled trial. Lancet. 2003;362(9383):516-522. doi: 10.1016/S0140-6736(03)14110-4
"""

from typing import Dict, Any


class GelfCriteriaCalculator:
    """Calculator for GELF Criteria for Follicular Lymphoma Treatment Decisions"""
    
    def __init__(self):
        # GELF criteria parameters - any one positive indicates high tumor burden
        self.GELF_CRITERIA = [
            "tumor_mass_over_7cm",
            "three_or_more_nodal_sites", 
            "systemic_b_symptoms",
            "splenic_enlargement",
            "compression_syndrome",
            "serous_effusion",
            "leukemic_phase",
            "granulocyte_count_low",
            "platelet_count_low"
        ]
        
        # Criteria descriptions for interpretation
        self.CRITERIA_DESCRIPTIONS = {
            "tumor_mass_over_7cm": "Tumor mass >7cm diameter",
            "three_or_more_nodal_sites": "≥3 nodal sites >3cm diameter",
            "systemic_b_symptoms": "B symptoms (fever, night sweats, weight loss)",
            "splenic_enlargement": "Splenomegaly below umbilical line",
            "compression_syndrome": "Compression syndrome (ureteral/orbital/GI)",
            "serous_effusion": "Pleural or peritoneal effusion",
            "leukemic_phase": "Leukemic phase >5.0×10⁹/L malignant cells",
            "granulocyte_count_low": "Granulocytes <1.0×10⁹/L",
            "platelet_count_low": "Platelets <100×10⁹/L"
        }
    
    def calculate(self, tumor_mass_over_7cm: str, three_or_more_nodal_sites: str,
                 systemic_b_symptoms: str, splenic_enlargement: str, compression_syndrome: str,
                 serous_effusion: str, leukemic_phase: str, granulocyte_count_low: str,
                 platelet_count_low: str) -> Dict[str, Any]:
        """
        Calculates GELF criteria assessment for follicular lymphoma treatment decisions
        
        Args:
            tumor_mass_over_7cm (str): Any nodal/extranodal tumor mass >7cm (yes/no)
            three_or_more_nodal_sites (str): ≥3 nodal sites >3cm each (yes/no)
            systemic_b_symptoms (str): B symptoms present (yes/no)
            splenic_enlargement (str): Splenomegaly below umbilical line (yes/no)
            compression_syndrome (str): Compression syndrome present (yes/no)
            serous_effusion (str): Pleural/peritoneal effusion (yes/no)
            leukemic_phase (str): Leukemic phase >5.0×10⁹/L (yes/no)
            granulocyte_count_low (str): Granulocytes <1.0×10⁹/L (yes/no)
            platelet_count_low (str): Platelets <100×10⁹/L (yes/no)
            
        Returns:
            Dict with GELF assessment and treatment recommendation
        """
        
        # Collect all parameters in a dictionary for validation
        parameters = {
            "tumor_mass_over_7cm": tumor_mass_over_7cm,
            "three_or_more_nodal_sites": three_or_more_nodal_sites,
            "systemic_b_symptoms": systemic_b_symptoms,
            "splenic_enlargement": splenic_enlargement,
            "compression_syndrome": compression_syndrome,
            "serous_effusion": serous_effusion,
            "leukemic_phase": leukemic_phase,
            "granulocyte_count_low": granulocyte_count_low,
            "platelet_count_low": platelet_count_low
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Count positive criteria
        positive_criteria = []
        criteria_count = 0
        
        for criterion, value in parameters.items():
            if value.lower() == "yes":
                positive_criteria.append(criterion)
                criteria_count += 1
        
        # Determine recommendation based on criteria
        recommendation = self._get_recommendation(criteria_count, positive_criteria)
        
        # Generate comprehensive interpretation
        interpretation = self._generate_interpretation(criteria_count, positive_criteria, parameters)
        
        return {
            "result": recommendation["result"],
            "unit": "recommendation",
            "interpretation": interpretation,
            "stage": recommendation["stage"],
            "stage_description": recommendation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _get_recommendation(self, criteria_count: int, positive_criteria: list) -> Dict[str, str]:
        """
        Determines treatment recommendation based on GELF criteria
        
        Args:
            criteria_count (int): Number of positive criteria
            positive_criteria (list): List of positive criteria
            
        Returns:
            Dict with recommendation details
        """
        
        if criteria_count == 0:
            return {
                "result": "Active Surveillance Appropriate",
                "stage": "Low Tumor Burden", 
                "description": "No GELF criteria met - watch and wait recommended"
            }
        else:
            return {
                "result": "Immediate Therapy Recommended",
                "stage": "High Tumor Burden",
                "description": f"{criteria_count} GELF criteria met - treatment indicated"
            }
    
    def _generate_interpretation(self, criteria_count: int, positive_criteria: list, 
                               parameters: Dict[str, str]) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            criteria_count (int): Number of positive criteria
            positive_criteria (list): List of positive criteria
            parameters (Dict): All parameter values
            
        Returns:
            str: Comprehensive clinical interpretation
        """
        
        # Build criteria summary
        if criteria_count == 0:
            criteria_summary = "No GELF criteria are met. "
        else:
            positive_descriptions = [self.CRITERIA_DESCRIPTIONS[criterion] for criterion in positive_criteria]
            criteria_summary = (
                f"{criteria_count} GELF criteria met: {', '.join(positive_descriptions)}. "
            )
        
        # Generate recommendation text
        if criteria_count == 0:
            recommendation_text = (
                "GELF Assessment: Low tumor burden. Active surveillance (watch and wait) is "
                "appropriate. Regular monitoring recommended with treatment initiation when "
                "disease progression, transformation, or symptomatic disease develops. "
            )
            
            clinical_guidance = (
                "Clinical guidance: Monitor every 3-6 months initially, then every 6-12 months "
                "if stable. Consider FLIPI score for additional prognostic stratification. "
                "Patient education about symptoms requiring immediate evaluation is essential. "
                "Quality of life should be preserved during surveillance period."
            )
        else:
            recommendation_text = (
                "GELF Assessment: High tumor burden requiring immediate therapy rather than "
                "active surveillance. Treatment should be initiated promptly to prevent "
                "disease-related complications and optimize outcomes. "
            )
            
            clinical_guidance = (
                "Clinical guidance: Consider rituximab-based regimens such as R-CHOP, R-CVP, "
                "or R-bendamustine based on patient age, comorbidities, and institutional "
                "preferences. Multidisciplinary team discussion recommended for optimal "
                "treatment planning. Consider clinical trial enrollment if appropriate. "
                "Staging with PET-CT and bone marrow biopsy should be completed before "
                "treatment initiation."
            )
        
        # Add important clinical considerations
        clinical_considerations = (
            "Important considerations: GELF criteria were developed to standardize treatment "
            "decisions in follicular lymphoma but should be used in conjunction with clinical "
            "judgment, patient preferences, and comorbidities. Consider FLIPI score for "
            "prognostic assessment. Recent studies suggest some discordance between GELF "
            "criteria and actual treatment patterns in routine practice. The criteria were "
            "developed in the pre-rituximab era but remain relevant for current management "
            "decisions."
        )
        
        # Combine all components
        interpretation = (
            f"{criteria_summary}{recommendation_text}{clinical_guidance}{clinical_considerations}"
        )
        
        return interpretation


def calculate_gelf_criteria(tumor_mass_over_7cm: str, three_or_more_nodal_sites: str,
                           systemic_b_symptoms: str, splenic_enlargement: str, 
                           compression_syndrome: str, serous_effusion: str,
                           leukemic_phase: str, granulocyte_count_low: str,
                           platelet_count_low: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gelf_criteria pattern
    """
    calculator = GelfCriteriaCalculator()
    return calculator.calculate(
        tumor_mass_over_7cm, three_or_more_nodal_sites, systemic_b_symptoms,
        splenic_enlargement, compression_syndrome, serous_effusion,
        leukemic_phase, granulocyte_count_low, platelet_count_low
    )