FROM python:3-alpine

# RUN adduser -ms /bin/bash newuser
# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Tell docker that all future commands should run as the appuser user
USER appuser

WORKDIR /app
EXPOSE 8080

COPY . /app
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
CMD ["python", "-u", "app.py"]