"""
Bristol Stool Form Scale Calculator

Classifies stool form and correlates with intestinal transit time to assess 
bowel health and identify constipation or diarrhea. Developed at Bristol Royal 
Infirmary in 1997 by Stephen Lewis and Ken Heaton.

References:
- Lewis SJ, Heaton KW. Stool form scale as a useful guide to intestinal transit time. 
  Scand J Gastroenterol. 1997;32(9):920-4.
- Heaton KW, et al. Defecation frequency and timing, and stool form in the general 
  population: a prospective study. Gut. 1992;33(6):818-24.
"""

from typing import Dict, Any


class BristolStoolFormScaleCalculator:
    """Calculator for Bristol Stool Form Scale classification"""
    
    def __init__(self):
        # Scale definitions with clinical interpretations
        self.scale_definitions = {
            1: {
                "stage": "Severe Constipation",
                "description": "Separate hard lumps (nuts)",
                "interpretation": "Severe constipation. Hard, separate pellets that are difficult to pass. Indicates prolonged colonic transit time with excessive water absorption. Requires dietary modifications (increased fiber and fluids) and possible laxative therapy.",
                "transit_time": "Very slow",
                "clinical_significance": "Pathological - requires intervention"
            },
            2: {
                "stage": "Mild Constipation", 
                "description": "Sausage-like but lumpy",
                "interpretation": "Mild constipation. Hard, lumpy stools that are somewhat larger but still difficult to pass. Indicates slow colonic transit with increased water absorption. Requires increased fiber intake, hydration, and physical activity.",
                "transit_time": "Slow",
                "clinical_significance": "Abnormal - lifestyle modifications recommended"
            },
            3: {
                "stage": "Normal (Lower Range)",
                "description": "Sausage-like with cracks", 
                "interpretation": "Normal bowel function (lower normal range). Sausage-shaped with surface cracks. Represents adequate hydration and fiber intake with normal colonic transit time. Generally considered healthy stool consistency.",
                "transit_time": "Normal",
                "clinical_significance": "Normal - acceptable"
            },
            4: {
                "stage": "Normal (Ideal)",
                "description": "Smooth, soft sausage or snake",
                "interpretation": "Ideal bowel function. Smooth, soft, sausage-shaped stool that is easy to pass. Represents optimal hydration, diet, and normal colonic transit time. This is the target consistency for healthy bowel movements.",
                "transit_time": "Normal",
                "clinical_significance": "Ideal - optimal bowel health"
            },
            5: {
                "stage": "Normal (Upper Range)",
                "description": "Soft blobs with clear edges",
                "interpretation": "Normal bowel function (upper normal range). Soft blobs with clear-cut edges that pass easily. May indicate slightly faster colonic transit or higher water content. Generally acceptable but monitor for progression to diarrhea.",
                "transit_time": "Normal to slightly fast",
                "clinical_significance": "Normal - monitor if frequent"
            },
            6: {
                "stage": "Mild Diarrhea",
                "description": "Fluffy pieces with ragged edges",
                "interpretation": "Mild diarrhea. Mushy stool with fluffy pieces and ragged edges. Indicates rapid colonic transit with reduced water absorption. May be caused by dietary factors, medications, or mild gastrointestinal conditions.",
                "transit_time": "Fast",
                "clinical_significance": "Abnormal - evaluate underlying causes"
            },
            7: {
                "stage": "Severe Diarrhea",
                "description": "Entirely liquid",
                "interpretation": "Severe diarrhea. Watery stool with no solid pieces. Indicates very rapid intestinal transit with minimal water absorption. May lead to dehydration and electrolyte imbalance. Requires medical evaluation if persistent.",
                "transit_time": "Very fast",
                "clinical_significance": "Pathological - medical evaluation needed"
            }
        }
    
    def calculate(self, stool_type: int) -> Dict[str, Any]:
        """
        Classifies stool using Bristol Stool Form Scale
        
        Args:
            stool_type (int): Bristol stool type (1-7)
            
        Returns:
            Dict with classification and clinical interpretation
        """
        
        # Validate input
        self._validate_inputs(stool_type)
        
        # Get classification
        classification_data = self.scale_definitions[stool_type]
        
        # Determine bowel health category
        bowel_health_category = self._get_bowel_health_category(stool_type)
        
        return {
            "result": stool_type,
            "unit": "type",
            "interpretation": classification_data["interpretation"],
            "stage": classification_data["stage"],
            "stage_description": classification_data["description"],
            "transit_time": classification_data["transit_time"],
            "clinical_significance": classification_data["clinical_significance"],
            "bowel_health_category": bowel_health_category,
            "recommendations": self._get_recommendations(stool_type)
        }
    
    def _validate_inputs(self, stool_type: int):
        """Validates input parameter"""
        
        if not isinstance(stool_type, int):
            raise ValueError("stool_type must be an integer")
        
        if stool_type < 1 or stool_type > 7:
            raise ValueError("stool_type must be between 1 and 7")
    
    def _get_bowel_health_category(self, stool_type: int) -> str:
        """Determines overall bowel health category"""
        
        if stool_type in [1, 2]:
            return "Constipation"
        elif stool_type in [3, 4, 5]:
            return "Normal"
        else:  # 6, 7
            return "Diarrhea"
    
    def _get_recommendations(self, stool_type: int) -> Dict[str, Any]:
        """Provides clinical recommendations based on stool type"""
        
        recommendations = {
            1: {
                "dietary": ["Increase fiber intake (25-35g daily)", "Increase fluid intake (8-10 glasses water daily)", "Add prunes, fruits, vegetables"],
                "lifestyle": ["Increase physical activity", "Establish regular toilet routine", "Allow adequate time for bowel movements"],
                "medical": ["Consider bulk-forming laxatives", "Evaluate for underlying conditions", "Consider medical consultation if persistent"]
            },
            2: {
                "dietary": ["Increase fiber gradually", "Increase water intake", "Include whole grains and fruits"],
                "lifestyle": ["Regular exercise", "Consistent meal times", "Stress management"],
                "medical": ["Monitor response to dietary changes", "Consider fiber supplements if needed"]
            },
            3: {
                "dietary": ["Maintain balanced diet", "Adequate fiber intake", "Regular hydration"],
                "lifestyle": ["Continue current habits", "Regular physical activity"],
                "medical": ["No intervention needed", "Routine monitoring"]
            },
            4: {
                "dietary": ["Maintain current diet", "Continue balanced nutrition"],
                "lifestyle": ["Maintain current routine", "Continue healthy habits"],
                "medical": ["Ideal - no changes needed", "Continue current management"]
            },
            5: {
                "dietary": ["Monitor diet for triggers", "Maintain hydration"],
                "lifestyle": ["Continue regular habits", "Monitor for changes"],
                "medical": ["Generally acceptable", "Monitor if becomes frequent"]
            },
            6: {
                "dietary": ["Identify dietary triggers", "Consider BRAT diet temporarily", "Avoid high-fat or spicy foods"],
                "lifestyle": ["Rest and hydration", "Stress management", "Monitor frequency"],
                "medical": ["Evaluate underlying causes", "Consider probiotics", "Medical evaluation if persistent"]
            },
            7: {
                "dietary": ["Clear fluids initially", "Oral rehydration solutions", "Gradual diet advancement"],
                "lifestyle": ["Rest and fluid replacement", "Monitor for dehydration signs"],
                "medical": ["Immediate medical evaluation", "Electrolyte monitoring", "Investigate underlying causes"]
            }
        }
        
        return recommendations.get(stool_type, {})


def calculate_bristol_stool_form_scale(stool_type: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_bristol_stool_form_scale pattern
    """
    calculator = BristolStoolFormScaleCalculator()
    return calculator.calculate(stool_type)