__author__ = 'Evan Murawski'

import unittest
import backend
from backend.interactions import *
from backend.beam import Beam
import backend.solver as solver
from backend.solver import SolverError
import backend.shearmomentgenerator as shearmomentgenerator
from backend.shearmomentgenerator import Shear_Moment_Error
import matplotlib.pyplot as plt
import numpy as np

class TestBeamAnalyzer(unittest.TestCase):
    """Unit tests for the backend."""
    
    ALMOST = 0.01
    beams = []
    STEP_SIZE = 0.001

    def setUp(self):
        """Setup the tests. Creates various beams with known solutions and force moment plots."""

        self.beams = []
        self.beams.append(Beam(10))

        self.beams[0].add_interaction(Force(5, -10))
        self.beams[0].add_interaction(Force(0, 0, False))
        self.beams[0].add_interaction(Force(10, 0, False))

        self.beams.append(Beam(5.5))

        self.beams[1].add_interaction(Force(0, 0, False))
        self.beams[1].add_interaction(Moment(0, 0, False))
        self.beams[1].add_interaction(Force(5.5, 10))
        self.beams[1].add_interaction(Moment(4, 40))

        self.beams.append(Beam(30))

        self.beams[2].add_interaction(Force(0, 0, False))
        self.beams[2].add_interaction(Force(20, 0, False))
        self.beams[2].add_interaction(Dist_Force(0, -1, 10))
        self.beams[2].add_interaction(Force(15, -20))
        self.beams[2].add_interaction(Force(30, -10))

        self.beams.append(Beam(10))

        self.beams[3].add_interaction(Force(1, 7))
        self.beams[3].add_interaction(Dist_Force(2, -5, 7))
        self.beams[3].add_interaction(Moment(8, 10))
        self.beams[3].add_interaction(Force(8, 0, False))
        self.beams[3].add_interaction(Moment(0, 0, False))


    #A very simple beam with one known force and two unknown forces
    def test_beam0(self):

        solver.solve(self.beams[0])

        #Test solution
        self.assertEqual(5, self.beams[0].interactions[0].magnitude)
        self.assertEqual(5, self.beams[0].interactions[2].magnitude)
        
        shear_moment = shearmomentgenerator.generate_numerical(self.beams[0], self.STEP_SIZE)

        #Test moment
        assert abs(shear_moment[0][1] - 0 ) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE/2)][1] - 25) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE/4)][1] - 25/2) < self.ALMOST

        #Test shear
        assert abs(shear_moment[1][0] - 5) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE/2) -1][0] - 5 ) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE/2) +2][0] - (-5)) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE) -1][0] - (-5)) < self.ALMOST

    def test_beam1(self):
        solver.solve(self.beams[1])

        #Test solution
        self.assertEqual(-10, self.beams[1].interactions[0].magnitude)
        self.assertEqual(-95, self.beams[1].interactions[1].magnitude)

        shear_moment = shearmomentgenerator.generate_numerical(self.beams[1], self.STEP_SIZE)

        #Test shear
        for item in shear_moment:
            assert abs(item[0] - (-10)) < self.ALMOST

        #Test moment
        assert abs(shear_moment[0][1] - 95) < self.ALMOST
        assert abs(shear_moment[int(4/self.STEP_SIZE - 1)][1] - 55 ) < self.ALMOST
        assert abs(shear_moment[int(5.5/self.STEP_SIZE) - 1][1] - 0) < self.ALMOST

    def test_beam2(self):
        solver.solve(self.beams[2])

        #Test the solution
        self.assertEqual(7.5, self.beams[2].interactions[0].magnitude)
        self.assertEqual(32.5, self.beams[2].interactions[3].magnitude)

        shear_moment = shearmomentgenerator.generate_numerical(self.beams[2], self.STEP_SIZE)

        #Test shear
        assert abs(shear_moment[0][0] - 7.5) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE)][0] - (-2.5)) < self.ALMOST
        assert abs(shear_moment[int(15/self.STEP_SIZE) - 1][0] - (-2.5)) < self.ALMOST
        assert abs(shear_moment[int(15/self.STEP_SIZE) + 1][0] - (-22.5)) < self.ALMOST
        assert abs(shear_moment[int(20/self.STEP_SIZE) - 1][0] - (-22.5)) < self.ALMOST
        assert abs(shear_moment[int(20/self.STEP_SIZE) + 1][0] - (10)) < self.ALMOST

        #Test moment
        assert abs(shear_moment[0][1] - 0) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE)][1] - 25) < self.ALMOST
        assert abs(shear_moment[int(15/self.STEP_SIZE)][1] - 12.5) < self.ALMOST
        assert abs(shear_moment[int(20/self.STEP_SIZE)][1] - (-100)) < self.ALMOST
        assert abs(shear_moment[int(30/self.STEP_SIZE) -1][1] - 0) < self.ALMOST

    def test_beam3(self):
        solver.solve(self.beams[3])

        #Test the solution
        self.assertEqual(-48.5, self.beams[3].interactions[0].magnitude)
        self.assertEqual(18, self.beams[3].interactions[4].magnitude)

        shear_moment = shearmomentgenerator.generate_numerical(self.beams[3], self.STEP_SIZE)

        #Test shear
        assert abs(shear_moment[0][0] - 0) < self.ALMOST
        assert abs(shear_moment[int(1/self.STEP_SIZE) -1][0] - 0) < self.ALMOST
        assert abs(shear_moment[int(1/self.STEP_SIZE) + 1][0] - 7) < self.ALMOST
        assert abs(shear_moment[int(2/self.STEP_SIZE) -1][0] - 7) < self.ALMOST
        assert abs(shear_moment[int(7/self.STEP_SIZE) +1][0] - (-18)) < self.ALMOST
        assert abs(shear_moment[int(8/self.STEP_SIZE) -1][0] - (-18)) < self.ALMOST
        assert abs(shear_moment[int(8/self.STEP_SIZE) +1][0] - (0)) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE) -1][0] - (0)) < self.ALMOST

        #Test moment
        assert abs(shear_moment[0][1] - 48.5) < self.ALMOST
        assert abs(shear_moment[int(1/self.STEP_SIZE) - 1][1] - 48.5) < self.ALMOST
        
        #Had to decrease criteria due to steep slope
        assert abs(shear_moment[int(8/self.STEP_SIZE) - 1][1] - 10) < 0.02
        assert abs(shear_moment[int(8/self.STEP_SIZE) +1][1] - 0) < self.ALMOST
        assert abs(shear_moment[int(10/self.STEP_SIZE) -1][1] - 0) < self.ALMOST

 
    def test_interaction_location_error(self):

        with self.assertRaises(InteractionLocationError):
            Force(-1, 3)

        with self.assertRaises(InteractionLocationError):
            self.beams[0].add_interaction(Force(13, 3))

    def test_solver_error(self):

        self.beams[0].add_interaction(Force(3, 0, False))

        with self.assertRaises(SolverError):
            solver.solve(self.beams[0])

    def test_shear_moment_error(self):

        with self.assertRaises(Shear_Moment_Error):
            shearmomentgenerator.generate_numerical(self.beams[0], self.STEP_SIZE)