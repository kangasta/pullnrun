# Examples

## Instructions from file

See example [fizzbuzz.json](./fizzbuzz.json) and execute the instructions with:

```bash
pullnrun -f examples/fizzbuzz.json
```

## Instructions to container via env variable

See example [Dockerfile](./Dockerfile) and [timetbl.json](./timetbl.json) and build and run the container with:

```bash
docker build . -t pullnrun
docker run -e "PULLNRUN=$(cat timetbl.json)" pullnrun
```
