# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"
cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

# PostgreSQL setup
package "postgresql-server-dev-all"
package "libpython-dev"
package "python3-pip"
execute 'pip_psycopg2' do
  command 'pip3 install Psycopg2'
end

package "postgresql"
execute 'postgresql_create' do
  command 'echo "CREATE DATABASE store16db; CREATE USER vagrant; GRANT ALL PRIVILEGES ON DATABASE store16db TO vagrant;" | sudo -u postgres psql'
end

# Install Pillow
execute 'install_pillow' do
  command 'pip3 install Pillow'
end

# Django setup
execute 'pip_django' do
  command 'pip3 install django'
end

#Install Crispy Forms
execute 'django-crispy-forms' do
  command 'pip3 install django-crispy-forms'
end

execute 'django_migrate' do
  user 'vagrant'
  cwd '/home/vagrant/project/store16'
  command 'python3 manage.py migrate'
end
 execute 'django_makemigrations' do
   user 'vagrant'
   cwd '/home/vagrant/project/store16'
   command 'python3 manage.py makemigrations store'
 end
 execute 'django_migrate' do
   user 'vagrant'
   cwd '/home/vagrant/project/store16'
   command 'python3 manage.py migrate'
 end
execute 'django_loaddata' do
  user 'vagrant'
  cwd '/home/vagrant/project/store16'
  command 'python3 manage.py loaddata initial_data.json'
end

execute 'static_permission' do
  command 'chmod 0755 /home/vagrant/project/static'
end
execute 'django_import_static' do
  user 'vagrant'
  cwd '/home/vagrant/project/store16'
  command 'python3 manage.py collectstatic --noinput'
end

# Nginx setup
package "nginx"
cookbook_file "nginx-default" do
  path "/etc/nginx/sites-available/default"
end
execute 'nginx_restart' do
  command 'nginx -s reload'
end

# uWSGI setup
execute 'pip_uwsgi' do
  command 'pip3 install uwsgi'
end
cookbook_file "rc.local" do
  path "/etc/rc.local"
end
execute 'rc_permission' do
  command 'chmod 0755 /etc/rc.local'
end
execute 'startup' do
  command "/etc/rc.local"
end
