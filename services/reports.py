from flask import Blueprint, jsonify, send_file
from core.jwt import validate_token
from flasgger import swag_from
import pdfkit

reports_bp = Blueprint('reports', __name__, url_prefix='/v1/reports/')

@reports_bp.route('/monthly-events', methods=['GET'])
@validate_token()
@swag_from({
    'summary': 'Endpoint for fetching monthly events.',
    'description': 'Returns a list of monthly events for the authenticated user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the authenticated user'
        }
    ],
    'responses': {
        200: {
            'description': 'A successful response with monthly events.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string'
                            },
                            'user_id': {
                                'type': 'integer'
                            }
                        }
                    }
                }
            }
        }
    }
})
def monthly_events(user_id):
    data = [
        {"name": "John", "surname": "Test"},
        # Add more data here
    ]

    # Generate HTML table from the data
    html = '<table border="1"><tr><th>Name</th><th>Surname</th></tr>'
    for entry in data:
        html += f'<tr><td>{entry["name"]}</td><td>{entry["surname"]}</td></tr>'
    html += '</table>'

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False)

    # Set the file name
    pdf_file_path = 'generated_pdf.pdf'

    # Save the PDF file
    with open(pdf_file_path, 'wb') as f:
        f.write(pdf)

    # Return the PDF file for download
    return send_file(pdf_file_path, as_attachment=True)


@reports_bp.route('/get_pdf')
def get_pdf():
    # Return the generated PDF file
    pdf_file_path = 'generated_pdf.pdf'
    return send_file(pdf_file_path, as_attachment=True)

    