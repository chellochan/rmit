# [1]W. Chan, Programming Fundamentals (COSC2531) Assignment 1. RMIT, 2022.

"""Analysis: I know Python is type-free programming language. I get use to design and implement code with type. That
is why I used class in my code. There are 3 main entities, Customer, Product & Purchase. Therefore, there are 3
global list saved. Order is relationship between purchase and product as it is many-to-many relationship

Change g_use_mock to True to use some mock data

Discussion: Added color for asking user input and Error message for better reading.

Reflection: Most challenging part is displaying most valuable customer. It is because the system design is for that
purpose.

Improvement Items:
1.) read product and prices by files
2.) export purchase records
3.) save in DB as it can not be saved

"""


# Class to save customer's name(string) and membership (boolean)
class Customer:
    def __init__(self, name, membership):
        self.name = name
        self.membership = membership


# Class to save product's name(string) and price(float), price is float as it is in 1 decimal place.
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


# Class to save purchase info customer(Customer) and order_list(Order[])
class Purchase:
    def __init__(self, customer, order_list):
        self.customer = customer  # for backward finding
        self.order_list = order_list


# Class to save order info, purchase(Purchase), product(Product) and quantity(int),
# quantity is int as it is positive integer
class Order:
    def __init__(self, purchase, product, quantity):
        self.purchase = purchase  # for backward finding
        self.product = product
        self.quantity = quantity


# Abstract class for showing Font color
class FontColor:
    GREEN = '\033[92m'  # green
    ERROR = '\033[91m'  # red
    END = '\033[0m'  # white


# Mock data of customers, products and purchase
# g_xxx means global variables for saving user data
g_discount_rate = 0.05
g_use_mock = False

mock_customer_list = [Customer("Wing", False), Customer("Hang", True)]
g_customer_list = mock_customer_list if g_use_mock else []

mock_product_list = [Product("apple", 2.0), Product("banana", 3.0)]
g_product_list = mock_product_list if g_use_mock else []

mock_purchase_list = [Purchase(mock_customer_list[1], [Order(None, mock_product_list[0], 10)]),
                      Purchase(mock_customer_list[1], [Order(None, mock_product_list[1], 10)]),
                      Purchase(mock_customer_list[0], [Order(None, mock_product_list[1], 10)])]
g_purchase_list = mock_purchase_list if g_use_mock else []


# Common variable
order_message = "{customer_name} purchases {quantity} x {product_name}.\nUnit price: {product_price} (AUD) "
discount_message = "{customer_name} gets a discount of {discount}%.\nTotal price: {price} (AUD) "
product_message = "Product Name: {product_name}Price: {price}"
separator_multiplier = 50
separator_message = "-" * separator_multiplier


def input_with_color(message):
    """
    show input messages in green color
    :param message:
    :return: str: input from user
    """
    return input(FontColor.GREEN + message + FontColor.END)


def error(message):
    """
    show error messages in red color
    :param message:
    :return:
    """
    print(FontColor.ERROR + "Error - " + message + FontColor.END)


def read_customer_name():
    return input_with_color("Enter the name of the customer: ")


def read_y_n(message):
    """
    read user input with 'y' or 'n' with error and retry
    :param message:
    :return: boolean: y = True, n = False
    """
    y_n = input_with_color(message)
    while not verify_y_n(y_n):
        error("Enter y or n only")
        y_n = input_with_color(message)
    return convert_y_n_to_boolean(y_n)


def read_is_join_membership():
    """
    read membership with error and retry
    :return: boolean: y = True, n = False
    """
    return read_y_n("Customer does not have a membership. Does the customer want to have a membership [enter y or n]: ")


def read_continue_shopping():
    """
    read continue shopping with error and retry
    :return: boolean: y = True, n = False
    """
    return read_y_n("Continue shopping? [enter y or n]: ")


def get_customer_by_name(customer_name):
    """
    get customer instance by customer name
    :param customer_name: (str)
    :return: Customer/None
    """
    for customer in g_customer_list:
        if customer.name == customer_name:
            return customer
    return None


