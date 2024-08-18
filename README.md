# WhatsAppChat
A proof of concept notebook of WhatsApp Q&amp;A Chat using LangChain and OpenAI


## Set-Up:

1. Create a .env file in the root of this project with the following variable:

```
OPENAI_API_KEY='your_openai_api_key'
```

Refer: https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt for any help to set up OpenAI API key.

2. To chat with the WhatsApp Group via the system, you'll need to export the group data. Open the desired WhatsApp Group, tap on the three dots -> More -> Export Chat -> Without Media.

3. Export the chat history as a .txt file and rename it to `chat_history.txt`. Then, create a `data` folder in the root of the project if it doesn't exist and place the file inside it.


## Usage:

Use the `WhatsAppChat_LangChain.ipynb` notebook to chat with the WhatsApp Group.


# WhatsApp Chat History Parser

This Python script parses WhatsApp chat history exported as a text file. It provides various options for filtering, anonymizing, and processing the chat data.

```
python parse.py data/recent_chat_history.txt output_file.txt --previous_weeks 2 --anonymize
```
## Features

- Parse WhatsApp chat history from a text file
- Filter chat history by date range
- Fetch chat history for a specified number of previous weeks
- Anonymize sender names/phone numbers
- Save filtered and processed results to a new text file

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository or download the script file.
2. Ensure you have Python 3.6 or higher installed on your system.

## Usage

Run the script from the command line with the following syntax:

```
python whatsapp_chat_parser.py <input_file> <output_file> [options]
```

### Basic Arguments

- `input_file`: Path to the input chat history text file (required)
- `output_file`: Path where the processed chat history will be saved (required)

### Options

- `--start_date START_DATE`: Start date for filtering (format: MM/DD/YY)
- `--end_date END_DATE`: End date for filtering (format: MM/DD/YY)
- `--previous_weeks WEEKS`: Number of previous weeks to fetch
- `--anonymize`: Anonymize sender names/phone numbers

## Examples

1. Parse entire chat history without filtering:
   ```
   python whatsapp_chat_parser.py input_chat.txt output_chat.txt
   ```

2. Filter chat history by date range:
   ```
   python whatsapp_chat_parser.py input_chat.txt output_chat.txt --start_date 04/15/24 --end_date 04/30/24
   ```

3. Fetch the previous two weeks of chat history:
   ```
   python whatsapp_chat_parser.py input_chat.txt output_chat.txt --previous_weeks 2
   ```

4. Anonymize sender names/phone numbers:
   ```
   python whatsapp_chat_parser.py input_chat.txt output_chat.txt --anonymize
   ```

5. Combine multiple options:
   ```
   python whatsapp_chat_parser.py input_chat.txt output_chat.txt --start_date 04/15/24 --end_date 04/30/24 --anonymize
   ```

## Detailed Option Descriptions

### Date Range Filtering

Use `--start_date` and `--end_date` to specify a date range for filtering the chat history. Both options should be used together.

- Format: MM/DD/YY
- Example: `--start_date 04/15/24 --end_date 04/30/24`

This will include all messages from April 15, 2024, to April 30, 2024, inclusive.

### Previous Weeks

Use `--previous_weeks` to fetch chat history for a specified number of weeks counting back from the most recent message in the chat.

- Example: `--previous_weeks 2`

This will include all messages from the two weeks prior to the most recent message in the chat history.

### Anonymization

Use `--anonymize` to replace all sender names or phone numbers with anonymous identifiers.

- Sender names/numbers are replaced with identifiers like "A1", "A2", ..., "Z20"
- The same sender always gets the same identifier throughout the chat
- Identifiers are assigned in the order that unique senders appear in the chat history

## Output Format

The processed chat history is saved in the following format:

```
MM/DD/YY, HH:MM - Sender: Message
```

If anonymization is used, "Sender" will be replaced with the anonymous identifier.

## Notes

- The script assumes the input file is in UTF-8 encoding. If your file uses a different encoding, you may need to modify the `open()` function calls in the script.
- The script uses regular expressions to parse the chat history. If your chat history format differs significantly from the expected format, you may need to adjust the regular expression pattern in the `parse_chat_history()` function.

## Troubleshooting

If you encounter any issues:

1. Ensure your input file is in the correct format.
2. Check that you're using the correct date format (MM/DD/YY) for filtering options.
3. Verify that your Python version is 3.6 or higher.

For any other issues or feature requests, please open an issue in the GitHub repository.