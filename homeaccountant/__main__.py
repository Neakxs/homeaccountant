import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)).rsplit('/',1)[0])

from homeaccountant.log.logger import getLogger, log_wrapper
from homeaccountant.server.api.app import WebAPI 

logger = getLogger()

log_wrapper.start()
api = WebAPI()
try:
    asyncio.get_event_loop().run_until_complete(api.run())
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logger.warning('Shutting down with KeyboardInterrupt')
log_wrapper.stop()