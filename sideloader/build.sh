#!/bin/bash

cd $REPO

docker build -t gem-molo .

docker tag gem-molo qa-mesos-persistence:5000/gem-molo

docker push qa-mesos-persistence:5000/gem-molo
