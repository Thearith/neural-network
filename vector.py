X_AXIS  = 0
Y_AXIS  = 1
Z_AXIS  = 2

class Vector:
  def __init__ (self, x, y, z, sensor_type):
    self.x = x
    self.y = y
    self.z = z
    self.sensor_type = sensor_type

  def get_reading(self, axis):
    if axis == X_AXIS:
      return self.x
    elif axis == Y_AXIS:
      return self.y
    elif axis == Z_AXIS:
      return self.z