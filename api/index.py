from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from g4f.client import Client

# https://github.com/rspeer/python-ftfy
# ftfy is Licensed under the Apache License, Version 2.0
import ftfy

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """
    Render the index.html template
    """
    return render_template('index.html')

@app.route('/ai')
def ai_index():
    """
    Render the ai_decode.html template
    Used for using LLMs to decode garbled text
    """
    return render_template('ai_decode.html')

############################################
#       Language Conversion Functions      #
############################################

def convert_simplified_cn(text: str, error_mode: str='replace') -> list:
    """
    Convert the provided text from garbled Chinese simplified to readable Chinese simplified
    Returns: List of tuples that contain the converted texts
    """
    # Assuming the text was incorrectly read as Latin-1 instead of GB2312/CP936
    try:
        l1_bytes = text.encode('latin-1')  # Encode to bytes using latin-1
    except UnicodeEncodeError:
        print("Conv_Could not encode text to Latin-1")
        return []
    results = []
    try:
        cp936_bytes = l1_bytes.decode('cp936', errors=error_mode).encode('utf-16', errors=error_mode)  # Decode CP936 and encode to UTF-16
        results.append(("cp936", cp936_bytes.decode('utf-16', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("Error decoding CP936")
    try:
        gb2312_bytes = l1_bytes.decode('gb2312', errors=error_mode).encode('utf-16', errors=error_mode)  # Decode GB2312 and encode to UTF-16
        results.append(("gb2312", gb2312_bytes.decode('utf-16', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("Error decoding GB2312")
    return results

def convert_japanese(text: str, error_mode: str='replace') -> list:
    """
    Convert the provided text from garbled Japanese to readable Japanese
    Returns: List of tuples that contain the converted texts
    
    Possible to recover some text:
    Encode utf8 decode iso-2022-jp
    Encode shift-jis decode iso-2022-jp
    Encode euc-jp decode iso-2022-jp
    Encode shift-jis decode euc-jp
    Encode sjis decode utf-8
    """
    results = []
    try:
        results.append(("utf8 to iso-2022-jp", text.encode('utf-8', errors=error_mode).decode('iso-2022-jp', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("JP: Error converting utf8 to iso-2022-jp")
    try:
        results.append(("shift-jis to iso-2022-jp", text.encode('shift-jis', errors=error_mode).decode('iso-2022-jp', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("JP: Error converting shift-jis to iso-2022-jp")
    try:
        results.append(("euc-jp to iso-2022-jp", text.encode('euc-jp', errors=error_mode).decode('iso-2022-jp', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("JP: Error converting euc-jp to iso-2022-jp")
    try:
        results.append(("shift-jis to euc-jp", text.encode('shift-jis', errors=error_mode).decode('euc-jp', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("JP: Error converting shift-jis to euc-jp")
    try:
        results.append(("sjis to utf-8", text.encode('shift-jis', errors=error_mode).decode('utf-8', errors=error_mode)))
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("JP: Error converting sjis to utf-8")
    return results


def open_ai_decode(text: str, api_key: str) -> str:
    """
    Attempt to use OpenAI to decode the provided text
    """
    print("GPT4 Decode")
    client = OpenAI(api_key=api_key)
    messages = [{"role": "user", "content": "The following text is corrupted due to using the wrong encoding/decoding format. Reply with the corrected readable text. Corrupted Text: " + text}]
    print(messages)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        print(response.choices[0])
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def g4f_ai_decode(text: str) -> str:
    """
    Attempt to use GPT4Free to decode the provided text
    """
    client = Client()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "The following text is corrupted due to using the wrong encoding/decoding format. Reply with the corrected readable text. Corrupted Text: " + text}])
    return response.choices[0].message.content

#############################################

@app.route('/api/convert', methods=['POST'])
def convert():
    """
    Convert the text from garbled characters to specified language
    Returns: JSON object with the converted text
    """
    data = request.get_json()
    text = data['text']
    error_mode = data['error_mode']
    # Default to simplified Chinese if language is not provided
    language = data.get('language', 'simplified_cn')
    success = True
    match language:
        case 'simplified_cn':
            results = convert_simplified_cn(text, error_mode=error_mode)
        case 'japanese':
            results = convert_japanese(text, error_mode=error_mode)
        case 'ftfy':
            results = [('"fixes text for you" conversion', ftfy.fix_text(text))]
        case _:
            results = text
            success = False
    return jsonify({'data': results, 'success': success})

@app.route('/api/ai', methods=['POST'])
def convert_ai():
    """
    Use AI to decode the garbled text
    Returns: JSON object with the converted text
    """
    data = request.get_json()
    text = data['text']
    model = data['model']
    api_key = data['api']
    # Default to simplified Chinese if language is not provided
    success = True
    match model:
        case 'openai_gpt4':
            result = open_ai_decode(text, api_key)
        case 'gpt4free':
            result = g4f_ai_decode(text)
        case _:
            success = False
            result = text
    return jsonify({'result': result, 'success': success})


if __name__ == "__main__":
    app.run(debug=True)