import time
import logging
import re
import requests

# Configure logging
logging.basicConfig(
    filename="log_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def monitor_log_file(file_path):
    """Continuously monitor the log file for errors."""
    try:
        with open(file_path, 'r') as log_file:
            # Move to the end of the file
            log_file.seek(0, 2)

            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(1)  # Wait for new lines to be written
                    continue

                if "ERROR" in line:
                    logging.info("Error detected: %s", line.strip())
                    debug_and_notify_slack(line)
    except Exception as e:
        logging.error("Exception in log monitoring: %s", str(e))

def debug_and_notify_slack(error_message):
    """Debug the error and notify Slack."""
    try:
        matches = re.findall(r'File "(.*?)", line (\d+), in (\w+)', error_message)
        if matches:
            # Select the last match
            file_path, line_number, method_name = matches[-1]
            line_number = int(line_number)

            # Read the specific method code as text
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Find the start of the method
                start_line = line_number - 1
                while start_line > 0 and not lines[start_line].strip().startswith(('def', 'async', '@')):
                    start_line -= 1

                # Find the end of the method
                end_line = line_number - 1
                while end_line < len(lines) and not lines[end_line].strip().startswith(('def', 'async', '@')):
                    end_line += 1

                method_code = ''.join(lines[start_line:end_line])

            logging.info("Extracted method code: \n%s", method_code)

            # Send truncated error message and method code to get_ai_response
            get_ai_response(error_message, method_code)
    except Exception as e:
        logging.error("Exception in debug_and_notify_slack: %s", str(e))

def get_ai_response(error_message, method_code):
    """Process the error message and method code using AI."""
    try:
        logging.info("Processing error message: %s", error_message)
        logging.info("Processing method code: \n%s", method_code)

        # Generate payload for AI call
        payload = generate_ai_payload(error_message, method_code)

        # Send POST request to AI service
        response = requests.post(
            "https://ai-services.k8s.latest0-su0.hspt.io/llm/general",
            json=payload
        )

        if response.status_code == 200:
            ai_response = response.json()
            ai_text = ai_response.get('choices', [{}])[0].get('text', 'No response text available')
            logging.info("AI Response Text: %s", ai_text)
            send_slack_notification(error_message, ai_text)  # Send notification to Slack
        else:
            logging.error("Failed to get AI response. Status code: %d, Response: %s", response.status_code, response.text)
    except Exception as e:
        logging.error("Exception in get_ai_response: %s", str(e))

def generate_ai_payload(error_message, method_code):
    """Generate payload for AI call."""
    return {
        "messages": [f" You are a software developer who works with python applications. You have encountered an error in your application, you are provided with error stack trace and exact code line where the error occurred along with a context of 5 lines above the error line and 5 lines below the error line. Error Stack Trace:\n{error_message}\n\nExtracted Method Code:\n{method_code}\n\nPlease provide a possible solution to resolve the issue."],
        "args": {
            "temperature": 0.7,
            "enable_event_logging": False
            },
        "prompt_key" : "chat_bot",
        "domain_id" : "highspot.com",

    }

def send_slack_notification(error_message, ai_response):
    """Send error stack trace and AI response to a Slack channel."""
    try:
        # Truncate the error message from the last occurrence of 'File'
        last_file_index = error_message.rfind('File')
        truncated_error_message = error_message[last_file_index:] if last_file_index != -1 else error_message

        # Slack webhook URL
        slack_webhook_url = "https://hooks.slack.com/services/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"

        # Construct the payload
        payload = {
            "text": f"*Error in Application:*\n```{truncated_error_message}```\n\n*Possible AI Solution:*\n```{ai_response}"
        }

        # Send POST request to Slack webhook
        response = requests.post(slack_webhook_url, json=payload)

        if response.status_code == 200:
            logging.info("Successfully sent notification to Slack.")
        else:
            logging.error("Failed to send notification to Slack. Status code: %d, Response: %s", response.status_code, response.text)
    except Exception as e:
        logging.error("Exception in send_slack_notification: %s", str(e))

if __name__ == "__main__":
    log_file_path = "application.log"
    logging.info("Starting log monitoring for file: %s", log_file_path)
    monitor_log_file(log_file_path)
