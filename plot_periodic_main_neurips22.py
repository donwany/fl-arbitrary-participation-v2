import csv
from matplotlib import pyplot as plt
import numpy as np
from difflib import SequenceMatcher
import matplotlib.ticker as ticker

import os
from cycler import cycler

#NOTE: Moving average only works for equally spaced data
#NOTE2: This code is specifically modified to this plot, so that the first common part is only plotted for the first file

moving_average_window_frac = 0.03

iterations_per_round = 5

# directory1 = '../results/fashion'

# files1 = [
#          'fashion_periodic_lr0.1_amplify1_waitall_disconnect400_all.csv',
#          'fashion_periodic_lr0.1_amplify1_waitall_fullbatch_disconnect400_all.csv',
#          'fashion_periodic_lr0.00001_amplify1_disconnect400_all.csv',
#          'fashion_periodic_lr0.00001_amplify10_disconnect400_all.csv',
#          ]

# directory2 = '../results/cifar'

# files2 = [
#          'cifar_periodic_lr0.05_amplify1_waitall_disconnect400_all.csv',
#          'cifar_periodic_lr0.05_amplify1_waitall_fullbatch_disconnect400_all.csv',
#          'cifar_periodic_lr0.00005_amplify1_disconnect400_all.csv',
#          'cifar_periodic_lr0.000005_amplify10_disconnect400_all.csv',
#          ]

directory1 = '/home/ts75080/Desktop/fl-arbitrary-participation/fashion_test_results/01'
directory2 = '/home/ts75080/Desktop/fl-arbitrary-participation/cifar_test_results/01'


files1 = ['fashion_wait_minibatch_alpha_1.csv',
          'fashion_wait_full_alpha_1.csv',
          'fashion_alg1_no_amplify_alpha_1.csv',
          'fashion_alg1_amplify_alpha_1.csv'
          ]

files2 = [
    'cifar_wait_full.csv',
    'cifar_wait_minibatch.csv',
    'cifar_alg1_amplify.csv',
    'cifar_alg1_no_amplify.csv',
]


legends1 = [r'wait-minibatch', r'wait-full', r'Alg. 1 without amplification', r'Alg. 1 with amplification']
legends2 = [r'wait-minibatch', r'wait-full', r'Alg. 1 without amplification', r'Alg. 1 with amplification']

xlim_loss1 = [0, 300000]
ylim_loss1 = [0.0006, 0.0012]
xlim_acc1 = [0, 300000]
ylim_acc1 = [0.86, 0.905]
xlim_loss2 = [0, 600000]
ylim_loss2 = [0.0015, 0.0032]
xlim_acc2 = [0, 600000]
ylim_acc2 = [0.68,0.775]


fig = plt.figure(1)
ax1 = fig.add_axes((0.05,0.15,0.17,0.65))
ax2 = fig.add_axes((0.30,0.15,0.17,0.65))
ax3 = fig.add_axes((0.55,0.15,0.17,0.65))
ax4 = fig.add_axes((0.80,0.15,0.17,0.65))


def moving_average(dict, wind, all_as_separate_entries=True):
    new_dict = {}
    keys = list(dict.keys())

    for i in range(0, len(keys) - wind):
        # last = min(i + wind, len(keys))
        last = i + wind
        dim = len(dict[keys[i]])

        new_entry = []

        for d in range(0, dim):
            tmp = 0
            is_break = False
            for j in range(i, last):
                if len(dict[keys[j]]) <= d:
                    is_break = True
                    break
                else:
                    if not all_as_separate_entries:
                        tmp += dict[keys[j]][d]
                    else:
                        new_entry.append(dict[keys[j]][d])

            if is_break:
                break

            if not all_as_separate_entries:
                tmp /= last - i
                new_entry.append(tmp)

        new_dict[keys[i]] = new_entry

    return new_dict


