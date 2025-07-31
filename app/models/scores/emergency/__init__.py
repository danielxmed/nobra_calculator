"""
Emergency score models
"""

from .four_c_mortality import FourCMortalityRequest, FourCMortalityResponse
from .ais_inhalation_injury import AisInhalationInjuryRequest, AisInhalationInjuryResponse
from .emergency_medicine_coding_guide_2023 import EmergencyMedicineCodingGuide2023Request, EmergencyMedicineCodingGuide2023Response
from .abc_score import AbcScoreRequest, AbcScoreResponse
from .acep_ed_covid19_management_tool import (
    AcepEdCovid19ManagementToolRequest,
    AcepEdCovid19ManagementToolResponse,
)
from .acetaminophen_overdose_nac import (
    AcetaminophenOverdoseNacRequest,
    AcetaminophenOverdoseNacResponse,
)
from .adapt_protocol import AdaptProtocolRequest, AdaptProtocolResponse
from .age_adjusted_d_dimer import AgeAdjustedDDimerRequest, AgeAdjustedDDimerResponse
from .aims65 import Aims65Request, Aims65Response
from .alt_70_cellulitis import Alt70CellulitisRequest, Alt70CellulitisResponse
from .altitude_adjusted_perc import AltitudeAdjustedPercRequest, AltitudeAdjustedPercResponse
from .alvarado_score import AlvaradoScoreRequest, AlvaradoScoreResponse
from .antivenom_dosing_algorithm import AntivenomDosingAlgorithmRequest, AntivenomDosingAlgorithmResponse
from .apache_ii_score import ApacheIiScoreRequest, ApacheIiScoreResponse
from .air_score import AirScoreRequest, AirScoreResponse
from .abg_analyzer import AbgAnalyzerRequest, AbgAnalyzerResponse
from .basic_statistics_calc import BasicStatisticsCalcRequest, BasicStatisticsCalcResponse
from .bastion_classification import BastionClassificationRequest, BastionClassificationResponse
from .behavioral_pain_scale import BehavioralPainScaleRequest, BehavioralPainScaleResponse
from .benzodiazepine_conversion import BenzodiazepineConversionRequest, BenzodiazepineConversionResponse
from .bicarbonate_deficit import BicarbonateDeficitRequest, BicarbonateDeficitResponse
from .bisap_score import BisapScoreRequest, BisapScoreResponse
from .blast_lung_injury_severity import BlastLungInjurySeverityRequest, BlastLungInjurySeverityResponse
from .burch_wartofsky_point_scale import BurchWartofskypointScaleRequest, BurchWartofskypointScaleResponse
from .canadian_c_spine_rule import CanadianCSpineRuleRequest, CanadianCSpineRuleResponse
from .canadian_ct_head_rule import CanadianCtHeadRuleRequest, CanadianCtHeadRuleResponse
from .canadian_syncope_risk_score import CanadianSyncopeRiskScoreRequest, CanadianSyncopeRiskScoreResponse
from .caprini_score_2005 import CapriniScore2005Request, CapriniScore2005Response
from .cart_score import CartScoreRequest, CartScoreResponse
from .centor_score import CentorScoreRequest, CentorScoreResponse
from .cedocs_score import CedocsScoreRequest, CedocsScoreResponse
from .chip_prediction_rule import ChipPredictionRuleRequest, ChipPredictionRuleResponse
from .chosen_covid_discharge import ChosenCovidDischargeRequest, ChosenCovidDischargeResponse
from .covid_inpatient_risk_calculator import CovidInpatientRiskCalculatorRequest, CovidInpatientRiskCalculatorResponse
from .cincinnati_prehospital_stroke_severity_scale import (
    CincinnatiPrehospitalStrokeSeverityScaleRequest,
    CincinnatiPrehospitalStrokeSeverityScaleResponse,
)
from .cam_icu import CamIcuRequest, CamIcuResponse
from .covid_gram_critical_illness import CovidGramCriticalIllnessRequest, CovidGramCriticalIllnessResponse
from .cpot_pain_observation import CpotPainObservationRequest, CpotPainObservationResponse
from .danger_assessment_tool import DangerAssessmentToolRequest, DangerAssessmentToolResponse
from .ed_safe_patient_safety_screener import EdSafePatientSafetyScreenerRequest, EdSafePatientSafetyScreenerResponse
from .naloxone_drip_dosing import NaloxoneDripDosingRequest, NaloxoneDripDosingResponse
from .news import NewsRequest, NewsResponse
from .news_2 import News2Request, News2Response
from .nedocs import NedocsRequest, NedocsResponse
from .digifab_dosing import DigifabDosingRequest, DigifabDosingResponse
from .emergency_department_assessment_chest_pain_edacs import EmergencyDepartmentAssessmentChestPainEdacsRequest, EmergencyDepartmentAssessmentChestPainEdacsResponse
from .emergency_heart_failure_mortality_risk_grade_ehmrg import EmergencyHeartFailureMortalityRiskGradeEhmrgRequest, EmergencyHeartFailureMortalityRiskGradeEhmrgResponse
from .nexus_criteria import NexusCriteriaRequest, NexusCriteriaResponse
from .newsom_score import NewsomScoreRequest, NewsomScoreResponse
from .nexus_chest_ct import NexusChestCtRequest, NexusChestCtResponse
from .nexus_chest_blunt_trauma import NexusChestBluntTraumaRequest, NexusChestBluntTraumaResponse
from .ottawa_ankle_rule import OttawaAnkleRuleRequest, OttawaAnkleRuleResponse
from .ottawa_copd_risk_scale import OttawaCopdRiskScaleRequest, OttawaCopdRiskScaleResponse
from .ottawa_heart_failure_risk_scale import OttawaHeartFailureRiskScaleRequest, OttawaHeartFailureRiskScaleResponse
from .ottawa_knee_rule import OttawaKneeRuleRequest, OttawaKneeRuleResponse
from .embed import EmbedRequest, EmbedResponse
from .ett_depth_tidal_volume import EttDepthTidalVolumeRequest, EttDepthTidalVolumeResponse
from .fast import FastRequest, FastResponse
from .fomepizole_dosing import FomepizoleDosingRequest, FomepizoleDosingResponse
from .go_far_score import GoFarScoreRequest, GoFarScoreResponse
from .gupta_mica import GuptaMicaRequest, GuptaMicaResponse
from .gupta_postoperative_pneumonia_risk import GuptaPostoperativePneumoniaRiskRequest, GuptaPostoperativePneumoniaRiskResponse
from .gupta_postoperative_respiratory_failure_risk import GuptaPostoperativeRespiratoryFailureRiskRequest, GuptaPostoperativeRespiratoryFailureRiskResponse
from .hacor_score import HacorScoreRequest, HacorScoreResponse
from .hacks_impairment_index import HacksImpairmentIndexRequest, HacksImpairmentIndexResponse

