""" FILE: FloorplanTransformation/code/floorplan_utils.py """

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

""" {{{ invertFloorplan function """

""" LUA """
# function utils.invertFloorplan(model, floorplan, withoutQP, relaxedQP, useStack)
""" PYTHON """
def invertFloorplan(model, floorplan, withoutQP=False,relaxedQP=False, useStack=False): 

""" LUA """
#    local lineWidth = lineWidth or 3
#    local useStack = useStack or false
""" PYTHON """
    lineWidth = 3

""" LUA """
#    local oriWidth = floorplan:size(3)
#    local oriHeight = floorplan:size(2)
#    local width = 256
#    local height = 256
""" PYTHON """
    oriWidth = floorplan.shape[2]
    oriHeight = floorplan.shape[1]
    wid th = 256
    height = 256

""" LUA """
#    local floorplanOri = floorplan:clone()
#    image.save('test/floorplan.png', floorplanOri)
#    local floorplan = image.scale(floorplan, width, height)
""" PYTHON """
    floorplanOri = np.copy(floorplan)
    if not os.path.exists('test/'):
        os.makedirs('test/')
    mpimg.imsave(fname="test/floorplan.png", arr=floorplanOri)
    floorplan = Image.open("test/floorplan.png")
    floorplan.thumbnail((width, height))
    floorplan = np.array(floorplan)
    floorplan = np.reshape(floorplan, (1, floorplan.shape[0], floorplan.shape[1], floorplan.shape[2]))
    
""" LUA """ 
#    local junctionHeatmaps, doorHeatmaps, iconHeatmaps, segmentations = utils.estimateHeatmaps(model, floorplanOri:clone(), 'single', useStack)
#    --local junctionHeatmaps, doorHeatmaps, iconHeatmaps, _ = utils.estimateHeatmaps(floorplanOri:clone(), 'single', true)
""" PYTHON """
    junctionHeatmaps, doorHeatmaps, iconHeatmaps, segmentations = estimateHeatmaps(model, np.copy(floorplanOri), "single", useStack)
    
""" LUA """
#    pl.dir.makepath('test/heatmaps/')
#    for i = 1, 13 do
#       image.save('test/heatmaps/junction_heatmap_' .. i .. '.png', junctionHeatmaps[i])
#    end
""" PYTHON """
    if not os.path.exists("test/heatmaps/"):
        os.makedirs("test/heatmaps/")
    for i in range(13):
        mpimg.imsave(fname="test/heatmaps/junction_heatmap_{}.png".format(i+1), junctionHeatmaps[i])

""" LUA """
#    for i = 1, 4 do
#       image.save('test/heatmaps/door_heatmap_' .. i .. '.png', doorHeatmaps[i])
#       image.save('test/heatmaps/icon_heatmap_' .. i .. '.png', iconHeatmaps[i])
#    end
""" PYTHON """
    for i in range(4):
        mpimg.imsave(fname="test/heatmaps/door_heatmap_{}.png".format(i+1), doorHeatmaps[i])
        mpimg.imsave(fname="test/heatmaps/icon_heatmap_{}.png".format(i+1), iconHeatmaps[i])

""" LUA """
#    pl.dir.makepath('test/segmentation/')
#    for segmentIndex = 1, 30 do
#       image.save('test/segmentation/segment_' .. segmentIndex .. '.png', segmentations[segmentIndex])
#    end
""" PYTHON """
    if not os.path.exists("test/segmentation/")
        os.makedirs("test/segmentation/")
    for segmentIndex in range(30):
        mpimg.imsave(fname="test/segmentation/segment_{}.png".format(i+1), segmentations[segmentIndex])

""" LUA """
#    local representation = {}
#    py.execute('import os')
""" PYTHON """
    class Representation:
        points = None
        doors = None
        icons = None
        walls = None

    representation = Representation()

