from main.models import Order
from datetime import datetime
from ib.ext.Order import Order as IB_Order, Double
# IBOrder class inherits IBOrder type from ib.ext namespace, therefore functions
# for two purposes at ones
"""
This code explains what we do here.... shadowing IBOrder and linking it to model Order


from django.db import models
from django.conf import settings
from ib.lib import Double, Integer

#settings.configure()
# Django Model Order
class Order(object):
    def __init__(self):
        self.Price = models.FloatField()
# Order from package IBPy
class IBOrder(object):
    def __init__(self):
        self.m_lmtPrice = Double.MAX_VALUE
        self.m_auxPrice = Double.MAX_VALUE
        self.m_activeStartTime = self.EMPTY_STR
        self.m_activeStopTime = self.EMPTY_STR
# specific IB order for our use
class IBSOrder(Order, IBOrder):
    # Shadowing price as LMT price for use with IB
    @property
    def m_lmtPrice(self):
        return Double(self.Price)
    @m_lmtPrice.setter
    def m_lmtPrice(self, value):
        self.Price = float(value)

# We create Django model object assign price 100
x = Order()
x.Price = 100
# This is how we cast it when used in IBBroker class methods
x.__class__ = IBSOrder # we cast class as IBSOrder
# IB package can use our order as if being IBOrder as multiple inheritance and property based override allows it
# There is direct linkage to Price (++)
print(x.m_lmtPrice)
"""
class IBOrder(Order, IB_Order):
    _tif_map = {Order.TimeInForceChoice.Day: "DAY",
                Order.TimeInForceChoice.GoodTillCancel: "GTC",
                Order.TimeInForceChoice.AtTheOpening: None,
                Order.TimeInForceChoice.ImmediateOrCancel: "IOC",
                Order.TimeInForceChoice.FillOrKill: "FOK",
                Order.TimeInForceChoice.GoodTillCrossing: None,
                Order.TimeInForceChoice.GoodTillDate: "GTD"
               }
    @property
    def m_lmtPrice(self):
        return Double(self.Price)
    @m_lmtPrice.setter
    def m_lmtPrice(self, value):
        self.Price = float(self.Price)

    @property
    def m_totalQuantity(self):
        return self.Quantity
    @m_totalQuantity.setter
    def m_totalQuantity(self, value):
        self.Quantity = value

    @property
    def m_action(self):
        return "Buy" if self.Side==Order.SideChoice.Buy else "Sell"
    @m_action.setter
    def m_action(self, value):
        self.Side =   Order.SideChoice.Buy if value=="Buy" else Order.SideChoice.Sell

    @property
    def m_tif(self):
        val = self._tif_map[self.TimeInForce]
        if val is None:
            raise NotImplementedError('Time in force of this type ' + Order.TimeInForceChoice.to_str(self.TimeInForce))
        return  val
    @m_tif.setter
    def m_tif(self, value):
        val = value  # context safe
        keys = [key for key, value in self._tif_map.items() if value == val]
        if keys.count() == 0:
            raise NotImplementedError('Time in force of this type ' + Order.TimeInForceChoice.to_str(self.TimeInForce))
        self.TimeInForce = keys[0]

    @property
    def m_goodTillDate(self):
        return self.ExpireDate.strftime('%Y%m%d %H:%M:%S %Z')  #  FORMAT: 20060505 08:00:00 {time zone}
    @m_goodTillDate.setter
    def m_goodTillDate(self, value):
        self.ExpireDate = datetime.strptime(value, '%Y%m%d %H:%M:%S %Z')
