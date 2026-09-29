import os
from flask import Flask, render_template, request, jsonify
from database import init_db, save_meeting, get_all_meetings, get_meeting_by_id, update_meeting_brief, delete_meeting
from generator import generate_meeting_brief
from samples import SAMPLES, get_sample_by_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meeting-prep-agent-secret-key-2026'

# Ensure database is initialized
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prepare-meeting', methods=['POST'])
def prepare_meeting():
    try:
        data = request.get_json() or {}
        
        title = data.get('title', '').strip()
        person_company = data.get('person_company', '').strip()
        date_time = data.get('date_time', '').strip()
        purpose = data.get('purpose', '').strip()
        previous_notes = data.get('previous_notes', '').strip()
        additional_info = data.get('additional_info', '').strip()
        api_key = data.get('api_key', '').strip()
        save_history = data.get('save_history', True)

        if not title:
            return jsonify({'success': False, 'error': 'Meeting title is required.'}), 400
        if not person_company:
            return jsonify({'success': False, 'error': 'Person or Company name is required.'}), 400

        # Generate the Meeting Preparation Brief
        brief = generate_meeting_brief(
            title=title,
            person_company=person_company,
            date_time=date_time,
            purpose=purpose,
            previous_notes=previous_notes,
            additional_info=additional_info,
            api_key=api_key if api_key else None
        )

        meeting_id = None
        if save_history:
            meeting_id = save_meeting(
                title=title,
                person_company=person_company,
                date_time=date_time,
                purpose=purpose,
                previous_notes=previous_notes,
                additional_info=additional_info,
                brief_data=brief
            )

        return jsonify({
            'success': True,
            'meeting_id': meeting_id,
            'brief': brief,
            'message': 'Meeting Preparation Brief generated successfully.'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to generate brief: {str(e)}'}), 500

@app.route('/api/meetings', methods=['GET'])
def list_meetings():
    try:
        meetings = get_all_meetings()
        return jsonify({'success': True, 'meetings': meetings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/meetings/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    try:
        meeting = get_meeting_by_id(meeting_id)
        if not meeting:
            return jsonify({'success': False, 'error': 'Meeting brief not found.'}), 404
        return jsonify({'success': True, 'meeting': meeting})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/meetings/<int:meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    try:
        data = request.get_json() or {}
        brief = data.get('brief')
        if not brief:
            return jsonify({'success': False, 'error': 'No brief data provided.'}), 400
        
        update_meeting_brief(meeting_id, brief)
        return jsonify({'success': True, 'message': 'Brief updated successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/meetings/<int:meeting_id>', methods=['DELETE'])
def remove_meeting(meeting_id):
    try:
        deleted = delete_meeting(meeting_id)
        if deleted:
            return jsonify({'success': True, 'message': 'Meeting deleted successfully.'})
        return jsonify({'success': False, 'error': 'Meeting not found.'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/samples', methods=['GET'])
def list_samples():
    return jsonify({'success': True, 'samples': SAMPLES})

@app.route('/api/samples/<sample_id>', methods=['GET'])
def get_sample(sample_id):
    sample = get_sample_by_id(sample_id)
    if sample:
        return jsonify({'success': True, 'sample': sample})
    return jsonify({'success': False, 'error': 'Sample not found.'}), 404

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

@app.route('/api/network-info', methods=['GET'])
def network_info():
    local_ip = get_local_ip()
    port = int(os.environ.get('PORT', 8080))
    return jsonify({
        'success': True,
        'local_ip': local_ip,
        'port': port,
        'local_url': f"http://localhost:{port}",
        'network_url': f"http://{local_ip}:{port}"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    local_ip = get_local_ip()
    print(f"Meeting Prep Agent running at http://localhost:{port}")
    print(f"Local URL:   http://localhost:{port}")
    print(f"Network URL: http://{local_ip}:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
