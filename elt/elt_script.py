import subprocess
import time
import os

def wait_for_postgres(host, max_retries=5, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ['pg_isready', '-h', host, '-U', os.environ.get('SOURCE_POSTGRES_USER', 'postgres')],
                check=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f'[SUCCESS] Database {host} is ready')
                return True
        except subprocess.CalledProcessError as e:
            retries += 1
            print(f'[WAITING] Database {host} not ready. Attempt {retries}/{max_retries}')
            time.sleep(delay)
    
    print(f'[ERROR] Could not connect to {host} after {max_retries} attempts')
    return False

def extract_and_load():
    print('[STEP] Starting ELT Pipeline...')
    
    # Source database config
    source_config = {
        'host': os.environ.get('SOURCE_POSTGRES_HOST', 'source_postgres'),
        'database': os.environ.get('SOURCE_POSTGRES_DB', 'source_db'),
        'user': os.environ.get('SOURCE_POSTGRES_USER', 'postgres'),
        'password': os.environ.get('SOURCE_POSTGRES_PASSWORD', 'secret')
    }
    
    # Destination database config
    destination_config = {
        'host': os.environ.get('DESTINATION_POSTGRES_HOST', 'destination_postgres'),
        'database': os.environ.get('DESTINATION_POSTGRES_DB', 'destination_db'),
        'user': os.environ.get('DESTINATION_POSTGRES_USER', 'postgres'),
        'password': os.environ.get('DESTINATION_POSTGRES_PASSWORD', 'secret')
    }
    
    print(f'[CONFIG] Source: {source_config["host"]}/{source_config["database"]}')
    print(f'[CONFIG] Destination: {destination_config["host"]}/{destination_config["database"]}')
    
    # Wait for databases
    print('[STEP] Checking database readiness...')
    if not wait_for_postgres(source_config['host']):
        return
    if not wait_for_postgres(destination_config['host']):
        return
    
    # Dump source database
    print('[STEP] Extracting data from source database...')
    dump_command = [
        'pg_dump',
        '-h', source_config['host'],
        '-U', source_config['user'],
        '-d', source_config['database'],
        '-f', 'data_dump.sql',
        '-w'
    ]
    
    subprocess_env = os.environ.copy()
    subprocess_env['PGPASSWORD'] = source_config['password']
    
    try:
        subprocess.run(dump_command, env=subprocess_env, check=True)
        print('[SUCCESS] Data extraction completed')
    except subprocess.CalledProcessError as e:
        print(f'[ERROR] Data extraction failed: {e}')
        return
    
    # Load into destination
    print('[STEP] Loading data into destination database...')
    load_command = [
        'psql',
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['database'],
        '-a', '-f', 'data_dump.sql'
    ]
    
    subprocess_env['PGPASSWORD'] = destination_config['password']
    
    try:
        subprocess.run(load_command, env=subprocess_env, check=True)
        print('[SUCCESS] ELT Pipeline completed successfully!')
    except subprocess.CalledProcessError as e:
        print(f'[ERROR] Data load failed: {e}')
        return

if __name__ == '__main__':
    extract_and_load()
