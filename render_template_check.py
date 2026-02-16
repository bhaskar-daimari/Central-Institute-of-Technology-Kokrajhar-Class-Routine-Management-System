from types import SimpleNamespace
from flask import Flask, render_template

# Create a minimal Flask app pointing to the existing templates directory
test_app = Flask(__name__, template_folder='templates', static_folder='static')

# add minimal endpoints so url_for('dashboard') and url_for('logout') work
@test_app.route('/', endpoint='dashboard')
def _dashboard():
    return ''

@test_app.route('/logout', endpoint='logout')
def _logout():
    return ''

mock_user = SimpleNamespace(
    username='test',
    role='admin',
    branch_id=1,
    branch=SimpleNamespace(name='Main Branch'),
    is_admin=lambda: True,
    is_student=lambda: False
)

with test_app.test_request_context('/'):
    try:
        out = render_template('dashboard.html', current_user=mock_user, branches=[SimpleNamespace(id=1,name='Main Branch')], years=[], classes=[], current_branch_id='', current_year_id='', current_day='')
        print('Template rendered successfully (truncated):')
        print(out[:400])
    except Exception as e:
        import traceback
        traceback.print_exc()
