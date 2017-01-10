class ExecutionEngine(object):
        def __init__(self, broker):
            self.broker = broker


        def send_order(self, ticker, quantity, limit_price):

            if quantity == 0 or limit_price <= 0:
                return
            order_req = BaseOrderRequest(symbol, quantity, 'LMT')
            order_req = limit_price


            ib_order = IBOrder()
            ib_order.m_lmtPrice = limit_price
            ib_order.m_orderType = 'LMT'
            ib_order.m_totalQuantity = abs(quantity)
            ib_order.m_allOrNone = False
            ib_order.m_transmit = True
            ib_order.m_clientId = self.clientid

            ib_order.m_tif = 'GTD'
            valid_till = self.current_time() + timedelta(seconds=10)
            ib_order.m_goodTillDate = valid_till.strftime('%Y%m%d %H:%M:%S') + ' EST'

            if quantity > 0:
                ib_order.m_action = 'BUY'
            else:
                ib_order.m_action = 'SELL'

            ib_order.m_faProfile = ticker

            contract = make_contract(ticker)
            ib_id = self._get_next_valid_order_id()
            order = Order(order=ib_order,
                          contract=contract,
                          ib_id=ib_id,
                          symbol=contract.m_symbol,
                          remaining=ib_order.m_totalQuantity)
            self.orders[order.ib_id] = order
            return order.ib_id