def get_product_by_name(product_name):
    """
    get customer instance by customer name
    :param product_name: (str)
    :return: Product/None
    """
    for product in g_product_list:
        if product.name == product_name:
            return product
    return None


def verify_y_n(val):
    """
    verify string is 'y' or 'n'
    :param val: (str)
    :return: boolean
    """
    return val == 'y' or val == 'n'


def convert_y_n_to_boolean(val):
    """
    convert 'y' to True and 'n' to False
    :param val:
    :return: boolean
    """
    if val == 'y':
        return True
    else:
        return False


def read_product_name():
    """
    read product name in color
    :return: (str) user input
    """
    return input_with_color("Enter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]: ")


def read_order_quantity():
    """
    read order quantity in color
    :return: (str) user input
    """
    return input_with_color("Enter the product quantity [enter a positive integer only, e.g. 1, 2, 3]: ")


def read_add_product_name():
    """
    read product name in color
    :return: (str) user input
    """
    return input_with_color("Enter the product name to be added [commas separated format]: ")


def read_add_product_price():
    """
    read product price in color
    :return: (str) user input
    """
    return input_with_color("Enter the product price to be added [commas separated format]: ")


def verify_integer(val):
    """
    verify input integer value and return True if it is integer, return False if it is not
    :param val:
    :return: boolean
    """
    try:
        int(val)
        return True
    except ValueError:
        return False


def verify_quantity(val):
    """
    verify quantity and return True if it is positive integer, return False if it is not
    :param val:
    :return: boolean
    """
    if verify_integer(val):
        return int(val) >= 0
    else:
        return False


def display_menu():
    """
    Display main menu and read user input option
    :return: (str) option
    """
    print("Welcome to the RMIT retail management system!")
    print("#" * separator_multiplier)
    print("You can choose from the following options: ")
    print("1: Place an order")
    print("2: Add/update products and prices")
    print("3: Display existing customers")
    print("4: Display existing customers with membership")
    print("5: Display existing products")
    print("6: Reveal the most valuable customer")
    print("7: Display a customer order history")
    print("0: Exit the program")
    print("#" * separator_multiplier)
    option = input_with_color("Choose one option: ")
    return option


def add_customer(cust_name, join_membership):
    """
    Create Customer and add to global list
    :param cust_name: (str)
    :param join_membership: (boolean)
    :return: Customer
    """
    customer = Customer(cust_name, join_membership)
    g_customer_list.append(customer)
    return customer


def create_order(purchase, product, quantity):
    """
    Create order and add to global list
    :param purchase: (Purchase)
    :param product: (Product)
    :param quantity: (int)
    :return: void
    """
    order = Order(purchase, product, quantity)

    purchase.order_list.append(order)


def get_discount(customer):
    """
    Get discount from global value by customer membership
    float because it is a percentage
    :param customer:
    :return: (float)
    """
    discount = 0
    if customer.membership:
        discount = g_discount_rate
    return discount


def calculate_total(purchase, discount):
    """
    calculate total with membership discount
    return float because price is in 1 decimal place and multiplied by discount rate
    :param purchase:
    :param discount:
    :return: (float)
    """
    total_cost = 0
    for order in purchase.order_list:
        total_cost += round(order.product.price * order.quantity, 2)

    discounted_total_cost = round(total_cost * (1 - discount), 2)
    return discounted_total_cost


def show_cost(purchase):
    """
    show all costs of a single purchase with formatted string
    a purchase can have more than 1 product
    :param purchase:
    :return: void
    """
    discount = get_discount(purchase.customer)
    discounted_total_cost = calculate_total(purchase, discount)

    print(separator_message)
    order_cost = 0.0
    for order in purchase.order_list:
        order_cost += order.product.price * round(order.quantity * (1 - discount), 2)
        print(order_message.format(customer_name=purchase.customer.name,
                                   quantity=order.quantity,
                                   product_name=order.product.name,
                                   product_price=str(order.product.price).rjust(15)))
    print(discount_message.format(customer_name=purchase.customer.name,
                                  discount=discount * 100,
                                  price=str(order_cost).rjust(14)))

    print(separator_message)
    pass