""" LUA """
#    if withoutQP then
#       py.execute('os.system("python PostProcessing/QP.py 1")')
#       representation.points = utils.loadItems('test/points_out.txt')
#       representation.doors = utils.loadItems('test/doors_out.txt')
#       representation.icons = utils.loadItems('test/icons_out.txt')
#       representation.walls = utils.pointsToLines(oriWidth, oriHeight, representation.points, lineWidth, true)
""" PYTHON """
    if withoutQP:
        os.system("python PostProcessing/QP.py 1")
        representation.points = loadItems("test/points_out.txt")
        representation.doors = loadItems("test/doors_out.txt")
        representation.icons = loadItems("test/icons_out.txt")
        representation.walls = pointsToLines(oriWidth, oriHeight, representation.points, lineWidth, True)

""" LUA """
#       local wallMask = utils.drawLineMask(oriWidth, oriHeight, representation.walls, lineWidth)
#       --image.save('test/floorplan.png', floorplan)
#       --image.save('test/wall_mask.png', wallMask)
#       local rooms, numRooms = utils.findConnectedComponents(1 - wallMask)
""" PYTHON """
    wallMask = drawLineMask(oriWidth, oriHeight, representation.walls, lineWidth)
    rooms, numRooms = findConnectedComponents(1 - wallMask)

""" LUA """
#       local backgroundRoomIndex
#       local imageCorners = {{1, 1}, {oriWidth, 1}, {oriWidth, oriHeight}, {1, oriHeight}}
""" PYTHON """
    backgroundRoomIndex = None
    imageCorners = [(1, 1), (oriWidth, 1), (oriWidth, oriHeight), (1, oriHeight)]

""" LUA """
#       for _, imageCorner in pairs(imageCorners) do
#          local roomIndex = rooms[imageCorner[2]][imageCorner[1]]
#          if roomIndex > 0 then
#             if not backgroundRoomIndex then
#                backgroundRoomIndex = roomIndex
#             elseif roomIndex ~= backgroundRoomIndex then
#                rooms[rooms:eq(roomIndex)] = backgroundRoomIndex
#             end
#          end
#       end
""" PYTHON """
    for imageCorner in imageCorners:
        roomIndex = rooms[imageCorner[2]][imageCorner[1]]
        if roomIndex > 0:
            if not backgroundRoomIndex:
                backgroundRoomIndex = roomIndex
            elif roomIndex != backgroundIndex:
                rooms[rooms.index(roomIndex)] = backgroundRoomIndex

""" LUA """
#       if not backgroundRoomIndex then
#          backgroundRoomIndex = numRooms
#       end
#       representation.labels = {}
# 
""" PYTHON """
    if not backgroundRoomIndex:
        backgroundRoomIndex = numRooms
    representation.labels = []

""" LUA """
#       for roomIndex = 1, numRooms - 1 do
#          if roomIndex ~= backgroundRoomIndex then
#             local roomMask = rooms:eq(roomIndex)
#             if ##roomMask:nonzero() > 0 then
#                local means = roomMask:nonzero():double():mean(1)[1]
#                local y = means[1]
#                local x = means[2]
#                local maxSum
#                local maxSumSegmentIndex
#                for segmentIndex = 1, 10 do
#                   local sum = segmentations[segmentIndex][roomMask]:sum()
#                   if not maxSum or sum > maxSum then
#                      maxSum = sum
#                      maxSumSegmentIndex = segmentIndex
#                   end
#                end
#                if maxSumSegmentIndex then
#                   table.insert(representation.labels, {{x - 20, y - 10}, {x + 20, y + 10}, utils.getItemInfo('labels', maxSumSegmentIndex)})
#                end
#             end
#          end
#       end
#       return representation
#    end
# 
""" PYTHON """
    # TODO: FIGURE OUT HOW TO DO THIS
    for roomIndex in range(1, numRooms):
        if (roomIndex != backgroundRoomIndex):
            roomMask = rooms.find(roomIndex)

            if len(len(roomMask.nonzero())) > 0:
                means = roomMask.nonzero

