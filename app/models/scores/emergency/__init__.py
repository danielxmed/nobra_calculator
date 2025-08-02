"""
Emergency score models
"""

from .four_c_mortality import FourCMortalityRequest, FourCMortalityResponse
from .ais_inhalation_injury import AisInhalationInjuryRequest, AisInhalationInjuryResponse
from .injury_severity_score import InjurySeverityScoreRequest, InjurySeverityScoreResponse
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
from .tpa_alteplase_dosing_stroke import (
    TpaAlteplaseDosingStrokeRequest,
    TpaAlteplaseDosingStrokeResponse
)
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
from .ottawa_sah_rule import OttawaSahRuleRequest, OttawaSahRuleResponse
from .psi_port_score import PsiPortScoreRequest, PsiPortScoreResponse
from .pesi import PesiRequest, PesiResponse
from .pe_sard_score import PeSardScoreRequest, PeSardScoreResponse
from .qsofa_score import QsofaScoreRequest, QsofaScoreResponse
from .qcsi import QcsiRequest, QcsiResponse
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
from .he_macs import HeMacsRequest, HeMacsResponse
from .hestia_criteria import HestiaCriteriaRequest, HestiaCriteriaResponse
from .hark import HarkRequest, HarkResponse
from .hits_score import HitsScoreRequest, HitsScoreResponse
from .hope_score import HopeScoreRequest, HopeScoreResponse
from .intraoperative_fluid_dosing import IntraoperativeFluidDosingRequest, IntraoperativeFluidDosingResponse
from .iv_drip_rate_calculator import IvDripRateCalculatorRequest, IvDripRateCalculatorResponse
from .kings_college_criteria_acetaminophen import KingsCollegeCriteriaAcetaminophenRequest, KingsCollegeCriteriaAcetaminophenResponse
from .kocher_criteria_septic_arthritis import KocherCriteriaSepticArthritisRequest, KocherCriteriaSepticArthritisResponse
from .lace_index_readmission import LaceIndexReadmissionRequest, LaceIndexReadmissionResponse
from .local_anesthetic_dosing_calculator import LocalAnestheticDosingCalculatorRequest, LocalAnestheticDosingCalculatorResponse
from .lrinec_score import LrinecScoreRequest, LrinecScoreResponse
from .lung_injury_prediction_score import LungInjuryPredictionScoreRequest, LungInjuryPredictionScoreResponse
from .macocha_score import MacochaScoreRequest, MacochaScoreResponse
from .mangled_extremity_severity_score import MangledExtremitySeverityScoreRequest, MangledExtremitySeverityScoreResponse
from .mrc_icu_score import MrcIcuScoreRequest, MrcIcuScoreResponse
from .modified_early_warning_score import ModifiedEarlyWarningScoreRequest, ModifiedEarlyWarningScoreResponse
from .modified_brain_injury_guideline import ModifiedBrainInjuryGuidelineRequest, ModifiedBrainInjuryGuidelineResponse
from .modified_mallampati_classification import ModifiedMallampatiClassificationRequest, ModifiedMallampatiClassificationResponse
from .modified_sofa import ModifiedSofaRequest, ModifiedSofaResponse
from .rose_rule import RoseRuleRequest, RoseRuleResponse
from .roth_score import RothScoreRequest, RothScoreResponse
from .rox_index import RoxIndexRequest, RoxIndexResponse
from .rule_of_7s_lyme_meningitis import RuleOf7sLymeMeningitisRequest, RuleOf7sLymeMeningitisResponse
from .rule_of_nines import RuleOfNinesRequest, RuleOfNinesResponse
from .triss import TrissRequest, TrissResponse
from .winters_formula_metabolic_acidosis import WintersFormulaMetabolicAcidosisRequest, WintersFormulaMetabolicAcidosisResponse
from .wisconsin_criteria_maxillofacial_trauma import WisconsinCriteriaMaxillofacialTraumaRequest, WisconsinCriteriaMaxillofacialTraumaResponse
from .woman_abuse_screening_tool import WomanAbuseScreeningToolRequest, WomanAbuseScreeningToolResponse
from .years_algorithm_pe import YearsAlgorithmPeRequest, YearsAlgorithmPeResponse
from .utah_covid19_risk_score import UtahCovid19RiskScoreRequest, UtahCovid19RiskScoreResponse
from .rems_score import RemsScoreRequest, RemsScoreResponse

