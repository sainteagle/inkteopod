from fabric import Connection, task

@task
def deploy(ctx):
    # VPS bağlantısı
    conn = Connection(
        host='194.113.64.207',
        user='root',
        connect_kwargs={'password': 'Heysem3506!Inkteo'}
    )
    
    # Proje dizini
    project_dir = '/var/www/inkteoPOD'
    
    with conn.cd(project_dir):
        # Git repo güncellemesi (eğer git kullanıyorsanız)
        # conn.run('git pull')
        
        # Dosyaları kopyala
        conn.put('./*', project_dir)
        
        # Virtual environment ve bağımlılıklar
        conn.run('python3 -m venv venv')
        conn.run('source venv/bin/activate && pip install -r requirements.txt')
        
        # Django komutları
        conn.run('source venv/bin/activate && python manage.py migrate')
        conn.run('source venv/bin/activate && python manage.py collectstatic --noinput')
        
        # Servisleri yeniden başlat
        conn.run('systemctl restart gunicorn')
        conn.run('systemctl restart nginx')