""" LUA """
#    py.execute('os.system("python PostProcessing/QP.py")')
#    --os.exit(1)
""" PYTHON """
    os.system("python PostProcessing/QP.py")
    
""" LUA """
#    local points = utils.loadItems('test/points_out.txt')
#    local pointLabelsFile = csvigo.load({path='test/point_labels.txt', mode="large", header=false, separator='\t', verbose=false})
#    local pointLabels = {}
#    for _, labels in pairs(pointLabelsFile) do
#       table.insert(pointLabels, {tonumber(labels[1]), tonumber(labels[2]), tonumber(labels[3]), tonumber(labels[4])})
#    end
""" PYTHON """
    points = loadItems("test/points_out.txt")
    pointLabelsFile = csv.reader(open('test/point_labels.txt'), delimiter='\t')
    pointLabels = []
    for labels in pointLabelsFile:
        pointLabels.append((int(labels[0]), int(labels[1]), int(labels[2]), int(labels[3])))

""" LUA """
#    representation.points = points
# 
#    representation.walls, wallJunctionsMap = utils.pointsToLines(oriWidth, oriHeight, points, lineWidth, true)
""" PYTHON """
    representation.points = points
    representaion.walls, wallJunctionsMap = pointsToLines(oriWidth, oriHeight, points, lineWidth, True)

