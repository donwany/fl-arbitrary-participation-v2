#!/bin/bash

nohup python main.py \
-data cifar \
-availability periodic \
-seeds 1,2,3,4,5 \
-lr-warmup 0.05 \
-iters-warmup 20000 \
-iters-total 3000000 \
-lr 0.05 \
-lr-global 1.0 \
-wait-all 1 \
-full-batch 0 \
-out cifar_wait_minibatch.csv > cifar1.log