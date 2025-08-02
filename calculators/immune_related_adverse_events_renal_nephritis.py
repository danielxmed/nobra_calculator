"""
Immune-Related Adverse Events for Renal Toxicities - Nephritis Calculator

Grades severity of nephritis secondary to immune checkpoint inhibitor (ICPi) therapy 
based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria.

This calculator evaluates serum creatinine levels, renal function changes, and clinical 
symptoms to determine the severity of immune-mediated nephritis and provides evidence-based 
management recommendations for ICPi therapy decisions.

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
3. Cortazar FB, Marrone KA, Troxel AB, Ralto KM, Hoenig MP, Brahmer JR, et al. 
   Clinicopathological features of acute kidney injury associated with immune 
   checkpoint inhibitors. Kidney Int. 2016 Sep;90(3):638-47. 
   doi: 10.1016/j.kint.2016.04.008.
4. Shirali AC, Perazella MA, Gettinger S. Association of Acute Interstitial 
   Nephritis With Programmed Cell Death 1 Inhibitor Therapy in Lung Cancer Patients. 
   Am J Kidney Dis. 2016 Aug;68(2):287-91. doi: 10.1053/j.ajkd.2016.02.057.
"""

from typing import Dict, Any


class ImmuneRelatedAdverseEventsRenalNephritisCalculator:
    """Calculator for Immune-Related Adverse Events for Renal Toxicities - Nephritis"""
    
    def __init__(self):
        # CTCAE v5.0 grading thresholds for creatinine fold increase
        self.creatinine_thresholds = {
            "grade_1": {
                "min_fold": 1.5,
                "max_fold": 2.0
            },
            "grade_2": {
                "min_fold": 2.0,
                "max_fold": 3.0
            },
            "grade_3": {
                "min_fold": 3.0,
                "max_fold": 6.0
            },
            "grade_4": {
                "min_fold": 6.0
            }
        }
    
    def calculate(self, baseline_creatinine: float, current_creatinine: float, 
                 proteinuria_present: str, hematuria_present: str, 
                 clinical_symptoms: str, fluid_retention: str,
                 dialysis_required: str) -> Dict[str, Any]:
        """
        Calculates the CTCAE grade for immune-related nephritis
        
        Args:
            baseline_creatinine (float): Baseline creatinine level in mg/dL
            current_creatinine (float): Current creatinine level in mg/dL
            proteinuria_present (str): Presence of proteinuria ("yes" or "no")
            hematuria_present (str): Presence of hematuria ("yes" or "no")
            clinical_symptoms (str): Severity of clinical symptoms
            fluid_retention (str): Presence of fluid retention ("yes" or "no")
            dialysis_required (str): Need for dialysis ("yes" or "no")
            
        Returns:
            Dict with the grade and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(baseline_creatinine, current_creatinine, proteinuria_present,
                            hematuria_present, clinical_symptoms, fluid_retention, dialysis_required)
        
        # Calculate creatinine fold increase
        creatinine_fold = current_creatinine / baseline_creatinine
        
        # Determine grade based on CTCAE criteria
        grade = self._calculate_grade(creatinine_fold, proteinuria_present, hematuria_present,
                                    clinical_symptoms, fluid_retention, dialysis_required)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, baseline_creatinine: float, current_creatinine: float,
                        proteinuria_present: str, hematuria_present: str,
                        clinical_symptoms: str, fluid_retention: str, dialysis_required: str):
        """Validates input parameters"""
        
        # Validate creatinine values
        if not isinstance(baseline_creatinine, (int, float)) or baseline_creatinine <= 0.3 or baseline_creatinine > 15.0:
            raise ValueError("Baseline creatinine must be a number between 0.3 and 15.0 mg/dL")
        
        if not isinstance(current_creatinine, (int, float)) or current_creatinine <= 0.3 or current_creatinine > 30.0:
            raise ValueError("Current creatinine must be a number between 0.3 and 30.0 mg/dL")
        
        # Validate binary parameters
        if proteinuria_present not in ["yes", "no"]:
            raise ValueError("Proteinuria present must be 'yes' or 'no'")
        
        if hematuria_present not in ["yes", "no"]:
            raise ValueError("Hematuria present must be 'yes' or 'no'")
        
        if fluid_retention not in ["yes", "no"]:
            raise ValueError("Fluid retention must be 'yes' or 'no'")
        
        if dialysis_required not in ["yes", "no"]:
            raise ValueError("Dialysis required must be 'yes' or 'no'")
        
        # Validate clinical symptoms
        if clinical_symptoms not in ["asymptomatic", "mild", "moderate", "severe"]:
            raise ValueError("Clinical symptoms must be one of: asymptomatic, mild, moderate, severe")
    
    def _calculate_grade(self, creatinine_fold: float, proteinuria_present: str,
                        hematuria_present: str, clinical_symptoms: str,
                        fluid_retention: str, dialysis_required: str) -> int:
        """
        Determines CTCAE grade based on creatinine fold increase and clinical factors
        
        CTCAE v5.0 grading criteria for nephritis:
        - Grade 1: Creatinine 1.5-2× baseline
        - Grade 2: Creatinine 2-3× baseline  
        - Grade 3: Creatinine >3-6× baseline
        - Grade 4: Creatinine >6× baseline OR dialysis required
        """
        
        # Grade 4: Dialysis required overrides all other criteria
        if dialysis_required == "yes":
            return 4
        
        # Grade 4: Creatinine >6× baseline
        if creatinine_fold > self.creatinine_thresholds["grade_4"]["min_fold"]:
            return 4
        
        # Grade 3: Creatinine >3-6× baseline
        if creatinine_fold > self.creatinine_thresholds["grade_3"]["min_fold"]:
            return 3
        
        # Grade 2: Creatinine 2-3× baseline
        if creatinine_fold >= self.creatinine_thresholds["grade_2"]["min_fold"]:
            return 2
        
        # Grade 1: Creatinine 1.5-2× baseline
        if creatinine_fold >= self.creatinine_thresholds["grade_1"]["min_fold"]:
            return 1
        
        # Special consideration: If creatinine fold is <1.5 but there are concerning features,
        # still classify as Grade 1 (early nephritis)
        if (proteinuria_present == "yes" or hematuria_present == "yes" or 
            clinical_symptoms in ["mild", "moderate", "severe"] or fluid_retention == "yes"):
            return 1
        
        # If no significant creatinine increase and no concerning features, default to Grade 1
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
                "description": "Mild - Creatinine 1.5-2× baseline",
                "interpretation": "Continue ICPi with close monitoring. Repeat creatinine and urinalysis in 1-2 weeks. Rule out alternative causes (dehydration, medications, contrast, obstruction). Consider nephrology consultation if persistent. Monitor for progression to higher grades. Ensure adequate hydration."
            },
            2: {
                "stage": "Grade 2",
                "description": "Moderate - Creatinine 2-3× baseline",
                "interpretation": "Hold ICPi until creatinine improves to grade ≤1. Start corticosteroids (prednisone 1 mg/kg/day or equivalent). Obtain nephrology consultation. Rule out infectious and obstructive causes. Consider kidney biopsy if diagnosis unclear or no improvement. Monitor creatinine closely. Resume ICPi when grade ≤1 and steroids tapered."
            },
            3: {
                "stage": "Grade 3",
                "description": "Severe - Creatinine >3-6× baseline",
                "interpretation": "Permanently discontinue ICPi. Start high-dose corticosteroids (methylprednisolone 1-2 mg/kg/day). Urgent nephrology consultation required. Consider hospitalization for monitoring. Kidney biopsy strongly recommended. If no improvement in 3-5 days, add mycophenolate mofetil or other immunosuppressants. Monitor for need for dialysis."
            },
            4: {
                "stage": "Grade 4",
                "description": "Life-threatening - Creatinine >6× baseline OR dialysis required",
                "interpretation": "Permanently discontinue ICPi. Immediate hospitalization required. Start high-dose IV corticosteroids (methylprednisolone 1-2 mg/kg/day). Urgent nephrology and intensive care consultation. Initiate renal replacement therapy if indicated. Kidney biopsy when stable. Add second-line immunosuppressants if refractory to steroids. Consider plasmapheresis for severe cases."
            }
        }
        
        return interpretations.get(grade, interpretations[1])


def calculate_immune_related_adverse_events_renal_nephritis(baseline_creatinine: float, 
                                                          current_creatinine: float,
                                                          proteinuria_present: str, 
                                                          hematuria_present: str,
                                                          clinical_symptoms: str, 
                                                          fluid_retention: str,
                                                          dialysis_required: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImmuneRelatedAdverseEventsRenalNephritisCalculator()
    return calculator.calculate(baseline_creatinine, current_creatinine, proteinuria_present,
                              hematuria_present, clinical_symptoms, fluid_retention, dialysis_required)