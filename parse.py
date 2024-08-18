import re
from datetime import datetime, timedelta
import argparse
import string

def parse_chat_history(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to match the date, time, sender, and message
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.+)'
    matches = re.findall(pattern, content, re.MULTILINE)
    
    parsed_messages = []
    for match in matches:
        date, time, sender, message = match
        date_obj = datetime.strptime(f"{date} {time}", "%m/%d/%y %H:%M")
        parsed_messages.append({
            'date': date_obj,
            'sender': sender.strip(),
            'message': message.strip()
        })
    
    return parsed_messages

def filter_by_date_range(messages, start_date, end_date):
    return [msg for msg in messages if start_date <= msg['date'] <= end_date]

def get_previous_weeks_history(messages, weeks=2):
    end_date = max(msg['date'] for msg in messages)
    start_date = end_date - timedelta(weeks=weeks)
    return filter_by_date_range(messages, start_date, end_date)

def anonymize_senders(messages):
    unique_senders = list(set(msg['sender'] for msg in messages))
    anonymized_senders = {}
    
    for i, sender in enumerate(unique_senders):
        letter = string.ascii_uppercase[i // 20]
        number = i % 20 + 1
        anonymized_senders[sender] = f"{letter}{number}"
    
    anonymized_messages = []
    for msg in messages:
        anonymized_msg = msg.copy()
        anonymized_msg['sender'] = anonymized_senders[msg['sender']]
        anonymized_messages.append(anonymized_msg)
    
    return anonymized_messages

def save_to_file(messages, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for msg in messages:
            file.write(f"{msg['date'].strftime('%m/%d/%y, %H:%M')} - {msg['sender']}: {msg['message']}\n")

def main():
    parser = argparse.ArgumentParser(description="Parse and filter WhatsApp chat history")
    parser.add_argument("input_file", help="Path to the input chat history file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("--start_date", help="Start date for filtering (MM/DD/YY)")
    parser.add_argument("--end_date", help="End date for filtering (MM/DD/YY)")
    parser.add_argument("--previous_weeks", type=int, help="Number of previous weeks to fetch")
    parser.add_argument("--anonymize", action="store_true", help="Anonymize sender names")

    args = parser.parse_args()

    messages = parse_chat_history(args.input_file)

    if args.start_date and args.end_date:
        start_date = datetime.strptime(args.start_date, "%m/%d/%y")
        end_date = datetime.strptime(args.end_date, "%m/%d/%y")
        filtered_messages = filter_by_date_range(messages, start_date, end_date)
    elif args.previous_weeks:
        filtered_messages = get_previous_weeks_history(messages, args.previous_weeks)
    else:
        filtered_messages = messages

    if args.anonymize:
        filtered_messages = anonymize_senders(filtered_messages)

    save_to_file(filtered_messages, args.output_file)
    print(f"Filtered chat history saved to {args.output_file}")

if __name__ == "__main__":
    main()