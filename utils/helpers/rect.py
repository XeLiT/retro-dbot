class Rectangle:
    def __init__(self, top_left, w, h):
        self.top_left = top_left
        self.w = w
        self.h = h
        self.bottom_right = top_left[0] + w, top_left[1] + h
        self.center = top_left[0] + w // 2, top_left[1] + h // 2

    def __repr__(self):
        return self.__dict__