for f_index in range(len(files1)):
    filename = files1[f_index]

    full_path = os.path.join(directory1, filename)

    entries_loss = {}
    entries_accuracy = {}


    with open(full_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue

            # print(row)

            iter = int(row[1])
            if iter not in entries_loss:
                entries_loss[iter] = []
                entries_accuracy[iter] = []

            entries_loss[iter].append(float(row[2]))
            entries_accuracy[iter].append(float(row[4]))

    total = len(entries_loss.keys())
    print('total', total)
    if xlim_loss1 is not None:
        total = min(float(total), xlim_loss1[1] * iterations_per_round / 250)
    moving_average_window = int(moving_average_window_frac * total)
    print('moving_average_window =', moving_average_window)

    if moving_average_window > 1:
        entries_loss = moving_average(entries_loss, moving_average_window)
        entries_accuracy = moving_average(entries_accuracy, moving_average_window)

    keys_list = list(entries_loss.keys())
    amp_factor = float(keys_list[-1] + moving_average_window * (keys_list[-1] - keys_list[-2])) / float(keys_list[-1])
    #Stretch x-axis for moving average window
    rounds = np.array(keys_list, dtype=float) * amp_factor / float(iterations_per_round)

    entries_loss_mean = []
    entries_loss_std = []
    entries_loss_span = []
    entries_accuracy_mean = []
    entries_accuracy_std = []
    entries_accuracy_span = []

    for val in entries_loss.values():
        entries_loss_mean.append(np.mean(val))
        entries_loss_std.append(np.std(val))
        entries_loss_span.append(np.max(val) - np.min(val))

    for val in entries_accuracy.values():
        entries_accuracy_mean.append(np.mean(val))
        entries_accuracy_std.append(np.std(val))
        entries_accuracy_span.append(np.max(val) - np.min(val))

    entries_loss_mean = np.array(entries_loss_mean)
    entries_loss_std = np.array(entries_loss_std)
    entries_loss_span = np.array(entries_loss_span)
    entries_accuracy_mean = np.array(entries_accuracy_mean)
    entries_accuracy_std = np.array(entries_accuracy_std)
    entries_accuracy_span = np.array(entries_accuracy_span)

    start_index = 0

    ax1.plot(rounds[start_index:], entries_loss_mean[start_index:], label=legends1[f_index])
    ax1.fill_between(rounds[start_index:],
                     entries_loss_mean[start_index:] - entries_loss_std[start_index:],
                     entries_loss_mean[start_index:] + entries_loss_std[start_index:],
                     alpha = 0.1)

    ax2.plot(rounds[start_index:], entries_accuracy_mean[start_index:], label=legends1[f_index])
    ax2.fill_between(rounds[start_index:],
                     entries_accuracy_mean[start_index:] - entries_accuracy_std[start_index:],
                     entries_accuracy_mean[start_index:] + entries_accuracy_std[start_index:],
                     alpha=0.1)

    print(filename, np.mean(entries_loss_mean), np.std(entries_loss_mean), entries_loss_mean[-1], entries_loss_std[-1], entries_loss_span[-1],
          np.mean(entries_accuracy_mean), np.std(entries_accuracy_mean), entries_accuracy_mean[-1], entries_accuracy_std[-1], entries_accuracy_span[-1])


for f_index in range(len(files2)):
    filename = files2[f_index]

    full_path = os.path.join(directory2, filename)

    entries_loss = {}
    entries_accuracy = {}


    with open(full_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue

            # print(row)

            iter = int(row[1])
            if iter not in entries_loss:
                entries_loss[iter] = []
                entries_accuracy[iter] = []

            entries_loss[iter].append(float(row[2]))
            entries_accuracy[iter].append(float(row[4]))

    total = len(entries_loss.keys())
    print('total', total)
    if xlim_loss2 is not None:
        total = min(float(total), xlim_loss2[1] * iterations_per_round / 250)
    moving_average_window = int(moving_average_window_frac * total)
    print('moving_average_window =', moving_average_window)

    if moving_average_window > 1:
        entries_loss = moving_average(entries_loss, moving_average_window)
        entries_accuracy = moving_average(entries_accuracy, moving_average_window)

    keys_list = list(entries_loss.keys())
    amp_factor = float(keys_list[-1] + moving_average_window * (keys_list[-1] - keys_list[-2])) / float(keys_list[-1])
    #Stretch x-axis for moving average window
    rounds = np.array(keys_list, dtype=float) * amp_factor / float(iterations_per_round)

    entries_loss_mean = []
    entries_loss_std = []
    entries_loss_span = []
    entries_accuracy_mean = []
    entries_accuracy_std = []
    entries_accuracy_span = []

    for val in entries_loss.values():
        entries_loss_mean.append(np.mean(val))
        entries_loss_std.append(np.std(val))
        entries_loss_span.append(np.max(val) - np.min(val))

    for val in entries_accuracy.values():
        entries_accuracy_mean.append(np.mean(val))
        entries_accuracy_std.append(np.std(val))
        entries_accuracy_span.append(np.max(val) - np.min(val))

    entries_loss_mean = np.array(entries_loss_mean)
    entries_loss_std = np.array(entries_loss_std)
    entries_loss_span = np.array(entries_loss_span)
    entries_accuracy_mean = np.array(entries_accuracy_mean)
    entries_accuracy_std = np.array(entries_accuracy_std)
    entries_accuracy_span = np.array(entries_accuracy_span)

    start_index = 0

    ax3.plot(rounds[start_index:], entries_loss_mean[start_index:], label=legends2[f_index])
    ax3.fill_between(rounds[start_index:],
                     entries_loss_mean[start_index:] - entries_loss_std[start_index:],
                     entries_loss_mean[start_index:] + entries_loss_std[start_index:],
                     alpha = 0.1)

    ax4.plot(rounds[start_index:], entries_accuracy_mean[start_index:], label=legends2[f_index])
    ax4.fill_between(rounds[start_index:],
                     entries_accuracy_mean[start_index:] - entries_accuracy_std[start_index:],
                     entries_accuracy_mean[start_index:] + entries_accuracy_std[start_index:],
                     alpha=0.1)

    print(filename, np.mean(entries_loss_mean), np.std(entries_loss_mean), entries_loss_mean[-1], entries_loss_std[-1], entries_loss_span[-1],
          np.mean(entries_accuracy_mean), np.std(entries_accuracy_mean), entries_accuracy_mean[-1], entries_accuracy_std[-1], entries_accuracy_span[-1])


if xlim_loss1 is not None:
    ax1.set_xlim(xlim_loss1)
if ylim_loss1 is not None:
    ax1.set_ylim(ylim_loss1)
if xlim_acc1 is not None:
    ax2.set_xlim(xlim_acc1)
if ylim_acc1 is not None:
    ax2.set_ylim(ylim_acc1)
if xlim_loss2 is not None:
    ax3.set_xlim(xlim_loss2)
if ylim_loss2 is not None:
    ax3.set_ylim(ylim_loss2)
if xlim_acc2 is not None:
    ax4.set_xlim(xlim_acc2)
if ylim_acc2 is not None:
    ax4.set_ylim(ylim_acc2)

ax1.set_xlabel('Training rounds')
ax1.set_ylabel('Global training loss')
ax1.set_title('FashionMNIST', loc='right')
ax1.yaxis.set_major_locator(ticker.MaxNLocator(6))
ax1.ticklabel_format(axis='y', scilimits=[-3, 3], useMathText=True)
ax1.set_xticks([0, 150000, 300000])

ax1.legend(bbox_to_anchor=(0.5, 1.33), loc='upper left', ncol=4)

ax2.set_xlabel('Training rounds')
ax2.set_ylabel('Test accuracy')
ax2.set_title('FashionMNIST', loc='right')
ax2.set_xticks([0, 150000, 300000])

ax3.set_xlabel('Training rounds')
ax3.set_ylabel('Global training loss')
ax3.set_title('CIFAR-10', loc='right')
ax3.yaxis.set_major_locator(ticker.MaxNLocator(4))
ax3.ticklabel_format(axis='y', scilimits=[-3, 3], useMathText=True)
ax3.set_xticks([0, 300000, 600000])

ax4.set_xlabel('Training rounds')
ax4.set_ylabel('Test accuracy')
ax4.set_title('CIFAR-10', loc='right')
ax4.set_xticks([0, 300000, 600000])

plt.figure(1)
fig = plt.gcf()
fig.set_size_inches(11.0, 3.0)
fig.savefig('results.png', dpi=200)

plt.show()

