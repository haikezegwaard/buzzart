import models as ga_models
from monitor import models


def get_settings_by_project_id(project_id):
    """
    Helper lookup function, retrieve analyticssettings object
    by given project id
    """
    project = models.Project.objects.get(id = project_id)
    return ga_models.AnalyticsSettings.objects.get(project = project)

def get_view_by_project_id(project_id):
    """
    Lookup and return view id for given project_id
    """
    settings = get_settings_by_project_id(project_id)
    return settings.ga_view
