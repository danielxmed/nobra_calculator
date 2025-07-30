"""
Clinical Dementia Rating (CDR) Scale Calculator

Stages dementia, including Alzheimer's disease, in elderly patients.

References:
1. Morris JC. The Clinical Dementia Rating (CDR): current version and scoring rules. 
   Neurology. 1993 Nov;43(11):2412-4.
2. Hughes CP, Berg L, Danziger WL, Coben LA, Martin RL. A new clinical scale for 
   the staging of dementia. Br J Psychiatry. 1982 Jun;140:566-72.
"""

from typing import Dict, Any, List


class ClinicalDementiaRatingCalculator:
    """Calculator for Clinical Dementia Rating (CDR) Scale"""
    
    def calculate(
        self,
        memory: str,
        orientation: str,
        judgment_problem_solving: str,
        community_affairs: str,
        home_hobbies: str,
        personal_care: str
    ) -> Dict[str, Any]:
        """
        Calculates the CDR global score and sum of boxes
        
        Args:
            memory: Memory domain score ("0", "0.5", "1", "2", "3")
            orientation: Orientation domain score ("0", "0.5", "1", "2", "3")
            judgment_problem_solving: Judgment/Problem Solving score ("0", "0.5", "1", "2", "3")
            community_affairs: Community Affairs score ("0", "0.5", "1", "2", "3")
            home_hobbies: Home and Hobbies score ("0", "0.5", "1", "2", "3")
            personal_care: Personal Care score ("0", "1", "2", "3")
            
        Returns:
            Dict with global CDR score, sum of boxes, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            memory, orientation, judgment_problem_solving,
            community_affairs, home_hobbies, personal_care
        )
        
        # Convert string scores to floats
        m_score = float(memory)
        scores = {
            'memory': m_score,
            'orientation': float(orientation),
            'judgment_problem_solving': float(judgment_problem_solving),
            'community_affairs': float(community_affairs),
            'home_hobbies': float(home_hobbies),
            'personal_care': float(personal_care)
        }
        
        # Calculate CDR Sum of Boxes
        cdr_sob = sum(scores.values())
        
        # Calculate Global CDR using Washington University algorithm
        global_cdr = self._calculate_global_cdr(scores)
        
        # Get interpretation
        interpretation = self._get_interpretation(global_cdr, cdr_sob)
        
        return {
            "result": {
                "global_cdr": global_cdr,
                "sum_of_boxes": cdr_sob
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(
        self, memory, orientation, judgment_problem_solving,
        community_affairs, home_hobbies, personal_care
    ):
        """Validates input parameters"""
        
        valid_scores = ["0", "0.5", "1", "2", "3"]
        valid_personal_care = ["0", "1", "2", "3"]  # No 0.5 for personal care
        
        # Validate memory
        if memory not in valid_scores:
            raise ValueError(f"Memory score must be one of {valid_scores}")
        
        # Validate orientation
        if orientation not in valid_scores:
            raise ValueError(f"Orientation score must be one of {valid_scores}")
        
        # Validate judgment/problem solving
        if judgment_problem_solving not in valid_scores:
            raise ValueError(f"Judgment/Problem Solving score must be one of {valid_scores}")
        
        # Validate community affairs
        if community_affairs not in valid_scores:
            raise ValueError(f"Community Affairs score must be one of {valid_scores}")
        
        # Validate home/hobbies
        if home_hobbies not in valid_scores:
            raise ValueError(f"Home/Hobbies score must be one of {valid_scores}")
        
        # Validate personal care (no 0.5 option)
        if personal_care not in valid_personal_care:
            raise ValueError(f"Personal Care score must be one of {valid_personal_care}")
    
    def _calculate_global_cdr(self, scores: Dict[str, float]) -> float:
        """
        Calculates Global CDR using Washington University algorithm
        
        Memory (M) is the primary category, all others are secondary
        """
        
        m = scores['memory']
        secondary_scores = [
            scores['orientation'],
            scores['judgment_problem_solving'],
            scores['community_affairs'],
            scores['home_hobbies'],
            scores['personal_care']
        ]
        
        # Count how many secondary categories equal memory score
        count_equal_m = sum(1 for s in secondary_scores if s == m)
        
        # Rule 1: CDR = M if at least 3 secondary categories equal M
        if count_equal_m >= 3:
            return m
        
        # When M = 0
        if m == 0:
            # Count impairments (score >= 0.5) in secondary categories
            impairments = sum(1 for s in secondary_scores if s >= 0.5)
            if impairments >= 2:
                return 0.5
            else:
                return 0
        
        # When M = 0.5
        if m == 0.5:
            # CDR = 1 if at least 3 secondary categories are 1 or greater
            if sum(1 for s in secondary_scores if s >= 1) >= 3:
                return 1
            else:
                return 0.5
        
        # When M >= 1, CDR cannot be 0
        if m >= 1:
            # Check if majority of secondary categories are 0
            if sum(1 for s in secondary_scores if s == 0) >= 3:
                return 0.5
            
            # Count scores on each side of M
            higher = sum(1 for s in secondary_scores if s > m)
            lower = sum(1 for s in secondary_scores if s < m)
            equal = sum(1 for s in secondary_scores if s == m)
            
            # If only 1-2 secondary categories equal M
            if equal <= 2:
                # CDR = M if no more than 2 categories on either side
                if higher <= 2 and lower <= 2:
                    return m
            
            # With ties in secondary categories, choose tied score closest to M
            score_counts = {}
            for s in secondary_scores:
                score_counts[s] = score_counts.get(s, 0) + 1
            
            # Find tied scores
            tied_scores = [score for score, count in score_counts.items() if count >= 2]
            
            if tied_scores:
                # Choose tied score closest to M
                distances = [(abs(score - m), score) for score in tied_scores]
                distances.sort()
                return distances[0][1]
            
            # Default to M if no clear rule applies
            return m
    
    def _get_interpretation(self, global_cdr: float, cdr_sob: float) -> Dict[str, str]:
        """
        Determines the interpretation based on global CDR score
        
        Args:
            global_cdr: Global CDR score
            cdr_sob: Sum of boxes score
            
        Returns:
            Dict with interpretation details
        """
        
        sob_ranges = {
            0: "CDR-SOB: 0",
            0.5: "CDR-SOB: 0.5-4.0",
            1: "CDR-SOB: 4.5-9.0",
            2: "CDR-SOB: 9.5-15.5",
            3: "CDR-SOB: 16.0-18.0"
        }
        
        sob_info = f" (Sum of Boxes = {cdr_sob}, typical range for CDR {global_cdr}: {sob_ranges.get(global_cdr, 'N/A')})"
        
        if global_cdr == 0:
            return {
                "stage": "0",
                "description": "Normal",
                "interpretation": f"No cognitive impairment. The individual has no consistent or persistent changes in cognitive function{sob_info}."
            }
        elif global_cdr == 0.5:
            return {
                "stage": "0.5",
                "description": "Very Mild Dementia",
                "interpretation": f"Questionable or very mild dementia. Mild consistent forgetfulness with partial recollection of events. Mild difficulty with time relationships{sob_info}."
            }
        elif global_cdr == 1:
            return {
                "stage": "1",
                "description": "Mild Dementia",
                "interpretation": f"Mild dementia. Moderate memory loss, more marked for recent events. Moderate difficulty with time relationships. Impaired in community affairs{sob_info}."
            }
        elif global_cdr == 2:
            return {
                "stage": "2",
                "description": "Moderate Dementia",
                "interpretation": f"Moderate dementia. Severe memory loss with only highly learned material retained. Severely impaired in handling problems. Cannot function independently outside home{sob_info}."
            }
        else:  # global_cdr == 3
            return {
                "stage": "3",
                "description": "Severe Dementia",
                "interpretation": f"Severe dementia. Severe memory loss with only fragments remaining. Unable to handle problems or make judgments. Requires much help with personal care{sob_info}."
            }


def calculate_clinical_dementia_rating(
    memory, orientation, judgment_problem_solving,
    community_affairs, home_hobbies, personal_care
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ClinicalDementiaRatingCalculator()
    return calculator.calculate(
        memory, orientation, judgment_problem_solving,
        community_affairs, home_hobbies, personal_care
    )