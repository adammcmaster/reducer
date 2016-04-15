# reducer

Very much a work in progress.

Python module for reducing FITS images, aiming to abstract away basically
all the complicated parts of the process.

For development this is wrapped in a script that naively tries to reduce
everything in `/data/`.

Example usage that works on all FITS files in the current directory:

```
docker run -it --rm -v $PWD:/data/ astopy/reducer
```
