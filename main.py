import logging
import time
from center_finder import CenterFinder
from genetic.genetics import GeneticAlgorithm
from gui.drawers.matplot import MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D
import input.input_source
from gui.point import Point

logging.getLogger().setLevel(logging.INFO)
in_source = input.input_source.TxtFileInput("./sample.txt")
finder = CenterFinder(in_source, GeneticAlgorithm())
finder.draw_target_points()
finder.draw_current_points()
end_flag, res_point = finder.check_end_condition()
print('End flag is:', end_flag)

time.sleep(60)
