from pathlib import Path
TEST_MODE = False

PROJECT = Path(__file__).resolve().parent
STATIC_CODES = PROJECT/'codes.json'
TELEGRAM_JSON_FILE = PROJECT/'telegram.json'
UPDATE_CODES_INTERVAL = 5 * 60 * 60 * 24
SLEEP_BETWEEN_EPOCH = 60  # seconds
SLEEP_BETWEEN_REQ = 3    # seconds
WEEK_AVG_TIMES = 2

import logging
FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
LOGGER = logging.getLogger('Console')
LOGGER.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setFormatter(FORMATTER)
LOGGER.addHandler(console)
LOGGER.info("Init...")


## Get Single Stock info
class StockInfoSetting:
    RETRY_MAX_TIME = 3