from collections import deque
import heapq

class Exchange:
    def __init__(self):
        self.orderBook = {}
        # use heaps
        self.buyOrder = [] # store buy in decreasing order of price, increasing order of time
        self.sellOrder = [] # store sell in increasing order of price, increasing order of time
        self.currId = 1
        pass

    
    def matchOrder(self):
        while self.buyOrder and self.sellOrder:
            buy,sell = heapq.heappop(self.buyOrder),heapq.heappop(self.sellOrder)
            p1,id1,v1 = -buy[0][0],buy[0][1],buy[1] # p1 is maximum price, a buyer is willing to buy 
            p2,id2,v2 = sell[0][0],sell[0][1],sell[1] # p2 is minimum price, a seller is willing to sell
            
            if p2>p1: return
            #print("processing: ",id1," & ",id2)
            if v1==v2:
                self.orderBook[id1][-1] = (self.orderBook[id1][-1]*self.orderBook[id1][-2] + p2*v1)/(v1+self.orderBook[id1][-2])
                self.orderBook[id2][-1] = (self.orderBook[id2][-1]*self.orderBook[id2][-2] + p1*v2)/(v2+self.orderBook[id2][-2])
                self.orderBook[id1][-2]+=v1
                self.orderBook[id2][-2]+=v2
            elif v1>v2:
                self.orderBook[id1][-1] = (self.orderBook[id1][-1]*self.orderBook[id1][-2] + p2*v2)/(v2+self.orderBook[id1][-2])
                self.orderBook[id2][-1] = (self.orderBook[id2][-1]*self.orderBook[id2][-2] + p1*v2)/(v2+self.orderBook[id2][-2])
                self.orderBook[id1][-2]+=v2
                self.orderBook[id2][-2]+=v2
                heapq.heappush(self.buyOrder,[(-p1,id1),v1-v2])
            else: # v2>v1
                self.orderBook[id1][-1] = (self.orderBook[id1][-1]*self.orderBook[id1][-2] + p2*v1)/(v1+self.orderBook[id1][-2])
                self.orderBook[id2][-1] = (self.orderBook[id2][-1]*self.orderBook[id2][-2] + p1*v1)/(v1+self.orderBook[id2][-2])
                self.orderBook[id1][-2]+=v1
                self.orderBook[id2][-2]+=v1
                heapq.heappush(self.sellOrder,[(p2,id2),v2-v1])
        
        return
        
    
    def InputOrder(self, side, volume, price):
        """
        InputOrder receives order, and return assigned order Id.
        :param side: 0 is buy, 1 is sell,-1 means not valid
        :param volume:order's quantity
        :param price:order's prices
        :return: order Id, an integer
        """
        if side<0: return None
        uid = self.currId
        self.currId += 1
        self.orderBook[uid]=[0,0] # total Vol, avg Price
        
        if side>0: #sell
            heapq.heappush(self.sellOrder,[(price, uid), volume])
        else: #buy
            heapq.heappush(self.buyOrder,[(-price, uid), volume])
        
        self.matchOrder()
        
        return uid

    def QueryOrderTrade(self, orderId):
        """
        queries order's trade volume and average price.
        :param orderId: assigned order Id
        :return: (order's trade volume, avg_price),tuple
        """        
        tradeVol, avg_price = self.orderBook[orderId][-2],self.orderBook[orderId][-1]
        return (tradeVol, avg_price)
    
    def printOrderBook(self):
        print(self.orderBook)

    

if __name__ == "__main__":
    # 0 is buy, 1 is sell
    ex = Exchange()
    orders = list()
    orders.append(ex.InputOrder(0, 1, 100))
    orders.append(ex.InputOrder(0, 2, 101))
    orders.append(ex.InputOrder(0, 3, 102))
    orders.append(ex.InputOrder(1, 4, 100))
    orders.append(ex.InputOrder(1, 5, 101))
    orders.append(ex.InputOrder(1, 6, 102))
    
    # print(ex.sellOrder)
    # print(ex.buyOrder)
    # ex.printOrderBook()
    
    for orderId in orders:
        tradeVolume, avgPrice = ex.QueryOrderTrade(orderId)
        print("orderId:%d, tradeVolume:%d, averagePrices:%f"%(orderId,tradeVolume,avgPrice))

