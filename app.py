from project import app
# from project.model import Documents

if __name__ == '__main__':
    app.run(debug=True)

"""
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Documents':Documents}
"""