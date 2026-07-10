import re
import csv
from datetime import datetime

LOG_FILE = "auth.log"  # Replace with your log files
OUTPUT_FILE = "threat_report.csv"

failed_login_pattern = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)")
success_login_pattern = re.compile(r"Accepted password for .* from (\d+\.\d+\.\d+\.\d+)")

ip_attempts = {}

def analyze_logs():
    with open(LOG_FILE, "r") as file:
        for line in file:
            failed_match = failed_login_pattern.search(line)
            success_match = success_login_pattern.search(line)

            if failed_match:
                ip = failed_match.group(1)
                ip_attempts[ip] = ip_attempts.get(ip, 0) + 1

            elif success_match:
                ip = success_match.group(1)
                ip_attempts[ip] = ip_attempts.get(ip, 0)

def detect_threats(threshold=5):
    threats = []
    for ip, attempts in ip_attempts.items():
        if attempts >= threshold:
            threats.append((ip, attempts))
    return threats

def save_report(threats):
    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Failed Attempts", "Threat Level", "Timestamp"])

        for ip, attempts in threats:
            threat_level = "HIGH" if attempts > 10 else "MEDIUM"
            writer.writerow([ip, attempts, threat_level, datetime.now()])

def alert(threats):
    if threats:
        print("\n🚨 ALERT: Suspicious Activity Detected 🚨")
        for ip, attempts in threats:
            print(f"IP: {ip} | Failed Attempts: {attempts}")
    else:
        print("✅ No threats detected.")

def main():
    print("🔍 Analyzing logs...")
    analyze_logs()
    
    threats = detect_threats()
    
    alert(threats)
    save_report(threats)
    
    print(f"\n📄 Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
