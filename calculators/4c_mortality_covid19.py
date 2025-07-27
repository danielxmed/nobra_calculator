"""
4C Mortality Score for COVID-19 Calculator

Prediz mortalidade hospitalar em pacientes internados com COVID-19.
Referência: Knight SR et al., BMJ 2020;370:m3339
"""

from typing import Dict, Any


class FourCMortalityCovid19Calculator:
    """Calculadora para o 4C Mortality Score para COVID-19"""
    
    def calculate(self, age: int, sex: str, comorbidities: int, respiratory_rate: int,
                 oxygen_saturation: float, glasgow_coma_scale: int, urea_unit: str,
                 urea_value: float, crp: float) -> Dict[str, Any]:
        """
        Calcula o 4C Mortality Score para COVID-19
        
        Args:
            age: Idade em anos
            sex: "masculino" ou "feminino"
            comorbidities: Número de comorbidades (0-20)
            respiratory_rate: Frequência respiratória (irpm)
            oxygen_saturation: Saturação de O2 (%)
            glasgow_coma_scale: Escala de Coma de Glasgow (3-15)
            urea_unit: "mmol_L" ou "mg_dL"
            urea_value: Valor da ureia sérica
            crp: Proteína C-reativa (mg/L)
            
        Returns:
            Dict com resultado, interpretação e classificação de risco
        """
        
        # Validações
        self._validate_inputs(age, sex, comorbidities, respiratory_rate,
                            oxygen_saturation, glasgow_coma_scale, urea_unit,
                            urea_value, crp)
        
        # Calcular pontuação
        score = 0
        
        # Idade (0-7 pontos)
        score += self._score_age(age)
        
        # Sexo (0-1 ponto)
        score += self._score_sex(sex)
        
        # Comorbidades (0-2 pontos)
        score += self._score_comorbidities(comorbidities)
        
        # Frequência respiratória (0-2 pontos)
        score += self._score_respiratory_rate(respiratory_rate)
        
        # Saturação de oxigênio (0-2 pontos)
        score += self._score_oxygen_saturation(oxygen_saturation)
        
        # Escala de Coma de Glasgow (0-2 pontos)
        score += self._score_glasgow_coma_scale(glasgow_coma_scale)
        
        # Ureia (0-3 pontos)
        score += self._score_urea(urea_value, urea_unit)
        
        # PCR (0-2 pontos)
        score += self._score_crp(crp)
        
        # Obter interpretação
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "pontos",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, comorbidities: int,
                        respiratory_rate: int, oxygen_saturation: float,
                        glasgow_coma_scale: int, urea_unit: str,
                        urea_value: float, crp: float):
        """Valida os parâmetros de entrada"""
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Idade deve ser um inteiro entre 0 e 120 anos")
        
        if sex not in ["masculino", "feminino"]:
            raise ValueError("Sexo deve ser 'masculino' ou 'feminino'")
        
        if not isinstance(comorbidities, int) or comorbidities < 0 or comorbidities > 20:
            raise ValueError("Número de comorbidades deve ser um inteiro entre 0 e 20")
        
        if not isinstance(respiratory_rate, int) or respiratory_rate < 5 or respiratory_rate > 60:
            raise ValueError("Frequência respiratória deve ser um inteiro entre 5 e 60 irpm")
        
        if not isinstance(oxygen_saturation, (int, float)) or oxygen_saturation < 50.0 or oxygen_saturation > 100.0:
            raise ValueError("Saturação de oxigênio deve estar entre 50.0 e 100.0%")
        
        if not isinstance(glasgow_coma_scale, int) or glasgow_coma_scale < 3 or glasgow_coma_scale > 15:
            raise ValueError("Escala de Coma de Glasgow deve ser um inteiro entre 3 e 15")
        
        if urea_unit not in ["mmol_L", "mg_dL"]:
            raise ValueError("Unidade da ureia deve ser 'mmol_L' ou 'mg_dL'")
        
        if not isinstance(urea_value, (int, float)) or urea_value < 0.1 or urea_value > 300.0:
            raise ValueError("Valor da ureia deve estar entre 0.1 e 300.0")
        
        if not isinstance(crp, (int, float)) or crp < 0.0 or crp > 1000.0:
            raise ValueError("PCR deve estar entre 0.0 e 1000.0 mg/L")
    
    def _score_age(self, age: int) -> int:
        """Calcula pontos para idade"""
        if age < 50:
            return 0
        elif age < 60:
            return 2
        elif age < 70:
            return 4
        elif age < 80:
            return 6
        else:  # ≥80
            return 7
    
    def _score_sex(self, sex: str) -> int:
        """Calcula pontos para sexo"""
        return 1 if sex == "masculino" else 0
    
    def _score_comorbidities(self, comorbidities: int) -> int:
        """Calcula pontos para comorbidades"""
        if comorbidities == 0:
            return 0
        elif comorbidities == 1:
            return 1
        else:  # ≥2
            return 2
    
    def _score_respiratory_rate(self, respiratory_rate: int) -> int:
        """Calcula pontos para frequência respiratória"""
        if respiratory_rate < 20:
            return 0
        elif respiratory_rate < 30:
            return 1
        else:  # ≥30
            return 2
    
    def _score_oxygen_saturation(self, oxygen_saturation: float) -> int:
        """Calcula pontos para saturação de oxigênio"""
        return 0 if oxygen_saturation >= 92.0 else 2
    
    def _score_glasgow_coma_scale(self, glasgow_coma_scale: int) -> int:
        """Calcula pontos para Escala de Coma de Glasgow"""
        return 0 if glasgow_coma_scale == 15 else 2
    
    def _score_urea(self, urea_value: float, urea_unit: str) -> int:
        """Calcula pontos para ureia"""
        if urea_unit == "mmol_L":
            # Conversão para mmol/L
            if urea_value < 7.0:
                return 0
            elif urea_value <= 14.0:
                return 1
            else:  # >14
                return 3
        else:  # mg_dL (BUN)
            # Conversão para mg/dL
            if urea_value < 19.6:
                return 0
            elif urea_value <= 39.2:
                return 1
            else:  # >39.2
                return 3
    
    def _score_crp(self, crp: float) -> int:
        """Calcula pontos para PCR"""
        if crp < 50.0:
            return 0
        elif crp < 100.0:
            return 1
        else:  # ≥100
            return 2
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determina a interpretação baseada no escore
        
        Args:
            score: Escore calculado (0-21)
            
        Returns:
            Dict com interpretação
        """
        
        if score <= 3:
            return {
                "stage": "Baixo Risco",
                "description": "Risco baixo de mortalidade",
                "interpretation": f"Escore de {score} pontos indica baixo risco com mortalidade hospitalar de 1.2-1.7%. Pacientes podem ser considerados para alta precoce ou manejo ambulatorial se clinicamente estáveis."
            }
        elif score <= 8:
            return {
                "stage": "Risco Intermediário",
                "description": "Risco intermediário de mortalidade",
                "interpretation": f"Escore de {score} pontos indica risco intermediário com mortalidade hospitalar de 9.1-9.9%. Pacientes requerem monitorização hospitalar padrão com vigilância para deterioração clínica."
            }
        elif score <= 14:
            return {
                "stage": "Alto Risco",
                "description": "Alto risco de mortalidade",
                "interpretation": f"Escore de {score} pontos indica alto risco com mortalidade hospitalar de 31.4-34.9%. Pacientes requerem cuidados intensivos ou monitorização em unidade de alta dependência."
            }
        else:  # ≥15
            return {
                "stage": "Risco Muito Alto",
                "description": "Risco muito alto de mortalidade",
                "interpretation": f"Escore de {score} pontos indica risco muito alto com mortalidade hospitalar de 61.5-66.2%. Pacientes requerem cuidados intensivos imediatos e consideração de limitação de suporte se apropriado."
            }


def calculate_4c_mortality_covid19(age: int, sex: str, comorbidities: int,
                                   respiratory_rate: int, oxygen_saturation: float,
                                   glasgow_coma_scale: int, urea_unit: str,
                                   urea_value: float, crp: float) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = FourCMortalityCovid19Calculator()
    return calculator.calculate(age, sex, comorbidities, respiratory_rate,
                              oxygen_saturation, glasgow_coma_scale, urea_unit,
                              urea_value, crp)