#!/usr/bin/python3
import os
import math
from GCodeLib import gcode_lib

# ------------------------------------------------------------------------------
                                                               # things to drill
show_bounding_box = True
drill_fixing_holes = True
drill_ventilation_slits = True
    
# ------------------------------------------------------------------------------
                                                           # drilling parameters
board_thickness = 6
board_drill_depth = board_thickness + 3
drill_diameter = 4
fast_displacement_speed = 1000
drill_displacement_speed = 250

machining_parameters = {
    'displacement_height'      : 10,
    'drill_depth'              : board_drill_depth,
    'pass_depth'               : 1,
    'drill_diameter'           : drill_diameter,
    'fast_displacement_speed'  : fast_displacement_speed,
    'drill_displacement_speed' : drill_displacement_speed,
    'drill_bore_speed'         : 100
}

# ------------------------------------------------------------------------------
                                                                      # geometry
box_length = 210
box_width  = 148
box_height  = 80

board_length = box_length
board_width  = box_width - board_thickness

fixing_holes_x_offset = board_thickness/2
fixing_holes_y_offset = 22
fixing_holes_length = board_length - 2*fixing_holes_x_offset
fixing_holes_width = board_width - 2*fixing_holes_y_offset + board_thickness

ventilation_slits_x_offset = 21
ventilation_slits_y_offset = 16
ventilation_slits_y_spacing = 16
ventilation_slits_length = 41
ventilation_slits_width = drill_diameter
ventilation_slits_spacing = 2*ventilation_slits_width
ventilation_slit_nb = 22

# ------------------------------------------------------------------------------
                                                                     # file spec
(g_code_file_path, g_code_file_name) = os.path.split(__file__)
g_code_file_path = g_code_file_path.rstrip('./')
design_name = g_code_file_name.replace('.py', '')
g_code_file_name = g_code_file_path + os.sep + design_name + '.gcode'

# ------------------------------------------------------------------------------
                                                                       # display
INDENT = 2 * ' '

# ==============================================================================
                                                                   # main script
print('Building g-codes for the A4 box top plate')

# ------------------------------------------------------------------------------
                                                           # write g-code header
print(INDENT + "Writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters
))

comment = "A4 top plate"
g_code_file.write(";\n; %s\n" % comment)
print(INDENT + comment)

# ------------------------------------------------------------------------------
                                                                   # board shape
if show_bounding_box :
    comment = "shape"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n;\n" % comment)
    g_code_file.write(gcode_lib.rectangle_gcode(
        board_length, board_width, fast_displacement_speed
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                  # fixing holes
if drill_fixing_holes :
    comment = "fixing holes"
    print(2*INDENT + comment)
                                                                       # 4 holes
    g_code_file.write(gcode_lib.build_hole_set(
        gcode_lib.build_retangle(
            fixing_holes_x_offset, fixing_holes_y_offset - board_thickness,
            fixing_holes_length, fixing_holes_width
        ),
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                             # ventilation slits
if drill_ventilation_slits :
    comment = 'ventilation slits'
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n;\n" % comment)
                                                               # bottom slit set
    g_code_file.write(gcode_lib.build_slit_set(
		ventilation_slits_x_offset, ventilation_slits_y_offset,
		0, ventilation_slits_length, ventilation_slits_spacing, 0,
        ventilation_slit_nb,
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())
                                                                  # top slit set
    g_code_file.write(gcode_lib.build_slit_set(
		ventilation_slits_x_offset,
		board_width - ventilation_slits_y_offset
			- ventilation_slits_length - board_thickness,
		0, ventilation_slits_length, ventilation_slits_spacing, 0,
        ventilation_slit_nb,
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()