__all__ = [
    "FourCMortalityRequest",
    "FourCMortalityResponse",
    "AisInhalationInjuryRequest",
    "AisInhalationInjuryResponse",
    "InjurySeverityScoreRequest",
    "InjurySeverityScoreResponse",
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
    "OttawaSahRuleRequest",
    "OttawaSahRuleResponse",
    "PsiPortScoreRequest",
    "PsiPortScoreResponse",
    "PesiRequest",
    "PesiResponse",
    "PeSardScoreRequest",
    "PeSardScoreResponse",
    "QsofaScoreRequest",
    "QsofaScoreResponse",
    "QcsiRequest",
    "QcsiResponse",
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
    "HeMacsRequest",
    "HeMacsResponse",
    "HestiaCriteriaRequest",
    "HestiaCriteriaResponse",
    "HarkRequest",
    "HarkResponse",
    "HitsScoreRequest",
    "HitsScoreResponse",
    "HopeScoreRequest",
    "HopeScoreResponse",
    "IntraoperativeFluidDosingRequest",
    "IntraoperativeFluidDosingResponse",
    "IvDripRateCalculatorRequest",
    "IvDripRateCalculatorResponse",
    "KingsCollegeCriteriaAcetaminophenRequest",
    "KingsCollegeCriteriaAcetaminophenResponse",
    "KocherCriteriaSepticArthritisRequest",
    "KocherCriteriaSepticArthritisResponse",
    "LaceIndexReadmissionRequest",
    "LaceIndexReadmissionResponse",
    "LocalAnestheticDosingCalculatorRequest",
    "LocalAnestheticDosingCalculatorResponse",
    "LrinecScoreRequest",
    "LrinecScoreResponse",
    "LungInjuryPredictionScoreRequest",
    "LungInjuryPredictionScoreResponse",
    "MacochaScoreRequest",
    "MacochaScoreResponse",
    "MangledExtremitySeverityScoreRequest",
    "MangledExtremitySeverityScoreResponse",
    "MrcIcuScoreRequest",
    "MrcIcuScoreResponse",
    "ModifiedEarlyWarningScoreRequest",
    "ModifiedEarlyWarningScoreResponse",
    "ModifiedBrainInjuryGuidelineRequest",
    "ModifiedBrainInjuryGuidelineResponse",
    "ModifiedMallampatiClassificationRequest",
    "ModifiedMallampatiClassificationResponse",
    "ModifiedSofaRequest",
    "ModifiedSofaResponse",
    "RoseRuleRequest",
    "RoseRuleResponse",
    "RothScoreRequest",
    "RothScoreResponse",
    "RoxIndexRequest",
    "RoxIndexResponse",
    "RuleOf7sLymeMeningitisRequest",
    "RuleOf7sLymeMeningitisResponse",
    "RuleOfNinesRequest",
    "RuleOfNinesResponse",
    "TpaAlteplaseDosingStrokeRequest",
    "TpaAlteplaseDosingStrokeResponse",
    "TrissRequest",
    "TrissResponse",
    "WintersFormulaMetabolicAcidosisRequest",
    "WintersFormulaMetabolicAcidosisResponse",
    "WisconsinCriteriaMaxillofacialTraumaRequest",
    "WisconsinCriteriaMaxillofacialTraumaResponse",
    "WomanAbuseScreeningToolRequest",
    "WomanAbuseScreeningToolResponse",
    "YearsAlgorithmPeRequest",
    "YearsAlgorithmPeResponse",
    "UtahCovid19RiskScoreRequest",
    "UtahCovid19RiskScoreResponse",
    "RemsScoreRequest",
    "RemsScoreResponse"
]
