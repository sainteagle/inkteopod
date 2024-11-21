import os
import subprocess
from fabric import Connection
from django.conf import settings
import datetime

def deploy_to_vps(deployment_id):
    from .models import Deployment
    
    deployment = Deployment.objects.get(id=deployment_id)
    deployment.status = 'in_progress'
    deployment.save()

    try:
        # VPS bağlantı bilgileri
        conn = Connection(
            host='194.113.64.207',
            user='root',
            connect_kwargs={'password': 'Heysem3506!Inkteo'}
        )

        # Veritabanı yedeği al
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        local_backup = f'backup_{timestamp}.sql'
        
        # Local veritabanı yedeği
        subprocess.run([
            'pg_dump',
            '-h', 'localhost',
            '-U', settings.DATABASES['default']['USER'],
            '-d', settings.DATABASES['default']['NAME'],
            '-f', local_backup
        ])

        # Dosyaları VPS'e kopyala
        project_files = [
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
            local_backup,
        ]

        for file in project_files:
            if os.path.exists(file):
                conn.put(file, f'/var/www/inkteoPOD/{file}')

        # VPS'de komutları çalıştır
        with conn.cd('/var/www/inkteoPOD'):
            # Virtual environment güncelle
            conn.run('source venv/bin/activate && pip install -r requirements.txt')
            
            # Veritabanını güncelle
            conn.run(f'psql -U inkteouser -d inkteodb -f {local_backup}')
            
            # Django komutlarını çalıştır
            conn.run('source venv/bin/activate && python manage.py migrate')
            conn.run('source venv/bin/activate && python manage.py collectstatic --noinput')
            
            # Servisleri yeniden başlat
            conn.run('systemctl restart gunicorn')
            conn.run('systemctl restart nginx')

        # Yerel yedek dosyasını sil
        os.remove(local_backup)

        deployment.status = 'completed'
        deployment.log = 'Deployment completed successfully'
        deployment.save()

    except Exception as e:
        deployment.status = 'failed'
        deployment.log = f'Error during deployment: {str(e)}'
        deployment.save()
