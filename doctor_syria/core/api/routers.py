"""
Core API router utilities for consistent API URL patterns across the application.
"""
from rest_framework import routers


class ExtendedDefaultRouter(routers.DefaultRouter):
    """
    Extended router that adds additional functionality to the DefaultRouter.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the router with Arabic documentation support.
        """
        super().__init__(*args, **kwargs)
        self.include_format_suffixes = False
        
    def get_api_root_view(self, api_urls=None):
        """
        Customize API root view with Arabic documentation.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        return self.APIRootView.as_view(api_root_dict=api_root_dict)


def create_router(app_name):
    """
    Create a router instance with predefined settings for an app.
    
    Args:
        app_name (str): The name of the app to create router for
        
    Returns:
        ExtendedDefaultRouter: Configured router instance
    """
    router = ExtendedDefaultRouter()
    router.include_root_view = True
    return router
