import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# Helper functions
def decode_file(file_b64):
    try:
        decoded_file = base64.b64decode(file_b64)
        return decoded_file, True
    except:
        return None, False

def file_info(file_data):
    file_size_kb = len(file_data) / 1024  # Convert to KB
    return file_size_kb

@app.route('/bfhl', methods=['POST', 'GET'])
def bfhl():
    if request.method == 'POST':
        try:
            # Extract user data
            data = request.json.get('data', [])
            file_b64 = request.json.get('file_b64', None)
            email = "sa5251@srmist.edu.in"  # Your College Email ID
            roll_number = "RA2111003010510"  # Your College Roll Number
            full_name = "sarthak_agarwal"  # Modify with your full name
            dob = "17091999"  # Modify with your date of birth
            user_id = f"{full_name}_{dob}"
            
            # Extract numbers and alphabets
            numbers = [item for item in data if item.isdigit()]
            alphabets = [item for item in data if item.isalpha()]
            
            # Highest lowercase alphabet
            lowercase_alphabets = [char for char in alphabets if char.islower()]
            highest_lowercase = max(lowercase_alphabets) if lowercase_alphabets else None
            
            # File handling
            file_valid = False
            file_mime_type = None
            file_size_kb = None
            if file_b64:
                decoded_file, file_valid = decode_file(file_b64)
                if file_valid:
                    file_size_kb = file_info(decoded_file)
                    file_mime_type = "application/octet-stream"  # Modify based on content
                
            # Success Response
            response = {
                "is_success": True,
                "user_id": user_id,
                "email": email,
                "roll_number": roll_number,
                "numbers": numbers,
                "alphabets": alphabets,
                "highest_lowercase_alphabet": [highest_lowercase] if highest_lowercase else [],
                "file_valid": file_valid,
                "file_mime_type": file_mime_type,
                "file_size_kb": file_size_kb
            }
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"is_success": False, "error": str(e)}), 400

    elif request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

if __name__ == "__main__":
    app.run(debug=True)
