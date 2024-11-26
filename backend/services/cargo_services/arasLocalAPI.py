from services.distance import Distance
import math
from services.cargo_services.base import BaseService
class ArasService(BaseService):
    prices = {
        [72.57, 87.46, 93.92, 103.29, 112.54, 121.75, 130.62, 139.69, 148.14, 156.57, 165.00, 173.23, 181.24, 188.58, 196.14, 202.45, 212.75, 223.11, 233.44, 243.79, 254.19, 263.52, 272.81, 282.17, 291.34, 300.81, 309.73, 318.70, 327.64, 336.54, 345.57, 8.97],
        [92.54, 107.01, 114.83, 125.48, 136.85, 147.80, 156.24, 164.81, 173.12, 181.51, 190.06, 198.45, 202.86, 209.11, 215.47, 221.86, 233.41, 245.18, 256.80, 268.40, 279.97, 290.48, 301.00, 311.50, 322.01, 332.56, 342.62, 352.75, 362.84, 373.00, 383.02, 10.11],
        [97.13, 116.39, 127.24, 141.23, 155.73, 169.85, 181.25, 192.38, 204.32, 215.82, 227.33, 238.64, 246.27, 255.79, 265.23, 275.25, 301.95, 314.28, 326.65, 339.16, 356.18, 368.42, 369.64, 383.03, 396.83, 410.92, 422.68, 435.55, 448.43, 461.22, 474.14, 12.74],
        [104.61, 125.24, 138.81, 155.20, 172.27, 188.88, 203.00, 216.51, 228.24, 242.31, 254.48, 268.45, 276.63, 287.71, 298.71, 309.91, 344.57, 357.44, 371.53, 386.04, 412.35, 426.51, 443.96, 459.80, 476.26, 492.65, 508.67, 526.01, 543.62, 561.86, 551.77, 14.92],
        [113.34, 140.59, 162.54, 182.66, 203.28, 223.49, 239.60, 255.78, 273.85, 288.19, 304.31, 315.65, 326.79, 338.12, 349.73, 361.73, 379.63, 398.73, 417.61, 437.25, 455.57, 472.72, 488.88, 505.52, 522.54, 538.81, 556.21, 573.57, 591.92, 608.49, 625.94, 16.98]
        }
    pickUp = [25.42, 35.16, 42.95, 43.18, 44.69, 44.69, 51.86, 51.86, 51.86, 51.86, 51.86, 60.62, 60.62, 60.62, 60.62, 60.62, 62.97, 62.97, 62.97, 62.97, 62.97, 67.77, 67.77, 67.77, 67.77, 67.77, 75.66, 75.66, 75.66, 75.66, 75.66, 2.84]
    def calculateDistance(fromLocation, toLocation):
        return Distance.calculateDistance(fromLocation, toLocation)
    def learnPrice(self, distance, type, weight, pickUp, deliverIt):
        additionalService = pickUp + deliverIt
    # Fiyat tablosu
        distance = math.ceil(distance)
        if type == "Letter":
            if distance == 0:
                return self.prices[0][0] + additionalService*pickUp[0]
            elif distance <= 200:
                return self.prices[1][0] + additionalService*pickUp[0]
            elif distance <=600:
                return self.prices[2][0] + additionalService*pickUp[0]
            elif distance <=1000:
                return self.prices[3][0] + additionalService*pickUp[0]
            else:
                return self.prices[4][0] + additionalService*pickUp[0]
        else:
            additionalPrice = 0
            if 30<weight<40:
                additionalPrice += 115
            elif weight<50:
                additionalPrice += 190
            elif weight<75:
                additionalPrice += 310
            elif weight<100:
                additionalPrice += 460
            elif weight>100:
                additionalPrice += 3500
            weight = math.ceil(weight)
            additionalWeight = 0
            if weight>30:
                additionalWeight = weight - 30
                weight=30
            if distance == 0:
                return self.prices[0][weight] + additionalWeight*self.prices[0][31] + additionalService*pickUp[weight] + additionalWeight*pickUp[31] + additionalPrice
            elif distance <= 200:
                return self.prices[1][weight]+ additionalWeight*self.prices[1][31] + additionalService*pickUp[weight] + additionalWeight*pickUp[31] + additionalPrice
            elif distance <=600:
                return self.prices[2][weight]+ additionalWeight*self.prices[2][31] + additionalService*pickUp[weight] + additionalWeight*pickUp[31] + additionalPrice
            elif distance <=1000:
                return self.prices[3][weight]+ additionalWeight*self.prices[3][31] + additionalService*pickUp[weight] + additionalWeight*pickUp[31] + additionalPrice
            else:
                return self.prices[4][weight]+ additionalWeight*self.prices[4][31] + additionalService*pickUp[weight] + additionalWeight*pickUp[31] + additionalPrice
    

