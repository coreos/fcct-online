# build client side static files
FROM node:10.16-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build


# build server container with reverse proxy
FROM registry.access.redhat.com/ubi8/ubi as production
WORKDIR /app

RUN yum install -y golang && \
    mkdir -p $HOME/go && \
    echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc && \
    source $HOME/.bashrc

RUN yum install -y gnupg curl nginx && \
    yum clean all

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./setup.sh ./
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./server .

RUN ./setup.sh --container && go build ./main.go

CMD nginx && ./main
