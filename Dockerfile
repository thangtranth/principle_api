FROM ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip
ADD . /app/
RUN python3 -m pip install -r /app/requirements.txt
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh