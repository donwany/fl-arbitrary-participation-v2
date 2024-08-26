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
-alpha_m 0.5 \
-wait-all 1 \
-full-batch 1 \
-out /home/ts75080/Desktop/fl-arbitrary-participation/cifar_test_results/05/cifar_wait_full.csv > test_05_cifar_wait_full.log
