import sentry_sdk
from nonebot.compat import model_dump
from nonebot.plugin import PluginMetadata
from nonebot import logger, get_driver, get_plugin_config

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="Sentry日志监控",
    description="使用Sentry监控机器人日志并处理报错",
    usage="在配置文件中填写Sentry DSN即可启用",
    type="application",
    homepage="https://github.com/nonebot/plugin-sentry",
    config=Config,
    supported_adapters=None,
)

driver = get_driver()
config = get_plugin_config(Config)


def init_sentry(config: Config):
    sentry_config = {key[7:]: value for key, value in model_dump(config).items()}
    sentry_sdk.init(**sentry_config)


if config.sentry_dsn:
    init_sentry(config)
else:
    logger.warning("Sentry DSN not provided! Sentry plugin disabled!")
