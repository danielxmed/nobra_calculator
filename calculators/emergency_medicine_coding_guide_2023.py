"""
2023 Emergency Medicine Coding Guide Calculator

Rates the level of service required in emergency medicine based on 2023 AMA CPT 
Evaluation and Management (E/M) coding changes. Determines appropriate emergency 
department service level (99281-99285) based on medical decision making components.

References:
- American Medical Association. CPT® Evaluation and Management (E/M) Code and Guideline Changes. 2023
- MDCalc: 2023 Emergency Medicine Coding Guide
"""

from typing import Dict, Any


class EmergencyMedicineCodingGuide2023Calculator:
    """Calculator for 2023 Emergency Medicine Coding Guide"""
    
    def __init__(self):
        # MDM level scoring constants
        self.RISK_LEVELS = {
            "minimal": 0,
            "low": 1, 
            "moderate": 2,
            "high": 3
        }
        
    def calculate(self, number_complexity_problems: int, tests_ordered: int, 
                 tests_reviewed: int, prior_notes_reviewed: int,
                 independent_historian: str, independent_interpretation: str,
                 external_discussion: str, risk_level: str) -> Dict[str, Any]:
        """
        Calculates Emergency Medicine service level using 2023 coding guidelines
        
        Args:
            number_complexity_problems (int): Complexity score for problems (2-5)
            tests_ordered (int): Number of unique tests ordered
            tests_reviewed (int): Number of test results reviewed
            prior_notes_reviewed (int): Number of prior external notes reviewed
            independent_historian (str): Whether independent historian was used
            independent_interpretation (str): Whether independent interpretation was done
            external_discussion (str): Whether external discussion occurred
            risk_level (str): Risk level (minimal, low, moderate, high)
            
        Returns:
            Dict with the service level and interpretation
        """
        
        # Validations
        self._validate_inputs(number_complexity_problems, tests_ordered, tests_reviewed,
                            prior_notes_reviewed, independent_historian, 
                            independent_interpretation, external_discussion, risk_level)
        
        # Calculate data complexity score
        data_score = self._calculate_data_complexity(
            tests_ordered, tests_reviewed, prior_notes_reviewed,
            independent_historian, independent_interpretation, external_discussion
        )
        
        # Get risk score
        risk_score = self.RISK_LEVELS[risk_level]
        
        # Determine MDM level based on 2 of 3 criteria
        mdm_level = self._determine_mdm_level(number_complexity_problems, data_score, risk_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(mdm_level)
        
        return {
            "result": interpretation["stage"],
            "unit": "CPT code",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, number_complexity_problems, tests_ordered, tests_reviewed,
                        prior_notes_reviewed, independent_historian, 
                        independent_interpretation, external_discussion, risk_level):
        """Validates input parameters"""
        
        if not isinstance(number_complexity_problems, int) or number_complexity_problems < 2 or number_complexity_problems > 5:
            raise ValueError("Number/complexity of problems must be integer between 2 and 5")
        
        if not isinstance(tests_ordered, int) or tests_ordered < 0:
            raise ValueError("Tests ordered must be non-negative integer")
            
        if not isinstance(tests_reviewed, int) or tests_reviewed < 0:
            raise ValueError("Tests reviewed must be non-negative integer")
            
        if not isinstance(prior_notes_reviewed, int) or prior_notes_reviewed < 0:
            raise ValueError("Prior notes reviewed must be non-negative integer")
        
        valid_yes_no = ["yes", "no"]
        if independent_historian not in valid_yes_no:
            raise ValueError("Independent historian must be 'yes' or 'no'")
            
        if independent_interpretation not in valid_yes_no:
            raise ValueError("Independent interpretation must be 'yes' or 'no'")
            
        if external_discussion not in valid_yes_no:
            raise ValueError("External discussion must be 'yes' or 'no'")
        
        if risk_level not in self.RISK_LEVELS:
            raise ValueError("Risk level must be 'minimal', 'low', 'moderate', or 'high'")
    
    def _calculate_data_complexity(self, tests_ordered, tests_reviewed, prior_notes_reviewed,
                                 independent_historian, independent_interpretation, external_discussion):
        """Calculates data complexity score based on 2023 guidelines"""
        
        # Category 1: Tests, documents, orders, or independent historian
        category1_score = 0
        if tests_ordered >= 3:
            category1_score = 3
        elif tests_ordered == 2:
            category1_score = 2
        elif tests_ordered == 1:
            category1_score = 1
            
        if tests_reviewed >= 3:
            category1_score = max(category1_score, 3)
        elif tests_reviewed == 2:
            category1_score = max(category1_score, 2)
        elif tests_reviewed == 1:
            category1_score = max(category1_score, 1)
            
        if prior_notes_reviewed >= 3:
            category1_score = max(category1_score, 3)
        elif prior_notes_reviewed == 2:
            category1_score = max(category1_score, 2)
        elif prior_notes_reviewed == 1:
            category1_score = max(category1_score, 1)
            
        if independent_historian == "yes":
            category1_score = max(category1_score, 1)
        
        # Category 2: Independent interpretation
        category2_score = 1 if independent_interpretation == "yes" else 0
        
        # Category 3: Discussion with external professional
        category3_score = 1 if external_discussion == "yes" else 0
        
        # Determine overall data complexity level
        # Limited: Category 1 (at least 1 of 2) = any 1 element OR assessment requiring independent historian
        # Moderate: Category 1 (any combination of 3) OR Category 2 OR Category 3
        # Extensive: Category 1 (any combination of 3) AND (Category 2 OR Category 3)
        
        if category1_score >= 3 and (category2_score == 1 or category3_score == 1):
            return 3  # Extensive
        elif category1_score >= 3 or category2_score == 1 or category3_score == 1:
            return 2  # Moderate  
        elif category1_score >= 1:
            return 1  # Limited
        else:
            return 0  # Minimal
    
    def _determine_mdm_level(self, problems_score, data_score, risk_score):
        """Determines MDM level based on 2 of 3 criteria"""
        
        # Convert scores to MDM levels (0=straightforward, 1=low, 2=moderate, 3=high)
        problem_level = min(problems_score - 2, 3)  # 2->0, 3->1, 4->2, 5->3
        data_level = min(data_score, 3)  # 0->0, 1->1, 2->2, 3->3
        risk_level = min(risk_score, 3)  # 0->0, 1->1, 2->2, 3->3
        
        # Count how many criteria meet each level
        levels = [problem_level, data_level, risk_level]
        levels.sort(reverse=True)
        
        # Take the second highest (2 of 3 rule)
        return levels[1]
    
    def _get_interpretation(self, mdm_level: int) -> Dict[str, str]:
        """
        Determines the ED service level based on MDM level
        
        Args:
            mdm_level (int): Medical decision making level (0-3)
            
        Returns:
            Dict with CPT code and interpretation
        """
        
        if mdm_level == 0:
            return {
                "stage": "99281",
                "description": "Level 1 ED Visit",
                "interpretation": "Emergency department visit that may not require the presence of a physician or other qualified health care professional. Straightforward medical decision making or no MDM required."
            }
        elif mdm_level == 1:
            return {
                "stage": "99282",
                "description": "Level 2 ED Visit", 
                "interpretation": "Emergency department visit requiring straightforward medical decision making. Simple, routine case with minimal complexity."
            }
        elif mdm_level == 2:
            return {
                "stage": "99283",
                "description": "Level 3 ED Visit",
                "interpretation": "Emergency department visit requiring low level of medical decision making. Limited complexity with some data review or minimal risk."
            }
        elif mdm_level == 3:
            return {
                "stage": "99284",
                "description": "Level 4 ED Visit",
                "interpretation": "Emergency department visit requiring moderate level of medical decision making. Moderate complexity with multiple problems, data analysis, or moderate risk."
            }
        else:  # mdm_level >= 4
            return {
                "stage": "99285",
                "description": "Level 5 ED Visit",
                "interpretation": "Emergency department visit requiring high level of medical decision making. High complexity with extensive problems, significant data analysis, or high risk of complications."
            }


def calculate_emergency_medicine_coding_guide_2023(number_complexity_problems: int, tests_ordered: int,
                                                  tests_reviewed: int, prior_notes_reviewed: int,
                                                  independent_historian: str, independent_interpretation: str,
                                                  external_discussion: str, risk_level: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = EmergencyMedicineCodingGuide2023Calculator()
    return calculator.calculate(number_complexity_problems, tests_ordered, tests_reviewed,
                              prior_notes_reviewed, independent_historian, 
                              independent_interpretation, external_discussion, risk_level)