from django.http import JsonResponse
from analyzer.utils.pdf_extractor import PdfReader
from logs.logguer import logger

def validate_and_extract(document, pdf_file):
    
    pdf_reader = PdfReader(document.resume_file.path)
    loader = pdf_reader.reader()
    
    full_text = loader.get("full_text", "")
    num_pages = loader.get("num_pages", 0)
    logger.info(f"Páginas extraídas: {num_pages}")

    if num_pages > 6:
        raise ValueError("El CV tiene más de 6 páginas. Por favor, sube un CV con menos de 6 páginas.")

    if not full_text:
         raise ValueError("No se pudo extraer texto del PDF. Archivo vacío o corrupto.")

    return full_text, num_pages

def handle_analysis_error(document, e):
    error_message = f"Error en el proceso de análisis o carga: {str(e)}"
    logger.error(f"ERROR: {error_message}")
    
    if document:
        try:
            document.delete()
        except Exception as delete_error:
             logger.warning(f"Advertencia: No se pudo eliminar el documento fallido de la DB. Error: {delete_error}")
             
    return JsonResponse({"success": False, "error": error_message}, status=500)