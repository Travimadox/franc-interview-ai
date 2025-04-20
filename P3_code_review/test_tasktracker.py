#!/usr/bin/env python3
"""
Test Suite for Task Tracker Application

This module contains comprehensive tests for the Task Tracker application,
verifying all functional requirements are met.
"""
import unittest
import os
import json
import datetime
from unittest.mock import patch, MagicMock
import uuid
from io import StringIO
import sys

# Import the application module
import task_tracker as app

class TestTaskTracker(unittest.TestCase):
    """Test cases for Task Tracker application."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary tasks file for testing
        self.test_tasks_file = "test_tasks.json"
        app.TASKS_FILE = self.test_tasks_file
        app.tasks = {}
        
        # Sample task data for testing
        self.sample_task_id = "test-uuid-1234"
        self.sample_task = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": "incomplete",
            "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Create a controlled UUID for testing
        self.uuid_patch = patch('uuid.uuid4')
        self.mock_uuid = self.uuid_patch.start()
        self.mock_uuid.return_value = uuid.UUID(int=0)  # Predictable UUID

    def tearDown(self):
        """Clean up after each test."""
        # Stop UUID patch
        self.uuid_patch.stop()
        
        # Remove test tasks file if it exists
        if os.path.exists(self.test_tasks_file):
            os.remove(self.test_tasks_file)

    def write_test_tasks_file(self, tasks_data):
        """Helper method to write test tasks to file."""
        with open(self.test_tasks_file, 'w') as f:
            json.dump(tasks_data, f)

    # FR2.1, FR2.2: Test loading and saving tasks
    def test_load_tasks_empty_file(self):
        """Test loading tasks when file doesn't exist."""
        # Ensure file doesn't exist
        if os.path.exists(self.test_tasks_file):
            os.remove(self.test_tasks_file)
        
        app.load_tasks()
        
        # Verify empty tasks and file was created
        self.assertEqual(app.tasks, {})
        self.assertTrue(os.path.exists(self.test_tasks_file))

    def test_load_tasks_corrupted_file(self):
        """Test loading tasks from corrupted JSON file."""
        # Create a corrupted JSON file
        with open(self.test_tasks_file, 'w') as f:
            f.write("{invalid json")
        
        # Redirect stdout to capture print warnings
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.load_tasks()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify empty tasks and warning message
        self.assertEqual(app.tasks, {})
        self.assertIn("Warning: Tasks file is corrupted", captured_output.getvalue())

    def test_load_tasks_valid_file(self):
        """Test loading tasks from valid JSON file."""
        test_tasks = {"task1": self.sample_task}
        self.write_test_tasks_file(test_tasks)
        
        app.load_tasks()
        
        # Verify tasks were loaded correctly
        self.assertEqual(app.tasks, test_tasks)

    def test_save_tasks(self):
        """Test saving tasks to file."""
        app.tasks = {"task1": self.sample_task}
        app.save_tasks()
        
        # Verify file contains correct data
        with open(self.test_tasks_file, 'r') as f:
            loaded_tasks = json.load(f)
            self.assertEqual(loaded_tasks, app.tasks)

    def test_save_tasks_error_handling(self):
        """Test error handling when saving tasks fails."""
        app.tasks = {"task1": self.sample_task}
        
        # Mock open to raise IOError
        with patch('builtins.open', side_effect=IOError("Test error")):
            # Redirect stdout to capture print warnings
            captured_output = StringIO()
            sys.stdout = captured_output
            
            app.save_tasks()
            
            # Reset stdout
            sys.stdout = sys.__stdout__
            
            # Verify error message was printed
            self.assertIn("Error saving tasks", captured_output.getvalue())

    # FR1.2: Test task ID generation
    def test_generate_task_id(self):
        """Test unique task ID generation."""
        # Set up mock UUID
        self.mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        
        task_id = app.generate_task_id()
        self.assertEqual(task_id, "12345678-1234-5678-1234-567812345678")
        
        # Verify different UUIDs generate different IDs
        self.mock_uuid.return_value = uuid.UUID("87654321-4321-8765-4321-876543210987")
        new_task_id = app.generate_task_id()
        self.assertEqual(new_task_id, "87654321-4321-8765-4321-876543210987")
        self.assertNotEqual(task_id, new_task_id)

    # FR1.1, FR1.3: Test adding tasks
    @patch('builtins.input')
    def test_add_task_success(self, mock_input):
        """Test successfully adding a new task."""
        # Set up mock inputs for add_task
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        mock_input.side_effect = ["Test Title", "Test Description", tomorrow]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Set predictable UUID
        self.mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        
        app.add_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify task was added with correct properties
        task_id = "12345678-1234-5678-1234-567812345678"
        self.assertIn(task_id, app.tasks)
        self.assertEqual(app.tasks[task_id]["title"], "Test Title")
        self.assertEqual(app.tasks[task_id]["description"], "Test Description")
        self.assertEqual(app.tasks[task_id]["due_date"], tomorrow)
        self.assertEqual(app.tasks[task_id]["status"], "incomplete")
        self.assertIn("created_date", app.tasks[task_id])
        
        # Verify success message
        self.assertIn("added successfully", captured_output.getvalue())

    @patch('builtins.input')
    def test_add_task_empty_title(self, mock_input):
        """Test validation when adding task with empty title."""
        mock_input.side_effect = ["", "Test Description", "2023-12-31"]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.add_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify validation message and no task added
        self.assertIn("Title cannot be empty", captured_output.getvalue())
        self.assertEqual(app.tasks, {})

    @patch('builtins.input')
    def test_add_task_empty_description(self, mock_input):
        """Test validation when adding task with empty description."""
        mock_input.side_effect = ["Test Title", "", "2023-12-31"]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.add_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify validation message and no task added
        self.assertIn("Description cannot be empty", captured_output.getvalue())
        self.assertEqual(app.tasks, {})

    @patch('builtins.input')
    def test_add_task_invalid_date_format(self, mock_input):
        """Test validation when adding task with invalid date format."""
        mock_input.side_effect = ["Test Title", "Test Description", "invalid-date"]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.add_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify validation message and no task added
        self.assertIn("Invalid date format", captured_output.getvalue())
        self.assertEqual(app.tasks, {})

    @patch('builtins.input')
    def test_add_task_past_date(self, mock_input):
        """Test validation when adding task with past due date."""
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        mock_input.side_effect = ["Test Title", "Test Description", yesterday]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.add_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify validation message and no task added
        self.assertIn("Due date cannot be in the past", captured_output.getvalue())
        self.assertEqual(app.tasks, {})

    # FR1.4: Test viewing all tasks
    def test_view_all_tasks_empty(self):
        """Test viewing all tasks when no tasks exist."""
        app.tasks = {}
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.view_all_tasks()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify appropriate message
        self.assertIn("No tasks found", captured_output.getvalue())

    def test_view_all_tasks(self):
        """Test viewing all tasks with existing tasks."""
        # Set up sample tasks
        app.tasks = {
            "task1": self.sample_task,
            "task2": {
                "title": "Another Task",
                "description": "Another Description",
                "due_date": "2023-12-31",
                "status": "complete",
                "created_date": "2023-01-01 12:00:00"
            }
        }
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.view_all_tasks()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify output contains task information
        output = captured_output.getvalue()
        self.assertIn("Test Task", output)
        self.assertIn("Another Task", output)
        self.assertIn("incomplete", output)
        self.assertIn("complete", output)

    # FR1.5: Test viewing specific task
    @patch('builtins.input')
    def test_view_task_exists(self, mock_input):
        """Test viewing details of an existing task."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task}
        mock_input.return_value = task_id
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.view_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify output contains task details
        output = captured_output.getvalue()
        self.assertIn("Test Task", output)
        self.assertIn("Test Description", output)
        self.assertIn(self.sample_task["due_date"], output)
        self.assertIn("incomplete", output)

    @patch('builtins.input')
    def test_view_task_not_found(self, mock_input):
        """Test viewing a non-existent task."""
        app.tasks = {}
        mock_input.return_value = "nonexistent-id"
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.view_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify error message
        self.assertIn("not found", captured_output.getvalue())

    # FR1.6: Test updating task
    @patch('builtins.input')
    def test_update_task_success(self, mock_input):
        """Test successfully updating a task."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task.copy()}
        
        # Mock user inputs (leave description empty to keep current value)
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        mock_input.side_effect = [task_id, "Updated Title", "", tomorrow]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.update_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify task was updated properly
        updated_task = app.tasks[task_id]
        self.assertEqual(updated_task["title"], "Updated Title")
        self.assertEqual(updated_task["description"], "Test Description")  # Should be unchanged
        self.assertEqual(updated_task["due_date"], tomorrow)
        
        # Verify success message
        self.assertIn("updated successfully", captured_output.getvalue())

    @patch('builtins.input')
    def test_update_task_not_found(self, mock_input):
        """Test updating a non-existent task."""
        app.tasks = {}
        mock_input.return_value = "nonexistent-id"
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.update_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify error message
        self.assertIn("not found", captured_output.getvalue())

    @patch('builtins.input')
    def test_update_task_invalid_date(self, mock_input):
        """Test updating task with invalid date format."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task.copy()}
        
        # Mock inputs with invalid date
        mock_input.side_effect = [task_id, "Updated Title", "Updated Description", "invalid-date"]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.update_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify validation message and task not updated
        self.assertIn("Invalid date format", captured_output.getvalue())
        self.assertEqual(app.tasks[task_id]["title"], "Test Task")  # Should be unchanged

    @patch('builtins.input')
    def test_update_task_past_date(self, mock_input):
        """Test updating task with past due date."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task.copy()}
        
        # Mock inputs with past date
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        mock_input.side_effect = [task_id, "Updated Title", "Updated Description", yesterday]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.update_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify validation message and task not updated
        self.assertIn("Due date cannot be in the past", captured_output.getvalue())
        self.assertEqual(app.tasks[task_id]["title"], "Test Task")  # Should be unchanged

    # FR1.7: Test marking task as complete
    @patch('builtins.input')
    def test_mark_task_complete(self, mock_input):
        """Test marking a task as complete."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task.copy()}
        mock_input.return_value = task_id
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.mark_task_complete()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify task status was updated
        self.assertEqual(app.tasks[task_id]["status"], "complete")
        
        # Verify success message
        self.assertIn("marked as complete", captured_output.getvalue())

    @patch('builtins.input')
    def test_mark_task_complete_not_found(self, mock_input):
        """Test marking a non-existent task as complete."""
        app.tasks = {}
        mock_input.return_value = "nonexistent-id"
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.mark_task_complete()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify error message
        self.assertIn("not found", captured_output.getvalue())

    # FR1.8: Test deleting task
    @patch('builtins.input')
    def test_delete_task_confirmed(self, mock_input):
        """Test deleting a task with confirmation."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task.copy()}
        mock_input.side_effect = [task_id, "y"]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.delete_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify task was deleted
        self.assertNotIn(task_id, app.tasks)
        
        # Verify success message
        self.assertIn("deleted successfully", captured_output.getvalue())

    @patch('builtins.input')
    def test_delete_task_cancelled(self, mock_input):
        """Test cancelling task deletion."""
        # Set up sample task
        task_id = "test-uuid-1234"
        app.tasks = {task_id: self.sample_task.copy()}
        mock_input.side_effect = [task_id, "n"]
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.delete_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify task was not deleted
        self.assertIn(task_id, app.tasks)
        
        # Verify cancellation message
        self.assertIn("cancelled", captured_output.getvalue())

    @patch('builtins.input')
    def test_delete_task_not_found(self, mock_input):
        """Test deleting a non-existent task."""
        app.tasks = {}
        mock_input.return_value = "nonexistent-id"
        
        # Redirect stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        app.delete_task()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify error message
        self.assertIn("not found", captured_output.getvalue())

    # Test main menu functionality
    @patch('builtins.input')
    def test_main_menu_invalid_choice(self, mock_input):
        """Test handling of invalid menu choices."""
        # Mock load_tasks to do nothing
        with patch('task_tracker.load_tasks'):
            # Set up inputs: invalid choice, then exit
            mock_input.side_effect = ["invalid", "7"]
            
            # Redirect stdout
            captured_output = StringIO()
            sys.stdout = captured_output
            
            app.main()
            
            # Reset stdout
            sys.stdout = sys.__stdout__
            
            # Verify error message
            self.assertIn("Invalid choice", captured_output.getvalue())

    @patch('builtins.input')
    def test_main_menu_exit(self, mock_input):
        """Test exiting the application."""
        # Mock load_tasks to do nothing
        with patch('task_tracker.load_tasks'):
            # Set up input to exit
            mock_input.return_value = "7"
            
            # Redirect stdout
            captured_output = StringIO()
            sys.stdout = captured_output
            
            app.main()
            
            # Reset stdout
            sys.stdout = sys.__stdout__
            
            # Verify exit message
            self.assertIn("Exiting Task Tracker", captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()