# [1]W. Chan, Programming Fundamentals (COSC2531) Assignment 2. RMIT, 2022.

"""Analysis: it is a comprehensive exercise reflecting OO concept like encapsulation, polymorphism, access control, etc.
it also requires students to design how to implement a program. Concept of static variable vs. instance variable within
classes is also in this assignment.

Discussion: most programming skills were taught in lectorial or lab. It should teach more about lambda because it is
the trend to use lambda.

Reflection: can re-use part of code from assignment 1. Better design compares to assignment 1. Saving value in customer
class cannot reflect the amount of orders item if the discount rate of a VIP changed or the threshold changed.

Improvement Items:
1.) separate the code into different files
2.) Exception handling can be better
3.) can append file instead of replace file when terminates
4.) threshold cannot be saved

"""

from datetime import datetime
import sys

# Common variable
separator_multiplier = 50
separator_message = "-" * separator_multiplier
g_datetime_format = "%d/%m/%Y %H:%M:%S"

class FontColor:
    """Abstract class for showing Font color
    """
    GREEN = '\033[92m'  # green
    ERROR = '\033[91m'  # red
    END = '\033[0m'  # white

def error(message):
    """show error messages in red color
    :param err:
    :param message:
    :return:
    """
    print( "{}Error - {}{}".format(FontColor.ERROR, message, FontColor.END))

def input_with_color(message):
    """show input messages in green color
    :param message:
    :return: str: input from user
    """
    return input(FontColor.GREEN + message + FontColor.END)

