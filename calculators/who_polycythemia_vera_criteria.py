"""
WHO Diagnostic Criteria for Polycythemia Vera (2016) Calculator

World Health Organization 2016 diagnostic criteria for polycythemia vera.
Designed to detect masked PV cases missed by 2008 criteria.

References:
1. Arber DA, Orazi A, Hasserjian R, et al. The 2016 revision to the World Health 
   Organization classification of myeloid neoplasms and acute leukemia. Blood. 
   2016;127(20):2391-2405. doi: 10.1182/blood-2016-03-643544
2. Barbui T, Thiele J, Gisslinger H, et al. The 2016 WHO classification and diagnostic 
   criteria for myeloproliferative neoplasms: document summary and in-depth discussion. 
   Blood Cancer J. 2018;8(2):15. doi: 10.1038/s41408-018-0054-y
3. Tefferi A, Barbui T. Polycythemia vera and essential thrombocythemia: 2021 update 
   on diagnosis, risk-stratification and management. Am J Hematol. 2020;95(12):1599-1613. 
   doi: 10.1002/ajh.26008
"""

from typing import Dict, Any, List


class WhoPolycythemiaVeraCriteriaCalculator:
    """Calculator for WHO 2016 Diagnostic Criteria for Polycythemia Vera"""
    
    def __init__(self):
        # WHO 2016 thresholds
        self.HEMOGLOBIN_THRESHOLDS = {
            "male": 16.5,    # g/dL
            "female": 16.0   # g/dL
        }
        
        self.HEMATOCRIT_THRESHOLDS = {
            "male": 49.0,    # %
            "female": 48.0   # %
        }
        
        # Criterion descriptions
        self.MAJOR_CRITERIA_DESCRIPTIONS = {
            "criterion_1": "Hemoglobin >16.5 g/dL (men) or >16.0 g/dL (women) OR Hematocrit >49% (men) or >48% (women) OR elevated red cell mass >25% above normal",
            "criterion_2": "Bone marrow hypercellularity for age with trilineage growth including prominent erythroid, granulocytic, and megakaryocytic proliferation",
            "criterion_3": "Presence of JAK2V617F or JAK2 exon 12 mutation"
        }
        
        self.MINOR_CRITERIA_DESCRIPTIONS = {
            "criterion_1": "Subnormal serum erythropoietin level"
        }
    
    def calculate(self, gender: str, hemoglobin: float, hematocrit: float, 
                 red_cell_mass_elevated: str, bone_marrow_hypercellular: str,
                 jak2_mutation: str, erythropoietin_level: str) -> Dict[str, Any]:
        """
        Evaluates WHO 2016 diagnostic criteria for polycythemia vera
        
        Args:
            gender (str): Patient gender (male/female)
            hemoglobin (float): Hemoglobin level in g/dL
            hematocrit (float): Hematocrit percentage
            red_cell_mass_elevated (str): Red cell mass status (yes/no/not_measured)
            bone_marrow_hypercellular (str): Bone marrow biopsy result (yes/no/not_performed)
            jak2_mutation (str): JAK2 mutation status
            erythropoietin_level (str): EPO level status (subnormal/normal/elevated/not_measured)
            
        Returns:
            Dict with diagnosis assessment and detailed criteria analysis
        """
        
        # Organize parameters
        parameters = {
            "gender": gender,
            "hemoglobin": hemoglobin,
            "hematocrit": hematocrit,
            "red_cell_mass_elevated": red_cell_mass_elevated,
            "bone_marrow_hypercellular": bone_marrow_hypercellular,
            "jak2_mutation": jak2_mutation,
            "erythropoietin_level": erythropoietin_level
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
        
        # Gender validation
        if parameters["gender"] not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        # Hemoglobin validation
        if not isinstance(parameters["hemoglobin"], (int, float)):
            raise ValueError("Hemoglobin must be a number")
        if parameters["hemoglobin"] < 5.0 or parameters["hemoglobin"] > 25.0:
            raise ValueError("Hemoglobin must be between 5.0 and 25.0 g/dL")
        
        # Hematocrit validation
        if not isinstance(parameters["hematocrit"], (int, float)):
            raise ValueError("Hematocrit must be a number")
        if parameters["hematocrit"] < 10.0 or parameters["hematocrit"] > 80.0:
            raise ValueError("Hematocrit must be between 10.0 and 80.0%")
        
        # Categorical validations
        valid_red_cell_mass = ["yes", "no", "not_measured"]
        if parameters["red_cell_mass_elevated"] not in valid_red_cell_mass:
            raise ValueError(f"Red cell mass elevated must be one of: {valid_red_cell_mass}")
        
        valid_bone_marrow = ["yes", "no", "not_performed"]
        if parameters["bone_marrow_hypercellular"] not in valid_bone_marrow:
            raise ValueError(f"Bone marrow hypercellular must be one of: {valid_bone_marrow}")
        
        valid_jak2 = ["jak2v617f_positive", "jak2_exon12_positive", "negative", "not_tested"]
        if parameters["jak2_mutation"] not in valid_jak2:
            raise ValueError(f"JAK2 mutation must be one of: {valid_jak2}")
        
        valid_epo = ["subnormal", "normal", "elevated", "not_measured"]
        if parameters["erythropoietin_level"] not in valid_epo:
            raise ValueError(f"Erythropoietin level must be one of: {valid_epo}")
    
    def _evaluate_criteria(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates WHO 2016 diagnostic criteria"""
        
        criteria_details = {}
        major_criteria_met = 0
        minor_criteria_met = 0
        
        # Major Criterion 1: Hemoglobin OR Hematocrit OR Red cell mass
        criterion_1_met = self._evaluate_major_criterion_1(parameters)
        criteria_details["major_criterion_1"] = {
            "description": self.MAJOR_CRITERIA_DESCRIPTIONS["criterion_1"],
            "met": criterion_1_met["met"],
            "details": criterion_1_met["details"],
            "components": criterion_1_met["components"]
        }
        if criterion_1_met["met"]:
            major_criteria_met += 1
        
        # Major Criterion 2: Bone marrow hypercellularity
        criterion_2_met = self._evaluate_major_criterion_2(parameters)
        criteria_details["major_criterion_2"] = {
            "description": self.MAJOR_CRITERIA_DESCRIPTIONS["criterion_2"],
            "met": criterion_2_met["met"],
            "details": criterion_2_met["details"]
        }
        if criterion_2_met["met"]:
            major_criteria_met += 1
        
        # Major Criterion 3: JAK2 mutation
        criterion_3_met = self._evaluate_major_criterion_3(parameters)
        criteria_details["major_criterion_3"] = {
            "description": self.MAJOR_CRITERIA_DESCRIPTIONS["criterion_3"],
            "met": criterion_3_met["met"],
            "details": criterion_3_met["details"]
        }
        if criterion_3_met["met"]:
            major_criteria_met += 1
        
        # Minor Criterion 1: Subnormal erythropoietin
        minor_criterion_1_met = self._evaluate_minor_criterion_1(parameters)
        criteria_details["minor_criterion_1"] = {
            "description": self.MINOR_CRITERIA_DESCRIPTIONS["criterion_1"],
            "met": minor_criterion_1_met["met"],
            "details": minor_criterion_1_met["details"]
        }
        if minor_criterion_1_met["met"]:
            minor_criteria_met += 1
        
        return {
            "major_criteria_met": major_criteria_met,
            "minor_criteria_met": minor_criteria_met,
            "total_major_criteria": 3,
            "total_minor_criteria": 1,
            "criteria_details": criteria_details
        }
    
    def _evaluate_major_criterion_1(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Major Criterion 1: Hemoglobin OR Hematocrit OR Red cell mass"""
        
        gender = parameters["gender"]
        hemoglobin = parameters["hemoglobin"]
        hematocrit = parameters["hematocrit"]
        red_cell_mass = parameters["red_cell_mass_elevated"]
        
        components = {}
        
        # Check hemoglobin threshold
        hgb_threshold = self.HEMOGLOBIN_THRESHOLDS[gender]
        hgb_met = hemoglobin > hgb_threshold
        components["hemoglobin"] = {
            "value": hemoglobin,
            "threshold": f">{hgb_threshold} g/dL",
            "met": hgb_met,
            "details": f"Hemoglobin {hemoglobin} g/dL vs threshold >{hgb_threshold} g/dL for {gender}"
        }
        
        # Check hematocrit threshold
        hct_threshold = self.HEMATOCRIT_THRESHOLDS[gender]
        hct_met = hematocrit > hct_threshold
        components["hematocrit"] = {
            "value": hematocrit,
            "threshold": f">{hct_threshold}%",
            "met": hct_met,
            "details": f"Hematocrit {hematocrit}% vs threshold >{hct_threshold}% for {gender}"
        }
        
        # Check red cell mass
        rcm_met = red_cell_mass == "yes"
        components["red_cell_mass"] = {
            "value": red_cell_mass,
            "met": rcm_met,
            "details": f"Red cell mass >25% above normal: {red_cell_mass}"
        }
        
        # Criterion is met if ANY component is met
        criterion_met = hgb_met or hct_met or rcm_met
        
        details = []
        if hgb_met:
            details.append(f"Hemoglobin criteria met: {hemoglobin} > {hgb_threshold} g/dL")
        if hct_met:
            details.append(f"Hematocrit criteria met: {hematocrit} > {hct_threshold}%")
        if rcm_met:
            details.append("Red cell mass >25% above normal")
        
        if not criterion_met:
            details.append("None of the hemoglobin, hematocrit, or red cell mass criteria are met")
        
        return {
            "met": criterion_met,
            "details": "; ".join(details),
            "components": components
        }
    
    def _evaluate_major_criterion_2(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Major Criterion 2: Bone marrow hypercellularity"""
        
        bone_marrow = parameters["bone_marrow_hypercellular"]
        
        if bone_marrow == "yes":
            return {
                "met": True,
                "details": "Bone marrow biopsy shows hypercellularity with trilineage growth"
            }
        elif bone_marrow == "no":
            return {
                "met": False,
                "details": "Bone marrow biopsy does not show characteristic hypercellularity"
            }
        else:  # not_performed
            return {
                "met": False,
                "details": "Bone marrow biopsy not performed - criterion cannot be assessed"
            }
    
    def _evaluate_major_criterion_3(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Major Criterion 3: JAK2 mutation"""
        
        jak2_mutation = parameters["jak2_mutation"]
        
        if jak2_mutation == "jak2v617f_positive":
            return {
                "met": True,
                "details": "JAK2V617F mutation detected"
            }
        elif jak2_mutation == "jak2_exon12_positive":
            return {
                "met": True,
                "details": "JAK2 exon 12 mutation detected"
            }
        elif jak2_mutation == "negative":
            return {
                "met": False,
                "details": "No JAK2 mutations detected"
            }
        else:  # not_tested
            return {
                "met": False,
                "details": "JAK2 mutation testing not performed - criterion cannot be assessed"
            }
    
    def _evaluate_minor_criterion_1(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates Minor Criterion 1: Subnormal erythropoietin"""
        
        epo_level = parameters["erythropoietin_level"]
        
        if epo_level == "subnormal":
            return {
                "met": True,
                "details": "Serum erythropoietin level is subnormal"
            }
        elif epo_level == "normal":
            return {
                "met": False,
                "details": "Serum erythropoietin level is normal"
            }
        elif epo_level == "elevated":
            return {
                "met": False,
                "details": "Serum erythropoietin level is elevated"
            }
        else:  # not_measured
            return {
                "met": False,
                "details": "Serum erythropoietin level not measured - criterion cannot be assessed"
            }
    
    def _determine_diagnosis(self, criteria_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Determines diagnosis based on criteria fulfillment"""
        
        major_met = criteria_assessment["major_criteria_met"]
        minor_met = criteria_assessment["minor_criteria_met"]
        
        # Diagnosis requires: 3 major criteria OR 2 major + 1 minor
        if major_met >= 3:
            return {
                "status": "diagnosis_met",
                "stage": "Polycythemia Vera Diagnosed",
                "stage_description": "WHO 2016 criteria met - diagnosis confirmed",
                "interpretation": f"WHO 2016 diagnostic criteria for polycythemia vera are MET. Patient fulfills {major_met} of 3 major criteria. "
                               f"Diagnosis of polycythemia vera is confirmed. Initiate appropriate management including phlebotomy, "
                               f"cytoreductive therapy as indicated, and monitoring for thrombotic complications. Consider referral "
                               f"to hematology-oncology for specialized care and risk stratification."
            }
        elif major_met >= 2 and minor_met >= 1:
            return {
                "status": "diagnosis_met",
                "stage": "Polycythemia Vera Diagnosed",
                "stage_description": "WHO 2016 criteria met - diagnosis confirmed",
                "interpretation": f"WHO 2016 diagnostic criteria for polycythemia vera are MET. Patient fulfills {major_met} of 3 major criteria "
                               f"and {minor_met} minor criterion. Diagnosis of polycythemia vera is confirmed. Initiate appropriate management "
                               f"including phlebotomy, cytoreductive therapy as indicated, and monitoring for thrombotic complications. "
                               f"Consider referral to hematology-oncology for specialized care and risk stratification."
            }
        elif major_met >= 2:
            return {
                "status": "probable_pv",
                "stage": "Probable Polycythemia Vera",
                "stage_description": "Some criteria met but additional testing needed",
                "interpretation": f"Patient fulfills {major_met} of 3 major criteria but lacks minor criteria. Consider measuring serum "
                               f"erythropoietin level to complete diagnostic workup. If EPO is subnormal, diagnosis of polycythemia vera "
                               f"would be confirmed. Continue monitoring and consider hematology consultation for further evaluation."
            }
        elif major_met >= 1:
            return {
                "status": "probable_pv",
                "stage": "Insufficient Criteria",
                "stage_description": "Partial criteria met - additional testing needed",
                "interpretation": f"Patient fulfills {major_met} of 3 major criteria. Additional testing needed to establish diagnosis. "
                               f"Consider completing missing evaluations (bone marrow biopsy, JAK2 mutation testing, erythropoietin level) "
                               f"to fully assess WHO criteria. Hematology consultation recommended for further workup and management."
            }
        else:
            return {
                "status": "criteria_not_met",
                "stage": "Criteria Not Met",
                "stage_description": "WHO criteria for polycythemia vera not fulfilled",
                "interpretation": "Current findings do not meet WHO 2016 diagnostic criteria for polycythemia vera. Consider alternative "
                               "causes of erythrocytosis including secondary polycythemia, other myeloproliferative neoplasms, or "
                               "relative polycythemia. Complete additional testing as indicated and consider hematology consultation "
                               "for comprehensive evaluation of elevated red blood cell parameters."
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
            "major_criteria": f"{major_met}/3 met",
            "minor_criteria": f"{minor_met}/1 met",
            "diagnosis_requirement": "3 major criteria OR 2 major + 1 minor criterion",
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
                "Initiate therapeutic phlebotomy to maintain hematocrit <45%",
                "Consider low-dose aspirin (81-100 mg daily) unless contraindicated",
                "Evaluate thrombotic risk factors and cardiovascular comorbidities",
                "Consider cytoreductive therapy (hydroxyurea) for high-risk patients",
                "Monitor for disease progression and secondary complications",
                "Refer to hematology-oncology for specialized management",
                "Screen for associated complications (splenomegaly, thrombosis, hemorrhage)"
            ])
        elif status == "probable_pv":
            recommendations.extend([
                "Complete missing diagnostic workup (EPO level, bone marrow biopsy, or JAK2 testing)",
                "Consider hematology consultation for expert evaluation",
                "Monitor hemoglobin and hematocrit levels closely",
                "Evaluate for secondary causes of erythrocytosis if criteria remain incomplete",
                "Consider therapeutic phlebotomy if symptomatic or very high hematocrit"
            ])
        else:
            recommendations.extend([
                "Investigate secondary causes of erythrocytosis",
                "Consider sleep apnea, pulmonary disease, renal pathology, or other conditions",
                "Evaluate medication history and smoking status",
                "Consider relative polycythemia due to dehydration or stress",
                "Hematology consultation if erythrocytosis persists without explanation"
            ])
        
        # Add specific recommendations based on parameters
        if parameters["hemoglobin"] > 18.0 or parameters["hematocrit"] > 55.0:
            recommendations.append("Very high red blood cell parameters - urgent evaluation recommended")
        
        return recommendations
    
    def _generate_laboratory_interpretation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generates interpretation of laboratory values"""
        
        gender = parameters["gender"]
        hemoglobin = parameters["hemoglobin"]
        hematocrit = parameters["hematocrit"]
        
        hgb_threshold = self.HEMOGLOBIN_THRESHOLDS[gender]
        hct_threshold = self.HEMATOCRIT_THRESHOLDS[gender]
        
        interpretation = {
            "hemoglobin_analysis": {
                "value": f"{hemoglobin} g/dL",
                "threshold": f">{hgb_threshold} g/dL ({gender})",
                "elevated": hemoglobin > hgb_threshold,
                "degree_elevation": "severe" if hemoglobin > 20.0 else "moderate" if hemoglobin > 18.0 else "mild"
            },
            "hematocrit_analysis": {
                "value": f"{hematocrit}%",
                "threshold": f">{hct_threshold}% ({gender})",
                "elevated": hematocrit > hct_threshold,
                "degree_elevation": "severe" if hematocrit > 60.0 else "moderate" if hematocrit > 55.0 else "mild"
            },
            "additional_tests": {
                "red_cell_mass": parameters["red_cell_mass_elevated"],
                "bone_marrow": parameters["bone_marrow_hypercellular"],
                "jak2_mutation": parameters["jak2_mutation"],
                "erythropoietin": parameters["erythropoietin_level"]
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
                "Polycythemia vera (diagnosis confirmed by WHO criteria)",
                "Consider monitoring for transformation to myelofibrosis or acute leukemia"
            ])
        else:
            differential.extend([
                "Secondary polycythemia (hypoxic conditions, EPO-producing tumors)",
                "Essential thrombocythemia with elevated hematocrit",
                "Primary myelofibrosis with elevated red blood cells",
                "Relative polycythemia (dehydration, stress, smoking)",
                "Congenital polycythemia (rare genetic conditions)",
                "Drug-induced erythrocytosis (testosterone, EPO)"
            ])
            
            # Add specific considerations based on test results
            jak2_status = parameters["jak2_mutation"]
            if jak2_status in ["jak2v617f_positive", "jak2_exon12_positive"]:
                differential.append("JAK2-positive myeloproliferative neoplasm (likely PV if other criteria met)")
            elif jak2_status == "negative":
                differential.append("JAK2-negative conditions (secondary causes more likely)")
        
        return differential
    
    def _generate_follow_up_recommendations(self, diagnosis_result: Dict[str, Any], 
                                          criteria_assessment: Dict[str, Any]) -> List[str]:
        """Generates follow-up recommendations"""
        
        follow_up = []
        status = diagnosis_result["status"]
        
        if status == "diagnosis_met":
            follow_up.extend([
                "Regular hematology follow-up every 3-6 months",
                "Monitor complete blood count monthly until stable",
                "Annual assessment for thrombotic/bleeding complications",
                "Periodic evaluation for disease progression or transformation",
                "Genetic counseling if familial MPN history"
            ])
        elif status == "probable_pv":
            follow_up.extend([
                "Complete missing diagnostic tests within 4-6 weeks",
                "Repeat hematologic evaluation in 3 months",
                "Monitor for symptom development or progression",
                "Consider interim phlebotomy if symptomatic"
            ])
        else:
            follow_up.extend([
                "Investigate and treat underlying causes of erythrocytosis",
                "Repeat blood work in 4-8 weeks after addressing secondary causes",
                "Consider specialist referral if erythrocytosis persists",
                "Monitor for development of additional MPN features"
            ])
        
        # Add specific follow-up based on missing tests
        missing_tests = []
        criteria_details = criteria_assessment["criteria_details"]
        
        if "not_performed" in criteria_details["major_criterion_2"]["details"]:
            missing_tests.append("bone marrow biopsy")
        if "not_tested" in criteria_details["major_criterion_3"]["details"]:
            missing_tests.append("JAK2 mutation testing")
        if "not_measured" in criteria_details["minor_criterion_1"]["details"]:
            missing_tests.append("serum erythropoietin level")
        
        if missing_tests:
            follow_up.append(f"Complete missing tests: {', '.join(missing_tests)}")
        
        return follow_up


def calculate_who_polycythemia_vera_criteria(gender, hemoglobin, hematocrit, red_cell_mass_elevated,
                                           bone_marrow_hypercellular, jak2_mutation, erythropoietin_level) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_who_polycythemia_vera_criteria pattern
    """
    calculator = WhoPolycythemiaVeraCriteriaCalculator()
    return calculator.calculate(
        gender, hemoglobin, hematocrit, red_cell_mass_elevated,
        bone_marrow_hypercellular, jak2_mutation, erythropoietin_level
    )