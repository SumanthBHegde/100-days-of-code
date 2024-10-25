import os
import shutil
import yagmail
import psutil
import argparse
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import schedule
import time
import datetime

# Email Automation
def check_and_send_emails(email, password, subject_filter):
    yag = yagmail.SMTP(email, password)
    print("Checking emails...")
    
    # assuming a report request email is recieved
    if subject_filter.lower() in "report":
        yag.send(to=email, subject="Automated Report", contents="Here is your requested report!")
        print("Email sent!")
    
# File Backup
def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    for filename in os.listdir(source_dir):
        full_file_path = os.path.join(source_dir, filename)
        if os.path.isfile(full_file_path):
            shutil.copy(full_file_path, backup_dir)
            print(f"Backed up {filename} to {backup_dir}")
    print("Backup complete")
    
# System Monitoring
def monitor_system(cpu_threshold):
    print("Monitoring System....")
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > cpu_threshold:
        print(f"High CPU Usage Detected: {cpu_usage}%")
        
        # Sending alert
        print(f"Sending alert: CPU usage is {cpu_usage}%")
    else:
        print(f"CPU usage is {cpu_usage}%")

# PDF Report Generation
def generate_pdf_report(input_csv, output_pdf):
    print(f"Generating report from {input_csv}....")
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Task Automation Report")
    
    y = 700
    with open(input_csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            c.drawString(100, y, f"Task: {row[0]} - Status: {row[1]}")
            y -= 20
    c.save()
    print(f"PDF report saved as {output_pdf}")
    
# Scheduling Tasks
def schedule_tasks(task, **kwargs):
    if task == "email":
        schedule.every(1).day.do(check_and_send_emails, kwargs['email'], kwargs['password'], kwargs['filter'])
    elif task == "backup":
        schedule.every().day.at("12:00").do(backup_files, kwargs['source_dir'], kwargs['backup_dir'])
    elif task == "monitor":
        schedule.every(10).seconds.do(monitor_system, kwargs['cpu_threshold'])
    elif task == "report":
        schedule.every().day.at("17:00").do(generate_pdf_report, kwargs['input_file'], kwargs['output_file'])

    while True:
        schedule.run_pending()
        time.sleep(1)

# --- CLI Interface ---
def main():
    parser = argparse.ArgumentParser(description="Task Automation Bot")
    
    subparsers = parser.add_subparsers(dest="task")

    # Email Automation
    email_parser = subparsers.add_parser("email", help="Automate email tasks")
    email_parser.add_argument("--email", required=True, help="Your email address")
    email_parser.add_argument("--password", required=True, help="Your email password")
    email_parser.add_argument("--filter", required=False, default="", help="Subject filter for emails")

    # File Backup
    backup_parser = subparsers.add_parser("backup", help="Automate file backup")
    backup_parser.add_argument("--source-dir", required=True, help="Directory to back up")
    backup_parser.add_argument("--backup-dir", required=True, help="Backup destination directory")

    # System Monitoring
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system performance")
    monitor_parser.add_argument("--cpu-threshold", type=int, required=True, help="CPU usage threshold for alerts")

    # PDF Report Generation
    report_parser = subparsers.add_parser("report", help="Generate PDF report")
    report_parser.add_argument("--input-file", required=True, help="CSV file containing task data")
    report_parser.add_argument("--output-file", required=True, help="Output PDF file name")

    # Scheduling tasks
    schedule_parser = subparsers.add_parser("schedule", help="Schedule automated tasks")
    schedule_parser.add_argument("--task", required=True, help="Task to schedule (email, backup, monitor, report)")

    args = parser.parse_args()

    if args.task == "email":
        check_and_send_emails(args.email, args.password, args.filter)
    elif args.task == "backup":
        backup_files(args.source_dir, args.backup_dir)
    elif args.task == "monitor":
        monitor_system(args.cpu_threshold)
    elif args.task == "report":
        generate_pdf_report(args.input_file, args.output_file)
    elif args.task == "schedule":
        schedule_tasks(args.task)

if __name__ == "__main__":
    main()