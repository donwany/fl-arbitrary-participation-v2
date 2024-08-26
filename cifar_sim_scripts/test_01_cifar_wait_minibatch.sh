#!/bin/bash

nohup python /home/ts75080/Desktop/fl-arbitrary-participation/main.py \
-data cifar \
-availability periodic \
-seeds 1,2,3,4,5 \
-lr-warmup 0.05 \
-iters-warmup 20000 \
-iters-total 3000000 \
-lr 0.05 \
-lr-global 1.0 \
-alpha_m 0.1 \
-wait-all 1 \
-full-batch 0 \
-out /home/ts75080/Desktop/fl-arbitrary-participation/cifar_test_results/01/cifar_wait_minibatch.csv > test_01_cifar_wait_minibatch.log