class Customer:
    """Class of a customer, which store
    ID(int), name(string), value (float), discount_rate (float)
    """
    discount_rate=0
    def __init__(self, ID, name, value = '0.0'):
        if not Customer.is_id(ID):
            raise Exception("invalid customer ID")
        if not Verify.float_positive(value):
            raise Exception("invalid price")
        self.__ID = ID.strip()
        self.__name = name.strip()
        self.__value = float(str(value).strip())

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, ID):
        if Customer.is_id(ID):
            self.__ID = ID.strip()
        else:
            error("error of Customer ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name.strip()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = float(str(value).strip())
        except ValueError as err:
            error("error of Customer value")
            raise err

    def get_discount(self, total_cost):
        """get discount for VIP customer as VIP may have second discount
        :param total_cost:
        :return: (float)
        """
        return self.discount_rate

    def is_VIP(self):
        """true if is VIP Member
        :return: (bool)
        """
        return False

    @staticmethod
    def is_id(value):
        """
        validate ID
        :param value:
        :return: (bool)
        """
        if value[0].upper() == "C" or value[0].upper() == "M" or value[0].upper() == "V":
            try:
                int(value[1:])
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def get_by_name(customer_name):
        """
        get customer instance by customer name
        :param customer_name: (str)
        :return: Customer/None
        """
        for customer in Records.customers.values():
            if customer.name == customer_name:
                return customer
        return None

    @staticmethod
    def find(value):
        """
        find customer instance by customer ID / name, firstly by ID then by name
        :param value: (str) customer id or name
        :return: Customer / None
        """
        if Customer.is_id(value) and value in Records.customers:
            cust = Records.customers[value]
            if cust is not None:
                return cust
        return Customer.get_by_name(value)

    @staticmethod
    def read(filename):
        """
        read customer info from file
        :param filename:
        :return:
        """
        customers_from_file = Read.file(filename)
        counter = 1
        for cust in customers_from_file:
            if len(cust) != 4:
                error("invalid customer line, line: {}".format(counter))

            if cust[0][0].upper() == "C":
                # Customer
                try:
                    customer = Customer(cust[0], cust[1], cust[3])
                    Records.customers.update({customer.ID: customer})
                except ValueError as err:
                    error("error on line: {}. Skipped".format(counter))
            elif cust[0][0].upper() == "M":
                # Member
                try:
                    member = Member(cust[0], cust[1], cust[3])
                    member.set_rate(cust[2])
                    Records.customers.update({member.ID: member})
                except ValueError as err:
                    error("error on line: {}. Skipped".format(counter))
                pass
            elif cust[0][0].upper() == "V":
                # VIP
                try:
                    vip_member = VIPMember(cust[0], cust[1], cust[3])
                    vip_member.set_rate(cust[2])
                    Records.customers.update({vip_member.ID: vip_member})
                except ValueError as err:
                    error("error on line: {}. Skipped".format(counter))
                pass
            else:
                error("invalid customer format, line: {}".format(counter))
            counter += 1

    @staticmethod
    def list():
        """
        to list all customers from Records
        :return:
        """
        for cust in Records.customers.values():
            print("id: {}, name: {}, discount: {}, value: {}".format(cust.ID, cust.name, cust.discount_rate, cust.value))

    @staticmethod
    def get_latest_id():
        return Records.get_latest_identifier(Records.customers)

    @staticmethod
    def add(cust_name, member_type):
        """
        Create Customer and add to Records
        :param member_type:
        :param cust_name: (str)
        :return: Customer
        """
        ID_int = Customer.get_latest_id() + 1
        ID = member_type + str(ID_int)
        if member_type == "C":
            new = Customer(ID, cust_name, 0.0)
        elif member_type == "M":
            new = Member(ID, cust_name, 0.0)
        else:
            new = VIPMember(ID, cust_name, 200.0)
        Records.customers[ID] = new
        return new

    @staticmethod
    def reveal_most_valuable():
        """
        reveal most valuable customer
        use max function to select the customer with the greatest value
        :return:
        """
        most_valued_cust_id= max(Records.customers, key=lambda k: Records.customers[k].value)
        most_valued_cust = Customer.find(most_valued_cust_id)
        print("The most popular product is {}, with $ {} cost.".format(
            most_valued_cust.name, most_valued_cust.value))

class Member(Customer):
    """Class of a member which is a child of Customer
    discount_rate is 0.05
    """
    discount_rate=0.05
    def __init__(self, ID, name, value=0.0):
        super().__init__(ID, name, value)

    @staticmethod
    def set_rate(rate):
        try:
            Member.discount_rate = float(rate.strip())
        except ValueError as err:
            error("error of Member discount_rate")
            raise err

    def get_discount(self, total_cost):
        return self.discount_rate

class VIPMember(Member):
    """Class of a VIP member which is a child of Member
    default discount_rate is 0.1, it is adjustable for each VIP
    second_discount_rate is 0.05, it is a read only value
    threshold is 1000, it is adjustable for all VIPs
    """
    discount_rate = 0.1
    threshold = 1000

    def __init__(self, ID, name, value=0):
        super().__init__(ID, name, value)

    @property
    def second_discount_rate(self):
        return 0.05

    @property
    def vip_fee(self):
        return 200

    def set_rate(self, rate):
        """ set first discount rate for a VIP member
        :param rate:
        :return:
        """
        try:
            rate = float(rate.strip())
            if rate >= 1:
                rate /= 100
            self.discount_rate = rate
        except ValueError as err:
            error("error of VIP discount_rate")
            raise err

    def is_VIP(self):
        return True

    def get_discount(self, total_cost):
        if total_cost < VIPMember.threshold:
            return self.discount_rate
        else:
            return self.discount_rate + self.second_discount_rate

    @staticmethod
    def adjust_discount():
        """
        to adjust a particular VIP discount from user input
        :return:
        """
        vip_id_name = Read.vip_id_or_name()
        customer = Customer.find(vip_id_name)

        if customer is not None and customer.is_VIP():
            vip_discount_str = Read.vip_discount()
            vip_discount = Verify.float_positive(vip_discount_str)
            while not vip_discount:
                error("Wrong float!")
                vip_discount_str = Read.vip_discount()
                vip_discount = Verify.float_positive(vip_discount_str)

            customer.set_rate(vip_discount_str)
        else:
            error("Invalid customer!")

    @staticmethod
    def adjust_threshold():
        """
        to adjust threshold for all VIPs from user input
        :return:
        """
        threshold = Read.threshold_with_validation()
        VIPMember.threshold = threshold

class Product:
    """Class to keep track product information
    ID(string), name(string), price(float) and stock(int)
    """
    def __init__(self, ID, name, price, stock):
        if not Product.is_id(ID):
            raise Exception("invalid customer ID")
        if price.strip() == "":
            price = '0.0'
        if not Verify.price(price):
            raise Exception("invalid price")
        if not Verify.integer(stock):
            raise Exception("invalid stock")
        self.__ID = ID.strip()
        self.__name = name.strip()
        self.__price = float(str(price).strip())
        self.__stock = int(stock.strip())

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, ID):
        if Product.is_id(ID):
            self.__ID = ID.strip()
        else:
            error("error of Customer ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name.strip()

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        try:
            self.__price = float(price.strip())
        except ValueError as err:
            error("error of Product price")
            raise err

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, stock):
        try:
            self.__stock = int(stock.strip())
        except ValueError as err:
            error("error of Product stock")
            raise err

    def decrease_stock(self, value):
        """to lower the stock level if a customer place an order
        :param value:
        :return:
        """
        if self.__stock - value >= 0:
            self.__stock -= value
        else:
            error("Stock ({}) in low level - {}. Cannot be sold for {} pieces".format(self.name, self.stock, value))

    def is_bundle(self):
        """return True if it is a bundle product
        :return:
        """
        return False

    @staticmethod
    def is_id(value):
        """ check value is product ID format
        :param value:
        :return:
        """
        if value[0].upper() == "P" or value[0].upper() == "B":
            try:
                int(value[1:])
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def get_by_name(product_name):
        """
        get product instance by product name
        :param product_name: (str)
        :return: Product/None
        """
        for product in Records.products.values():
            if product.name == product_name:
                return product
        return None

    @staticmethod
    def find(value):
        """
        find product instance by product ID / name
        :param value: (str) product id or name
        :return: Product / None
        """
        if Product.is_id(value) and value in Records.products:
            prod = Records.products[value]
            if prod is not None:
                return prod
        return Product.get_by_name(value)

    @staticmethod
    def read(filename):
        """
        read product info from files
        :param filename:
        :return:
        """
        products_from_file = Read.file(filename)
        for prod in products_from_file:
            if not Product.is_id(prod[0]):
                raise Exception()
            if prod[0][0] == "P":
                product = Product(prod[0], prod[1], prod[2], prod[3])
            elif prod[0][0] == "B":
                product = Bundle(prod[0], prod[1], prod[2:-1], prod[-1])
            Records.products.update({product.ID: product})

    @staticmethod
    def list():
        """
        list all products from Records
        :return:
        """
        for prod in Records.products.values():
            if not prod.is_bundle():
                print("id: {}, name: {}, price: {}, stock: {}".format(prod.ID, prod.name, prod.price, prod.stock))
            else:
                component_names = ""
                for bundle_component in prod.product_list:
                    component_names += bundle_component.ID + ", "
                print("id: {}, name: {}, name of component: {}stock: {}".format(prod.ID, prod.name, component_names,
                                                                                prod.stock))

    @staticmethod
    def get_latest_id():
        """
        get the latest no. of the identifier
        :return:
        """
        return Records.get_latest_identifier(Records.products)

    @staticmethod
    def reveal_most_popular():
        """
        find the most popular (i.e. the highest no. of ordered product)
        :return:
        """
        num_matrix, qty_matrix = Order.create_prod_order_matrix()
        if num_matrix:
            most_pop_prod = max(num_matrix, key=num_matrix.get)
            print("The most popular product is {}, with {} order(s).".format(
                Product.find(most_pop_prod).name, num_matrix[most_pop_prod]))
        else:
            error("No order record!!!")

