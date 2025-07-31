"""
Grogan Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM) Calculator

The Grogan Staging System classifies prognosis of patients with wild-type transthyretin 
amyloid cardiomyopathy using cardiac biomarkers NT-proBNP and troponin T. This staging 
system helps inform goals of care discussions, therapeutic decisions, and can stratify 
patients for clinical trials.

The staging system was developed at Mayo Clinic and uses two key cardiac biomarkers:
- NT-proBNP (N-terminal pro-B-type natriuretic peptide)
- Troponin T (cardiac troponin T)

Clinical Applications:
- Risk stratification for wild-type ATTR-CM patients
- Prognosis estimation with 4-year survival rates
- Treatment planning and therapeutic decision-making
- Clinical trial stratification
- Goals of care discussions with patients and families

References (Vancouver style):
1. Grogan M, Scott CG, Kyle RA, et al. Natural history of wild-type transthyretin 
   cardiac amyloidosis and risk stratification using a novel staging system. J Am 
   Coll Cardiol. 2016;68(10):1014-1020. doi: 10.1016/j.jacc.2016.06.033
2. Cappelli F, Baldasseroni S, Bergesio F, et al. Biomarker-based staging system 
   for cardiac transthyretin-related amyloidosis. Eur J Heart Fail. 2020;22(11):2187-2196. 
   doi: 10.1002/ejhf.1898
3. Maurer MS, Hanna M, Grogan M, et al. Genotype and phenotype of transthyretin 
   cardiac amyloidosis: THAOS (Transthyretin Amyloid Outcome Survey). J Am Coll 
   Cardiol. 2016;68(2):161-172. doi: 10.1016/j.jacc.2016.03.596
"""

from typing import Dict, Any


