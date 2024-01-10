from flask import Blueprint, send_file
from collections import defaultdict
from core.models import Event, EventType
from core.token import validate_token
from core.util import get_first_day_of_month
from flasgger import swag_from
import pdfkit

reports_bp = Blueprint('reports', __name__, url_prefix='/v1/reports/')

@reports_bp.route('/monthly-events', methods=['GET'])
@validate_token()
@swag_from({
    'summary': 'Endpoint for fetching and downloading monthly events as a PDF file.',
    'description': 'Downloads a PDF file containing monthly events for the authenticated user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'ID of the authenticated user'
        }
    ],
    'responses': {
        200: {
            'description': 'PDF file with monthly events.',
            'content': {
                'application/pdf': {
                    'schema': {
                        'type': 'file'
                    }
                }
            }
        }
    }
})
def monthly_events(user_id):
    events = Event.query.filter(
        Event.start_date >= get_first_day_of_month(),
        Event.user_id == user_id
    ).all()

    event_types = EventType.query.all()
    event_types_grouped = {et.id: et.title for et in event_types}

    html = '''
        <h1>Monthly events</h1>
        <table style="width: 100%; border-collapse: collapse; border: 1px solid black;">
        <tr>
            <th style="border: 1px solid black;">Event type</th>
            <th style="border: 1px solid black;">Start</th>
            <th style="border: 1px solid black;">End</th>
        </tr>'''

    for event in events:
        html += f'''<tr>
            <td style="border: 1px solid black;">&nbsp;&nbsp;{event_types_grouped[event.event_type_id]}</td>
            <td style="border: 1px solid black;">&nbsp;&nbsp;{event.start_date.strftime("%d/%m/%Y %H:%M")}</td>
            <td style="border: 1px solid black;">&nbsp;&nbsp;{event.end_date.strftime("%d/%m/%Y %H:%M")}</td>
        </tr>'''
    html += '</table>'
    pdf = pdfkit.from_string(html, False)
    pdf_file_path = 'generated_pdf.pdf'
    with open(pdf_file_path, 'wb') as f:
        f.write(pdf)

    return send_file(pdf_file_path, as_attachment=True)


@reports_bp.route('/grouped-monthly-events', methods=['GET'])
@validate_token()
@swag_from({
    'summary': 'Endpoint for fetching grouped monthly events as PDF file.',
    'description': 'Fetches and groups monthly events by event type, calculating total work hours.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'ID of the authenticated user'
        }
    ],
    'responses': {
        200: {
            'description': 'Grouped monthly events with total work hours PDF.',
            'content': {
                'application/pdf': {
                    'schema': {
                        'type': 'file'
                    }
                }
            }
        }
    }
})
def grouped_monthly_events(user_id):
    events = Event.query.filter(
        Event.start_date >= get_first_day_of_month(),
        Event.user_id == user_id
    ).all()

    event_type_hours = defaultdict(int)
    for event in events:
        duration = (event.end_date - event.start_date).total_seconds() / 3600
        event_type_hours[event.event_type_id] = duration

    event_types = EventType.query.all()
    event_types_grouped = {et.id: et.title for et in event_types}
    data = [(event_type_hours.get(et_id, .0), et_name) for et_id, et_name in event_types_grouped.items()]
    data.sort(key=lambda x: (-x[0], x[1]))
    html = f'''
    <h1>Grouped monthly events</h1>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid black;">
        <tr>{"".join(f'<th style="border: 1px solid black;">{item[1]}</th>' for item in data)}</tr>
        <tr>{"".join(f'<td style="border: 1px solid black;">&nbsp;&nbsp;{item[0]}</td>' for item in data)}</tr>
    </table>
    '''
    pdf = pdfkit.from_string(html, False)
    pdf_file_path = 'generated_pdf.pdf'
    with open(pdf_file_path, 'wb') as f:
        f.write(pdf)

    return send_file(pdf_file_path, as_attachment=True)
    