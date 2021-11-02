FROM python:3-alpine

# To download resources from external sites, we also need to set up proxy
ENV HTTP_PROXY=${HTTP_PROXY:-http://nl-userproxy-access.net.abnamro.com:8080} \
    HTTPS_PROXY=${HTTPS_PROXY:-http://nl-userproxy-access.net.abnamro.com:8080} \
    http_proxy=${HTTP_PROXY:-http://nl-userproxy-access.net.abnamro.com:8080} \
    https_proxy=${HTTPS_PROXY:-http://nl-userproxy-access.net.abnamro.com:8080} \
    NO_PROXY=${NO_PROXY:-127.0.0.1,localhost,nl.eu.abnamro.com} \
    no_proxy=${NO_PROXY:-127.0.0.1,localhost,nl.eu.abnamro.com,}


# RUN adduser -ms /bin/bash newuser
# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Tell docker that all future commands should run as the appuser user
USER appuser

WORKDIR /app
EXPOSE 5001

COPY . /app
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
CMD ["app.py"]

ENTRYPOINT ["python"]
