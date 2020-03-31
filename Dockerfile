# Build client side static files
FROM node:10.16-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build

# Build server container with reverse proxy
FROM registry.access.redhat.com/ubi8/ubi as build-golang
WORKDIR /app
RUN yum install -y golang && \
    mkdir -p $HOME/go && \
    echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc && \
    source $HOME/.bashrc
RUN yum install -y gnupg curl && \
    yum clean all
COPY ./setup.sh ./
COPY ./server .
RUN ./setup.sh --container && go build ./main.go

# Use alpine image to save space
FROM nginx:alpine as production
WORKDIR /app
# https://stackoverflow.com/a/50861580/8584691
RUN apk add --no-cache libc6-compat
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY --from=build-golang /app .

CMD nginx && ./main
