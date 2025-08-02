"""
Los Angeles (LA) Grading of Esophagitis Models

Request and response models for LA Grading of Esophagitis classification.

References (Vancouver style):
1. Lundell LR, Dent J, Bennett JR, Blum AL, Armstrong D, Galmiche JP, et al. 
   Endoscopic assessment of oesophagitis: clinical and functional correlates and 
   further validation of the Los Angeles classification. Gut. 1999 Aug;45(2):172-80. 
   doi: 10.1136/gut.45.2.172.
2. Katz PO, Gerson LB, Vela MF. Guidelines for the diagnosis and management of 
   gastroesophageal reflux disease. Am J Gastroenterol. 2013 Mar;108(3):308-28; 
   quiz 329. doi: 10.1038/ajg.2012.444.
3. Kahrilas PJ, Shaheen NJ, Vaezi MF, Hiltz SW, Black E, Modlin IM, et al. American 
   Gastroenterological Association Medical Position Statement on the management of 
   gastroesophageal reflux disease. Gastroenterology. 2008 Oct;135(4):1383-1391, 
   1391.e1-5. doi: 10.1053/j.gastro.2008.05.045.

The Los Angeles Classification is the gold standard for endoscopic assessment of 
erosive esophagitis severity. It provides standardized criteria for classifying 
mucosal breaks into four grades (A-D) based on size and circumferential extent, 
with excellent inter-observer agreement and clinical correlation with symptoms 
and treatment response. This classification is recommended by ACG guidelines and 
widely adopted internationally for GERD management and research.
"""

from pydantic import BaseModel, Field
from typing import Literal


class LosAngelesGradingEsophagitisRequest(BaseModel):
    """
    Request model for Los Angeles (LA) Grading of Esophagitis
    
    The LA Classification provides standardized endoscopic criteria for erosive 
    esophagitis severity assessment based on mucosal break characteristics:
    
    Mucosal Break Categories:
    - breaks_5mm_or_less_no_continuity: Grade A - Mucosal break(s) ≤5 mm in length, 
      confined to mucosal folds without continuity across fold tops
    - breaks_greater_than_5mm_no_continuity: Grade B - Mucosal break(s) >5 mm in length, 
      confined to mucosal folds without continuity across fold tops
    - breaks_continuous_between_folds_less_than_75_percent: Grade C - Mucosal break(s) 
      continuous between tops of ≥2 mucosal folds, involving <75% of esophageal circumference
    - breaks_75_percent_or_more_circumference: Grade D - Mucosal break(s) involving 
      ≥75% of esophageal circumference
    
    Clinical Application:
    - Grades A-B: Mild reflux esophagitis requiring 4 weeks of standard-dose PPI therapy
    - Grades C-D: Severe reflux esophagitis requiring 8 weeks of standard-dose PPI therapy
    - Higher grades correlate with increased symptom severity and treatment duration
    - Grade D patients may require maintenance therapy and surgical evaluation
    
    Endoscopic Assessment Guidelines:
    - Use white light endoscopy with adequate insufflation and mucosal cleansing
    - Assess the distal 5-8 cm of esophagus systematically
    - Document location, size, and extent of all mucosal breaks
    - Distinguish erosions from ulcerations (deeper mucosal defects)
    - Consider narrow band imaging for subtle mucosal changes
    
    References (Vancouver style):
    1. Lundell LR, Dent J, Bennett JR, Blum AL, Armstrong D, Galmiche JP, et al. 
    Endoscopic assessment of oesophagitis: clinical and functional correlates and 
    further validation of the Los Angeles classification. Gut. 1999 Aug;45(2):172-80. 
    doi: 10.1136/gut.45.2.172.
    2. Katz PO, Gerson LB, Vela MF. Guidelines for the diagnosis and management of 
    gastroesophageal reflux disease. Am J Gastroenterol. 2013 Mar;108(3):308-28; 
    quiz 329. doi: 10.1038/ajg.2012.444.
    3. Kahrilas PJ, Shaheen NJ, Vaezi MF, Hiltz SW, Black E, Modlin IM, et al. American 
    Gastroenterological Association Medical Position Statement on the management of 
    gastroesophageal reflux disease. Gastroenterology. 2008 Oct;135(4):1383-1391, 
    1391.e1-5. doi: 10.1053/j.gastro.2008.05.045.
    """
    
    mucosal_break_size: Literal[
        "breaks_5mm_or_less_no_continuity",
        "breaks_greater_than_5mm_no_continuity", 
        "breaks_continuous_between_folds_less_than_75_percent",
        "breaks_75_percent_or_more_circumference"
    ] = Field(
        ...,
        description="Endoscopic appearance of mucosal breaks in the distal esophagus. "
                   "Grade A: ≤5mm breaks without continuity across folds. "
                   "Grade B: >5mm breaks without continuity across folds. "
                   "Grade C: Continuous breaks between ≥2 folds, <75% circumference. "
                   "Grade D: Breaks involving ≥75% of circumference",
        example="breaks_greater_than_5mm_no_continuity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "mucosal_break_size": "breaks_greater_than_5mm_no_continuity"
            }
        }


