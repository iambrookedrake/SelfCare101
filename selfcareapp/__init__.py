"""Entry point for TwitOff aka SelfCare101 Flask Application."""
from selfcareapp import app
from .app import create_app

APP = create_app()
