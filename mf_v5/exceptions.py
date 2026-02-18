"""Custom exceptions for the MF v5.1 procedural engine."""

class MFError(Exception):
    """Base exception for all MF v5.1 errors."""
    pass

class GenerationError(MFError):
    """Raised when the procedural generation process fails."""
    pass

class GeometryError(MFError):
    """Raised when mesh creation or bmesh operations fail."""
    pass

class ExportError(MFError):
    """Raised when GLB export or manifest generation fails."""
    pass

class ConfigurationError(MFError):
    """Raised when invalid parameters are provided to the engine."""
    pass
