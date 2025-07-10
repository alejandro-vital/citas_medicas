class BusinessLogicError(Exception):
  """Excepción para errores de lógica de negocio"""
  pass

class ValidationError(Exception):
  """Excepción para errores de validación"""
  pass

class NotFoundError(Exception):
  """Excepción para recursos no encontrados"""
  pass