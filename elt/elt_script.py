"""
ELT Pipeline: PostgreSQL Source -> Destination
Extracts data using pg_dump and loads into destination database
"""

import subprocess
import time
import os
from logger_config import setup_logger

# Initialize structured logger
logger = setup_logger()


def wait_for_postgres(host, max_retries=5, delay=5):
    """
    Wait for PostgreSQL to become available
    
    Args:
        host: Database host identifier
        max_retries: Maximum connection attempts
        delay: Seconds between retries
    
    Returns:
        True if connection successful, False otherwise
    """
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
                logger.info(
                    'Database connection successful',
                    extra={
                        'host': host,
                        'attempt': retries + 1,
                        'max_retries': max_retries
                    }
                )
                return True
                
        except subprocess.CalledProcessError as e:
            retries += 1
            logger.warning(
                'Database not ready, retrying',
                extra={
                    'host': host,
                    'attempt': retries,
                    'max_retries': max_retries,
                    'error': str(e)
                }
            )
            time.sleep(delay)
    
    logger.error(
        'Failed to connect to database',
        extra={
            'host': host,
            'total_attempts': max_retries
        }
    )
    return False


def extract_and_load():
    """
    Main ELT function: Extract from source and load into destination
    """
    logger.info('Starting ELT pipeline')
    
    # Read configuration from environment
    source_config = {
        'host': os.environ.get('SOURCE_POSTGRES_HOST', 'source_postgres'),
        'database': os.environ.get('SOURCE_POSTGRES_DB', 'source_db'),
        'user': os.environ.get('SOURCE_POSTGRES_USER', 'postgres'),
        'password': os.environ.get('SOURCE_POSTGRES_PASSWORD', 'secret')
    }
    
    destination_config = {
        'host': os.environ.get('DESTINATION_POSTGRES_HOST', 'destination_postgres'),
        'database': os.environ.get('DESTINATION_POSTGRES_DB', 'destination_db'),
        'user': os.environ.get('DESTINATION_POSTGRES_USER', 'postgres'),
        'password': os.environ.get('DESTINATION_POSTGRES_PASSWORD', 'secret')
    }
    
    logger.info('Configuration loaded from environment', extra={
        'source_db': source_config['database'],
        'destination_db': destination_config['database']
    })
    
    # Wait for databases
    logger.info('Waiting for databases to be ready')
    
    if not wait_for_postgres(source_config['host']):
        return
    
    if not wait_for_postgres(destination_config['host']):
        return
    
    # Dump source database
    logger.info('Starting data extraction from source database')
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
        subprocess.run(dump_command, env=subprocess_env, check=True, capture_output=True)
        logger.info('Data extraction completed successfully')
    except subprocess.CalledProcessError as e:
        logger.error(
            'Data extraction failed',
            extra={'error': str(e), 'returncode': e.returncode}
        )
        return
    
    # Load into destination database
    logger.info('Starting data load into destination database')
    load_command = [
        'psql',
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['database'],
        '-a', '-f', 'data_dump.sql'
    ]
    
    subprocess_env['PGPASSWORD'] = destination_config['password']
    
    try:
        subprocess.run(load_command, env=subprocess_env, check=True, capture_output=True)
        logger.info(
            'ELT pipeline completed successfully',
            extra={
                'source': f"{source_config['host']}/{source_config['database']}",
                'destination': f"{destination_config['host']}/{destination_config['database']}"
            }
        )
    except subprocess.CalledProcessError as e:
        logger.error(
            'Data load failed',
            extra={'error': str(e), 'returncode': e.returncode}
        )
        return


if __name__ == '__main__':
    extract_and_load()