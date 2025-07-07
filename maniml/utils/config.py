"""
Configuration compatibility layer.
"""

import maniml.manimgl_core
import warnings


class manimlConfig:
    """CE-compatible configuration object."""
    
    def __init__(self):
        # Common configuration values
        self.pixel_height = 1080
        self.pixel_width = 1920
        self.frame_rate = 60
        self.background_color = "#000000"
        
        # CE-specific configs that don't apply to GL
        self.verbosity = "INFO"
        self.progress_bar = True
        self.preview = False
        self.write_to_movie = True
        self.save_last_frame = False
        self.media_dir = "./media"
        self.log_dir = "./logs"
        
        # Try to get GL config values
        from maniml import manimgl_core
        if hasattr(manimgl_core, 'config'):
            gl_config = manimgl_core.config
            if hasattr(gl_config, 'pixel_height'):
                self.pixel_height = gl_config.pixel_height
            if hasattr(gl_config, 'pixel_width'):
                self.pixel_width = gl_config.pixel_width
            if hasattr(gl_config, 'frame_rate'):
                self.frame_rate = gl_config.frame_rate
    
    def __getattr__(self, name):
        """Handle CE config requests that don't exist in GL."""
        warnings.warn(
            f"maniml: Config '{name}' not supported in GL backend.",
            UserWarning
        )
        return None
    
    @property
    def aspect_ratio(self):
        """Calculate aspect ratio."""
        return self.pixel_width / self.pixel_height
    
    @property
    def frame_width(self):
        """Get frame width in GL units."""
        from maniml import manimgl_core
        if hasattr(manimgl_core, 'FRAME_WIDTH'):
            return manimgl_core.FRAME_WIDTH
        return 14.2  # Default
    
    @property 
    def frame_height(self):
        """Get frame height in GL units."""
        from maniml import manimgl_core
        if hasattr(manimgl_core, 'FRAME_HEIGHT'):
            return manimgl_core.FRAME_HEIGHT
        return 8.0  # Default


# Create singleton config object
config = manimlConfig()