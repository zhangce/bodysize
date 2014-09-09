#! /bin/bash

. "$(dirname $0)/env.sh"

cd $DEEPDIVE_HOME
./sbt/sbt "run -c $APP_HOME/application.conf"
