from api.base import BaseDataGenerator, ProductCategories


class ProductGenerator(BaseDataGenerator):
    def generate(self, n=10): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "name": self.fake.bs().title().capitalize(),
                "category": self.fake.random_element([cat.value for cat in ProductCategories]),
                "price": round(self.fake.pyfloat(left_digits=3, right_digits=2, min_value=5, max_value=999), 2),
                "ean_13": self.fake.ean13(),
                "stock": self.fake.random_int(0, 500),
                "vendor": self.fake.company(),
                "picture": self._get_product_image_url(i),
                "description": self.fake.sentence(nb_words=10),
                "rating": round(self.fake.pyfloat(left_digits=1, right_digits=1, min_value=1, max_value=5), 1),
                "reviews_count": self.fake.random_int(0, 1000),
                "created_at": self.fake.date_time_this_year().isoformat(),
            }
            for i in range(1, n + 1)
        ]
    
    def _get_product_image_url(self, index: int) -> str:
        """
        Return a stable product image URL, with fallback to local image.
        """
        # no HTTP request to send. So no need to test if it exists or not
        return f"https://source.unsplash.com/400x400/?product&sig={index}"



def generate_products_data(length=10):
    return ProductGenerator().generate(n=length)
