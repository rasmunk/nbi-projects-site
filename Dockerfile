FROM nielsbohr/projects-site:latest

ARG NBI_DIR=/var/nbi-projects-site

# Setup configuration
# Also enable wsgi and header modules
COPY apache/apache2-http.conf /etc/apache2/sites-available/nbi-projects-site.conf
RUN a2dissite 000-default.conf && \
	a2dissite projects.conf && \
    a2ensite nbi-projects-site.conf

# Prepare WSGI launcher script
COPY ./res $NBI_DIR/res
COPY ./apache/app.wsgi $NBI_DIR/wsgi/app.wsgi
COPY ./run.py $NBI_DIR/run.py
RUN mkdir -p $NBI_DIR/persistence && \
    chown root:www-data $NBI_DIR/persistence && \
    chmod 775 -R $NBI_DIR/persistence && \
    chmod 2755 -R $NBI_DIR/wsgi

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
WORKDIR $NBI_DIR

EXPOSE 80
