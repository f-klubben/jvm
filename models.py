class Product(object):
    """docstring for Product"""

    def __init__(
        self,
        id,
        name,
        cost_coffee_beans,
        cost_milk,
        cost_choco,
        cost_sugar,
        sold_out_last,
        number_dispensed,
        price,
        product_index,
        product_identifier,
        localized_name,
    ):
        super(Product, self).__init__()
        self.id = id
        self.name = name
        self.cost_coffee_beans = cost_coffee_beans
        self.cost_milk = cost_milk
        self.cost_choco = cost_choco
        self.cost_sugar = cost_sugar
        self.sold_out_last = sold_out_last
        self.number_dispensed = number_dispensed
        self.price = price
        self.product_index = product_index
        self.product_identifier = product_identifier
        self.localized_name = localized_name

    def __repr__(self):
        return f'Product(id={self.id},name={self.name})'


class DispensedEvent(object):
    """docstring for DispensedEvent"""

    def __init__(self, timestamp, status):
        super(DispensedEvent, self).__init__()
        self.timestamp = timestamp
        self.status = status


class FillEvent(object):
    """docstring for FillEvent"""

    def __init__(self, timestamp, ingredient, value):
        super(FillEvent, self).__init__()
        self.timestamp = timestamp
        self.ingredient = ingredient
        self.value = value

    def __repr__(self):
        return f'FillEvent(timestamp={self.timestamp},ingredient={self.ingredient},value={self.value})'


class DispenserInfo(object):
    """docstring for DispenserInfo"""

    def __init__(self):
        super(DispenserInfo, self).__init__()
        self.last_cleaned = None
        self.initialization_date = None
        self.total_prod_dispensed = None
        self.coffee_beans_dispensed = None
        self.milk_dispensed = None
        self.choco_dispensed = None
        self.sugar_dispensed = None
