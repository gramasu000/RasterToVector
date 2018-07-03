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
import numpy as np
import tensorflow
from tensorflow import keras
import h5py
from PIL import Image
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
inputShape = keras.layers.Input(shape=(1, sampleDim, sampleDim, 3))

modelHeatmap_val = keras.models.load_model(opt.loadModel)(inputShape)

heatmapBranch_val = keras.models.Sequential([
    keras.layers.Lambda(lambda x : x * 0.1)
])(modelHeatmap_val)

segmentationBranch_1_val = keras.models.Sequential([
    keras.layers.Activation("softmax"),
    keras.layers.Reshape((sampleDim, sampleDim, 13)),
    keras.layers.Permute((2,3)),
    keras.layers.Permute((1,2))
])(modelHeatmap_val)

segmentationBranch_2_val = keras.models.Sequential([
    keras.layers.Activation("softmax"),
    keras.layers.Reshape((sampleDim, sampleDim, 17)),
    keras.layers.Permute((2,3)),
    keras.layers.Permute((1,2))
])(modelHeatMap_val)

modelHeatMap_val = keras.layers.concatenate([heatmapBranch_val, segmentationBranch_1_val, segmentationBranch_2_val], axis=1)

modelHeatMap = keras.models.Model(inputShape, modelHeatMap)
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
floorplan = np.array(Image.open(opt.floorplanFilename))
representationPrediction = fp_ut.invertFloorplan(modelHeatmap, floorplan)
representationImage = fp_ut.drawRepresentationImage(floorplan, representationPrediction)
fp_ut.saveRepresentation("{}.txt".format(opt.outputFilename), representationPrediction)
fp_ut.writePopupData(floorplan.shape[2], floorplan.shape[1], representationPrediction, "{}_popup".format(opt.outputFilename), representationPrediction)
Image # save method

""" }}} """
