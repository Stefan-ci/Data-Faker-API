import random
from datetime import date, timedelta
from utils.base import BaseDataGenerator, Constants


class AnalyticGenerator(BaseDataGenerator):
    
    @property
    def metrics(self):
        METRICS = [
            {"name": "visits", "unit": "users", "category": "traffic"},
            {"name": "sales", "unit": "$", "category": "finance"},
            {"name": "signups", "unit": "users", "category": "conversion"},
            {"name": "bounce_rate", "unit": "%", "category": "traffic"},
            {"name": "revenue", "unit": "$", "category": "finance"},
            {"name": "conversion_rate", "unit": "%", "category": "conversion"},
        ]
        return METRICS
    
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        today = date.today()
        
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "metric_name": metric["name"],
                "value": (val := self._generate_random_value(metric["name"])),
                "previous_value": (prev := round(val * (1 - (trend := random.uniform(-0.2, 0.2))), 2)),
                "trend": round((val - prev) / prev * 100, 2) if prev else 0.0,
                "category": metric["category"].capitalize(),
                "unit": metric["unit"],
                "timestamp": self.fake.date_between(start_date=today - timedelta(days=30), end_date=today).isoformat(),
            }
            for i, metric in enumerate(random.choices(self.metrics, k=n))
        ]
    
    
    def _generate_random_value(self, metric_name: str) -> float:
        match metric_name:
            case "visits" | "signups":
                return round(random.uniform(100, 5000), 2)
            case "sales" | "revenue":
                return round(random.uniform(1000, 50000), 2)
            case "bounce_rate" | "conversion_rate":
                return round(random.uniform(10, 90), 2)
            case _:
                return round(random.uniform(1, 1000), 2)


def generate_analytics_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return AnalyticGenerator().generate(n=length)
