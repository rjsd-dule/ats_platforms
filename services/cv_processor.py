from .gemini_client import GeminiModel
from analyzer.utils.prompt_templates import cv_prompt
from logs.logguer import logger
import json
import re

class CVProcessor:
    def __init__(self, full_text, puesto_objetivo: str):
        self.full_text = full_text
        self.puesto_objetivo = puesto_objetivo
        self.max_output_limit = 4096
        
        self.llm = GeminiModel().get_llm(
            temperature=0.0,
            max_tokens=self.max_output_limit
        )

    def analyze(self):
        try:
            logger.info("--- Iniciando Análisis del CV ---")
            
            chain = cv_prompt | self.llm
            response = chain.invoke({
                "context": self.full_text[:100000],
                "puesto_objetivo": self.puesto_objetivo
            })

            raw_content = response.content.strip()
            logger.info(f" Respuesta cruda (200 chars): {raw_content[:200]}...")

            try:
                return json.loads(raw_content)
            except json.JSONDecodeError:
                logger.warning("Primer intento falló. Intentando limpieza leve...")

            cleaned = raw_content.replace("```json", "").replace("```", "").strip()

            return json.loads(cleaned)

        except json.JSONDecodeError as err:
            logger.error(f"Error al parsear JSON: {err}")
            raise ValueError("La respuesta del LLM no es un JSON válido.")

        except Exception as e:
            logger.error(f"Error general analizando CV: {str(e)}")
            raise e
