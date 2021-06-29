import unittest
import pybresenham
from draw_file import Bresenham
import json

XY = [[], []]


def change_shape_list(array_to_change):
    array_result = [[], []]
    for i in range(array_to_change.__len__()):
        array_result[0].append(array_to_change[array_to_change.__len__()-i-1][0])
        array_result[1].append(array_to_change[array_to_change.__len__()-i-1][1])
    return array_result

class TestBresenhemLine(unittest.TestCase):
  def test_u(self):
      with open('Data_for_test/Bresenhem.json', 'r', encoding='utf-8') as f:  # открыли файл
          data = json.load(f)  # загнали все из файла в переменную
          for i in range(data['points'].__len__()):
              self.assertEqual(change_shape_list( list(pybresenham.line(
                  int(data['points'][i]['beginX']),
                  int(data['points'][i]['beginY']),
                  int(data['points'][i]['endX']),
                  int(data['points'][i]['endY']), True))),
                           Bresenham.line(XY,
                                          int(data['points'][i]['beginX']),
                                          int(data['points'][i]['beginY']),
                                          int(data['points'][i]['endX']),
                                          int(data['points'][i]['endY'])))
              XY[0].clear()
              XY[1].clear()

unittest.main()




