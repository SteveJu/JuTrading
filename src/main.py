import robin_connection as rc
import openbb_connection as oc
import simulator as sim
import time_system as ts
import models as models
import printing_system as ps
import asset_management as am
import time


class main:
    def __init__(self):
        pass

    if __name__ == '__main__':
        threshold = 20

        time_sys = ts.time_system()
        current_hour = time_sys.getHour()

        steve_rc = rc.robin_connection()
        steve_rc.robin_login(time_sys.getFullDateAndTime())

        stock_names, exps, strikes, types = [], [], [], []

        while current_hour < 24:
            current_hour = time_sys.getHour()
            current_min = time_sys.getMin()
            current_time = time_sys.getFullDateAndTime()
            ps.printCurrTime(current_time)

            curr_info = sim.readCurrent()
            curr_depo = sim.getCurrDepo(curr_info)
            ps.printCurrDepo(curr_depo)

            asset = sim.getCurrAsset(curr_info)
            ps.printAssets(asset)

            if current_min % 30 == 0 or len(stock_names) == 0:
                stock_names, exps, strikes, types = oc.getUnu(threshold)
            if len(stock_names) == 0:
                ps.printEmpty()
                time.sleep(1770)
            else:
                ps.printSection()
                prices = rc.see_a_stock(stock_names)
                for i in range(len(stock_names)):
                    Stock_Price = round(float(prices[i]), 2)
                    Stock_Name = stock_names[i]
                    Expiration_Date = exps[i]
                    Strike = strikes[i]
                    Opr_Type = types[i]
                    Opt_Info = rc.see_an_option(stock_names[i], exps[i], strikes[i], types[i])
                    Ask_Price = round(float(Opt_Info[0]), 2)
                    Bid_Price = round(float(Opt_Info[1]), 2)
                    Trading_Cost = round(Ask_Price - Bid_Price, 2)
                    Gamma = float(Opt_Info[2])
                    Implied_Volatility = float(Opt_Info[3])
                    Time_To_Exp = time_sys.getTimeToExp(Opt_Info[4])
                    ifCall = True
                    if Opr_Type == 'Put':
                        ifCall = False
                    m = models.models(ifCall, Stock_Price, Strike, Time_To_Exp, 0.04, Implied_Volatility, 1.0, Gamma)
                    Cal_Price = m.JumpDiffusion()
                    ps.printUnu(i, Stock_Name, Expiration_Date, Strike, Opr_Type, Stock_Price, Ask_Price, Bid_Price,
                                Trading_Cost, Cal_Price)

            time.sleep(30)
        rc.robin_logout(time_sys.getFullDateAndTime())
