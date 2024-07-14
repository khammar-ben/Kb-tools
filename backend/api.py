# app.py
from flask import Flask, request, jsonify, send_from_directory, request
from flask_cors import CORS, cross_origin
from check_spf_dmarc import check_spf, check_dmarc
import os   


app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

@app.route('/api/check_records', methods=['POST'])

def check_records():
    data = request.json
    domains = data.get('domains')
    if not domains or not isinstance(domains, list):
        return jsonify({'error': 'No domains provided or invalid format'}), 400
    
    results = []
    for domain in domains:
        spf_record = check_spf(domain)
        dmarc_record = check_dmarc(domain)
        results.append({
            'domain': domain,
            'spf_record': spf_record,
            'dmarc_record': dmarc_record
            
        })
    
    return jsonify(results)

frontend_folder = os.path.join(os.getcwd(), "..", "frontend") 
build_folder = os.path.join(frontend_folder,"build")

# Server static files from the "dist" folder under the "frontend" directory
@app.route("/",defaults={"filename":""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(build_folder,filename)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/Check_spf_dmarc', methods=['GET'])
def check_spf_dmarc():
    try:
        # Your logic here, e.g., checking SPF/DKIM records
        result = {"status": "success", "message": "SPF/DMARC check passed"}
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"Error in /Check_spf_dmarc: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500





if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change port to 5001

