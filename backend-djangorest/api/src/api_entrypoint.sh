#!/bin/sh

# Exit immediately if any of the following command exits 
# with a non-zero status
set -e

# Postgres checking
until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 10
done
>&2 echo "Postgres is up - continuing"

# Create log directory
touch /var/log/api/app.log
chmod 777 /var/log/api/app.log

# Check migrations
echo "Checking migrations"
python manage.py migrate --check || python manage.py migrate --no-input || exit 0

# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
cat << "EOF"

  ______                                                                        
 /      \                                                                       
/$$$$$$  | __    __   ______    ______    ______   _______    _______  __    __ 
$$ |  $$/ /  |  /  | /      \  /      \  /      \ /       \  /       |/  |  /  |
$$ |      $$ |  $$ |/$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$$  |/$$$$$$$/ $$ |  $$ |
$$ |   __ $$ |  $$ |$$ |  $$/ $$ |  $$/ $$    $$ |$$ |  $$ |$$ |      $$ |  $$ |
$$ \__/  |$$ \__$$ |$$ |      $$ |      $$$$$$$$/ $$ |  $$ |$$ \_____ $$ \__$$ |
$$    $$/ $$    $$/ $$ |      $$ |      $$       |$$ |  $$ |$$       |$$    $$ |
 $$$$$$/   $$$$$$/  $$/       $$/        $$$$$$$/ $$/   $$/  $$$$$$$/  $$$$$$$ |
                                                                      /  \__$$ |
                                                                      $$    $$/ 
                                                                       $$$$$$/  
 ________                      __                                               
/        |                    /  |                                              
$$$$$$$$/  __    __   _______ $$ |____    ______   _______    ______    ______  
$$ |__    /  \  /  | /       |$$      \  /      \ /       \  /      \  /      \ 
$$    |   $$  \/$$/ /$$$$$$$/ $$$$$$$  | $$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |
$$$$$/     $$  $$<  $$ |      $$ |  $$ | /    $$ |$$ |  $$ |$$ |  $$ |$$    $$ |
$$ |_____  /$$$$  \ $$ \_____ $$ |  $$ |/$$$$$$$ |$$ |  $$ |$$ \__$$ |$$$$$$$$/ 
$$       |/$$/ $$  |$$       |$$ |  $$ |$$    $$ |$$ |  $$ |$$    $$ |$$       |
$$$$$$$$/ $$/   $$/  $$$$$$$/ $$/   $$/  $$$$$$$/ $$/   $$/  $$$$$$$ | $$$$$$$/ 
                                                            /  \__$$ |          
                                                            $$    $$/           
                                                             $$$$$$/            
                          ______   _______   ______                             
                         /      \ /       \ /      |                            
                        /$$$$$$  |$$$$$$$  |$$$$$$/                             
                        $$ |__$$ |$$ |__$$ |  $$ |                              
                        $$    $$ |$$    $$/   $$ |                              
                        $$$$$$$$ |$$$$$$$/    $$ |                              
                        $$ |  $$ |$$ |       _$$ |_                             
                        $$ |  $$ |$$ |      / $$   |                            
                        $$/   $$/ $$/       $$$$$$/                             
                                                                

EOF

APP_USER_UID=`id -u $APP_USER`
exec gunicorn --certfile=/certs/fullchain.pem --keyfile=/certs/privkey.pem --bind 0.0.0.0:443 --user $APP_USER_UID \
    --workers 1 --threads 4 --timeout 0 $WSGI_APLICATION "$@"