## Brilliant Pebbles coverage similator

This is nothing particularly complicated. It simulates the range of a single on-orbit interceptor according to performance paramaters input by the user. That range is then used to 'tile' the globe in order to predict the number of interceptors needed for global coverage.

Most of the important material is copied straight from Alfonso Gonzalez's repo [here](https://github.com/alfonsogonzalez/AWP) accordingly credit goes to him.

The modifications added in this repo allow us to model constellation sizes for various on-orbit interceptors and various launch scenarios.

I will add more instructions later but running the following commands from the root directory should build and install the package. I'll include the .whl as a proper release later:

```
uv build
```

```
pip install ./dist/brilliant_pebbles-0.2.0-py3-none-any.whl --force-reinstall
```

From there youcan run either the BP_cloud.py or GPALS_BP_cloud.py scripts. The first models a standard interceptor. The second is one with an added solid kick stage. Missile and interceptor paramaters may be edited as global variables near the top of each script.
The final output is a dictionary which specifies the totan number of interceptors needed for global coverage.
Multiplying the interceptor total by ssbn_margin (from the same dictionary) gives the total number needed to defend against salvos from single coverage areas.

Of course that all assumes zero redundancy. 