class Bundle(Product):
    """Child class of Product
    Group of Products
    Enjoy 80% discount
    """
    bundle_discount = 0.8
    def __init__(self, ID, name, product_list, stock):
        price = 0.0
        self.__product_list = []

        for product_name in product_list:
            product = Product.find(product_name.strip())
            if product is not None:
                price += product.price
                self.__product_list.append(product)
            else:
                raise Exception('Product ID not in Product list for Bundle')
        price *= Bundle.bundle_discount
        super().__init__(ID, name, str(price), stock)

    @property
    def product_list(self):
        return self.__product_list

    @product_list.setter
    def product_list(self, value):
        self.__product_list = value

    def is_bundle(self):
        """
        return true if is a bundle product
        :return:
        """
        return True

class Verify:
    """
    a class with all static method about verification
    """
    @staticmethod
    def membership_type(type):
        return type == "V" or type == "M"

    @staticmethod
    def y_n(val):
        """
        verify string is 'y' or 'n'
        :param val: (str)
        :return: boolean
        """
        return val == 'y' or val == 'n'

    @staticmethod
    def integer(val):
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

    @staticmethod
    def quantity(val):
        """
        verify quantity and return True if it is positive integer, return False if it is not
        :param val:
        :return: boolean
        """
        if Verify.integer(val):
            return int(val) > 0
        else:
            return False

    @staticmethod
    def float_positive(value):
        """
        check value is float
        :param value:
        :return:
        """
        try:
            p = float(value)
            return p >= 0
        except ValueError:
            return False

    @staticmethod
    def price(price):
        """
        check price is float except empty
        :param price:
        :return:
        """
        if price.strip() == "":
            return True
        try:
            p = float(price)
            return True
        except ValueError:
            return False

