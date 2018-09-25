FROM fedora:25

LABEL maintainer="vlussenburg@xebialabs.com"

RUN dnf -y install procps net-tools pcre pcre-static python && \
    dnf clean all 
RUN pip install --upgrade pip==10.0.1
RUN pip install flask==1.0.2
RUN mkdir /samson-stub

ENV FLASK_APP=/samson-stub/app.py
ENV FLASK_ENV=development

COPY app /samson-stub

VOLUME /samson-stub

EXPOSE 5000

CMD flask run --host=0.0.0.0