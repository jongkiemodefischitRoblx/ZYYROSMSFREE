import subprocess
import time
import sys
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)
PROMPT = "ZYYRO-SMSFREE $ "
LOG_FILE = "sms_history.txt"

def typing(text, delay=0.03):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(msg="Processing"):
    spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    for i in range(20):
        print(f"\r{msg}... {spinner[i % len(spinner)]}", end="")
        time.sleep(0.1)
    print("\r" + " " * 60, end="\r")

# --- Check SIM / Signal ---
def check_sim():
    try:
        result = subprocess.run("termux-telephony-deviceinfo", shell=True, capture_output=True, text=True)
        if "error" in result.stdout.lower() or "No SIM" in result.stdout:
            return False
        return True
    except Exception:
        return False

def send_sms(number, message):
    try:
        subprocess.run(f'termux-sms-send -n "{number}" "ZYYRO-SMSFREE: {message}"', shell=True)
        return True
    except:
        return False

def log_sms(number, message, status):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{status}] {number} - \"{message}\" - {time_now}\n")

def menu_send_sms():
    if not check_sim():
        typing(Fore.RED + "⚠ SIM not ready or inactive. Cannot send SMS!" + Style.RESET_ALL)
        return

    typing(Fore.CYAN + "\nEnter phone number (+62...):" + Style.RESET_ALL)
    number = input("> ")

    typing(Fore.CYAN + "Enter your message:" + Style.RESET_ALL)
    message = input("> ")

    typing(Fore.YELLOW + "\nSending SMS..." + Style.RESET_ALL)
    loading_animation("Sending")

    success = send_sms(number, message)
    status = "SUCCESS" if success else "FAILED"
    typing(Fore.GREEN + f"{status} ✓ SMS Sent!\n" + Style.RESET_ALL if success else Fore.RED + f"{status} ❌\n" + Style.RESET_ALL)

    log_sms(number, message, status)

    print(Fore.MAGENTA + "[ REPLAY CHAT ]" + Style.RESET_ALL)
    replay = input("Press ENTER to continue or type NO to cancel: ")

    if replay.lower() == "no":
        return

    typing(Fore.CYAN + "\nSend Your Message Here:" + Style.RESET_ALL)
    reply_msg = input("> ")

    typing(Fore.YELLOW + "\nSending reply..." + Style.RESET_ALL)
    loading_animation("Replying")

    reply_success = send_sms(number, reply_msg)
    reply_status = "SUCCESS" if reply_success else "FAILED"
    log_sms(number, reply_msg, reply_status)

    final_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    typing(Fore.GREEN + f"\n✓ REPLY {reply_status}" + Style.RESET_ALL)
    print(Fore.CYAN + "\n--- MESSAGE INFO ---" + Style.RESET_ALL)
    print(Fore.YELLOW + f"NUMBER     : {number}")
    print(f"MESSAGE    : {reply_msg}")
    print(f"SENT AT    : {final_time}" + Style.RESET_ALL)

def main():
    while True:
        print(Fore.MAGENTA + "\n=== SMS-ZYYRO FREE [BETA v2] ===" + Style.RESET_ALL)
        print("1. Send SMS")
        print("2. Exit")

        choice = input(PROMPT)

        if choice == "1":
            menu_send_sms()
        elif choice == "2":
            typing("Exiting...", 0.03)
            break
        else:
            typing(Fore.RED + "Invalid option!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