class Read:
    """
    a class with all static method about read file or user input
    """
    @staticmethod
    def file(filename):
        file = None
        try:
            file = open(filename, 'r')
            line_from_file = file.readline()
            lines = []
            while line_from_file:
                fields_from_line = line_from_file.split(',')
                lines.append(fields_from_line)
                line_from_file = file.readline()
        except:
            raise Exception("IO error")
        finally:
            file.close()
        return lines

    @staticmethod
    def customer_name():
        return input_with_color("Enter the name of the customer: ")

    @staticmethod
    def y_n(message):
        """
        read user input with 'y' or 'n' with error and retry
        :param message:
        :return: boolean: y = True, n = False
        """
        y_n = input_with_color(message)
        while not Verify.y_n(y_n):
            error("Enter y or n only")
            y_n = input_with_color(message)
        return convert_y_n_to_boolean(y_n)

    @staticmethod
    def is_join_membership():
        """
        read membership with error and retry
        :return: boolean: y = True, n = False
        """
        return Read.y_n("Customer does not have a membership. Does the customer want to have a membership [enter y or n]: ")

    @staticmethod
    def membership_type():
        """
        read membership type with error and retry
        :return: boolean: y = True, n = False
        """
        message = "Please choose a membership type. Member[M] or VIP[V]: "
        member_type = input_with_color(message)
        while not Verify.membership_type(member_type):
            error("Enter M or V only")
            member_type = input_with_color(message)
        return member_type

    @staticmethod
    def continue_shopping():
        """
        read continue shopping with error and retry
        :return: boolean: y = True, n = False
        """
        return Read.y_n("Continue shopping? [enter y or n]: ")

    @staticmethod
    def product_name():
        """
        read product name in color
        :return: (str) user input
        """
        return input_with_color("Enter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]: ")

    @staticmethod
    def order_quantity():
        """
        read order quantity in color
        :return: (str) user input
        """
        return input_with_color("Enter the product quantity [enter a positive integer only, e.g. 1, 2, 3]: ")

    @staticmethod
    def add_product_name():
        """
        read product name in color
        :return: (str) user input
        """
        return input_with_color("Enter the product name to be added [commas separated format]: ")

    @staticmethod
    def add_product_price():
        """
        read product price in color
        :return: (str) user input
        """
        return input_with_color("Enter the product price to be added [commas separated format]: ")

    @staticmethod
    def vip_id_or_name():
        """
        read vip name or id
        :return: (str)
        """
        return input_with_color("Enter VIP name or ID: ")

    @staticmethod
    def vip_discount():
        """
        read vip discount
        :return: (str)
        """
        return input_with_color("Enter VIP discount: ")

    @staticmethod
    def threshold():
        """
        read vip discount
        :return: (str)
        """
        return input_with_color("Enter VIP Threshold: ")

    @staticmethod
    def product_name_with_validation():
        """
        read product name by user input with checking product is in list
        :return: product/None
        """
        prod_name = Read.product_name()
        product = Product.find(prod_name)
        while not product:
            error("Product is not in product list.")
            prod_name = Read.product_name()
            product = Product.find(prod_name)
        if product.price > 0:
            return product
        else:
            error("Product - " + product.name + " cannot be sold.")
            return None

    @staticmethod
    def order_quantity_with_validation():
        """
        read order quantity by user input with checking positive integer
        :return: (int)
        """
        quantity = Read.order_quantity()
        while not Verify.quantity(quantity):
            error("Quantity is not a positive integer.")
            quantity = Read.order_quantity()
        return int(quantity)

    @staticmethod
    def threshold_with_validation():
        """
        read threshold by user input with checking positive number
        :return: (float)
        """
        threshold = Read.threshold()
        while not Verify.float_positive(threshold):
            error("Threshold is not a positive number.")
            threshold = Read.threshold()
        return float(threshold)

