"""
Los Angeles (LA) Grading of Esophagitis Calculator

Classifies severity of erosive esophagitis based on endoscopic findings.
Recommended by ACG guidelines for standardized reporting and treatment decisions.

References:
1. Lundell LR, Dent J, Bennett JR, Blum AL, Armstrong D, Galmiche JP, et al. 
   Endoscopic assessment of oesophagitis: clinical and functional correlates and 
   further validation of the Los Angeles classification. Gut. 1999 Aug;45(2):172-80.
2. Katz PO, Gerson LB, Vela MF. Guidelines for the diagnosis and management of 
   gastroesophageal reflux disease. Am J Gastroenterol. 2013 Mar;108(3):308-28.
"""

from typing import Dict, Any


class LosAngelesGradingEsophagitisCalculator:
    """Calculator for Los Angeles Grading of Esophagitis"""
    
    def __init__(self):
        # Grade definitions based on mucosal break characteristics
        self.GRADE_DEFINITIONS = {
            "breaks_5mm_or_less_no_continuity": {
                "grade": "A",
                "severity": "Mild",
                "ppi_duration": 4,
                "description": "Mucosal break(s) ≤5 mm, without continuity across mucosal folds"
            },
            "breaks_greater_than_5mm_no_continuity": {
                "grade": "B", 
                "severity": "Mild",
                "ppi_duration": 4,
                "description": "Mucosal break(s) >5 mm, without continuity across mucosal folds"
            },
            "breaks_continuous_between_folds_less_than_75_percent": {
                "grade": "C",
                "severity": "Severe",
                "ppi_duration": 8,
                "description": "Mucosal break(s) continuous between ≥2 mucosal folds, involving <75% of esophageal circumference"
            },
            "breaks_75_percent_or_more_circumference": {
                "grade": "D",
                "severity": "Severe", 
                "ppi_duration": 8,
                "description": "Mucosal break(s) involving ≥75% of esophageal circumference"
            }
        }
        
        # Treatment recommendations by grade
        self.TREATMENT_RECOMMENDATIONS = {
            "A": {
                "ppi_therapy": "Standard-dose PPI for 4 weeks",
                "additional_testing": "Consider further testing to confirm GERD diagnosis per ACG guidelines",
                "follow_up": "Evaluate response to therapy and consider step-down approach",
                "surgical_consideration": "Not typically indicated"
            },
            "B": {
                "ppi_therapy": "Standard-dose PPI for 4 weeks", 
                "additional_testing": "Clinical diagnosis usually sufficient",
                "follow_up": "Evaluate response to therapy and consider step-down approach",
                "surgical_consideration": "Consider if symptoms persist despite optimal medical therapy"
            },
            "C": {
                "ppi_therapy": "Standard-dose PPI for 8 weeks",
                "additional_testing": "Repeat endoscopy after PPI therapy to assess healing",
                "follow_up": "Consider maintenance therapy if symptoms recur",
                "surgical_consideration": "Consider antireflux surgery for persistent symptoms or complications"
            },
            "D": {
                "ppi_therapy": "Standard-dose PPI for 8 weeks",
                "additional_testing": "Repeat endoscopy after PPI therapy to exclude Barrett's esophagus",
                "follow_up": "Likely requires maintenance PPI therapy",
                "surgical_consideration": "Strong consideration for antireflux surgery, especially with large hiatal hernia"
            }
        }
    
    def calculate(self, mucosal_break_size: str) -> Dict[str, Any]:
        """
        Classifies esophagitis severity based on endoscopic findings
        
        Args:
            mucosal_break_size (str): Description of mucosal break characteristics
            
        Returns:
            Dict with LA grade and clinical recommendations
        """
        
        # Validate input
        self._validate_input(mucosal_break_size)
        
        # Get grade information
        grade_info = self.GRADE_DEFINITIONS[mucosal_break_size]
        grade = grade_info["grade"]
        
        # Get treatment recommendations
        treatment = self.TREATMENT_RECOMMENDATIONS[grade]
        
        # Generate interpretation
        interpretation = self._get_interpretation(grade_info, treatment)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_input(self, mucosal_break_size):
        """Validates input parameter"""
        
        if mucosal_break_size not in self.GRADE_DEFINITIONS:
            valid_options = list(self.GRADE_DEFINITIONS.keys())
            raise ValueError(f"Mucosal break size must be one of: {valid_options}")
    
    def _get_interpretation(self, grade_info, treatment):
        """
        Provides comprehensive clinical interpretation and management recommendations
        """
        
        grade = grade_info["grade"]
        severity = grade_info["severity"]
        description = grade_info["description"]
        ppi_duration = grade_info["ppi_duration"]
        
        # Build comprehensive interpretation
        interpretation = (
            f"Los Angeles Grade {grade} Esophagitis Classification:\n\n"
            f"Endoscopic Findings:\n"
            f"• {description}\n"
            f"• Severity: {severity} reflux esophagitis\n\n"
            f"Treatment Recommendations:\n"
            f"• Primary therapy: {treatment['ppi_therapy']}\n"
            f"• Additional testing: {treatment['additional_testing']}\n"
            f"• Follow-up: {treatment['follow_up']}\n"
            f"• Surgical consideration: {treatment['surgical_consideration']}\n\n"
            f"Clinical Management Guidelines:\n"
        )
        
        if grade in ["A", "B"]:
            interpretation += (
                f"• Mild esophagitis - good prognosis with PPI therapy\n"
                f"• Lifestyle modifications: weight loss, head of bed elevation, avoid trigger foods\n"
                f"• Consider step-down therapy after symptom resolution\n"
                f"• Maintenance therapy usually not required unless symptoms recur\n"
                f"• Monitor for symptom improvement within 2-4 weeks\n"
            )
        else:  # Grades C, D
            interpretation += (
                f"• Severe esophagitis - requires aggressive treatment and close monitoring\n"
                f"• Lifestyle modifications essential: weight loss, head of bed elevation, dietary changes\n" 
                f"• Higher risk of complications: stricture, Barrett's esophagus, bleeding\n"
                f"• Maintenance PPI therapy often required to prevent recurrence\n"
                f"• Consider H. pylori testing and eradication if positive\n"
                f"• Evaluate for underlying conditions: large hiatal hernia, delayed gastric emptying\n"
            )
            
            if grade == "D":
                interpretation += (
                    f"• Highest grade - comprehensive evaluation for surgical candidacy\n"
                    f"• Screen for Barrett's esophagus with repeat endoscopy after healing\n"
                    f"• Consider esophageal pH monitoring or impedance testing\n"
                    f"• Evaluate for antireflux surgery, especially in young patients\n"
                )
        
        interpretation += (
            f"\nKey Clinical Considerations:\n"
            f"• LA Classification applies only to erosive esophagitis (visible mucosal breaks)\n"
            f"• Non-erosive reflux disease (NERD) requires different diagnostic approach\n"
            f"• Inter-observer agreement is excellent for LA Classification\n"
            f"• Standardized reporting improves communication and treatment consistency\n"
            f"• Consider comorbidities that may affect PPI response or surgical candidacy\n"
            f"• Patient age, symptoms, and preferences should guide treatment decisions"
        )
        
        return {
            "stage": f"Grade {grade}",
            "stage_description": f"{severity} reflux esophagitis", 
            "interpretation": interpretation
        }


def calculate_los_angeles_grading_esophagitis(mucosal_break_size: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_los_angeles_grading_esophagitis pattern
    """
    calculator = LosAngelesGradingEsophagitisCalculator()
    return calculator.calculate(mucosal_break_size)