from random import randint, choice
from datetime import datetime, timedelta
from api.products.utils import ProductGenerator
from utils.base import BaseDataGenerator, Constants


class OrderGenerator(BaseDataGenerator):
    def generate_order_item(self, product, index: int):
        quantity = randint(1, 5)
        total = round(product["price"] * quantity, 2)
        return {
            "id": index,
            "uuid": self.fake.uuid4(),
            "quantity": quantity,
            "total": total,
            "product": product,
        }
    
    
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        products = ProductGenerator().generate(n=n)
        
        orders = []
        for i in range(1, n + 1):
            order_items = []
            nb_items = randint(1, 5)
            chosen_products = [choice(products) for _ in range(nb_items)]
            
            for index, product in enumerate(chosen_products):
                order_items.append(self.generate_order_item(product=product, index=index+1))
            
            total = round(sum(item["total"] for item in order_items), 2)
            order_date = datetime.now() - timedelta(days=randint(0, 365))
            
            orders.append({
                "id": i,
                "uuid": self.fake.uuid4(),
                "customer": self.fake.name(),
                "total": total,
                "date": order_date.isoformat(),
                "address": self.fake.address(),
                "order_items": order_items,
            })
        
        return orders



class OrderItemGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        order_items = []
        for index, product in enumerate(ProductGenerator().generate(n=n), start=1):
            quantity = randint(1, 5)
            order_items.append(
                {
                    "id": index,
                    "uuid": self.fake.uuid4(),
                    "quantity": quantity,
                    "total": round(product["price"] * quantity, 2),
                    "product": product,
                }
            )
        return order_items




def generate_orders_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return OrderGenerator().generate(n=length)


def generate_order_items_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return OrderItemGenerator().generate(n=length)
