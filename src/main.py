import asyncio
from viam.module.module import Module
from .models.ping_monitor import PingMonitor
from .models.speedtest import Speedtest


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
