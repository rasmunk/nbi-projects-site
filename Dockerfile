FROM nielsbohr/projects-site:latest

ARG APP_NAME=escience-projects
ARG SERVER_NAME=projects.escience.dk
ARG APP_DIR=/var/${APP_NAME}

ENV SERVERNAME=${SERVER_NAME}
ENV APP_NAME=${APP_NAME}
ENV APP_DIR=${APP_DIR}

# Setup configuration
# Also enable wsgi and header modules
COPY apache/apache2-http.conf /etc/apache2/sites-available/${SERVER_NAME}.conf
RUN a2dissite 000-default.conf && \
	a2dissite projects.conf && \
    a2ensite ${SERVER_NAME}.conf

# Prepare WSGI launcher script
COPY ./res ${APP_DIR}/res
COPY ./apache/app.wsgi ${APP_DIR}/wsgi/app.wsgi
COPY ./run.py ${APP_DIR}/run.py
RUN mkdir -p ${APP_DIR}/persistence && \
    chown root:www-data ${APP_DIR}/persistence && \
    chmod 775 -R ${APP_DIR}/persistence && \
    chmod 2755 -R ${APP_DIR}/wsgi

# Copy in the source code
COPY . /app
WORKDIR /app

# Install the envvars script, code and cleanup
RUN pip3 install setuptools && \
    pip3 install wheel==0.30.0 && \
    python3 setup.py bdist_wheel && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

RUN rm -r /app
WORKDIR $APP_DIR

EXPOSE 80
