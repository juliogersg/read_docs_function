import azure.functions as func
from api import api

app = func.AsgiFunctionApp(
    app=api.app, 
    http_auth_level=func.AuthLevel.ANONYMOUS
    )