"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    # Horizontal: object's centre must be over the basket.
    in_x = basket_rect.left <= obj.x <= basket_rect.right
    # Vertical: the object must have actually reached the basket's height
    # (its bottom edge touches the basket top) and not yet be fully below it.
    reached = obj.y + obj.radius >= basket_rect.top
    not_below = obj.y - obj.radius <= basket_rect.bottom
    return in_x and reached and not_below