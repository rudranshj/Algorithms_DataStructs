#include <iostream>
#include <queue>
#include <unordered_map>
#include <algorithm>

using namespace std;

class Exchange {
public:

       priority_queue< pair< pair<int, int>,int> > sellOrder; //<<price,uid>,volume>
       priority_queue< pair< pair<int, int>,int> > buyOrder;
       unordered_map<int,pair<int, double>> orderBook; // {id: (volume,avgPrice)}
       int currId;

       Exchange(){
              this->currId = 1;
       }

       // InputOrder receives order, and return assigned order Id.
       // Parameters:
       //   int side:   0 is buy, 1 is sell
       //   int volume: order's quantity
       //   int price:  order's price
       // Return:
       //   int: order Id
       int inputOrder(int side, int volume, int price){
              int uid = currId;
              currId += 1;
              orderBook[uid] = make_pair(0,0.00); // tradeVol, avgPrice
              // cout<<orderBook[uid].second<<endl;
              if(side>0)
                     sellOrder.push(make_pair(make_pair(-1*price,-1*uid),volume));
              else
                     buyOrder.push(make_pair(make_pair(price,-1*uid),volume));

              matchOrder();
              return uid;
       };
       

       void matchOrder(){
              while(!sellOrder.empty() && !buyOrder.empty()){
                     pair< pair<int, int>,int> buy = buyOrder.top();
                     pair< pair<int, int>,int> sell = sellOrder.top(); 
                     int p1,id1,v1,p2,id2,v2;
                     p1 = buy.first.first; p2 = -1*(sell.first.first);
                     id1 = -1*(buy.first.second); id2 = -1*(sell.first.second);
                     v1 = buy.second; v2 = sell.second;

                     buyOrder.pop();
                     sellOrder.pop();

                     if(p2>p1) return;

                     // cout<<"processing: "<<id1<<" & "<<id2<<endl;
                     if(v1==v2){
                            orderBook[id1].second = (orderBook[id1].second*orderBook[id1].first + 1.0*p2*v1)/(1.0*(v1+orderBook[id1].first));
                            orderBook[id2].second = (orderBook[id2].second*orderBook[id2].first + 1.0*p1*v2)/(1.0*(v2+orderBook[id2].first));
                            orderBook[id1].first += v1;
                            orderBook[id2].first += v2;
                     }
                            
                     else if(v1>v2){
                            orderBook[id1].second = 0.0+ (orderBook[id1].second*orderBook[id1].first + p2*v2)/(1.0*(v2+orderBook[id1].first ));
                            orderBook[id2].second = 0.0+ (orderBook[id2].second*orderBook[id2].first + p1*v2)/(1.0*(v2+orderBook[id2].first));
                            orderBook[id1].first += v2;
                            orderBook[id2].first += v2;
                            buyOrder.push(make_pair(make_pair(p1,-1*id1),v1-v2));

                     }
                            
                     else{ //v2>v1
                            orderBook[id1].second = 0.0+(orderBook[id1].second*orderBook[id1].first + p2*v1)/(1.0*(v1+orderBook[id1].first));
                            orderBook[id2].second = 0.0+(orderBook[id2].second*orderBook[id2].first + p1*v1)/(1.0*(v1+orderBook[id2].first));
                            orderBook[id1].first += v1;
                            orderBook[id2].first += v1;
                            sellOrder.push(make_pair(make_pair(-1*p2,-1*id2),v2-v1));

                     } 
              }

       return;
       };


       // QueryOrderTrade queries order's trade volume and average price.
       // Parameters:
       //   int orderId: assigned order Id
       //   int averagePrice: return order's average trade price
       // Return:
       //   int: return order's trade volume
       void showOrderBook(){
              while(!buyOrder.empty()){
                     cout<<buyOrder.top().first.first<<" "<<buyOrder.top().first.second<<" "<<buyOrder.top().second <<endl;
                     buyOrder.pop();
              }
              cout<<endl;
              while(!sellOrder.empty()){
                     cout<<sellOrder.top().first.first<<" "<<sellOrder.top().first.second<<" "<<sellOrder.top().second <<endl;
                     sellOrder.pop();
              }
       };

       int QueryOrderTrade(int orderId, double& averagePrice){
              pair<int,double> p = orderBook[orderId];
              averagePrice = p.second;
              int tradeVolume = p.first;
              return tradeVolume;
       };

 };

int main() {
       Exchange ex;
       std::vector<int> orders;
       orders.push_back(ex.inputOrder(0, 1, 100));
       orders.push_back(ex.inputOrder(0, 2, 101));
       orders.push_back(ex.inputOrder(0, 3, 102));
       orders.push_back(ex.inputOrder(1, 4, 100));
       orders.push_back(ex.inputOrder(1, 5, 101));
       orders.push_back(ex.inputOrder(1, 6, 102));
       // ex.showOrderBook();
       for (auto& orderId : orders)
       {
              double averagePrice;
              int tradeVolume = ex.QueryOrderTrade(orderId, averagePrice);
              std::cout << "orderId: " << orderId << " tradeVolume: " << tradeVolume << " averagePrice: " << averagePrice << std::endl;
       }
               
       return 0; 
}