class LosAngelesGradingEsophagitisResponse(BaseModel):
    """
    Response model for Los Angeles (LA) Grading of Esophagitis
    
    The LA Classification provides standardized grades (A-D) with specific treatment 
    recommendations and prognostic implications:
    
    Grade A: Mild reflux esophagitis
    - Mucosal breaks ≤5 mm without continuity across folds
    - 4 weeks standard-dose PPI therapy
    - Consider step-down approach after healing
    
    Grade B: Mild reflux esophagitis  
    - Mucosal breaks >5 mm without continuity across folds
    - 4 weeks standard-dose PPI therapy
    - Consider surgical evaluation if symptoms persist
    
    Grade C: Severe reflux esophagitis
    - Continuous breaks between ≥2 folds, <75% circumference
    - 8 weeks standard-dose PPI therapy
    - Repeat endoscopy to assess healing
    - Consider maintenance therapy
    
    Grade D: Severe reflux esophagitis
    - Breaks involving ≥75% of circumference
    - 8 weeks standard-dose PPI therapy
    - Screen for Barrett's esophagus after healing
    - Strong consideration for antireflux surgery
    
    Reference: Lundell LR, et al. Gut. 1999;45(2):172-80.
    """
    
    result: Literal["A", "B", "C", "D"] = Field(
        ...,
        description="Los Angeles classification grade based on endoscopic mucosal break characteristics",
        example="B"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with treatment recommendations and management guidelines",
        example="Los Angeles Grade B Esophagitis Classification:\n\nEndoscopic Findings:\n• Mucosal break(s) >5 mm, without continuity across mucosal folds\n• Severity: Mild reflux esophagitis\n\nTreatment Recommendations:\n• Primary therapy: Standard-dose PPI for 4 weeks\n• Additional testing: Clinical diagnosis usually sufficient\n• Follow-up: Evaluate response to therapy and consider step-down approach\n• Surgical consideration: Consider if symptoms persist despite optimal medical therapy"
    )
    
    stage: str = Field(
        ...,
        description="LA Classification grade designation",
        example="Grade B"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category",
        example="Mild reflux esophagitis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "B",
                "unit": "grade",
                "interpretation": "Los Angeles Grade B Esophagitis Classification:\n\nEndoscopic Findings:\n• Mucosal break(s) >5 mm, without continuity across mucosal folds\n• Severity: Mild reflux esophagitis\n\nTreatment Recommendations:\n• Primary therapy: Standard-dose PPI for 4 weeks\n• Additional testing: Clinical diagnosis usually sufficient\n• Follow-up: Evaluate response to therapy and consider step-down approach\n• Surgical consideration: Consider if symptoms persist despite optimal medical therapy\n\nClinical Management Guidelines:\n• Mild esophagitis - good prognosis with PPI therapy\n• Lifestyle modifications: weight loss, head of bed elevation, avoid trigger foods\n• Consider step-down therapy after symptom resolution\n• Maintenance therapy usually not required unless symptoms recur\n• Monitor for symptom improvement within 2-4 weeks",
                "stage": "Grade B",
                "stage_description": "Mild reflux esophagitis"
            }
        }