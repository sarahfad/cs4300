def calculate_discount(price, discount):
    """Calculates the total price of a product after applying a given discount"""
    if type(price) is bool or type(discount) is bool:
        raise TypeError("price/discount must not be boolean") #explicitly state that the number cant be a bool (since its under an int)
    
    #make sure there is a valid price
    try:
        if price < 0:
            raise ValueError("price must be >= 0")
    except TypeError as e:
        raise TypeError("price must be non-negative") 
    try:
        if discount < 0 or discount > 100:
            raise ValueError("discount must be 0% to 100%")
    except TypeError as e:
        raise TypeError("discount must be a percent 0% to 100%") 

    try:
        return price - (price * discount / 100)
    except Exception as e:
        raise TypeError("price/discount must support these operations: *, /, -")


if __name__ == "__main__":
    print(calculate_discount(100, 20))
    print(calculate_discount(59.99, 0))     
    print(calculate_discount(10, 100))      
