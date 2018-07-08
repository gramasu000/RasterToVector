""" FILE: FloorplanTransformation/code/predict.lua """

""" {{{ Imports """
""" LUA """
# require 'nn'
# require 'cudnn'
# require 'cunn'
# image = require 'image'
# package.path = '../util/lua/?.lua;' .. package.path
# local fp_ut = require 'floorplan_utils'
# pl = require 'pl.import_into' ()
# pl.dir.makepath('test/')

""" PYTHON """
import numpy
import torch
from torch import nn
import torchvision
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt
import floorplan_utils as fp_ut
""" }}} """

""" {{{ Command Line Options Parsing """
""" LUA """
# local opts = require 'opts'
# local opt = opts.parse(arg)
# opts.init(opt)

""" PYTHON """
import argparse
opts = argparse.ArgumentParser(description="Script to run a prediction on floorplan image.")
opts.add_argument("-loadModel", help="model path", default="model.h5")
opts.add_argument("-floorplanFilename", help="path to the floorplan image", default="floorplan.jpg")
opts.add_argument("-outputFilename", help="output filename", default="output.txt")
opt = opts.parse_args()
sampleDim = # FILL THIS IN LATER
""" }}} """

""" {{{ Adding non-parametric layers to pretrained Convnet Model """
""" LUA """
# local modelHeatmap = torch.load(opt.loadModel)
# local heatmapBranch = nn.Sequential():add(nn.MulConstant(0.1))
# local segmentationBranch_1 = nn.Sequential():add(nn.SoftMax()):add(nn.View(-1, opt.sampleDim, opt.sampleDim, 13)):add(nn.Transpose({3, 4}, {2, 3}))
# local segmentationBranch_2 = nn.Sequential():add(nn.SoftMax()):add(nn.View(-1, opt.sampleDim, opt.sampleDim, 17)):add(nn.Transpose({3, 4}, {2, 3}))
# modelHeatmap:add(nn.ParallelTable():add(heatmapBranch):add(segmentationBranch_1):add(segmentationBranch_2))
# modelHeatmap:add(nn.JoinTable(1, 3))
# modelHeatmap:cuda()
# modelHeatmap:evaluate()

""" PYTHON """

class CustomNonParamLayer(nn.Module):

    def __init__(self, sampleDim): 
        super(CustomNonParamLayer, self).__init__()
        self.sampleDim = sampleDim

    def forward(self, x):
        heatmapBranch = x * 0.1
        segmentationBranch_1 = nn.functional.softmax(x).view(-1, self.sampleDim, self.sampleDim, 13).transpose(2,3).transpose(1,2)
        segmentationBranch_2 = nn.functional.softmax(x).view(-1, self.sampleDim, self.sampleDim, 17).transpose(2,3).transpose(1,2)
        return torch.cat([heatmapBranch, segmentationBranch_1, segmentationBranch_2], 1) 

modelHeatmap = torch.load(opt.loadModel)
modelHeatmap = nn.Sequential(modelHeatmap, CustomNonParamLayer(sampleDim))
modelHeatmap.to(torch.device("cuda:0")
modelHeatmap.eval()

""" }}} """

""" {{{  Use functions from FloorPlanTransformation/utils/floorplan_utils.lua to complete prediction """
""" LUA """ 
# local floorplan = image.load(opt.floorplanFilename, 3)
# local representationPrediction = fp_ut.invertFloorplan(modelHeatmap, floorplan)
# local representationImage = fp_ut.drawRepresentationImage(floorplan, representationPrediction)
# fp_ut.saveRepresentation(opt.outputFilename .. '.txt', representationPrediction)
# fp_ut.writePopupData(floorplan:size(3), floorplan:size(2), representationPrediction, opt.outputFilename .. '_popup', representationPrediction)
# image.save(opt.outputFilename .. '.png', representationImage)

""" PYTHON """
floorplan = np.array(mpimg.imread(opt.floorplanFilename))
floorplan = np.reshape(floorplan, (1, floorplan.shape[0], floorplan.shape[1], floorplan.shape[2]));
representationPrediction = fp_ut.invertFloorplan(modelHeatmap, floorplan)
representationImage = fp_ut.drawRepresentationImage(floorplan, representationPrediction)
fp_ut.saveRepresentation("{}.txt".format(opt.outputFilename), representationPrediction)
fp_ut.writePopupData(floorplan.shape[2], floorplan.shape[1], representationPrediction, "{}_popup".format(opt.outputFilename), representationPrediction)
mpimg.imsave(fname="{}.png".format(opt.outputFilename), arr=representationImage)
""" }}} """