__all__ = [
    "FourCMortalityRequest",
    "FourCMortalityResponse",
    "AisInhalationInjuryRequest",
    "AisInhalationInjuryResponse",
    "EmergencyMedicineCodingGuide2023Request",
    "EmergencyMedicineCodingGuide2023Response",
    "AbcScoreRequest",
    "AbcScoreResponse",
    "AcepEdCovid19ManagementToolRequest",
    "AcepEdCovid19ManagementToolResponse",
    "AcetaminophenOverdoseNacRequest",
    "AcetaminophenOverdoseNacResponse",
    "AdaptProtocolRequest",
    "AdaptProtocolResponse",
    "AgeAdjustedDDimerRequest",
    "AgeAdjustedDDimerResponse",
    "Aims65Request",
    "Aims65Response",
    "Alt70CellulitisRequest",
    "Alt70CellulitisResponse",
    "AltitudeAdjustedPercRequest",
    "AltitudeAdjustedPercResponse",
    "AlvaradoScoreRequest",
    "AlvaradoScoreResponse",
    "AntivenomDosingAlgorithmRequest",
    "AntivenomDosingAlgorithmResponse",
    "ApacheIiScoreRequest",
    "ApacheIiScoreResponse",
    "AirScoreRequest",
    "AirScoreResponse",
    "AbgAnalyzerRequest",
    "AbgAnalyzerResponse",
    "BasicStatisticsCalcRequest",
    "BasicStatisticsCalcResponse",
    "BastionClassificationRequest",
    "BastionClassificationResponse",
    "BehavioralPainScaleRequest",
    "BehavioralPainScaleResponse",
    "BenzodiazepineConversionRequest",
    "BenzodiazepineConversionResponse",
    "BicarbonateDeficitRequest",
    "BicarbonateDeficitResponse",
    "BisapScoreRequest",
    "BisapScoreResponse",
    "BlastLungInjurySeverityRequest",
    "BlastLungInjurySeverityResponse",
    "BurchWartofskypointScaleRequest",
    "BurchWartofskypointScaleResponse",
    "CanadianCSpineRuleRequest",
    "CanadianCSpineRuleResponse",
    "CanadianCtHeadRuleRequest",
    "CanadianCtHeadRuleResponse",
    "CanadianSyncopeRiskScoreRequest",
    "CanadianSyncopeRiskScoreResponse",
    "CapriniScore2005Request",
    "CapriniScore2005Response",
    "CartScoreRequest",
    "CartScoreResponse",
    "CentorScoreRequest",
    "CentorScoreResponse",
    "CedocsScoreRequest",
    "CedocsScoreResponse",
    "ChipPredictionRuleRequest",
    "ChipPredictionRuleResponse",
    "ChosenCovidDischargeRequest",
    "ChosenCovidDischargeResponse",
    "CovidInpatientRiskCalculatorRequest",
    "CovidInpatientRiskCalculatorResponse",
    "CincinnatiPrehospitalStrokeSeverityScaleRequest",
    "CincinnatiPrehospitalStrokeSeverityScaleResponse",
    "CamIcuRequest",
    "CamIcuResponse",
    "CovidGramCriticalIllnessRequest",
    "CovidGramCriticalIllnessResponse",
    "CpotPainObservationRequest",
    "CpotPainObservationResponse",
    "DangerAssessmentToolRequest",
    "DangerAssessmentToolResponse",
    "EdSafePatientSafetyScreenerRequest",
    "EdSafePatientSafetyScreenerResponse",
    "NaloxoneDripDosingRequest",
    "NaloxoneDripDosingResponse",
    "NewsRequest",
    "NewsResponse",
    "News2Request",
    "News2Response",
    "NedocsRequest",
    "NedocsResponse",
    "DigifabDosingRequest",
    "DigifabDosingResponse",
    "EmergencyDepartmentAssessmentChestPainEdacsRequest",
    "EmergencyDepartmentAssessmentChestPainEdacsResponse",
    "EmergencyHeartFailureMortalityRiskGradeEhmrgRequest",
    "EmergencyHeartFailureMortalityRiskGradeEhmrgResponse",
    "NexusCriteriaRequest",
    "NexusCriteriaResponse",
    "NewsomScoreRequest",
    "NewsomScoreResponse",
    "NexusChestCtRequest",
    "NexusChestCtResponse",
    "NexusChestBluntTraumaRequest",
    "NexusChestBluntTraumaResponse",
    "OttawaAnkleRuleRequest",
    "OttawaAnkleRuleResponse",
    "OttawaCopdRiskScaleRequest",
    "OttawaCopdRiskScaleResponse",
    "OttawaHeartFailureRiskScaleRequest",
    "OttawaHeartFailureRiskScaleResponse",
    "OttawaKneeRuleRequest",
    "OttawaKneeRuleResponse",
    "EmbedRequest",
    "EmbedResponse",
    "EttDepthTidalVolumeRequest",
    "EttDepthTidalVolumeResponse",
    "FastRequest",
    "FastResponse",
    "FomepizoleDosingRequest",
    "FomepizoleDosingResponse",
    "GoFarScoreRequest",
    "GoFarScoreResponse",
    "GuptaMicaRequest",
    "GuptaMicaResponse",
    "GuptaPostoperativePneumoniaRiskRequest",
    "GuptaPostoperativePneumoniaRiskResponse",
    "GuptaPostoperativeRespiratoryFailureRiskRequest",
    "GuptaPostoperativeRespiratoryFailureRiskResponse",
    "HacorScoreRequest",
    "HacorScoreResponse",
    "HacksImpairmentIndexRequest",
    "HacksImpairmentIndexResponse",
]
