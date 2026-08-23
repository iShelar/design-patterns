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
    def __init__(self):
        self.strategies = {
            "vip": VipDiscount(),
            "premium": PremiumDiscount(),
            "first_order_promo": FirstOrderPromoDiscount(),
            "regular": RegularDiscount(),
        }

    def checkout(self, customer_type: str, subtotal: float) -> float:
        strategy = self.strategies[customer_type]
        discount = strategy.discount(subtotal)
        print(f'Subtotal: {subtotal}, Discount Applied: {discount}, After Discount Subtotal: {subtotal - discount}')
        return subtotal - discount



service = OrderService()

service.checkout("regular", 1000)
service.checkout("vip", 1000)
service.checkout("premium", 1000)
service.checkout("first_order_promo", 1000)
