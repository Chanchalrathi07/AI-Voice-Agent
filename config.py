# from pydantic_settings import BaseSettings
# import os
# from dotenv import load_dotenv

# load_dotenv()



#     # murf_api_key: str = os.getenv("MURF_API_KEY")
#     # murf_base_url: str = os.getenv("MURF_BASE_URL", "https://api.murf.ai")
#     # assemblyai_api_key: str = os.getenv("ASSEMBLYAI_API_KEY") 
# class Settings(BaseSettings):
#     murf_api_key: str
#     murf_base_url: str = "https://api.murf.ai"
#     assemblyai_api_key: str
#     class Config:
#         env_file = ".env"


# settings = Settings()
# config.py

# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     murf_api_key: str
#     murf_base_url: str = "https://api.murf.ai"
#     assemblyai_api_key: str
#     gemini_api_key: str

#     class Config:
#         env_file = ".env"  # Tells pydantic to load from .env file

# # Create a settings instance to use in the app
# settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    murf_api_key: str
    murf_base_url: str = "https://api.murf.ai"
    assemblyai_api_key: str
    gemini_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

