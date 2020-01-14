from pathlib import Path

PROJECT = Path(__file__).resolve().parent
STATIC_CODES = PROJECT/'codes.json'
UPDATE_CODES_INTERVAL = 5 * 60 * 60 * 24

SLEEP_BETWEEN_EPOCH = 300  # seconds
SLEEP_BETWEEN_REQ = 3    # seconds

VOL_THRESHOLD = 500