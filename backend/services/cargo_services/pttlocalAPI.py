import math
from models.output import Bill, BillItem, Route
from services.cargo_services.base import BaseService
def calculateWeightForPost(gram):
    if gram <= 20:
        return 29
    elif gram <= 50:
        return 38
    elif gram <= 100:
        return 61
    elif gram <= 250:
        return 77
    elif gram <= 500:
        return 98
    elif gram <= 1000:
        return 123
    elif gram <= 2000:
        return 145
    elif gram <= 3000:
        return 177
    elif gram <= 4000:
        return 207
    elif gram <= 5000:
        return 240
    else:  
        return -1
    
def calculateWeightForBox(desi, interCity):
    price = 0
    if desi <= 0.5:
        return price + 102 + 20*interCity
    elif desi <= 1:
        return price + 108 + 37*interCity
    elif desi <= 2:
        return price + 130 + 30*interCity
    else:
        price = price + 145 + 30*interCity
    desi = math.ceil(desi)

    price= price + (desi-3)*(10 + interCity*2.5)
    return price
    
def calculateHomePickUp(gram):
    if gram <= 2000:
        return 65
    elif gram <= 10000:
        return 80
    elif gram <= 20000:
        return 100
    elif gram <= 30000:
        return 160
    elif gram <= 50000:
        return 305
    else:
        # For weights above 50,000 grams, add 29 TL for every additional 1,000 grams or part thereof
        excess_weight = weight_in_grams - 50000
        additional_cost = (excess_weight // 1000) * 29
        return 305 + additional_cost
    

class PTTService(BaseService):
    ...