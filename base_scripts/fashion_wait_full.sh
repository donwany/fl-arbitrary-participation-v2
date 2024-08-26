#!/bin/bash

nohup python main.py \
-data fashion \
-availability periodic \
-seeds 1,2,3,4,5,6,7,8,9,10 \
-lr-warmup 0.1 \
-iters-warmup 10000 \
-iters-total 1500000 \
-lr 0.1 \
-lr-global 1.0 \
-wait-all 1 \
-full-batch 1 \
-out fashion_wait_full.csv > fashion2.log