class GroganStagingAttrCmCalculator:
    """Calculator for Grogan Staging System for ATTR-CM"""
    
    def __init__(self):
        # Biomarker thresholds for staging
        self.NT_PROBNP_THRESHOLD = 3000.0  # pg/mL
        self.TROPONIN_T_THRESHOLD = 0.05   # ng/mL
        
        # Staging definitions with survival outcomes
        self.STAGING_DEFINITIONS = {
            "Stage I": {
                "criteria": "NT-proBNP ≤3000 pg/mL AND Troponin T ≤0.05 ng/mL",
                "description": "Best prognosis",
                "four_year_survival": 57,
                "median_survival_months": 66,
                "clinical_implications": (
                    "Excellent prognosis with lowest cardiac biomarker burden. Consider early "
                    "disease-modifying therapy. Appropriate for aggressive interventions and "
                    "clinical trial enrollment. Regular monitoring recommended to detect disease progression."
                )
            },
            "Stage II": {
                "criteria": "One biomarker above threshold",
                "description": "Intermediate prognosis", 
                "four_year_survival": 42,
                "median_survival_months": 42,
                "clinical_implications": (
                    "Intermediate prognosis with moderate cardiac biomarker elevation. Disease-modifying "
                    "therapy strongly indicated. Multidisciplinary team approach recommended. Consider "
                    "supportive heart failure therapies and monitoring for disease progression."
                )
            },
            "Stage III": {
                "criteria": "NT-proBNP >3000 pg/mL AND Troponin T >0.05 ng/mL",
                "description": "Poor prognosis",
                "four_year_survival": 18,
                "median_survival_months": 20,
                "clinical_implications": (
                    "Poor prognosis with both biomarkers elevated indicating advanced cardiac involvement. "
                    "Urgent disease-modifying therapy consideration. Aggressive heart failure management "
                    "required. Consider advanced therapies including heart transplantation evaluation in "
                    "appropriate candidates. Focus on symptom management and quality of life."
                )
            }
        }
    
    def calculate(self, nt_probnp: float, troponin_t: float) -> Dict[str, Any]:
        """
        Calculates Grogan staging based on NT-proBNP and troponin T levels
        
        Args:
            nt_probnp (float): NT-proBNP level in pg/mL
            troponin_t (float): Troponin T level in ng/mL
            
        Returns:
            Dict with staging result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(nt_probnp, troponin_t)
        
        # Determine stage based on biomarker thresholds
        stage = self._determine_stage(nt_probnp, troponin_t)
        
        # Get staging information
        stage_info = self.STAGING_DEFINITIONS[stage]
        
        # Generate comprehensive interpretation
        interpretation = self._generate_interpretation(
            stage, nt_probnp, troponin_t, stage_info
        )
        
        return {
            "result": stage,
            "unit": "stage",
            "interpretation": interpretation,
            "stage": stage,
            "stage_description": stage_info["description"]
        }
    
    def _validate_inputs(self, nt_probnp: float, troponin_t: float):
        """Validates input parameters"""
        
        if not isinstance(nt_probnp, (int, float)):
            raise ValueError("NT-proBNP must be a number")
        
        if not isinstance(troponin_t, (int, float)):
            raise ValueError("Troponin T must be a number")
        
        if nt_probnp < 0:
            raise ValueError("NT-proBNP cannot be negative")
        
        if troponin_t < 0:
            raise ValueError("Troponin T cannot be negative")
        
        if nt_probnp > 50000:
            raise ValueError("NT-proBNP value seems unusually high (>50,000 pg/mL)")
        
        if troponin_t > 5.0:
            raise ValueError("Troponin T value seems unusually high (>5.0 ng/mL)")
    
    def _determine_stage(self, nt_probnp: float, troponin_t: float) -> str:
        """
        Determines Grogan stage based on biomarker levels
        
        Args:
            nt_probnp (float): NT-proBNP level in pg/mL
            troponin_t (float): Troponin T level in ng/mL
            
        Returns:
            str: Stage classification (Stage I, Stage II, or Stage III)
        """
        
        # Check if both biomarkers are below thresholds (Stage I)
        if nt_probnp <= self.NT_PROBNP_THRESHOLD and troponin_t <= self.TROPONIN_T_THRESHOLD:
            return "Stage I"
        
        # Check if both biomarkers are above thresholds (Stage III)
        elif nt_probnp > self.NT_PROBNP_THRESHOLD and troponin_t > self.TROPONIN_T_THRESHOLD:
            return "Stage III"
        
        # One biomarker above threshold (Stage II)
        else:
            return "Stage II"
    
    def _generate_interpretation(self, stage: str, nt_probnp: float, troponin_t: float, 
                               stage_info: Dict[str, Any]) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            stage (str): Determined Grogan stage
            nt_probnp (float): NT-proBNP level
            troponin_t (float): Troponin T level
            stage_info (Dict): Stage information from definitions
            
        Returns:
            str: Comprehensive clinical interpretation
        """
        
        # Format biomarker values
        nt_probnp_formatted = f"{nt_probnp:,.0f} pg/mL"
        troponin_t_formatted = f"{troponin_t:.3f} ng/mL"
        
        # Build biomarker summary
        biomarker_summary = (
            f"Biomarker levels: NT-proBNP {nt_probnp_formatted}, Troponin T {troponin_t_formatted}. "
        )
        
        # Add threshold comparison
        nt_probnp_status = "elevated" if nt_probnp > self.NT_PROBNP_THRESHOLD else "normal"
        troponin_t_status = "elevated" if troponin_t > self.TROPONIN_T_THRESHOLD else "normal"
        
        threshold_summary = (
            f"NT-proBNP is {nt_probnp_status} (threshold: {self.NT_PROBNP_THRESHOLD:,.0f} pg/mL), "
            f"Troponin T is {troponin_t_status} (threshold: {self.TROPONIN_T_THRESHOLD:.3f} ng/mL). "
        )
        
        # Add stage-specific information
        stage_summary = (
            f"Grogan Classification: {stage} ({stage_info['description']}). "
            f"Four-year survival: {stage_info['four_year_survival']}%. "
            f"Median survival: {stage_info['median_survival_months']} months. "
        )
        
        # Add clinical recommendations
        clinical_recommendations = f"Clinical implications: {stage_info['clinical_implications']} "
        
        # Add important clinical notes
        clinical_notes = (
            "Important considerations: This staging system is specifically validated for "
            "wild-type transthyretin amyloid cardiomyopathy (ATTRwt-CM). Should be used in "
            "conjunction with clinical assessment, imaging findings, and tissue diagnosis. "
            "Regular reassessment recommended as biomarkers may change with disease progression "
            "or treatment response. Consider multidisciplinary team approach for optimal management."
        )
        
        # Combine all components
        interpretation = (
            f"{biomarker_summary}{threshold_summary}{stage_summary}"
            f"{clinical_recommendations}{clinical_notes}"
        )
        
        return interpretation


def calculate_grogan_staging_attr_cm(nt_probnp: float, troponin_t: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_grogan_staging_attr_cm pattern
    """
    calculator = GroganStagingAttrCmCalculator()
    return calculator.calculate(nt_probnp, troponin_t)