FROM golang:1.12.0-alpine3.9
WORKDIR /code
COPY . /code/
# CMD ./go
RUN apk add --no-cache git --repository https://alpine.global.ssl.fastly.net/alpine/v3.13/community --repository https://alpine.global.ssl.fastly.net/alpine/v3.13/main
RUN  go get "github.com/jasonlvhit/gocron"
RUN  go get "github.com/lib/pq"
CMD go run updateMatchStatus.go  