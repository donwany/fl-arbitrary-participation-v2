#!/bin/bash

nohup python main.py \
-data cifar \
-availability periodic \
-seeds 1,2,3,4,5 \
-lr-warmup 0.05 \
-iters-warmup 20000 \
-iters-total 3000000 \
-lr 0.000005 \
-lr-global 10.0 \
-out cifar_alg1_amplify.csv > cifar4.log