#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np

class Simularor():

    def execute(self, iteration, threshold, n):

        real_data = np.empty([int(self.match), 2])
        i_day = 0
        for setsu in xrange(int(self.match)):
            i_day += self.data[setsu,1]
            real_data[setsu,0] = i_day+1
            real_data[setsu,1] = self.data[setsu,2]

        output = np.empty([int(self.match), 2])
        hoge = np.empty(int(self.match))

        hist = np.empty(iteration)
        count = 0
        flag = False
        for x in xrange(iteration):
            sample = []
            i_sum = 0
            lose_counter = 0
            for setsu in xrange(int(self.match)):
                sample = real_data
                sample = sample[sample[:,0] < sample[setsu,0] + threshold]
                sample = sample[sample[:,0] > sample[setsu,0] - threshold]
                point = sample[np.random.choice(len(sample)),1]
                i_sum += point
                hoge[setsu] = point
                if point == 0:
                    lose_counter += 1
                    if lose_counter >= n:
                        count += 1
                        lose_counter = 0
                        flag = True
                else:
                    lose_counter = 0
            hist[x] = i_sum

            if flag:
                i_sum = 0
                for setsu in xrange(int(self.match)):
                    i_sum += hoge[setsu]
                    output[setsu,0] = setsu+1
                    output[setsu,1] = i_sum
                flag = False
        
        print("MAX勝ち点: %d"%(max(hist)))
        print("MIN勝ち点: %d"%(min(hist)))
        print("%d連敗: %d"%(n,count))

        return hist, output

    def readFile(self):
        
        if not os.path.exists(self.input_file):
            return False

        with open(self.input_file) as f:
            data = [s.strip().split(',') for s in f.readlines()]
        data = np.array(data)[:,0:4]
        data = np.delete(data, 2, 1)
        self.data = np.array([[float(x) for x in y] for y in data])

        self.match = len(self.data)
        self.season = sum(self.data[:,1])+1

        print("試合数: %d"%self.match)
        print("日にち: %d"%self.season)

        return True
    
    def __init__(self, input_file, output_file):
        
        self.input_file = input_file
        self.output_file = output_file

        self.data = []
        self.match = 0
        self.season = 0
