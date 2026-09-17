# Docker verification

Fill this in after you build and run your container (see README.md,
"Part 2 — Dockerfile"). This is how we confirm your container actually works, since an
automated grader running in a sandbox may not always have Docker-in-Docker
available.

## Build

Paste the command you ran and its final output line (the one showing the
built image ID/tag):

```
docker build -t week6-detector 

output:
=> => writing image sha256:f7bfe54a5381e6837ec4a2a967c0b42da7eb402c99f26079cbb4439c278da404  0.0s
 => => naming to docker.io/library/week6-detector
```

## Run

Paste the command you used to start the container (should map a host port
to the container's 8080):

```
docker run --rm -p 8080:8080 week6-detector
```

## Verify

Paste the exact `curl` commands and their JSON output for both endpoints,
run against the running container (not against `python src/app.py` directly
— the point is to prove the *container* works):

```
TODO: curl http://localhost:8080/health
TODO: {"status":"ok"}

TODO: curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect
TODO: [{"bbox":[127,47,27,14],"category_id":0,"id":0,"image_id":0,"score":0.98},{"bbox":[190,68,27,22],"category_id":6,"id":1,"image_id":0,"score":0.98},{"bbox":[147,98,41,21],"category_id":7,"id":2,"image_id":0,"score":0.98},{"bbox":[129,110,22,22],"category_id":8,"id":3,"image_id":0,"score":0.98}]
```
