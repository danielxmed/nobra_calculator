"""
2012 EULAR/ACR Classification Criteria for Polymyalgia Rheumatica Calculator

Classifica polimialgia reumática usando critérios clínicos e ultrassonográficos.
Referência: Dasgupta et al., Ann Rheum Dis 2012;71(4):484-92
"""

from typing import Dict, Any


class EularAcr2012PmrCalculator:
    """Calculadora para critérios de classificação EULAR/ACR 2012 para PMR"""
    
    def calculate(self, morning_stiffness: str, hip_pain_limited_rom: str,
                 rf_or_acpa: str, other_joint_pain: str,
                 ultrasound_shoulder_hip: str = "not_performed",
                 ultrasound_both_shoulders: str = "not_performed") -> Dict[str, Any]:
        """
        Calcula o escore EULAR/ACR 2012 para polimialgia reumática
        
        Args:
            morning_stiffness: "<=45min" ou ">45min" - duração da rigidez matinal
            hip_pain_limited_rom: "no" ou "yes" - dor no quadril ou ROM limitada
            rf_or_acpa: "present" ou "absent" - FR ou ACPA presente
            other_joint_pain: "present" ou "absent" - dor em outras articulações
            ultrasound_shoulder_hip: "no", "yes", "not_performed" - US ombro/quadril
            ultrasound_both_shoulders: "no", "yes", "not_performed" - US ambos ombros
            
        Returns:
            Dict com resultado, interpretação e classificação
        """
        
        # Validações
        self._validate_inputs(morning_stiffness, hip_pain_limited_rom, rf_or_acpa,
                            other_joint_pain, ultrasound_shoulder_hip,
                            ultrasound_both_shoulders)
        
        # Calcular pontuação
        score = 0
        
        # Rigidez matinal >45min: 2 pontos
        if morning_stiffness == ">45min":
            score += 2
        
        # Dor no quadril ou ROM limitada: 1 ponto
        if hip_pain_limited_rom == "yes":
            score += 1
        
        # Ausência de FR ou ACPA: 2 pontos
        if rf_or_acpa == "absent":
            score += 2
        
        # Ausência de dor em outras articulações: 1 ponto
        if other_joint_pain == "absent":
            score += 1
        
        # Determinar se ultrassom foi realizado
        us_performed = (ultrasound_shoulder_hip != "not_performed" or 
                       ultrasound_both_shoulders != "not_performed")
        
        # Adicionar pontos do ultrassom se realizado
        if us_performed:
            if ultrasound_shoulder_hip == "yes":
                score += 1
            if ultrasound_both_shoulders == "yes":
                score += 1
        
        # Obter interpretação baseada no escore e se US foi realizado
        interpretation = self._get_interpretation(score, us_performed)
        
        return {
            "result": score,
            "unit": "pontos",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, morning_stiffness: str, hip_pain_limited_rom: str,
                        rf_or_acpa: str, other_joint_pain: str,
                        ultrasound_shoulder_hip: str, ultrasound_both_shoulders: str):
        """Valida os parâmetros de entrada"""
        
        if morning_stiffness not in ["<=45min", ">45min"]:
            raise ValueError("Rigidez matinal deve ser '<=45min' ou '>45min'")
        
        if hip_pain_limited_rom not in ["no", "yes"]:
            raise ValueError("Dor no quadril/ROM limitada deve ser 'no' ou 'yes'")
        
        if rf_or_acpa not in ["present", "absent"]:
            raise ValueError("FR ou ACPA deve ser 'present' ou 'absent'")
        
        if other_joint_pain not in ["present", "absent"]:
            raise ValueError("Dor em outras articulações deve ser 'present' ou 'absent'")
        
        valid_us_options = ["no", "yes", "not_performed"]
        if ultrasound_shoulder_hip not in valid_us_options:
            raise ValueError(f"Ultrassom ombro/quadril deve ser: {', '.join(valid_us_options)}")
        
        if ultrasound_both_shoulders not in valid_us_options:
            raise ValueError(f"Ultrassom ambos ombros deve ser: {', '.join(valid_us_options)}")
        
        # Validar consistência do ultrassom
        if ((ultrasound_shoulder_hip == "not_performed" and 
             ultrasound_both_shoulders != "not_performed") or
            (ultrasound_shoulder_hip != "not_performed" and 
             ultrasound_both_shoulders == "not_performed")):
            raise ValueError("Se ultrassom foi realizado, ambos os parâmetros de US devem ser fornecidos")
    
    def _get_interpretation(self, score: int, us_performed: bool) -> Dict[str, str]:
        """
        Determina a interpretação baseada no escore e se US foi realizado
        
        Args:
            score: Escore calculado
            us_performed: Se ultrassom foi realizado
            
        Returns:
            Dict com interpretação
        """
        
        if not us_performed:
            # Sem ultrassom: ponto de corte ≥4
            if score >= 4:
                return {
                    "stage": "PMR",
                    "description": "Classifica como PMR (sem ultrassom)",
                    "interpretation": f"Escore de {score} pontos (≥4) classifica como polimialgia reumática pelos critérios EULAR/ACR 2012. Sensibilidade 72%, especificidade 65%."
                }
            else:
                return {
                    "stage": "Não-PMR",
                    "description": "Não classifica como PMR (sem ultrassom)",
                    "interpretation": f"Escore de {score} pontos (<4) não classifica como polimialgia reumática. Considere diagnósticos alternativos."
                }
        else:
            # Com ultrassom: ponto de corte ≥5
            if score >= 5:
                return {
                    "stage": "PMR (US)",
                    "description": "Classifica como PMR (com ultrassom)",
                    "interpretation": f"Escore de {score} pontos (≥5) classifica como polimialgia reumática pelos critérios EULAR/ACR 2012 com ultrassom. Sensibilidade 71%, especificidade 70%."
                }
            else:
                return {
                    "stage": "Não-PMR (US)",
                    "description": "Não classifica como PMR (com ultrassom)",
                    "interpretation": f"Escore de {score} pontos (<5) não classifica como polimialgia reumática com ultrassonografia. Considere diagnósticos alternativos."
                }


def calculate_eular_acr_2012_pmr(morning_stiffness: str, hip_pain_limited_rom: str,
                                 rf_or_acpa: str, other_joint_pain: str,
                                 ultrasound_shoulder_hip: str = "not_performed",
                                 ultrasound_both_shoulders: str = "not_performed") -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = EularAcr2012PmrCalculator()
    return calculator.calculate(morning_stiffness, hip_pain_limited_rom,
                              rf_or_acpa, other_joint_pain,
                              ultrasound_shoulder_hip, ultrasound_both_shoulders)