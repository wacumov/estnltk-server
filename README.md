# estnltk-server
A simple wrapper for [estnltk](https://github.com/estnltk/estnltk).

### How to run
```bash
echo 'ADDRESS=0.0.0.0\nPORT=XXXX' > ./.env
docker build -t estnltk-server .
docker run -d -p XXXX:XXXX --env-file ./.env estnltk-server
```