from pig_util import outputSchema

# return a string called price_value to PIG scirpt
@outputSchema("price_value:chararray")
def price_value(num):
    if num < 100:
        # price lower than 100 is low value
        return "low value"
    if num < 300:
        # price higher or equal to 100 and lower than 300 is medium
        return "medium"
    # price higher or equal to 300 is high value
    return "high value"