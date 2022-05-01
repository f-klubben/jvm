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
        return f"Product(id={self.id},name={self.name})"


class DispensedEvent(object):
    """docstring for DispensedEvent"""

    def __init__(self, dispensed_date, status, insert_date):
        super(DispensedEvent, self).__init__()
        self.dispensed_date = dispensed_date
        self.status = status
        self.insert_date = insert_date


class FillEvent(object):
    """docstring for FillEvent"""

    def __init__(self, fill_date, insert_date, ingredient, value):
        super(FillEvent, self).__init__()
        self.fill_date = fill_date
        self.insert_date = insert_date
        self.ingredient = ingredient
        self.value = value

    def __repr__(self):
        return f"FillEvent(timestamp={self.timestamp},ingredient={self.ingredient},value={self.value})"


class IngredientLevel(object):
    """An ingredient level"""

    def __init__(self, level_date, insert_date, ingredient, value):
        super(IngredientLevel, self).__init__()
        self.level_date = level_date
        self.insert_date = insert_date
        self.ingredient = ingredient
        self.value = value


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


class EVADTS(object):
    """docstring for EVADTS"""

    def __init__(self):
        super(EVADTS, self).__init__()
        self.dispenser_date = None
        self.coffee_beans = None
        self.milk_product = None
        self.sugar = None
        self.chocolate = None
