from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, order_id, status) -> None:
        ...

class Observable(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        ...
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        ...
    @abstractmethod
    def notify(self) -> None:
        ...

class Order(Observable): # order is a Observable
    def __init__(self, order_id: str, status: str):
        self.order_id = order_id
        self.status = status
        self._observers: List[Observer] = [] # Order has observers

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        for o in list(self._observers): # if obsever after first notification, removes the observer from list, it will give error. So, we make a copy of the observer's list.
            try: # try because one observer fails shouldn't affect other observers.
                o.update(self.order_id, self.status)
            except Exception as e:
                print(f"Observer {o} failed: {e}")
    
    def set_status(self, status) -> None:
        if self.status == status:
            return # return if the status is same, no need to notify again for same status update
        self.status = status
        self.notify()
        

class EmailNotifier(Observer):
    def update(self, order_id: str, status: str) -> None:
        print(f"Email sent for order {order_id}: {status}")

class SmsNotifier(Observer):
    def update(self, order_id: str, status: str) -> None:
        print(f"SMS sent for order {order_id}: {status}")

class WarehouseService(Observer):
    def update(self, order_id: str, status: str) -> None:
        print(f"Warehouse informed: {order_id} -> {status}")


class OrderController:
    def create_order(self):
        observers = [EmailNotifier(), SmsNotifier(), WarehouseService()] # we can use factory pattern for objection creation as well.

        order = Order("ORD-123", "CREATED")
        for obs in observers:
            order.attach(obs)

        return order

controller = OrderController()
order = controller.create_order()
order.set_status("SHIPPED") 