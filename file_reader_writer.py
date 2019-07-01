from sensor_data import SensorData

def read_file(file_name):
  lines = []
  with open(file_name, 'r') as reader:
    for line_terminated in reader:
      line = line_terminated.rstrip('\n')
      lines.append(line)

  return lines

def write_file(file_name, outputs):
  with open(file_name, 'w') as writer:
    for output in outputs:
      writer.write(output + "\n")

def get_sensor_list(file_name):
  lines = read_file(file_name)
  datas = []
  for line in lines:
    words = line.split()
    sensor_type = int(words[0])
    x = float(words[1])
    y = float(words[2])
    z = float(words[3])
    timestamp = long(words[4])
    is_heel_strike = int(words[5])
    data = SensorData(x, y, z, sensor_type, timestamp, is_heel_strike)
    datas.append(data)

  return datas

def get_normalizer(file_name):
  lines= read_file(file_name)
  normalizers = []
  for line in lines:
    words = line.split(", ")
    for word in words:
      if word != '':
        normalizer = float(word)
        normalizers.append(word)

  return normalizers

def get_ground_truth_raw(file_name):
  lines = read_file(file_name)
  ground_truths = []
  for line in lines:
    words = line.split()
    ground_truth = long(words[1])
    ground_truths.append(ground_truth)

  return ground_truths

def get_ground_truth(file_name):
  lines = read_file(file_name)
  ground_truths = []
  for line in lines:
    words = line.split()
    ground_truth = long(words[0])
    ground_truths.append(ground_truth)

  return ground_truths

if __name__ == "__main__":
  lines = read_file("training/percentage.txt")
  print lines



