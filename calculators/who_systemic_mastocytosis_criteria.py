"""
WHO Diagnostic Criteria for Systemic Mastocytosis (2016) Calculator

World Health Organization 2016 diagnostic criteria for systemic mastocytosis.
Requires 1 major criterion + 1 minor criterion OR 3 minor criteria for diagnosis.

References:
1. Valent P, Akin C, Hartmann K, et al. Updated diagnostic criteria and classification 
   of mast cell disorders: a consensus proposal. HemaSphere. 2021;5(11):e646. 
   doi: 10.1097/HS9.0000000000000646
2. Arber DA, Orazi A, Hasserjian R, et al. The 2016 revision to the World Health 
   Organization classification of myeloid neoplasms and acute leukemia. Blood. 
   2016;127(20):2391-2405. doi: 10.1182/blood-2016-03-643544
3. Valent P, Alin C, Metcalfe DD. Mastocytosis: 2016 updated WHO classification 
   and novel emerging treatment concepts. Blood. 2017;129(11):1420-1427. 
   doi: 10.1182/blood-2016-09-731893
"""

from typing import Dict, Any, List


class WhoSystemicMastocytosisCriteriaCalculator:
    """Calculator for WHO 2016 Diagnostic Criteria for Systemic Mastocytosis"""
    
    def __init__(self):
        # WHO 2016 criteria thresholds
        self.TRYPTASE_THRESHOLD = 20.0  # ng/mL
        self.TRYPTASE_NORMAL_UPPER = 11.4  # ng/mL
        
        # Criterion descriptions
        self.MAJOR_CRITERION_DESCRIPTION = "Multifocal dense infiltrates of mast cells (≥15 mast cells in aggregates) in bone marrow biopsies and/or other extracutaneous organ sections"
        
        self.MINOR_CRITERIA_DESCRIPTIONS = {
            "criterion_1": "≥25% of mast cells are atypical (type I or II) on bone marrow smears or spindle-shaped in mast cell infiltrates",
            "criterion_2": "KIT-activating point mutations at codon 816 (usually D816V) or other critical KIT regions",
            "criterion_3": "Mast cells express CD2 and/or CD25 and/or CD30 (aberrant phenotype) in addition to normal mast cell markers",
            "criterion_4": "Baseline serum tryptase concentration >20 ng/mL (in absence of associated myeloid neoplasm)"
        }
    
    def calculate(self, multifocal_mast_cell_infiltrates: str, atypical_mast_cell_morphology: str,
                 kit_mutation: str, aberrant_cd_expression: str, serum_tryptase: float,
                 associated_myeloid_neoplasm: str) -> Dict[str, Any]:
        """
        Evaluates WHO 2016 diagnostic criteria for systemic mastocytosis
        
        Args:
            multifocal_mast_cell_infiltrates (str): Major criterion - mast cell aggregates ≥15 cells
            atypical_mast_cell_morphology (str): Minor criterion 1 - atypical morphology ≥25%
            kit_mutation (str): Minor criterion 2 - KIT mutations
            aberrant_cd_expression (str): Minor criterion 3 - CD2/CD25/CD30 expression
            serum_tryptase (float): Serum tryptase level for minor criterion 4
            associated_myeloid_neoplasm (str): Affects tryptase criterion interpretation
            
        Returns:
            Dict with diagnosis assessment and detailed criteria analysis
        """
        
        # Organize parameters
        parameters = {
            "multifocal_mast_cell_infiltrates": multifocal_mast_cell_infiltrates,
            "atypical_mast_cell_morphology": atypical_mast_cell_morphology,
            "kit_mutation": kit_mutation,
            "aberrant_cd_expression": aberrant_cd_expression,
            "serum_tryptase": serum_tryptase,
            "associated_myeloid_neoplasm": associated_myeloid_neoplasm
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Evaluate criteria
        criteria_assessment = self._evaluate_criteria(parameters)
        
        # Determine diagnosis
        diagnosis_result = self._determine_diagnosis(criteria_assessment)
        
        # Generate detailed analysis
        detailed_analysis = self._generate_detailed_analysis(parameters, criteria_assessment, diagnosis_result)
        
        return {
            "result": diagnosis_result["status"],
            "unit": "categorical",
            "interpretation": diagnosis_result["interpretation"],
            "stage": diagnosis_result["stage"],
            "stage_description": diagnosis_result["stage_description"],
            "major_criteria_met": criteria_assessment["major_criteria_met"],
            "minor_criteria_met": criteria_assessment["minor_criteria_met"],
            "total_major_criteria": criteria_assessment["total_major_criteria"],
            "total_minor_criteria": criteria_assessment["total_minor_criteria"],
            "criteria_details": criteria_assessment["criteria_details"],
            "detailed_analysis": detailed_analysis
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        # Categorical validations
        valid_yes_no_na = ["yes", "no", "not_assessed"]
        if parameters["multifocal_mast_cell_infiltrates"] not in valid_yes_no_na:
            raise ValueError(f"Multifocal mast cell infiltrates must be one of: {valid_yes_no_na}")
        
        if parameters["atypical_mast_cell_morphology"] not in valid_yes_no_na:
            raise ValueError(f"Atypical mast cell morphology must be one of: {valid_yes_no_na}")
        
        valid_kit = ["d816v_positive", "other_kit_positive", "negative", "not_tested"]
        if parameters["kit_mutation"] not in valid_kit:
            raise ValueError(f"KIT mutation must be one of: {valid_kit}")
        
        if parameters["aberrant_cd_expression"] not in valid_yes_no_na:
            raise ValueError(f"Aberrant CD expression must be one of: {valid_yes_no_na}")
        
        valid_myeloid = ["yes", "no", "unknown"]
        if parameters["associated_myeloid_neoplasm"] not in valid_myeloid:
            raise ValueError(f"Associated myeloid neoplasm must be one of: {valid_myeloid}")
        
        # Serum tryptase validation
        if not isinstance(parameters["serum_tryptase"], (int, float)):
            raise ValueError("Serum tryptase must be a number")
        if parameters["serum_tryptase"] < 0.0 or parameters["serum_tryptase"] > 200.0:
            raise ValueError("Serum tryptase must be between 0.0 and 200.0 ng/mL")
    
    def _evaluate_criteria(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates WHO 2016 diagnostic criteria"""
        
        criteria_details = {}
        major_criteria_met = 0
        minor_criteria_met = 0
        
        # Major Criterion: Multifocal mast cell infiltrates
        major_criterion_met = self._evaluate_major_criterion(parameters)
        criteria_details["major_criterion"] = {
            "description": self.MAJOR_CRITERION_DESCRIPTION,
            "met": major_criterion_met["met"],
            "details": major_criterion_met["details"]
        }
        if major_criterion_met["met"]:
            major_criteria_met += 1
        
        # Minor Criterion 1: Atypical morphology
        minor_criterion_1_met = self._evaluate_minor_criterion_1(parameters)
        criteria_details["minor_criterion_1"] = {
            "description": self.MINOR_CRITERIA_DESCRIPTIONS["criterion_1"],
            "met": minor_criterion_1_met["met"],
            "details": minor_criterion_1_met["details"]
        }
        if minor_criterion_1_met["met"]:
            minor_criteria_met += 1
        
        # Minor Criterion 2: KIT mutation
        minor_criterion_2_met = self._evaluate_minor_criterion_2(parameters)
        criteria_details["minor_criterion_2"] = {
            "description": self.MINOR_CRITERIA_DESCRIPTIONS["criterion_2"],
            "met": minor_criterion_2_met["met"],
            "details": minor_criterion_2_met["details"]
        }
        if minor_criterion_2_met["met"]:
            minor_criteria_met += 1
        
        # Minor Criterion 3: Aberrant CD expression
        minor_criterion_3_met = self._evaluate_minor_criterion_3(parameters)
        criteria_details["minor_criterion_3"] = {
            "description": self.MINOR_CRITERIA_DESCRIPTIONS["criterion_3"],
            "met": minor_criterion_3_met["met"],
            "details": minor_criterion_3_met["details"]
        }
        if minor_criterion_3_met["met"]:
            minor_criteria_met += 1
        
        # Minor Criterion 4: Serum tryptase
        minor_criterion_4_met = self._evaluate_minor_criterion_4(parameters)
        criteria_details["minor_criterion_4"] = {
            "description": self.MINOR_CRITERIA_DESCRIPTIONS["criterion_4"],
            "met": minor_criterion_4_met["met"],
            "details": minor_criterion_4_met["details"]
        }
        if minor_criterion_4_met["met"]:
            minor_criteria_met += 1
        
        return {
            "major_criteria_met": major_criteria_met,
            "minor_criteria_met": minor_criteria_met,
            "total_major_criteria": 1,
            "total_minor_criteria": 4,
            "criteria_details": criteria_details
        }
    
    def _evaluate_major_criterion(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Major Criterion: Multifocal mast cell infiltrates"""
        
        infiltrates = parameters["multifocal_mast_cell_infiltrates"]
        
        if infiltrates == "yes":
            return {
                "met": True,
                "details": "Multifocal dense infiltrates of mast cells (≥15 cells in aggregates) present in bone marrow and/or extracutaneous organs"
            }
        elif infiltrates == "no":
            return {
                "met": False,
                "details": "Multifocal mast cell infiltrates not identified or do not meet ≥15 cells threshold"
            }
        else:  # not_assessed
            return {
                "met": False,
                "details": "Tissue evaluation not performed - major criterion cannot be assessed"
            }
    
    def _evaluate_minor_criterion_1(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Minor Criterion 1: Atypical mast cell morphology"""
        
        morphology = parameters["atypical_mast_cell_morphology"]
        
        if morphology == "yes":
            return {
                "met": True,
                "details": "≥25% of mast cells show atypical morphology (type I/II) or spindle-shaped appearance"
            }
        elif morphology == "no":
            return {
                "met": False,
                "details": "Mast cells show normal morphology, <25% atypical forms"
            }
        else:  # not_assessed
            return {
                "met": False,
                "details": "Morphological assessment not performed - criterion cannot be evaluated"
            }
    
    def _evaluate_minor_criterion_2(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Minor Criterion 2: KIT mutation"""
        
        kit_mutation = parameters["kit_mutation"]
        
        if kit_mutation == "d816v_positive":
            return {
                "met": True,
                "details": "KIT D816V mutation detected (most common activating mutation in systemic mastocytosis)"
            }
        elif kit_mutation == "other_kit_positive":
            return {
                "met": True,
                "details": "Other KIT activating mutation detected at critical regions"
            }
        elif kit_mutation == "negative":
            return {
                "met": False,
                "details": "No KIT mutations detected"
            }
        else:  # not_tested
            return {
                "met": False,
                "details": "KIT mutation testing not performed - criterion cannot be assessed"
            }
    
    def _evaluate_minor_criterion_3(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Minor Criterion 3: Aberrant CD expression"""
        
        cd_expression = parameters["aberrant_cd_expression"]
        
        if cd_expression == "yes":
            return {
                "met": True,
                "details": "Mast cells express aberrant markers (CD2/CD25/CD30) by flow cytometry or immunohistochemistry"
            }
        elif cd_expression == "no":
            return {
                "met": False,
                "details": "Mast cells do not express aberrant CD markers"
            }
        else:  # not_assessed
            return {
                "met": False,
                "details": "Immunophenotyping not performed - criterion cannot be evaluated"
            }
    
    def _evaluate_minor_criterion_4(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Minor Criterion 4: Serum tryptase"""
        
        tryptase = parameters["serum_tryptase"]
        myeloid_neoplasm = parameters["associated_myeloid_neoplasm"]
        
        # Criterion only valid in absence of associated myeloid neoplasm
        if myeloid_neoplasm == "yes":
            return {
                "met": False,
                "details": f"Serum tryptase {tryptase} ng/mL, but associated myeloid neoplasm present (criterion not valid)"
            }
        
        if tryptase > self.TRYPTASE_THRESHOLD:
            if myeloid_neoplasm == "no":
                return {
                    "met": True,
                    "details": f"Serum tryptase {tryptase} ng/mL > {self.TRYPTASE_THRESHOLD} ng/mL threshold, no associated myeloid neoplasm"
                }
            else:  # unknown
                return {
                    "met": True,
                    "details": f"Serum tryptase {tryptase} ng/mL > {self.TRYPTASE_THRESHOLD} ng/mL threshold (note: associated myeloid neoplasm status unknown)"
                }
        else:
            elevation_status = "elevated" if tryptase > self.TRYPTASE_NORMAL_UPPER else "normal"
            return {
                "met": False,
                "details": f"Serum tryptase {tryptase} ng/mL ≤ {self.TRYPTASE_THRESHOLD} ng/mL threshold ({elevation_status} range)"
            }
    
    def _determine_diagnosis(self, criteria_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Determines diagnosis based on criteria fulfillment"""
        
        major_met = criteria_assessment["major_criteria_met"]
        minor_met = criteria_assessment["minor_criteria_met"]
        
        # Diagnosis requires: (1 major + 1 minor) OR (3 minor criteria)
        if (major_met >= 1 and minor_met >= 1) or (minor_met >= 3):
            return {
                "status": "diagnosis_met",
                "stage": "Systemic Mastocytosis Diagnosed",
                "stage_description": "WHO 2016 criteria met - diagnosis confirmed",
                "interpretation": f"WHO 2016 diagnostic criteria for systemic mastocytosis are MET. Patient fulfills {major_met} major criterion "
                               f"and {minor_met} minor criteria. Diagnosis of systemic mastocytosis is confirmed. Proceed with staging, risk "
                               f"stratification, and appropriate management. Consider referral to hematology-oncology for specialized care and "
                               f"evaluation of disease subtype and prognosis."
            }
        elif major_met >= 1 or minor_met >= 1:
            return {
                "status": "probable_sm",
                "stage": "Probable Systemic Mastocytosis",
                "stage_description": "Some criteria met but additional testing needed",
                "interpretation": f"Patient fulfills {major_met} major criterion and {minor_met} minor criteria. Additional testing needed to "
                               f"establish definitive diagnosis. Complete missing evaluations (bone marrow biopsy, molecular testing, "
                               f"immunophenotyping, serum tryptase) to fully assess WHO criteria. Hematology consultation recommended for "
                               f"further workup and management."
            }
        else:
            return {
                "status": "criteria_not_met",
                "stage": "Criteria Not Met",
                "stage_description": "WHO criteria for systemic mastocytosis not fulfilled",
                "interpretation": "Current findings do not meet WHO 2016 diagnostic criteria for systemic mastocytosis. Consider alternative "
                               "diagnoses including cutaneous mastocytosis, mast cell activation syndrome, hereditary alpha-tryptasemia, "
                               "or other conditions. If clinical suspicion remains high, consider specialist consultation for comprehensive "
                               "evaluation and additional testing."
            }
    
    def _generate_detailed_analysis(self, parameters: Dict[str, Any], criteria_assessment: Dict[str, Any], 
                                  diagnosis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generates detailed clinical analysis"""
        
        analysis = {
            "criteria_summary": self._generate_criteria_summary(criteria_assessment),
            "clinical_recommendations": self._generate_clinical_recommendations(diagnosis_result, parameters),
            "laboratory_interpretation": self._generate_laboratory_interpretation(parameters),
            "differential_diagnosis": self._generate_differential_diagnosis(diagnosis_result, parameters),
            "follow_up_recommendations": self._generate_follow_up_recommendations(diagnosis_result, criteria_assessment)
        }
        
        return analysis
    
    def _generate_criteria_summary(self, criteria_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generates summary of criteria assessment"""
        
        major_met = criteria_assessment["major_criteria_met"]
        minor_met = criteria_assessment["minor_criteria_met"]
        
        summary = {
            "major_criteria": f"{major_met}/1 met",
            "minor_criteria": f"{minor_met}/4 met",
            "diagnosis_requirement": "1 major criterion + 1 minor criterion OR 3 minor criteria",
            "criteria_breakdown": []
        }
        
        for criterion_name, criterion_data in criteria_assessment["criteria_details"].items():
            summary["criteria_breakdown"].append({
                "criterion": criterion_name.replace("_", " ").title(),
                "description": criterion_data["description"],
                "status": "Met" if criterion_data["met"] else "Not Met",
                "details": criterion_data["details"]
            })
        
        return summary
    
    def _generate_clinical_recommendations(self, diagnosis_result: Dict[str, Any], 
                                         parameters: Dict[str, Any]) -> List[str]:
        """Generates clinical management recommendations"""
        
        recommendations = []
        status = diagnosis_result["status"]
        
        if status == "diagnosis_met":
            recommendations.extend([
                "Refer to hematology-oncology for specialized management and staging",
                "Perform disease subtype classification (indolent, smoldering, aggressive, etc.)",
                "Assess for organ involvement and functional impairment",
                "Consider bone marrow cytogenetics to evaluate for associated hematologic neoplasm",
                "Screen for mediator release symptoms and treat accordingly",
                "Evaluate for osteoporosis and fracture risk (DEXA scan)",
                "Consider allergy/immunology consultation for symptom management",
                "Baseline assessment for hepatosplenomegaly and lymphadenopathy"
            ])
        elif status == "probable_sm":
            recommendations.extend([
                "Complete comprehensive bone marrow evaluation with immunohistochemistry",
                "Perform KIT mutation testing if not done",
                "Obtain flow cytometry or immunohistochemistry for CD2/CD25/CD30",
                "Measure serum tryptase if not available",
                "Consider hematology consultation for expert evaluation",
                "Monitor symptoms and clinical progression"
            ])
        else:
            recommendations.extend([
                "Consider cutaneous mastocytosis if skin involvement present",
                "Evaluate for mast cell activation syndrome if symptomatic",
                "Test for hereditary alpha-tryptasemia if tryptase elevated",
                "Consider other causes of elevated tryptase (renal disease, hematologic malignancies)",
                "Specialist consultation if clinical suspicion remains high despite negative criteria"
            ])
        
        # Add specific recommendations based on parameters
        tryptase = parameters["serum_tryptase"]
        if tryptase > 50.0:
            recommendations.append("Very high tryptase level - urgent hematology consultation recommended")
        
        return recommendations
    
    def _generate_laboratory_interpretation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generates interpretation of laboratory values"""
        
        tryptase = parameters["serum_tryptase"]
        
        interpretation = {
            "tryptase_analysis": {
                "value": f"{tryptase} ng/mL",
                "normal_range": f"<{self.TRYPTASE_NORMAL_UPPER} ng/mL",
                "threshold": f">{self.TRYPTASE_THRESHOLD} ng/mL",
                "elevated": tryptase > self.TRYPTASE_NORMAL_UPPER,
                "meets_criterion": tryptase > self.TRYPTASE_THRESHOLD,
                "degree_elevation": "marked" if tryptase > 50.0 else "moderate" if tryptase > 25.0 else "mild" if tryptase > self.TRYPTASE_NORMAL_UPPER else "normal"
            },
            "molecular_testing": {
                "kit_mutation": parameters["kit_mutation"],
                "significance": "KIT D816V most common in systemic mastocytosis" if parameters["kit_mutation"] == "d816v_positive" else "Other activating KIT mutations also diagnostic"
            },
            "morphology_assessment": {
                "atypical_morphology": parameters["atypical_mast_cell_morphology"],
                "infiltrates": parameters["multifocal_mast_cell_infiltrates"]
            },
            "immunophenotype": {
                "aberrant_cd_expression": parameters["aberrant_cd_expression"],
                "note": "CD25 most commonly positive, followed by CD2 and CD30"
            }
        }
        
        return interpretation
    
    def _generate_differential_diagnosis(self, diagnosis_result: Dict[str, Any], 
                                       parameters: Dict[str, Any]) -> List[str]:
        """Generates differential diagnosis considerations"""
        
        differential = []
        status = diagnosis_result["status"]
        
        if status == "diagnosis_met":
            differential.extend([
                "Systemic mastocytosis (diagnosis confirmed by WHO criteria)",
                "Evaluate subtype: indolent, smoldering, aggressive, or mast cell leukemia",
                "Consider associated clonal hematologic non-mast cell lineage disease (SM-AHNMD)"
            ])
        else:
            differential.extend([
                "Cutaneous mastocytosis (urticaria pigmentosa, diffuse cutaneous mastocytosis)",
                "Mast cell activation syndrome (MCAS)",
                "Hereditary alpha-tryptasemia",
                "Secondary causes of elevated tryptase (renal disease, hematologic malignancies)",
                "Idiopathic anaphylaxis",
                "Primary myelofibrosis with mast cell proliferation"
            ])
            
            # Add specific considerations based on test results
            tryptase = parameters["serum_tryptase"]
            if tryptase > self.TRYPTASE_NORMAL_UPPER:
                differential.append("Consider non-SM causes of elevated tryptase if criteria not met")
        
        return differential
    
    def _generate_follow_up_recommendations(self, diagnosis_result: Dict[str, Any], 
                                          criteria_assessment: Dict[str, Any]) -> List[str]:
        """Generates follow-up recommendations"""
        
        follow_up = []
        status = diagnosis_result["status"]
        
        if status == "diagnosis_met":
            follow_up.extend([
                "Regular hematology-oncology follow-up every 3-6 months",
                "Annual bone marrow assessment for disease progression",
                "Monitor complete blood count and biochemistry quarterly",
                "Assess for organ dysfunction and mediator symptoms at each visit",
                "Annual DEXA scan for osteoporosis screening",
                "Consider genetic counseling if familial clustering"
            ])
        elif status == "probable_sm":
            follow_up.extend([
                "Complete missing diagnostic tests within 4-6 weeks",
                "Hematology consultation within 2-4 weeks",
                "Monitor symptoms and tryptase levels every 3 months",
                "Repeat evaluation if new symptoms develop"
            ])
        else:
            follow_up.extend([
                "Monitor symptoms if present",
                "Repeat tryptase annually if initially elevated",
                "Consider re-evaluation if new symptoms develop",
                "Specialist referral if clinical concern persists"
            ])
        
        # Add specific follow-up based on missing tests
        missing_tests = []
        criteria_details = criteria_assessment["criteria_details"]
        
        if "not_assessed" in criteria_details["major_criterion"]["details"]:
            missing_tests.append("bone marrow biopsy with immunohistochemistry")
        if "not_tested" in criteria_details["minor_criterion_2"]["details"]:
            missing_tests.append("KIT mutation testing")
        if "not_assessed" in criteria_details["minor_criterion_3"]["details"]:
            missing_tests.append("flow cytometry for aberrant CD markers")
        
        if missing_tests:
            follow_up.append(f"Complete missing tests: {', '.join(missing_tests)}")
        
        return follow_up


def calculate_who_systemic_mastocytosis_criteria(multifocal_mast_cell_infiltrates, atypical_mast_cell_morphology,
                                               kit_mutation, aberrant_cd_expression, serum_tryptase,
                                               associated_myeloid_neoplasm) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_who_systemic_mastocytosis_criteria pattern
    """
    calculator = WhoSystemicMastocytosisCriteriaCalculator()
    return calculator.calculate(
        multifocal_mast_cell_infiltrates, atypical_mast_cell_morphology,
        kit_mutation, aberrant_cd_expression, serum_tryptase,
        associated_myeloid_neoplasm
    )