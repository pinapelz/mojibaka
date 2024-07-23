from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import chardet

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """
    Render the index.html template
    """
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect():
    """
    Detect the encoding of the provided text
    Returns: JSON object of all possible encodings and their confidence
    """
    # Stub: TODO
    data = request.get_json()
    text = data['text']
    result = chardet.detect(text.encode('latin-1'))
    return jsonify(result)

############################################
#       Language Conversion Functions      #
############################################

def convert_mandarin(text: str):
    """
    Convert the provided text from garbled Chinese simplified to readable Chinese simplified
    Returns: String of the converted text
    """
    cp936_bytes = text.encode('latin-1')  # Encode to bytes using latin-1
    utf16_bytes = cp936_bytes.decode('cp936').encode('utf-16')  # Decode CP936 and encode to UTF-16
    result = utf16_bytes.decode('utf-16')
    return result

#############################################

@app.route('/api/convert', methods=['POST'])
def convert():
    """
    Convert the text from garbled characters to specified language
    Returns: JSON object with the converted text
    """
    data = request.get_json()
    text = data['text']
    # Default to simplified Chinese if language is not provided
    language = data.get('language', 'simplified_cn')
    success = True
    match language:
        case 'simplified_cn':
            result = language_converter.convert_mandarin(text)
        case _:
            result = text
            success = False
    return jsonify({'text': result, 'success': success})

if __name__ == "__main__":
    app.run(debug=True)
