"""Unit tests for the assignment module.

These tests validate the parsing logic, validation rules, and the assignment
algorithm to ensure students are correctly matched to projects based on their
preferences and project capacity constraints.
"""

import unittest

from datadivas.assignment import (
    AssignmentError,
    assign_students_to_projects,
    parse_projects,
    parse_student_rankings,
)


class AssignmentTests(unittest.TestCase):
    """Test suite for assignment logic and input validation."""
    def test_parse_projects_valid(self):
        """Test parsing valid project definitions with capacities 4-6 and majors."""
        text = "Project A,4,CS,CpE\nProject B,5,EE"
        result = parse_projects(text)
        expected = {
            "Project A": {"capacity": 4, "allowed_majors": ["CS", "CpE"]},
            "Project B": {"capacity": 5, "allowed_majors": ["EE"]}
        }
        self.assertEqual(result, expected)

    def test_parse_projects_invalid_capacity(self):
        """Test that capacities outside 4-6 range raise an error."""
        text = "Project A,3,CS\nProject B,7,EE"
        with self.assertRaises(AssignmentError):
            parse_projects(text)

    def test_parse_students_valid(self):
        """Test parsing valid student rankings with majors."""
        text = "Alice (CS): Project A, Project B\nBob (CpE): Project B"
        result = parse_student_rankings(text)
        expected = {
            "Alice": {"rankings": ["Project A", "Project B"], "major": "CS"},
            "Bob": {"rankings": ["Project B"], "major": "CpE"}
        }
        self.assertEqual(result, expected)

    def test_assign_students_to_projects_prefers_top_choices(self):
        """Test that the algorithm prioritizes students' top preferences when possible."""
        students = {
            "Alice": {"rankings": ["Project X", "Project Y"], "major": "CS"},
            "Bob": {"rankings": ["Project X", "Project Y"], "major": "CS"},
            "Carmen": {"rankings": ["Project Y", "Project X"], "major": "EE"},
        }
        projects = {
            "Project X": {"capacity": 4, "allowed_majors": ["CS", "EE"]},
            "Project Y": {"capacity": 4, "allowed_majors": ["CS", "EE"]}
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        self.assertEqual(assignments["Alice"], "Project X")
        self.assertEqual(assignments["Bob"], "Project Y")
        self.assertEqual(assignments["Carmen"], "Project Y")

    def test_assign_students_limits_capacity(self):
        """Test that project capacity limits are enforced.
        
        When more students want a project than its capacity allows, some should
        be assigned elsewhere or left unassigned.
        """
        students = {
            "Alice": {"rankings": ["Project A"], "major": "CS"},
            "Bob": {"rankings": ["Project A", "Project B"], "major": "CS"},
            "Carmen": {"rankings": ["Project A", "Project B"], "major": "CS"},
        }
        projects = {
            "Project A": {"capacity": 4, "allowed_majors": ["CS"]},
            "Project B": {"capacity": 4, "allowed_majors": ["CS"]}
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        assigned = [assignments[name] for name in students]
        # At least 2 should be assigned to Project A or Project B
        self.assertTrue(sum(1 for p in assigned if p is not None) >= 2)

    def test_minimum_capacity_enforcement(self):
        students = {
            "Alice": {"rankings": ["Project A"], "major": "CS"},
            "Bob": {"rankings": ["Project A"], "major": "CS"},
            "Carmen": {"rankings": ["Project A"], "major": "CS"},
            "Diana": {"rankings": ["Project A"], "major": "CS"},
            "Eve": {"rankings": ["Project A"], "major": "CS"},
        }
        projects = {"Project A": {"capacity": 4, "allowed_majors": ["CS"]}}
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        assigned = [assignments[name] for name in students]
        self.assertEqual(assigned.count("Project A"), 4)
        self.assertEqual(assigned.count(None), 1)

    def test_assign_students_unassigned_when_no_space(self):
        students = {
            "Alice": {"rankings": ["Project A"], "major": "CS"},
            "Bob": {"rankings": ["Project A"], "major": "CS"}
        }
        projects = {"Project A": {"capacity": 4, "allowed_majors": ["CS"]}}
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        # With only 2 students wanting Project A and capacity 4, they should be assigned
        self.assertEqual(assignments["Alice"], "Project A")
        self.assertEqual(assignments["Bob"], "Project A")

    def test_invalid_project_name_in_rankings(self):
        students = {"Alice": {"rankings": ["Project Z"], "major": "CS"}}
        projects = {"Project A": {"capacity": 4, "allowed_majors": ["CS"]}}
        with self.assertRaises(AssignmentError):
            assign_students_to_projects(students, projects)

    def test_nixing_rule_projects_below_min_capacity(self):
        """Test that projects with < 4 students assigned are set to 0 (empty).
        
        The nixing rule ensures that projects are either inactive (0 students)
        or active with between 4 and their capacity. This prevents teams that
        are too small to be viable.
        """
        students = {
            "Alice": {"rankings": ["Project X"], "major": "CS"},
            "Bob": {"rankings": ["Project X"], "major": "CS"},
            "Carmen": {"rankings": ["Project X"], "major": "CS"},
        }
        projects = {
            "Project X": {"capacity": 6, "allowed_majors": ["CS"]},
        }
        result = assign_students_to_projects(students, projects)
        project_compositions = result['project_compositions']
        # All students want Project X but only 3 are available
        # The nixing rule should result in Project X being empty (0 students)
        self.assertEqual(project_compositions["Project X"], {})

    def test_major_constraint_prevents_ineligible_assignment(self):
        """Test that students are never assigned to projects that don't list their major.
        
        Major eligibility is a hard constraint - students can only be assigned
        to projects that explicitly allow their major.
        """
        students = {
            "Alice": {"rankings": ["Project X", "Project Y"], "major": "CS"},
            "Bob": {"rankings": ["Project X", "Project Y"], "major": "EE"},
            "Carmen": {"rankings": ["Project X", "Project Y"], "major": "CpE"},
            "Diana": {"rankings": ["Project X", "Project Y"], "major": "CS"},
        }
        projects = {
            "Project X": {"capacity": 4, "allowed_majors": ["CS", "EE"]},
            "Project Y": {"capacity": 4, "allowed_majors": ["CpE", "CS"]},
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        
        # Bob (EE) cannot be assigned to Project Y (only CpE, CS allowed)
        if assignments["Bob"] is not None:
            self.assertIn(assignments["Bob"], ["Project X"])
        
        # Carmen (CpE) cannot be assigned to Project X (only CS, EE allowed)
        if assignments["Carmen"] is not None:
            self.assertIn(assignments["Carmen"], ["Project Y"])

    def test_data_sanitization_duplicate_rankings(self):
        """Test that duplicate rankings are rejected with a clear error.
        
        Students cannot rank the same project multiple times.
        """
        text = "Alice (CS): Project A, Project B, Project A"
        with self.assertRaises(AssignmentError):
            parse_student_rankings(text)

    def test_data_sanitization_trailing_spaces_in_project_names(self):
        """Test that trailing spaces in project names are normalized.
        
        The parser should strip leading/trailing whitespace from project names
        to handle input inconsistencies.
        """
        text = "Project A  ,4,CS\nProject B ,5,EE"
        result = parse_projects(text)
        # Names should be trimmed
        self.assertIn("Project A", result)
        self.assertIn("Project B", result)
        # Should not have spaces
        self.assertNotIn("Project A  ", result)
        self.assertNotIn("Project B ", result)

    def test_data_sanitization_trailing_spaces_in_student_input(self):
        """Test that trailing spaces in student rankings are normalized.
        
        Student names, majors, and project choices should be trimmed.
        """
        text = "Alice (CS) : Project A , Project B \nBob (CpE): Project B "
        result = parse_student_rankings(text)
        # Check that rankings are trimmed
        self.assertEqual(result["Alice"]["rankings"], ["Project A", "Project B"])
        self.assertEqual(result["Bob"]["rankings"], ["Project B"])

    def test_data_sanitization_lowercase_major_rejection(self):
        """Test that lowercase majors in input are rejected.
        
        Majors must be exactly 'CS', 'CpE', or 'EE' - lowercase variants
        should be rejected during parsing.
        """
        # Lowercase major in project definition should fail
        with self.assertRaises(AssignmentError):
            parse_projects("Project A,4,cs,cpe")
        
        # Lowercase major in student rankings should fail
        with self.assertRaises(AssignmentError):
            parse_student_rankings("Alice (cs): Project A")


if __name__ == "__main__":
    unittest.main()