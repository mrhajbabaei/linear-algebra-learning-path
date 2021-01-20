# import os
# from pdf2image import convert_from_path


# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, 'eqn.pdf')
# pages = convert_from_path(file_path, 500)
# for page in pages:
#     page.save(os.path.join(current_dir, 'out.jpg'), 'JPEG')



import os
import glob
import argparse
import subprocess
from pdf2image import convert_from_path


current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, 'formulas')
content = r'''\documentclass{standalone}
\begin{document}
$\displaystyle I = \int_0^h y^2\mathrm{d}A$
\end{document}
'''

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--course')
parser.add_argument('-t', '--title')
parser.add_argument('-n', '--name',) 
parser.add_argument('-s', '--school', default='My U')

args = parser.parse_args()
formula_tex_file = os.path.join(output_dir, 'formula.tex')
with open(formula_tex_file,'w') as f:
    f.write(content%args.__dict__)

cmd = ['pdflatex', '-interaction', 'nonstopmode', formula_tex_file]
proc = subprocess.Popen(cmd)
proc.communicate()

file_path = os.path.join(current_dir, 'formula.pdf')
retcode = proc.returncode
if not retcode == 0:
    os.unlink(file_path)
    raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 

os.unlink(formula_tex_file)
os.unlink(os.path.join(current_dir, 'formula.log'))
os.unlink(os.path.join(current_dir, 'formula.aux'))

pages = convert_from_path(file_path, 500)
image_files_number = len(glob.glob1(output_dir, '*.png'))
for page in pages:
    page.save(os.path.join(output_dir, f'formula-{image_files_number}.png'), 'PNG')

os.remove(file_path)