class Order:
    """Class to handle customers' orders
    customer(Customer), product(Product) and quantity(int),
    quantity is int as it is positive integer
    """
    order_message = "{customer_name} purchases {quantity} x {product_name}.\nUnit price: {product_price} (AUD) "
    discount_message = "{customer_name} gets a discount of {discount}%.\nTotal price: {price} (AUD) "

    def __init__(self, customer):
        self.customer = customer
        self.prod_quan_dict = {}

    def add_prod_quan(self, prod, quan):
        quantity = self.prod_quan_dict[prod] + quan if prod in self.prod_quan_dict else quan
        self.prod_quan_dict[prod] = quantity

    def check_empty(self):
        """
        checking an order is empty
        :param self:
        :return: (bool)
        """
        return self.customer is not None and len(self.prod_quan_dict) > 0

    def show_cost(self, is_new_member):
        """
        show all costs of a single order with formatted string
        an order can have more than 1 product
        :param self:
        :param is_new_member: boolean
        :return: void
        """
        discounted_total_cost = self.calculate_total()

        print(separator_message)
        order_cost = 0.0
        for product in self.prod_quan_dict.keys():
            order_cost += product.price * round(self.prod_quan_dict[product], 2)
            print(Order.order_message.format(customer_name=self.customer.name,
                                       quantity=self.prod_quan_dict[product],
                                       product_name=product.name,
                                       product_price=str(product.price).rjust(15)))
        discount_rate = self.customer.get_discount(order_cost)
        order_cost = round(order_cost * (1 - discount_rate), 2)

        if is_new_member and self.customer.is_VIP():
            print("Membership price: {} (AUD)".format(str(200.0).rjust(9)))
            order_cost += 200
        print(Order.discount_message.format(customer_name=self.customer.name,
                                      discount=discount_rate * 100,
                                      price=str(round(order_cost, 2)).rjust(14)))
        print(separator_message)
        return order_cost

    def calculate_total(self):
        """
        calculate total with membership discount
        return float because price is in 1 decimal place and multiplied by discount rate
        :param self:
        :return: (float)
        """
        total_cost = 0
        for prod in self.prod_quan_dict.keys():
            total_cost += round(prod.price * self.prod_quan_dict[prod], 2)

        if self.customer.is_VIP():
            if total_cost > self.customer.threshold:
                discounted_total_cost = round(
                    total_cost * (1 - self.customer.discount_rate - self.customer.second_discount_rate), 2)
            else:
                discounted_total_cost = round(total_cost * (1 - self.customer.discount_rate), 2)
        else:
            discounted_total_cost = round(total_cost * (1 - self.customer.discount_rate), 2)
        return discounted_total_cost

    @staticmethod
    def read(filename):
        """
        read file with passed variable and return array of string
        :param filename: (str)
        :return: (array)
        """
        orders_from_file = Read.file(filename)
        for i, order in enumerate(orders_from_file):
            try:
                customer = Customer.find(order[0])
                if customer is None:
                    raise FileReadError("Cannot find customer in orders at line: " + str(i+1))
                class_order = ClassOrder(customer, datetime.strptime(order[-1].strip(), g_datetime_format))
                prod_quan_list = order[1:-1]
                if len(prod_quan_list) % 2 != 0:
                    raise FileReadError("Orders not in format at line: " + str(i + 1))
                for j in range(0, len(prod_quan_list), 2):
                    product_id_name = prod_quan_list[j].strip()
                    product = Product.find(product_id_name)
                    if product is None:
                        raise FileReadError("Cannot find product at line: " + str(i+1))

                    product_quan = prod_quan_list[j+1]
                    if not Verify.quantity(product_quan):
                        raise FileReadError("Quantity format is not correct line: " + str(i + 1))
                    class_order.add_prod_quan(product, int(product_quan))
                Records.orders.append(class_order)
            except FileReadError as err:
                error("skip order file line: " + str(i+1))
                pass

    @staticmethod
    def display_all(show_customer=False):
        """
        to display all orders or orders from a particular customer
        :param show_customer:
        :return:
        """
        customer = None
        if show_customer:
            cust_name = Read.customer_name()
            customer = Customer.find(cust_name)
            if not customer:
                error("Invalid customer!")
                return
        for order in Records.orders:
            prod_str = ""
            for prod in order.prod_quan_dict.keys():
                prod_str = prod.name + ", " + str(order.prod_quan_dict[prod])
            if customer is not None:
                if customer.ID != order.customer.ID:
                    pass
                else:
                    print("{}, {}, {}".format(order.customer.name, prod_str, order.order_date_time))
            else:
                print("{}, {}, {}".format(order.customer.name, prod_str, order.order_date_time))

    @staticmethod
    def summarize():
        """
        to show the tables for summarization of all orders
        :return:
        """
        order_cust_matrix = {}
        prod_order_matrix = {}
        for order in Records.orders:
            if order.customer.name in order_cust_matrix.keys():
                dict = order_cust_matrix[order.customer.name]
            else:
                dict = {}
            for prod in Records.products.values():
                if prod in order.prod_quan_dict.keys():
                    quan = order.prod_quan_dict[prod]
                else:
                    quan = 0
                if prod.ID in dict.keys():
                    dict[prod.ID] += quan
                else:
                    dict[prod.ID] = quan
            order_cust_matrix[order.customer.name] = dict
        # print(order_cust_matrix)
        print("".ljust(15), end="")
        for prod_id in Records.products.keys():
            print(prod_id.ljust(5), end="")
        print()
        for cust_name in order_cust_matrix.keys():
            print(cust_name.ljust(15), end="")
            for prod_id in Records.products.keys():
                print(str(order_cust_matrix[cust_name][prod_id]).ljust(5), end="")
            print()
        print("-"*(15+len(Records.products)*5))

        prod_order_num_matrix, prod_order_qty_matrix = Order.create_prod_order_matrix()
        print("OrderNum".ljust(15), end="")
        for prod_id in prod_order_num_matrix.keys():
            print(str(prod_order_num_matrix[prod_id]).ljust(5), end="")
        print()
        print("OrderQty".ljust(15), end="")
        for prod_id in prod_order_qty_matrix.keys():
            print(str(prod_order_qty_matrix[prod_id]).ljust(5), end="")
        print()

    @staticmethod
    def create_prod_order_matrix():
        """
        create a dictionary for showing the summarize table
        :return:
        """
        prod_order_num_matrix = {}
        prod_order_qty_matrix = {}
        for order in Records.orders:
            for product in Records.products.values():
                if product.ID not in prod_order_num_matrix.keys():
                    prod_order_num_matrix[product.ID] = 0
                if product in order.prod_quan_dict.keys():
                    quan = order.prod_quan_dict[product]
                    prod_order_num_matrix[product.ID] += 1
                else:
                    quan = 0
                if product.ID in prod_order_qty_matrix.keys():
                    prod_order_qty_matrix[product.ID] += quan
                else:
                    prod_order_qty_matrix[product.ID] = 0
        return prod_order_num_matrix, prod_order_qty_matrix

    @staticmethod
    def place():
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
        join_membership = False
        cust_name = Read.customer_name()
        customer = Customer.find(cust_name)
        if not customer:
            join_membership = Read.is_join_membership()
            if join_membership:
                member_type = Read.membership_type()
                customer = Customer.add(cust_name, member_type)
            else:
                customer = Customer.add(cust_name, "C")
        now = datetime.now()
        class_order = ClassOrder(customer, now)

        while continue_shop:
            product = Read.product_name_with_validation()
            if product:
                quantity = Read.order_quantity_with_validation()
                product.decrease_stock(quantity)
                class_order.add_prod_quan(product, quantity)
            continue_shop = Read.continue_shopping()

        if class_order.check_empty():
            Records.orders.append(class_order)
            cost = class_order.show_cost(join_membership)
            customer.value += cost

