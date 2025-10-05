import subprocess
import time
<<<<<<< HEAD
import psycopg2


def wait_for_postgres(host, user="postgres", max_retries=10, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    for attempt in range(1, max_retries + 1):
        try:
            # Check if Postgres is responding
            result = subprocess.run(
                ["pg_isready", "-h", host, "-U", user],
                check=True,
                capture_output=True,
                text=True,
            )
            if "accepting connections" in result.stdout:
                print(f"[INFO] {host} is ready to accept connections.")
                # Test an actual connection with psycopg2
                conn = psycopg2.connect(
                    dbname="postgres", user=user, password="secret", host=host
                )
                conn.close()
                return True
        except Exception as e:
            print(f"[WARN] {host} not ready yet ({e}). Retry {attempt}/{max_retries}...")
            time.sleep(delay_seconds)
    print(f"[ERROR] {host} did not become ready after {max_retries} retries.")
    return False


def run_subprocess(command, env=None, description=""):
    """Helper to run subprocess commands safely."""
    print(f"[RUN] {description}: {' '.join(command)}")
    result = subprocess.run(command, env=env, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {description}")
    print(f"[OK] {description} completed successfully.")


# --- MAIN LOGIC ---
if __name__ == "__main__":
    print("[STEP] Checking database readiness...")

    if not wait_for_postgres("source_postgres"):
        exit(1)
    if not wait_for_postgres("destination_postgres"):
        exit(1)

    print("[STEP] Starting ELT script...")

    source_config = {
        'dbname': 'source_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'source_postgres'
    }

    destination_config = {
        'dbname': 'destination_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'destination_postgres'
    }

    # --- Extract (dump) ---
    dump_command = [
        "pg_dump",
        "-h", source_config['host'],
        "-U", source_config['user'],
        "-d", source_config['dbname'],
        "-f", "data_dump.sql",
        "-w"
    ]
    run_subprocess(dump_command,
                   env={"PGPASSWORD": source_config['password']},
                   description="Dumping source database")

    # --- Load (restore) ---
    load_command = [
        "psql",
        "-h", destination_config['host'],
        "-U", destination_config['user'],
        "-d", destination_config['dbname'],
        "-a", "-f", "data_dump.sql"
    ]
    run_subprocess(load_command,
                   env={"PGPASSWORD": destination_config['password']},
                   description="Loading data into destination")

    print("[DONE] ELT process completed successfully.")
=======


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False


# Use the function before running the ELT process
if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("Starting ELT script...")

# Configuration for the source PostgreSQL database
source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'source_postgres'
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'destination_postgres'
}

# Use pg_dump to dump the source database to a SQL file
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'  # Do not prompt for password
]

# Set the PGPASSWORD environment variable to avoid password prompt
subprocess_env = dict(PGPASSWORD=source_config['password'])

# Execute the dump command
subprocess.run(dump_command, env=subprocess_env, check=True)

# Use psql to load the dumped SQL file into the destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql'
]

# Set the PGPASSWORD environment variable for the destination database
subprocess_env = dict(PGPASSWORD=destination_config['password'])

# Execute the load command
subprocess.run(load_command, env=subprocess_env, check=True)

print("Ending ELT script...")
>>>>>>> 9fc2d7dfc722989374bfb8a4d64cca8bbaf112b7
