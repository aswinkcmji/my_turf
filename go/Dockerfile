FROM golang:1.12.0-alpine3.9
WORKDIR /code
COPY . /code/
# CMD ./go
RUN apk add git
RUN  go get "github.com/jasonlvhit/gocron"
RUN  go get "github.com/lib/pq"
CMD go run updateMatchStatus.go  