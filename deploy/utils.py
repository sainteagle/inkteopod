import os
import subprocess
from datetime import datetime
from fabric import Connection
from django.conf import settings
import shutil

def create_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Database backup
    db_backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sql')
    subprocess.run([
        'pg_dump',
        '-h', settings.DATABASES['default']['HOST'],
        '-U', settings.DATABASES['default']['USER'],
        '-d', settings.DATABASES['default']['NAME'],
        '-f', db_backup_file
    ])
    
    # Files backup
    files_backup = os.path.join(backup_dir, f'files_backup_{timestamp}.tar.gz')
    shutil.make_archive(
        files_backup[:-7],  # remove .tar.gz
        'gztar',
        settings.BASE_DIR,
        base_dir='.'
    )
    
    return f'backups/files_backup_{timestamp}.tar.gz'

def deploy_to_vps(deployment):
    try:
        deployment.status = 'in_progress'
        deployment.save()

        # VPS bağlantısı
        conn = Connection(
            host='194.113.64.207',
            user='root',
            connect_kwargs={'password': 'Heysem3506!Inkteo'}
        )

        # Proje dizini
        remote_dir = '/var/www/inkteoPOD'

        with conn.cd(remote_dir):
            # Backup dosyasını VPS'e kopyala
            conn.put(
                os.path.join(settings.MEDIA_ROOT, deployment.backup_file.name),
                f'{remote_dir}/backups/'
            )
            
            # Proje dosyalarını kopyala
            local_files = [
                'manage.py',
                'requirements.txt',
                '.env',
                'core/',
                'accounts/',
                'products/',
                'orders/',
                'deploy/',
                'templates/',
                'static/',
            ]
            
            for file in local_files:
                if os.path.exists(file):
                    conn.put(file, f'{remote_dir}/{file}')

            # Virtual environment güncelle
            conn.run('source venv/bin/activate && pip install -r requirements.txt')
            
            # Migrations ve static dosyaları
            conn.run('source venv/bin/activate && python manage.py migrate')
            conn.run('source venv/bin/activate && python manage.py collectstatic --noinput')
            
            # Servisleri yeniden başlat
            conn.run('systemctl restart gunicorn')
            conn.run('systemctl restart nginx')

        deployment.status = 'completed'
        deployment.log = 'Deployment completed successfully'
        deployment.save()

    except Exception as e:
        deployment.status = 'failed'
        deployment.log = str(e)
        deployment.save()
        raise
