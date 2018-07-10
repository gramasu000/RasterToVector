""" FILE: FloorplanTransformation/code/floorplan_utils.py - estimateHeatmaps """

""" {{{ Imports """
""" LUA """
# require 'csvigo'
# require 'image'
# local pl = require 'pl.import_into' ()
# cv = require 'cv'
# require 'cv.imgproc'
# py = require('python')
# --paths.dofile('/home/chenliu/Projects/Floorplan/floorplan/InverseCAD/models/SpatialSymmetricPadding.lua')

""" PYTHON """
from PIL import Image
import csv
import matplotlib.image as mpimg
import os
""" }}} """

""" LUA """
# function utils.estimateHeatmaps(modelHeatmap, floorplan, scaleType)
""" PYTHON """
def estimateHeatmaps(modelHeatmap, floorplan, scaleType="single", useStack=False):

""" LUA """
#    local scaleType = scaleType or 'single'
#    local width, height = floorplan:size(3), floorplan:size(2)
#    local sampleDim = 256
""" PYTHON """
    width, height = floorplan.shape[2], floorplan.shape[1]
    sampleDim = 256

""" LUA """
#    package.path = 'datasets/?.lua;' .. package.path
#    package.path = '?.lua;' .. package.path
#    local dataset = require('floorplan-representation')
#    dataset.split = 'val'
""" PYTHON """
    # TODO: Figure this out

