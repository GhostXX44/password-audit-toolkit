import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
SESSION_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")

REPORT_FILE = os.path.join(BASE_DIR, f"report_{SESSION_TIME}.txt")


def init_report():
    with open(REPORT_FILE, "w") as f:
        f.write("=== Password Audit Toolkit Report ===\n")
        f.write(f"Session Started: {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")


def log_event(event, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(REPORT_FILE, "a") as f:
        f.write(f"[{timestamp}] [{level}] {event}\n")



def save_dictionary_info(count):
    log_event(f"Dictionary generated with {count} words")


def save_generated_hash(password, hash_value):
    log_event(f"Hash generated | Password: {password} | Hash: {hash_value}")


def save_cracked_password(hash_value, password, method="Unknown"):
    log_event(
        f"Password cracked | Method: {method} | Hash: {hash_value} | Password: {password}",
        level="SUCCESS"
    )


def log_error(error_msg):
    log_event(f"ERROR: {error_msg}", level="ERROR")


def finalize_report():
    with open(REPORT_FILE, "a") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Session Ended: {datetime.now()}\n")
        f.write("=== End of Report ===\n")