def read_product_name_with_validation():
    """
    read product name by user input with checking product is in list
    :return: product/None
    """
    prod_name = read_product_name()
    product = get_product_by_name(prod_name)
    while not product:
        error("Product is not in product list.")
        prod_name = read_product_name()
        product = get_product_by_name(prod_name)
    if product.price:
        return product
    else:
        error("Product - " + product.name + " cannot be sold.")
        return None


def read_order_quantity_with_validation():
    """
    read order quantity by user input with checking positive integer
    :return: (int)
    """
    quantity = read_order_quantity()
    while not verify_quantity(quantity):
        error("Quantity is not a positive integer.")
        quantity = read_order_quantity()
    return int(quantity)


def create_purchase(customer):
    return Purchase(customer, [])


def check_purchase_empty(purchase):
    """
    checking a purchase is empty
    :param purchase:
    :return: (bool)
    """
    return purchase is not None and len(purchase.order_list) > 0


def place_order():
    """
    Step of Place an order
    1.) check customer membership
    1a.) add customer to membership global list
    2.) check continue shop
    3.) read product name
    4.) read order quantity
    5.) create purchase
    6.) show cost
    :return: (void)
    """
    purchase = None
    continue_shop = True
    cust_name = read_customer_name()
    customer = get_customer_by_name(cust_name)
    if not customer:
        join_membership = read_is_join_membership()
        customer = add_customer(cust_name, join_membership)

    while continue_shop:
        product = read_product_name_with_validation()
        if product:
            quantity = read_order_quantity_with_validation()

            if not purchase:
                purchase = create_purchase(customer)
            create_order(purchase, product, quantity)

        continue_shop = read_continue_shopping()
    if check_purchase_empty(purchase):
        g_purchase_list.append(purchase)
        show_cost(purchase)
    pass


def split_and_trim(csv):
    """
    split csv text and trim
    :param csv:
    :return: array(str)
    """
    split_csv = csv.split(",")
    for idx, val in enumerate(split_csv):
        split_csv[idx] = val.strip()
    return split_csv


def update_product(product, price):
    """
    update product price in float
    :param product:
    :param price:
    :return:
    """
    if price:
        product.price = float(price)
    else:
        price = None


def add_product(product_name, price):
    """
    add product by name and price
    :param product_name:
    :param price:
    :return:
    """
    if price:
        g_product_list.append(Product(product_name, float(price)))
    else:
        g_product_list.append(Product(product_name, None))


def verify_price(price):
    """
    check price is float
    :param price:
    :return:
    """
    try:
        p = float(price)
        return p > 0
    except ValueError:
        return False


def add_update_product():
    """
    add or update product in csv format
    1.) read product name in csv
    2.) read product price in csv
    3.) split and trim product name csv
    4.) split and trim price csv
    5.) check product in product list
    6.) verify price
    7.) add/update product
    :return:
    """
    product_name_csv = read_add_product_name()
    product_price_csv = read_add_product_price()

    product_name_list = split_and_trim(product_name_csv)
    product_price_list = split_and_trim(product_price_csv)

    for idx, product_name in enumerate(product_name_list):
        product = get_product_by_name(product_name)
        if idx < len(product_price_list):
            price = product_price_list[idx]
            if not verify_price(price):
                price = None
        else:
            price = None

        if product:
            update_product(product, price)
        else:
            add_product(product_name, price)

    return


def display_exist_customers(is_membership=False):
    """
    display all customers
    :param is_membership:
    :return:
    """
    print(separator_message)
    for customer in g_customer_list:
        if is_membership and customer.membership or not is_membership:
            print(customer.name)
    print(separator_message)


