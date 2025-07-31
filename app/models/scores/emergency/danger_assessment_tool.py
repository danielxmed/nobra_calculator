"""
Danger Assessment Tool for Domestic Abuse Models

Request and response models for Danger Assessment Tool calculation.

References (Vancouver style):
1. Campbell JC, Webster D, Koziol-McLain J, et al. Risk factors for femicide in abusive 
   relationships: results from a multisite case control study. Am J Public Health. 
   2003;93(7):1089-1097. doi: 10.2105/ajph.93.7.1089.
2. Campbell JC, Webster DW, Glass N. The danger assessment: validation of a lethality risk 
   assessment instrument for intimate partner femicide. J Interpers Violence. 2009;24(4):653-674. 
   doi: 10.1177/0886260508317180.
3. Messing JT, Campbell J, Webster DW, et al. The Oklahoma Lethality Assessment Study: 
   a quasi-experimental evaluation of the lethality assessment program. Soc Serv Rev. 
   2015;89(3):499-530. doi: 10.1086/682621.
4. Campbell JC, Alhusen JL, Draughon JE, Kub J, Walton-Moss B. Vulnerability and protective 
   factors for intimate partner violence. In: Mitchell C, Anglin D, eds. Intimate Partner 
   Violence: A Health-Based Perspective. Oxford University Press; 2009:143-162.

The Danger Assessment Tool is a validated lethality risk assessment instrument designed 
to predict the risk of intimate partner femicide. Developed by Dr. Jacquelyn Campbell 
at Johns Hopkins University, this evidence-based tool helps identify women at highest 
risk of being killed by their intimate partners.

The assessment is based on a comprehensive 11-city case-control study of intimate partner 
femicide that analyzed 310 femicide cases compared with 324 abused women controls. The 
resulting instrument uses weighted scoring based on adjusted odds ratios to provide 
accurate risk stratification for clinical and safety planning purposes.

This tool is widely used by healthcare providers, law enforcement, domestic violence 
advocates, and court systems to inform safety planning, resource allocation, and 
intervention strategies. Proper training is recommended for administration and 
interpretation of results.
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Dict


class DangerAssessmentToolRequest(BaseModel):
    """
    Request model for Danger Assessment Tool for Domestic Abuse
    
    The Danger Assessment Tool evaluates 20 validated risk factors to predict the 
    likelihood of intimate partner femicide. Each factor is assessed as a yes/no 
    question, with some factors allowing "not applicable" responses.
    
    **Risk Factor Categories:**
    
    **Escalation and Weapons (Highest Risk):**
    - physical_violence_increased: Escalation in frequency or severity of violence
    - owns_gun: Gun ownership by perpetrator (highest single risk factor)
    - threatened_weapon: Threats or attempts to kill with a weapon
    - tried_to_strangle: History of strangulation (strong predictor of lethality)
    
    **Threats and Intent:**
    - threatened_kill_you: Direct threats to kill the victim
    - avoided_killing: Victim's perception that perpetrator might try to kill them
    - threatened_kill_children: Threats against children
    - threatened_suicide: Perpetrator threats or attempts of suicide
    
    **Control and Jealousy:**
    - jealous_controlling: Violent and constant jealousy
    - controls_daily_activities: Control over victim's daily activities
    - follows_spies: Stalking behaviors, surveillance, property destruction
    
    **Violence Patterns:**
    - beaten_pregnant: Violence during pregnancy
    - controls_activities: Violence when perpetrator is intoxicated
    - violent_others: Violence toward children
    - violent_toward_others: Violence toward other family members or friends
    - forced_sex: Sexual violence and coercion
    
    **Risk Factors:**
    - child_not_his: Presence of child who is not perpetrator's biological child
    - employment_problems: Perpetrator job loss in past year
    - drugs_alcohol_problems: Illegal drug use by perpetrator
    - stepchild_present: Alcohol abuse or problem drinking by perpetrator
    
    **Clinical Considerations:**
    - Assessment should be conducted in private, safe environment
    - Victim safety is paramount during and after assessment
    - Results should be used to inform safety planning, not to predict with certainty
    - Regular reassessment is recommended as risk factors can change
    - Professional training is recommended for proper administration
    
    **Response Options:**
    - "yes": Risk factor is present
    - "no": Risk factor is not present  
    - "not_applicable": Used for pregnancy-related or child-related questions when not relevant
    
    **Scoring and Interpretation:**
    The tool uses weighted scoring based on adjusted odds ratios from validation studies. 
    Scores are categorized into three risk levels:
    - Variable Danger (0-7): Low to moderate risk
    - Increased Danger (8-13): Moderate to high risk  
    - Extreme Danger (14-20): High to extreme risk
    
    References (Vancouver style):
    1. Campbell JC, Webster D, Koziol-McLain J, et al. Risk factors for femicide in abusive 
    relationships: results from a multisite case control study. Am J Public Health. 
    2003;93(7):1089-1097. doi: 10.2105/ajph.93.7.1089.
    2. Campbell JC, Webster DW, Glass N. The danger assessment: validation of a lethality risk 
    assessment instrument for intimate partner femicide. J Interpers Violence. 2009;24(4):653-674. 
    doi: 10.1177/0886260508317180.
    """
    
    physical_violence_increased: Literal["yes", "no"] = Field(
        ...,
        description="Has the physical violence increased in frequency or severity over the past year? Escalation is a key predictor of lethality",
        example="no"
    )
    
    owns_gun: Literal["yes", "no"] = Field(
        ...,
        description="Does he own a gun? Gun ownership by perpetrator is the highest single risk factor for intimate partner femicide",
        example="no"
    )
    
    threatened_weapon: Literal["yes", "no"] = Field(
        ...,
        description="Has he ever threatened or tried to kill you with a weapon? Weapon threats indicate high lethality potential",
        example="no"
    )
    
    threatened_kill_you: Literal["yes", "no"] = Field(
        ...,
        description="Has he threatened to kill you? Direct death threats are strong predictors of femicide risk",
        example="no"
    )
    
    avoided_killing: Literal["yes", "no"] = Field(
        ...,
        description="Do you think he might try to kill you? Victim's perception of perpetrator's lethal intent is a significant risk factor",
        example="no"
    )
    
    beaten_pregnant: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Has he beaten you while you were pregnant? Violence during pregnancy indicates high risk and potential for escalation",
        example="not_applicable"
    )
    
    jealous_controlling: Literal["yes", "no"] = Field(
        ...,
        description="Is he violently and constantly jealous of you? Pathological jealousy is associated with increased lethality risk",
        example="no"
    )
    
    controls_activities: Literal["yes", "no"] = Field(
        ...,
        description="Have you ever been beaten by him when he was drunk or high on drugs? Substance-related violence often indicates lack of impulse control",
        example="no"
    )
    
    controls_daily_activities: Literal["yes", "no"] = Field(
        ...,
        description="Does he control most or all of your daily activities? Extreme control is associated with higher risk of severe violence",
        example="no"
    )
    
    violent_others: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Has he ever been violent toward your children? Violence toward children indicates general propensity for violence and escalation",
        example="not_applicable"
    )
    
    violent_toward_others: Literal["yes", "no"] = Field(
        ...,
        description="Has he ever been violent toward other family members or friends? History of violence toward others indicates general violence pattern",
        example="no"
    )
    
    threatened_suicide: Literal["yes", "no"] = Field(
        ...,
        description="Has he ever threatened or attempted suicide? Suicidal ideation in perpetrators increases risk of murder-suicide",
        example="no"
    )
    
    threatened_kill_children: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Has he threatened to kill your children? Threats against children indicate extreme danger and potential for family annihilation",
        example="not_applicable"
    )
    
    child_not_his: Literal["yes", "no"] = Field(
        ...,
        description="Do you have a child that is not his? Presence of stepchildren is associated with increased risk in intimate partner relationships",
        example="no"
    )
    
    employment_problems: Literal["yes", "no"] = Field(
        ...,
        description="Has he lost his job in the past year? Recent job loss can increase stress and risk of violence escalation",
        example="no"
    )
    
    follows_spies: Literal["yes", "no"] = Field(
        ...,
        description="Does he follow or spy on you, leave threatening notes, destroy your property, or call you when you don't want him to? Stalking behaviors indicate obsession and high risk",
        example="no"
    )
    
    forced_sex: Literal["yes", "no"] = Field(
        ...,
        description="Has he forced you to have sex when you did not wish to do so? Sexual violence is associated with increased risk of femicide",
        example="no"
    )
    
    tried_to_strangle: Literal["yes", "no"] = Field(
        ...,
        description="Has he ever tried to choke you? Strangulation is one of the strongest predictors of intimate partner femicide",
        example="no"
    )
    
    drugs_alcohol_problems: Literal["yes", "no"] = Field(
        ...,
        description="Does he use illegal drugs? Illegal drug use is associated with increased violence and impaired judgment",
        example="no"
    )
    
    stepchild_present: Literal["yes", "no"] = Field(
        ...,
        description="Is he an alcoholic or problem drinker? Alcohol abuse increases risk of violence and reduces inhibitions",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "physical_violence_increased": "no",
                "owns_gun": "no",
                "threatened_weapon": "no",
                "threatened_kill_you": "no",
                "avoided_killing": "no",
                "beaten_pregnant": "not_applicable",
                "jealous_controlling": "no",
                "controls_activities": "no",
                "controls_daily_activities": "no",
                "violent_others": "not_applicable",
                "violent_toward_others": "no",
                "threatened_suicide": "no",
                "threatened_kill_children": "not_applicable",
                "child_not_his": "no",
                "employment_problems": "no",
                "follows_spies": "no",
                "forced_sex": "no",
                "tried_to_strangle": "no",
                "drugs_alcohol_problems": "no",
                "stepchild_present": "no"
            }
        }


class DangerAssessmentToolResponse(BaseModel):
    """
    Response model for Danger Assessment Tool for Domestic Abuse
    
    Provides comprehensive risk assessment with validated danger scoring, risk level 
    classification, safety planning recommendations, and professional guidance for 
    intimate partner violence lethality assessment.
    
    **Risk Level Classifications:**
    
    **Variable Danger (Score 0-7):**
    - Risk Level: Low to moderate
    - Interpretation: Danger is probably not extreme at this time
    - Action: Basic safety planning, resource connection, periodic reassessment
    - Monitoring: Regular check-ins and risk factor monitoring
    
    **Increased Danger (Score 8-13):**
    - Risk Level: Moderate to high  
    - Interpretation: Elevated risk of intimate partner homicide
    - Action: Enhanced safety planning, professional intervention, coordinated response
    - Monitoring: Frequent reassessment and intensive support services
    
    **Extreme Danger (Score 14-20):**
    - Risk Level: High to extreme
    - Interpretation: Severe and immediate risk of intimate partner homicide
    - Action: Emergency safety planning, immediate intervention, high-risk protocols
    - Monitoring: Continuous safety monitoring and crisis intervention readiness
    
    **Critical Risk Factors:**
    - Gun ownership: Highest single risk factor (5x increased risk)
    - Strangulation history: Strong predictor of future femicide
    - Death threats: Direct indication of lethal intent
    - Weapon threats: Evidence of escalation to lethal violence
    - Threats against children: Indication of potential family annihilation
    
    **Safety Planning Components:**
    - Immediate safety measures and emergency planning
    - Professional resource connections and referrals
    - Legal protection options and advocacy
    - Support network activation and safety communication
    - Risk factor monitoring and reassessment scheduling
    
    Reference: Campbell JC, et al. J Interpers Violence. 2009;24(4):653-674.
    """
    
    result: float = Field(
        ...,
        description="Weighted danger assessment score based on validated risk factors",
        example=3.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the danger assessment score",
        example="danger score"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk level assessment and safety planning guidance",
        example="Danger Assessment score of 3.2 indicates variable danger level. While the immediate risk may not be extreme, safety planning is still important. Monitor situation for changes and connect with domestic violence resources for support."
    )
    
    stage: str = Field(
        ...,
        description="Risk level classification stage (Variable Danger, Increased Danger, Extreme Danger)",
        example="Variable Danger"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level characteristics",
        example="Low to moderate risk"
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level category (variable, increased, extreme)",
        example="variable"
    )
    
    weighted_score: float = Field(
        ...,
        description="Weighted score based on adjusted odds ratios from validation studies",
        example=3.2
    )
    
    simple_score: int = Field(
        ...,
        description="Simple count of 'yes' responses to risk factor questions",
        example=3
    )
    
    risk_analysis: Dict = Field(
        ...,
        description="Detailed risk analysis including key risk factors and severity indicators",
        example={
            "weighted_score": 3.2,
            "simple_count": 3,
            "risk_level": "variable",
            "key_risk_factors": [],
            "severity_indicators": []
        }
    )
    
    safety_recommendations: Dict = Field(
        ...,
        description="Comprehensive safety recommendations including general and specific measures, emergency contacts, and planning steps",
        example={
            "general_recommendations": [
                "Develop basic safety plan with trusted friend or family member",
                "Keep emergency contact numbers readily available",
                "Identify safe places to go if needed",
                "Consider documenting incidents with photos and dates",
                "Monitor situation for changes in risk factors",
                "Connect with local domestic violence resources"
            ],
            "specific_recommendations": [],
            "emergency_contacts": {
                "national_hotline": "1-800-799-7233 (National Domestic Violence Hotline)",
                "emergency_services": "911 for immediate danger",
                "text_line": "Text START to 88788 (Crisis Text Line)",
                "online_chat": "Available at thehotline.org",
                "local_resources": "Contact local domestic violence shelter or advocacy organization"
            },
            "safety_planning_steps": [
                "Identify safe friends, family, or shelters where you can go",
                "Keep emergency bag ready with essentials",
                "Plan escape routes from home and work",
                "Establish code words with trusted contacts",
                "Keep important documents in safe location",
                "Have emergency money and transportation arranged"
            ]
        }
    )
    
    immediate_actions: List[str] = Field(
        ...,
        description="Immediate actions recommended based on risk level assessment",
        example=[
            "Create basic safety plan",
            "Connect with domestic violence resources",
            "Document any future incidents",
            "Monitor for changes in behavior or risk factors"
        ]
    )
    
    high_risk_factors: List[str] = Field(
        ...,
        description="List of critical high-risk factors identified in the assessment",
        example=[]
    )
    
    protective_factors: List[str] = Field(
        ...,
        description="List of protective factors that may reduce risk",
        example=["No gun in home", "No substance abuse issues", "No history of violence toward others"]
    )
    
    counseling_points: List[str] = Field(
        ...,
        description="Key counseling points for victim support and empowerment",
        example=[
            "You are not alone - help and support are available",
            "The abuse is not your fault",
            "Your safety and the safety of your children is the priority",
            "You have the right to live free from violence and fear",
            "There are people trained to help you navigate this situation safely"
        ]
    )
    
    professional_referrals: List[str] = Field(
        ...,
        description="Recommended professional referrals based on risk level and needs",
        example=[
            "Domestic violence advocate or counselor",
            "Legal advocacy services",
            "Mental health counseling services",
            "Healthcare provider for medical evaluation"
        ]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3.2,
                "unit": "danger score",
                "interpretation": "Danger Assessment score of 3.2 indicates variable danger level. While the immediate risk may not be extreme, safety planning is still important. Monitor situation for changes and connect with domestic violence resources for support.",
                "stage": "Variable Danger",
                "stage_description": "Low to moderate risk",
                "risk_level": "variable",
                "weighted_score": 3.2,
                "simple_score": 3,
                "risk_analysis": {
                    "weighted_score": 3.2,
                    "simple_count": 3,
                    "risk_level": "variable",
                    "key_risk_factors": [],
                    "severity_indicators": []
                },
                "safety_recommendations": {
                    "general_recommendations": [
                        "Develop basic safety plan with trusted friend or family member",
                        "Keep emergency contact numbers readily available",
                        "Identify safe places to go if needed",
                        "Consider documenting incidents with photos and dates",
                        "Monitor situation for changes in risk factors",
                        "Connect with local domestic violence resources"
                    ],
                    "specific_recommendations": [],
                    "emergency_contacts": {
                        "national_hotline": "1-800-799-7233 (National Domestic Violence Hotline)",
                        "emergency_services": "911 for immediate danger",
                        "text_line": "Text START to 88788 (Crisis Text Line)",
                        "online_chat": "Available at thehotline.org",
                        "local_resources": "Contact local domestic violence shelter or advocacy organization"
                    },
                    "safety_planning_steps": [
                        "Identify safe friends, family, or shelters where you can go",
                        "Keep emergency bag ready with essentials",
                        "Plan escape routes from home and work",
                        "Establish code words with trusted contacts",
                        "Keep important documents in safe location",
                        "Have emergency money and transportation arranged"
                    ]
                },
                "immediate_actions": [
                    "Create basic safety plan",
                    "Connect with domestic violence resources",
                    "Document any future incidents",
                    "Monitor for changes in behavior or risk factors"
                ],
                "high_risk_factors": [],
                "protective_factors": ["No gun in home", "No substance abuse issues", "No history of violence toward others"],
                "counseling_points": [
                    "You are not alone - help and support are available",
                    "The abuse is not your fault",
                    "Your safety and the safety of your children is the priority",
                    "You have the right to live free from violence and fear",
                    "There are people trained to help you navigate this situation safely"
                ],
                "professional_referrals": [
                    "Domestic violence advocate or counselor",
                    "Legal advocacy services",
                    "Mental health counseling services",
                    "Healthcare provider for medical evaluation"
                ]
            }
        }