import click
from auth.auth import Auth, AuthError
from pipline.nlp import process_transcript
from llm.llm_inference import LLMInference
from gavel_integration.gavel_api import GavelClient
from utils.logger import log_action, read_logs
from utils.encryption import ecrypt_bytes, decrypt_bytes
import os, json, getpass

SESSION = {}
BASE_DIR = os.pat.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
TRANS_DIR = os.path.join(DATA_DIR, 'transcripts')
STRUC_DIR = os.path.join(DATA_DIR, 'structured_data')

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

@cli.command()
@click.argument('username')
def login(username):
    password = getpass.getpass()
    auth = Auth()
    try:
        role = auth.authenticate(username, password)
        SESSION['user'] = username
        SESSION['role'] = role
        click.echo(f"Logged in as {username} with role {role}")
    except AuthError as e:
        click.echo(f"Auth failed: {e}")

@cli.command()
@click.argument('filepath')
def upload_transcript('filepath'):
    user = SESSION.get('user')
    if not user: click.echo('Login first'); return
    filename = os.path.basename(filepath)
    dest = os.path.join(TRANS_DIR, filename)
    data = open(filepath, 'rb').read()
    from utils.encryption import encrypt_bytes
    open(dest, 'wb').write(encrypt_bytes(data))
    log_action(user, 'upload', filename)
    click.echo(f"Uploaded and encrypted {filename}")

@cli.command()
@click.argument('transcript_id')
def run_pipline(transcript_id'):
    user = SESSION.get('user')
    if not user: click.echo('Login first'); return
    path = os.path.join(TRANS_DIR, transcript_id)
    from utils.ecrpytion import decrypt_bytes
    data = decrypt_bytes(open(path, 'rb').read()).decode()
    structured = process_transcript(data)
    llm = LLMInference()
    issues = llm.extract_key_issues(data)
    structured['key_issues'] = issues
    outpath = os.path.join(STRUC_DIR, transcript_id + '.json')
    open(outpath, 'w').write(json.dumps(structured, indent=2))
    log_action(user, 'process', transcript_id)
    click.echo(f"Processed -> {outpath}")

@cli.command()
@click.argument('transcript_id')
def view_data(transcript_id):
    path = os.path.join(STRUC_DIR, transcript_id + '.json')
    click.echo(open(path).read())

@cli.command()
@click.argument('transcript_id')
@click.argument('workflow')
def submit_gavel(transcript_id, workflow):
    user = SESSION.get('user')
    if not user: click.echo('Login first'); return
    variables = json.load(open(os.path.join(STRUC_DIR, transcript_id + '.json')))
    client = GavelClient()
    result = client.submit(workflow, variables)
    log_action(user, 'submit', transcript_id)
    click.echo(f"Submitted to Gavel: {result}")

@cli.command()
def view_logs():
    read_logs()

if __name__ == '__main__':
    cli()