def display_exist_products():
    """
    display all existing products in format
    :return:
    """
    print(separator_message)
    for product in g_product_list:
        print(product_message.format(product_name=product.name.ljust(15), price=product.price))
    print(separator_message)


def calculate_total_cost(purchase_list):
    """
    calculate total cost with rounding to 2 decimal places
    :param purchase_list:
    :return: (float)
    """
    total = 0.0
    for purchase in purchase_list:
        discount = get_discount(purchase.customer)
        for order in purchase.order_list:
            total += (order.quantity * round(order.product.price * (1 - discount), 2))
    return total


def reveal_most_valuable_customer():
    """
    reveal most valuable customer
    1.) convert global purchase list into a dictionary key by customer name
    2.) calculate total cost spent for all customers
    3.) find max total cost
    4.) display with formatted string with most valuable customer
    :return:
    """
    customer_purchase_dict = {}
    for purchase in g_purchase_list:
        if purchase.customer.name in customer_purchase_dict:
            customer_purchase_dict[purchase.customer.name].append(purchase)
        else:
            customer_purchase_dict[purchase.customer.name] = [purchase]

    customer_total_cost_dict = {}
    for customer_name in customer_purchase_dict.keys():
        customer_total_cost_dict[customer_name] = calculate_total_cost(customer_purchase_dict[customer_name])

    most_valuable_customer_name = max(customer_total_cost_dict, key=customer_total_cost_dict.get)
    print(separator_message)
    print("Most valuable customer: {customer_name}, Total Value: {value}".format(
        customer_name=most_valuable_customer_name, value=customer_total_cost_dict[most_valuable_customer_name]))
    print(separator_message)
    pass


def find_order_quantity_by_product_name(order_list, product_name):
    """
    find order quantity in str format
    :param order_list:
    :param product_name:
    :return:
    """
    for order in order_list:
        if order.product.name == product_name:
            return str(order.quantity)
    return ""


def display_customer_order_history():
    """
    display order history with user input customer name
    1.) ask user input customer name
    2.) check input is in customer list else return to step 1
    3.) list user order by looping global purchase list
    4.) print formatted message
    :return:
    """
    ljust_num = 10
    customer_name = input_with_color("Input customer name to retrieve order history: ")
    customer = get_customer_by_name(customer_name)
    while not customer:
        error("Customer is not in customer list.")
        customer_name = input_with_color("Input customer name to retrieve order history: ")
        product = get_customer_by_name(customer_name)

    print(separator_message)
    print("This is the order history of " + customer_name)
    header = "".ljust(15)
    for product in g_product_list:
        header += product.name.ljust(ljust_num)
    print(header)
    idx = 1
    for purchase in g_purchase_list:
        if purchase.customer.name == customer_name:
            quantity_str = ""
            for product in g_product_list:
                quantity_str += find_order_quantity_by_product_name(purchase.order_list, product.name).ljust(ljust_num)
            print("Purchase {idx}".format(idx=str(idx)).ljust(15) + quantity_str)
            idx += 1
    print(separator_message)
    pass


def get_option():
    """
    read option for main menu
    :return:
    """
    option = display_menu()
    while (not verify_integer(option)) or 0 < int(option) > 7:
        error("Wrong option. Please re-enter")
        option = display_menu()
    return int(option)


def main():
    """
    main programme
    read options
    Option 1: place an order
    Option 2: add/update products and prices
    Option 3: display existing customers
    Option 4: display existing customers with membership
    Option 5: display existing products
    Option 6: reval the most valuable customer
    Option 7: display a customer order history
    Option 0: Exit
    :return:
    """
    option = get_option()

    while option > 0:
        if option == 1:
            place_order()
        elif option == 2:
            add_update_product()
        elif option == 3:
            display_exist_customers()
        elif option == 4:
            display_exist_customers(True)
        elif option == 5:
            display_exist_products()
        elif option == 6:
            reveal_most_valuable_customer()
        elif option == 7:
            display_customer_order_history()
        option = get_option()


if __name__ == "__main__":
    main()