# TODO: FINISH THE REST
#    for wallIndex, junctions in pairs(wallJunctionsMap) do
#       local lineDim = utils.lineDim(representation.walls[wallIndex])
#       local labels_1 = pointLabels[junctions[1]]
#       local labels_2 = pointLabels[junctions[2]]
#       local label_1, label_2
#       if lineDim == 1 then
#          label_1 = math.min(labels_1[1], labels_2[4])
#          label_2 = math.min(labels_1[2], labels_2[3])
#       elseif lineDim == 2 then
#          label_1 = math.min(labels_1[3], labels_2[4])
#          label_2 = math.min(labels_1[2], labels_2[1])
#       end
#       if label_1 == 0 then
#          label_1 = 11
#       end
#       if label_2 == 0 then
#          label_2 = 11
#       end
#       table.insert(representation.walls[wallIndex], {label_1, label_2})
#    end
# 
# 
#    local wallMask = utils.drawLineMask(oriWidth, oriHeight, representation.walls, lineWidth)
# 
#    local rooms, numRooms = utils.findConnectedComponents(1 - wallMask)
#    --image.save('test/walls_backup.png', wallMask)
#    --image.save('test/rooms_backup.png', utils.drawSegmentation(rooms))
# 
#    local deltas = {{1, -1}, {1, 1}, {-1, 1}, {-1, -1}}
#    local roomLabelsMap = {}
#    for pointIndex, point in pairs(points) do
#       local roomLabels = {}
#       for orientation, delta in pairs(deltas) do
#          local label = pointLabels[pointIndex][orientation]
#          if label >= 1 then
#             local x = torch.round(point[1][1])
#             local y = torch.round(point[1][2])
#             --x = math.max(math.min(x, width), 1)
#             --y = math.max(math.min(y, height), 1)
#             for i = 1, 10 do
#                if x < 1 or x > oriWidth or y < 1 or y > oriHeight then
#                   break
#                end
#                local roomIndex = rooms[y][x]
#                if roomIndex > 0 then
#                   if not roomLabels[roomIndex] then
#                      roomLabels[roomIndex] = {}
#                   end
#                   roomLabels[roomIndex][label] = true
#                   break
#                end
#                x = x + delta[1]
#                y = y + delta[2]
#             end
#          end
#       end
#       for roomIndex, labels in pairs(roomLabels) do
#          if not roomLabelsMap[roomIndex] then
#             roomLabelsMap[roomIndex] = {}
#          end
#          for label, _ in pairs(labels) do
#             if not roomLabelsMap[roomIndex][label] then
#                roomLabelsMap[roomIndex][label] = {}
#             end
#             local x = point[1][1]
#             local y = point[1][2]
#             table.insert(roomLabelsMap[roomIndex][label], {x, y})
#          end
#       end
#    end
# 
#    representation.labels = {}
#    local labelWidth = 50
#    local labelHeight = 20
#    for roomIndex, labels in pairs(roomLabelsMap) do
#       local numLabels = 0
#       for label, locations in pairs(labels) do
#          numLabels = numLabels + 1
#       end
#       if numLabels == 1 then
#          local means = rooms:eq(roomIndex):nonzero():double():mean(1)[1]
#          local y = means[1]
#          local x = means[2]
#          for label, locations in pairs(labels) do
#             table.insert(representation.labels, {{x - labelWidth / 2, y - labelHeight / 2}, {x + labelWidth / 2, y + labelHeight / 2}, utils.getItemInfo('labels', label)})
#          end
#       else
#          for label, locations in pairs(labels) do
#             local locationGroupMap = {}
#             local groupIndex = 1
#             for locationIndex, location in pairs(locations) do
#                if not locationGroupMap[locationIndex] then
#                   locationGroupMap[locationIndex] = groupIndex
#                   local groupLocations = {location}
#                   while true do
#                      local hasChange = false
#                      for _, groupLocation in pairs(groupLocations) do
#                         for neighborLocationIndex, neighborLocation in pairs(locations) do
#                            if not locationGroupMap[neighborLocationIndex] and (math.abs(neighborLocation[1] - groupLocation[1]) < lineWidth or math.abs(neighborLocation[2] - groupLocation[2]) < lineWidth) then
#                               local lineDim = utils.lineDim({groupLocation, neighborLocation}, lineWidth)
#                               local fixedValue = torch.round((groupLocation[3 - lineDim] + neighborLocation[3 - lineDim]) / 2)
#                               local minValue = torch.round(math.min(groupLocation[lineDim], neighborLocation[lineDim]))
#                               local maxValue = torch.round(math.max(groupLocation[lineDim], neighborLocation[lineDim]))
#                               local onWall = true
#                               for value = minValue, maxValue do
#                                  if (lineDim == 1 and wallMask[fixedValue][value] == 0) or (lineDim == 2 and wallMask[value][fixedValue] == 0) then
#                                     onWall = false
#                                  end
#                               end
#                               if onWall then
#                                  table.insert(groupLocations, neighborLocation)
#                                  locationGroupMap[neighborLocationIndex] = groupIndex
#                                  hasChange = true
#                               end
#                            end
#                         end
#                      end
# 
#                      if not hasChange then
#                         break
#                      end
#                   end
#                   groupIndex = groupIndex + 1
#                end
#             end
# 
#             for groupIndex = 1, groupIndex - 1 do
#                local groupLocations = {}
#                for locationIndex, index in pairs(locationGroupMap) do
#                   if index == groupIndex then
#                      table.insert(groupLocations, locations[locationIndex])
#                   end
#                end
# 
#                if #groupLocations > 2 then
#                   local x = 0
#                   local y = 0
#                   for _, location in pairs(groupLocations) do
#                      x = x + location[1]
#                      y = y + location[2]
#                   end
#                   x = x / #groupLocations
#                   y = y / #groupLocations
# 
#                   table.insert(representation.labels, {{x - labelWidth / 2, y - labelHeight / 2}, {x + labelWidth / 2, y + labelHeight / 2}, utils.getItemInfo('labels', label)})
#                end
#             end
#          end
#       end
#    end
# 
#    representation.doors = utils.loadItems('test/doors_out.txt')
#    representation.icons = utils.loadItems('test/icons_out.txt')
#    return representation
# end


""" PYTHON """

""" }}} """

