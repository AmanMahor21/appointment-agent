from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    telegram_bot_token: str
    telegram_webhook_url: str       # e.g. https://yourdomain.com/webhook
    database_url: str = "appointments.db"
    model_name: str = "llama-3.1-8b-instant"

    @property
    def telegram_api_base(self) -> str:
        return f"https://api.telegram.org/bot{self.telegram_bot_token}"

    class Config:
        env_file = ".env"


settings = Settings()
