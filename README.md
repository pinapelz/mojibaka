# Mojibaka
This is a very simple static flask web app that attempts to resolve "mojibake". These are garbled characters that occur due to text being encoded/decoded in mismatching formats.

While not everything can be recovered 100% of the time (since its a lossy process), sometimes these mismatches line up just right such that none (or nearly none) of the characters are mapped to NULL, meaning that its just a matter of "remapping" everything to make the text readable again.

These days I still run into older Chinese/Japanese programs (specifically Windows installers) where the characters don't quite show up right. While you could troubleshoot fixing it, I find its handy to have a tool like this to quickly get the gist of whats happening.

# API Route
You're welcome to call the conversion route

## `/api/convert`

### Method: `POST`

### Description
Converts garbled text into a specified language or format.

### Request Body

- **text** (string): The text to convert.
- **error_mode** (string): Specifies error handling during conversion.
- **language** (string, optional): Target conversion type, defaults to `'simplified_cn'`. Supported values:
  - `'simplified_cn'`: Converts to Simplified Chinese.
  - `'japanese'`: Converts to Japanese.
  - `'ftfy'`: Applies the "fixes text for you" (ftfy) library.

### Response

- **data** (list/string): Converted text or original text if the conversion fails.
- **success** (boolean): `True` if conversion succeeds, otherwise `False`.

### Example

**Request:**
```json
{
    "text": "Garbled text",
    "error_mode": "strict",
    "language": "simplified_cn"
}
```

**Response**
```json
{
    "data": ["Simplified Chinese text"],
    "success": true
}
```

![Screenshot of Mojibaka site](https://files.catbox.moe/6vshtu.png)

Hosted at: https://mojibaka.pinapelz.com
