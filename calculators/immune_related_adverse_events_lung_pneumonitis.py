"""
Immune-Related Adverse Events for Lung Toxicity - Pneumonitis Calculator

Grades severity of pneumonitis secondary to immune checkpoint inhibitor (ICPi) therapy 
based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria.

This calculator evaluates respiratory symptoms, functional impact, oxygen requirements, 
and radiographic findings to determine the severity of immune-mediated pneumonitis and 
provides evidence-based management recommendations for ICPi therapy decisions.

References (Vancouver style):
1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
   Management of Immune-Related Adverse Events in Patients Treated With Immune 
   Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
   Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
   doi: 10.1200/JCO.2017.77.6385.
2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
   NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
   Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
   doi: 10.6004/jnccn.2020.0012.
3. Nishino M, Giobbie-Hurder A, Hatabu H, Ramaiya NH, Hodi FS. Incidence of 
   Programmed Cell Death 1 Inhibitor-Related Pneumonitis in Patients With Advanced 
   Cancer: A Systematic Review and Meta-analysis. JAMA Oncol. 2016 Dec 1;2(12):1607-1616. 
   doi: 10.1001/jamaoncol.2016.2453.
4. Naidoo J, Wang X, Woo KM, Iyriboz T, Halpenny D, Cunningham J, et al. Pneumonitis 
   in Patients Treated With Anti-Programmed Death-1/Programmed Death Ligand 1 Therapy. 
   J Clin Oncol. 2017 Mar 10;35(7):709-717. doi: 10.1200/JCO.2016.68.2005.
"""

from typing import Dict, Any