class ClassOrder(Order):
    """a child class of order to record order_date_time
    """
    def __init__(self, customer, order_date_time):
        super().__init__(customer)
        self.order_date_time = order_date_time

class Records:
    """
    a class to store customers, products and orders data
    """
    customers = {} # {customerId : customer}
    products = {} # {productId : product}
    orders = [] # [ClassOrder]

    # file can be edited by program argument
    customer_file = "customers.txt"
    product_file = "products.txt"
    order_file = None

    @staticmethod
    def get_latest_identifier(ids):
        identifier = -1
        for ID in ids.keys():
            identifier = int(ID[1:]) if int(ID[1:]) > identifier else identifier
        return identifier

class ArgumentError(Exception):
    """
    an error class for argument error
    """
    def __init__(self, arg_length):
        error("Wrong number of arguments. 0 argument, 2 to 3 arguments. Arg: " + str(arg_length))
        error('E.g. python ProgFunA2_3939713.py ["customers.txt" "products.txt" ["orders.txt"]]')
        error("Customers & Products txt files are mandatory if inputted. Orders txt file is optional.")

class FileReadError(Exception):
    """
    an error class for recording error from file read and show its line no.
    """
    def __init__(self, err_msg):
        error(err_msg)

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

def get_option():
    """
    read option for main menu
    :return:
    """
    option = display_menu()
    while (not Verify.integer(option)) or 0 < int(option) > 11:
        error("Wrong option. Please re-enter")
        option = display_menu()
    return int(option)

