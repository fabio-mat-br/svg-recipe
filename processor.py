#!/usr/bin/python
"""
grid (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)

"""
import sys
import re
header = """<svg height="[HEIGHT]" width="[WIDTH]" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" transform="translate(0 0)">
"""
footer = """
  </g>
</svg>
"""

delta_x = 0
delta_y = 0
zero_pos_x = 0
zero_pos_y = 0
cmdargs = sys.argv

file_in = open(cmdargs[1], "r")

file_out = open(cmdargs[1] + '.svg',"w") 
file_out_result = ""

for row in file_in.readlines():
  if "grid" in row:
    row_parameters = re.search('grid ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?)', row)
    x0, y0, xf, yf = int(row_parameters.group(1)), int(row_parameters.group(2)), int(row_parameters.group(3)), int(row_parameters.group(4))
    file_out_result += ('<g stroke="#ccc" stroke-width=".25">' + "\n")
    delta_x = (xf - x0)
    delta_y = (yf - y0)
    for i in range(0, delta_x + 1, 10):
      if((x0 + i) == 0):
        zero_pos_x = i
        file_out_result += f'<path d="m {i} 0 v {delta_y}" stroke="#396" stroke-width=".5"/>' + "\n"
      else:
        file_out_result += f'<path d="m {i} 0 v {delta_y}"/>' + "\n"
    for i in range(delta_y, -1, -10):
      if((y0 + i) == 0):
        zero_pos_y = delta_y - i
        file_out_result += f'<path d="m 0 {delta_y - i} h {delta_x}" stroke="#396" stroke-width=".5"/>' + "\n"
      else:
        file_out_result += f'<path d="m 0 {delta_y - i} h {delta_x}"/>' + "\n"
    file_out_result += ('</g>' + "\n")
  
  if "circle" in row:
    row_parameters = re.search('circle ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([a-z]+)', row)
    x, y, r, f = float(row_parameters.group(1)), float(row_parameters.group(2)), float(row_parameters.group(3)), row_parameters.group(4)
    file_out_result += f'<circle cx="{-x + zero_pos_x}" cy="{-y + zero_pos_y}" r="{r}" fill="{f}"/>' + "\n"
  if "line" in row:
    m = re.search('line ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([-+]?\d+(?:\.\d+)?) ([a-z]+) ([L|B|BF]+)', row)
    x0, y0, xf, yf, f, t = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5), m.group(6)
    if(t == 'L'):
      file_out_result += f'<line x1="{x0 + zero_pos_x}" y1="{-y0 + zero_pos_y}" x2="{xf + zero_pos_x}" y2="{-yf + zero_pos_y}" stroke="{f}" />'
    if(t == 'BF' or t == 'B'):
      file_out_result += f'<polygon points="{x0 + zero_pos_x},{-y0 + zero_pos_y} {xf + zero_pos_x},{-y0 + zero_pos_y} {xf + zero_pos_x},{-yf + zero_pos_y} {x0 + zero_pos_x},{-yf + zero_pos_y}" '
    if(t == 'BF'):
      file_out_result += f'fill="{f}" />' + "\n"
    if(t == 'B'):
      file_out_result += f'stroke="{f}" />' + "\n"
  
file_out.write(header.replace('[WIDTH]', str(delta_x)).replace('[HEIGHT]', str(delta_y))) 
file_out.write(file_out_result)
file_out.write(footer)
file_out.close() 
print('DONE')
