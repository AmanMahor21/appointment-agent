from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_bookings_per_user: int = 3
    openai_api_key: str
    telegram_bot_token: str
    telegram_webhook_url: str       # e.g. https://yourdomain.com/webhook
    database_url: str = "appointments.db"
    model_name: str = "llama-3.1-8b-instant"
    upstash_redis_rest_url: str
    upstash_redis_rest_token: str
    rate_limit: int = 10
    rate_limit_window: int = 60

    @property
    def telegram_api_base(self) -> str:
        return f"https://api.telegram.org/bot{self.telegram_bot_token}"

    class Config:
        env_file = ".env"


settings = Settings()