def display_menu():
    """
    Display main menu and read user input option
    :return: (str) option
    """
    print("Welcome to the RMIT retail management system!")
    print("#" * separator_multiplier)
    print("You can choose from the following options: ")
    print("1: Place an order")
    print("2: Display existing customers")
    print("3: Display existing products")
    print("4: Adjust the discount rates of a VIP member")
    print("5: Adjust the threshold limit of all VIP members")
    print("6: Display all orders")
    print("7: Display all orders of a customer")
    print("8: Summarize all orders")
    print("9: Reveal the most valuable customer")
    print("10: Reveal the most popular product")
    print("0: Exit the program")
    print("#" * separator_multiplier)
    option = input_with_color("Choose one option: ")
    return option

def write():
    """
    to write customers, products and orders data to files as saving purpose
    :return:
    """
    cust_data = []
    prod_data = []
    ord_data = []
    for cust in Records.customers.values():
        cust_data.append("{}, {}, {}, {}".format(cust.ID, cust.name, cust.discount_rate, cust.value))
    for prod in Records.products.values():
        if prod.is_bundle():
            sub_prod_id_str = ""
            for sub_prod in prod.product_list:
                sub_prod_id_str += sub_prod.ID + ", "
            prod_data.append("{}, {}, {}{}".format(prod.ID, prod.name, sub_prod_id_str, prod.stock))
        else:
            prod_data.append("{}, {}, {}, {}".format(prod.ID, prod.name, prod.price, prod.stock))
    for order in Records.orders:
        prod_str = ""
        for prod in order.prod_quan_dict.keys():
            prod_str += "{}, {},".format(prod.name, order.prod_quan_dict[prod])
        ord_data.append("{}, {} {}".format(order.customer.name, prod_str, order.order_date_time.strftime(g_datetime_format)))
    with open(Records.customer_file, 'w') as f:
        f.write('\n'.join(cust_data))
    with open(Records.product_file, 'w') as f:
        f.write('\n'.join(prod_data))
    with open(Records.order_file, 'w') as f:
        f.write('\n'.join(ord_data))

def main():
    """
    main programme
    read files
    read options
    :return:
    """
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        Records.customer_file = sys.argv[1]
        Records.product_file = sys.argv[2]
    Customer.read(Records.customer_file)
    Product.read(Records.product_file)

    if len(sys.argv) == 4:
        Records.order_file = sys.argv[3]
    try:
        if Records.order_file is not None:
            Order.read(Records.order_file)
    except:
        error("Cannot load the order file. Run as if there is no order previously.")

    option = get_option()

    while option > 0:
        if option == 1:
            Order.place()
        elif option == 2:
            Customer.list()
        elif option == 3:
            Product.list()
        elif option == 4:
            VIPMember.adjust_discount()
        elif option == 5:
            VIPMember.adjust_threshold()
        elif option == 6:
            Order.display_all()
        elif option == 7:
            Order.display_all(True)
        elif option == 8:
            Order.summarize()
        elif option == 9:
            Customer.reveal_most_valuable()
        elif option == 10:
            Product.reveal_most_popular()
        option = get_option()

if __name__ == "__main__":
    try:
        if len(sys.argv) != 1 and (len(sys.argv) < 3 or len(sys.argv) > 4):
            raise ArgumentError(len(sys.argv))
        main()
    except Exception as err:
        error(err)
    finally:
        # any exception to write to the files
        write()