class ImmuneRelatedAdverseEventsLungPneumonitisCalculator:
    """Calculator for Immune-Related Adverse Events for Lung Toxicity - Pneumonitis"""
    
    def __init__(self):
        # CTCAE v5.0 grading criteria weights and thresholds
        self.symptom_scores = {
            "asymptomatic": 0,
            "mild": 1,
            "moderate": 2,
            "severe": 3
        }
        
        self.functional_scores = {
            "none": 0,
            "limiting_instrumental_adls": 1,
            "limiting_self_care_adls": 2,
            "life_threatening": 3
        }
        
        self.oxygen_scores = {
            "room_air": 0,
            "low_flow_oxygen": 1,
            "high_flow_oxygen": 2,
            "mechanical_ventilation": 3
        }
        
        self.radiographic_scores = {
            "normal": 0,
            "minimal": 1,
            "moderate": 2,
            "extensive": 3
        }
    
    def calculate(self, respiratory_symptoms: str, functional_impact: str, 
                 oxygen_requirement: str, radiographic_findings: str,
                 hospitalization_indicated: str) -> Dict[str, Any]:
        """
        Calculates the CTCAE grade for immune-related pneumonitis
        
        Args:
            respiratory_symptoms (str): Presence and severity of respiratory symptoms
            functional_impact (str): Impact on activities of daily living
            oxygen_requirement (str): Need for supplemental oxygen or respiratory support
            radiographic_findings (str): Extent of radiographic involvement
            hospitalization_indicated (str): Clinical indication for hospitalization
            
        Returns:
            Dict with the grade and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(respiratory_symptoms, functional_impact, oxygen_requirement,
                            radiographic_findings, hospitalization_indicated)
        
        # Determine grade based on CTCAE criteria
        grade = self._calculate_grade(respiratory_symptoms, functional_impact, 
                                    oxygen_requirement, radiographic_findings,
                                    hospitalization_indicated)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, respiratory_symptoms: str, functional_impact: str,
                        oxygen_requirement: str, radiographic_findings: str,
                        hospitalization_indicated: str):
        """Validates input parameters"""
        
        # Validate respiratory symptoms
        if respiratory_symptoms not in self.symptom_scores:
            raise ValueError("Respiratory symptoms must be one of: asymptomatic, mild, moderate, severe")
        
        # Validate functional impact
        if functional_impact not in self.functional_scores:
            raise ValueError("Functional impact must be one of: none, limiting_instrumental_adls, limiting_self_care_adls, life_threatening")
        
        # Validate oxygen requirement
        if oxygen_requirement not in self.oxygen_scores:
            raise ValueError("Oxygen requirement must be one of: room_air, low_flow_oxygen, high_flow_oxygen, mechanical_ventilation")
        
        # Validate radiographic findings
        if radiographic_findings not in self.radiographic_scores:
            raise ValueError("Radiographic findings must be one of: normal, minimal, moderate, extensive")
        
        # Validate hospitalization indication
        if hospitalization_indicated not in ["yes", "no"]:
            raise ValueError("Hospitalization indicated must be 'yes' or 'no'")
    
    def _calculate_grade(self, respiratory_symptoms: str, functional_impact: str,
                        oxygen_requirement: str, radiographic_findings: str,
                        hospitalization_indicated: str) -> int:
        """
        Determines CTCAE grade based on symptoms, functional impact, oxygen needs, and imaging
        
        CTCAE v5.0 grading criteria for pneumonitis:
        - Grade 1: Asymptomatic; clinical or diagnostic observations only
        - Grade 2: Symptomatic; limiting instrumental ADLs
        - Grade 3: Severe symptoms; limiting self-care ADLs; oxygen indicated
        - Grade 4: Life-threatening respiratory compromise; urgent intervention indicated
        """
        
        # Grade 4: Life-threatening respiratory compromise
        if (functional_impact == "life_threatening" or 
            oxygen_requirement == "mechanical_ventilation" or
            (oxygen_requirement == "high_flow_oxygen" and respiratory_symptoms == "severe")):
            return 4
        
        # Grade 3: Severe symptoms limiting self-care ADLs; oxygen indicated
        if (functional_impact == "limiting_self_care_adls" or
            oxygen_requirement in ["low_flow_oxygen", "high_flow_oxygen"] or
            (respiratory_symptoms == "severe" and hospitalization_indicated == "yes")):
            return 3
        
        # Grade 2: Symptomatic; limiting instrumental ADLs
        if (respiratory_symptoms in ["mild", "moderate", "severe"] or
            functional_impact == "limiting_instrumental_adls" or
            hospitalization_indicated == "yes"):
            return 2
        
        # Grade 1: Asymptomatic; clinical or diagnostic observations only
        if (respiratory_symptoms == "asymptomatic" and 
            radiographic_findings != "normal"):
            return 1
        
        # If normal imaging and asymptomatic, default to Grade 1 (minimal findings)
        return 1
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Provides clinical interpretation and management recommendations based on grade
        
        Args:
            grade (int): CTCAE grade (1-4)
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        interpretations = {
            1: {
                "stage": "Grade 1",
                "description": "Mild - Asymptomatic; clinical or diagnostic observations only",
                "interpretation": "Continue ICPi with close monitoring. Repeat chest imaging in 3-4 weeks. Rule out alternative causes (infection, progression, radiation pneumonitis). Monitor pulmonary function tests. Consider pulmonology consultation if persistent. Hold ICPi if symptoms develop or imaging worsens."
            },
            2: {
                "stage": "Grade 2",
                "description": "Moderate - Symptomatic; limiting instrumental ADLs",
                "interpretation": "Hold ICPi until symptoms improve to grade ≤1. Start corticosteroids (prednisone 1 mg/kg/day or equivalent). Obtain pulmonology consultation. Rule out infectious causes with bronchoscopy if indicated. Consider hospitalization for close monitoring. Repeat chest imaging in 3-5 days. Resume ICPi when grade ≤1 and steroids tapered."
            },
            3: {
                "stage": "Grade 3",
                "description": "Severe - Limiting self-care ADLs; oxygen indicated",
                "interpretation": "Permanently discontinue ICPi. Immediate hospitalization required. Start high-dose corticosteroids (methylprednisolone 2-4 mg/kg/day IV). Urgent pulmonology and intensive care consultation. Bronchoscopy to rule out infection. If no improvement in 48-72 hours, add mycophenolate mofetil, infliximab, or cyclophosphamide. Monitor for respiratory failure."
            },
            4: {
                "stage": "Grade 4",
                "description": "Life-threatening - Life-threatening respiratory compromise; urgent intervention indicated",
                "interpretation": "Permanently discontinue ICPi. Immediate ICU admission required. Start high-dose IV corticosteroids (methylprednisolone 2-4 mg/kg/day). Urgent pulmonology and critical care consultation. Consider mechanical ventilation support. Bronchoscopy when stable. Add second-line immunosuppressants (infliximab, cyclophosphamide, IVIG) if refractory to steroids. Consider plasmapheresis for refractory cases."
            }
        }
        
        return interpretations.get(grade, interpretations[1])


def calculate_immune_related_adverse_events_lung_pneumonitis(respiratory_symptoms: str, 
                                                           functional_impact: str,
                                                           oxygen_requirement: str, 
                                                           radiographic_findings: str,
                                                           hospitalization_indicated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImmuneRelatedAdverseEventsLungPneumonitisCalculator()
    return calculator.calculate(respiratory_symptoms, functional_impact, oxygen_requirement,
                              radiographic_findings, hospitalization_indicated)