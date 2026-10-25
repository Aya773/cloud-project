#!/bin/bash
OUT=results.csv
echo "setup,run,startup_ms,rss_kb,req_per_sec" > $OUT

wait_ready() {
  until curl -s -o /dev/null --max-time 1 localhost:$1; do sleep 0.01; done
}
ms() { awk -v s=$1 -v e=$2 'BEGIN{printf "%.0f",(e-s)*1000}'; }
rps() { ab -n 20000 -c 10 -q http://localhost:$1/ 2>/dev/null | awk '/Requests per second/{print $4}'; }

for run in 1 2 3; do
  # ---- app running directly on the VM ----
  s=$(date +%s.%N)
  python3 app.py &
  PID=$!
  wait_ready 8000
  e=$(date +%s.%N)
  sleep 2
  rss=$(ps -o rss= -p $PID | tr -d ' ')
  echo "vm,$run,$(ms $s $e),$rss,$(rps 8000)" >> $OUT
  kill $PID; wait $PID 2>/dev/null
  sleep 2

  # ---- app in a container (inside the same VM) ----
  s=$(date +%s.%N)
  docker run -d --name hello -p 8001:8000 hello-app > /dev/null
  wait_ready 8001
  e=$(date +%s.%N)
  sleep 2
  CPID=$(docker inspect -f '{{.State.Pid}}' hello)
  rss=$(ps -o rss= -p $CPID | tr -d ' ')
  echo "container,$run,$(ms $s $e),$rss,$(rps 8001)" >> $OUT
  docker rm -f hello > /dev/null
  sleep 2
done
cat $OUT