# TODO: Finish the rest
#    local output
#    if scaleType == 'single' then
#       --local input = dataset:preprocessResize(sampleDim, sampleDim)(floorplan):repeatTensor(1, 1, 1, 1):cuda()
#       --output = modelHeatmap:forward(input)[1]:double()
# 
# 
#       local floorplanScaled = dataset:preprocessScale(sampleDim)(floorplan)
#       --image.save('test/scale.png', floorplanScaled:double())
#       local offsetX, offsetY
#       if floorplanScaled:size(2) < sampleDim then
# 	 offsetY = math.floor((sampleDim - floorplanScaled:size(2)) / 2)
# 	 offsetX = 0
#       else
# 	 offsetX = math.floor((sampleDim - floorplanScaled:size(3)) / 2)
# 	 offsetY = 0
#       end
#       local temp = torch.zeros(3, sampleDim, sampleDim)
#       temp:narrow(2, offsetY + 1, floorplanScaled:size(2)):narrow(3, offsetX + 1, floorplanScaled:size(3)):copy(floorplanScaled)
#       local input = temp:repeatTensor(1, 1, 1, 1):cuda()
# 
#       output = modelHeatmap:forward(input)[1]:double()
#       output = image.crop(output, offsetX, offsetY, offsetX + floorplanScaled:size(3), offsetY + floorplanScaled:size(2))
# 
#       --[[
# 	 image.save('test/heatmaps/floorplan.png', dataset:postprocess()(input[1]))
# 	 for i = 1, 13 do
# 	 image.save('test/heatmaps/junction_heatmap_' .. i .. '.png', output[i])
# 	 end
# 	 os.exit(1)
#       ]]--
#    elseif scaleType == 'full' then
#       local floorplanNormalized = dataset:preprocessNormalization()(floorplan)
#    else
#       local floorplanNormalized = dataset:preprocessNormalization()(floorplan)
# 
#       local inputParamMap = {}
#       local scale = 0
#       local inputs
#       while math.max(floorplanNormalized:size(3), floorplanNormalized:size(2)) > sampleDim / 2 or not inputs do
# 	 for offsetX = 0, floorplanNormalized:size(3) - 1, sampleDim do
# 	    for offsetY = 0, floorplanNormalized:size(2) - 1, sampleDim do
# 	       local input = torch.zeros(3, sampleDim, sampleDim)
# 	       local inputWidth = math.min(sampleDim, floorplanNormalized:size(3) - offsetX)
# 	       local inputHeight = math.min(sampleDim, floorplanNormalized:size(2) - offsetY)
# 
# 	       input:narrow(2, 1, inputHeight):narrow(3, 1, inputWidth):copy(image.crop(floorplanNormalized, offsetX, offsetY, offsetX + inputWidth, offsetY + inputHeight))
# 
# 	       input = input:repeatTensor(1, 1, 1, 1)
# 
# 
# 	       if not inputs then
# 		  inputs = input
# 	       else
# 		  inputs = torch.cat(inputs, input, 1)
# 	       end
# 	       inputParamMap[inputs:size(1)] = {scale, offsetX, offsetY}
# 	    end
# 	 end
# 	 scale = scale + 1
# 	 floorplanNormalized = image.scale(floorplanNormalized, floorplanNormalized:size(3) / 2, floorplanNormalized:size(2) / 2)
#       end
# 
#       inputs = inputs:cuda()
# 
#       local outputs = torch.zeros(inputs:size(1), 51, sampleDim, sampleDim)
#       for batchOffset = 0, inputs:size(1) - 1, 4 do
# 	 local numInputs = math.min(inputs:size(1) - batchOffset, 4)
# 	 outputs[{{batchOffset + 1, batchOffset + numInputs}}]:copy(modelHeatmap:forward(inputs[{{batchOffset + 1, batchOffset + numInputs}}]):double())
#       end
# 
# 
#       local scaleWeights = {}
#       for i = 0, 10 do
# 	 scaleWeights[i] = 1
#       end
# 
#       local prediction = torch.zeros(51, height, width)
#       for i = 1, inputs:size(1) do
# 	 local inputParam = inputParamMap[i]
# 	 local scaleFactor = 2^inputParam[1]
# 	 local output = image.scale(outputs[i], outputs[i]:size(3) * scaleFactor, outputs[i]:size(2) * scaleFactor)
# 
# 
# 	 local offsetX = inputParam[2] * scaleFactor
# 	 local offsetY = inputParam[3] * scaleFactor
# 	 local outputWidth = math.min(width - offsetX, output:size(3))
# 	 local outputHeight = math.min(height - offsetY, output:size(2))
# 	 prediction:narrow(2, offsetY + 1, outputHeight):narrow(3, offsetX + 1, outputWidth):add(output:narrow(2, 1, outputHeight):narrow(3, 1, outputWidth) * scaleWeights[inputParam[1]])
# 
# 	 image.save('test/output_' .. i .. '.png', prediction:narrow(1, 1, 13):sum(1)[1])
#       end
#       local scaleSum = 0
# 
#       for i = 0, scale - 1 do
# 	 scaleSum = scaleSum + scaleWeights[i]
#       end
# 
#       prediction:div(scaleSum)
#       output = prediction
#    end
# 
# 
#    if true then
#       output = image.scale(output:double(), width, height, 'bicubic')
#       local doorOffset = 13
#       local doorHeatmaps = torch.cat(torch.cat(torch.cat(output:narrow(1, doorOffset + 3, 1), output:narrow(1, doorOffset + 2, 1), 1), output:narrow(1, doorOffset + 4, 1), 1), output:narrow(1, doorOffset + 1, 1), 1)
#       local iconOffset = 17
#       local iconHeatmaps = torch.cat(torch.cat(torch.cat(output:narrow(1, iconOffset + 4, 1), output:narrow(1, iconOffset + 3, 1), 1), output:narrow(1, iconOffset + 1, 1), 1), output:narrow(1, iconOffset + 2, 1), 1)
#       return output:narrow(1, 1, 13):double(), doorHeatmaps, iconHeatmaps, output:narrow(1, 22, 30):double()
#    end
# 
#    --local junctionHeatmaps = torch.zeros(nClasses, height, width)
#    --local junctionHeatmaps = output:narrow(1, 1, 13):double()
#    local confidenceMasks = output:narrow(1, 1, 13):double()
#    local junctionHeatmaps = fp_ut.extractWallPoints(confidenceMasks, nil, nil, nil, true)
# 
#    --[[
#       for i = 1, 13 do
#       image.save('test/mask_' .. i .. '.png', confidenceMasks[i])
#       end
#       for i = 1, 13 do
#       image.save('test/heatmap_' .. i .. '.png', junctionHeatmaps[i])
#       end
#    ]]--
# 
#    local confidenceMasks = output:narrow(1, 13 + 1, 4):double()
#    local heatmap_1, heatmap_2 = fp_ut.extractLinePoints(confidenceMasks[1], confidenceMasks[2], 1, nil, nil, nil, true)
#    local heatmap_3, heatmap_4 = fp_ut.extractLinePoints(confidenceMasks[3], confidenceMasks[4], 2, nil, nil, nil, true)
#    local doorHeatmaps = torch.cat(torch.cat(torch.cat(heatmap_3:repeatTensor(1, 1, 1), heatmap_2:repeatTensor(1, 1, 1), 1), heatmap_4:repeatTensor(1, 1, 1), 1), heatmap_1:repeatTensor(1, 1, 1), 1)
# 
# 
#    local confidenceMasks = output:narrow(1, 13 + 4 + 1, 4):double()
#    --[[
#       image.save('test/mask_1.png', confidenceMasks[4 * (number - 1) + 1])
#       image.save('test/mask_2.png', confidenceMasks[4 * (number - 1) + 2])
#       image.save('test/mask_3.png', confidenceMasks[4 * (number - 1) + 3])
#       image.save('test/mask_4.png', confidenceMasks[4 * (number - 1) + 4])
#    ]]--
#    local heatmap_1, heatmap_2, heatmap_3, heatmap_4 = fp_ut.extractRectanglePoints(confidenceMasks[1], confidenceMasks[2], confidenceMasks[3], confidenceMasks[4], numPoints, true)
#    local iconHeatmaps = torch.cat(torch.cat(torch.cat(heatmap_4:repeatTensor(1, 1, 1), heatmap_3:repeatTensor(1, 1, 1), 1), heatmap_1:repeatTensor(1, 1, 1), 1), heatmap_2:repeatTensor(1, 1, 1), 1)
# 
#    local segmentations = output:narrow(1, 22, 30):double()
# 
# 
#    junctionHeatmaps = image.scale(junctionHeatmaps, width, height)
#    doorHeatmaps = image.scale(doorHeatmaps, width, height)
#    iconHeatmaps = image.scale(iconHeatmaps, width, height)
# 
#    segmentations = image.scale(segmentations, width, height)
#    return junctionHeatmaps, doorHeatmaps, iconHeatmaps, segmentations
# end

