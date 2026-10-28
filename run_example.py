from pyfedappwrap.engine.config.system_config import system_settings
from pyfedappwrap.engine.runtime import FedDBEngine

from app import MyAPP



engine = FedDBEngine(test_mode=True)

engine.register(MyAPP())

if __name__ == "__main__":
    engine.start()
    engine.wait_until_stop()
