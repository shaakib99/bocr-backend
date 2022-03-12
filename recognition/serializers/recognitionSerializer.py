from datetime import datetime
from rest_framework import serializers
from recognition.yolov5.classes import CLASSES, TOP, LEFT, RIGHT, BOTTOM
from recognition.yolov5.detect import run as classifier


class RecognitionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    uri = serializers.URLField(max_length=200, required=False)
    result = serializers.JSONField(required=False)
    cAt = serializers.FloatField(required=False)


class RecognizerSerializer(serializers.Serializer):
    uri = serializers.URLField()
    overlapThreshold = serializers.FloatField(default=0.8, required=False)
    __classes = CLASSES
    __left = LEFT
    __right = RIGHT
    __top = TOP
    __bottom = BOTTOM

    def getResult(self):
        self.is_valid(raise_exception=True)

        self.uri = self.validated_data['uri']
        self.overlapThreshold = self.validated_data[
            'overlapThreshold'] if 'overlapThreshold' in self.validated_data else self.overlapThreshold

        classifiedResult: list[int, float, list[float, float, float,
                                                float]] = classifier(self.uri)
        classifiedResult = self.__removeInnerBox(
            classifiedResult=classifiedResult)

        mappedResult = self.__mapResult(classifiedResult)

        word = self.__constructWord(mappedResult)
        result = {"output": word, "map": classifiedResult}

        return RecognitionSerializer({
            "uri": self.uri,
            "result": result,
            "uAt": datetime.now().timestamp()
        }).data

    def __constructWord(self, result):
        string = ''
        for res in result:
            tmpStr = ''
            if 'top' in res:
                for top in res['top']:
                    if top == 66:
                        tmpStr = self.__classes[66] + tmpStr
            if 'main' in res:
                tmpStr += self.__classes[res['main']]
            if 'bottom' in res:
                for bottom in res['bottom']:
                    tmpStr += self.__classes[bottom]
            if 'right' in res:
                for right in res['right']:
                    if self.__classes[right] == 'া' and len(
                            tmpStr) > 1 and tmpStr[-1] == 'অ':
                        tmp = tmpStr[:-1]
                        tmpStr = tmpStr[-1]
                        tmpStr = 'আ'
                        tmpStr = tmp + tmpStr
                    elif self.__classes[right] == 'া' and len(
                            tmpStr) == 1 and tmpStr[0] == 'অ':
                        tmpStr = 'আ'
                    else:
                        tmpStr += self.__classes[right]
            if 'top' in res:
                for top in res['top']:
                    if top != 66:
                        tmpStr += self.__classes[top]
            if 'left' in res:
                tmpStr += self.__classes[res['left']]

            string += tmpStr

        return string

    def __mapResult(self, result):
        sortedResult = sorted(result, key=lambda x: x[2][0])
        mappedResult = []

        # ? organize, left, right and main alphabet
        for alph in sortedResult:
            cls = alph[0]

            if cls in self.__left:
                mappedResult.append({'left': cls})
            elif cls in self.__right:
                if len(mappedResult) and 'right' not in mappedResult[-1]:
                    mappedResult[-1]['right'] = [cls]
                elif len(mappedResult) and 'right' in mappedResult[-1]:
                    mappedResult[-1]['right'].append(cls)
                else:
                    mappedResult.append({'right': [cls]})
            elif cls not in self.__top and cls not in self.__bottom:
                if len(mappedResult) and 'main' not in mappedResult[-1]:
                    mappedResult[-1]['main'] = cls
                else:
                    mappedResult.append({'main': cls})
                mappedResult[-1]['item'] = alph

        # ? organize,top and bottom alphabet
        for alph in sortedResult:
            coord = alph

            # ? setting top and bottom cordinate to full size of the image in order to
            # ? place them more accurately
            coord[2][1], coord[2][3] = 0, 10000000

            cls = alph[0]

            if cls in self.__top:
                slot = self.__findSlot(coord, mappedResult)
                if slot == -1:
                    mappedResult.append({'top': [cls]})
                elif 'top' in mappedResult[slot]:
                    mappedResult[slot]['top'].append(cls)
                else:
                    mappedResult[slot]['top'] = [cls]

            elif cls in self.__bottom:
                slot = self.__findSlot(coord, mappedResult)
                if slot == -1:
                    mappedResult.append({'bottom': [cls]})
                elif 'bottom' in mappedResult[slot]:
                    mappedResult[slot]['bottom'].append(cls)
                else:
                    mappedResult[slot]['bottom'] = [cls]
        return mappedResult

    def __findSlot(self, item, result) -> int:
        overlappedRatios = [
            self.__overlapRatioWithBox1(item, res['item'])
            if 'item' in res else 0 for res in result
        ]
        index = overlappedRatios.index(max(overlappedRatios))

        if overlappedRatios[index] == 0:
            return -1

        return index

    def __removeInnerBox(self, classifiedResult: list):
        result = []
        for index1, box1 in enumerate(classifiedResult):
            isOverlapping = False
            for index2, box2 in enumerate(classifiedResult):
                if index1 != index2:
                    overlapRatio = self.__overlapRatioWithBox1(box1, box2)
                    if overlapRatio > self.overlapThreshold:
                        isOverlapping = True
                        break
            if isOverlapping == False:
                result.append(box1)
        return result

    def __overlapRatioWithBox1(self, box1: list, box2: list):
        box1Area = self.__area(box1)

        if box1Area == 0:
            raise Exception('Box1 area is 0')

        overlappedArea = self.__overlappedArea(box1, box2)
        return overlappedArea / box1Area

    def __area(self, box):
        coord = box[2]
        return abs(coord[0] - coord[2]) * abs(coord[1] - coord[3])

    def __overlappedArea(self, box1, box2):
        box1Coord = box1[2]
        box2Coord = box2[2]
        dx = min(box1Coord[2], box2Coord[2]) - max(box1Coord[0], box2Coord[0])
        dy = min(box1Coord[3], box2Coord[3]) - max(box1Coord[1], box2Coord[1])
        if (dx >= 0) and (dy >= 0):
            return dx * dy
        return 0