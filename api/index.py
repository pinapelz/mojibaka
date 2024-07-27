from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

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

if __name__ == "__main__":
    app.run(debug=True)