import http.server
import socketserver
import json
import csv
import urllib.parse
import random
import os

PORT = 8000
DATASET_FILE = 'dataset.csv'

def load_dataset():
    data = {}
    if os.path.exists(DATASET_FILE):
        with open(DATASET_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row['url'].strip().lower()
                data[url] = {
                    'visual_design': float(row['visual_design']),
                    'mobile_experience': float(row['mobile_experience']),
                    'content_clarity': float(row['content_clarity']),
                    'accessibility': float(row['accessibility']),
                    'navigation': float(row['navigation']),
                    'content_volume': float(row['content_volume']),
                    'issues_identified': int(row['issues_identified']),
                    'critical_fixes': int(row['critical_fixes']),
                    'score_gain': int(row['score_gain'])
                }
    return data

DATASET = load_dataset()

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/analyze':
            query = urllib.parse.parse_qs(parsed_path.query)
            url = query.get('url', [''])[0].strip().lower()
            
            # Remove trailing slash for better matching
            if url.endswith('/'):
                url = url[:-1]
                
            if url in DATASET:
                result = DATASET[url]
                result['is_mock'] = False
            else:
                # Generate realistic random data if URL not found
                result = {
                    'visual_design': round(random.uniform(2.0, 9.0), 1),
                    'mobile_experience': round(random.uniform(2.0, 9.0), 1),
                    'content_clarity': round(random.uniform(2.0, 9.0), 1),
                    'accessibility': round(random.uniform(2.0, 9.0), 1),
                    'navigation': round(random.uniform(2.0, 9.0), 1),
                    'content_volume': round(random.uniform(2.0, 9.0), 1),
                    'issues_identified': random.randint(5, 35),
                    'critical_fixes': random.randint(1, 12),
                    'score_gain': random.randint(10, 85),
                    'is_mock': True
                }
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            # Serve static files for all other paths
            super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"Serving fullstack server at http://localhost:{PORT}")
        print("To stop the server, press Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
