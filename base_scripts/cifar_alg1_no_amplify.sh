#!/bin/bash

nohup python main.py \
-data cifar \
-availability periodic \
-seeds 1,2,3,4,5 \
-lr-warmup 0.05 \
-iters-warmup 20000 \
-iters-total 3000000 \
-lr 0.00005 \
-lr-global 1.0 \
-out cifar_alg1_no_amplify.csv > cifar3.log