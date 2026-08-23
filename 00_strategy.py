from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def discount(self, subtotal: float) -> float: ...


class RegularDiscount(DiscountStrategy):
    def discount(self, subtotal: float) -> float:
        # Regular discount
        return subtotal * 0.05


class VipDiscount(DiscountStrategy):
    def discount(self, subtotal: float) -> float:
        # Vip discount
        return subtotal * 0.1


class PremiumDiscount(DiscountStrategy):
    def discount(self, subtotal: float) -> float:
        # Premium discount
        return subtotal * 0.15


class FirstOrderPromoDiscount(DiscountStrategy):
    def discount(self, subtotal: float) -> float:
        # FirstOrderPromo discount (Max 200)
        return min(subtotal * 0.2, 200)


class OrderService:
    def __init__(self, strategy: DiscountStrategy):
        self.discount_strategy = strategy

    def checkout(self, subtotal: float) -> float:
        discount = self.discount_strategy.discount(subtotal)
        print(
            f"Subtotal: {subtotal}, Discount Applied: {discount}, After Discount Subtotal: {subtotal - discount}"
        )
        return subtotal - discount


class OrderController:
    def checkout(self, customer_type: str, subtotal: float) -> float:

        strategies = {
            "regular": RegularDiscount(),
            "vip": VipDiscount(),
            "premium": PremiumDiscount(),
            "first_order": FirstOrderPromoDiscount(),
        }

        strategy = strategies[customer_type]

        order_service = OrderService(strategy)

        return order_service.checkout(subtotal)


controller = OrderController()

controller.checkout("regular", 1000)
controller.checkout("vip", 1000)

controller.checkout("first_order", 1000)
