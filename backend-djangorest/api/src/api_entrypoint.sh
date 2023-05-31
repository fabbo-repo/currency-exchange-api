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

# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
cat << "EOF"

        ______                                                                              
       /      \                                                                             
      /$$$$$$  | __    __   ______   ______   ______   _______    _______  __    __         
      $$ |  $$/ /  |  /  | /      \ /      \ /      \ /       \  /       |/  |  /  |        
      $$ |      $$ |  $$ |/$$$$$$  /$$$$$$  /$$$$$$  |$$$$$$$  |/$$$$$$$/ $$ |  $$ |        
      $$ |   __ $$ |  $$ |$$ |  $$/$$ |  $$/$$    $$ |$$ |  $$ |$$ |      $$ |  $$ |        
      $$ \__/  |$$ \__$$ |$$ |     $$ |     $$$$$$$$/ $$ |  $$ |$$ \_____ $$ \__$$ |        
      $$    $$/ $$    $$/ $$ |     $$ |     $$       |$$ |  $$ |$$       |$$    $$ |        
       $$$$$$/   $$$$$$/  $$/      $$/       $$$$$$$/ $$/   $$/  $$$$$$$/  $$$$$$$ |        
                                                                          /  \__$$ |        
  ______                                                             __   $$    $$/         
 /      \                                                           /  |   $$$$$$/          
/$$$$$$  |  ______   _______   __     __ ______    ______   _______ $$/   ______   _______  
$$ |  $$/  /      \ /       \ /  \   /  /      \  /      \ /       |/  | /      \ /       \ 
$$ |      /$$$$$$  |$$$$$$$  |$$  \ /$$/$$$$$$  |/$$$$$$  /$$$$$$$/ $$ |/$$$$$$  |$$$$$$$  |
$$ |   __ $$ |  $$ |$$ |  $$ | $$  /$$/$$    $$ |$$ |  $$/$$      \ $$ |$$ |  $$ |$$ |  $$ |
$$ \__/  |$$ \__$$ |$$ |  $$ |  $$ $$/ $$$$$$$$/ $$ |      $$$$$$  |$$ |$$ \__$$ |$$ |  $$ |
$$    $$/ $$    $$/ $$ |  $$ |   $$$/  $$       |$$ |     /     $$/ $$ |$$    $$/ $$ |  $$ |
 $$$$$$/   $$$$$$/  $$/   $$/     $/    $$$$$$$/ $$/      $$$$$$$/  $$/  $$$$$$/  $$/   $$/ 
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

# Execute schedule jobs
python manage.py run-jobs &

if [ "$USE_HTTPS" = true ]; then
    exec gunicorn --certfile=/certs/fullchain.pem --keyfile=/certs/privkey.pem \
        --bind 0.0.0.0:443 --workers 1 --threads 4 \
        --timeout 0 $WSGI_APLICATION "$@"
else
    exec gunicorn --bind 0.0.0.0:80 --workers 1 --threads 4 \
        --timeout 0 $WSGI_APLICATION "$@"
fi