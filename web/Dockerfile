FROM node as npm-builder

COPY . /static/

RUN cd /static && npm i && npm run build

FROM nginx

COPY --from=npm-builder /static/robots.txt /usr/share/nginx/html/robots.txt
COPY --from=npm-builder /static/dist/ /usr/share/nginx/html/static/dist/
COPY --from=npm-builder /static/authentik/ /usr/share/nginx/html/static/authentik/
COPY ./nginx.conf /etc/nginx/nginx.conf
