# build
FROM node:10.16-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build


# production
FROM registry.access.redhat.com/ubi8/ubi as production
WORKDIR /app
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/requirements.txt ./
COPY ./setup.sh ./

RUN yum install -y gnupg curl python3-devel python3-pip nginx && \
    yum clean all

RUN pip3 install -r requirements.txt && \
    pip3 install gunicorn

COPY --from=build-vue /app/dist /usr/share/nginx/html
RUN ./setup.sh --container
COPY ./server .
CMD gunicorn -b 127.0.0.1:5000 app:app --daemon --log-file logfile && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'
