#!/bin/bash  
echo Starting Gunicorn. 
exec gunicorn ipl.wsgi:application \ 
    --bind 0.0.0.0:8080 \ 
    --workers 3